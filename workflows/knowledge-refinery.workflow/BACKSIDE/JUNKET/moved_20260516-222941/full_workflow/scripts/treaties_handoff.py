"""
treaties_handoff.py
Build a downstream Treaties/proof-explorer handoff package for one scored paper.

This does not render the final Treaties HTML. It creates the stable bridge artifact
that Treaties can ingest after FAP, paper-proof-grader, axiom mapping, and station
scorecards have run.

Output:
  <batch>/<jobid>/treaties-handoff.json
  X:/knowledge-refinery/06_HTML_REPORTS/treaties-handoff/<jobid>.json
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


FAP_ROOT = Path(r"X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP")
FAP_OUTPUT = FAP_ROOT / "output"
FAP_AXIOM_MAPPED = FAP_ROOT / "axiom-mapped"
PROOF_QUEUE = Path(r"X:\knowledge-refinery\06_HTML_REPORTS\treaties-handoff")


def _read_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _find_axiom_payload(jobid: str) -> Path | None:
    direct = FAP_AXIOM_MAPPED / jobid / "postgres_mapping_payload.json"
    if direct.exists():
        return direct
    if not FAP_AXIOM_MAPPED.exists():
        return None
    matches = sorted(
        FAP_AXIOM_MAPPED.glob(f"*{jobid}*/postgres_mapping_payload.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return matches[0] if matches else None


def build_handoff(jobid: str, batch_dir: Path) -> dict:
    paper_dir = batch_dir / jobid
    scorecard_path = paper_dir / "scorecard.json"
    draft_html_path = paper_dir / "production-draft.html"
    fap_manifest_path = FAP_OUTPUT / jobid / "job_manifest.json"
    axiom_payload_path = _find_axiom_payload(jobid)

    return {
        "schema_version": "treaties.handoff.v1",
        "jobid": jobid,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "role": "downstream-proof-explorer-snapshot-input",
        "pipeline_position": [
            "FAP intake",
            "lossless extraction",
            "paper-proof-grader",
            "axiom mapping",
            "full_workflow station scorecard",
            "Treaties snapshot renderer",
            "proof-explorer HTML",
        ],
        "inputs": {
            "scorecard_json": str(scorecard_path) if scorecard_path.exists() else None,
            "production_draft_html": str(draft_html_path) if draft_html_path.exists() else None,
            "fap_manifest_json": str(fap_manifest_path) if fap_manifest_path.exists() else None,
            "postgres_mapping_payload_json": str(axiom_payload_path) if axiom_payload_path else None,
        },
        "scorecard": _read_json(scorecard_path),
        "fap_manifest": _read_json(fap_manifest_path),
        "axiom_mapping": _read_json(axiom_payload_path) if axiom_payload_path else None,
        "treaties_target": {
            "repo": r"D:\GitHub\Treaties",
            "snapshot_cache": r"D:\GitHub\Treaties\snapshots",
            "public_output": r"X:\knowledge-refinery\06_HTML_REPORTS",
            "proof_explorer_output": r"\\dlowenas\brain\proof-explorer",
        },
    }


def write_handoff(jobid: str, batch_dir: Path) -> tuple[Path, Path]:
    handoff = build_handoff(jobid, batch_dir)
    paper_dir = batch_dir / jobid
    paper_dir.mkdir(parents=True, exist_ok=True)
    local_path = paper_dir / "treaties-handoff.json"
    local_path.write_text(json.dumps(handoff, indent=2, ensure_ascii=False), encoding="utf-8")

    PROOF_QUEUE.mkdir(parents=True, exist_ok=True)
    queue_path = PROOF_QUEUE / f"{jobid}.json"
    queue_path.write_text(json.dumps(handoff, indent=2, ensure_ascii=False), encoding="utf-8")
    return local_path, queue_path
