"""
station_helpers.py — Shared utilities for all SSS_v1 stations.
POF 2828 | 2026-06-17

Import in any station: from _shared.station_helpers import *
"""
from __future__ import annotations
import json, math, re, logging
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

API_BASE = "http://localhost:8700/nlp"
API_TIMEOUT = 120
_VECTOR_STATE_ROOT = Path(__file__).resolve().parent.parent / "_state" / "paper_vectors"
_VECTOR_SCHEMA_VERSION = "v1"


def api_call(endpoint: str, payload: dict[str, Any], timeout: int = API_TIMEOUT) -> dict[str, Any]:
    """Call the shared NLP FastAPI service."""
    response = requests.post(f"{API_BASE}/{endpoint}", json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()


def read_input(path: Path) -> Any:
    """Read a file, auto-detect JSON vs text."""
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return text


def text_from_input(obj: Any) -> str:
    """Extract plain text from any input (string, JSON artifact, etc)."""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        data = obj.get("data", obj)
        for key in ("text", "document", "original_text", "content", "summary"):
            if isinstance(data.get(key), str):
                return data[key]
        if isinstance(data.get("versions"), dict):
            return data["versions"].get("academic", {}).get("text", "")
    return json.dumps(obj, ensure_ascii=False)


def strip_html(text: str) -> str:
    """Remove HTML tags, scripts, styles."""
    if "<" not in text or ">" not in text:
        return text
    text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]


def split_sections(text: str) -> list[dict[str, Any]]:
    """Split markdown text into sections by headings."""
    sections = []
    current = {"heading": "Introduction", "text": []}
    for line in text.splitlines():
        m = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$", line)
        if m:
            if current["text"]:
                sections.append({"heading": current["heading"],
                                 "text": "\n".join(current["text"]).strip()})
            current = {"heading": m.group(2).strip(), "text": []}
        else:
            current["text"].append(line)
    if current["text"] or not sections:
        sections.append({"heading": current["heading"],
                         "text": "\n".join(current["text"]).strip()})
    return sections


def score_map(api_result: dict[str, Any]) -> dict[str, float]:
    """Extract label->score dict from API classification result."""
    labels = api_result.get("labels") or api_result.get("classes") or []
    scores = api_result.get("scores") or api_result.get("probabilities") or []
    if isinstance(scores, dict):
        return {str(k): float(v) for k, v in scores.items()}
    return {str(label): float(score) for label, score in zip(labels, scores)}


def top_label(api_result: dict[str, Any], default: str = "unknown") -> tuple[str, float, dict[str, float]]:
    """Get the highest-scoring label from a classification result."""
    scores = score_map(api_result)
    if scores:
        label = max(scores, key=scores.get)
        return label, scores[label], scores
    label = str(api_result.get("label") or api_result.get("class") or default)
    return label, float(api_result.get("score", 0.0) or 0.0), {label: float(api_result.get("score", 0.0) or 0.0)}


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    n = min(len(a), len(b))
    dot = sum(float(a[i]) * float(b[i]) for i in range(n))
    na = math.sqrt(sum(float(a[i]) ** 2 for i in range(n)))
    nb = math.sqrt(sum(float(b[i]) ** 2 for i in range(n)))
    return dot / (na * nb) if na and nb else 0.0


def extract_embeddings(api_result: dict[str, Any]) -> list[list[float]]:
    value = api_result.get("embeddings", api_result.get("embedding", []))
    if value and isinstance(value[0], (int, float)):
        return [value]
    return value or []


def _sanitize_vector_input(text: str, max_chars: int = 30000) -> str:
    """Sanitize and trim text for vectorization payloads."""
    if not isinstance(text, str):
        return ""
    txt = text.strip()
    if max_chars and len(txt) > max_chars:
        txt = txt[:max_chars]
    return " ".join(txt.split())


def _normalize_embedding_payload(raw: Any, expected_dim: int | None = None) -> tuple[list[float], int]:
    """Normalize unknown embedding response shapes into a single vector."""
    vecs = extract_embeddings(raw if isinstance(raw, dict) else {"embeddings": raw})
    vector: list[float] = []
    if vecs and isinstance(vecs[0], list):
        vector = [float(v) for v in vecs[0] if isinstance(v, (int, float))]
    if expected_dim and len(vector) > expected_dim:
        vector = vector[:expected_dim]
    if expected_dim and len(vector) < expected_dim:
        vector = vector + [0.0] * (expected_dim - len(vector))
    return vector, len(vector)


def _safe_load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8-sig") as fp:
            data = json.load(fp)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _build_series_context(series_id: str | None, source_file: str | None,
                         cfg: dict[str, Any], log: logging.Logger | None) -> dict[str, Any]:
    series_cfg = cfg.get("series", {}) if isinstance(cfg, dict) else {}
    if not series_id or not series_cfg:
        return {"enabled": False}

    enabled = bool(series_cfg.get("enabled", True))
    method = series_cfg.get("method", "running_mean")
    state = {
        "enabled": bool(enabled),
        "series_id": series_id,
        "method": method,
        "source_file": source_file or "",
    }
    if not enabled:
        return state

    try:
        _VECTOR_STATE_ROOT.mkdir(parents=True, exist_ok=True)
        state_file = _VECTOR_STATE_ROOT / f"{series_id}.json"
        payload = _safe_load_json(state_file)
        docs = payload.get("documents") if isinstance(payload.get("documents"), list) else []
        docs.append({
            "source_file": source_file or "",
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        })
        payload = {
            "series_id": series_id,
            "method": method,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "document_count": len(docs),
            "documents": docs[-int(series_cfg.get("window", 200)):],
        }
        state_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        state.update(payload)
    except Exception as exc:
        if log:
            log.warning("Series vector state write failed: %s", exc)
    return state


