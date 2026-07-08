"""
05_YOUTUBE — transcript_puller.py
Pull auto-generated or manual captions from YouTube videos
and store them in Postgres alongside the existing video metadata.

Uses youtube-transcript-api v1.2.4 (no API quota, no auth needed).
Falls back gracefully when transcripts are unavailable.

Usage:
  python transcript_puller.py              # pull transcripts for all videos missing them
  python transcript_puller.py --test       # test with one video
  python transcript_puller.py --limit 100  # process max 100 videos
"""
from __future__ import annotations

import argparse
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
    logfile = LOG_DIR / f"transcript_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger("transcript")
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


def pull_transcript(video_id: str) -> dict:
    """Pull transcript for a single video using youtube-transcript-api v1.2.4."""
    from youtube_transcript_api import YouTubeTranscriptApi

    try:
        ytt = YouTubeTranscriptApi()
        result = ytt.fetch(video_id, languages=["en"])

        # result is a FetchedTranscript with .snippets, .language, .language_code, .is_generated
        full_text = " ".join(snippet.text for snippet in result.snippets)

        segments = [
            {
                "text": snippet.text,
                "start": snippet.start,
                "duration": snippet.duration,
            }
            for snippet in result.snippets
        ]

        source = "auto" if result.is_generated else "manual"

        return {
            "success": True,
            "video_id": video_id,
            "transcript": full_text.strip(),
            "segments": segments,
            "source": source,
            "language": result.language_code,
            "char_count": len(full_text),
        }

    except Exception as e:
        error_type = type(e).__name__
        return {"success": False, "error": error_type, "error_detail": str(e), "video_id": video_id}


def ensure_transcript_column(db) -> None:
    """Add transcript columns to youtube_apologetics if they don't exist."""
    cols = [
        ("transcript", "TEXT"),
        ("transcript_source", "VARCHAR(20)"),
        ("transcript_language", "VARCHAR(10)"),
        ("transcript_char_count", "INT"),
        ("transcript_pulled_at", "TIMESTAMP"),
    ]
    for col, typ in cols:
        try:
            db.execute(f"ALTER TABLE youtube_apologetics ADD COLUMN IF NOT EXISTS {col} {typ}")
        except Exception:
            pass


def run(limit: int = 0, test_mode: bool = False) -> int:
    log = _setup_logging()
    cfg = _load_config()
    table = cfg.get("table", "youtube_apologetics")

    from db_utils import Database

    with Database(application_name="transcript_puller") as db:
        ensure_transcript_column(db)

        if test_mode:
            rows = db.query(f"SELECT video_id, title FROM {table} LIMIT 1")
            if not rows:
                log.error("no videos in table")
                return 1
            vid = rows[0]["video_id"]
            log.info("TEST MODE: pulling transcript for %s — %s", vid, rows[0]["title"])
            result = pull_transcript(vid)
            if result["success"]:
                log.info("SUCCESS: %d chars, source=%s, lang=%s",
                         result["char_count"], result["source"], result["language"])
                log.info("First 300 chars: %s", result["transcript"][:300])
            else:
                log.info("FAILED: %s — %s", result["error"], result.get("error_detail", ""))
            return 0

        # Pull transcripts for all videos that don't have one yet
        limit_clause = f"LIMIT {limit}" if limit > 0 else ""
        rows = db.query(
            f"SELECT video_id, title FROM {table} "
            f"WHERE transcript IS NULL "
            f"ORDER BY id "
            f"{limit_clause}"
        )
        total = len(rows)
        log.info("found %d videos needing transcripts", total)
        if not total:
            return 0

        success_count = 0
        fail_count = 0
        error_types: dict[str, int] = {}

        for i, row in enumerate(rows, 1):
            vid = row["video_id"]
            result = pull_transcript(vid)

            if result["success"]:
                db.execute(
                    f"UPDATE {table} SET "
                    f"transcript = %s, "
                    f"transcript_source = %s, "
                    f"transcript_language = %s, "
                    f"transcript_char_count = %s, "
                    f"transcript_pulled_at = NOW() "
                    f"WHERE video_id = %s",
                    (
                        result["transcript"],
                        result["source"],
                        result["language"],
                        result["char_count"],
                        vid,
                    )
                )
                success_count += 1
                if i % 50 == 0 or i == total:
                    log.info("[%d/%d] success=%d fail=%d — last: %s",
                             i, total, success_count, fail_count, row["title"][:60])
            else:
                fail_count += 1
                err = result["error"]
                error_types[err] = error_types.get(err, 0) + 1
                if i % 50 == 0:
                    log.info("[%d/%d] success=%d fail=%d", i, total, success_count, fail_count)

        log.info("DONE. total=%d success=%d fail=%d", total, success_count, fail_count)
        if error_types:
            log.info("error breakdown: %s", json.dumps(error_types, indent=2))

        stats = db.query(
            f"SELECT "
            f"COUNT(*) AS total, "
            f"COUNT(transcript) AS has_transcript, "
            f"COUNT(*) - COUNT(transcript) AS missing_transcript, "
            f"AVG(transcript_char_count) AS avg_chars "
            f"FROM {table}"
        )[0]
        log.info("table stats: %s", stats)

    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="YouTube transcript puller")
    ap.add_argument("--test", action="store_true", help="test with one video")
    ap.add_argument("--limit", type=int, default=0, help="max videos to process (0=all)")
    args = ap.parse_args()
    return run(limit=args.limit, test_mode=args.test)


if __name__ == "__main__":
    sys.exit(main())
