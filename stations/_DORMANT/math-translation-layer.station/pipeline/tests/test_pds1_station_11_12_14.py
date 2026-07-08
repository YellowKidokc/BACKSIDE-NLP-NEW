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
    station_11_report_export,
    station_12_vector_index,
    station_13_manifest,
    station_14_comms_handoff,
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


def run_through_partner_d_inputs():
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
    station_08_formal_routing.run(intake.paper_uuid)
    station_09_objections.run(intake.paper_uuid)
    station_10_score_readiness.run(intake.paper_uuid)
    return intake


def test_station_11_writes_final_report_files_and_preserves_order():
    intake = run_through_partner_d_inputs()
    try:
        payload = station_11_report_export.run(intake.paper_uuid)
        output_dir = OUTPUT_ROOT / intake.paper_uuid
        assert payload["snapshot_order"][0] == "CLAIM_ARCH"
        assert payload["snapshot_order"][-1] == "EIGHT_GAPS"
        for filename in ["11_paper_grade.json", "11_paper_grade.md", "11_paper_grade.html", "11_paper_grade.csv"]:
            assert (output_dir / filename).exists()
        assert (output_dir / "11_paper_grade.md").read_text(encoding="utf-8").strip().startswith("CLAIM_ARCH")
        assert (output_dir / "11_paper_grade.md").read_text(encoding="utf-8").strip().endswith("EIGHT_GAPS")
    finally:
        cleanup(intake.paper_uuid)


def test_station_11_html_starts_with_claim_arch_and_ends_with_eight_gaps():
    intake = run_through_partner_d_inputs()
    try:
        station_11_report_export.run(intake.paper_uuid)
        html = (OUTPUT_ROOT / intake.paper_uuid / "11_paper_grade.html").read_text(encoding="utf-8").strip()
        assert html.startswith("CLAIM_ARCH")
        assert html.endswith("EIGHT_GAPS")
        assert "Academic_Readiness" in html
        assert "Risk" in html
    finally:
        cleanup(intake.paper_uuid)


def test_station_12_writes_one_jsonl_row_per_snapshot_component():
    intake = run_through_partner_d_inputs()
    try:
        station_11_report_export.run(intake.paper_uuid)
        rows = station_12_vector_index.run(intake.paper_uuid)
        output_dir = OUTPUT_ROOT / intake.paper_uuid
        assert (output_dir / "12_vector_summary.jsonl").exists()
        assert len(rows) == 11
        assert [row["component"] for row in rows][0] == "CLAIM_ARCH"
        assert rows[0]["metadata"]["external_embedding_api_called"] is False
    finally:
        cleanup(intake.paper_uuid)


def test_station_14_writes_run_summary_and_comms_post():
    intake = run_through_partner_d_inputs()
    try:
        station_11_report_export.run(intake.paper_uuid)
        station_12_vector_index.run(intake.paper_uuid)
        station_13_manifest.run(intake.paper_uuid)
        summary = station_14_comms_handoff.run(intake.paper_uuid)
        output_dir = OUTPUT_ROOT / intake.paper_uuid
        assert (output_dir / "14_run_summary.md").exists()
        assert (output_dir / "14_comms_ready_post.md").exists()
        assert "11_report_export" in summary["stations_completed"]
        assert "12_vector_index" in summary["stations_completed"]
        assert "PDS-1 Partner D handoff" in (output_dir / "14_comms_ready_post.md").read_text(encoding="utf-8")
    finally:
        cleanup(intake.paper_uuid)
