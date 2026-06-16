"""
PROMPT RUNNER
=============
Generic OpenAI call helper + run_all() that fans out across all prompts.

Each individual prompt file exposes:
  - SECTION_NAME (str)
  - MODEL (str)
  - TEMPERATURE (float)
  - SYSTEM_PROMPT (str)
  - USER_PROMPT_TEMPLATE (str, with {content} placeholder)
  - EXPECTED_JSON_SHAPE (dict, illustrative)
  - run(content, client) -> dict

Usage:
    from openai import OpenAI
    from prompts._runner import run_all, call_openai_json

    client = OpenAI()
    results = run_all(paper_text, client)
    # results = {"claim_inventory": {...}, "equation_audit": {...}, ...}
"""
import json
from typing import Any


def trim_content(content: str, head: int = 6000, tail: int = 2000) -> str:
    """Keep first `head` chars + last `tail` chars if content exceeds head+tail."""
    if len(content) <= head + tail:
        return content
    return f"{content[:head]}\n\n[...middle truncated for analysis...]\n\n{content[-tail:]}"


def call_openai_json(client, *, model: str, system: str, user: str,
                     temperature: float = 0.2, max_tokens: int = 2000) -> dict:
    """One canonical OpenAI call. Returns dict — either parsed JSON or {"error": ...}."""
    if client is None:
        return {"error": "OpenAI client not configured"}
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
        )
        text = resp.choices[0].message.content or "{}"
        return json.loads(text)
    except Exception as e:
        return {"error": str(e)}


def _import_prompt_modules():
    """Lazy import so missing prompt files don't blow up the runner."""
    from . import (
        claim_inventory,
        equation_audit,
        assumption_stack,
        kill_conditions,
        evidence_map,
        physics_comparison,
        novelty_classification,
        coherence_score,
        overstatement_detector,
        revision_plan,
        spine_analysis,
    )
    all_prompts = [
        claim_inventory,
        equation_audit,
        assumption_stack,
        kill_conditions,
        evidence_map,
        physics_comparison,
        novelty_classification,
        coherence_score,
        overstatement_detector,
        revision_plan,
        spine_analysis,
    ]
    return all_prompts


def run_all(content: str, client, sections: list[str] | None = None) -> dict[str, Any]:
    """Run every prompt module against the paper content.

    Args:
        content: raw paper text
        client: openai.OpenAI() instance
        sections: optional whitelist of SECTION_NAME values to run

    Returns:
        dict keyed by SECTION_NAME, value is the parsed JSON dict from each prompt.
    """
    modules = _import_prompt_modules()
    trimmed = trim_content(content)
    results: dict[str, Any] = {}
    for mod in modules:
        name = getattr(mod, "SECTION_NAME", mod.__name__.split(".")[-1])
        if sections and name not in sections:
            continue
        try:
            results[name] = mod.run(trimmed, client)
        except Exception as e:
            results[name] = {"error": f"{type(e).__name__}: {e}"}
    return results
