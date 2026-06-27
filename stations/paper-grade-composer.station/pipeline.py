"""
STATION_SCRIPT_STANDARD v1 (SSS_v1)
====================================
Canonical Python template for ALL Theophysics Brain stations.
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
import sys
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Any

# ============================================================
# 00_IMPORTS
# ============================================================

HERE = Path(__file__).resolve().parent
STATIONS = HERE.parent
BRAIN = STATIONS.parent

def _resolve(numbered: str, flat: str) -> Path:
    p = BRAIN / numbered
    return p if p.is_dir() else BRAIN / flat

MODELS = _resolve("05_MODELS", "models")
ENGINES = _resolve("06_ENGINES", "engines")
JOB_CARDS = _resolve("03_JOB_CARDS", "job_cards")
EXPORTS = _resolve("10_EXPORTS", "exports") / "1 Exports TEST"

STATION_ID = "ST_050"
STATION_NAME = "paper-grade-composer"
STATION_DESC = "Composes paper-grade artifacts for dashboard and review outputs"


def load_config() -> dict[str, Any]:
    yaml_path = HERE / "station.yaml"
    json_path = HERE / "config.json"
    if yaml_path.exists():
        try:
            import yaml
            return yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        except ImportError:
            pass
    return json.loads(json_path.read_text(encoding="utf-8-sig"))


def setup_logging(cfg: dict[str, Any]) -> logging.Logger:
    log_dir = HERE / "_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logfile = log_dir / f"{STATION_ID}_{STATION_NAME}_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger(f"{STATION_ID}.{STATION_NAME}")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    return logger


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


def validate_input(path: Path, cfg: dict[str, Any], log: logging.Logger) -> bool:
    if not path.exists() or not path.is_file():
        log.warning("Invalid input: %s", path)
        return False
    if path.stat().st_size == 0:
        log.warning("Empty input: %s", path)
        return False
    return True


def choose_nlp(path: Path, cfg: dict[str, Any]) -> dict[str, Any]:
    workers = cfg.get("workers", {})
    default = workers.get("default", ["NONE"])
    nlp_id = default[0] if isinstance(default, list) and default else str(default or "NONE")
    return {"nlp_id": nlp_id, "nlp_path": None}


def _vectorization_series_id(path: Path, cfg: dict[str, Any]) -> str | None:
    vector_cfg = cfg.get("vectorization", {})
    if isinstance(vector_cfg, dict):
        sid = vector_cfg.get("series_id")
        if sid:
            return str(sid)
    default_series = cfg.get("series_id")
    if default_series:
        return str(default_series)
    return None


def _build_vectorization(path: Path, text: str, cfg: dict[str, Any], log: logging.Logger) -> dict[str, Any]:
    import sys as _sys
    _sys.path.insert(0, str(STATIONS))
    from _shared.station_helpers import build_vectorization_payload

    return build_vectorization_payload(
        text=text,
        cfg=cfg,
        log=log,
        source_file=path.name,
        series_id=_vectorization_series_id(path, cfg),
    )


def _safe_text(raw: Any) -> str:
    if isinstance(raw, str):
        return raw.strip()
    if isinstance(raw, (int, float)):
        return str(raw)
    return ""


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return re.sub(r"-+", "-", slug).strip("-")


def _strip_tags(html_text: str) -> str:
    no_scripts = re.sub(r"(?is)<script.*?>.*?</script>", " ", html_text)
    no_styles = re.sub(r"(?is)<style.*?>.*?</style>", " ", no_scripts)
    text = re.sub(r"<[^>]+>", " ", no_styles)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _read_input_text(path: Path) -> str:
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(payload, dict):
            for key in ("text", "content", "body", "markdown"):
                if key in payload and isinstance(payload[key], str) and payload[key].strip():
                    return _strip_tags(payload[key])
            return _strip_tags(json.dumps(payload, ensure_ascii=False))
        if isinstance(payload, list):
            return _strip_tags("\n\n".join(_safe_text(x) for x in payload))
        return _safe_text(payload)
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in {".html", ".htm"}:
        return _strip_tags(raw)
    return raw


def _extract_sections(text: str) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    if not text:
        return sections
    chunks = re.split(r"\n\n+", text.strip())
    for idx, chunk in enumerate(chunks[:20], 1):
        chunk = chunk.strip()
        if not chunk:
            continue
        sections.append({
            "title": f"Section {idx}",
            "text": chunk[:3000],
            "character_count": len(chunk),
        })
    return sections


def _extract_equations(text: str) -> list[str]:
    equations = []
    equations.extend(re.findall(r"\$[^\$]{3,400}?\$", text))
    equations.extend(re.findall(r"\\\([\s\S]{2,400}?\\\)", text))
    equations.extend(re.findall(r"\\\[[\s\S]{2,400}?\\\]", text))
    cleaned = []
    for eq in equations:
        eq = eq.strip()
        if len(eq) > 6 and eq not in cleaned:
            cleaned.append(eq)
    return cleaned[:12]


def _find_station_output(station_name: str, station_id: str, stem: str) -> tuple[dict[str, Any] | None, Path | None]:
    outbox = STATIONS / station_name / "_outbox"
    if not outbox.is_dir():
        return None, None

    patterns = [
        f"*{station_id}*{stem}*.json",
        f"*{stem}*.json",
        f"*{station_id}*.json",
    ]
    candidates: list[Path] = []
    for pattern in patterns:
        candidates.extend(sorted(outbox.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True))
    if not candidates:
        return None, None
    for path in candidates:
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            if isinstance(data, dict) and "input_file" in data and stem in _safe_text(data.get("input_file")):
                return data, path
        except Exception:
            continue
    fallback = candidates[0]
    return json.loads(fallback.read_text(encoding="utf-8-sig")), fallback


def _compose_claim(row: dict[str, Any], index: int, section_name: str) -> dict[str, Any]:
    label = _safe_text(row.get("claim_maturity_label") or "Structural")
    level = row.get("claim_maturity_level")
    try:
        level_num = int(float(level))
    except (TypeError, ValueError):
        level_num = 3

    return {
        "section": section_name,
        "one_sentence_claim": _safe_text(row.get("one_sentence_claim")) or _safe_text(row.get("claim")) or "No explicit claim sentence extracted.",
        "claim_maturity_level": level_num,
        "claim_maturity_label": label,
        "facts_snapshot": _safe_text(row.get("facts_snapshot")),
        "Q1_identity": _safe_text(row.get("Q1_identity") or "present"),
        "Q2_scope": _safe_text(row.get("Q2_scope") or "scope-present"),
        "Q3_mechanism": _safe_text(row.get("Q3_mechanism") or "inferred"),
        "Q4_evidence": _safe_text(row.get("Q4_evidence") or "mixed"),
        "Q5_falsifiability": _safe_text(row.get("Q5_falsifiability") or "open"),
        "Q6_boundary": _safe_text(row.get("Q6_boundary") or "global-context"),
        "Q7_listener_risk": _safe_text(row.get("Q7_listener_risk") or "medium"),
        "forward_test": _safe_text(row.get("forward_test") or f"Forward consistency test {index}."),
        "reverse_test": _safe_text(row.get("reverse_test") or f"Reverse robustness test {index}."),
        "evidence_bar": _safe_text(row.get("evidence_bar") or "No explicit evidence marker."),
        "kill_conditions": _safe_text(row.get("kill_conditions") or "Open verification conditions pending."),
        "not_claimed": _safe_text(row.get("not_claimed") or "No explicit exclusions provided."),
        "proof_boundary": _safe_text(row.get("proof_boundary") or "Requires empirical and textual boundary checks."),
        "nearby_equation": _safe_text(row.get("nearby_equation") or "No direct equation match."),
    }


def _derive_claims(intelligence: dict[str, Any] | None, proof: dict[str, Any] | None) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []

    proof_scores = _safe_proof_scores(proof)
    if proof_scores:
        pairs = sorted(
            (
                (k, float(v))
                for k, v in proof_scores.items()
                if isinstance(v, (int, float))
            ),
            key=lambda item: item[1],
            reverse=True,
        )[:2]
        for idx, (anchor, score) in enumerate(pairs, 1):
            label = "Formal" if score > 0.07 else "Structural"
            claims.append(
                _compose_claim({
                    "claim": f"Dominant {anchor.replace('_', ' ')} signal is strongest at {score:.4f}",
                    "claim_maturity_level": 5 if score > 0.07 else 4,
                    "claim_maturity_label": label,
                    "facts_snapshot": f"fruit anchor score for {anchor}: {score:.4f}",
                    "Q1_identity": "present",
                    "Q2_scope": "narrow",
                    "Q3_mechanism": "semantic anchor scoring",
                    "Q4_evidence": "no explicit citation",
                    "Q5_falsifiability": "measurable",
                    "Q6_boundary": "within article text",
                    "Q7_listener_risk": "low",
                    "forward_test": "Does this claim cohere across future claims?",
                    "reverse_test": "Does reversing premises break the claim?",
                    "evidence_bar": f"{anchor}: {score:.4f}",
                    "kill_conditions": "No direct refutation marker in current extract.",
                    "not_claimed": "No explicit negation.",
                    "proof_boundary": "Derived from semantic scoring layer.",
                    "nearby_equation": "N/A",
                }, idx, "Proof Scoring")
            )

    if intelligence:
        fd = intelligence.get("data", {}).get("fruit_dynamics", {}) if isinstance(intelligence.get("data"), dict) else intelligence
        text_metrics = fd.get("text_metrics", {}) if isinstance(fd, dict) else {}
        dominant_fruit = _safe_text(text_metrics.get("dominant_fruit") or "faithfulness")
        if dominant_fruit:
            claims.append(
                _compose_claim({
                    "claim": f"Dominant fruit signal trends toward {dominant_fruit}.",
                    "claim_maturity_level": 4,
                    "claim_maturity_label": "Structural",
                    "facts_snapshot": f"dominant fruit = {dominant_fruit}; density = {text_metrics.get('fruit_density', 0)}",
                    "Q1_identity": "present",
                    "Q2_scope": "global",
                    "Q3_mechanism": "token trajectory",
                    "Q4_evidence": "semantic token hits in text",
                    "Q5_falsifiability": "trajectory drift detectable",
                    "Q6_boundary": "article-level",
                    "Q7_listener_risk": "medium",
                    "forward_test": "Can same semantic trajectory reproduce claim sequence?",
                    "reverse_test": "Can reverse trajectory support falsification?",
                    "evidence_bar": f"dominant_fruit={dominant_fruit}",
                    "kill_conditions": "Low fruit_density is a repair target.",
                    "not_claimed": "No formal theorem claim asserted.",
                    "proof_boundary": "Derived from trajectory and density metrics.",
                    "nearby_equation": "N/A",
                }, len(claims) + 1, "Fruit Dynamics")
            )

    return claims[:8]


def _safe_proof_scores(proof_data: dict[str, Any] | None) -> dict[str, float]:
    if not proof_data:
        return {}
    root = proof_data.get("data") if isinstance(proof_data, dict) else {}
    if not isinstance(root, dict):
        return {}
    scores = root.get("scores") if isinstance(root.get("scores"), dict) else None
    if not isinstance(scores, dict):
        return {}
    return scores


def _compose_versions(text: str, claims: list[dict[str, Any]]) -> dict[str, str]:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    academic = " ".join(sentences[:8]) or "No textual content available for academic output."
    easy = " ".join(sentences[:3]) or "No textual content available for plain-language output."
    if easy and len(easy) > 420:
        easy = easy[:420].rsplit(" ", 1)[0] + "..."
    if academic and len(academic) > 900:
        academic = academic[:900].rsplit(" ", 1)[0] + "..."

    top_terms = _top_terms(text)
    claim_summary = ", ".join(c["one_sentence_claim"][:120] for c in claims[:3])
    lossless = {
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "word_count": len(text.split()),
        "top_terms": top_terms,
        "claims_40_limit": len(claims),
        "claim_summary": claim_summary or "No derived claims.",
    }
    return {
        "easy_reading": easy,
        "academic_reading": academic,
        "lossless_summary": json.dumps(lossless, indent=2),
    }


def _top_terms(text: str, top_n: int = 20) -> list[str]:
    words = [w.lower().strip("\"'.,:;()[]{}") for w in re.split(r"\W+", text.lower()) if len(w) > 3]
    common = Counter(words).most_common(top_n)
    return [w for w, _ in common]


def _build_payload(path: Path, text: str, intelligence: dict[str, Any] | None, proof: dict[str, Any] | None) -> dict[str, Any]:
    stem = path.stem
    source_stamp = hashlib.sha256(path.read_bytes()).hexdigest()[:16]

    sections = _extract_sections(text)
    equations = _extract_equations(text)
    claims = _derive_claims(intelligence, proof)

    intel_metrics = {}
    if intelligence and isinstance(intelligence.get("data"), dict):
        intel_metrics = intelligence["data"].get("fruit_dynamics", {})
        if isinstance(intel_metrics, dict) and isinstance(intel_metrics.get("text_metrics"), dict):
            intel_metrics = intel_metrics.get("text_metrics")

    text_words = [w for w in re.split(r"\s+", text) if w]
    metrics = {
        "word_count": len(text_words),
        "char_count": len(text),
        "section_count": len(sections),
        "equation_count": len(equations),
        "claim_candidate_count": len(claims),
        "top_terms": ", ".join(_top_terms(text, 12)),
        "proof_anchor_count": len(_safe_proof_scores(proof)),
        "source_hash": source_stamp,
    }

    if isinstance(intel_metrics, dict):
        metrics.update({
            "fruit_density": intel_metrics.get("fruit_density", 0),
            "dominant_fruit": intel_metrics.get("dominant_fruit", ""),
        })

    versions = _compose_versions(text, claims)
    upstream = {
        "paper_intelligence_stem": _safe_text((intelligence or {}).get("input_file")),
        "paper_proof_stem": _safe_text((proof or {}).get("input_file")),
        "paper_intelligence_success": bool(intelligence and intelligence.get("success", False)),
        "paper_proof_success": bool(proof and proof.get("success", False)),
    }

    station_marks = []
    for source in (intelligence, proof):
        if not isinstance(source, dict):
            continue
        station_marks.append({
            "station_id": _safe_text(source.get("station_name")) or source.get("station_id", "unknown"),
            "status": "OK" if source.get("success", False) else "FAILED",
            "warnings": [*source.get("errors", [])[:3]] if isinstance(source.get("errors"), list) else [],
        })

    payload: dict[str, Any] = {
        "paper_id": stem,
        "source_file": path.name,
        "source_path": str(path),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "metrics": metrics,
        "sections": sections,
        "equations": equations,
        "claims": claims,
        "claims_source": ["paper_intelligence", "paper_proof_grader"],
        "station_marks": station_marks,
        "version_reading": {
            "easy": versions["easy_reading"],
            "academic": versions["academic_reading"],
        },
        "lossless_summary": versions["lossless_summary"],
        "upstream": upstream,
        "proof_scores": _safe_proof_scores(proof),
        "fruit_dynamics": intel_metrics,
    }

    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# Paper Grade Composer: {payload['paper_id']}",
        "",
        f"- Source: `{payload['source_file']}`",
        f"- Generated: `{payload['generated_at']}`",
        "",
        "## Easy Reading",
        "",
        payload["version_reading"].get("easy", ""),
        "",
        "## Academic Version",
        "",
        payload["version_reading"].get("academic", ""),
        "",
        "## Lossless Summary",
        "",
        payload.get("lossless_summary", ""),
        "",
        "## Metrics",
        "",
    ]
    for key, value in payload.get("metrics", {}).items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Claims", ""]) 
    if payload.get("claims"):
        for idx, claim in enumerate(payload["claims"], 1):
            lines.append(f"### Claim {idx}")
            lines.append(f"- Section: {claim.get('section')}")
            lines.append(f"- Claim: {claim.get('one_sentence_claim')}")
            lines.append(f"- Maturity: {claim.get('claim_maturity_level')} / {claim.get('claim_maturity_label')}")
            lines.append(f"- Evidence: {claim.get('evidence_bar')}")
            lines.append(f"- Kill: {claim.get('kill_conditions')}")
            lines.append("")
    else:
        lines.append("No deterministic claims extracted.")

    path.write_text("\n".join(lines), encoding="utf-8")


def process_one(path: Path, nlp_info: dict[str, Any], cfg: dict[str, Any], log: logging.Logger) -> dict[str, Any]:
    result: dict[str, Any] = {
        "input_file": str(path.name),
        "station_id": STATION_ID,
        "station_name": STATION_NAME,
        "nlp_used": nlp_info.get("nlp_id", "NONE"),
        "processed_at": datetime.now().isoformat(timespec="seconds"),
        "success": True,
        "artifacts": [],
        "errors": [],
        "data": {},
        "debug": {},
    }

    try:
        text = _read_input_text(path)
        intel, intel_path = _find_station_output("paper-intelligence-suite.station", "ST_038", path.stem)
        proof, proof_path = _find_station_output("paper-proof-grader.station", "ST_039", path.stem)
        payload = _build_payload(path, text, intel, proof)
        payload["vectorization"] = _build_vectorization(path, text, cfg, log)
        vector_payload = payload.get("vectorization", {})

        outbox = HERE / "_outbox"
        outbox.mkdir(parents=True, exist_ok=True)

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        grade_json = outbox / f"ART_{stamp}__{STATION_ID}__{path.stem}.paper-grade.json"
        grade_md = outbox / f"ART_{stamp}__{STATION_ID}__{path.stem}.paper-grade.md"
        _write_json(grade_json, payload)
        _write_markdown(grade_md, payload)

        snapshot = {
            "paper_id": payload["paper_id"],
            "source_file": payload["source_file"],
            "generated_at": payload["generated_at"],
            "semantic_address": {
                "address": f"proof-dashboard/{payload['paper_id']}",
                "filename_safe": payload["paper_id"],
            },
            "semantic_vector": {"vector": payload["proof_scores"] and str(payload["proof_scores"])[:80] or "N/A"},
            "semantic_hash": {"hash": hashlib.sha256(text.encode('utf-8')).hexdigest()},
            "epistemic_status": {
                "rigor_verdict": "pass" if payload["claims"] else "partial",
                "overall_tier": "composer",
            },
            "math_translation_layer": {
                "status": "derived",
                "translated_spans": payload.get("equations", []),
            },
            "station_marks": payload.get("station_marks", []),
        }
        snapshot_path = outbox / f"ART_{stamp}__{STATION_ID}__{path.stem}.paper-snapshot.json"
        _write_json(snapshot_path, snapshot)

        result["data"] = {
            "paper_grade_payload": payload,
            "vectorization": vector_payload,
            "grade_json_path": str(grade_json),
            "markdown_path": str(grade_md),
            "snapshot_path": str(snapshot_path),
            "upstream_intelligence": _safe_text(str(intel_path)),
            "upstream_proof": _safe_text(str(proof_path)),
        }
        result["artifacts"] = [str(grade_json), str(grade_md), str(snapshot_path)]
        result["debug"] = {
            "slug": payload["paper_id"],
            "upstream_found": {
                "intelligence_found": bool(intel),
                "proof_found": bool(proof),
            },
            "station_marks": payload.get("station_marks", []),
        }
    except Exception as exc:
        log.exception("Processing failed for %s", path.name)
        result["success"] = False
        result["errors"].append(str(exc))
    return result


def write_artifact(result: dict[str, Any], input_path: Path) -> Path:
    outbox = HERE / "_outbox"
    outbox.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact_name = f"ART_{stamp}__{STATION_ID}__{input_path.stem}.json"
    artifact_path = outbox / artifact_name
    artifact_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return artifact_path


def update_job_card(result: dict[str, Any], artifact_path: Path, cfg: dict[str, Any], log: logging.Logger) -> None:
    return None


def handoff(result: dict[str, Any], artifact_path: Path, cfg: dict[str, Any], log: logging.Logger) -> None:
    if cfg.get("outputs", {}).get("final_export", False):
        export_dir = EXPORTS
        export_dir.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(artifact_path, export_dir / artifact_path.name)


def archive_input(path: Path, log: logging.Logger) -> Path:
    archive_dir = HERE / "_processed"
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / (path.name if not re.match(r".+_\d{8}_\d{6}", path.name) else path.name)
    if dest.exists():
        dest = archive_dir / f"{path.stem}_{datetime.now():%Y%m%d_%H%M%S}{path.suffix}"
    path.replace(dest)
    log.info("Archived input -> %s", dest)
    return dest


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
            if not validate_input(path, cfg, log):
                log.warning("SKIP (invalid): %s", path.name)
                fail_count += 1
                continue

            nlp_info = choose_nlp(path, cfg)
            log.info("Processing: %s -> NLP: %s", path.name, nlp_info["nlp_id"])

            result = process_one(path, nlp_info, cfg, log)
            artifact_path = write_artifact(result, path)
            log.info("Artifact -> %s", artifact_path.name)

            update_job_card(result, artifact_path, cfg, log)
            handoff(result, artifact_path, cfg, log)
            archive_input(path, log)

            if result.get("success"):
                success_count += 1
            else:
                fail_count += 1
        except Exception as exc:
            log.exception("FAILED processing %s: %s", path.name, exc)
            fail_count += 1

    log.info("=" * 60)
    log.info("COMPLETE: %d success, %d failed, %d total", success_count, fail_count, success_count + fail_count)
    log.info("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
