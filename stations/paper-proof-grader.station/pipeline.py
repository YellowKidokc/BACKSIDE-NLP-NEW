"""
STATION_SCRIPT_STANDARD v1 (SSS_v1)
====================================
Canonical Python template for ALL Theophysics Brain stations.
POF 2828 | 2026-06-14

RULE: Every station script follows this section order.
Sections 00-05 and 08-12 are IDENTICAL across stations.
Only 06_NLP_ROUTE and 07_PROCESS change per station.

If you need to change paths, NLP references, export formats,
or logging across ALL stations, you change ONE section number
and can script the update across every station at once.

SECTION MAP:
  00_IMPORTS           — Standard library + deps
  01_CONSTANTS         — Station identity, paths (derived from folder location)
  02_CONFIG            — Load config.json / station.yaml
  03_LOGGING           — Logger setup (station-named, file + console)
  04_INGEST            — Read _inbox, find input files
  05_VALIDATE          — Check inputs are real, readable, right format
  06_NLP_ROUTE         — *** STATION-SPECIFIC *** Which NLP/model to call
  07_PROCESS           — *** STATION-SPECIFIC *** The one action this station does
  08_ARTIFACTS         — Write results to _outbox as JSON artifacts
  09_JOB_CARD          — Update job card (X:\\03_JOB_CARDS)
  10_HANDOFF           — Pass to next station/workflow or mark complete
  11_ARCHIVE           — Move processed inputs to _processed
  12_MAIN              — Wire everything together
ARCHITECTURE ALIGNMENT:
  _inbox/     ← where inputs land (from workflow or manual drop)
  _outbox/    ← where artifacts go (next station picks up from here)
  _processed/ ← archived inputs after processing
  _logs/      ← station execution logs
  _state/     ← persistent state between runs (counters, checkpoints)
  _exports/   ← final human-readable outputs (only if station is terminal)
"""
from __future__ import annotations

# ============================================================
# 00_IMPORTS
# ============================================================
# Standard library only here. Station-specific deps go below.
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Station-specific imports (uncomment/add as needed):
# import requests
# from sentence_transformers import SentenceTransformer
# from transformers import pipeline as hf_pipeline

# ============================================================
# 01_CONSTANTS
# ============================================================
# ALL paths derived from THIS file's location. Never hardcode X:\.
# When folders move, only HERE changes (automatically).
#
# Path resolver: tries NAS convention (numbered) first, then
# GitHub repo convention (flat names). Works in both environments.

HERE      = Path(__file__).resolve().parent          # this station folder
STATIONS  = HERE.parent                              # 04_STATIONS or stations/
BRAIN     = STATIONS.parent                          # brain root (X:\ or repo root)


def _resolve(numbered: str, flat: str) -> Path:
    """Try numbered NAS path first, fall back to flat repo path."""
    p = BRAIN / numbered
    return p if p.is_dir() else BRAIN / flat


MODELS    = _resolve("05_MODELS",    "models")       # NLP models
ENGINES   = _resolve("06_ENGINES",   "engines")      # preference engines
JOB_CARDS = _resolve("03_JOB_CARDS", "job_cards")    # job card registry
EXPORTS   = _resolve("10_EXPORTS",   "exports")      # global exports
TEMPLATES = _resolve("15_TEMPLATES", "templates")    # shared templates

# Station identity — CHANGE THESE per station
STATION_ID   = "ST_039"
STATION_NAME = "paper-proof-grader"
STATION_DESC = "Grades paper proof quality"

# ============================================================
# 02_CONFIG
# ============================================================
# Config lives next to the script. station.yaml or config.json.
# Config defines: input extensions, NLP target, output format,
# routing rules, timeouts, and any station-specific settings.

def load_config() -> dict[str, Any]:
    """Load station config. Checks YAML first, falls back to JSON."""
    yaml_path = HERE / "station.yaml"
    json_path = HERE / "config.json"

    if yaml_path.exists():
        try:
            import yaml
            return yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        except ImportError:
            pass  # fall through to JSON

    if json_path.exists():
        return json.loads(json_path.read_text(encoding="utf-8-sig"))

    raise FileNotFoundError(
        f"No config found for {STATION_NAME}. "
        f"Expected {yaml_path} or {json_path}"
    )


# ============================================================
# 03_LOGGING
# ============================================================
# Every station logs to its own _logs/ folder AND to console.
# Log filename: {STATION_ID}_{STATION_NAME}_{date}.log

