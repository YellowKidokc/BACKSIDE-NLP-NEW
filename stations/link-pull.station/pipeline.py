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

# Station identity — CHANGE THESE per station
STATION_ID   = "ST_024"
STATION_NAME = "link-pull"
STATION_DESC = "Processes link pull station inputs"

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
# The ONE action this station performs: Processes link pull station inputs.

def _load_legacy_module() -> Any:
    legacy_path = HERE / "pipeline_legacy.py"
    if not legacy_path.exists():
        raise FileNotFoundError(f"Missing legacy implementation: {legacy_path}")
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"{STATION_NAME}_legacy", legacy_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import legacy implementation: {legacy_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read_input_payload(path: Path) -> Any:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8-sig"))
    return path.read_text(encoding="utf-8", errors="replace")


def _station_output_dir() -> Path:
    out_dir = HERE / "_outbox" / "phase2_logic"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def _fallback_embed_one(text: str, dim: int = 384) -> list[float]:
    import hashlib
    import math
    vector = [0.0] * dim
    tokens = [token.lower() for token in text.split() if len(token) > 2] or [text[:64] or "empty"]
    for token in tokens[:2000]:
        digest = hashlib.sha256(token.encode("utf-8", errors="ignore")).digest()
        idx = int.from_bytes(digest[:4], "little") % dim
        vector[idx] += 1.0
    norm = math.sqrt(sum(value * value for value in vector))
    return [value / norm for value in vector] if norm else vector


def _fallback_classify(text: str, labels: list[str]) -> dict[str, Any]:
    lower = text.lower()
    scored = []
    for label in labels:
        terms = [term for term in label.lower().split() if len(term) > 2]
        hits = sum(1 for term in terms if term in lower)
        scored.append((label, hits / max(len(terms), 1)))
    scored.sort(key=lambda item: item[1], reverse=True)
    top_label, top_score = scored[0] if scored else ("unclassified", 0.0)
    if top_score == 0:
        top_label = "unclassified"
    return {
        "label": top_label,
        "score": float(top_score),
        "labels": [label for label, _ in scored],
        "scores": [float(score) for _, score in scored],
        "engine": "deterministic-fallback",
    }


def _extract_urls(text: str) -> list[str]:
    import re
    return re.findall(r"https?://[^\s)\]>\"']+", text)


def _basic_fetch_url(url: str, timeout: int = 20, max_chars: int = 20000) -> dict[str, Any]:
    from html import unescape
    from urllib.request import Request, urlopen
    import re
    req = Request(url, headers={"User-Agent": "BACKSIDE-NLP/SSS_v1"})
    with urlopen(req, timeout=timeout) as response:
        raw = response.read(max_chars * 4)
        content_type = response.headers.get("content-type", "")
    html = raw.decode("utf-8", errors="replace")
    title_match = re.search(r"(?is)<title[^>]*>(.*?)</title>", html)
    title = unescape(re.sub(r"\s+", " ", title_match.group(1)).strip()) if title_match else ""
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = unescape(re.sub(r"(?s)<[^>]+>", " ", text))
    text = re.sub(r"\s+", " ", text).strip()[:max_chars]
    return {"url": url, "title": title, "content_type": content_type, "text": text}


def _simple_paper_proof_grade(text: str) -> dict[str, Any]:
    import re
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    equation_count = len(re.findall(r"(?:\$[^$]+\$|\\\(|\\\[|=|≤|≥|\\frac|\\sum|\\int)", text))
    claim_terms = ["therefore", "thus", "we prove", "we show", "implies", "theorem", "lemma", "proof"]
    evidence_terms = ["because", "since", "follows", "by", "given", "assume", "derive", "verified"]
    claim_hits = sum(text.lower().count(term) for term in claim_terms)
    evidence_hits = sum(text.lower().count(term) for term in evidence_terms)
    rigor_score = min(1.0, (claim_hits + evidence_hits + equation_count) / max(len(sentences), 1))
    return {
        "sentence_count": len(sentences),
        "equation_count": equation_count,
        "claim_signal_count": claim_hits,
        "evidence_signal_count": evidence_hits,
        "rigor_score": round(rigor_score, 4),
        "grade": "strong" if rigor_score >= 0.35 else "developing" if rigor_score >= 0.15 else "thin",
    }


def process_one(path: Path, nlp_info: dict, cfg: dict[str, Any],
                log: logging.Logger) -> dict[str, Any]:
    """Run the migrated core action for one input file."""
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
        out_dir = _station_output_dir()

        if STATION_NAME == "classify-documents":
            text = path.read_text(encoding="utf-8", errors="replace")
            labels = cfg.get("labels") or [
                "theology", "science", "philosophy", "history",
                "apologetics", "research", "unclassified",
            ]
            vector = _fallback_embed_one(text)
            classification = _fallback_classify(text[: int(cfg.get("max_text_chars", 2000))], labels)
            result["data"] = {
                "action": "classify document",
                "classification": classification,
                "embedding_dim": len(vector),
                "embedding_engine": "deterministic-fallback",
            }

        elif STATION_NAME == "session-handoff-drop":
            legacy = _load_legacy_module()
            text = legacy._read_text(path)
            lines = legacy._normalize_lines(text)
            manifest_items = legacy._manifest_objects(
                legacy._collect_bullets(legacy._extract_layer(lines, ["layer 1", "session manifest"]))
            )
            decision_items = legacy._decision_objects(
                legacy._collect_bullets(legacy._extract_layer(lines, ["layer 2", "decisions and results"]))
            )
            thread_items = legacy._open_thread_objects(
                legacy._collect_bullets(legacy._extract_layer(lines, ["layer 3", "open threads"]))
            )
            session_date = legacy._extract_date(text, cfg.get("default_date", datetime.now().strftime("%Y-%m-%d")))
            ai_partner = cfg.get("default_ai_partner", "Codex")
            markdown = legacy._render_markdown(
                session_date, ai_partner, manifest_items, decision_items, thread_items, path.name, [path.name]
            )
            md_path = out_dir / f"{path.stem}__handoff.md"
            json_path = out_dir / f"{path.stem}__handoff.json"
            md_path.write_text(markdown, encoding="utf-8")
            json_payload = {
                "session_date": session_date,
                "ai_partner": ai_partner,
                "manifest": manifest_items,
                "decisions": decision_items,
                "open_threads": thread_items,
            }
            json_path.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")
            result["artifacts"].extend([str(md_path), str(json_path)])
            result["data"] = json_payload

        elif STATION_NAME == "link-pull":
            payload = _read_input_payload(path)
            if isinstance(payload, dict):
                urls = [payload.get("url") or payload.get("link")] if (payload.get("url") or payload.get("link")) else []
            elif isinstance(payload, list):
                urls = [str(item.get("url", item)) if isinstance(item, dict) else str(item) for item in payload]
            else:
                urls = _extract_urls(str(payload))
            pulled = []
            for url in urls:
                try:
                    item = _basic_fetch_url(str(url), int(cfg.get("timeout", 20)), int(cfg.get("max_chars", 20000)))
                    out_path = out_dir / f"{len(pulled)+1:03d}__link.json"
                    out_path.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
                    result["artifacts"].append(str(out_path))
                    pulled.append(item)
                except Exception as exc:
                    result["errors"].append(f"{url}: {exc}")
            result["success"] = not result["errors"]
            result["data"] = {"action": "pull linked web content", "urls": urls, "pulled": pulled}

        elif STATION_NAME == "harvest-links":
            legacy = _load_legacy_module()
            payload = _read_input_payload(path)
            urls = payload if isinstance(payload, list) else [line.strip() for line in str(payload).splitlines() if line.strip()]
            harvested = []
            for url in urls:
                try:
                    harvested.append(legacy._fetch_and_parse(
                        str(url),
                        cfg.get("user_agent", "BACKSIDE-NLP/SSS_v1"),
                        int(cfg.get("timeout", 20)),
                        cfg.get("strategy", "requests"),
                        int(cfg.get("max_chars", 20000)),
                    ))
                except Exception as exc:
                    result["errors"].append(f"{url}: {exc}")
            result["success"] = not result["errors"]
            result["data"] = {"action": "harvest link text", "urls": urls, "harvested": harvested}

        elif STATION_NAME == "reading-level-glossary":
            legacy = _load_legacy_module()
            analysis = legacy.analyze_file(path, cfg, out_dir)
            result["data"] = {"action": "reading level and glossary analysis", "analysis": analysis}

        elif STATION_NAME == "paper-proof-grader":
            text = path.read_text(encoding="utf-8", errors="replace")
            result["data"] = {"action": "grade paper proof", "grade": _simple_paper_proof_grade(text)}

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