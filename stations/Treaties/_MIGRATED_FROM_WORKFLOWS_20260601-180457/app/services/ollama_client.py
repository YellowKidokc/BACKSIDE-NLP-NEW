"""Strict-JSON LLM client — supports Ollama (local) and OpenAI (o3/o3-mini).

Every response is validated against a Pydantic model before the caller touches it.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from app.config import settings

T = TypeVar("T", bound=BaseModel)

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


class OllamaJSONError(RuntimeError):
    def __init__(self, raw: str, detail: str):
        super().__init__(f"LLM returned non-conforming JSON: {detail}\n--- RAW ---\n{raw}")
        self.raw = raw
        self.detail = detail


def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.txt").read_text(encoding="utf-8")


def render_prompt(name: str, **substitutions: str) -> str:
    template = load_prompt(name)
    for key, value in substitutions.items():
        template = template.replace("{" + key + "}", value)
    return template


# ── OLLAMA BACKEND ──

def _post_ollama(prompt: str) -> str:
    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1},
    }
    with httpx.Client(timeout=settings.ollama_timeout_seconds) as client:
        resp = client.post(f"{settings.ollama_base_url}/api/generate", json=payload)
        resp.raise_for_status()
        data = resp.json()
    return data.get("response", "")


# ── OPENAI BACKEND ──

def _post_openai(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.openai_model,
        "messages": [
            {"role": "system", "content": "You are a research analysis engine. Always respond with valid JSON only. No markdown, no commentary, no backticks."},
            {"role": "user", "content": prompt},
        ],
        "response_format": {"type": "json_object"},
    }
    # o3 models may need longer timeout
    with httpx.Client(timeout=300) as client:
        resp = client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    return data["choices"][0]["message"]["content"]


# ── UNIFIED INTERFACE ──

def _post_generate(prompt: str) -> str:
    """Route to the configured backend."""
    if settings.llm_backend == "openai":
        return _post_openai(prompt)
    else:
        return _post_ollama(prompt)


def call_json(prompt: str, schema: type[T]) -> T:
    raw = _post_generate(prompt)
    # Strip markdown fences if present
    clean = raw.strip()
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[-1]
        if clean.endswith("```"):
            clean = clean[:-3]
        clean = clean.strip()
    try:
        parsed = json.loads(clean)
    except json.JSONDecodeError as e:
        raise OllamaJSONError(raw, f"json.loads failed: {e}") from e
    try:
        return schema.model_validate(parsed)
    except ValidationError as e:
        raise OllamaJSONError(raw, f"schema validation failed: {e}") from e


def call_json_template(name: str, schema: type[T], **substitutions: str) -> T:
    return call_json(render_prompt(name, **substitutions), schema)
