"""
STATION_SCRIPT_STANDARD v1 (SSS_v1)
====================================
Paper Intelligence Suite sub-station wrapper.

This file wraps the existing station script instead of rewriting scoring logic.
Only Section 07 is station-specific.
"""
from __future__ import annotations

# ============================================================
# 00_IMPORTS
# ============================================================
import importlib.util
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# ============================================================
# 01_CONSTANTS
# ============================================================
HERE      = Path(__file__).resolve().parent
SUITE     = HERE.parent
STATIONS  = SUITE.parent
BRAIN     = STATIONS.parent


def _resolve(numbered: str, flat: str) -> Path:
    p = BRAIN / numbered
    return p if p.is_dir() else BRAIN / flat


MODELS    = _resolve("05_MODELS", "models")
ENGINES   = _resolve("06_ENGINES", "engines")
WORKFLOWS = _resolve("03_WORKFLOWS", "workflows")
EXPORTS   = _resolve("10_EXPORTS", "exports")

STATION_ID   = "PI_03"
STATION_NAME = "theophysics-metrics"
STATION_DESC = "Theophysics metrics scoring wrapper"

# ============================================================
# 02_CONFIG
# ============================================================
def load_config() -> dict[str, Any]:
    config_path = HERE / "config.json"
    if config_path.exists():
        return json.loads(config_path.read_text(encoding="utf-8-sig"))
    raise FileNotFoundError(f"Missing config.json for {STATION_NAME}: {config_path}")

# ============================================================
# 03_LOGGING
# ============================================================
def setup_logging(cfg: dict[str, Any]) -> logging.Logger:
    log_dir = HERE / "_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(f"{STATION_ID}.{STATION_NAME}")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = logging.FileHandler(log_dir / f"{STATION_ID}_{STATION_NAME}_{datetime.now():%Y%m%d}.log", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    return logger

# ============================================================
# 04_INGEST
# ============================================================
def find_inputs(cfg: dict[str, Any]) -> list[Path]:
    input_dir = HERE / "_inbox"
    input_dir.mkdir(parents=True, exist_ok=True)
    allowed = {ext.lower() for ext in cfg.get("input_extensions", [])}
    return sorted(
        p for p in input_dir.iterdir()
        if p.is_file() and not p.name.startswith(".") and (not allowed or p.suffix.lower() in allowed)
    )

# ============================================================
# 05_VALIDATE
# ============================================================
def validate_input(path: Path, cfg: dict[str, Any], log: logging.Logger) -> bool:
    if not path.exists() or not path.is_file():
        log.warning("Not a file: %s", path)
        return False
    if path.stat().st_size == 0:
        log.warning("Empty file: %s", path)
        return False
    return True

# ============================================================
# 06_NLP_ROUTE  *** STATION-SPECIFIC ***
# ============================================================
def choose_nlp(path: Path, cfg: dict[str, Any]) -> dict[str, Any]:
    workers = cfg.get("workers", {})
    default = workers.get("default", ["NONE"])
    nlp_id = default[0] if isinstance(default, list) and default else str(default or "NONE")
    return {"nlp_id": nlp_id, "nlp_path": None if nlp_id in {"NONE", "OPENAI", "OLLAMA"} else MODELS / nlp_id}

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def _read_text(path: Path) -> str:
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        return json.dumps(payload, ensure_ascii=False)
    return path.read_text(encoding="utf-8", errors="replace")


def _json_ready(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): _json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_ready(v) for v in value]
    return str(value)


def _load_existing_module(cfg: dict[str, Any]):
    script = HERE / cfg["entrypoint"]["script"]
    module_name = f"{STATION_NAME.replace('-', '_')}_existing"
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    spec = importlib.util.spec_from_file_location(module_name, script)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load existing station script: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_payload(path: Path) -> Any:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8-sig"))
    return _read_text(path)


