from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTBOX = ROOT / "01_OUTBOX_REPORTS"
FINAL = ROOT / "03_FINAL_READY"
SURFACE_SCRIPT = ROOT / "scripts" / "paper_grade_surface.py"
SURFACE_TEMPLATE = ROOT / "paper-grade-dashboard-template.html"


def paper_id_from_report(path: Path) -> str:
    return path.name.replace(".paper-grade.json", "")


def series_for(paper_id: str) -> str:
    lower = paper_id.lower()
    if lower.startswith("gtq-"):
        return "Genesis-to-Quantum"
    if lower.startswith("pa-") or lower in {"index", "pa-00-bundle-viewer"}:
        return "Proof-Architecture"
    if "cannon" in lower or "theophysics" in lower:
        return "Cannon"
    if "smoke_test" in lower:
        return "Smoke-Tests"
    return "Unsorted"


def render_one(source_json: Path) -> dict[str, str]:
    paper_id = paper_id_from_report(source_json)
    paper_root = FINAL / series_for(paper_id) / paper_id
    html_dir = paper_root / "HTML"
    excel_dir = paper_root / "EXCEL"
    html_dir.mkdir(parents=True, exist_ok=True)
    excel_dir.mkdir(parents=True, exist_ok=True)
    out_html = html_dir / f"{paper_id}.paper-grade-dashboard.html"
    out_xlsx = excel_dir / f"{paper_id}.paper-grade.review.xlsx"
    freshness_inputs = [source_json, SURFACE_SCRIPT]
    if SURFACE_TEMPLATE.exists():
        freshness_inputs.append(SURFACE_TEMPLATE)
    newest_input = max(path.stat().st_mtime for path in freshness_inputs)
    if (
        out_html.exists()
        and out_xlsx.exists()
        and out_html.stat().st_mtime >= newest_input
        and out_xlsx.stat().st_mtime >= source_json.stat().st_mtime
    ):
        return {
            "paper_id": paper_id,
            "source_json": str(source_json),
            "dashboard_html": str(out_html),
            "review_xlsx": str(out_xlsx),
            "status": "up-to-date",
        }
    cmd = [
        sys.executable,
        str(SURFACE_SCRIPT),
        str(source_json),
        "--snapshot-root",
        str(FINAL),
        "--out-html",
        str(out_html),
        "--out-xlsx",
        str(out_xlsx),
    ]
    subprocess.run(cmd, check=True, text=True)
    return {
        "paper_id": paper_id,
        "source_json": str(source_json),
        "dashboard_html": str(out_html),
        "review_xlsx": str(out_xlsx if out_xlsx.exists() else ""),
        "status": "rendered",
    }


def main() -> int:
    rows = [render_one(path) for path in sorted(OUTBOX.glob("*.paper-grade.json"))]
    print(json.dumps({"ok": True, "count": len(rows), "rows": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
