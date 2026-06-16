#!/usr/bin/env python3
"""
generate_reading_levels.py

Two-stage reading level generator for Theophysics articles.
Stage 1: Standard → Academic (enrich terms, add citations, formalize)
Stage 2: Standard + Term Inventory → Easy (analogies, 8th grade)

Usage:
    python generate_reading_levels.py MDA-001-story-introduction.md
    python generate_reading_levels.py MDA-001-story-introduction.md --paper-grade MDA-001.paper-grade.json
    python generate_reading_levels.py MDA-001-story-introduction.md --api openai
    python generate_reading_levels.py MDA-001-story-introduction.md --api anthropic

Without --api: outputs the prompts as .txt files for manual paste into any LLM.
With --api: calls the API directly (requires OPENAI_API_KEY or ANTHROPIC_API_KEY env var).
OpenAI defaults to o3 unless OPENAI_MODEL is set.
"""

from __future__ import annotations
import argparse
import json
import os
import re
from pathlib import Path
from datetime import datetime


SCRIPT_DIR = Path(__file__).parent
STAGE1_PROMPT = SCRIPT_DIR / "STAGE1_ACADEMIC.txt"
STAGE2_PROMPT = SCRIPT_DIR / "STAGE2_EASY.txt"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def build_stage1_input(article: str, paper_grade: dict | None) -> str:
    """Build the full Stage 1 input: prompt + article + optional paper-grade data."""
    prompt = read_text(STAGE1_PROMPT)
    parts = [prompt, "\n---\n\n# ARTICLE TO PROCESS\n\n", article]
    if paper_grade:
        claims = paper_grade.get("claims", [])
        equations = paper_grade.get("equations", [])
        if claims:
            parts.append(f"\n\n# PAPER-GRADE DATA\n\n## Claims ({len(claims)} extracted)\n")
            for c in claims[:30]:
                text = c.get("text", c.get("claim", ""))[:200]
                status = c.get("status", c.get("maturity", "unknown"))
                parts.append(f"- [{status}] {text}\n")
        if equations:
            parts.append(f"\n## Equations ({len(equations)} found)\n")
            for eq in equations[:20]:
                parts.append(f"- {eq.get('raw', eq.get('text', str(eq)))[:150]}\n")
    return "".join(parts)


def build_stage2_input(article: str, term_inventory: list[dict]) -> str:
    """Build the full Stage 2 input: prompt + article + term inventory."""
    prompt = read_text(STAGE2_PROMPT)
    inv_json = json.dumps({"terms": term_inventory}, indent=2, ensure_ascii=False)
    return f"{prompt}\n---\n\n# TERM INVENTORY (from Academic pass)\n\n```json\n{inv_json}\n```\n\n---\n\n# ARTICLE TO SIMPLIFY\n\n{article}"


def call_openai(prompt_text: str, temp: float = 0.3) -> str:
    """Call OpenAI API. Requires OPENAI_API_KEY env var."""
    import openai
    client = openai.OpenAI()
    primary = os.environ.get("OPENAI_MODEL", "gpt-4o").strip() or "gpt-4o"
    fallbacks = os.environ.get("OPENAI_MODEL_FALLBACKS", "gpt-4o-mini")
    models = []
    for model in [primary, *(m.strip() for m in fallbacks.split(",") if m.strip())]:
        if model not in models:
            models.append(model)

    # Reasoning models (o-series) need max_completion_tokens, not max_tokens
    REASONING_PREFIXES = ("o1", "o3", "o4")

    for model in models:
        is_reasoning = any(model.startswith(p) for p in REASONING_PREFIXES)
        token_key = "max_completion_tokens" if is_reasoning else "max_tokens"
        request = {
            "model": model,
            token_key: 8192,
            "messages": [{"role": "user", "content": prompt_text}],
        }
        if not is_reasoning:
            request["temperature"] = temp
        try:
            resp = client.chat.completions.create(**request)
            return resp.choices[0].message.content
        except (openai.NotFoundError, openai.BadRequestError) as exc:
            if model == models[-1]:
                raise
            print(f"OpenAI model failed or unavailable: {model} ({exc})")
            continue
    raise RuntimeError("No OpenAI response returned.")


def call_anthropic(prompt_text: str, temp: float = 0.3) -> str:
    """Call Anthropic API. Requires ANTHROPIC_API_KEY env var."""
    import anthropic
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        temperature=temp,
        messages=[{"role": "user", "content": prompt_text}],
    )
    return resp.content[0].text


