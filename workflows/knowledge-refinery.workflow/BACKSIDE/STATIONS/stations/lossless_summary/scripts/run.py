"""
ST-SUM-001 — Lossless Summary.

Preserves the argument WITHOUT flattening. Keeps claims, evidence, equations,
assumptions, argument order, unresolved gaps. NOT a "short summary" — designed
to be re-expandable to the original paper's reasoning shape.

Usage:
    python run.py --in <source.md> --out <summary.lossless.md>
    Optional: --claims <claims.json>

Outputs: summary.lossless.md + summary.lossless.json (alongside).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

STATION_ID = "ST-SUM-001"
MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are a lossless argument-preserving summarizer.
You do NOT compress. You re-organize the source so its full argument shape
is recoverable: every claim, every assumption, every equation, every piece
of evidence, the order of reasoning, and every unresolved gap is captured.
Return only valid JSON. No fences. No preamble."""

SUMMARY_PROMPT = """Produce a LOSSLESS structured summary of this paper.

Hard constraints:
- DO NOT compress. If you have to choose between length and completeness, choose completeness.
- DO NOT flatten ordered reasoning into a flat bullet list. Preserve argument order.
- INCLUDE every claim, equation, assumption, evidence statement, and gap.
- LABEL gradient on each major claim: load-bearing | suggestive | overclaimed.

{claims_context}
PAPER CONTENT:
{content}

Respond in JSON:

{{
  "title": "...",
  "abstract_paraphrase": "...",
  "domains": ["..."],
  "argument_arc": [
    {{"step": 1, "move": "premise|definition|claim|evidence|derivation|objection|response|conclusion",
      "content": "...", "depends_on": ["step or claim id"]}}
  ],
  "claims": [
    {{"id": "...", "text": "...", "gradient": "load-bearing|suggestive|overclaimed"}}
  ],
  "assumptions": ["..."],
  "equations": ["..."],
  "evidence_statements": ["..."],
  "unresolved_gaps": ["..."],
  "argument_order_preserved": true
}}"""


def call_openai(user_prompt: str, max_tokens: int = 4000) -> dict:
    try:
        from openai import OpenAI
    except ImportError:
        return {"error": "openai package not installed"}

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return {"error": "OPENAI_API_KEY not set"}

    client = OpenAI(api_key=api_key)
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}


def to_markdown(s: dict) -> str:
    lines = [
        f"# {STATION_ID} — Lossless Summary: {s.get('title','(untitled)')}",
        f"*Generated: {datetime.now().isoformat(timespec='seconds')} | Model: {MODEL}*",
        "",
        "## Abstract paraphrase",
        s.get("abstract_paraphrase", ""),
        "",
        f"**Domains:** {', '.join(s.get('domains', []))}",
        "",
        "## Argument arc",
        "",
    ]
    for step in s.get("argument_arc", []):
        deps = step.get("depends_on", [])
        dep_str = f" *(← {', '.join(deps)})*" if deps else ""
        lines.append(f"{step.get('step','?')}. **[{step.get('move','?')}]**{dep_str} {step.get('content','')}")
    lines += ["", "## Claims (gradient-labeled)", ""]
    for c in s.get("claims", []):
        grad = c.get("gradient", "")
        lines.append(f"- **{c.get('id','?')}** `[{grad}]` {c.get('text','')}")
    for section, key in [("Assumptions", "assumptions"), ("Equations", "equations"),
                          ("Evidence statements", "evidence_statements"),
                          ("Unresolved gaps", "unresolved_gaps")]:
        items = s.get(key, [])
        lines += ["", f"## {section}", ""]
        for x in items:
            lines.append(f"- {x}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True)
    parser.add_argument("--out", dest="out", required=True)
    parser.add_argument("--claims", default=None)
    args = parser.parse_args()

    paper = Path(args.inp)
    content = paper.read_text(encoding="utf-8", errors="ignore")
    if len(content) > 10000:
        content = content[:10000] + "\n\n[...truncated for analysis...]"

    claims_context = ""
    if args.claims and Path(args.claims).exists():
        try:
            cd = json.loads(Path(args.claims).read_text(encoding="utf-8"))
            claims_context = f"PRIOR CLAIM EXTRACTION (use these IDs):\n{json.dumps(cd.get('claims', cd), indent=2)[:1500]}\n\n"
        except Exception:
            pass

    result = call_openai(SUMMARY_PROMPT.format(
        claims_context=claims_context, content=content))

    payload = {
        "station":     STATION_ID,
        "paper":       paper.name,
        "model":       MODEL,
        "computed_at": datetime.now().isoformat(timespec="seconds"),
        **(result if isinstance(result, dict) else {"result": result}),
    }

    out_path = Path(args.out)
    if out_path.suffix.lower() == ".json":
        json_path = out_path
        md_path = out_path.with_suffix(".md")
    else:
        md_path = out_path
        json_path = out_path.with_suffix(".json")

    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(to_markdown(payload), encoding="utf-8")

    err = result.get("error") if isinstance(result, dict) else None
    print(json.dumps({
        "status":         "error" if err else "ok",
        "error":          err,
        "argument_steps": len(result.get("argument_arc", []) if isinstance(result, dict) else []),
        "claims":         len(result.get("claims", []) if isinstance(result, dict) else []),
    }))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
