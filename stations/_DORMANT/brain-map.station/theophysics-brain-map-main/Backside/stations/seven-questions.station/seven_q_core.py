"""
Seven Questions System — Core Utilities
======================================
Shared helpers for the 7QS pipeline.

Design goals:
- Keep ontology, evaluation, and rendering separate.
- Preserve compatibility with existing 7Q JSON keys where possible.
- Make public labels human-readable while retaining internal IDs.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

DEFAULT_MODEL = os.environ.get("SEVEN_Q_MODEL", "gpt-4o-mini")

SEVEN_QUESTIONS = [
    {"id": "Q1", "label": "Existence", "question": "What must exist for this claim to have a referent?"},
    {"id": "Q2", "label": "Distinction", "question": "What distinction does this claim depend on or introduce?"},
    {"id": "Q3", "label": "Substrate", "question": "What carries, grounds, or instantiates the claim?"},
    {"id": "Q4", "label": "Order", "question": "What structure or ordering principle is required?"},
    {"id": "Q5", "label": "Observation", "question": "What would make the claim empirically, phenomenally, or logically observable?"},
    {"id": "Q6", "label": "Relation", "question": "How does the claim connect domains, agents, variables, or systems?"},
    {"id": "Q7", "label": "Coherence", "question": "What would preserve or destroy coherence across the whole system?"},
]

MODES = {
    "F": {"label": "Foundations", "verb": "build", "purpose": "constructive derivation"},
    "R": {"label": "Reversals", "verb": "break", "purpose": "adversarial collapse analysis"},
    "E": {"label": "Evidence", "verb": "test", "purpose": "empirical and literature pressure"},
}


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def slugify(value: str, max_len: int = 80) -> str:
    value = re.sub(r"[^\w\-\.]+", "_", value.strip())
    value = re.sub(r"_+", "_", value).strip("_")
    return value[:max_len] or "untitled"


def read_text(path: str | Path, max_chars: Optional[int] = None) -> str:
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    if max_chars and len(text) > max_chars:
        return text[:max_chars] + "\n\n[...truncated for analysis...]"
    return text


def ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, str):
        parts = [p.strip() for p in re.split(r"\n|;|•|\d+\.| - |\* ", value) if p.strip()]
        return parts or [value.strip()]
    return [value]


def safe_str(value: Any, limit: Optional[int] = None) -> str:
    if value is None:
        out = ""
    elif isinstance(value, (dict, list)):
        out = json.dumps(value, ensure_ascii=False)
    else:
        out = str(value)
    out = out.strip()
    return out[:limit] if limit else out


def normalize_confidence(raw: Any, default: float = 0.5) -> float:
    try:
        val = float(raw)
        if val > 1.0:
            val = val / 10.0 if val <= 10 else val / 100.0
        return max(0.0, min(1.0, round(val, 3)))
    except Exception:
        return default


def extract_json_object(text: str) -> Dict[str, Any]:
    """Robustly parse JSON returned by a model, including fenced JSON."""
    text = text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start:end + 1])
        raise


def get_openai_client():
    try:
        from openai import OpenAI
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return None
        return OpenAI(api_key=api_key)
    except Exception:
        return None


def call_openai_json(prompt: str, system: str, model: str = DEFAULT_MODEL, max_tokens: int = 3000, temperature: float = 0.25) -> Dict[str, Any]:
    client = get_openai_client()
    if client is None:
        return {"error": "OpenAI client not configured. Set OPENAI_API_KEY and install the openai package."}
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content or "{}"
        return extract_json_object(raw)
    except Exception as exc:
        return {"error": str(exc)}


def infer_death_tests(reverse: Dict[str, Any]) -> int:
    verdict = safe_str(reverse.get("verdict", reverse.get("assessment", ""))).lower()
    confidence = normalize_confidence(reverse.get("confidence_score", reverse.get("confidence", 0.5)))
    if any(x in verdict for x in ["does not survive", "fails", "collapses", "fatal"]):
        return 1
    if any(x in verdict for x in ["weakened", "serious", "major unresolved"]):
        return 2
    if any(x in verdict for x in ["partial", "qualified", "survives with"]):
        return 3
    return 4 if confidence >= 0.75 else 3


def infer_tier(score: float) -> str:
    if score >= 90:
        return "NEAR-CANONICAL"
    if score >= 75:
        return "STRONG"
    if score >= 60:
        return "PROVISIONAL"
    return "WEAK"


def compute_tscore(forward: Dict[str, Any], reverse: Dict[str, Any], evidence: Optional[Dict[str, Any]] = None) -> Tuple[float, str, int]:
    evidence = evidence or {}
    deaths = infer_death_tests(reverse)
    conf = normalize_confidence(reverse.get("confidence_score", reverse.get("confidence", 0.5)))

    domains = ensure_list(forward.get("q1", forward.get("domains", [])))
    bridge_count = min(len([d for d in domains if safe_str(d)]), 10)

    evidence_items = ensure_list(evidence.get("evidence_items", evidence.get("e1", [])))
    evidence_weight = min(len(evidence_items), 5) / 5 if evidence_items else 0.35

    assumptions = ensure_list(reverse.get("r2", reverse.get("assumptions", [])))
    alternatives_weight = min(len(assumptions), 5) / 5 if assumptions else 0.2

    score = (
        (deaths / 4) * 25
        + evidence_weight * 20
        + (bridge_count / 10) * 20
        + alternatives_weight * 15
        + conf * 20
    )
    score = round(score, 1)
    return score, infer_tier(score), deaths


def write_json(path: str | Path, data: Dict[str, Any]) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def format_value_markdown(value: Any) -> str:
    if isinstance(value, list):
        return "\n".join(f"- {safe_str(v)}" for v in value)
    if isinstance(value, dict):
        return "```json\n" + json.dumps(value, indent=2, ensure_ascii=False) + "\n```"
    return safe_str(value)
