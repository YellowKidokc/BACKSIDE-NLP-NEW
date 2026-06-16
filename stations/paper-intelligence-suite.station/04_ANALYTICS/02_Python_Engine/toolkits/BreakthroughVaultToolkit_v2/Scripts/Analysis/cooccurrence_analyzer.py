
"""
cooccurrence_analyzer.py
Computes co-mentions (simple statistical co-occurrence) from tags/concepts per note.
"""

import sqlite3
from pathlib import Path
import itertools

def compute(db_path: Path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    # Reconstruct per-note concept sets from notes.tags (comma-separated) and title heuristics are already counted into 'concepts' table for global stats,
    # but for co-occurrence we approximate using tags only for now (pure-Python v1).
    cur.execute("SELECT uid, tags FROM notes")
    rows = cur.fetchall()
    pairs = {}
    for uid, tags in rows:
        if not tags:
            continue
        items = [t.strip().lower() for t in tags.split(",") if t.strip()]
        items = sorted(set(items))
        for a, b in itertools.combinations(items, 2):
            key = (a,b)
            pairs[key] = pairs.get(key, 0) + 1
    # write
    cur.execute("DELETE FROM co_mentions")
    for (a,b), c in pairs.items():
        cur.execute("INSERT INTO co_mentions(concept1, concept2, count) VALUES (?,?,?)", (a,b,c))
    con.commit()
    con.close()

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Compute co-mentions from tags")
    ap.add_argument("--db", default=str(Path(__file__).resolve().parent.parent / "08_Database" / "theophysics.db"))
    args = ap.parse_args()
    compute(Path(args.db))
    print(f"co_mentions updated in {args.db}")

if __name__ == "__main__":
    main()