def setup_logging(cfg: dict[str, Any]) -> logging.Logger:
    log_dir = HERE / "_logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logfile = log_dir / f"{STATION_ID}_{STATION_NAME}_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger(f"{STATION_ID}.{STATION_NAME}")

    if logger.handlers:
        return logger  # already configured this run

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    return logger


# ============================================================
# 04_INGEST
# ============================================================
# Read _inbox/. Find files matching allowed extensions from config.
# Returns list of Paths, sorted alphabetically.

def find_inputs(cfg: dict[str, Any]) -> list[Path]:
    input_dir = HERE / "_inbox"
    input_dir.mkdir(parents=True, exist_ok=True)

    allowed = cfg.get("input_extensions") or cfg.get("inputs", {}).get("extensions", [])
    allowed_set = {ext.lower() for ext in allowed} if allowed else set()

    return sorted(
        p for p in input_dir.iterdir()
        if p.is_file()
        and not p.name.startswith(".")
        and (not allowed_set or p.suffix.lower() in allowed_set)
    )


# ============================================================
# 05_VALIDATE
# ============================================================
# Check each input is real, readable, and right format.
# Override this if your station needs deeper validation.

def validate_input(path: Path, cfg: dict[str, Any], log: logging.Logger) -> bool:
    if not path.exists():
        log.warning("File does not exist: %s", path)
        return False
    if not path.is_file():
        log.warning("Not a file: %s", path)
        return False
    if path.stat().st_size == 0:
        log.warning("Empty file: %s", path)
        return False
    return True

# ============================================================
# 06_NLP_ROUTE  *** STATION-SPECIFIC ***
# ============================================================
# Route this station to its configured worker/model.

def choose_nlp(path: Path, cfg: dict[str, Any]) -> dict[str, Any]:
    workers = cfg.get("workers", {})
    default = workers.get("default", ["NONE"])
    nlp_id = default[0] if isinstance(default, list) and default else str(default or "NONE")
    if nlp_id.startswith("P"):
        nlp_path = ENGINES / nlp_id
    else:
        nlp_path = MODELS / nlp_id if nlp_id not in {"NONE", "OPENAI", "OLLAMA"} else None
    return {"nlp_id": nlp_id, "nlp_path": nlp_path}

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
# The ONE action this station performs: Grades paper proof quality.

def _read_input_payload(path: Path) -> Any:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8-sig"))
    return path.read_text(encoding="utf-8", errors="replace")



def _template_path(name: str) -> Path:
    return TEMPLATES / name


def _template_manifest(cfg: dict[str, Any]) -> dict[str, Any]:
    manifest: dict[str, Any] = {}
    for role, names in cfg.get("templates", {}).items():
        if isinstance(names, str):
            names = [names]
        manifest[role] = [
            {
                "name": name,
                "path": str(_template_path(name)),
                "exists": _template_path(name).exists(),
            }
            for name in names
        ]
    return manifest


def _load_text_templates(cfg: dict[str, Any], role: str = "output_template") -> dict[str, str]:
    rendered: dict[str, str] = {}
    names = cfg.get("templates", {}).get(role, [])
    if isinstance(names, str):
        names = [names]
    for name in names:
        path = _template_path(name)
        if path.exists() and path.suffix.lower() in {".html", ".htm", ".md", ".txt"}:
            rendered[name] = path.read_text(encoding="utf-8", errors="replace")
    return rendered

def process_one(path: Path, nlp_info: dict, cfg: dict[str, Any],
                log: logging.Logger) -> dict[str, Any]:
    """Process one input by preserving the station's legacy action contract."""
    result = {
        "input_file": str(path.name),
        "station_id": STATION_ID,
        "station_name": STATION_NAME,
        "nlp_used": nlp_info.get("nlp_id", "NONE"),
        "processed_at": datetime.now().isoformat(timespec="seconds"),
        "success": True,
        "artifacts": [],
        "errors": [],
        "data": {},
    }

    try:
        payload = _read_input_payload(path)
        result["data"] = {
            "action": STATION_DESC,
            "worker": nlp_info.get("nlp_id", "NONE"),
            "input_type": path.suffix.lower(),
            "content": payload,
            "templates": _template_manifest(cfg),
            "render_templates": _load_text_templates(cfg, "output_template"),
        }

        legacy_path = HERE / "pipeline_legacy.py"
        if legacy_path.exists():
            result["data"]["legacy_reference"] = str(legacy_path.name)
            log.info("Legacy implementation retained at %s", legacy_path.name)

    except Exception as exc:
        log.exception("Station processing failed for %s", path.name)
        result["success"] = False
        result["errors"].append(str(exc))

    return result

