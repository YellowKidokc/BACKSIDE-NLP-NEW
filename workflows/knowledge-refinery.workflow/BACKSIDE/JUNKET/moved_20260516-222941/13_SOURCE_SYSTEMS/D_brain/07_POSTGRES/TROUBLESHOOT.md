# 07_POSTGRES — Troubleshooting

## `OperationalError: could not connect to server`

Check the basics:

```
ping 192.168.1.177
```

If ping works but Postgres doesn't, the port (2665) probably isn't listening yet, or the server is down. From any machine that has psql:

```
psql -h 192.168.1.177 -p 2665 -U root -d crawlab_data
```

If that fails too, the issue is server-side, not Python.

## `psycopg2.OperationalError: FATAL: password authentication failed`

The password in `config.json` rotated. Update `config.json` → `postgres.password`. Every other tool reads from this same file, so one edit fixes all of them.

## `ModuleNotFoundError: psycopg2`

Run `INSTALL.bat`, or manually:

```
C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe -m pip install psycopg2-binary
```

`psycopg2-binary` is the prebuilt wheel — no compiler needed.

## `relation "<table>" does not exist`

The named table hasn't been created yet. For `youtube_apologetics`, run:

```
LOAD_YOUTUBE_JSON.bat
```

(it creates the table via `ensure_youtube_table` before inserting). For `harvested_links_apologetics` / `scraped_content_apologetics`, those are created by other parts of the system (CrawlLab) — Bill doesn't manage their schema.

## CONNECT.bat exits immediately

If `db_utils.py` raises during import, Python exits before `-i` drops you into a REPL. Run `INSTALL.bat` to confirm the connection works first.

## EXPORT.bat / IMPORT.bat: `permission denied for relation`

The configured user lacks read/write grants. From `psql` as a superuser:

```
GRANT SELECT ON <table> TO root;
GRANT INSERT, UPDATE ON <table> TO root;
```

## Bulk JSON load is slow

`upsert_youtube_videos` uses `execute_batch` with page_size=200. For 3,913 rows that's ~20 round-trips. If it's slow, the latency to the DB is the bottleneck — not the Python. Check `ping`.

## ON CONFLICT DO NOTHING — how to know what actually inserted

After `LOAD_YOUTUBE_JSON.bat` finishes it reports the total row count. Compare to the JSON length (3,913) to see how many were already present.

## Connection leak warnings

Always use `with Database() as db:` — the context manager closes on exit even if an exception is raised. The runners follow this pattern.
