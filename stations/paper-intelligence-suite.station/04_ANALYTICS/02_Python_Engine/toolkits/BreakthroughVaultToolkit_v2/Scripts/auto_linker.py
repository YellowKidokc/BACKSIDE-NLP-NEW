
"""
auto_linker.py
Generates Obsidian links and typed relationships:
- supports / contradicts / analogy / related
Heuristics (v1, pure Python):
- Tag overlap → 'related' (and possibly 'supports' if high overlap)
- Title cues ('not', 'vs', 'rebuttal') → 'contradicts'
- 'as', 'like', 'analogy' in title → 'analogy'
Writes to DB (edges) and can optionally update YAML frontmatter links.
"""

import re, sqlite3, json
from pathlib import Path

def jaccard(a:set,b:set)->float:
    if not a and not b: return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter/union if union else 0.0

def load_notes(db_path: Path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT uid, title, path, domain, tags FROM notes")
    rows = cur.fetchall()
    con.close()
    return rows

def infer_relation(title_a:str, title_b:str, tags_a:set, tags_b:set, j:float) -> str:
    t = (title_a + " " + title_b).lower()
    if re.search(r"\b(rebuttal|refute|against|versus|vs\.?)\b", t):
        return "contradicts"
    if re.search(r"\b(as|like|analogy|metaphor)\b", t):
        return "analogy"
    # strong tag overlap suggests support
    if j >= 0.66:
        return "supports"
    if j >= 0.33:
        return "related"
    return ""

def write_edges(db_path: Path, edges):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("DELETE FROM edges")
    for src, dst, rel, weight in edges:
        cur.execute("INSERT OR REPLACE INTO edges(src,dst,rel,weight) VALUES (?,?,?,?)", (src,dst,rel,weight))
    con.commit(); con.close()

def update_yaml_links(path: Path, relmap: dict, use_wikilinks=True):
    """
    relmap: {"supports":[["UID1","Title1"]...], "contradicts":[...], "analogy":[...]}
    Appends to YAML frontmatter blocks if keys exist; otherwise, inserts a Links section at end.
    Minimal invasive: we don't parse heavy YAML—just append a block at bottom.
    """
    try:
        txt = path.read_text(encoding="utf-8")
    except Exception:
        return False
    # Build link lines
    def link_s(title): 
        return f"[[{title}]]" if use_wikilinks else f"[{title}]({title.replace(' ','%20')}.md)"
    blocks = []
    for k, items in relmap.items():
        if not items: continue
        lst = "\n".join([f"  - {link_s(title)}" for uid,title in items])
        blocks.append(f"{k}:\n{lst}")
    if not blocks: 
        return False
    addition = "\n\n---\n# Auto Links (generated)\n" + "\n".join(blocks) + "\n"
    txt = txt + addition
    path.write_text(txt, encoding="utf-8")
    return True

def run(db_path: Path, write_yaml: bool = False, wikilinks: bool = True, min_jaccard: float = 0.33):
    rows = load_notes(db_path)
    # Precompute tag sets
    info = []
    for uid, title, path, domain, tags in rows:
        tagset = set([t.strip().lower() for t in (tags or "").split(",") if t.strip()])
        info.append((uid, title, Path(path), domain, tagset))
    edges = []
    # simple N^2 for modest sets; for 40k we would block by common tags
    for i in range(len(info)):
        uid_a, title_a, path_a, dom_a, tags_a = info[i]
        for j in range(i+1, len(info)):
            uid_b, title_b, path_b, dom_b, tags_b = info[j]
            jacc = jaccard(tags_a, tags_b)
            if jacc < min_jaccard:
                continue
            rel = infer_relation(title_a, title_b, tags_a, tags_b, jacc)
            if not rel:
                continue
            weight = jacc
            edges.append((uid_a, uid_b, rel, weight))
            edges.append((uid_b, uid_a, rel, weight))
            if write_yaml:
                # Update both notes with reciprocal links
                relmap_a = {rel:[(uid_b, title_b)]}
                relmap_b = {rel:[(uid_a, title_a)]}
                update_yaml_links(path_a, relmap_a, wikilinks)
                update_yaml_links(path_b, relmap_b, wikilinks)
    write_edges(db_path, edges)
    return len(edges)

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Auto Linker")
    ap.add_argument("--db", default=str(Path(__file__).resolve().parent.parent / "Data" / "coherence.db"))
    ap.add_argument("--write-yaml", action="store_true", help="Append links into note files")
    ap.add_argument("--markdown-links", action="store_true", help="Use Markdown links instead of wikilinks")
    ap.add_argument("--min-jaccard", type=float, default=0.33, help="Minimum tag-overlap Jaccard to consider")
    args = ap.parse_args()
    n = run(Path(args.db), write_yaml=args.write_yaml, wikilinks=not args.markdown_links, min_jaccard=args.min_jaccard)
    print(f"Wrote {n} edges (DB); YAML updated: {args.write_yaml}")

if __name__ == "__main__":
    main()