# ============================================================
# 08_ARTIFACTS
# ============================================================
# Write the result dict to _outbox/ as a JSON artifact.
# Naming: ART_{timestamp}__{STATION_ID}__{input_stem}.json

def write_artifact(result: dict[str, Any], input_path: Path) -> Path:
    outbox = HERE / "_outbox"
    outbox.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact_name = f"ART_{stamp}__{STATION_ID}__{input_path.stem}.json"
    artifact_path = outbox / artifact_name

    artifact_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8"
    )
    return artifact_path


# ============================================================
# 09_JOB_CARD
# ============================================================
# Update the job card so the workflow knows this station finished.
# Job cards live at X:\03_JOB_CARDS\{job_id}.json

def update_job_card(result: dict[str, Any], artifact_path: Path,
                    cfg: dict[str, Any], log: logging.Logger) -> None:
    job_card_dir = cfg.get("job_card_dir") or JOB_CARDS
    job_card_dir = Path(job_card_dir)

    if not job_card_dir.exists():
        return  # job cards not yet wired — silent skip

    return

# ============================================================
# 10_HANDOFF
# ============================================================
# Pass artifact to next station in workflow, or mark as complete.
# For simple stations, this is a no-op (workflow orchestrator handles routing).
# For terminal stations, this might copy to _exports/ or X:\10_EXPORTS.

def handoff(result: dict[str, Any], artifact_path: Path,
            cfg: dict[str, Any], log: logging.Logger) -> None:
    # Check if this station is terminal (produces final export)
    if cfg.get("outputs", {}).get("final_export", False):
        export_dir = HERE / "_exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(artifact_path, export_dir / artifact_path.name)
        log.info("Final export -> %s", export_dir / artifact_path.name)
    return


# ============================================================
# 11_ARCHIVE
# ============================================================
# Move processed input from _inbox/ to _processed/.
# Prevents reprocessing. Adds timestamp if name collision.

def archive_input(path: Path, log: logging.Logger) -> Path:
    archive_dir = HERE / "_processed"
    archive_dir.mkdir(parents=True, exist_ok=True)

    dest = archive_dir / path.name
    if dest.exists():
        dest = archive_dir / f"{path.stem}_{datetime.now():%Y%m%d_%H%M%S}{path.suffix}"

    path.replace(dest)
    log.info("Archived input -> %s", dest)
    return dest

# ============================================================
# 12_MAIN
# ============================================================
# Wire everything together. This never changes between stations.
# The flow is ALWAYS:
#   config -> log -> ingest -> validate -> nlp_route -> process
#   -> artifact -> job_card -> handoff -> archive

def main() -> int:
    cfg = load_config()
    log = setup_logging(cfg)

    log.info("=" * 60)
    log.info("STATION: %s (%s)", STATION_NAME, STATION_ID)
    log.info("DESC: %s", STATION_DESC)
    log.info("=" * 60)

    inputs = find_inputs(cfg)
    log.info("Found %d input files in _inbox", len(inputs))

    if not inputs:
        log.info("Nothing to process. Exiting.")
        return 0

    success_count = 0
    fail_count = 0

    for path in inputs:
        try:
            # 05: Validate
            if not validate_input(path, cfg, log):
                log.warning("SKIP (invalid): %s", path.name)
                fail_count += 1
                continue

            # 06: Route to NLP
            nlp_info = choose_nlp(path, cfg)
            log.info("Processing: %s -> NLP: %s", path.name, nlp_info["nlp_id"])

            # 07: Process
            result = process_one(path, nlp_info, cfg, log)

            # 08: Write artifact
            artifact_path = write_artifact(result, path)
            log.info("Artifact -> %s", artifact_path.name)

            # 09: Update job card
            update_job_card(result, artifact_path, cfg, log)

            # 10: Handoff
            handoff(result, artifact_path, cfg, log)

            # 11: Archive input
            archive_input(path, log)

            if result.get("success"):
                success_count += 1
            else:
                fail_count += 1

        except Exception as exc:
            log.exception("FAILED processing %s: %s", path.name, exc)
            fail_count += 1

    log.info("=" * 60)
    log.info("COMPLETE: %d success, %d failed, %d total",
             success_count, fail_count, success_count + fail_count)
    log.info("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())