"""
MDA TWO-LANE OPENAI RUNNER
==========================
Cheap, narrow alternative to openai_8_prompts.py.

Lanes:
  math       - equations, variables, isomorphism maps, derivation gaps only
  attention  - reader attention, clarity, rhythm, entry point, paragraph flow only

Usage:
  python openai_mda_two_lane.py paper.md --lane math
  python openai_mda_two_lane.py paper.md --lane attention
  python openai_mda_two_lane.py paper.md --lane both --output out_dir

Default model is intentionally cheap. Override with --model o3 if needed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from openai import OpenAI
    _client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    HAS_OPENAI = True
except Exception:
    _client = None
    HAS_OPENAI = False


DEFAULT_MODEL = "gpt-4o-mini"


DEVELOPER_CONTEXT = """You are analyzing an article from David Lowe's MDA/Theophysics work.
The task is narrow. Do not run a full peer review. Do not flatter. Give exact,
actionable findings with quoted text and replacement guidance."""


LANES = {
    "math": {
        "label": "MATH LAYER ONLY",
        "max_tokens": 2200,
        "prompt": """Run a math-only audit.

Do NOT critique prose style, persuasion, audience fit, moral claims, theology,
or overclaim temperature except where a mathematical phrase is misused.

Focus only on:
1. Variables: are symbols such as chi/χ, P, C, entropy, coherence, or order
   parameter defined consistently?
2. Equations: where does the prose imply an equation, substitution, derivative,
   threshold, metric, or formal model that is not actually shown?
3. Isomorphism: where does the text claim or imply isomorphism? For each case,
   classify it as:
   - proven_here
   - candidate_isomorphism
   - structural_correspondence
   - analogy_only
4. Derivation gaps: what exact step is missing to move the claim one rung
   higher?
5. Minimal patch list: 3-7 concrete edits that would make the math layer honest.

Output format:
- MATH_STATUS: one of CLEAN / NEEDS_DEFINITIONS / NEEDS_DERIVATION / MISUSES_MATH
- LOAD_BEARING_MATH: bullet list
- ISOMORPHISM_TABLE: mapping | current status | missing proof step | safe wording
- MISSING_EQUATIONS_OR_DEFINITIONS: bullet list
- MINIMAL_PATCHES: exact quoted phrase -> replacement or addition

Keep it concise. Do not invent equations for decoration.""",
    },
    "attention": {
        "label": "READER ATTENTION ONLY",
        "max_tokens": 1800,
        "prompt": """Run a reader-attention audit.

Do NOT do an overclaim audit. Do NOT judge whether the argument is true. Do NOT
police scope unless the wording causes the reader to lose the thread.

Your question is: will a serious but busy reader keep reading?

Focus only on:
1. Opening pull: does the first screen create momentum?
2. Attention drops: where would a reader skim, stall, or quit?
3. Cognitive load: where is jargon stacked too densely?
4. Rhythm: where are paragraphs too long, repetitive, or same-shaped?
5. Transitions: where does the article jump without carrying the reader?
6. Memorable lines: which lines should be kept because they carry attention?
7. Minimal patch list: 5-8 edits that improve readability without weakening the
   argument.

Output format:
- ATTENTION_STATUS: one of STRONG / UNEVEN / DRAGGING / CONFUSING
- KEEP_THESE_LINES: quoted lines that work
- ATTENTION_DROPS: quoted passage | why attention drops | quick fix
- JARGON_BOTTLENECKS: phrase | reader risk | simpler doorway
- RHYTHM_FIXES: exact local edit suggestions
- OPENING_REWRITE: optional replacement for only the first 1-3 paragraphs

Keep it practical. This is about keeping a human in the chair.""",
    },
}


def trim_content(content: str, head: int = 9000, tail: int = 2000) -> str:
    if len(content) <= head + tail:
        return content
    return f"{content[:head]}\n\n[...middle truncated for focused lane audit...]\n\n{content[-tail:]}"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def cache_key(paper: Path, lane: str, model: str, content: str) -> str:
    h = hashlib.sha256()
    h.update(str(paper.resolve()).encode("utf-8", errors="replace"))
    h.update(lane.encode("utf-8"))
    h.update(model.encode("utf-8"))
    h.update(content.encode("utf-8", errors="replace"))
    return h.hexdigest()[:16]


def call_openai(model: str, lane: str, content: str, title: str) -> dict:
    config = LANES[lane]
    full_prompt = f"""PAPER: {title}

CONTENT:
{content}

{config["prompt"]}"""

    kwargs = {
        "model": model,
        "messages": [
            {"role": "developer", "content": DEVELOPER_CONTEXT},
            {"role": "user", "content": full_prompt},
        ],
    }
    if model.startswith("o3"):
        kwargs["max_completion_tokens"] = config["max_tokens"]
    else:
        kwargs["temperature"] = 0.2
        kwargs["max_tokens"] = config["max_tokens"]

    response = _client.chat.completions.create(**kwargs)
    usage = response.usage
    return {
        "lane": lane,
        "label": config["label"],
        "model": model,
        "text": response.choices[0].message.content or "",
        "meta": {
            "input_tokens": usage.prompt_tokens if usage else 0,
            "output_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        },
    }


def run_lane(paper: Path, lane: str, model: str, cache_dir: Path) -> dict:
    if not HAS_OPENAI:
        return {"lane": lane, "error": "OpenAI client not configured"}
    raw = read_text(paper)
    content = trim_content(raw)
    key = cache_key(paper, lane, model, content)
    cache_path = cache_dir / f"{paper.stem}_{lane}_{model}_{key}.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))

    result = call_openai(model, lane, content, paper.stem)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(0.4)
    return result


def write_report(paper: Path, results: list[dict], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"{paper.stem}_TWO_LANE_REPORT.md"
    total_tokens = sum(r.get("meta", {}).get("total_tokens", 0) for r in results)
    lines = [
        f"# Two-Lane MDA Report: {paper.stem}",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        f"**Total tokens:** {total_tokens:,}",
        "",
        "---",
        "",
    ]
    for result in results:
        label = result.get("label", result.get("lane", "lane"))
        meta = result.get("meta", {})
        lines.extend([
            f"## {label}",
            "",
            f"*Model: `{result.get('model', '?')}` | Tokens: `{meta.get('total_tokens', '?')}`*",
            "",
        ])
        if "error" in result:
            lines.append(f"Error: {result['error']}")
        else:
            lines.append(result.get("text", ""))
        lines.extend(["", "---", ""])
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description="MDA two-lane OpenAI runner")
    parser.add_argument("paper", help="Path to paper .md/.html/.txt")
    parser.add_argument("--lane", choices=["math", "attention", "both"], default="both")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--output", "-o", default=None)
    args = parser.parse_args()

    paper = Path(args.paper)
    output_dir = Path(args.output) if args.output else paper.parent / "_two_lane_intel"
    cache_dir = output_dir / "_cache"
    lanes = ["math", "attention"] if args.lane == "both" else [args.lane]

    print(f"Two-lane MDA runner: {paper.name}")
    print(f"Model: {args.model}")
    results = []
    for lane in lanes:
        print(f"  {LANES[lane]['label']}...", end="", flush=True)
        result = run_lane(paper, lane, args.model, cache_dir)
        tokens = result.get("meta", {}).get("total_tokens", "?")
        print(f" {tokens} tokens")
        results.append(result)

    report = write_report(paper, results, output_dir)
    print(json.dumps({"status": "ok", "report": str(report)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
