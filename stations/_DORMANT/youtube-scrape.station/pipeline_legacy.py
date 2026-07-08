"""
youtube-scrape workflow.

Order of operations:
  1. 05_YOUTUBE.run()        — scrape new videos into config.table
  2. 02_SBERT.run()          — embed any rows where sbert_embedding IS NULL
  3. 03_DEBERTA.run()        — classify any rows where deberta_label IS NULL
  4. 04_HDBSCAN.run()        — re-cluster the whole table

Each step is gated by config.steps and is fully resumable on its own.
A failure in any step is logged and the next step still runs.
"""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATIONS_ROOT = HERE.parent
BACKSIDE_ROOT = STATIONS_ROOT.parent
LOG_DIR = BACKSIDE_ROOT / "_LOGS"

# Add tool folders to sys.path.
TOOL_STATIONS = {
    "youtube": STATIONS_ROOT / "youtube-fetch.station",
    "sbert": STATIONS_ROOT / "sbert-embedder.station",
    "deberta": STATIONS_ROOT / "deberta-runner.station",
    "hdbscan": STATIONS_ROOT / "hdbscan-cluster.station",
    "postgres": STATIONS_ROOT / "postgres-sync.station",
}

for p in TOOL_STATIONS.values():
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


def _setup_logging(name: str) -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    logfile = LOG_DIR / f"workflow_{name}_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger(f"workflow.{name}")
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


def _load_runner_config(tool_dir: str) -> dict:
    return json.loads((TOOL_STATIONS[tool_dir] / "config.json").read_text(encoding="utf-8"))


def main() -> int:
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    log = _setup_logging(cfg.get("name", "youtube-scrape"))
    table = cfg.get("table", "youtube_apologetics")
    steps = cfg.get("steps", {})

    log.info("=== START youtube-scrape (table=%s) ===", table)

    # 1. SCRAPE -----------------------------------------------------------
    if steps.get("scrape", True):
        log.info("--- step 1/4: scrape ---")
        try:
            import youtube_scraper

            yt_cfg = _load_runner_config("youtube")
            yt_cfg["table"] = table
            youtube_scraper.run(yt_cfg)
        except Exception as e:
            log.exception("scrape failed: %s — continuing", e)

    # 2. EMBED ------------------------------------------------------------
    if steps.get("embed", True):
        log.info("--- step 2/4: embed ---")
        try:
            import sbert_runner

            sb_cfg = _load_runner_config("sbert")
            sb_cfg["source"]["type"] = "postgres"
            sb_cfg["source"]["table"] = table
            sbert_runner.run(sb_cfg)
        except Exception as e:
            log.exception("embed failed: %s — continuing", e)

    # 3. CLASSIFY ---------------------------------------------------------
    if steps.get("classify", True):
        log.info("--- step 3/4: classify ---")
        try:
            import deberta_runner

            db_cfg = _load_runner_config("deberta")
            db_cfg["source"]["type"] = "postgres"
            db_cfg["source"]["table"] = table
            deberta_runner.run(db_cfg)
        except Exception as e:
            log.exception("classify failed: %s — continuing", e)

    # 4. CLUSTER ----------------------------------------------------------
    if steps.get("cluster", True):
        log.info("--- step 4/4: cluster ---")
        try:
            import cluster_runner

            cl_cfg = _load_runner_config("hdbscan")
            cl_cfg["source"]["type"] = "postgres"
            cl_cfg["source"]["table"] = table
            cluster_runner.run(cl_cfg)
        except Exception as e:
            log.exception("cluster failed: %s", e)

    log.info("=== END youtube-scrape ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
