from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_EXPORT_ROOT = Path(r"X:\EXPORTS\chi-tagging")
DEFAULT_STATE_ROOT = Path(r"X:\Backside\_state\chi-tagging")
STATIONS = [
    "master-equation-canon",
    "trinity-canon",
    "fruits-spirit-canon",
    "operators-canon",
]


def run_id() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def run_station(station_id: str, out_dir: Path) -> dict:
    station_py = REPO_ROOT / "Backside" / "stations" / f"{station_id}.station" / "station.py"
    if not station_py.exists():
        raise FileNotFoundError(station_py)
    out_dir.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [sys.executable, str(station_py), "--out", str(out_dir)],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return {
            "station": station_id,
            "status": "FAILED",
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    index_path = out_dir / "canon-index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    return {
        "station": station_id,
        "status": "PASS",
        "out_dir": str(out_dir),
        "summary": index.get("summary", {}),
        "stdout": completed.stdout,
    }


def aggregate(station_dirs: list[Path], export_dir: Path) -> dict:
    merged_blocks: list[dict] = []
    merged_equations: list[dict] = []
    var_counts = {var: 0 for var in "GMESTKRQFC"}
    sources: list[dict] = []

    for station_dir in station_dirs:
        index_path = station_dir / "canon-index.json"
        if not index_path.exists():
            continue
        index = json.loads(index_path.read_text(encoding="utf-8"))
        station_id = index.get("station_id", station_dir.name)
        for source in index.get("sources", []):
            source["station_id"] = station_id
            sources.append(source)
        for block in index.get("blocks", []):
            block["station_id"] = station_id
            merged_blocks.append(block)
        for equation in index.get("equations", []):
            equation["station_id"] = station_id
            merged_equations.append(equation)
        for var, count in index.get("summary", {}).get("var_counts", {}).items():
            var_counts[var] = var_counts.get(var, 0) + count

    combined = {
        "schema": "theophysics.chi_tagging.canon_aggregate.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "stations": [path.name for path in station_dirs],
        "summary": {
            "sources": len(sources),
            "tagged_blocks": len(merged_blocks),
            "equations": len(merged_equations),
            "var_counts": var_counts,
            "needs_review_blocks": sum(
                1
                for block in merged_blocks
                for detection in block.get("detections", [])
                if detection.get("status") == "NEEDS_REVIEW"
            ),
        },
        "sources": sources,
        "blocks": merged_blocks,
        "equations": merged_equations,
    }
    (export_dir / "canon-index.aggregate.json").write_text(json.dumps(combined, indent=2), encoding="utf-8")
    render_aggregate_markdown(combined, export_dir / "canon-index.aggregate.md")
    return combined


def render_aggregate_markdown(combined: dict, path: Path) -> None:
    lines = [
        "# Chi Tagging Canon Aggregate",
        "",
        f"- Generated: {combined['generated_at']}",
        f"- Sources: {combined['summary']['sources']}",
        f"- Tagged blocks: {combined['summary']['tagged_blocks']}",
        f"- Equations: {combined['summary']['equations']}",
        f"- Needs review blocks: {combined['summary']['needs_review_blocks']}",
        "",
        "## Variable Counts",
        "",
    ]
    for var, count in combined["summary"]["var_counts"].items():
        lines.append(f"- {var}: {count}")
    lines.extend(
        [
            "",
            "## Next Database Targets",
            "",
            "1. `public.cross_domain.chi_vars text[]`",
            "2. `framework_topology.canonical_axioms.chi_vars text[]`",
            "3. `framework_math.equation_terms` links for remaining equations",
            "",
            "Use block-level evidence as the tagging basis. Aggregate to row/document level only after evidence spans are preserved.",
        ]
    )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_readme(export_dir: Path, state_dir: Path, results: list[dict], combined: dict) -> None:
    lines = [
        "# Chi Tagging Workflow Export",
        "",
        f"- Export: `{export_dir}`",
        f"- State: `{state_dir}`",
        f"- Tagged blocks: {combined['summary']['tagged_blocks']}",
        f"- Equations: {combined['summary']['equations']}",
        "",
        "## Station Results",
        "",
    ]
    for result in results:
        lines.append(f"- {result['station']}: {result['status']}")
    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `canon-index.aggregate.json`",
            "- `canon-index.aggregate.md`",
            "- `stations/<station-id>/canon-index.json`",
            "- `stations/<station-id>/canon-index.md`",
        ]
    )
    (export_dir / "README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run canon stations and aggregate chi-variable index.")
    parser.add_argument("--export-root", type=Path, default=DEFAULT_EXPORT_ROOT)
    parser.add_argument("--state-root", type=Path, default=DEFAULT_STATE_ROOT)
    args = parser.parse_args()

    rid = run_id()
    export_dir = args.export_root / rid
    state_dir = args.state_root / rid
    station_root = export_dir / "stations"
    export_dir.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)

    results = [run_station(station, station_root / station) for station in STATIONS]
    failed = [row for row in results if row["status"] != "PASS"]
    (state_dir / "station-results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    if failed:
        print(json.dumps({"failed": failed}, indent=2))
        return 2

    combined = aggregate([station_root / station for station in STATIONS], export_dir)
    (state_dir / "canon-index.aggregate.json").write_text(json.dumps(combined, indent=2), encoding="utf-8")
    write_readme(export_dir, state_dir, results, combined)
    print(f"Export written: {export_dir}")
    print(f"Tagged blocks: {combined['summary']['tagged_blocks']}")
    print(f"Equations: {combined['summary']['equations']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
