
"""
duplicate_finder.py
Finds exact and near-duplicate notes.
- Exact duplicates: SHA1 hash collision on content (already stored in notes.hash)
- Near duplicates: SequenceMatcher ratio on normalized text (0..1), user sets threshold (0..100%)
Writes Data/duplicate_report.csv and populates duplicates table.
"""

import sqlite3, re, csv
from pathlib import Path
from difflib import SequenceMatcher

def normalize(text: str) -> str:
    text = re.sub(r"^---\s*[\s\S]*?---\s*", "", text.strip(), flags=re.M)  # strip frontmatter
    text = re.sub(r"\[\[.*?\]\]", " ", text)  # strip wikilinks
    text = re.sub(r"`[^`]+`", " ", text)  # strip code
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()

def load_notes(db_path: Path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT uid, title, path, hash FROM notes")
    notes = cur.fetchall()
    con.close()
    return notes

def read_file(path: str) -> str:
    p = Path(path)
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        try:
            return p.read_text(encoding="latin-1")
        except Exception:
            return ""

def ensure_table(db_path: Path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS duplicates(
        uid1 TEXT, uid2 TEXT, similarity REAL, exact INTEGER,
        PRIMARY KEY(uid1, uid2)
    )""")
    con.commit(); con.close()

def find_duplicates(db_path: Path, sim_threshold: float = 0.8, limit_pairs:int=200000):
    ensure_table(db_path)
    notes = load_notes(db_path)
    # Build exact-hash groups
    by_hash = {}
    for uid, title, path, h in notes:
        by_hash.setdefault(h, []).append((uid,title,path))
    exact_pairs = []
    for h, group in by_hash.items():
        if len(group) > 1:
            for i in range(len(group)):
                for j in range(i+1, len(group)):
                    exact_pairs.append((group[i], group[j]))

    # Near-duplicates via SequenceMatcher on normalized text
    # To avoid O(N^2) blowup at 40k, we do a cheap blocking by first 12 chars of normalized text.
    blocks = {}
    normalized_cache = {}
    for uid, title, path, h in notes:
        txt = read_file(path)
        norm = normalize(txt)
        normalized_cache[uid] = norm
        key = norm[:12]
        blocks.setdefault(key, []).append((uid,title,path))

    near_pairs = []
    # Compare within blocks
    for key, group in blocks.items():
        n = len(group)
        for i in range(n):
            uid1, t1, p1 = group[i]
            for j in range(i+1, n):
                uid2, t2, p2 = group[j]
                a = normalized_cache.get(uid1,"")
                b = normalized_cache.get(uid2,"")
                if not a or not b:
                    continue
                sim = SequenceMatcher(None, a, b).ratio()
                if sim >= sim_threshold:
                    near_pairs.append(((uid1,t1,p1),(uid2,t2,p2), sim))
                if len(near_pairs) > limit_pairs:
                    break

    # Write DB + CSV
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("DELETE FROM duplicates")
    for (u1,t1,p1),(u2,t2,p2) in exact_pairs:
        cur.execute("INSERT OR REPLACE INTO duplicates(uid1,uid2,similarity,exact) VALUES (?,?,?,1)", (u1,u2,1.0))
    for (u1,t1,p1),(u2,t2,p2), sim in near_pairs:
        cur.execute("INSERT OR REPLACE INTO duplicates(uid1,uid2,similarity,exact) VALUES (?,?,?,0)", (u1,u2,sim))
    con.commit(); con.close()

    # CSV report
    out_csv = db_path.parent.parent / "Data" / "duplicate_report.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["uid1","uid2","similarity","exact"])
        for (u1,t1,p1),(u2,t2,p2) in exact_pairs:
            w.writerow([u1,u2,1.0,1])
        for (u1,t1,p1),(u2,t2,p2), sim in near_pairs:
            w.writerow([u1,u2,round(sim,4),0])
    return len(exact_pairs), len(near_pairs), str(out_csv)

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Duplicate Finder")
    ap.add_argument("--db", required=False, default=str(Path(__file__).resolve().parent.parent / "Data" / "coherence.db"))
    ap.add_argument("--threshold", type=float, default=0.8, help="Near-duplicate threshold (0.0 - 1.0). Suggest 0.75–0.9")
    args = ap.parse_args()
    e, n, path = find_duplicates(Path(args.db), args.threshold)
    print(f"Exact duplicates: {e}, Near-duplicates: {n}\nReport: {path}")

if __name__ == "__main__":
    main()
