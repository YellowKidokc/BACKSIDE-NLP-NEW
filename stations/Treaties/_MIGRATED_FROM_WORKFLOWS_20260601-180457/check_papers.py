import psycopg
conn = psycopg.connect("postgresql://root:Moss9pep28$@192.168.1.177:2665/treaties")
cur = conn.cursor()
cur.execute("SELECT id, title, length(full_text) as chars FROM papers ORDER BY id")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  ID={r[0]}  title={r[1]}  chars={r[2]}")
else:
    print("No papers in database")
cur.close()
conn.close()