from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "stations" / "STATION_REGISTRY.json"
STATION_OUTPUT_CONTRACT_PATH = Path(__file__).resolve().parent / "station_output_contract.json"
DEFAULT_EXPORT_ROOT = Path(r"\\192.168.2.50\brain\10_EXPORTS\1 Exports TEST")
DEFAULT_STATE_ROOT = Path(r"\\192.168.2.50\brain\Backside\_state\paper-production")
DEFAULT_TIMEOUT_SEC = 600


WORKFLOW_STAGES = [
    {"station": "math-translation-layer", "input_from": "source"},
    {"station": "classify-documents", "input_from": "source"},
    {"station": "plain-language", "input_from": "source"},
    {"station": "claim-extraction", "input_from": "source"},
    {"station": "claim-classification", "input_from": "claim-extraction"},
    {"station": "master-equation-canon", "input_from": "source"},
    {"station": "fruits-spirit-canon", "input_from": "source"},
    {"station": "sbert-embedder", "input_from": "source"},
    {"station": "paper-intelligence-suite", "input_from": "source"},
    {"station": "paper-proof-grader", "input_from": "source"},
]


@dataclass
class StageRun:
    index: int
    station: str
    source: Path
    input_from: str
    status: str
    return_code: int | None
    duration_ms: int
    artifact: Path | None = None
    artifact_payload: dict[str, Any] | None = None
    contract: dict[str, Any] | None = None
    stdout: str = ""
    stderr: str = ""
    error: str = ""


