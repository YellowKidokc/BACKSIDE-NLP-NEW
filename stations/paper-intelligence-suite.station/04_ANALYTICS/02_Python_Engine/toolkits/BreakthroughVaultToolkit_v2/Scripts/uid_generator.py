
"""
uid_generator.py
Deterministic, human-meaningful UIDs for notes.
Format: {DOMAIN}-{TOPIC}-{KIND}-{NNNN}
  - DOMAIN: THEO|PHYS|PHIL|HIST|SYN|AGCY|META (configurable mapping)
  - TOPIC: slug (GRACE, ENTROPY, RESURRECTION, etc.)
  - KIND: ATOM|LAW|EQ|PAPER|NOTE
  - NNNN: zero-padded index per (DOMAIN, TOPIC, KIND)
"""

import re
import sqlite3
from pathlib import Path

DOMAIN_MAP = {
    "theology": "THEO",
    "science": "PHYS",
    "philosophy": "PHIL",
    "history": "HIST",
    "synthesis": "SYN",
    "agency": "AGCY",
    "meta": "META",
}

def slugify(s: str) -> str:
    s = s.strip().upper()
    s = re.sub(r'[^A-Z0-9]+','-', s)
    s = re.sub(r'-+','-', s).strip('-')
    return s[:16] if s else "GEN"

def ensure_tables(db_path: Path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS uid_registry(
        domain TEXT, topic TEXT, kind TEXT, idx INTEGER,
        PRIMARY KEY (domain, topic, kind)
    )""")
    con.commit()
    con.close()

def next_index(db_path: Path, domain: str, topic: str, kind: str) -> int:
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT idx FROM uid_registry WHERE domain=? AND topic=? AND kind=?", (domain, topic, kind))
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO uid_registry(domain, topic, kind, idx) VALUES (?,?,?,?)", (domain, topic, kind, 1))
        con.commit()
        con.close()
        return 1
    else:
        nxt = row[0] + 1
        cur.execute("UPDATE uid_registry SET idx=? WHERE domain=? AND topic=? AND kind=?", (nxt, domain, topic, kind))
        con.commit()
        con.close()
        return nxt

def generate_uid(db_path: Path, domain: str, topic: str, kind: str) -> str:
    ensure_tables(db_path)
    dcode = DOMAIN_MAP.get(domain.lower(), "META")
    tcode = slugify(topic)
    kc = kind.strip().upper()
    idx = next_index(db_path, dcode, tcode, kc)
    return f"{dcode}-{tcode}-{kc}-{idx:04d}"
