
"""
validation_scaffold.py
Computes simple placeholder metrics:
- SIS (Semantic Integrity Score): average tag Jaccard with neighbors (proxy for internal coherence)
- LCS (Logical Consistency Score): 1 - (contradicts edges / all typed edges)
- SRI (Scar Resolution Index): placeholder = supports / (supports + contradicts), until 'scars' are tracked
Writes to metrics table and a Markdown dashboard.
"""

import sqlite3, math, datetime
from pathlib import Path
from collections import defaultdict

def compute(db_path: Path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    # Build tag sets
    cur.execute("SELECT uid, tags FROM notes")
    tagmap = {uid:set([t.strip().lower() for t in (tags or '').split(',') if t.strip()]) for uid,tags in cur.fetchall()}
    # Collect edges
    cur.execute("SELECT src, dst, rel, weight FROM edges")
    edges = cur.fetchall()

    neighbors = defaultdict(list)
    counts = defaultdict(lambda: {"supports":0,"contradicts":0,"analogy":0,"related":0})
    for s,d,rel,w in edges:
        neighbors[s].append(d)
        counts[s][rel] = counts[s].get(rel,0)+1

    # SIS: avg Jaccard with neighbors
    def jaccard(a:set,b:set)->float:
        if not a and not b: return 0.0
        inter = len(a & b); union = len(a | b)
        return inter/union if union else 0.0

    metrics = {}
    for uid in tagmap:
        nbrs = neighbors.get(uid, [])
        if nbrs:
            sis = sum(jaccard(tagmap.get(uid,set()), tagmap.get(n,set())) for n in nbrs) / len(nbrs)
        else:
            sis = 0.0
        total_typed = sum(counts[uid].values())
        contradicts = counts[uid].get("contradicts",0)
        supports = counts[uid].get("supports",0)
        lcs = 1.0 - (contradicts / total_typed) if total_typed else 1.0
        sri = (supports / (supports + contradicts)) if (supports + contradicts)>0 else None
        metrics[uid] = (sis, lcs, sri)

    # write to DB
    cur.execute("DELETE FROM metrics")
    for uid, (sis, lcs, sri) in metrics.items():
        cur.execute("INSERT OR REPLACE INTO metrics(uid,SIS,LCS,SRI) VALUES (?,?,?,?)",
                    (uid, round(sis,4), round(lcs,4), None if sri is None else round(sri,4)))
    con.commit()

    # dashboard
    dashboard = db_path.parent.parent / "Dashboards"
    dashboard.mkdir(parents=True, exist_ok=True)
    md = ["# Validation Dashboard",
          f"_Updated: {datetime.datetime.now().isoformat(timespec='seconds')}_",
          "",
          "## Top Coherent Notes (SIS)"]
    cur.execute("SELECT notes.title, metrics.SIS FROM metrics JOIN notes ON metrics.uid=notes.uid ORDER BY SIS DESC LIMIT 20")
    for title, sis in cur.fetchall():
        md.append(f"- {title} — SIS: {sis}")
    md.append("\n## Most Consistent (LCS)")
    cur.execute("SELECT notes.title, metrics.LCS FROM metrics JOIN notes ON metrics.uid=notes.uid ORDER BY LCS DESC LIMIT 20")
    for title, lcs in cur.fetchall():
        md.append(f"- {title} — LCS: {lcs}")
    md.append("\n## Scar Resolution Index (SRI)")
    cur.execute("SELECT notes.title, metrics.SRI FROM metrics JOIN notes ON metrics.uid=notes.uid WHERE metrics.SRI IS NOT NULL ORDER BY SRI DESC LIMIT 20")
    for title, sri in cur.fetchall():
        md.append(f"- {title} — SRI: {sri}")
    (dashboard / "validation_dashboard.md").write_text("\n".join(md), encoding="utf-8")

    con.close()
    return len(metrics)

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Validation Scaffold")
    ap.add_argument("--db", default=str(Path(__file__).resolve().parent.parent / "Data" / "coherence.db"))
    args = ap.parse_args()
    n = compute(Path(args.db))
    print(f"Wrote metrics for {n} notes and generated Dashboards/validation_dashboard.md")

if __name__ == "__main__":
    main()
