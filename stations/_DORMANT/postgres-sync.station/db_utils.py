"""
07_POSTGRES — shared Postgres helpers used by every runner and workflow.

Canonical credentials live in 07_POSTGRES\\config.json. Other tools either
import this module or read that config directly.

Public surface:
  load_pg_config()      -> dict
  Database              -> connection wrapper
  Database.connect()
  Database.query(sql, params=None) -> list[dict]
  Database.execute(sql, params=None) -> rowcount
  Database.executemany(sql, rows)   -> rowcount
  Database.iter_null_rows(table, id_col, target_col, select_cols, where=None, batch_size=100)
       -> yields batches of dict rows where target_col IS NULL.
  Database.update_row(table, id_col, id_val, set_cols)
  Database.ensure_youtube_table()
  Database.upsert_youtube_videos(rows)
  encode_vector(np.ndarray) -> bytes  (float32 little-endian)
  decode_vector(bytes, dim) -> np.ndarray
"""
from __future__ import annotations

import json
import logging
import os
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                          # X:\Backside\stations
LOG_DIR = HERE.parent.parent / "_LOGS"      # shared X:\Backside\_LOGS (not stations\_LOGS)

CONFIG_PATH = HERE / "config.json"
# Zero-lockout secret resolution: try several .env locations in priority order
# (on-drive Backside tree first, then the legacy D:\brain location). Never
# depends on a single path, so a moved/missing file can't lock us out.
ENV_PATHS = [
    ROOT / ".env",              # X:\Backside\stations\.env
    ROOT.parent / ".env",       # X:\Backside\.env  (on-drive canonical copy)
    Path(r"D:\brain\.env"),     # legacy fallback
]
ENV_PATH = ENV_PATHS[0]         # back-compat alias

YOUTUBE_TABLE_CREATE = """
CREATE TABLE IF NOT EXISTS {table} (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(20) UNIQUE,
    title TEXT,
    channel_title TEXT,
    channel_id VARCHAR(64),
    description TEXT,
    published_at TIMESTAMP,
    search_query TEXT,
    thumbnail_url TEXT,
    sbert_embedding BYTEA,
    deberta_label TEXT,
    deberta_confidence FLOAT,
    cluster_id INT,
    scraped_at TIMESTAMP DEFAULT NOW()
)
"""

YOUTUBE_TABLE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_{table}_video_id ON {table}(video_id)",
    "CREATE INDEX IF NOT EXISTS idx_{table}_sbert_null ON {table}(id) WHERE sbert_embedding IS NULL",
    "CREATE INDEX IF NOT EXISTS idx_{table}_deberta_null ON {table}(id) WHERE deberta_label IS NULL",
    "CREATE INDEX IF NOT EXISTS idx_{table}_cluster_null ON {table}(id) WHERE cluster_id IS NULL",
]


def load_root_env() -> dict[str, str]:
    """Parse the first existing .env in ENV_PATHS (minimal shell-style rules)."""
    env: dict[str, str] = {}
    env_path = next((p for p in ENV_PATHS if p.exists()), None)
    if env_path is None:
        return env
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        env[key] = value
    return env


def get_secret(name: str, default: str = "") -> str:
    """Resolve a secret from process env first, then D:\\brain\\.env."""
    val = os.environ.get(name)
    if val:
        return val
    return load_root_env().get(name, default)


def load_pg_config(override_path: str | Path | None = None) -> dict:
    """Load the canonical Postgres config block and overlay env secrets."""
    p = Path(override_path) if override_path else CONFIG_PATH
    cfg = json.loads(p.read_text(encoding="utf-8"))
    pg = cfg.get("postgres", {})
    password_env = pg.get("password_env", "BRAIN_PG_PASSWORD")
    password = get_secret(password_env, "")
    if password:
        pg["password"] = password
    cfg["postgres"] = pg
    return cfg


def encode_vector(vec: np.ndarray) -> bytes:
    """float32 little-endian byte encoding for BYTEA storage."""
    return np.asarray(vec, dtype="<f4").tobytes()


def decode_vector(buf: bytes, dim: int | None = None) -> np.ndarray:
    arr = np.frombuffer(buf, dtype="<f4")
    if dim is not None and arr.size != dim:
        raise ValueError(f"vector length {arr.size} != expected {dim}")
    return arr


