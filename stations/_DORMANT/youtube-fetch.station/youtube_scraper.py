"""
05_YOUTUBE — YouTube Data API v3 search + dedup + Postgres write.

Modes:
  (default)        run search for every query in config.queries.
                   For each result: dedup against config.table on video_id;
                   insert new rows. Save a CSV mirror to config.output.csv_path.
  --load-json P    bulk-import a JSON array (3,913-video Bill Brain dump
                   shape: video_id, title, channel, channel_id, description,
                   published, thumbnail, search_query) into config.table.
  --self-test      validate config.api_key with a 1-result probe call.

Quota safety: a single search.list call costs 100 units, default daily quota
is 10,000 — that's 100 search calls. The runner stops gracefully on quota
errors and writes whatever it already collected.
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOG_DIR = ROOT / "_LOGS"
PG_DIR = ROOT / "07_POSTGRES"

if str(PG_DIR) not in sys.path:
    sys.path.insert(0, str(PG_DIR))


def _setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    logfile = LOG_DIR / f"youtube_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger("youtube")
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


def _load_config() -> dict:
    return json.loads((HERE / "config.json").read_text(encoding="utf-8"))


def _resolve_api_key(cfg: dict) -> str:
    env_name = cfg.get("api_key_env", "BRAIN_YOUTUBE_API_KEY")
    try:
        from db_utils import get_secret

        env_val = get_secret(env_name, "")
    except Exception:
        env_val = ""
    return env_val or cfg.get("api_key", "")


class YouTubeScraper:
    def __init__(self, api_key: str):
        from googleapiclient.discovery import build  # type: ignore

        if not api_key:
            raise ValueError("api_key is empty")
        self.api_key = api_key
        self.client = build("youtube", "v3", developerKey=api_key, cache_discovery=False)

    def search(
        self,
        query: str,
        max_results: int = 50,
        order: str = "relevance",
        type_: str = "video",
        safe_search: str = "none",
        region_code: str | None = "US",
        relevance_language: str | None = "en",
        max_pages: int = 1,
    ) -> list[dict]:
        results: list[dict] = []
        page_token = None
        for _ in range(max(1, max_pages)):
            req_kwargs = {
                "q": query,
                "part": "snippet",
                "maxResults": min(50, max_results),
                "order": order,
                "type": type_,
                "safeSearch": safe_search,
            }
            if region_code:
                req_kwargs["regionCode"] = region_code
            if relevance_language:
                req_kwargs["relevanceLanguage"] = relevance_language
            if page_token:
                req_kwargs["pageToken"] = page_token
            req = self.client.search().list(**req_kwargs)
            resp = req.execute()
            for item in resp.get("items", []):
                vid = item.get("id", {}).get("videoId")
                if not vid:
                    continue
                sn = item.get("snippet", {})
                results.append(
                    {
                        "video_id": vid,
                        "title": sn.get("title"),
                        "channel_title": sn.get("channelTitle"),
                        "channel_id": sn.get("channelId"),
                        "description": sn.get("description"),
                        "published_at": sn.get("publishedAt"),
                        "thumbnail_url": (sn.get("thumbnails", {}).get("high") or {}).get("url"),
                        "search_query": query,
                    }
                )
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        return results


def _self_test(log: logging.Logger) -> int:
    cfg = _load_config()
    key = _resolve_api_key(cfg)
    if not key:
        log.error("api_key missing in config.json and env")
        return 1
    try:
        sc = YouTubeScraper(key)
        out = sc.search("apologetics", max_results=1, max_pages=1)
    except Exception as e:
        log.exception("self-test API call failed: %s", e)
        return 2
    if not out:
        log.error("self-test returned 0 results — API key may be restricted")
        return 3
    log.info("self-test OK first result: %s — %r", out[0]["video_id"], out[0]["title"])
    return 0


def _dt_csv_path(template: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d")
    return Path(template.replace("YYYYMMDD", stamp))


def _write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "video_id", "title", "channel_title", "channel_id", "description",
        "published_at", "search_query", "thumbnail_url",
    ]
    new_file = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if new_file:
            w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in fields})


def _load_json(json_path: Path, log: logging.Logger, table: str) -> int:
    from db_utils import Database

    if not json_path.exists():
        log.error("missing json: %s", json_path)
        return 1
    rows = json.loads(json_path.read_text(encoding="utf-8"))
    log.info("parsed %d rows from %s", len(rows), json_path)
    with Database(application_name="youtube_loader") as db:
        db.ensure_youtube_table(table)
        BATCH = 500
        for i in range(0, len(rows), BATCH):
            chunk = rows[i : i + BATCH]
            try:
                db.upsert_youtube_videos(chunk, table)
            except Exception as e:
                log.exception("batch %d failed: %s", i, e)
        total = db.query(f"SELECT COUNT(*) AS c FROM {table}")[0]["c"]
        log.info("done. table %s now has %s rows", table, total)
    return 0


def run(config: dict | None = None) -> int:
    log = _setup_logging()
    cfg = config or _load_config()
    api_key = _resolve_api_key(cfg)
    if not api_key:
        log.error("api_key missing in config.json and env")
        return 1
    table = cfg.get("table", "youtube_apologetics")
    queries = cfg.get("queries", [])
    if not queries:
        log.warning("no queries configured")
        return 0

    ss = cfg.get("search_settings", {})
    csv_path = _dt_csv_path(cfg.get("output", {}).get("csv_path", str(LOG_DIR / "youtube_scrape_YYYYMMDD.csv")))

    from db_utils import Database

    sc = YouTubeScraper(api_key)
    total_found = 0
    total_inserted = 0
    quota_hit = False

    with Database(application_name="youtube_scraper") as db:
        db.ensure_youtube_table(table)
        existing_ids = {r["video_id"] for r in db.query(f"SELECT video_id FROM {table}")}
        log.info("starting with %d existing video_ids in %s", len(existing_ids), table)

        for qi, query in enumerate(queries, 1):
            if quota_hit:
                break
            log.info("[%d/%d] query=%r", qi, len(queries), query)
            try:
                results = sc.search(
                    query,
                    max_results=ss.get("max_results_per_query", 50),
                    order=ss.get("order", "relevance"),
                    type_=ss.get("type", "video"),
                    safe_search=ss.get("safe_search", "none"),
                    region_code=ss.get("region_code"),
                    relevance_language=ss.get("relevance_language"),
                    max_pages=ss.get("max_pages", 1),
                )
            except Exception as e:
                msg = str(e).lower()
                if "quota" in msg or "exceeded" in msg or "403" in msg:
                    log.error("quota exceeded — saving progress and exiting cleanly: %s", e)
                    quota_hit = True
                    break
                log.exception("search failed: %s — skipping query", e)
                continue

            new_rows = [r for r in results if r["video_id"] not in existing_ids]
            total_found += len(results)
            log.info("  found=%d new=%d (cumulative new=%d)",
                     len(results), len(new_rows), total_inserted + len(new_rows))

            if not new_rows:
                continue
            try:
                db.upsert_youtube_videos(new_rows, table)
                total_inserted += len(new_rows)
                existing_ids.update(r["video_id"] for r in new_rows)
                _write_csv(new_rows, csv_path)
            except Exception as e:
                log.exception("insert failed: %s", e)

    log.info("scrape complete. queries_run=%d found=%d inserted=%d quota_hit=%s csv=%s",
             qi if queries else 0, total_found, total_inserted, quota_hit, csv_path)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="YouTube apologetics scraper")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--load-json", help="bulk-load a JSON file into the table; skips API")
    args = ap.parse_args()

    log = _setup_logging()
    cfg = _load_config()
    if args.self_test:
        return _self_test(log)
    if args.load_json:
        return _load_json(Path(args.load_json), log, cfg.get("table", "youtube_apologetics"))
    return run(cfg)


if __name__ == "__main__":
    sys.exit(main())