def slug(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", text.strip().lower())
    return re.sub(r"-+", "-", text).strip("-") or "paper"


def _is_json_text(text: str) -> bool:
    return isinstance(text, str) and bool(text.strip())


def _tokenize_text(text: str) -> list[str]:
    return re.findall(r"\b\w+\b", text)


def _count_text_metrics(text: str) -> dict[str, int | float]:
    if not text:
        return {"char_count": 0, "word_count": 0, "sentence_count": 0, "avg_words_per_sentence": 0.0}
    words = _tokenize_text(text)
    if not words:
        word_count = 0
    else:
        word_count = len(words)
    sentence_count = max(1, len(re.findall(r"[.!?]", text)))
    avg_words = round(word_count / sentence_count, 3) if sentence_count else 0.0
    return {
        "char_count": len(text),
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_words_per_sentence": avg_words,
    }


def _collect_text_candidates(value: Any, depth: int = 0, max_depth: int = 2) -> list[str]:
    if depth > max_depth:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        text_values: list[str] = []
        for v in value.values():
            text_values.extend(_collect_text_candidates(v, depth + 1, max_depth))
        return text_values
    if isinstance(value, (list, tuple)):
        text_values: list[str] = []
        for item in value:
            text_values.extend(_collect_text_candidates(item, depth + 1, max_depth))
        return text_values
    return []


def _safe_list(obj: Any) -> list[Any]:
    return obj if isinstance(obj, list) else []


def _safe_dict(obj: Any) -> dict[str, Any]:
    return obj if isinstance(obj, dict) else {}


def _safe_number(obj: Any, default: float = 0.0) -> float:
    try:
        return float(obj)
    except (TypeError, ValueError):
        return default


def extract_station_metrics(station: str, payload: dict[str, Any], duration_ms: int) -> dict[str, Any]:
    data = _safe_dict(payload.get("data"))
    errors = _safe_list(payload.get("errors"))
    metrics: dict[str, Any] = {
        "station": station.replace(".station", ""),
        "success": bool(payload.get("success", False)),
        "duration_ms": duration_ms,
        "artifact_errors": len(errors),
        "artifact_size_bytes": 0,
    }

    # Common numeric summaries
    if "total_claims" in data and isinstance(data["total_claims"], (int, float)):
        metrics["claims_count"] = int(data["total_claims"])
    elif isinstance(data.get("claims"), list):
        metrics["claims_count"] = len(data["claims"])

    if isinstance(data.get("claims_by_type"), dict):
        claims_by_type = {k: v for k, v in data["claims_by_type"].items() if isinstance(v, (int, float))}
        if claims_by_type:
            metrics["claims_by_type_count"] = claims_by_type
            metrics["claim_type_entropy_proxy"] = len(claims_by_type)

    if isinstance(data.get("fruit_count"), (int, float)):
        metrics["fruit_count"] = int(data["fruit_count"])
    if isinstance(data.get("fruits_present"), dict):
        metrics["fruits_detected"] = len(data["fruits_present"])
    if data.get("dominant_fruit"):
        metrics["dominant_fruit"] = str(data["dominant_fruit"])

    if isinstance(data.get("classes"), list):
        metrics["class_count"] = len(data["classes"])
    if isinstance(data.get("predictions"), list):
        metrics["prediction_count"] = len(data["predictions"])
    if isinstance(data.get("summaries"), list):
        metrics["summary_count"] = len(data["summaries"])

    # Score-like arrays
    if isinstance(data.get("seven_q_scores"), list):
        score_entries = [item for item in _safe_list(data.get("seven_q_scores")) if isinstance(item, dict)]
        scores = [ _safe_number(item.get("score")) for item in score_entries if isinstance(item.get("score"), (int, float, str))]
        if scores:
            metrics["seven_q_score_count"] = len(scores)
            metrics["seven_q_max_score"] = max(scores)
            metrics["seven_q_mean_score"] = round(sum(scores) / len(scores), 4)

    if isinstance(data.get("full_ranking"), list):
        score_entries = [item for item in _safe_list(data.get("full_ranking")) if isinstance(item, dict)]
        scores = [ _safe_number(item.get("score")) for item in score_entries if isinstance(item.get("score"), (int, float, str))]
        if scores:
            metrics["ranking_count"] = len(scores)
            metrics["ranking_top_score"] = max(scores)
            metrics["ranking_mean_score"] = round(sum(scores) / len(scores), 4)

    if isinstance(data.get("master_equation_components"), list):
        metrics["equation_component_count"] = len(data["master_equation_components"])
    if isinstance(data.get("vectors"), list):
        metrics["vector_count"] = len(data["vectors"])

    if isinstance(data.get("classifier_score"), (int, float)):
        metrics["classifier_score"] = round(_safe_number(data["classifier_score"]), 4)
    if isinstance(data.get("score"), (int, float)):
        metrics["score"] = round(_safe_number(data["score"]), 4)

    # Text coverage (compact, station-agnostic)
    text_bits = [txt for txt in _collect_text_candidates(payload) if _is_json_text(txt)]
    if text_bits:
        merged = " ".join(text_bits)
        if len(merged) > 32000:
            merged = merged[:32000]
        metrics["text_metrics"] = _count_text_metrics(merged)

    return metrics


def build_quality_markdown(
    source: Path, bundle: dict[str, Any], station_metrics: list[dict[str, Any]]
) -> str:
    easy_chars = len(bundle.get("easy_version") or "")
    academic_chars = len(bundle.get("academic_version") or "")
    lines = [
        "# Paper Production Summary",
        "",
        f"- Source: `{source.name}`",
        f"- Total stages run: `{bundle.get('stage_count', 0)}`",
        f"- Pass stages: `{bundle.get('pass_stage_count', 0)}`",
        f"- Fail stages: `{bundle.get('fail_stage_count', 0)}`",
        "",
        "## Quantifiable summary",
        "",
    ]
    if easy_chars or academic_chars:
        lines.append(f"- Easy version chars: `{easy_chars}`")
        lines.append(f"- Academic version chars: `{academic_chars}`")
    if bundle.get("lossless_summary"):
        lines.append(f"- Lossless summary chars: `{len(bundle['lossless_summary'])}`")
    lines.append("")
    if station_metrics:
        lines.append("| station | duration_ms | metrics |")
        lines.append("| --- | ---: | --- |")
        for item in station_metrics:
            short = ", ".join(f"{k}:{v}" for k, v in item.items() if k in {"claims_count", "fruit_count", "ranking_top_score", "seven_q_max_score", "score", "artifact_errors"} and v is not None)
            lines.append(f"| `{item['station']}` | {item.get('duration_ms', 0)} | {short or 'n/a'} |")
    return "\n".join(lines) + "\n"


def load_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"STATION_REGISTRY.json not found: {REGISTRY_PATH}")
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def load_station_output_contracts() -> dict[str, Any]:
    if not STATION_OUTPUT_CONTRACT_PATH.exists():
        return {}
    try:
        return json.loads(STATION_OUTPUT_CONTRACT_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def station_path(registry: dict[str, Any], station_name: str) -> Path:
    entry = registry.get("stations", {}).get(station_name)
    if not entry:
        raise KeyError(f"Station not found in registry: {station_name}")
    requested = Path(entry["path"])
    if requested.exists():
        return requested

    candidates: list[Path] = []
    raw_path = str(requested)
    posix_path = requested.as_posix()

    if requested.is_absolute() and requested.drive.upper() == "X":
        relative = posix_path[3:].lstrip("/\\")
        if relative:
            candidates.append(Path(r"\\192.168.2.50\brain") / Path(relative))

    if posix_path.startswith("//192.168.2.50/brain/") or raw_path.startswith("\\\\192.168.2.50\\brain\\"):
        relative = posix_path.split("/brain/", 1)[-1]
        if relative and relative != posix_path:
            candidates.append(Path(r"\\192.168.2.50\brain") / Path(relative))

    candidates.extend(
        [
            REPO_ROOT / "stations" / f"{station_name}.station",
            REPO_ROOT / "stations" / requested.name,
            REPO_ROOT / "stations" / station_name,
        ]
    )

    # Deduplicate while preserving order.
    unique: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        unique.append(candidate)

    for candidate in unique:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(f"Station path missing: {requested}")


def ensure_station_dirs(station_dir: Path) -> tuple[Path, Path, Path, Path]:
    inbox = station_dir / "_inbox"
    outbox = station_dir / "_outbox"
    processed = station_dir / "_processed"
    logs = station_dir / "_logs"
    for path in (inbox, outbox, processed, logs):
        path.mkdir(parents=True, exist_ok=True)
    return inbox, outbox, processed, logs


def load_station_extensions(station_dir: Path) -> set[str]:
    cfg_path = station_dir / "config.json"
    if not cfg_path.exists():
        return set()
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    raw = cfg.get("input_extensions", []) or cfg.get("inputs", {}).get("extensions", [])
    return {str(ext).lower() for ext in raw}


def normalize_input(station_dir: Path, source: Path) -> Path:
    exts = load_station_extensions(station_dir)
    if not exts or source.suffix.lower() in exts:
        return source
    if source.suffix.lower() in {".html", ".htm"} and {".md", ".txt"} & exts:
        html = source.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
        text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        normalized = source.with_suffix(".md")
        normalized.write_text(text, encoding="utf-8")
        return normalized
    if not exts:
        return source
    raise ValueError(f"Station {station_dir.name} does not accept input suffix {source.suffix.lower()}; configured accepts {sorted(exts)}")


def clean_inbox(inbox: Path) -> None:
    for entry in list(inbox.iterdir()):
        if entry.is_file():
            entry.unlink()


def list_outbox_files(outbox: Path) -> list[Path]:
    return sorted((p for p in outbox.iterdir() if p.is_file()), key=lambda p: p.name)


def latest_artifact_for_stage(station_dir: Path, since: float, outbox_files_before: set[Path]) -> Path | None:
    outbox = station_dir / "_outbox"
    candidates = [p for p in outbox.iterdir() if p.is_file() and p.suffix.lower() == ".json"]
    fresh = [p for p in candidates if p not in outbox_files_before]
    if fresh:
        return sorted(fresh, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    fresh_by_time = [p for p in candidates if p.stat().st_mtime >= since - 1e-3]
    if fresh_by_time:
        return sorted(fresh_by_time, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    return None


def copy_stage_input(station_dir: Path, source: Path, stage_label: str) -> Path:
    inbox, _, _, _ = ensure_station_dirs(station_dir)
    clean_inbox(inbox)
    destination = inbox / f"{stage_label}{source.suffix.lower()}"
    return shutil.copy2(source, destination)


def run_station(station_dir: Path, source: Path, stage_label: str, timeout: int, contract: dict[str, Any] | None = None) -> StageRun:
    start = time.time()
    pipeline = station_dir / "pipeline.py"
    if not pipeline.exists():
        raise FileNotFoundError(f"pipeline.py missing in station folder: {station_dir}")

    _, outbox, _, _ = ensure_station_dirs(station_dir)
    outbox_snapshot = set(list_outbox_files(outbox))

    source_for_station = normalize_input(station_dir, source)
    copied = copy_stage_input(station_dir, source_for_station, stage_label)
    try:
        proc = subprocess.run(
            [sys.executable, "pipeline.py"],
            cwd=str(station_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        rc = proc.returncode
        out = proc.stdout or ""
        err = proc.stderr or ""
    except subprocess.TimeoutExpired as exc:
        return StageRun(
            index=0,
            station=station_dir.name,
            source=source,
            input_from="",
            status="fail",
            return_code=None,
            duration_ms=int((time.time() - start) * 1000),
            artifact=None,
            artifact_payload=None,
            contract=contract,
            stdout="",
            stderr=str(exc),
            error=f"timeout after {timeout}s",
        )
    except Exception as exc:  # pragma: no cover - platform-specific failures
        return StageRun(
            index=0,
            station=station_dir.name,
            source=source,
            input_from="",
            status="fail",
            return_code=None,
            duration_ms=int((time.time() - start) * 1000),
            artifact=None,
            artifact_payload=None,
            contract=contract,
            stdout="",
            stderr="",
            error=str(exc),
        )

    artifact = latest_artifact_for_stage(station_dir, start, outbox_snapshot)
    if rc != 0:
        return StageRun(
            index=0,
            station=station_dir.name.replace(".station", ""),
            source=source,
            input_from="",
            status="fail",
            return_code=rc,
            duration_ms=int((time.time() - start) * 1000),
            artifact=artifact,
            artifact_payload=None,
            contract=contract,
            stdout=out[:1200],
            stderr=err[:1200],
            error=f"{copied.name}: exit_code_{rc}",
        )
    if artifact is None:
        return StageRun(
            index=0,
            station=station_dir.name.replace(".station", ""),
            source=source,
            input_from="",
            status="fail",
            return_code=rc,
            duration_ms=int((time.time() - start) * 1000),
            artifact=None,
            artifact_payload=None,
            contract=contract,
            stdout=out[:1200],
            stderr=err[:1200],
            error="no json artifact found in _outbox",
        )
    status = "pass"
    try:
        payload = json.loads(artifact.read_text(encoding="utf-8"))
        if payload.get("success") is False:
            status = "fail"
            if artifact.exists():
                errors = payload.get("errors", [])
                if isinstance(errors, list) and errors:
                    error_text = "; ".join(str(x) for x in errors[:3])
                else:
                    error_text = "station payload reported success=false"
            else:
                error_text = "station payload malformed"
        else:
            error_text = ""
    except Exception as exc:
        status = "fail"
        error_text = f"artifact parse failed: {exc}"
        payload = None

    return StageRun(
        index=0,
        station=station_dir.name.replace(".station", ""),
        source=source,
        input_from="",
        status=status,
        return_code=rc,
        duration_ms=int((time.time() - start) * 1000),
        artifact=artifact,
        artifact_payload=payload,
        contract=contract,
        stdout=out[:1200],
        stderr=err[:1200],
        error=error_text,
    )


def pick_latest(source: Path) -> Path:
    if source.is_file():
        return source
    if not source.is_dir():
        raise ValueError(f"Input is not file or directory: {source}")
    files = sorted((p for p in source.iterdir() if p.is_file()), key=lambda p: p.name)
    if not files:
        raise ValueError(f"No files in input directory: {source}")
    return files[0]


def select_inputs(input_root: Path, glob: str | None, max_files: int | None) -> list[Path]:
    if input_root.is_file():
        return [input_root]
    pattern = glob or "*.*"
    files = sorted(input_root.glob(pattern))
    if max_files is not None:
        return files[:max_files]
    return files


def make_run_id(source: Path) -> str:
    digest = hashlib.sha1(f"{source}:{source.stat().st_mtime_ns}".encode("utf-8")).hexdigest()[:10]
    return f"{datetime.now():%Y%m%d-%H%M%S}_{slug(source.stem)}_{digest}"


def resolve_stage_run_file_name(station: str, source: Path, index: int, artifact: Path) -> str:
    safe_station = station.replace(" ", "_")
    return f"{index:02d}__{safe_station}__{source.stem}__{artifact.stem}.json"


def build_output_bundle(run_dir: Path, stage_artifacts: list[tuple[StageRun, Path]]) -> dict[str, Any]:
    bundle: dict[str, Any] = {
        "easy_version": None,
        "academic_version": None,
        "lossless_summary": None,
        "tags": {},
        "master_equation": None,
        "fruits": None,
        "grade": None,
    }
    for _, artifact in stage_artifacts:
        if not artifact.exists():
            continue
        try:
            payload = json.loads(artifact.read_text(encoding="utf-8"))
        except Exception:
            continue
        station = payload.get("station_name", "")
        data = payload.get("data", {})
        if station == "plain-language":
            versions = data.get("versions", {})
            bundle["easy_version"] = versions.get("easy", {}).get("text") or versions.get("grade_8", {}).get("text")
            bundle["academic_version"] = versions.get("academic", {}).get("text")
        if station == "claim-classification":
            bundle["tags"]["maturity_distribution"] = data.get("maturity_distribution")
            bundle["tags"]["domain_distribution"] = data.get("domain_distribution")
        if station == "master-equation-canon":
            bundle["master_equation"] = data
        if station == "fruits-spirit-canon":
            bundle["fruits"] = data
        if station == "paper-proof-grader":
            bundle["grade"] = data
    bundle["lossless_summary"] = (
        (bundle["easy_version"] or "")[:420] + "..."
        if bundle["easy_version"] and len(bundle["easy_version"]) > 420
        else bundle["easy_version"]
    )

    summary_path = run_dir / "paper_output_bundle.json"
    summary_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    return bundle


def run_pipeline_for_source(
    source: Path,
    args: argparse.Namespace,
    registry: dict[str, Any],
    station_output_contracts: dict[str, Any],
) -> dict[str, Any]:
    source = source.resolve()
    run_id = make_run_id(source)
    export_root = args.export_root.resolve()
    run_dir = export_root / run_id
    export_root.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)
    state_dir = args.state_root / run_id
    state_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir = run_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    source_copy = state_dir / source.name
    shutil.copy2(source, source_copy)

    stage_artifact_rows: list[tuple[StageRun, Path]] = []
    contract_snapshot: dict[str, Any] = {}
    stage_metrics: list[dict[str, Any]] = []
    stage_by_name: dict[str, Path] = {}
    selected = [s for s in WORKFLOW_STAGES if not args.stages or s["station"] in set(args.stages)]

    manifest_stages: list[dict[str, Any]] = []
    overall_status = "pass"
    for i, stage in enumerate(selected, start=1):
        station_name = stage["station"]
        input_from = stage["input_from"]
        if input_from == "source":
            stage_input = source_copy
        elif input_from == "claim-extraction":
            stage_input = stage_by_name.get("claim-extraction")
            if stage_input is None:
                overall_status = "fail"
                manifest_stages.append({
                    "index": i,
                    "station": station_name,
                    "status": "skipped",
                    "reason": "missing required upstream claim-extraction artifact",
                })
                break
        else:
            stage_input = source_copy

        station_dir = station_path(registry, station_name)
        station_contract = station_output_contracts.get(station_name)
        try:
            stage_result = run_station(
                station_dir,
                stage_input,
                f"{i:02d}_{station_name}",
                args.timeout,
                contract=station_contract,
            )
        except Exception as exc:
            stage_result = StageRun(
                index=i,
                station=station_name,
                source=stage_input,
                input_from=input_from,
                status="fail",
                return_code=None,
                duration_ms=0,
                artifact=None,
                artifact_payload=None,
                contract=station_contract,
                stdout="",
                stderr="",
                error=str(exc),
            )
        stage_result.index = i
        stage_result.input_from = input_from

        stage_record = {
            "index": i,
            "station": station_name,
            "input_from": input_from,
            "status": stage_result.status,
            "return_code": stage_result.return_code,
            "duration_ms": stage_result.duration_ms,
        "source": str(stage_result.source),
            "artifact": str(stage_result.artifact) if stage_result.artifact else None,
            "output_contract": stage_result.contract,
            "error": stage_result.error,
            "stdout": stage_result.stdout,
            "stderr": stage_result.stderr,
        }
        manifest_stages.append(stage_record)

        if stage_result.status != "pass":
            overall_status = "fail" if stage_result.status == "fail" else overall_status
            if args.fail_fast:
                break
            if stage_result.artifact is None:
                if args.fail_fast:
                    break

        if stage_result.artifact:
            copied = artifacts_dir / resolve_stage_run_file_name(station_name, stage_input, i, stage_result.artifact)
            shutil.copy2(stage_result.artifact, copied)
            stage_by_name[station_name] = copied
            stage_artifact_rows.append((stage_result, copied))
            if station_result_contract := stage_result.contract:
                contract_snapshot[station_name] = station_result_contract
            if stage_result.artifact_payload is not None and isinstance(stage_result.artifact_payload, dict):
                stage_metrics.append(extract_station_metrics(station_name, stage_result.artifact_payload, stage_result.duration_ms))
            else:
                try:
                    stage_metrics.append(
                        extract_station_metrics(
                            station_name,
                            json.loads(stage_result.artifact.read_text(encoding="utf-8")),
                            stage_result.duration_ms,
                        )
                    )
                except Exception:
                    stage_metrics.append(
                        {
                            "station": station_name.replace(".station", ""),
                            "success": stage_result.status == "pass",
                            "duration_ms": stage_result.duration_ms,
                            "artifact_errors": 1 if stage_result.error else 0,
                        }
                    )
        else:
            stage_metrics.append(
                {
                    "station": station_name.replace(".station", ""),
                    "success": stage_result.status == "pass",
                    "duration_ms": stage_result.duration_ms,
                    "artifact_errors": 1 if stage_result.error else 0,
                }
            )
        if args.progress:
            print(
                f"[{run_id}] {i:02d}/{len(selected)} {station_name}: {stage_result.status}"
            )

    manifest = {
        "run_id": run_id,
        "source": str(source),
        "source_mtime": source.stat().st_mtime,
        "started_at": datetime.fromtimestamp(time.time()).isoformat(timespec="seconds"),
        "status": overall_status,
        "bundle_json": str(run_dir / "paper_output_bundle.json"),
        "bundle_markdown": str(run_dir / "paper_output_bundle.md"),
        "stages": manifest_stages,
        "args": {k: str(v) for k, v in vars(args).items()},
        "station_count": len(selected),
    }

    out_bundle = build_output_bundle(run_dir, stage_artifact_rows)
    out_bundle["stage_contracts"] = contract_snapshot
    out_bundle["all_station_contracts_available"] = len(station_output_contracts)
    out_bundle["stage_count"] = len(selected)
    out_bundle["pass_stage_count"] = sum(1 for stage in manifest_stages if stage["status"] == "pass")
    out_bundle["fail_stage_count"] = sum(1 for stage in manifest_stages if stage["status"] == "fail")
    out_bundle["stage_metrics"] = stage_metrics

    quality_markdown = build_quality_markdown(source_copy, out_bundle, stage_metrics)
    markdown_path = run_dir / "paper_output_bundle.md"
    markdown_path.write_text(quality_markdown, encoding="utf-8")
    manifest["bundle"] = {
        "easy_version_len": len(out_bundle["easy_version"] or ""),
        "academic_version_len": len(out_bundle["academic_version"] or ""),
        "lossless_summary_len": len(out_bundle["lossless_summary"] or ""),
    }

    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run paper-production station chain.")
    parser.add_argument("--input", type=Path, help="Input file.")
    parser.add_argument("--input-root", "--input_root", dest="input_root", type=Path, help="Input folder for batch mode.")
    parser.add_argument("--glob", default=None, help="Glob filter when using --input-root.")
    parser.add_argument("--export-root", type=Path, default=DEFAULT_EXPORT_ROOT)
    parser.add_argument("--state-root", type=Path, default=DEFAULT_STATE_ROOT)
    parser.add_argument("--max-files", type=int, default=1, help="Max files in batch mode.")
    parser.add_argument("--fail-fast", action="store_true", help="Stop workflow on first failed station.")
    parser.add_argument("--progress", action="store_true", help="Print per-stage progress while running.")
    parser.add_argument(
        "--stages",
        nargs="*",
        help="Optional subset of station names to run, in declared workflow order. Example: plain-language claim-extraction claim-classification.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.environ.get("STATION_TIMEOUT", str(DEFAULT_TIMEOUT_SEC))),
        help="Per-station timeout in seconds.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input and not args.input_root:
        raise SystemExit("--input or --input-root required")

    registry = load_registry()
    station_output_contracts = load_station_output_contracts()
    inputs: list[Path]
    if args.input:
        inputs = [args.input]
    else:
        inputs = select_inputs(args.input_root, args.glob, args.max_files)

    run_results = []
    for source in inputs:
        if not source.exists():
            print(f"Skipping missing file: {source}")
            continue
        result = run_pipeline_for_source(source, args, registry, station_output_contracts)
        run_results.append(result)
        print(f"Done: {source.name} -> status={result['status']} stages={len(result['stages'])}")

    summary = {
        "workflow": "paper-production",
        "run_time": datetime.now().isoformat(timespec="seconds"),
        "completed": len(run_results),
        "results": [
            {
                "source": row["source"],
                "run_id": row["run_id"],
                "status": row["status"],
                "stage_count": row["station_count"],
            }
            for row in run_results
        ],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if all(item["status"] == "pass" for item in run_results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
