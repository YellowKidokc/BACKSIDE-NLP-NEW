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
WORKFLOWS = _resolve("03_WORKFLOWS", "workflows")    # workflow orchestration
EXPORTS   = _resolve("10_EXPORTS", "exports") / "1 Exports TEST"      # global exports

# Station identity — CHANGE THESE per station
STATION_ID   = "ST_007"
STATION_NAME = "evidence-map"
STATION_DESC = "Map evidence to claims, identify gaps and unsupported claims"

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
# Shared helpers keep the SSS_v1 station files focused on routing and processing.
import re
sys.path.insert(0, str(STATIONS))
from _shared.station_helpers import (
    API_BASE,
    base_result,
    call_nlp,
    cosine,
    data_from_artifact,
    embeddings,
    flesch_reading_ease,
    nlp_route,
    paragraphs,
    read_input,
    sections,
    sentences,
    strip_html,
    text_from_input,
    top_label,
    word_count,
)


def choose_nlp(path: Path, cfg: dict[str, Any]) -> dict[str, Any]:
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================

def process_one(path: Path, nlp_info: dict, cfg: dict[str, Any],
                log: logging.Logger) -> dict[str, Any]:
    result=base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj=read_input(path); data=obj.get("data",obj)
        claims=data.get("falsification_results", data.get("claims", []))
        doc_text=data.get("original_text") or data.get("document") or text_from_input(obj)
        passages=[(i+1,p) for i,p in enumerate(paragraphs(strip_html(doc_text))) if re.search(r"\b(data|study|survey|citation|evidence|results?|analysis|found|show|%|\d)\b", p, re.I)] or [(i+1,p) for i,p in enumerate(paragraphs(strip_html(doc_text)))]
        claim_emb=embeddings(call_nlp("embed", {"texts":[c.get("text","") for c in claims]})) if claims else []
        pass_emb=embeddings(call_nlp("embed", {"texts":[p for _,p in passages]})) if passages else []
        mapped=[]; summary={"SUPPORTED":0,"PARTIAL":0,"UNSUPPORTED":0,"EVIDENCE_GAP":0}
        for idx,c in enumerate(claims):
            sims=sorted([(j,cosine(claim_emb[idx] if idx<len(claim_emb) else [], e)) for j,e in enumerate(pass_emb)], key=lambda x:x[1], reverse=True)[:3]
            matches=[]
            for j,sim in sims:
                status="SUPPORTED" if sim>0.5 else "PARTIAL" if sim>=0.3 else "UNSUPPORTED"
                matches.append({"passage":passages[j][1],"similarity":round(sim,4),"paragraph_index":passages[j][0],"status":status})
            best=matches[0]["similarity"] if matches else 0.0
            coverage="SUPPORTED" if best>0.5 else "PARTIAL" if best>=0.3 else "EVIDENCE_GAP"
            summary[coverage]+=1
            mapped.append({"claim_id":c.get("claim_id"),"text":c.get("text",""),"evidence_matches":matches,"coverage_status":coverage,"best_similarity":best})
        result["data"]={"evidence_map":mapped,"coverage_summary":summary,"orphan_evidence":[]}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
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
# 09_WORKFLOW
# ============================================================
# Update the workflow record so the orchestrator knows this station finished.
# Workflows live at X:\03_WORKFLOWS\{workflow_id}.json

def update_workflow(result: dict[str, Any], artifact_path: Path,
                    cfg: dict[str, Any], log: logging.Logger) -> None:
    workflow_dir = cfg.get("workflow_dir") or WORKFLOWS
    workflow_dir = Path(workflow_dir)

    if not workflow_dir.exists():
        return  # workflows not yet wired — silent skip

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
        export_dir = EXPORTS
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

            # 09: Update workflow
            update_workflow(result, artifact_path, cfg, log)

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