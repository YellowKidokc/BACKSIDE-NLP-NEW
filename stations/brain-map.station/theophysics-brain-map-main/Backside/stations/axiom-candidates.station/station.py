"""
Seven Questions Axiom Candidate Extractor
========================================

Reads refined 7QS JSON and produces axiom candidates.

Important boundary:
- This script does NOT promote claims directly into axioms.
- It surfaces load-bearing claims that may become axioms after review.
- Promotion requires reversal survival, dependency clarity, evidence pressure,
  and explicit kill conditions.

Pipeline:
Question -> Claim -> Dependency -> Reversal -> Evidence -> Axiom Candidate -> Promoted Axiom
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from seven_q_core import ensure_list, normalize_confidence, safe_str, slugify, today, write_json


SCHEMA = "seven_questions.axiom_candidates.v1"


def _load(path: str | Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def _confidence_from_foundation(value: Any) -> float:
    if isinstance(value, dict):
        return normalize_confidence(value.get("confidence", 0.5))
    return 0.5


def _severity_from_reversal(value: Any) -> float:
    if isinstance(value, dict):
        return normalize_confidence(value.get("severity", 0.5))
    return 0.5


def _evidence_strength(evidence: Dict[str, Any]) -> float:
    items = ensure_list(evidence.get("evidence_items", []))
    if not items:
        return 0.0
    strengths: List[float] = []
    for item in items:
        if isinstance(item, dict):
            strengths.append(normalize_confidence(item.get("strength", 0.5)))
        else:
            strengths.append(0.35)
    return round(sum(strengths) / max(len(strengths), 1), 3)


def _promotion_status(score: float, has_kill_conditions: bool, reversal_severity: float) -> str:
    if not has_kill_conditions:
        return "blocked_missing_kill_conditions"
    if score >= 0.82 and reversal_severity <= 0.35:
        return "promotion_ready"
    if score >= 0.66:
        return "strong_candidate"
    if score >= 0.50:
        return "candidate_needs_work"
    return "weak_candidate"


def _candidate_score(
    foundation_confidence: float,
    reversal_severity: float,
    evidence_strength: float,
    dependency_count: int,
    kill_count: int,
) -> float:
    dependency_score = min(dependency_count, 5) / 5 if dependency_count else 0.2
    kill_score = min(kill_count, 4) / 4 if kill_count else 0.0
    score = (
        foundation_confidence * 0.30
        + (1.0 - reversal_severity) * 0.25
        + evidence_strength * 0.20
        + dependency_score * 0.15
        + kill_score * 0.10
    )
    return round(max(0.0, min(1.0, score)), 3)


def _question_pairs() -> List[Tuple[str, str, str]]:
    return [
        ("q1", "r1", "Existence"),
        ("q2", "r2", "Distinction"),
        ("q3", "r3", "Substrate"),
        ("q4", "r4", "Order"),
        ("q5", "r5", "Observation"),
        ("q6", "r6", "Relation"),
        ("q7", "r7", "Coherence"),
    ]


def extract_candidates(seven_q: Dict[str, Any]) -> Dict[str, Any]:
    foundations = seven_q.get("foundations_7q", {})
    reversals = seven_q.get("reversals_7q", {})
    evidence = seven_q.get("evidence_7q", {})
    source_path = seven_q.get("source_path", "")
    paper = seven_q.get("paper", "Unknown")

    dependencies = ensure_list(foundations.get("load_bearing_assumptions", []))
    kill_conditions = ensure_list(reversals.get("kill_conditions", []))
    evidence_strength = _evidence_strength(evidence)
    weakest_link = safe_str(reversals.get("weakest_link", ""), 300)
    verdict = safe_str(reversals.get("verdict", ""), 80)

    candidates: List[Dict[str, Any]] = []
    for q_key, r_key, label in _question_pairs():
        f_val = foundations.get(q_key, {})
        r_val = reversals.get(r_key, {})
        foundation_confidence = _confidence_from_foundation(f_val)
        reversal_severity = _severity_from_reversal(r_val)

        claim_text = ""
        if isinstance(f_val, dict):
            claim_text = safe_str(f_val.get("answer") or f_val.get("needs") or f_val, 600)
        else:
            claim_text = safe_str(f_val, 600)

        if not claim_text:
            continue

        score = _candidate_score(
            foundation_confidence=foundation_confidence,
            reversal_severity=reversal_severity,
            evidence_strength=evidence_strength,
            dependency_count=len(dependencies),
            kill_count=len(kill_conditions),
        )
        status = _promotion_status(score, bool(kill_conditions), reversal_severity)

        candidates.append(
            {
                "id": f"AC-{slugify(paper, 28)}-{q_key.upper()}",
                "question": q_key.upper(),
                "question_label": label,
                "candidate_claim": claim_text,
                "source": {
                    "paper": paper,
                    "source_path": source_path,
                    "foundation_key": q_key,
                    "reversal_key": r_key,
                },
                "dependency_check": {
                    "load_bearing_dependencies": dependencies,
                    "dependency_count": len(dependencies),
                },
                "reversal_check": {
                    "attack": r_val,
                    "severity": reversal_severity,
                    "weakest_link": weakest_link,
                    "verdict": verdict,
                },
                "evidence_check": {
                    "evidence_strength": evidence_strength,
                    "evidence_verdict": evidence.get("e7_evidence_verdict", ""),
                    "missing_evidence": evidence.get("e3_missing_evidence", []),
                    "source_chases": evidence.get("top_3_source_chases", []),
                },
                "kill_conditions": kill_conditions,
                "candidate_score": score,
                "promotion_status": status,
                "caveat": "Axiom candidate only. Promote manually after denial, reversal, dependency, evidence, and kill-condition review.",
            }
        )

    return {
        "schema": SCHEMA,
        "created_at": datetime.now().isoformat(),
        "source_schema": seven_q.get("schema", ""),
        "paper": paper,
        "source_path": source_path,
        "pipeline": [
            "Question",
            "Claim",
            "Dependency",
            "Reversal",
            "Evidence",
            "Axiom Candidate",
            "Promoted Axiom",
        ],
        "rule": "The 7QS surfaces load-bearing claims. Axioms are what remain after denial, reversal, dependency, evidence, and kill-condition testing.",
        "candidates": candidates,
        "summary": {
            "candidate_count": len(candidates),
            "promotion_ready": len([c for c in candidates if c["promotion_status"] == "promotion_ready"]),
            "strong_candidate": len([c for c in candidates if c["promotion_status"] == "strong_candidate"]),
            "needs_work": len([c for c in candidates if c["promotion_status"] in ["candidate_needs_work", "blocked_missing_kill_conditions"]]),
        },
    }


def write_markdown(path: str | Path, result: Dict[str, Any]) -> Path:
    lines: List[str] = [
        f"# Axiom Candidates: {result.get('paper', 'Unknown')}",
        f"*Generated: {result.get('created_at', '')}*",
        "",
        f"> {result.get('rule', '')}",
        "",
        "## Pipeline",
        "",
        " -> ".join(result.get("pipeline", [])),
        "",
        "## Summary",
        "",
    ]
    summary = result.get("summary", {})
    for key, value in summary.items():
        lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")
    lines += ["", "## Candidates", ""]

    for candidate in result.get("candidates", []):
        lines += [
            f"### {candidate.get('id', '')}",
            "",
            f"**Question:** {candidate.get('question', '')} - {candidate.get('question_label', '')}",
            f"**Promotion Status:** {candidate.get('promotion_status', '')}",
            f"**Candidate Score:** {candidate.get('candidate_score', '')}",
            "",
            "**Candidate Claim**",
            "",
            safe_str(candidate.get("candidate_claim", "")),
            "",
            "**Caveat**",
            "",
            safe_str(candidate.get("caveat", "")),
            "",
            "**Weakest Link**",
            "",
            safe_str(candidate.get("reversal_check", {}).get("weakest_link", "")),
            "",
            "**Kill Conditions**",
            "",
        ]
        kills = ensure_list(candidate.get("kill_conditions", []))
        if kills:
            for kill in kills:
                lines.append(f"- {safe_str(kill)}")
        else:
            lines.append("- Missing. Candidate cannot promote until kill conditions are explicit.")
        lines.append("")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def run(seven_q_json: str | Path, output_dir: Optional[str | Path] = None) -> Dict[str, Any]:
    source = Path(seven_q_json)
    data = _load(source)
    result = extract_candidates(data)
    out_dir = Path(output_dir) if output_dir else source.parent / "_AXIOM_CANDIDATES"
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = slugify(source.stem)
    json_path = out_dir / f"{stem}_AXIOM_CANDIDATES_{today()}.json"
    md_path = out_dir / f"{stem}_AXIOM_CANDIDATES_{today()}.md"
    write_json(json_path, result)
    write_markdown(md_path, result)
    print(f"Saved: {json_path}")
    print(f"Saved: {md_path}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract axiom candidates from refined 7QS JSON.")
    parser.add_argument("--seven-q", required=True, help="Path to refined 7QS JSON")
    parser.add_argument("--output", help="Output directory")
    args = parser.parse_args()
    run(args.seven_q, args.output)
