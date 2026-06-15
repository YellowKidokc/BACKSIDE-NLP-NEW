
"""
concept_hub_generator.py
Generates Concept Hub pages under /Concept_Hubs based on the database.
"""

import sqlite3, os, datetime
from pathlib import Path

HUB_DIR_DEFAULT = Path(__file__).resolve().parents[1] / "Concept_Hubs"

HUB_TEMPLATE = """# {name}

## Stats
Mentions: {mentions}
Backlinks (approx): {backlinks}
Last Updated: {updated}

## Top Co-Mentions
{co_lines}

## Recent Notes
{note_lines}
"""

def top_comentions(cur, concept: str, k=10):
    cur.execute("""SELECT concept2, count FROM co_mentions WHERE concept1=?
                   UNION ALL
                   SELECT concept1, count FROM co_mentions WHERE concept2=?
                   ORDER BY count DESC LIMIT ?""", (concept, concept, k))
    return cur.fetchall()

def recent_notes(cur, concept: str, k=10):
    # very simple: search notes whose tags contain concept
    cur.execute("""SELECT title, path, updated_at FROM notes WHERE LOWER(tags) LIKE ?
                   ORDER BY updated_at DESC LIMIT ?""", (f"%{concept}%", k))
    return cur.fetchall()

def backlinks_approx(cur, concept: str) -> int:
    # proxy: number of notes tagging this concept
    cur.execute("""SELECT COUNT(*) FROM notes WHERE LOWER(tags) LIKE ?""", (f"%{concept}%",))
    return cur.fetchone()[0]

def generate(db_path: Path, out_dir: Path = HUB_DIR_DEFAULT, limit:int=100):
    out_dir.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT concept, mentions FROM concepts ORDER BY mentions DESC LIMIT ?", (limit,))
    concepts = cur.fetchall()
    for concept, mentions in concepts:
        co = top_comentions(cur, concept, k=10)
        co_lines = "\n".join(f"- {c}: {cnt}" for c, cnt in co) if co else "_None yet_"
        notes = recent_notes(cur, concept, k=10)
        note_lines = "\n".join(f"- {title}  \n  `{path}`  \n  _{updated}_" for title, path, updated in notes) if notes else "_None_"
        hub = HUB_TEMPLATE.format(
            name=concept.replace("-", " ").title(),
            mentions=mentions,
            backlinks=backlinks_approx(cur, concept),
            updated=datetime.datetime.now().isoformat(timespec="seconds"),
            co_lines=co_lines,
            note_lines=note_lines
        )
        (out_dir / f"{concept}.md").write_text(hub, encoding="utf-8")
    con.close()
    return len(concepts)

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Generate Concept Hubs")
    ap.add_argument("--db", default=str(Path(__file__).resolve().parent.parent / "Data" / "coherence.db"))
    ap.add_argument("--out", default=str(HUB_DIR_DEFAULT))
    ap.add_argument("--limit", type=int, default=100)
    args = ap.parse_args()
    n = generate(Path(args.db), Path(args.out), args.limit)
    print(f"Generated {n} concept hubs in {args.out}")

if __name__ == "__main__":
    main()
