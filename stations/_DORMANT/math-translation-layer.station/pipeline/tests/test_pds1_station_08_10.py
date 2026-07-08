import json
import shutil
from pathlib import Path

from pipeline.stations import (
    station_00_intake,
    station_03_claims,
    station_05_evidence,
    station_06_7q_forward,
    station_07_7q_reverse,
    station_08_formal_routing,
    station_09_objections,
    station_10_score_readiness,
)
from pipeline.stations.common import OUTPUT_ROOT, write_json


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "pipeline" / "tests" / "fixtures" / "sample-paper.html"


def cleanup(paper_uuid: str) -> None:
    shutil.rmtree(OUTPUT_ROOT / paper_uuid, ignore_errors=True)


def infer_typing(claim: dict) -> dict:
    text = claim["claim_text"]
    lower = text.lower()
    badges = []
    if any(term in lower for term in ["equation", "phase", "signal", "capacity", "symmetry"]):
        badges.append("PHYSICS")
    if any(term in lower for term in ["grace", "theological", "christianity"]):
        badges.append("THEOLOGY")
    if any(term in lower for term in ["bridge", "maps", "across domains", "analogy"]):
        badges.append("ANALOGY")
    if not badges:
        badges.append("FORMAL")
    return {
        "claim_uuid": claim["claim_uuid"],
        "claim_type": "bridge" if "ANALOGY" in badges else "formal",
        "domain_badges": badges,
        "overstatement_flags": [word for word in ["proves", "cannot", "only"] if word in lower],
        "equation_semantics_needed": any(term in lower for term in ["equation", "phase", "signal", "capacity"]),
        "evidence_requirement": "high" if any(term in lower for term in ["predicts", "proves", "cannot"]) else "medium",
        "public_comm_risk": "high" if "proves" in lower else "medium",
        "recommended_next_station": "08",
    }


def run_through_partner_c_inputs():
    intake = station_00_intake.run(FIXTURE)
    station_03_claims.run(intake.paper_uuid)
    output_dir = OUTPUT_ROOT / intake.paper_uuid
    claims = json.loads((output_dir / "03_claims.json").read_text(encoding="utf-8"))["claims"]
    write_json(
        output_dir / "04_claim_typing.json",
        {
            "paper_uuid": intake.paper_uuid,
            "claim_typing": [infer_typing(claim) for claim in claims],
        },
    )
    station_05_evidence.run(intake.paper_uuid)
    station_06_7q_forward.run(intake.paper_uuid)
    station_07_7q_reverse.run(intake.paper_uuid)
    return intake


def test_station_08_produces_target_map():
    intake = run_through_partner_c_inputs()
    try:
        payload = station_08_formal_routing.run(intake.paper_uuid)
        assert payload["targets"]
        assert (OUTPUT_ROOT / intake.paper_uuid / "08_formal_targets.json").exists()
        assert (OUTPUT_ROOT / intake.paper_uuid / "08_formal_targets_human.md").exists()
        assert {item["primary_target"] for item in payload["targets"]} <= {
            "Lean",
            "Python/state-model",
            "Alloy/TLA-style spec",
            "Bridge-only / not formal yet",
        }
    finally:
        cleanup(intake.paper_uuid)


def test_station_08_routes_master_equation_as_bridge_not_law_equation():
    intake = run_through_partner_c_inputs()
    try:
        payload = station_08_formal_routing.run(intake.paper_uuid)
        guarded = [item for item in payload["targets"] if item["master_equation_guardrail"]]
        assert guarded
        assert all(item["primary_target"] == "Bridge-only / not formal yet" for item in guarded)
    finally:
        cleanup(intake.paper_uuid)


def test_station_08_adds_lean_dependency_hints():
    intake = run_through_partner_c_inputs()
    try:
        output_dir = OUTPUT_ROOT / intake.paper_uuid
        claims_payload = json.loads((output_dir / "03_claims.json").read_text(encoding="utf-8"))
        claim = claims_payload["claims"][0]
        claim["claim_text"] = "The canonical law order preserves no-drift topology and Law 9 terminal asymmetry."
        write_json(output_dir / "03_claims.json", claims_payload)
        payload = station_08_formal_routing.run(intake.paper_uuid)
        hinted = [item for item in payload["targets"] if item["claim_uuid"] == claim["claim_uuid"]][0]
        assert "canonical law order" in hinted["likely_lean_dependencies"]
        assert "no-drift topology" in hinted["likely_lean_dependencies"]
    finally:
        cleanup(intake.paper_uuid)


def test_station_10_has_exactly_four_tracks_with_events_reasons_and_fixes():
    intake = run_through_partner_c_inputs()
    try:
        station_08_formal_routing.run(intake.paper_uuid)
        station_09_objections.run(intake.paper_uuid)
        payload = station_10_score_readiness.run(intake.paper_uuid)
        assert list(payload["tracks"]) == [
            "Academic_Readiness",
            "Framework_Coherence",
            "Public_Communication",
            "Risk",
        ]
        assert "truth" not in payload
        for track in payload["tracks"].values():
            assert track["positive_score_events"]
            assert "deductions" in track
            for event in track["positive_score_events"] + track["deductions"]:
                assert event["reason"]
                assert event["source_reference"]
                assert event["fix_to_improve"]
    finally:
        cleanup(intake.paper_uuid)


def test_station_10_writes_json_and_human_ledger():
    intake = run_through_partner_c_inputs()
    try:
        station_08_formal_routing.run(intake.paper_uuid)
        station_09_objections.run(intake.paper_uuid)
        station_10_score_readiness.run(intake.paper_uuid)
        output_dir = OUTPUT_ROOT / intake.paper_uuid
        assert (output_dir / "10_score_ledger.json").exists()
        assert (output_dir / "10_score_ledger_human.md").exists()
    finally:
        cleanup(intake.paper_uuid)
