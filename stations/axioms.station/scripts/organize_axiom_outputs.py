from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUTBOX = ROOT / "01_OUTBOX_REPORTS"
HTML_BOX = ROOT / "02_HTML_OUTPUTS"
FINAL = ROOT / "03_FINAL_READY"
MANIFESTS = ROOT / "05_MANIFESTS"
SURFACE_SCRIPT = ROOT / "scripts" / "paper_grade_surface.py"
SURFACE_TEMPLATE = ROOT / "paper-grade-dashboard-template.html"


def clean_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._ -]+", "-", value).strip(" .-_")
    value = re.sub(r"\s+", "-", value)
    return value or "untitled"


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


def paper_id_from_report(path: Path) -> str:
    name = path.name
    for suffix in (
        ".paper-grade.json",
        ".paper-grade.md",
        ".paper-grade.html",
        ".paper-grade.xlsx",
        ".claim-audit.csv",
    ):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return path.stem


def lane_for(path: Path) -> str:
    if path.name.endswith(".paper-grade.html"):
        return "HTML"
    if path.name.endswith(".paper-grade.json"):
        return "JSON"
    if path.name.endswith(".paper-grade.xlsx"):
        return "EXCEL"
    if path.name.endswith(".claim-audit.csv"):
        return "CLAIMS"
    if path.name.endswith(".paper-grade.md"):
        return "MARKDOWN"
    return "OTHER"


def write_lossless_summary(json_path: Path, summary_path: Path) -> None:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    metrics = data.get("metrics", {})
    claims = data.get("claims", [])
    equations = data.get("equations", [])
    sections = data.get("sections", [])
    lines = [
        f"# Lossless Summary: {data.get('paper_id', json_path.stem)}",
        "",
        "## Source",
        "",
        f"- Source file: `{data.get('source_file', '')}`",
        f"- Generated at: `{data.get('generated_at', '')}`",
        "",
        "## Metrics",
        "",
    ]
    for key, value in metrics.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Sections", ""])
    for section in sections:
        title = section.get("title", "Untitled")
        text = re.sub(r"\s+", " ", section.get("text", "")).strip()
        lines.append(f"### {title}")
        lines.append("")
        lines.append(text[:2000] if text else "(empty)")
        lines.append("")
    lines.extend(["## Equations", ""])
    if equations:
        for equation in equations:
            lines.append(f"- `{equation}`")
    else:
        lines.append("- No equations detected.")
    lines.extend(["", "## Claims", ""])
    if claims:
        for idx, claim in enumerate(claims, 1):
            lines.append(f"### Claim {idx}")
            lines.append("")
            for key in (
                "section",
                "one_sentence_claim",
                "claim_maturity_label",
                "facts_snapshot",
                "forward_test",
                "reverse_test",
                "evidence_bar",
                "kill_conditions",
                "not_claimed",
                "proof_boundary",
                "nearby_equation",
                "Q1_identity",
                "Q2_scope",
                "Q3_mechanism",
                "Q4_evidence",
                "Q5_falsifiability",
                "Q6_boundary",
                "Q7_listener_risk",
            ):
                lines.append(f"- {key}: {claim.get(key, '')}")
            lines.append("")
    else:
        lines.append("- No claim candidates detected.")
    summary_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def render_dashboard_surface(source_json: Path, paper_root: Path, series: str) -> list[dict[str, str]]:
    html_dir = paper_root / "HTML"
    excel_dir = paper_root / "EXCEL"
    html_dir.mkdir(parents=True, exist_ok=True)
    excel_dir.mkdir(parents=True, exist_ok=True)
    paper_id = paper_id_from_report(source_json)
    dashboard_html = html_dir / f"{paper_id}.paper-grade-dashboard.html"
    review_xlsx = excel_dir / f"{paper_id}.paper-grade.review.xlsx"
    freshness_inputs = [source_json, SURFACE_SCRIPT]
    if SURFACE_TEMPLATE.exists():
        freshness_inputs.append(SURFACE_TEMPLATE)
    newest_input = max(path.stat().st_mtime for path in freshness_inputs)
    if (
        dashboard_html.exists()
        and review_xlsx.exists()
        and dashboard_html.stat().st_mtime >= newest_input
        and review_xlsx.stat().st_mtime >= source_json.stat().st_mtime
    ):
        return [
            {
                "lane": f"final/{series}/HTML",
                "source": str(source_json),
                "destination": str(dashboard_html),
                "bytes": str(dashboard_html.stat().st_size),
                "status": "up-to-date",
            },
            {
                "lane": f"final/{series}/EXCEL",
                "source": str(source_json),
                "destination": str(review_xlsx),
                "bytes": str(review_xlsx.stat().st_size),
                "status": "up-to-date",
            },
        ]
    cmd = [
        sys.executable,
        str(SURFACE_SCRIPT),
        str(source_json),
        "--snapshot-root",
        str(FINAL),
        "--out-html",
        str(dashboard_html),
        "--out-xlsx",
        str(review_xlsx),
    ]
    subprocess.run(cmd, check=True, text=True)
    rows = [
        {
            "lane": f"final/{series}/HTML",
            "source": str(source_json),
            "destination": str(dashboard_html),
            "bytes": str(dashboard_html.stat().st_size),
            "status": "rendered",
        }
    ]
    if review_xlsx.exists():
        rows.append(
            {
                "lane": f"final/{series}/EXCEL",
                "source": str(source_json),
                "destination": str(review_xlsx),
                "bytes": str(review_xlsx.stat().st_size),
                "status": "rendered",
            }
        )
    return rows


