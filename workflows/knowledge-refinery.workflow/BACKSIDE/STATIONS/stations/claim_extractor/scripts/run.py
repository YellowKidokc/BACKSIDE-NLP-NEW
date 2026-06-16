"""
ST-CLAIM-001 — Claim Extractor.

Read source.md and extract durable claims, assumptions, equations, hypotheses,
and evidence statements. Assign IDs. Avoid duplicates.

Usage:
    python run.py --in <source.md> --out <claims.json>

Output: claims.json + claims.md.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

STATION_ID = "ST-CLAIM-001"
MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are a claim extraction specialist. Pull DURABLE claims from a paper —
not narrative or background, but the load-bearing assertions that, if false,
would invalidate the paper. Return only valid JSON. No preamble, no fences."""

EXTRACT_PROMPT = """Extract every DURABLE claim from this paper.

For each one, classify as:
  - claim          (an assertion the paper is making)
  - assumption     (something taken as given without argument)
  - hypothesis     (a tentative claim being tested)
  - equation       (a formal mathematical/physical statement)
  - evidence_stmt  (a specific empirical statement)

Each item gets a stable ID:
  C-001, C-002, ...  for claims
  A-001, A-002, ...  for assumptions
  H-001 ...          for hypotheses
  EQ-001 ...         for equations
  EV-001 ...         for evidence statements

PAPER CONTENT:
{content}

Respond in JSON:

{{
  "claims": [
    {{"id": "C-001", "type": "claim|assumption|hypothesis|equation|evidence_stmt",
      "text": "...", "load_bearing": true,
      "gradient": "load-bearing|suggestive|overclaimed"}}
  ],
  "summary": {{
    "total": 0, "by_type": {{"claim": 0, "assumption": 0, "hypothesis": 0,
                              "equation": 0, "evidence_stmt": 0}}
  }}
}}"""


def call_openai(user_prompt: str, max_tokens: int = 3000) -> dict:
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True)
    parser.add_argument("--out", dest="out", required=True)
    args = parser.parse_args()

    paper = Path(args.inp)
    content = paper.read_text(encoding="utf-8", errors="ignore")
    if len(content) > 8000:
        content = content[:8000] + "\n\n[...truncated for analysis...]"

    result = call_openai(EXTRACT_PROMPT.format(content=content))

    payload = {
        "station":     STATION_ID,
        "paper":       paper.name,
        "model":       MODEL,
        "computed_at": datetime.now().isoformat(timespec="seconds"),
        **(result if isinstance(result, dict) else {"result": result}),
    }
    out_path = Path(args.out)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # claims.md companion
    claims = result.get("claims", []) if isinstance(result, dict) else []
    md_lines = [f"# {STATION_ID} — Claims extracted from {paper.name}",
                f"*Generated: {datetime.now().isoformat(timespec='seconds')} | Model: {MODEL}*",
                "", f"**Total:** {len(claims)}", ""]
    by_type: dict[str, list] = {}
    for c in claims:
        by_type.setdefault(c.get("type", "unknown"), []).append(c)
    for typ, items in by_type.items():
        md_lines += [f"## {typ.upper()} ({len(items)})", ""]
        for c in items:
            grad = c.get("gradient", "")
            grad_tag = f" `[{grad}]`" if grad else ""
            md_lines.append(f"- **{c.get('id','?')}**{grad_tag}: {c.get('text','')}")
        md_lines.append("")
    out_path.with_suffix(".md").write_text("\n".join(md_lines), encoding="utf-8")

    err = result.get("error") if isinstance(result, dict) else None
    print(json.dumps({"status": "error" if err else "ok",
                      "error": err, "claim_count": len(claims)}))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
