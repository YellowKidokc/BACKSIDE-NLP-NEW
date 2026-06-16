import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent / "08_Database" / "theophysics.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute("SELECT concept FROM concepts")
rows = cur.fetchall()

updated_concepts = {}
for row in rows:
    concept = row[0]
    if len(concept) > 50:
        new_concept = concept[:50]
        # handle duplicates
        if new_concept in updated_concepts:
            updated_concepts[new_concept] += 1
            new_concept = f"{new_concept}_{updated_concepts[new_concept]}"
        else:
            updated_concepts[new_concept] = 0
        
        print(f"Truncating '{concept}' to '{new_concept}'")
        cur.execute("UPDATE concepts SET concept = ? WHERE concept = ?", (new_concept, concept))

con.commit()
con.close()
