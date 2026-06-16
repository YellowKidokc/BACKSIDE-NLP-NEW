"""SQLite bridge for FIS classification cards.

Writes cards into the SHARED FIS database at:
  \\\\192.168.2.50\\brain\\09_DATABASES\\FIS\\sorter_cache.sqlite

Falls back to local fis.db if NAS is unreachable.
The shared DB is Codex's sorter_cache schema — we INSERT INTO
the existing tables, not create our own.
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime

# Shared FIS database (authoritative)
SHARED_DB = Path(r"\\192.168.2.50\brain\09_DATABASES\FIS\sorter_cache.sqlite")
LOCAL_DB = Path(__file__).parent.parent / "fis.db"


def get_connection(db_path: str = None) -> sqlite3.Connection:
    if db_path:
        path = db_path
    elif SHARED_DB.exists():
        path = str(SHARED_DB)
    else:
        path = str(LOCAL_DB)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db(db_path: str = None):
    """Create FIS tables — only used for local fallback.
    Shared DB already has Codex's full schema."""
    conn = get_connection(db_path)
    conn.executescript(SCHEMA)
    conn.close()


SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id TEXT UNIQUE NOT NULL,
    source_path TEXT NOT NULL,
    original_name TEXT NOT NULL,
    baseline TEXT NOT NULL,
    domain TEXT,
    domain_confidence REAL,
    domain_approved INTEGER DEFAULT 0,
    file_type_meaning TEXT,
    file_type_confidence REAL,
    summary TEXT,
    tags_json TEXT,
    keywords_json TEXT,
    slug TEXT,
    rename_preview_json TEXT,
    suggested_action TEXT,
    confidence_overall REAL,
    needs_review INTEGER DEFAULT 1,
    review_reason TEXT,
    final_name TEXT,
    final_path TEXT,
    status TEXT DEFAULT 'pending',
    classified_at TEXT,
    approved_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_files_domain ON files(domain);
CREATE INDEX IF NOT EXISTS idx_files_status ON files(status);
CREATE INDEX IF NOT EXISTS idx_files_source ON files(source_path);
""";


def insert_card(card: dict, db_path: str = None):
    """Insert a classification card into SQLite."""
    conn = get_connection(db_path)
    conn.execute("""
        INSERT OR REPLACE INTO files (
            file_id, source_path, original_name, baseline,
            domain, domain_confidence, domain_approved,
            file_type_meaning, file_type_confidence,
            summary, tags_json, keywords_json, slug,
            rename_preview_json, suggested_action,
            confidence_overall, needs_review, review_reason,
            classified_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        card["file_id"], card["source_path"], card["original_name"],
        card["baseline"],
        card["domain"]["value"], card["domain"]["confidence"],
        1 if card["domain"].get("approved") else 0,
        card["file_type_meaning"]["value"],
        card["file_type_meaning"]["confidence"],
        card["summary"],
        json.dumps(card.get("tags", [])),
        json.dumps(card.get("keywords", [])),
        card.get("slug", ""),
        json.dumps(card.get("rename_preview", {})),
        card.get("suggested_action", {}).get("primary", "review"),
        card.get("confidence", {}).get("overall", 0),
        1 if card.get("review", {}).get("needs_review") else 0,
        card.get("review", {}).get("reason"),
        card.get("classified_at"),
    ))
    conn.commit()
    conn.close()
