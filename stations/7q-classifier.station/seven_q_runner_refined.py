"""
Seven Questions Runner — Refined
================================
Runs the public-facing Seven Questions system in three modes:

F — Foundations: what the paper builds.
R — Reversals: what breaks if the claim is denied or attacked.
E — Evidence: what reality, literature, data, or tests put pressure on the claim.

Compatibility:
- Keeps legacy keys forward_7q and reverse_7q.
- Adds evidence_7q and seven_questions metadata.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from seven_q_core import (
    DEFAULT_MODEL,
    MODES,
    SEVEN_QUESTIONS,
    call_openai_json,
    compute_tscore,
    ensure_list,
    format_value_markdown,
    read_text,
    safe_str,
    slugify,
    today,
    write_json,
)

SYSTEM_PROMPT = """You are an intellectually rigorous research analyst.
You are evaluating original cross-domain theoretical writing.
Your task is not to flatter the author and not to dismiss the paper prematurely.
Your job is to expose structure: what is claimed, what grounds it, what would break it, and what evidence would matter.

Rules:
- Separate observation from inference.
- Separate structural isomorphism from analogy.
- Name real theories, authors, journals, and fields when relevant.
- Be direct about weaknesses.
- Do not invent citations. If unsure, mark citation_needed.
- Return ONLY valid JSON.
"""

FOUNDATIONS_PROMPT = """Run the SEVEN QUESTIONS — FOUNDATIONS MODE on this paper.

Use these seven public-facing questions:
Q1 Existence — What must exist for this claim to have a referent?
Q2 Distinction — What distinction does this claim depend on or introduce?
Q3 Substrate — What carries, grounds, or instantiates the claim?
Q4 Order — What structure or ordering principle is required?
Q5 Observation — What would make the claim empirically, phenomenally, or logically observable?
Q6 Relation — How does the claim connect domains, agents, variables, or systems?
Q7 Coherence — What would preserve or destroy coherence across the whole system?

Return this exact JSON object:
{
  "q1": {"label":"Existence", "answer":"...", "confidence":0.0, "needs":"..."},
  "q2": {"label":"Distinction", "answer":"...", "confidence":0.0, "needs":"..."},
  "q3": {"label":"Substrate", "answer":"...", "confidence":0.0, "needs":"..."},
  "q4": {"label":"Order", "answer":"...", "confidence":0.0, "needs":"..."},
  "q5": {"label":"Observation", "answer":"...", "confidence":0.0, "needs":"..."},
  "q6": {"label":"Relation", "answer":"...", "confidence":0.0, "needs":"..."},
  "q7": {"label":"Coherence", "answer":"...", "confidence":0.0, "needs":"..."},
  "posture":"humble|assertive|mixed|unclear",
  "domains":["..."],
  "central_claim":"one precise sentence",
  "load_bearing_assumptions":["..."],
  "summary":"short, honest summary",
  "top_3_strengthening_actions":["..."]
}

PAPER CONTENT:
{content}
"""

REVERSALS_PROMPT = """Run the SEVEN QUESTIONS — REVERSALS MODE on this paper.

Attack the central claim by reversing each question:
R1 Existence — What if the claimed referent does not exist or is misidentified?
R2 Distinction — What if the key distinction is false, blurred, or arbitrary?
R3 Substrate — What if the proposed grounding substrate is unnecessary or wrong?
R4 Order — What if the apparent order is imposed, cherry-picked, or overfit?
R5 Observation — What if the observable consequences do not follow?
R6 Relation — What if the cross-domain bridge is analogy, not structure?
R7 Coherence — What contradiction, regress, or collapse would defeat the claim?

Be the strongest possible adversary. Then report honestly.