def extract_term_inventory(academic_output: str) -> list[dict]:
    """Extract TERM_INVENTORY JSON from Stage 1 output."""
    match = re.search(r"```json\s*(\{.*?\"terms\".*?\})\s*```", academic_output, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1)).get("terms", [])
        except json.JSONDecodeError:
            pass
    # Fallback: try to find any JSON block with terms
    for block in re.findall(r"\{[^{}]*\"terms\"[^{}]*\[.*?\][^{}]*\}", academic_output, re.DOTALL):
        try:
            return json.loads(block).get("terms", [])
        except json.JSONDecodeError:
            continue
    return []


def main():
    parser = argparse.ArgumentParser(description="Generate Easy + Academic reading levels")
    parser.add_argument("article", type=Path, help="Standard article markdown file")
    parser.add_argument("--paper-grade", type=Path, default=None, help="Paper-grade JSON from Codex run")
    parser.add_argument("--api", choices=["openai", "anthropic"], default=None,
                        help="Call API directly. Without this, outputs prompt files for manual use.")
    parser.add_argument("--outdir", type=Path, default=None, help="Output directory (default: next to article)")
    args = parser.parse_args()

    article_text = read_text(args.article)
    stem = args.article.stem
    outdir = args.outdir or args.article.parent / f"{stem}_reading_levels"
    outdir.mkdir(parents=True, exist_ok=True)

    # Load paper-grade data if available
    paper_grade = None
    if args.paper_grade and args.paper_grade.exists():
        paper_grade = json.loads(read_text(args.paper_grade))
    else:
        # Auto-detect paper-grade JSON next to article
        auto = args.article.parent / f"{stem}.paper-grade.json"
        if auto.exists():
            paper_grade = json.loads(read_text(auto))
            print(f"Auto-detected paper-grade: {auto}")

    # === STAGE 1: ACADEMIC ===
    stage1_input = build_stage1_input(article_text, paper_grade)

    if args.api:
        print(f"Stage 1: Generating Academic version via {args.api}...")
        call_fn = call_openai if args.api == "openai" else call_anthropic
        academic_output = call_fn(stage1_input, temp=0.3)
        (outdir / f"{stem}_ACADEMIC.md").write_text(academic_output, encoding="utf-8")
        print(f"  Wrote: {outdir / f'{stem}_ACADEMIC.md'}")

        # Extract term inventory
        terms = extract_term_inventory(academic_output)
        (outdir / f"{stem}_TERM_INVENTORY.json").write_text(
            json.dumps({"terms": terms}, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"  Extracted {len(terms)} terms")

        # === STAGE 2: EASY ===
        if terms:
            stage2_input = build_stage2_input(article_text, terms)
            print(f"Stage 2: Generating Easy version via {args.api}...")
            easy_output = call_fn(stage2_input, temp=0.4)
            (outdir / f"{stem}_EASY.md").write_text(easy_output, encoding="utf-8")
            print(f"  Wrote: {outdir / f'{stem}_EASY.md'}")
        else:
            print("  WARNING: No term inventory extracted. Stage 2 skipped.")
            print("  Check the Academic output for the TERM_INVENTORY JSON block.")

    else:
        # No API — output prompt files for manual use
        (outdir / f"{stem}_STAGE1_PROMPT.txt").write_text(stage1_input, encoding="utf-8")
        print(f"Stage 1 prompt saved: {outdir / f'{stem}_STAGE1_PROMPT.txt'}")
        print(f"  Paste into ChatGPT/Claude/Kimi. Save output as {stem}_ACADEMIC.md")
        print(f"  Then run again with --api or paste Stage 2 prompt manually.")

        # Pre-build Stage 2 prompt with placeholder
        placeholder_terms = [
            {"term": "[PASTE TERMS FROM ACADEMIC OUTPUT]", "definition": "...", "domain": "...",
             "first_use_section": "...", "complexity": "..."}
        ]
        stage2_input = build_stage2_input(article_text, placeholder_terms)
        (outdir / f"{stem}_STAGE2_PROMPT.txt").write_text(stage2_input, encoding="utf-8")
        print(f"Stage 2 prompt saved: {outdir / f'{stem}_STAGE2_PROMPT.txt'}")
        print(f"  Replace placeholder terms with real TERM_INVENTORY from Stage 1 output.")

    # Save a run manifest
    manifest = {
        "article": str(args.article),
        "paper_grade": str(args.paper_grade) if args.paper_grade else "auto-detected" if paper_grade else "none",
        "api": args.api or "manual",
        "output_dir": str(outdir),
        "timestamp": datetime.now().isoformat(),
    }
    (outdir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nDone. Output: {outdir}")


if __name__ == "__main__":
    main()
