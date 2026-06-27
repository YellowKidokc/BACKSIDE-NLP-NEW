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


def base_result(path: Path, station_id: str, station_name: str,
                nlp_info: dict[str, Any]) -> dict[str, Any]:
    """Create the standard artifact envelope."""
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


def _sanitize_vector_input(text: str) -> str:
    return strip_html(text or "").replace("\x00", "").strip()


def _normalize_embedding_payload(response: Any) -> list[float]:
    vectors = []
    if isinstance(response, dict):
        vectors = response.get("embeddings", response.get("embedding", []))
    if not vectors:
        return []
    if isinstance(vectors, list) and vectors:
        first = vectors[0]
        if isinstance(first, list):
            return [float(x) for x in first]
        if isinstance(first, (int, float)):
            return [float(x) for x in vectors]
    return []


def _safe_load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}


def _series_state_root() -> Path:
    return Path(__file__).resolve().parent.parent / "_state" / "paper_vectors"


def _build_series_context(series_id: str, paper_vector: list[float],
                         cfg: dict[str, Any], log: Any) -> dict[str, Any]:
    vector_cfg = cfg.get("vectorization", {}).get("series_context", {})
    if not series_id:
        return {
            "enabled": False,
            "reason": "missing_series_id",
        }
    if not isinstance(paper_vector, list) or not paper_vector:
        return {
            "enabled": True,
            "reason": "paper_vector_empty",
        }
    if not vector_cfg.get("enabled", True):
        return {
            "enabled": False,
            "reason": "series_context_disabled",
        }

    root = _series_state_root()
    root.mkdir(parents=True, exist_ok=True)
    state_path = root / f"{re.sub(r'[^a-zA-Z0-9_.-]', '_', str(series_id))}.json"
    state = _safe_load_json(state_path)

    count = int(state.get("count", 0) or 0)
    prior_vector = state.get("vector", [])
    if isinstance(prior_vector, list) and prior_vector and len(prior_vector) != len(paper_vector):
        prior_vector = []
        count = 0

    context_vector = prior_vector if isinstance(prior_vector, list) else []
    method = str(vector_cfg.get("method", "running_mean")).lower()
    alpha = float(vector_cfg.get("ema_alpha", 0.3)) if isinstance(vector_cfg.get("ema_alpha"), (int, float)) else 0.3

    if method == "ema" and context_vector and len(context_vector) == len(paper_vector):
        try:
            context_vector = [
                float(alpha) * float(cv) + (1 - float(alpha)) * float(tv)
                for cv, tv in zip(context_vector, paper_vector)
            ]
            count = max(count, 1)
        except Exception:
            context_vector = []
    elif isinstance(prior_vector, list) and len(prior_vector) == len(paper_vector):
        # running mean context for previous papers
        context_vector = prior_vector
    else:
        context_vector = []

    # Update running mean for this series after building context
    if method == "ema":
        if context_vector and len(context_vector) == len(paper_vector):
            next_vector = context_vector
            new_count = count if count >= 1 else 1
        else:
            next_vector = paper_vector
            new_count = 1
    else:
        if isinstance(prior_vector, list) and len(prior_vector) == len(paper_vector) and count > 0:
            try:
                next_vector = [
                    (float(pc) * count + float(tv)) / float(count + 1)
                    for pc, tv in zip(prior_vector, paper_vector)
                ]
            except Exception:
                next_vector = paper_vector
        else:
            next_vector = paper_vector
        new_count = count + 1

    state_path.write_text(
        json.dumps({
            "series_id": series_id,
            "count": new_count,
            "vector": next_vector,
            "method": method,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        }, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    if not context_vector:
        return {
            "enabled": True,
            "method": method,
            "series_id": series_id,
            "position": max(new_count, 1),
            "n_prior_papers": count,
            "context_vector": [],
            "context_length": 0,
            "note": "initialized_series_context",
        }

    return {
        "enabled": True,
        "method": method,
        "series_id": series_id,
        "position": max(new_count, 1),
        "n_prior_papers": count,
        "context_vector": context_vector,
        "context_length": len(context_vector),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }


def build_vectorization_payload(text: str, cfg: dict[str, Any], log: Any,
                               *, series_id: str | None = None,
                               source_file: str | None = None) -> dict[str, Any]:
    """Generate a stable vectorization payload for an entire input text."""
    vec_cfg = cfg.get("vectorization", {})
    if vec_cfg is False or (isinstance(vec_cfg, dict) and vec_cfg.get("enabled") is False):
        return {"enabled": False}

    cleaned = _sanitize_vector_input(text or "")
    if not cleaned:
        return {
            "enabled": True,
            "paper": {"success": False, "error": "No extractable text for vectorization"},
            "series_context": {"enabled": False, "reason": "empty_text"},
        }

    try:
        response = call_nlp("embed", {"texts": [cleaned]})
        vector = _normalize_embedding_payload(response)
        paper_payload = {
            "success": True,
            "endpoint": "embed",
            "dimension": len(vector),
            "vector": vector,
            "model": response.get("model"),
            "text_length": len(cleaned),
            "source_file": source_file,
            "status": response.get("status"),
            "error": response.get("error"),
        }
        return {
            "enabled": True,
            "paper": paper_payload,
            "series_context": _build_series_context(series_id, vector, cfg, log),
            "schema_version": "v1",
        }
    except Exception as exc:
        if hasattr(log, "warning"):
            log.warning("Vectorization failed for %s: %s", source_file or "input", exc)
        return {
            "enabled": True,
            "paper": {"success": False, "error": str(exc)},
            "series_context": {"enabled": False, "reason": "embed_call_failed"},
            "schema_version": "v1",
        }
