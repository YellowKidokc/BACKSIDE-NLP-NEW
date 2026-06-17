"""Shared helpers for SSS_v1 NLP station pipelines.

The core 8 station scripts intentionally keep only station identity and
station-specific processing logic. Common FastAPI, artifact, and text utilities
live here so bugs and behavior changes are fixed once for every station.
"""
from __future__ import annotations

import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

API_BASE = "http://localhost:8700/nlp"


def call_nlp(endpoint: str, payload: dict[str, Any], timeout: int = 120) -> dict[str, Any]:
    """Call one NLP endpoint on the shared FastAPI service."""
    response = requests.post(f"{API_BASE}/{endpoint}", json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()


def read_input(path: Path) -> Any:
    """Read a raw text/HTML/Markdown file or parse a JSON artifact."""
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return text


def data_from_artifact(obj: Any) -> dict[str, Any]:
    """Return the artifact data payload if present, otherwise a dict object itself."""
    if isinstance(obj, dict):
        data = obj.get("data", obj)
        return data if isinstance(data, dict) else {}
    return {}


def text_from_input(obj: Any) -> str:
    """Best-effort text extraction from raw input or an upstream JSON artifact."""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        data = data_from_artifact(obj)
        for key in ("text", "document", "original_text", "content", "summary"):
            value = data.get(key)
            if isinstance(value, str):
                return value
        versions = data.get("versions")
        if isinstance(versions, dict):
            academic = versions.get("academic", {})
            if isinstance(academic, dict) and isinstance(academic.get("text"), str):
                return academic["text"]
    return json.dumps(obj, ensure_ascii=False)


def strip_html(text: str) -> str:
    """Remove common HTML tags without adding a BeautifulSoup dependency."""
    if "<" not in text or ">" not in text:
        return text
    text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def sentences(text: str) -> list[str]:
    """Split text into simple sentence units."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def paragraphs(text: str) -> list[str]:
    """Split text into paragraph blocks."""
    return [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]


def sections(text: str) -> list[dict[str, Any]]:
    """Split Markdown-like text into heading-scoped sections."""
    output: list[dict[str, Any]] = []
    current: dict[str, Any] = {"heading": "Introduction", "text": []}
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$", line)
        if match:
            if current["text"]:
                output.append({"heading": current["heading"], "text": "\n".join(current["text"]).strip()})
            current = {"heading": match.group(2).strip(), "text": []}
        else:
            current["text"].append(line)
    if current["text"] or not output:
        output.append({"heading": current["heading"], "text": "\n".join(current["text"]).strip()})
    return output


def score_map(api_result: dict[str, Any]) -> dict[str, float]:
    """Normalize common classifier response shapes into {label: score}."""
    labels = api_result.get("labels") or api_result.get("classes") or []
    scores = api_result.get("scores") or api_result.get("probabilities") or []
    if isinstance(scores, dict):
        return {str(k): float(v) for k, v in scores.items()}
    return {str(label): float(score) for label, score in zip(labels, scores)}


def top_label(api_result: dict[str, Any], default: str = "unknown") -> tuple[str, float, dict[str, float]]:
    """Return the best label, score, and full normalized score map."""
    scores = score_map(api_result)
    if scores:
        label = max(scores, key=scores.get)
        return label, scores[label], scores
    label = str(api_result.get("label") or api_result.get("class") or default)
    score = float(api_result.get("score", 0.0) or 0.0)
    return label, score, {label: score}


def word_count(text: str) -> int:
    """Count word-like tokens."""
    return len(re.findall(r"\b\w+\b", text))


def flesch_reading_ease(text: str) -> float:
    """Compute a lightweight Flesch Reading Ease score."""
    words = max(1, word_count(text))
    sentence_count = max(1, len(sentences(text)))
    syllables = max(words, sum(max(1, len(re.findall(r"[aeiouyAEIOUY]+", word))) for word in re.findall(r"\b\w+\b", text)))
    return round(206.835 - 1.015 * (words / sentence_count) - 84.6 * (syllables / words), 1)


def cosine(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity for two vectors."""
    if not a or not b:
        return 0.0
    size = min(len(a), len(b))
    dot = sum(float(a[i]) * float(b[i]) for i in range(size))
    norm_a = math.sqrt(sum(float(a[i]) ** 2 for i in range(size)))
    norm_b = math.sqrt(sum(float(b[i]) ** 2 for i in range(size)))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def embeddings(api_result: dict[str, Any]) -> list[list[float]]:
    """Normalize embedding response shapes into a list of vectors."""
    value = api_result.get("embeddings", api_result.get("embedding", []))
    if value and isinstance(value[0], (int, float)):
        return [value]
    return value or []


def base_result(path: Path, station_id: str, station_name: str, nlp_info: dict[str, Any]) -> dict[str, Any]:
    """Build the standard Core 8 JSON artifact envelope."""
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


def nlp_route(api_base: str, models_path: Path, cfg: dict[str, Any], nlp_id: str, endpoint: str) -> dict[str, Any]:
    """Build standard Section 06 routing metadata for a station."""
    selected = cfg.get("nlp_id", nlp_id)
    return {
        "nlp_id": selected,
        "nlp_path": models_path / cfg.get("model_folder", selected),
        "api_endpoint": f"{api_base}/{endpoint}",
    }
