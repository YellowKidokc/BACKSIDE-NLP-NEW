"""
Seven Questions Template Builder — Refined
=========================================
Builds human-readable Markdown artifacts from refined 7QS + Integration Pass JSON.

This replaces fragile regex-heavy filling for the common case while preserving the
concepts your old scripts already used:
- FACTS / 7QS infobox
- Seven Questions center
- Reversals / kill conditions
- Evidence pressure
- Integration map
- T-score and tier

If you need exact legacy template filling, keep your old template_filler.py as an
adapter. This file is the cleaner canonical artifact generator.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from seven_q_core import ensure_list, format_value_markdown, safe_str, slugify, today


def _load(path: str | Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _integration_payload(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not data:
        return {}
    return data.get("integration_pass") or data.get("promotion_pass") or data


def build_infobox(seven_q: Dict[str, Any], integration: Optional[Dict[str, Any]] = None) -> str:
    integration_payload = _integration_payload(integration)
    ib = integration_payload.get("infobox_fields", {}) if isinstance(integration_payload, dict) else {}
    metrics = seven_q.get("metrics", {})
    foundations = seven_q.get("foundations_7q", {})
    reversals = seven_q.get("reversals_7q", {})
    evidence = seven_q.get("evidence_7q", {})

    paper_name = seven_q.get("paper", "Unknown")
    claim = safe_str(foundations.get("central_claim") or seven_q.get("forward_7q", {}).get("q2"), 240)
    confidence = ib.get("confidence_label", metrics.get("tier", "Provisional"))
    t_score = metrics.get("t_score", "—")
    tier = metrics.get("tier", "—")
    deaths = metrics.get("death_tests_survived", "—")
    strongest = ib.get("strongest_q", {})
    weakest = ib.get("weakest_q", {})
    weakest_link = safe_str(reversals.get("weakest_link"), 160)
    evidence_verdict = safe_str(evidence.get("e7_evidence_verdict"), 180)
    iso_status = ib.get("iso_status") or integration_payload.get("i7_integration_verdict", {}).get("iso_status", "Partial")
    iso_hint = ib.get("iso_hint") or integration_payload.get("i7_integration_verdict", {}).get("one_sentence_verdict", "Run Integration Pass for deeper mapping.")

    return f"""> [!7qs-infobox]- Seven Questions Audit