def main() -> int:
    for path in (OUTBOX, HTML_BOX, FINAL, MANIFESTS):
        path.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rows: list[dict[str, str]] = []

    for src in sorted(OUTBOX.glob("*")):
        if not src.is_file():
            continue

        if src.suffix.lower() == ".html":
            target = HTML_BOX / src.name
            shutil.copy2(src, target)
            rows.append({"lane": "html", "source": str(src), "destination": str(target), "bytes": str(src.stat().st_size)})

        if any(src.name.endswith(suffix) for suffix in (
            ".paper-grade.json",
            ".paper-grade.md",
            ".paper-grade.html",
            ".paper-grade.xlsx",
            ".claim-audit.csv",
        )):
            paper_id = paper_id_from_report(src)
            series = series_for(paper_id)
            lane = lane_for(src)
            paper_root = FINAL / clean_name(series) / clean_name(paper_id)
            target_dir = paper_root / lane
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / src.name
            shutil.copy2(src, target)
            rows.append({"lane": f"final/{series}/{lane}", "source": str(src), "destination": str(target), "bytes": str(src.stat().st_size)})

            if src.name.endswith(".paper-grade.json"):
                summary_dir = paper_root / "LOSSLESS_SUMMARY"
                summary_dir.mkdir(parents=True, exist_ok=True)
                summary_path = summary_dir / f"{paper_id}.lossless-summary.md"
                write_lossless_summary(src, summary_path)
                rows.append({"lane": f"final/{series}/LOSSLESS_SUMMARY", "source": str(src), "destination": str(summary_path), "bytes": str(summary_path.stat().st_size)})
                rows.extend(render_dashboard_surface(src, paper_root, series))

    html_count = len(list(HTML_BOX.glob("*.html")))
    final_count = len([p for p in FINAL.rglob("*") if p.is_file()])
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "root": str(ROOT),
        "html_count": html_count,
        "final_file_count": final_count,
        "copied_records": len(rows),
    }

    (MANIFESTS / f"axioms-output-organizer-{stamp}.json").write_text(
        json.dumps({"summary": summary, "records": rows}, indent=2),
        encoding="utf-8",
    )
    with (MANIFESTS / f"axioms-output-organizer-{stamp}.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["lane", "source", "destination", "bytes", "status"])
        writer.writeheader()
        writer.writerows(rows)

    print("Axioms organizer complete.")
    print(f"HTML reports: {html_count}")
    print(f"Final-ready files: {final_count}")
    print(f"Manifest folder: {MANIFESTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
