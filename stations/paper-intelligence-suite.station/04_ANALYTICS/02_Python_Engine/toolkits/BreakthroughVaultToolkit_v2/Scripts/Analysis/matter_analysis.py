#!/usr/bin/env python3
import sqlite3, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "07_Data" / "theophysics.db"
OUT = ROOT / "07_Data" / "insights" / (datetime.date.today().isoformat()+"-matter-analysis.md")

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    layers = {id:code for code,id in conn.execute("SELECT code,id FROM layers")}
    data = conn.execute("SELECT name, layer_id, coherence_score FROM nodes").fetchall()
    agg = {}
    for name, lid, coh in data:
        code = layers.get(lid,"unknown")
        agg.setdefault(code, []).append(coh or 0.0)
    with open(OUT,"w") as f:
        f.write(f"# Matter Analysis ({datetime.date.today().isoformat()})\n\n")
        for code, vals in sorted(agg.items()):
            if not vals: continue
            avg = round(sum(vals)/len(vals),3)
            f.write(f"- **{code}** avg coherence: {avg}\n")
    print(f"Wrote {OUT}")

if __name__ == '__main__':
    main()
