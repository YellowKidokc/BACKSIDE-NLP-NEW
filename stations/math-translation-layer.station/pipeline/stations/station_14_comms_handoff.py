from __future__ import annotations

from pathlib import Path
from typing import Any

from pipeline.stations.common import paper_output_dir, read_json, utc_now


EXPECTED_FILES = [
    "11_paper_grade.json",
    "11_paper_grade.md",
    "11_paper_grade.html",
    "12_vector_summary.jsonl",
    "13_manifest.json",
]


def _load_optional(output_dir: Path, filename: str) -> dict[str, Any]:
    path = output_dir / filename
    return read_json(path) if path.exists() else {}


def _produced_files(output_dir: Path) -> list[str]:
    return sorted(str(path.relative_to(output_dir)) for path in output_dir.rglob("*") if path.is_file())


def build_summary(paper_uuid: str) -> dict[str, Any]:
    output_dir = paper_output_dir(paper_uuid)
    manifest = _load_optional(output_dir, "13_manifest.json")
    report = _load_optional(output_dir, "11_paper_grade.json")
    produced = _produced_files(output_dir)
    warnings = [f"Missing expected output: {filename}" for filename in EXPECTED_FILES if not (output_dir / filename).exists()]
    if report and report.get("contract") != "PDS-1 is a defensibility audit, not a truth score.":
        warnings.append("PDS-1 contract text drifted from defensibility-audit wording.")
    return {
        "paper_uuid": paper_uuid,
        "timestamp": utc_now(),
        "stations_completed": manifest.get("stations_completed", []),
        "files_produced": produced,
        "warnings": warnings,
        "next_action": "Integrator should run the full 00-14 verification after Partner A/B/C files are present, then copy reviewed Markdown to Canon and heavy data to the Canon data mirror.",
    }


def write_run_summary(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# PDS-1 Run Summary",
        "",
        f"- Paper UUID: {summary['paper_uuid']}",
        f"- Timestamp: {summary['timestamp']}",
        f"- Stations completed: {', '.join(summary['stations_completed']) or 'manifest unavailable'}",
        "",
        "## Files Produced",
        "",
    ]
    lines += [f"- `{filename}`" for filename in summary["files_produced"]]
    lines += ["", "## Warnings", ""]
    lines += [f"- {warning}" for warning in summary["warnings"]] or ["- None."]
    lines += ["", "## Next Action", "", summary["next_action"], ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_comms_post(path: Path, summary: dict[str, Any]) -> None:
    warnings = "; ".join(summary["warnings"]) if summary["warnings"] else "none"
    body = (
        "[codex-ledger]\n"
        f"PDS-1 Partner D handoff for paper {summary['paper_uuid']}.\n"
        f"Stations completed per manifest: {', '.join(summary['stations_completed']) or 'manifest unavailable'}.\n"
        "Produced Partner D outputs: 11_paper_grade.json/md/html/csv, 12_vector_summary.jsonl, 14_run_summary.md, 14_comms_ready_post.md.\n"
        f"Warnings: {warnings}.\n"
        f"Next: {summary['next_action']}\n"
    )
    path.write_text(body, encoding="utf-8")


def run(paper_uuid: str) -> dict[str, Any]:
    output_dir = paper_output_dir(paper_uuid)
    summary = build_summary(paper_uuid)
    write_run_summary(output_dir / "14_run_summary.md", summary)
    write_comms_post(output_dir / "14_comms_ready_post.md", summary)
    return summary