Return this exact JSON object:
{
  "r1": {"label":"Existence Reversal", "attack":"...", "severity":0.0},
  "r2": {"label":"Distinction Reversal", "attack":"...", "severity":0.0},
  "r3": {"label":"Substrate Reversal", "attack":"...", "severity":0.0},
  "r4": {"label":"Order Reversal", "attack":"...", "severity":0.0},
  "r5": {"label":"Observation Reversal", "attack":"...", "severity":0.0},
  "r6": {"label":"Relation Reversal", "attack":"...", "severity":0.0},
  "r7": {"label":"Coherence Reversal", "attack":"...", "severity":0.0},
  "weakest_link":"single weakest point",
  "strongest_counter_theory":"best alternative explanation",
  "kill_conditions":[{"condition":"...", "type":"logical|empirical|historical|mathematical|isomorphic", "decisive":true}],
  "verdict":"survives|survives_with_work|partial|fails",
  "confidence_score":0.0,
  "prescription":"specific work needed next"
}

PAPER CONTENT:
{content}
"""

EVIDENCE_PROMPT = """Run the SEVEN QUESTIONS — EVIDENCE MODE on this paper.

Do not merely list evidence. Classify evidence pressure.
For each item, distinguish: direct support, indirect support, analogy, missing evidence, counter-evidence.

Return this exact JSON object:
{
  "e1_observations":["what is actually observed or asserted as observed"],
  "e2_sources":[{"claim":"...", "source_or_citation":"...", "status":"provided|citation_needed|external_needed", "confidence":0.0}],
  "e3_missing_evidence":["..."],
  "e4_counter_evidence":[{"counter":"...", "strength":0.0, "response_needed":"..."}],
  "e5_domain_bridges":[{"domain_a":"...", "domain_b":"...", "bridge":"...", "quality":"structural|analogical|weak|contested", "transfers_equations":false}],
  "e6_predictions":[{"prediction":"...", "testable":true, "decisive":false}],
  "e7_evidence_verdict":"short evidence verdict",
  "evidence_items":[{"name":"...", "type":"empirical|formal|historical|scriptural|mathematical|conceptual", "strength":0.0}],
  "top_3_source_chases":["..."]
}

