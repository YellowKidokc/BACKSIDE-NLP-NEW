"""
ST-SEVENQ-002 — 7Q Reverse (Proof by Exhaustive Elimination).

Attempts to DISPROVE the central claim by working backwards.
If the claim survives, it is strengthened. If it fails, we know exactly where.

Extracted from seven_q_runner.py REVERSE_7Q_PROMPT.

Usage:
    python run.py --in <source.md> --out <reverse_7q.json>

Optional second input: pass `--forward <forward_7q.json>` to give the reverse
pass the forward classification for context (recommended).

Output: reverse_7q.json + reverse_7q.md + kill_conditions.yml.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

STATION_ID = "ST-SEVENQ-002"
MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are a rigorous academic analyst specializing in cross-domain research.
You apply the 7-Question Scientific Method with maximum intellectual honesty.
Be the best possible adversary. Then report honestly."""

REVERSE_7Q_PROMPT = """Apply the 7-Question Scientific Method (REVERSE — Proof by Exhaustive Elimination) to this paper.

The goal: Attempt to DISPROVE the central claim by working backwards.
If the claim survives, it is strengthened. If it fails, we know exactly where.

Reverse 7Q Process:
R1: STATE the central claim precisely
R2: LIST all assumptions the claim depends on
R3: CHALLENGE each assumption — what would have to be true for it to fail?
R4: IDENTIFY the single weakest link in the logical chain
R5: PROPOSE the strongest possible counter-theory
R6: ASSESS — does the claim survive this attack? What remains unresolved?
R7: PRESCRIBE — what specific work would settle the remaining question?

Be the best possible adversary. Then report honestly.

{forward_context}
PAPER CONTENT:
{content}

Respond in structured JSON with keys: r1, r2, r3, r4, r5, r6, r7, verdict, confidence_score"""


def call_openai(user_prompt: str, max_tokens: int = 2000) -> dict:
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
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}


def write_markdown(out_md: Path, paper_name: str, result: dict) -> None:
    labels = {
        "r1": "R1: Claim", "r2": "R2: Assumptions", "r3": "R3: Challenge",
        "r4": "R4: Weakest Link", "r5": "R5: Counter-Theory",
        "r6": "R6: Assessment", "r7": "R7: Prescription",
        "verdict": "Verdict", "confidence_score": "Confidence Score",
    }
    lines = [
        f"# {STATION_ID} — Reverse 7Q on {paper_name}",
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


def write_kill_conditions(out_yml: Path, result: dict) -> None:
    weakest = result.get("r4", "")
    assumptions = result.get("r2", [])
    if isinstance(assumptions, str):
        assumptions = [assumptions]
    lines = [
        f"station: {STATION_ID}",
        f"weakest_link: {json.dumps(weakest)}",
        "kill_conditions:",
    ]
    for a in assumptions[:5]:
        lines.append(f"  - {json.dumps(str(a))}")
    out_yml.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True)
    parser.add_argument("--out", dest="out", required=True)
    parser.add_argument("--forward", default=None,
                        help="Optional path to forward_7q.json for context.")
    args = parser.parse_args()

    paper = Path(args.inp)
    content = paper.read_text(encoding="utf-8", errors="ignore")
    if len(content) > 6000:
        content = content[:6000] + "\n\n[...truncated for analysis...]"

    forward_context = ""
    if args.forward and Path(args.forward).exists():
        try:
            fwd = json.loads(Path(args.forward).read_text(encoding="utf-8"))
            fwd_inner = fwd.get("forward_7q", fwd)
            forward_context = f"FORWARD 7Q CONTEXT (for reference):\n{json.dumps(fwd_inner, indent=2)[:1500]}\n\n"
        except Exception:
            pass

    reverse = call_openai(REVERSE_7Q_PROMPT.format(
        forward_context=forward_context, content=content))

    payload = {
        "station":     STATION_ID,
        "paper":       paper.name,
        "model":       MODEL,
        "computed_at": datetime.now().isoformat(timespec="seconds"),
        "reverse_7q":  reverse,
    }
    out_path = Path(args.out)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(out_path.with_suffix(".md"), paper.name, reverse)
    write_kill_conditions(out_path.with_name("kill_conditions.yml"), reverse)

    err = reverse.get("error") if isinstance(reverse, dict) else None
    print(json.dumps({"status": "error" if err else "ok",
                      "error": err, "verdict": reverse.get("verdict")}))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