def build_vectorization_payload(text: str, cfg: dict[str, Any], log: logging.Logger | None = None,
                               *, source_file: str | None = None,
                               series_id: str | None = None) -> dict[str, Any]:
    """Build a normalized vectorization object for downstream exporters/stores."""
    if log is None:
        log = logging.getLogger("vectorization")

    cfg = cfg or {}
    vcfg = cfg.get("vectorization", {})
    if not isinstance(vcfg, dict) or not vcfg.get("enabled", True):
        return {
            "enabled": False,
            "schema_version": _VECTOR_SCHEMA_VERSION,
            "reason": "disabled",
        }

    if not isinstance(text, str):
        text = text_from_input(text)
    safe_text = _sanitize_vector_input(text, max_chars=int(vcfg.get("max_chars", 30000)))
    if not safe_text:
        return {
            "enabled": False,
            "schema_version": _VECTOR_SCHEMA_VERSION,
            "reason": "empty_input",
        }

    try:
        embedding_result = call_nlp("embed", {"texts": [safe_text]})
    except Exception as exc:
        if log:
            log.warning("Vectorization failed: %s", exc)
        return {
            "enabled": False,
            "schema_version": _VECTOR_SCHEMA_VERSION,
            "reason": "embed_error",
            "error": str(exc),
        }

    vector, dim = _normalize_embedding_payload(
        embedding_result,
        expected_dim=int(vcfg.get("expected_dim", 0)) or None,
    )
    if not vector:
        return {
            "enabled": False,
            "schema_version": _VECTOR_SCHEMA_VERSION,
            "reason": "no_vector",
        }

    resolved_series_id = series_id or str(vcfg.get("series_id", "")) or cfg.get("series_id")
    series_ctx = _build_series_context(
        resolved_series_id or None,
        source_file,
        cfg=cfg,
        log=log,
    )
    return {
        "enabled": True,
        "schema_version": _VECTOR_SCHEMA_VERSION,
        "paper": {
            "source_file": source_file or "",
            "text_length": len(safe_text),
            "word_count": word_count(safe_text),
            "expected_dimension": dim,
            "requested_dimension": int(vcfg.get("expected_dim", dim) or dim),
            "model": vcfg.get("model", "m01_embedder"),
            "method": vcfg.get("method", "embed"),
        },
        "vector": vector,
        "series_context": series_ctx,
    }


def base_result(path: Path, station_id: str, station_name: str,
                nlp_info: dict[str, Any],
                cfg: dict[str, Any] | None = None,
                log: logging.Logger | None = None) -> dict[str, Any]:
    """Create the standard artifact envelope."""
    if cfg is None:
        cfg = {}
        try:
            station_dir = Path(path).resolve().parent.parent
            cfg_path = station_dir / "config.json"
            if cfg_path.exists():
                cfg = _safe_load_json(cfg_path)
        except Exception:
            cfg = {}

        if not isinstance(cfg, dict):
            cfg = {}

    try:
        vectorization = build_vectorization_payload(
            text_from_input(read_input(path)),
            cfg,
            log,
            source_file=path.name,
            series_id=cfg.get("series_id"),
        )
    except Exception as exc:
        if log:
            log.warning("Vectorization attach failed: %s", exc)
        vectorization = {
            "enabled": False,
            "schema_version": _VECTOR_SCHEMA_VERSION,
            "reason": "vectorization_exception",
            "error": str(exc),
        }

    return {
        "input_file": str(path.name),
        "station_id": station_id,
        "station_name": station_name,
        "nlp_used": nlp_info.get("nlp_id", "NONE"),
        "api_endpoint": nlp_info.get("api_endpoint"),
        "processed_at": datetime.now().isoformat(timespec="seconds"),
        "success": True,
        "artifacts": [],
        "errors": [],
        "vectorization": vectorization,
        "data": {},
    }


def is_likely_claim(sentence: str) -> bool:
    """Quick prefilter: skip sentences unlikely to be claims."""
    s = sentence.strip()
    if len(s.split()) < 6:
        return False
    skip_starts = ("in this section", "next we", "for example",
                   "see also", "note that", "figure ", "table ",
                   "as shown", "as discussed", "let us", "we will")
    sl = s.lower()
    if any(sl.startswith(p) for p in skip_starts):
        return False
    return True


# ─── Aliases for Codex pipeline imports ───
call_nlp = api_call
sentences = split_sentences
paragraphs = split_paragraphs
sections = split_sections
cosine = cosine_similarity
embeddings = extract_embeddings


def data_from_artifact(obj: Any) -> dict[str, Any]:
    """Extract the data dict from an upstream artifact."""
    if isinstance(obj, dict):
        return obj.get("data", obj)
    return {}


def flesch_reading_ease(text: str) -> float:
    """Approximate Flesch Reading Ease score."""
    sents = split_sentences(text)
    words = re.findall(r"\b\w+\b", text)
    if not sents or not words:
        return 0.0
    syllable_count = sum(
        max(1, len(re.findall(r"[aeiouy]+", w.lower())))
        for w in words
    )
    asl = len(words) / len(sents)
    asw = syllable_count / len(words)
    return 206.835 - 1.015 * asl - 84.6 * asw


def nlp_route(api_base: str, models_dir, cfg: dict[str, Any],
              default_nlp: str = "NONE",
              endpoint: str = "classify") -> dict[str, Any]:
    """Build NLP routing info dict for choose_nlp()."""
    nlp_id = cfg.get("nlp_id", default_nlp)
    return {
        "nlp_id": nlp_id,
        "nlp_path": Path(str(models_dir)) / cfg.get("model_folder", nlp_id) if nlp_id != "NONE" else None,
        "api_endpoint": f"{api_base}/{endpoint}",
    }