PAPER CONTENT:
{content}
"""


def legacy_forward(foundations: Dict[str, Any]) -> Dict[str, Any]:
    """Provide compatibility with older q0-q7 consumers."""
    domains = foundations.get("domains", [])
    return {
        "q0": foundations.get("posture", ""),
        "q1": domains,
        "q2": foundations.get("central_claim", safe_str(foundations.get("q2", {}).get("answer", ""))),
        "q3": foundations.get("q5", {}),
        "q4": foundations.get("load_bearing_assumptions", []),
        "q5": safe_str(foundations.get("q7", {}).get("needs", "")) or "See reversals kill_conditions.",
        "q6": foundations.get("q6", {}),
        "q7": foundations.get("top_3_strengthening_actions", []),
        "summary": foundations.get("summary", ""),
        "top_3_strengthening_actions": foundations.get("top_3_strengthening_actions", []),
    }


def legacy_reverse(reversals: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "r1": reversals.get("r1", {}),
        "r2": reversals.get("r2", {}),
        "r3": reversals.get("r3", {}),
        "r4": reversals.get("weakest_link", safe_str(reversals.get("r4", {}))),
        "r5": reversals.get("strongest_counter_theory", safe_str(reversals.get("r5", {}))),
        "r6": reversals.get("verdict", ""),
        "r7": reversals.get("prescription", ""),
        "verdict": reversals.get("verdict", ""),
        "confidence_score": reversals.get("confidence_score", 0.5),
    }


def run_paper(paper_path: str | Path, output_dir: Optional[str | Path] = None, max_chars: int = 12000, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    paper = Path(paper_path)
    content = read_text(paper, max_chars=max_chars)

    print(f"  7QS Foundations: {paper.name}")
    foundations = call_openai_json(FOUNDATIONS_PROMPT.format(content=content), SYSTEM_PROMPT, model=model, max_tokens=3500)

    print(f"  7QS Reversals:   {paper.name}")
    reversals = call_openai_json(REVERSALS_PROMPT.format(content=content), SYSTEM_PROMPT, model=model, max_tokens=3500)

    print(f"  7QS Evidence:    {paper.name}")
    evidence = call_openai_json(EVIDENCE_PROMPT.format(content=content), SYSTEM_PROMPT, model=model, max_tokens=3500)

    forward_legacy = legacy_forward(foundations)
    reverse_legacy = legacy_reverse(reversals)
    tscore, tier, deaths = compute_tscore(forward_legacy, reverse_legacy, evidence)

    result = {
        "schema": "seven_questions.refined.v1",
        "paper": paper.name,
        "source_path": str(paper),
        "analyzed_at": datetime.now().isoformat(),
        "model": model,
        "seven_questions": SEVEN_QUESTIONS,
        "modes": MODES,
        "foundations_7q": foundations,
        "reversals_7q": reversals,
        "evidence_7q": evidence,
        "forward_7q": forward_legacy,
        "reverse_7q": reverse_legacy,
        "metrics": {"t_score": tscore, "tier": tier, "death_tests_survived": deaths},
    }

    out_dir = Path(output_dir) if output_dir else paper.parent / "_7QS_ANALYSIS"
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = slugify(paper.stem)
    json_path = out_dir / f"{stem}_7QS_{today()}.json"
    md_path = out_dir / f"{stem}_7QS_{today()}.md"
    write_json(json_path, result)
    write_markdown(md_path, result)
    print(f"  Saved: {json_path.name}")
    return result


def write_markdown(path: str | Path, result: Dict[str, Any]) -> Path:
    lines: List[str] = []
    metrics = result.get("metrics", {})
    lines += [
        f"# Seven Questions Analysis: {result.get('paper','Unknown')}",
        f"*Generated: {result.get('analyzed_at','')} | Model: {result.get('model','')}*",
        f"*T-Score: {metrics.get('t_score','—')} | Tier: {metrics.get('tier','—')} | Death Tests: {metrics.get('death_tests_survived','—')}/4*",
        "",
        "---",
        "",
        "## The Seven Questions — Foundations",
        "",
    ]
    f = result.get("foundations_7q", {})
    for q in ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]:
        val = f.get(q, {})
        label = val.get("label", q.upper()) if isinstance(val, dict) else q.upper()
        lines += [f"### {q.upper()} — {label}", format_value_markdown(val), ""]
    lines += ["### Central Claim", safe_str(f.get("central_claim", "")), "", "### Top Actions", format_value_markdown(f.get("top_3_strengthening_actions", [])), ""]

    lines += ["---", "", "## The Seven Questions — Reversals", ""]
    r = result.get("reversals_7q", {})
    for q in ["r1", "r2", "r3", "r4", "r5", "r6", "r7"]:
        val = r.get(q, {})
        label = val.get("label", q.upper()) if isinstance(val, dict) else q.upper()
        lines += [f"### {q.upper()} — {label}", format_value_markdown(val), ""]
    for key in ["weakest_link", "strongest_counter_theory", "kill_conditions", "verdict", "prescription"]:
        lines += [f"### {key.replace('_',' ').title()}", format_value_markdown(r.get(key, "")), ""]

    lines += ["---", "", "## The Seven Questions — Evidence", ""]
    e = result.get("evidence_7q", {})
    for key, val in e.items():
        lines += [f"### {key.replace('_',' ').title()}", format_value_markdown(val), ""]

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def run_folder(folder_path: str | Path, output_dir: Optional[str | Path] = None, max_chars: int = 12000, model: str = DEFAULT_MODEL) -> List[Dict[str, Any]]:
    folder = Path(folder_path)
    papers = sorted([p for p in folder.glob("*.md") if not p.name.startswith("00") and not p.name.startswith("_")])
    print(f"Running refined 7QS on {len(papers)} papers in {folder}")
    return [run_paper(p, output_dir=output_dir, max_chars=max_chars, model=model) for p in papers]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run refined Seven Questions analysis on one paper or a folder.")
    parser.add_argument("--paper", help="Single markdown paper path")
    parser.add_argument("--folder", help="Folder containing markdown papers")
    parser.add_argument("--output", help="Output directory")
    parser.add_argument("--max-chars", type=int, default=12000)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    if args.paper:
        run_paper(args.paper, args.output, args.max_chars, args.model)
    elif args.folder:
        run_folder(args.folder, args.output, args.max_chars, args.model)
    else:
        parser.print_help()