class Database:
    def __init__(self, pg_config: dict | None = None, application_name: str | None = None):
        if pg_config is None:
            pg_config = load_pg_config()["postgres"]
        self.cfg = dict(pg_config)
        if application_name:
            self.cfg["application_name"] = application_name
        self.conn = None

    def connect(self):
        import psycopg2
        from psycopg2.extras import RealDictCursor  # noqa: F401  (used in cursors())

        if self.conn is not None and not self.conn.closed:
            return self
        self.conn = psycopg2.connect(
            host=self.cfg["host"],
            port=self.cfg["port"],
            user=self.cfg["user"],
            password=self.cfg["password"],
            dbname=self.cfg["database"],
            connect_timeout=self.cfg.get("connect_timeout", 10),
            application_name=self.cfg.get("application_name", "brain_pipeline"),
        )
        return self

    def close(self):
        if self.conn is not None and not self.conn.closed:
            self.conn.close()

    def __enter__(self):
        return self.connect()

    def __exit__(self, *args):
        self.close()

    @contextmanager
    def _cursor(self, dict_rows: bool = False):
        from psycopg2.extras import RealDictCursor

        if self.conn is None or self.conn.closed:
            self.connect()
        cur = self.conn.cursor(cursor_factory=RealDictCursor) if dict_rows else self.conn.cursor()
        try:
            yield cur
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cur.close()

    def query(self, sql: str, params: Sequence | None = None) -> list[dict]:
        with self._cursor(dict_rows=True) as cur:
            cur.execute(sql, params)
            return [dict(r) for r in cur.fetchall()]

    def execute(self, sql: str, params: Sequence | None = None) -> int:
        with self._cursor() as cur:
            cur.execute(sql, params)
            return cur.rowcount

    def executemany(self, sql: str, rows: Iterable[Sequence]) -> int:
        from psycopg2.extras import execute_batch

        with self._cursor() as cur:
            execute_batch(cur, sql, list(rows), page_size=200)
            return cur.rowcount

    def iter_null_rows(
        self,
        table: str,
        id_col: str,
        target_col: str,
        select_cols: Sequence[str],
        where: str | None = None,
        batch_size: int = 100,
    ) -> Iterator[list[dict]]:
        """Yield successive batches of rows where target_col IS NULL.

        Each batch is fetched with a fresh query, so the iterator naturally resumes:
        callers UPDATE the rows in each batch (setting target_col), and the next
        SELECT no longer returns them.
        """
        cols = ", ".join([id_col] + [c for c in select_cols if c != id_col])
        clause = f"{target_col} IS NULL"
        if where:
            clause = f"({where}) AND {clause}"
        sql = f"SELECT {cols} FROM {table} WHERE {clause} ORDER BY {id_col} LIMIT %s"
        while True:
            batch = self.query(sql, (batch_size,))
            if not batch:
                return
            yield batch

    def update_row(
        self,
        table: str,
        id_col: str,
        id_val: Any,
        set_cols: dict[str, Any],
    ) -> int:
        if not set_cols:
            return 0
        assignments = ", ".join(f"{k} = %s" for k in set_cols)
        sql = f"UPDATE {table} SET {assignments} WHERE {id_col} = %s"
        params = list(set_cols.values()) + [id_val]
        return self.execute(sql, params)

    def update_rows_bulk(
        self,
        table: str,
        id_col: str,
        set_cols: list[str],
        rows: Iterable[Sequence],
    ) -> int:
        """Bulk update via execute_batch. rows = list of (val_for_set_col1, ..., id_val)."""
        if not set_cols:
            return 0
        assignments = ", ".join(f"{c} = %s" for c in set_cols)
        sql = f"UPDATE {table} SET {assignments} WHERE {id_col} = %s"
        return self.executemany(sql, rows)

    def ensure_youtube_table(self, table_name: str = "youtube_apologetics") -> None:
        """Create table if missing; if it exists with a partial schema, add the
        ML columns (sbert_embedding, deberta_label, deberta_confidence, cluster_id)
        and the partial NULL indexes idempotently. Order is critical: table ->
        ALTER columns -> indexes (the partial indexes reference the ML columns)."""
        alter_cols = [
            ("sbert_embedding", "BYTEA"),
            ("deberta_label", "TEXT"),
            ("deberta_confidence", "FLOAT"),
            ("cluster_id", "INT"),
        ]
        with self._cursor() as cur:
            cur.execute(YOUTUBE_TABLE_CREATE.format(table=table_name))
            for col, typ in alter_cols:
                cur.execute(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {col} {typ}")
            for idx_sql in YOUTUBE_TABLE_INDEXES:
                cur.execute(idx_sql.format(table=table_name))

    def upsert_youtube_videos(
        self,
        rows: list[dict],
        table_name: str = "youtube_apologetics",
    ) -> int:
        """Insert YouTube rows; on video_id conflict do nothing.

        Each row dict supports both the JSON shape ('channel', 'published',
        'thumbnail') and the table shape ('channel_title', 'published_at',
        'thumbnail_url'). Returns rowcount of the last batch.
        """
        if not rows:
            return 0
        sql = f"""
            INSERT INTO {table_name}
                (video_id, title, channel_title, channel_id, description,
                 published_at, search_query, thumbnail_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (video_id) DO NOTHING
        """
        params: list[tuple] = []
        for r in rows:
            params.append(
                (
                    r.get("video_id"),
                    r.get("title"),
                    r.get("channel_title") or r.get("channel"),
                    r.get("channel_id"),
                    r.get("description"),
                    r.get("published_at") or r.get("published"),
                    r.get("search_query"),
                    r.get("thumbnail_url") or r.get("thumbnail"),
                )
            )
        return self.executemany(sql, params)

    def export_table_to_csv(self, table_name: str, out_path: Path) -> int:
        """COPY TO CSV via psycopg2.copy_expert. Returns rowcount."""
        out_path.parent.mkdir(parents=True, exist_ok=True)
        sql = f"COPY (SELECT * FROM {table_name}) TO STDOUT WITH CSV HEADER"
        if self.conn is None or self.conn.closed:
            self.connect()
        with self._cursor() as cur, open(out_path, "wb") as f:
            cur.copy_expert(sql, f)
            return cur.rowcount

    def import_csv_to_table(self, table_name: str, csv_path: Path) -> int:
        sql = f"COPY {table_name} FROM STDIN WITH CSV HEADER"
        if self.conn is None or self.conn.closed:
            self.connect()
        with self._cursor() as cur, open(csv_path, "rb") as f:
            cur.copy_expert(sql, f)
            return cur.rowcount


def _setup_logging(name: str = "postgres") -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    from datetime import datetime

    logfile = LOG_DIR / f"{name}_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


# CLI helpers ---------------------------------------------------------------

def _cmd_test_connection() -> int:
    log = _setup_logging()
    cfg = load_pg_config()
    pg = cfg["postgres"]
    log.info("connecting to %s:%s db=%s as %s", pg["host"], pg["port"], pg["database"], pg["user"])
    try:
        with Database(pg) as db:
            row = db.query("SELECT version() AS v, current_database() AS db, now() AS ts")[0]
            log.info("OK %s", row)
        return 0
    except Exception as e:
        log.exception("connection failed: %s", e)
        return 1


def _cmd_export(table: str, out: str) -> int:
    log = _setup_logging()
    out_path = Path(out)
    log.info("exporting %s -> %s", table, out_path)
    with Database() as db:
        n = db.export_table_to_csv(table, out_path)
    log.info("done. rowcount reported by driver: %s", n)
    return 0


def _cmd_import(table: str, csv: str) -> int:
    log = _setup_logging()
    csv_path = Path(csv)
    if not csv_path.exists():
        log.error("missing csv: %s", csv_path)
        return 1
    log.info("importing %s -> %s", csv_path, table)
    with Database() as db:
        n = db.import_csv_to_table(table, csv_path)
    log.info("done. rowcount: %s", n)
    return 0


def _cmd_load_youtube_json(json_path: str, table: str = "youtube_apologetics") -> int:
    log = _setup_logging("load_youtube")
    p = Path(json_path)
    if not p.exists():
        log.error("missing json: %s", p)
        return 1
    log.info("loading %s into %s", p, table)
    rows = json.loads(p.read_text(encoding="utf-8"))
    log.info("parsed %d rows", len(rows))
    with Database() as db:
        db.ensure_youtube_table(table)
        log.info("table %s ensured", table)
        BATCH = 500
        inserted = 0
        for i in range(0, len(rows), BATCH):
            chunk = rows[i : i + BATCH]
            try:
                db.upsert_youtube_videos(chunk, table)
                inserted += len(chunk)
                log.info("[%d/%d] upserted batch", inserted, len(rows))
            except Exception as e:
                log.exception("batch %d-%d failed: %s", i, i + len(chunk), e)
        existing = db.query(f"SELECT COUNT(*) AS c FROM {table}")[0]["c"]
        log.info("done. table now contains %s rows", existing)
    return 0


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Postgres utilities")
    sub = ap.add_subparsers(dest="cmd", required=False)

    sub.add_parser("test", help="ping the database and report version")

    p_exp = sub.add_parser("export", help="export a table to CSV via COPY")
    p_exp.add_argument("table")
    p_exp.add_argument("out")

    p_imp = sub.add_parser("import", help="import a CSV into a table via COPY")
    p_imp.add_argument("table")
    p_imp.add_argument("csv")

    p_yt = sub.add_parser("load-youtube-json", help="bulk-load youtube JSON into youtube_apologetics")
    p_yt.add_argument("json_path")
    p_yt.add_argument("--table", default="youtube_apologetics")

    args = ap.parse_args()

    if args.cmd is None or args.cmd == "test":
        return _cmd_test_connection()
    if args.cmd == "export":
        return _cmd_export(args.table, args.out)
    if args.cmd == "import":
        return _cmd_import(args.table, args.csv)
    if args.cmd == "load-youtube-json":
        return _cmd_load_youtube_json(args.json_path, args.table)
    return 2


if __name__ == "__main__":
    sys.exit(main())
