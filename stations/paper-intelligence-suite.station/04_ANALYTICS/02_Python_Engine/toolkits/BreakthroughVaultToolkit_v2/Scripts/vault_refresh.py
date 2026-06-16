
"""
vault_refresh.py
Scans a vault directory for .md files, extracts basic metadata, YAML frontmatter (best-effort),
and populates a local SQLite database (notes, concepts, co_mentions scaffold).
Pure standard library.
"""

import os, re, sqlite3, hashlib, datetime
from pathlib import Path
from typing import Dict, Tuple, List, Optional

DB_NAME = "coherence.db"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TITLE_RE = re.compile(r"^\s*#\s+(.*)$", re.MULTILINE)

def sha1_text(txt: str) -> str:
    return hashlib.sha1(txt.encode("utf-8", errors="ignore")).hexdigest()

def parse_frontmatter(md: str) -> Dict:
    """
    Minimal YAML-ish parser (no dependency). Key: value and simple lists only.
    """
    m = FRONTMATTER_RE.match(md)
    if not m:
        return {}
    blob = m.group(1)
    data = {}
    current_key = None
    for line in blob.splitlines():
        if re.match(r"^\s*#", line):  # comment
            continue
        kv = re.match(r"^\s*([A-Za-z0-9_\-]+)\s*:\s*(.*)\s*$", line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                # list like [a, b, c]
                items = [x.strip().strip(",") for x in val[1:-1].split(",") if x.strip()]
                data[key] = items
            elif val == "" or val == "|":
                data[key] = ""
                current_key = key
            else:
                data[key] = val
                current_key = key if val.endswith("|") else None
        elif current_key:
            data[current_key] = (data.get(current_key,"") + "\n" + line).strip()
    return data

def extract_title(md: str) -> str:
    m = TITLE_RE.search(md)
    return m.group(1).strip() if m else ""

def ensure_db(db_path: Path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS notes(
        uid TEXT PRIMARY KEY,
        title TEXT,
        path TEXT,
        domain TEXT,
        tags TEXT,
        word_count INTEGER,
        hash TEXT,
        updated_at TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS concepts(
        concept TEXT PRIMARY KEY,
        mentions INTEGER DEFAULT 0
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS co_mentions(
        concept1 TEXT,
        concept2 TEXT,
        count INTEGER,
        PRIMARY KEY(concept1, concept2)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS edges(
        src TEXT, dst TEXT, rel TEXT, weight REAL,
        PRIMARY KEY (src, dst, rel)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS metrics(
        uid TEXT PRIMARY KEY, SIS REAL, LCS REAL, SRI REAL
    )""")
    con.commit()
    con.close()

def upsert_note(db_path: Path, row: Tuple):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""INSERT INTO notes(uid,title,path,domain,tags,word_count,hash,updated_at)
                   VALUES (?,?,?,?,?,?,?,?)
                   ON CONFLICT(uid) DO UPDATE SET
                      title=excluded.title,
                      path=excluded.path,
                      domain=excluded.domain,
                      tags=excluded.tags,
                      word_count=excluded.word_count,
                      hash=excluded.hash,
                      updated_at=excluded.updated_at""", row)
    con.commit()
    con.close()

def add_concepts(db_path: Path, concepts: List[str]):
    if not concepts:
        return
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    for c in concepts:
        cur.execute("""INSERT INTO concepts(concept, mentions) VALUES (?,1)
                       ON CONFLICT(concept) DO UPDATE SET mentions = mentions + 1""", (c,))
    con.commit()
    con.close()

def words_count(md: str) -> int:
    body = re.sub(FRONTMATTER_RE, "", md)
    body = re.sub(r"`[^`]+`", " ", body)  # strip code spans
    body = re.sub(r"\[\[.*?\]\]", " ", body)  # strip wiki links for count
    tokens = re.findall(r"[A-Za-z0-9']+", body)
    return len(tokens)

def discover_concepts(front: Dict, title: str, md: str) -> List[str]:
    concepts = []
    # from tags
    tags = front.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    concepts += [t for t in tags if t]
    # from explicit "concepts" key
    extra = front.get("concepts", [])
    if isinstance(extra, str):
        extra = [t.strip() for t in extra.split(",") if t.strip()]
    concepts += [t for t in extra if t]
    # naive pull from title capitalized words
    caps = re.findall(r"\b([A-Z][a-zA-Z\-]{2,})\b", title)
    concepts += caps
    # normalize
    norm = []
    seen = set()
    for c in concepts:
        cc = re.sub(r'[^A-Za-z0-9\-]+', '-', c.strip()).strip('-').lower()
        if cc and cc not in seen:
            seen.add(cc); norm.append(cc)
    return norm

def scan_vault(vault_dir: Path, db_path: Path, uid_strategy: str = "path"):
    ensure_db(db_path)
    n_files = 0
    for root, _, files in os.walk(vault_dir):
        for f in files:
            if not f.lower().endswith(".md"):
                continue
            p = Path(root) / f
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                try:
                    text = p.read_text(encoding="latin-1")
                except Exception:
                    continue
            front = parse_frontmatter(text)
            title = front.get("title") or extract_title(text) or p.stem
            domain = (front.get("domain") or front.get("layer") or "meta").lower()
            tags = front.get("tags", [])
            if isinstance(tags, list):
                tags_str = ",".join(tags)
            else:
                tags_str = str(tags)
            wc = words_count(text)
            h = sha1_text(text)
            # UID: prefer existing, else derive from path
            uid = front.get("uid")
            if not uid:
                parts = [s for s in p.relative_to(vault_dir).parts if s]
                uid = "UID-" + "-".join(re.sub(r'[^A-Za-z0-9]+','',x)[:8].upper() for x in parts)
            updated = datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds")
            upsert_note(db_path, (uid, title, str(p), domain, tags_str, wc, h, updated))
            # concepts
            concepts = discover_concepts(front, title, text)
            add_concepts(db_path, concepts)
            n_files += 1
    return n_files

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Scan vault and refresh local coherence.db")
    ap.add_argument("--vault", required=True, help="Path to Obsidian vault root")
    ap.add_argument("--db", default=str(Path(__file__).resolve().parent.parent / "Data" / "coherence.db"))
    args = ap.parse_args()
    count = scan_vault(Path(args.vault), Path(args.db))
    print(f"Indexed {count} markdown files into {args.db}")

if __name__ == "__main__":
    main()