def _run_existing_logic(path: Path, text: str, cfg: dict[str, Any], log: logging.Logger) -> dict[str, Any]:
    entry = cfg["entrypoint"]
    mode = entry.get("mode", "function_path")
    out_dir = HERE / "_outbox" / path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    if mode == "metadata_only":
        return {"mode": mode, "source_file": path.name, "text_length_chars": len(text), "note": "Web intake station wrapper; FastAPI app remains in app.py."}

    if mode == "subprocess":
        script = HERE / entry["script"]
        completed = subprocess.run([sys.executable, str(script), str(path)], cwd=str(HERE), text=True, capture_output=True)
        return {"mode": mode, "returncode": completed.returncode, "stdout": completed.stdout[-4000:], "stderr": completed.stderr[-4000:]}

    if mode == "subprocess_vault":
        script = HERE / entry["script"]
        vault = text.strip() or str(path)
        completed = subprocess.run([sys.executable, str(script), "--vault", vault, "--output", str(out_dir)], cwd=str(HERE), text=True, capture_output=True)
        return {"mode": mode, "returncode": completed.returncode, "stdout": completed.stdout[-4000:], "stderr": completed.stderr[-4000:], "output_dir": str(out_dir)}

    module = _load_existing_module(cfg)
    func_name = entry.get("function")
    if not func_name:
        raise ValueError(f"Entry point function is required for mode {mode}")
    func = getattr(module, func_name)

    if mode == "function_path_is_path":
        output = func(str(path), is_path=True)
    elif mode == "function_path_outdir":
        output = func(path, out_dir)
    elif mode == "function_text":
        output = func(text)
    elif mode == "graph_builder":
        payload = _load_payload(path)
        rows = payload if isinstance(payload, list) else payload.get("rows", payload.get("papers", [payload])) if isinstance(payload, dict) else []
        output = func(rows, out_dir)
    elif mode == "html_report":
        payload = _load_payload(path)
        if isinstance(payload, str):
            payload = {"file": path.name, "body": payload}
        html = func(payload)
        html_path = out_dir / f"{path.stem}.html"
        html_path.write_text(html, encoding="utf-8")
        output = {"html_file": str(html_path), "html_length": len(html)}
    else:
        output = func(str(path))

    return {"mode": mode, "output": _json_ready(output)}


def process_one(path: Path, nlp_info: dict, cfg: dict[str, Any], log: logging.Logger) -> dict[str, Any]:
    result = {
        "input_file": path.name,
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
        text = _read_text(path)
        data = _run_existing_logic(path, text, cfg, log)
        result["data"] = {
            "action": STATION_DESC,
            "wrapped_script": cfg["entrypoint"]["script"],
            "input_type": path.suffix.lower(),
            "text_length_chars": len(text),
            "result": data,
        }
        log.info("Wrapped %s with %s", path.name, cfg["entrypoint"]["script"])
    except Exception as exc:
        log.exception("Processing failed for %s", path.name)
        result["success"] = False
        result["errors"].append(str(exc))
    return result

# ============================================================
# 08_ARTIFACTS
# ============================================================
def write_artifact(result: dict[str, Any], input_path: Path) -> Path:
    out_dir = HERE / "_outbox"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact = out_dir / f"ART_{stamp}__{STATION_ID}__{input_path.stem}.json"
    artifact.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return artifact

# ============================================================
# 09_JOB_CARD
# ============================================================
def update_job_card(result: dict[str, Any], artifact_path: Path, cfg: dict[str, Any], log: logging.Logger) -> None:
    if cfg.get("outputs", {}).get("update_job_card"):
        log.info("Job-card update requested but not implemented for nested PI wrappers yet.")

# ============================================================
# 10_HANDOFF
# ============================================================
def handoff(result: dict[str, Any], artifact_path: Path, cfg: dict[str, Any], log: logging.Logger) -> None:
    log.info("Artifact ready for orchestrator handoff: %s", artifact_path)

# ============================================================
# 11_ARCHIVE
# ============================================================
def archive_input(path: Path, result: dict[str, Any], cfg: dict[str, Any], log: logging.Logger) -> None:
    processed = HERE / "_processed"
    processed.mkdir(parents=True, exist_ok=True)
    target = processed / path.name
    if target.exists():
        target = processed / f"{path.stem}_{datetime.now():%Y%m%d_%H%M%S}{path.suffix}"
    path.replace(target)
    log.info("Archived %s -> %s", path.name, target)

# ============================================================
# 12_MAIN
# ============================================================
def main() -> int:
    cfg = load_config()
    log = setup_logging(cfg)
    inputs = find_inputs(cfg)
    if not inputs:
        log.info("No inputs found in %s", HERE / "_inbox")
        return 0
    failures = 0
    for path in inputs:
        if not validate_input(path, cfg, log):
            failures += 1
            continue
        nlp_info = choose_nlp(path, cfg)
        result = process_one(path, nlp_info, cfg, log)
        artifact = write_artifact(result, path)
        result["artifacts"].append(str(artifact))
        update_job_card(result, artifact, cfg, log)
        handoff(result, artifact, cfg, log)
        archive_input(path, result, cfg, log)
        if not result.get("success"):
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
