from __future__ import annotations

import csv
import html
from pathlib import Path
from typing import Any

from pipeline.stations.common import ROOT, paper_output_dir, read_json, utc_now, write_json


SNAPSHOT_ORDER = [
    "CLAIM_ARCH",
    "EVIDENCE_CHAIN",
    "KILL_ARCH",
    "EQ_SEM",
    "DOMAIN_BOUNDARY",
    "REVIEWER_SEEDS",
    "LEDGER_SCHEMA",
    "OVERSTATE_PATTERN",
    "BENCHMARK_ANCHOR",
    "CROSS_DEP",
    "EIGHT_GAPS",
]

EIGHT_GAPS = [
    "Score separation",
    "Hostile reviewer",
    "Evidence bridge",
    "Domain badge",
    "Score ledger",
    "Equation semantics",
    "Overstatement",
    "Benchmark/risk context",
]


def _load_optional(output_dir: Path, filename: str) -> dict[str, Any]:
    path = output_dir / filename
    if not path.exists():
        return {"missing": True, "filename": filename}
    return read_json(path)


def _typing_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("claim_typing") or payload.get("claims") or payload.get("typed_claims") or []


def _group_by(items: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        grouped.setdefault(str(item.get(key, "")), []).append(item)
    return grouped


def _component(name: str, findings: list[dict[str, Any]], flags: list[str] | None = None) -> dict[str, Any]:
    return {
        "component": name,
        "findings": findings,
        "score_events": [],
        "flags": flags or [],
        "evidence_quotes": [],
    }


def build_snapshot(output_dir: Path, paper_uuid: str) -> dict[str, Any]:
    intake = _load_optional(output_dir, "00_intake.json")
    claims = _load_optional(output_dir, "03_claims.json")
    typing = _load_optional(output_dir, "04_claim_typing.json")
    evidence = _load_optional(output_dir, "05_evidence.json")
    reverse = _load_optional(output_dir, "07_7q_reverse.json")
    targets = _load_optional(output_dir, "08_formal_targets.json")
    objections = _load_optional(output_dir, "09_objections.json")
    score = _load_optional(output_dir, "10_score_ledger.json")

    claim_items = claims.get("claims", [])
    typing_items = _typing_items(typing)
    typing_by_claim = {item.get("claim_uuid"): item for item in typing_items}
    evidence_by_claim = _group_by(evidence.get("rows", []), "claim_uuid")
    reverse_by_claim = {item.get("claim_uuid"): item for item in reverse.get("results", [])}
    objections_by_claim = _group_by(objections.get("objections", []), "claim_uuid")
    targets_by_claim = {item.get("claim_uuid"): item for item in targets.get("targets", [])}

    claim_arch = []
    for claim in claim_items:
        claim_uuid = claim.get("claim_uuid")
        claim_arch.append(
            {
                "claim_uuid": claim_uuid,
                "surface_claim": claim.get("claim_text"),
                "section": claim.get("section_heading") or "Untitled",
                "buried_claim": "Requires the section's domain assumptions to hold.",
                "operational_claim": "Must survive evidence, boundary, and kill-condition checks.",
                "rhetorical_load": "audit_required",
                "domain_shift": typing_by_claim.get(claim_uuid, {}).get("domain_badges", []),
            }
        )

    evidence_chain = [
        {
            "claim_uuid": claim.get("claim_uuid"),
            "evidence_rows": evidence_by_claim.get(claim.get("claim_uuid"), []),
            "gap": "No evidence row detected." if not evidence_by_claim.get(claim.get("claim_uuid")) else "Bridge still requires reviewer confirmation.",
            "counterevidence_present": "partial" if objections_by_claim.get(claim.get("claim_uuid")) else "no",
        }
        for claim in claim_items
    ]

    kill_arch = [
        {
            "claim_uuid": claim.get("claim_uuid"),
            "implicit_kill": reverse_by_claim.get(claim.get("claim_uuid"), {}).get("what_breaks_it", "No reverse 7Q result."),
            "reviewer_objections": objections_by_claim.get(claim.get("claim_uuid"), []),
            "testable_kill": "partial" if reverse_by_claim.get(claim.get("claim_uuid")) else "no",
        }
        for claim in claim_items
    ]

    eq_sem = [
        {
            "claim_uuid": item.get("claim_uuid"),
            "equation_semantics_needed": bool(item.get("equation_semantics_needed")),
            "status": "REQUIRES_EQ_SEM_REVIEW" if item.get("equation_semantics_needed") else "not_applicable",
            "formal_target": targets_by_claim.get(item.get("claim_uuid"), {}).get("primary_target", "not_routed"),
        }
        for item in typing_items
    ]

    domain_boundary = [
        {
            "claim_uuid": item.get("claim_uuid"),
            "domain_badges": item.get("domain_badges", []),
            "public_comm_risk": item.get("public_comm_risk"),
            "bridge_quality": "needs_boundary_note" if len(item.get("domain_badges", [])) > 1 else "single_domain",
        }
        for item in typing_items
    ]

    reviewer_seeds = [
        {
            "voice": voice,
            "attack": "Inspect unresolved objections, weak evidence bridges, and overstatement flags.",
            "source": "09_objections.json",
        }
        for voice in ["skeptical_physicist", "academic_philosopher", "information_theorist", "methodologist", "hostile_critic"]
    ]

    tracks = score.get("tracks", {})
    ledger_schema = [
        {
            "track": track_name,
            "positive_score_events": track.get("positive_score_events", []),
            "deductions": track.get("deductions", []),
            "readiness": track.get("readiness"),
        }
        for track_name, track in tracks.items()
    ]

    overstate_pattern = [
        {
            "claim_uuid": item.get("claim_uuid"),
            "overstatement_flags": item.get("overstatement_flags", []),
            "safer_alternative": "Scope absolute language to evidence and test conditions.",
        }
        for item in typing_items
        if item.get("overstatement_flags")
    ]

    benchmark_anchor = [
        {
            "track": track_name,
            "score": track.get("score"),
            "meaning": "Audit readiness marker for this track only; not a truth score.",
            "readiness": track.get("readiness"),
        }
        for track_name, track in tracks.items()
    ]

    cross_dep = [
        {
            "claim_uuid": item.get("claim_uuid"),
            "depends_on": item.get("likely_lean_dependencies", []),
            "enables": [item.get("primary_target")],
            "orphan_risk": "bridge_only" if item.get("primary_target") == "Bridge-only / not formal yet" else "tracked",
        }
        for item in targets.get("targets", [])
    ]

    components = {
        "CLAIM_ARCH": _component("CLAIM_ARCH", claim_arch),
        "EVIDENCE_CHAIN": _component("EVIDENCE_CHAIN", evidence_chain),
        "KILL_ARCH": _component("KILL_ARCH", kill_arch),
        "EQ_SEM": _component("EQ_SEM", eq_sem),
        "DOMAIN_BOUNDARY": _component("DOMAIN_BOUNDARY", domain_boundary),
        "REVIEWER_SEEDS": _component("REVIEWER_SEEDS", reviewer_seeds),
        "LEDGER_SCHEMA": _component("LEDGER_SCHEMA", ledger_schema),
        "OVERSTATE_PATTERN": _component("OVERSTATE_PATTERN", overstate_pattern),
        "BENCHMARK_ANCHOR": _component("BENCHMARK_ANCHOR", benchmark_anchor),
        "CROSS_DEP": _component("CROSS_DEP", cross_dep),
        "EIGHT_GAPS": _component("EIGHT_GAPS", [{"gap": gap} for gap in EIGHT_GAPS]),
    }

    return {
        "paper_uuid": paper_uuid,
        "station": "11_report_export",
        "timestamp": utc_now(),
        "title": intake.get("title"),
        "snapshot_order": SNAPSHOT_ORDER,
        "contract": "PDS-1 is a defensibility audit, not a truth score.",
        "components": components,
        "score_tracks": tracks,
    }


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines: list[str] = []
    for component_name in SNAPSHOT_ORDER:
        component = payload["components"][component_name]
        lines += [component_name, ""]
        if component_name == "LEDGER_SCHEMA":
            for track in component["findings"]:
                lines += [f"## {track['track']}", f"- Readiness: {track.get('readiness')}", ""]
                for event in track.get("positive_score_events", []):
                    lines.append(f"- Positive: {event.get('reason')} Fix: {event.get('fix_to_improve')}")
                for event in track.get("deductions", []):
                    lines.append(f"- Deduction: {event.get('reason')} Fix: {event.get('fix_to_improve')}")
                lines.append("")
        else:
            for item in component["findings"]:
                label = item.get("claim_uuid") or item.get("track") or item.get("voice") or item.get("gap") or "item"
                lines.append(f"- {label}: {item}")
            lines.append("")
    if not lines or lines[-1] != "EIGHT_GAPS":
        lines.append("EIGHT_GAPS")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def render_template(payload: dict[str, Any]) -> str:
    template_path = ROOT / "templates" / "pds1_audit_overlay.html"
    template = template_path.read_text(encoding="utf-8")
    track_rows = []
    for track_name, track in payload.get("score_tracks", {}).items():
        track_rows.append(
            "<tr>"
            f"<th>{html.escape(track_name)}</th>"
            f"<td>{html.escape(str(track.get('score', '')))}</td>"
            f"<td>{html.escape(str(track.get('readiness', '')))}</td>"
            f"<td>{len(track.get('deductions', []))}</td>"
            "</tr>"
        )
    sections = []
    for component_name in SNAPSHOT_ORDER:
        component = payload["components"][component_name]
        body = html.escape(str(component["findings"]))
        sections.append(f"<section><h2>{component_name}</h2><pre>{body}</pre></section>")
    return (
        template.replace("{{TITLE}}", html.escape(payload.get("title") or "Untitled PDS-1 Audit"))
        .replace("{{PAPER_UUID}}", html.escape(payload["paper_uuid"]))
        .replace("{{TRACK_ROWS}}", "\n".join(track_rows))
        .replace("{{SECTIONS}}", "\n".join(sections))
    )


def write_csv(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["component", "item_count"])
        writer.writeheader()
        for component_name in SNAPSHOT_ORDER:
            writer.writerow({"component": component_name, "item_count": len(payload["components"][component_name]["findings"])})


def run(paper_uuid: str) -> dict[str, Any]:
    output_dir = paper_output_dir(paper_uuid)
    payload = build_snapshot(output_dir, paper_uuid)
    write_json(output_dir / "11_paper_grade.json", payload)
    write_markdown(output_dir / "11_paper_grade.md", payload)
    (output_dir / "11_paper_grade.html").write_text(render_template(payload), encoding="utf-8")
    write_csv(output_dir / "11_paper_grade.csv", payload)
    return payload
