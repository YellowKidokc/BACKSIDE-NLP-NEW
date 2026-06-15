"""
ST-SEVENQ-001 — 7Q Forward (Classification Mode).

Apply the FORWARD 7-Question Scientific Method to a paper.
Extracted from:
  \\\\dlowenas\\HPWorkstation\\Desktop\\02_7Q_FRAMEWORK\\7q\\04_OPENAI_7Q\\seven_q_runner.py

Usage:
    python run.py --in <source.md> --out <forward_7q.json>

Output: forward_7q.json + forward_7q.md (alongside).
Requires: OPENAI_API_KEY env var.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

STATION_ID = "ST-SEVENQ-001"
MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are a rigorous academic analyst specializing in cross-domain research.
You apply the 7-Question Scientific Method with maximum intellectual honesty.
Your goal is NOT to validate claims — it is to STRENGTHEN the paper by identifying:
- Missing citations and supporting literature
- Alternative theories that should be addressed
- Stronger theoretical frameworks
- Deep conceptual questions the paper raises but doesn't answer
Be direct. Be specific. Name real theories, real authors, real journals where possible."""

FORWARD_7Q_PROMPT = """Apply the 7-Question Scientific Method (FORWARD — Classification Mode) to this paper.

The 7 Questions:
Q0: POSTURE — What is the paper's fundamental stance toward reality? (humility/surrender vs assertion)
Q1: DOMAIN — What field(s) does this paper operate in?
Q2: CLAIM — What is the central claim?
Q3: EVIDENCE — What evidence is presented? What's missing?
Q4: ASSUMPTIONS — What hidden assumptions are load-bearing?
Q5: FALSIFICATION — How could this claim be proven wrong?
Q6: INTEGRATION — How does this connect to existing literature?
Q7: STRENGTH GAPS — What citations, theories, or frameworks would most strengthen this paper?

For EACH question, be specific and actionable.
For Q7 especially: name real papers, authors, journals, and theories David should engage with.

PAPER CONTENT:
{content}

Respond in structured JSON with keys: q0, q1, q2, q3, q4, q5, q6, q7, summary, top_3_strengthening_actions"""


def call_openai(user_prompt: str, max_tokens: int = 2500) -> dict:
    try:
        from openai import OpenAI
    except ImportError:
        return {"error": "openai package not installed. pip install openai"}

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
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}


def write_markdown(out_md: Path, paper_name: str, result: dict) -> None:
    labels = {
        "q0": "Q0: Posture", "q1": "Q1: Domain", "q2": "Q2: Claim",
        "q3": "Q3: Evidence", "q4": "Q4: Assumptions", "q5": "Q5: Falsification",
        "q6": "Q6: Integration", "q7": "Q7: Strength Gaps",
        "summary": "Summary", "top_3_strengthening_actions": "Top 3 Actions",
    }
    lines = [
        f"# {STATION_ID} — Forward 7Q on {paper_name}",
        f"*Generated: {datetime.now().isoformat(timespec='seconds')} | Model: {MODEL}*",
        "",
    ]
    for k, label in labels.items():
        val = result.get(k, "")
        if isinstance(val, list):
            val = "\n".join(f"- {v}" for v in val)
        elif isinstance(val, dict):
            val = json.dumps(val, indent=2)
        lines += [f"## {label}", str(val), ""]
    out_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True)
    parser.add_argument("--out", dest="out", required=True)
    args = parser.parse_args()

    paper = Path(args.inp)
    content = paper.read_text(encoding="utf-8", errors="ignore")
    if len(content) > 6000:
        content = content[:6000] + "\n\n[...truncated for analysis...]"

    forward = call_openai(FORWARD_7Q_PROMPT.format(content=content))
    payload = {
        "station":      STATION_ID,
        "paper":        paper.name,
        "model":        MODEL,
        "computed_at":  datetime.now().isoformat(timespec="seconds"),
        "forward_7q":   forward,
    }
    Path(args.out).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(Path(args.out).with_suffix(".md"), paper.name, forward)

    err = forward.get("error") if isinstance(forward, dict) else None
    print(json.dumps({"status": "error" if err else "ok",
                      "error": err, "paper": paper.name}))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
