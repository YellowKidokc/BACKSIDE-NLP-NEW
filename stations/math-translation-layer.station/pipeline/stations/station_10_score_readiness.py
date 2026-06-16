from __future__ import annotations

from pathlib import Path
from typing import Any

from pipeline.stations.common import paper_output_dir, read_json, utc_now, write_json


TRACKS = ("Academic_Readiness", "Framework_Coherence", "Public_Communication", "Risk")


def _load_optional(output_dir: Path, filename: str, default: dict[str, Any]) -> dict[str, Any]:
    path = output_dir / filename
    return read_json(path) if path.exists() else default


def _event(points: int, source_reference: str, reason: str, fix: str) -> dict[str, Any]:
    return {
        "points": points,
        "source_reference": source_reference,
        "reason": reason,
        "fix_to_improve": fix,
    }


def _typing_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("claim_typing") or payload.get("claims") or payload.get("typed_claims") or []


def _claim_count(claims: dict[str, Any]) -> int:
    return len(claims.get("claims", []))


def _evidence_stats(evidence: dict[str, Any]) -> tuple[int, int]:
    rows = evidence.get("rows", [])
    missing = sum(1 for row in rows if row.get("strength") == "missing" or row.get("evidence_type") == "missing")
    return len(rows), missing


def _objection_stats(objections: dict[str, Any]) -> dict[str, int]:
    stats = {"critical": 0, "serious": 0, "minor": 0}
    for objection in objections.get("objections", []):
        severity = objection.get("severity")
        if severity in stats:
            stats[severity] += 1
    return stats


def _routing_stats(targets: dict[str, Any]) -> dict[str, int]:
    return targets.get("target_counts", {})


def _overstatement_count(typing: dict[str, Any]) -> int:
    return sum(len(item.get("overstatement_flags") or []) for item in _typing_items(typing))


def _equation_need_count(typing: dict[str, Any]) -> int:
    return sum(1 for item in _typing_items(typing) if item.get("equation_semantics_needed"))


