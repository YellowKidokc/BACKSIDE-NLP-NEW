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


def base_result(station_id: str, station_name: str, path: Path,
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