>
> ## {paper_name}
>
> **{confidence}** | T = **{t_score}** | Tier = **{tier}** | Death Tests = **{deaths}/4**
>
> ### Core Claim
> {claim or '[claim not found]'}
>
> ### Strongest Signal
> **{strongest.get('q_num','?')} {strongest.get('q_label','?')}** — {safe_str(strongest.get('explanation','Run Integration Pass'), 120)}
>
> ### Weakest Pressure Point
> **{weakest.get('q_num','?')} {weakest.get('q_label','?')}** — {safe_str(weakest.get('explanation', weakest_link), 120)}
>
> ### Evidence Verdict
> {evidence_verdict or '[Run Evidence Mode]'}
>
> ### Isomorphism Status
> **{iso_status}** — {safe_str(iso_hint, 160)}
"""


def _q_answer(obj: Any) -> str:
    if isinstance(obj, dict):
        answer = obj.get("answer") or obj.get("attack") or obj.get("needs") or obj
        return format_value_markdown(answer)
    return format_value_markdown(obj)


def build_seven_questions_page(seven_q: Dict[str, Any], integration: Optional[Dict[str, Any]] = None) -> str:
    foundations = seven_q.get("foundations_7q", {})
    reversals = seven_q.get("reversals_7q", {})
    evidence = seven_q.get("evidence_7q", {})
    metrics = seven_q.get("metrics", {})
    integration_payload = _integration_payload(integration)

    title = foundations.get("central_claim") or seven_q.get("paper", "Seven Questions Analysis")
    title = safe_str(title, 120)

    lines: List[str] = []
    lines.append("---")
    lines.append(f'title: "{title}"')
    lines.append(f'source_file: "{seven_q.get("paper", "")}"')
    lines.append(f'created: {today()}')
    lines.append('system: "Seven Questions"')
    lines.append(f't_score: {metrics.get("t_score", "")}' )
    lines.append(f'tier: "{metrics.get("tier", "")}"')
    lines.append(f'death_tests_survived: {metrics.get("death_tests_survived", "")}' )
    lines.append("---")
    lines.append("")
    lines.append(build_infobox(seven_q, integration))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append("## Page Zero — What This Test Is Doing")
    lines.append("")
    lines.append("This page does not ask whether the article sounds persuasive. It asks what the claim requires, what breaks if it is denied, and what evidence would matter.")
    lines.append("")

    lines.append("## The Seven Questions")
    lines.append("")
    q_labels = [
        ("q1", "Existence"), ("q2", "Distinction"), ("q3", "Substrate"),
        ("q4", "Order"), ("q5", "Observation"), ("q6", "Relation"), ("q7", "Coherence"),
    ]
    for key, label in q_labels:
        val = foundations.get(key, {})
        needs = val.get("needs", "") if isinstance(val, dict) else ""
        conf = val.get("confidence", "") if isinstance(val, dict) else ""
        lines.append(f"### {key.upper()} — {label}")
        lines.append("")
        lines.append(_q_answer(val))
        if conf != "":
            lines.append(f"\n**Confidence:** {conf}")
        if needs:
            lines.append(f"\n**Needs:** {safe_str(needs, 200)}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Reversals — What Would Break This")
    lines.append("")
    r_labels = [
        ("r1", "Existence Reversal"), ("r2", "Distinction Reversal"), ("r3", "Substrate Reversal"),
        ("r4", "Order Reversal"), ("r5", "Observation Reversal"), ("r6", "Relation Reversal"), ("r7", "Coherence Reversal"),
    ]
    for key, label in r_labels:
        val = reversals.get(key, {})
        severity = val.get("severity", "") if isinstance(val, dict) else ""
        lines.append(f"### {key.upper()} — {label}")
        lines.append("")
        lines.append(_q_answer(val))
        if severity != "":
            lines.append(f"\n**Severity:** {severity}")
        lines.append("")

    lines.append("### Kill Conditions")
    lines.append("")
    kills = ensure_list(reversals.get("kill_conditions", []))
    if kills:
        lines.append("| # | Condition | Type | Decisive |")
        lines.append("|---|---|---|---|")
        for i, k in enumerate(kills, 1):
            if isinstance(k, dict):
                lines.append(f"| {i} | {safe_str(k.get('condition'), 120)} | {safe_str(k.get('type'), 30)} | {safe_str(k.get('decisive'), 20)} |")
            else:
                lines.append(f"| {i} | {safe_str(k, 120)} | — | — |")
    else:
        lines.append("[No kill conditions generated. Rerun Reversals Mode or add manually.]")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Evidence Pressure")
    lines.append("")
    lines.append("### Evidence Verdict")
    lines.append(format_value_markdown(evidence.get("e7_evidence_verdict", "")))
    lines.append("")
    lines.append("### Evidence Items")
    items = ensure_list(evidence.get("evidence_items", []))
    if items:
        lines.append("| Item | Type | Strength |")
        lines.append("|---|---|---|")
        for item in items:
            if isinstance(item, dict):
                lines.append(f"| {safe_str(item.get('name'), 100)} | {safe_str(item.get('type'), 30)} | {safe_str(item.get('strength'), 20)} |")
            else:
                lines.append(f"| {safe_str(item, 100)} | — | — |")
    else:
        lines.append("[No evidence items generated.]")
    lines.append("")

    lines.append("### Missing Evidence")
    lines.append(format_value_markdown(evidence.get("e3_missing_evidence", [])))
    lines.append("")

    if integration_payload:
        lines.append("---")
        lines.append("")
        lines.append("## Integration Pass")
        lines.append("")
        verdict = integration_payload.get("i7_integration_verdict", {})
        lines.append(f"**Status:** {safe_str(verdict.get('iso_status', ''))}")
        lines.append("")
        lines.append(f"**Best Use:** {safe_str(verdict.get('best_use', ''))}")
        lines.append("")
        lines.append(f"**Verdict:** {safe_str(verdict.get('one_sentence_verdict', ''))}")
        lines.append("")
        lines.append("### Isomorphism Map")
        iso = ensure_list(integration_payload.get("i3_isomorphism_map", []))
        if iso:
            lines.append("| Domain A | Domain B | Mapping | Quality | Transfers Equations |")
            lines.append("|---|---|---|---|---|")
            for row in iso:
                if isinstance(row, dict):
                    lines.append(f"| {safe_str(row.get('domain_a'),40)} | {safe_str(row.get('domain_b'),40)} | {safe_str(row.get('mapping'),100)} | {safe_str(row.get('quality'),30)} | {safe_str(row.get('equations_transfer'),10)} |")
        else:
            lines.append("[No isomorphism map generated.]")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Audit Notes")
    lines.append("")
    lines.append("- [ ] Human reviewed")
    lines.append("- [ ] Citations chased")
    lines.append("- [ ] Kill conditions manually approved")
    lines.append("- [ ] Structural vs analogical mappings verified")
    lines.append("- [ ] Ready for Proof Explorer")
    lines.append("")

    return "\n".join(lines)


def build_from_files(seven_q_json: str | Path, integration_json: Optional[str | Path] = None, output_dir: Optional[str | Path] = None) -> Path:
    seven_q = _load(seven_q_json)
    integration = _load(integration_json) if integration_json else None
    output = Path(output_dir) if output_dir else Path(seven_q_json).parent / "PAGES"
    output.mkdir(parents=True, exist_ok=True)
    stem = slugify(Path(seven_q_json).stem.replace("_7QS_", "_"))
    out_path = output / f"{stem}_PROOF_PAGE.md"
    out_path.write_text(build_seven_questions_page(seven_q, integration), encoding="utf-8")
    print(f"  Proof page: {out_path.name}")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a Seven Questions proof page from JSON outputs.")
    parser.add_argument("--seven-q", required=True, help="Refined 7QS JSON")
    parser.add_argument("--integration", help="Optional Integration Pass JSON")
    parser.add_argument("--output", help="Output directory")
    args = parser.parse_args()
    build_from_files(args.seven_q, args.integration, args.output)
