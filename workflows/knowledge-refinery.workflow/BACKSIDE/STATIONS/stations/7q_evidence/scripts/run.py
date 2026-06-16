"""
ST-SEVENQ-003 — 7Q Evidence Pressure.

Reads forward + reverse 7Q outputs, identifies missing evidence, classifies
each evidence statement, and prepares citation targets.

Evidence classes:
    direct       — primary data / direct measurement / replication
    indirect     — supporting data from related domain
    analogical   — argument by structural analogy only
    weak         — present but underpowered / outdated / single source
    conflicting  — evidence cuts against the claim

Usage:
    python run.py --in <source.md> --out <evidence_7q.json>
    Optional: --forward <forward_7q.json>  --reverse <reverse_7q.json>

Outputs: evidence_7q.json + citation_targets.md + evidence_gaps.yml.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

STATION_ID = "ST-SEVENQ-003"
MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are an evidence auditor. You do not validate or attack claims.
You inventory what evidence exists, classify its strength, and name what's missing.
Return only valid JSON. No markdown fences. No preamble."""

EVIDENCE_PROMPT = """The paper has already been classified (forward 7Q) and pressure-tested (reverse 7Q).
Now: PRESSURE THE EVIDENCE.

Task:
1. EXTRACT every concrete evidence statement the paper makes (or implies).
2. CLASSIFY each one as: direct | indirect | analogical | weak | conflicting.
3. NAME gaps: claims that should have evidence but don't.
4. PROPOSE citation targets: specific papers, datasets, or studies that would close gaps.

Be specific. Name real authors/journals/datasets where possible.

{prior_context}
PAPER CONTENT:
{content}

Respond in JSON with this exact shape:

{{
  "evidence": [
    {{"text": "...", "class": "direct|indirect|analogical|weak|conflicting",
      "supports": "claim id or short claim text", "source_hint": "..." }}
  ],
  "gaps": [
    {{"claim": "...", "missing_evidence": "...", "severity": "low|medium|high"}}
  ],
  "citation_targets": [
    {{"target": "author/dataset/paper", "rationale": "...", "would_close_gap": "..."}}
  ],
  "summary": {{
    "direct_count": 0, "indirect_count": 0, "analogical_count": 0,
    "weak_count": 0, "conflicting_count": 0, "gap_count": 0
  }}
}}"""


def call_openai(user_prompt: str, max_tokens: int = 2500) -> dict:
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
    parser.add_argument("--forward", default=None)
    parser.add_argument("--reverse", default=None)
    args = parser.parse_args()

    paper = Path(args.inp)
    content = paper.read_text(encoding="utf-8", errors="ignore")
    if len(content) > 5500:
        content = content[:5500] + "\n\n[...truncated for analysis...]"

    prior_bits = []
    for tag, path_str in (("FORWARD 7Q", args.forward), ("REVERSE 7Q", args.reverse)):
        if path_str and Path(path_str).exists():
            try:
                payload = json.loads(Path(path_str).read_text(encoding="utf-8"))
                inner = payload.get("forward_7q") or payload.get("reverse_7q") or payload
                prior_bits.append(f"{tag} CONTEXT:\n{json.dumps(inner, indent=2)[:1200]}\n")
            except Exception:
                pass
    prior_context = "\n".join(prior_bits) + ("\n" if prior_bits else "")

    result = call_openai(EVIDENCE_PROMPT.format(prior_context=prior_context, content=content))

    payload = {
        "station":     STATION_ID,
        "paper":       paper.name,
        "model":       MODEL,
        "computed_at": datetime.now().isoformat(timespec="seconds"),
        **(result if isinstance(result, dict) else {"result": result}),
    }
    out_path = Path(args.out)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # citation_targets.md
    ct = result.get("citation_targets", []) if isinstance(result, dict) else []
    md_lines = [f"# {STATION_ID} — Citation Targets for {paper.name}", ""]
    for i, t in enumerate(ct, 1):
        md_lines.append(f"## {i}. {t.get('target','?')}")
        md_lines.append(f"- **Rationale:** {t.get('rationale','')}")
        md_lines.append(f"- **Would close gap:** {t.get('would_close_gap','')}")
        md_lines.append("")
    out_path.with_name("citation_targets.md").write_text("\n".join(md_lines), encoding="utf-8")

    # evidence_gaps.yml
    gaps = result.get("gaps", []) if isinstance(result, dict) else []
    yml_lines = [f"station: {STATION_ID}", f"paper: {json.dumps(paper.name)}", "gaps:"]
    for g in gaps:
        yml_lines += [
            f"  - claim: {json.dumps(g.get('claim',''))}",
            f"    missing_evidence: {json.dumps(g.get('missing_evidence',''))}",
            f"    severity: {g.get('severity','medium')}",
        ]
    out_path.with_name("evidence_gaps.yml").write_text("\n".join(yml_lines) + "\n", encoding="utf-8")

    err = result.get("error") if isinstance(result, dict) else None
    print(json.dumps({"status": "error" if err else "ok",
                      "error": err,
                      "evidence_count": len(result.get("evidence", []) if isinstance(result, dict) else []),
                      "gap_count": len(gaps)}))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