def build_tracks(
    claims: dict[str, Any],
    typing: dict[str, Any],
    evidence: dict[str, Any],
    forward: dict[str, Any],
    reverse: dict[str, Any],
    targets: dict[str, Any],
    objections: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    total_claims = _claim_count(claims)
    evidence_rows, missing_evidence = _evidence_stats(evidence)
    objection_counts = _objection_stats(objections)
    target_counts = _routing_stats(targets)
    overstatements = _overstatement_count(typing)
    equation_needs = _equation_need_count(typing)
    forward_count = len(forward.get("results", []))
    reverse_count = len(reverse.get("results", []))
    formal_count = sum(count for target, count in target_counts.items() if target != "Bridge-only / not formal yet")

    academic_positive = [
        _event(10, "03_claims.json", f"{total_claims} claims reconstructed for audit.", "Keep claim extraction aligned with section headings."),
        _event(8, "05_evidence.json", f"{evidence_rows} evidence rows available for source tracing.", "Replace weak or missing rows with primary sources."),
    ]
    academic_deductions = []
    if missing_evidence:
        academic_deductions.append(
            _event(-min(20, missing_evidence * 3), "05_evidence.json", f"{missing_evidence} claim(s) have missing detected evidence.", "Add direct primary/secondary source bridges.")
        )
    if objection_counts["critical"]:
        academic_deductions.append(
            _event(-min(20, objection_counts["critical"] * 5), "09_objections.json", "Critical reviewer objections remain open.", "Resolve or downgrade each critical objection.")
        )

    framework_positive = [
        _event(10, "06_7q_forward.json", f"{forward_count} forward 7Q records generated.", "Tighten mechanism/dependency fields where generic."),
        _event(10, "07_7q_reverse.json", f"{reverse_count} reverse 7Q records generated.", "Convert downgrade conditions into explicit kill tests."),
    ]
    framework_deductions = []
    bridge_only = target_counts.get("Bridge-only / not formal yet", 0)
    if bridge_only:
        framework_deductions.append(
            _event(-min(15, bridge_only * 2), "08_formal_targets.json", f"{bridge_only} claim(s) remain bridge-only.", "Add domain-boundary bridges or formal lemmas before treating them as proven.")
        )

    public_positive = [
        _event(8, "04_claim_typing.json", "Claim typing separates domain badges and public communication risk.", "Keep public-facing claims narrower than internal framework claims.")
    ]
    public_deductions = []
    if overstatements:
        public_deductions.append(
            _event(-min(20, overstatements * 4), "04_claim_typing.json", f"{overstatements} overstatement flag(s) detected.", "Replace absolute language with scoped, test-conditioned phrasing.")
        )
    if objection_counts["serious"]:
        public_deductions.append(
            _event(-min(12, objection_counts["serious"] * 3), "09_objections.json", "Serious objections may confuse public interpretation.", "Add explanatory boundary notes near affected claims.")
        )

    risk_positive = [
        _event(8, "08_formal_targets.json", f"{formal_count} claim(s) routed to formal or model targets.", "Keep formal target status visible in final reports.")
    ]
    risk_deductions = []
    if equation_needs:
        risk_deductions.append(
            _event(-min(16, equation_needs * 4), "04_claim_typing.json", f"{equation_needs} claim(s) need equation semantics review.", "Label equation role/status before publication.")
        )
    if objection_counts["critical"] or overstatements:
        risk_deductions.append(
            _event(-min(20, objection_counts["critical"] * 5 + overstatements * 2), "09_objections.json", "Critical objections or overstatement flags increase audit risk.", "Close critical objections and soften claims before external review.")
        )

    tracks = {
        "Academic_Readiness": {
            "positive_score_events": academic_positive,
            "deductions": academic_deductions,
            "score": max(0, 50 + sum(item["points"] for item in academic_positive + academic_deductions)),
            "readiness": "review_ready_with_repairs" if not objection_counts["critical"] else "not_ready",
        },
        "Framework_Coherence": {
            "positive_score_events": framework_positive,
            "deductions": framework_deductions,
            "score": max(0, 50 + sum(item["points"] for item in framework_positive + framework_deductions)),
            "readiness": "internally_traceable" if forward_count and reverse_count else "needs_framework_pass",
        },
        "Public_Communication": {
            "positive_score_events": public_positive,
            "deductions": public_deductions,
            "score": max(0, 50 + sum(item["points"] for item in public_positive + public_deductions)),
            "readiness": "needs_language_review" if overstatements else "public_summary_ready",
        },
        "Risk": {
            "positive_score_events": risk_positive,
            "deductions": risk_deductions,
            "score": max(0, 50 + sum(item["points"] for item in risk_positive + risk_deductions)),
            "readiness": "risk_review_required" if risk_deductions else "risk_tracked",
        },
    }
    return tracks


def run(paper_uuid: str) -> dict[str, Any]:
    output_dir = paper_output_dir(paper_uuid)
    claims = read_json(output_dir / "03_claims.json")
    typing = read_json(output_dir / "04_claim_typing.json")
    evidence = read_json(output_dir / "05_evidence.json")
    forward = read_json(output_dir / "06_7q_forward.json")
    reverse = read_json(output_dir / "07_7q_reverse.json")
    targets = read_json(output_dir / "08_formal_targets.json")
    objections = _load_optional(output_dir, "09_objections.json", {"paper_uuid": paper_uuid, "objections": []})

    tracks = build_tracks(claims, typing, evidence, forward, reverse, targets, objections)
    payload = {
        "paper_uuid": paper_uuid,
        "station": "10_score_readiness",
        "timestamp": utc_now(),
        "tracks": tracks,
        "track_order": list(TRACKS),
        "contract": "four independent audit tracks; no blended final truth score",
    }
    write_json(output_dir / "10_score_ledger.json", payload)
    write_human(output_dir / "10_score_ledger_human.md", payload)
    return payload


def write_human(path: Path, payload: dict[str, Any]) -> None:
    lines = [f"# Score/Readiness Ledger - {payload['paper_uuid']}", "", payload["contract"], ""]
    for track_name in payload["track_order"]:
        track = payload["tracks"][track_name]
        lines += [f"## {track_name}", "", f"- Score: {track['score']}", f"- Readiness: {track['readiness']}", ""]
        lines += ["### Positive Score Events", ""]
        for event in track["positive_score_events"]:
            lines.append(f"- {event['points']} from `{event['source_reference']}`: {event['reason']} Fix: {event['fix_to_improve']}")
        lines += ["", "### Deductions", ""]
        if not track["deductions"]:
            lines.append("- None.")
        for event in track["deductions"]:
            lines.append(f"- {event['points']} from `{event['source_reference']}`: {event['reason']} Fix: {event['fix_to_improve']}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
