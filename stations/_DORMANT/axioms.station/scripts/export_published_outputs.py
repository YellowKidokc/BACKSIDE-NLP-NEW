from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "03_FINAL_READY"
EXPORT_ROOT = Path(r"\\dlowenas\brain\EXPORTS\axioms.workflow")
LATEST = EXPORT_ROOT / "LATEST"
MANIFESTS = EXPORT_ROOT / "MANIFESTS"


def assert_export_target(path: Path) -> None:
    root = EXPORT_ROOT.resolve()
    target = path.resolve()
    if root != target and root not in target.parents:
        raise RuntimeError(f"Refusing to write outside export root: {target}")


def series_and_paper(path: Path) -> tuple[str, str]:
    rel = path.relative_to(FINAL)
    parts = rel.parts
    if len(parts) >= 4 and parts[2] in {"HTML", "EXCEL"}:
        return parts[0], parts[1]
    return "Unsorted", path.stem


def published_files() -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    for path in FINAL.rglob("*.html"):
        if "\\HTML\\" not in str(path) and "/HTML/" not in str(path):
            continue
        if "smoke" in path.name.lower():
            continue
        files.append(("HTML", path))
    for path in FINAL.rglob("*.paper-grade.review.xlsx"):
        if "\\EXCEL\\" not in str(path) and "/EXCEL/" not in str(path):
            continue
        files.append(("EXCEL", path))
    return sorted(files, key=lambda item: (item[0], str(item[1]).lower()))


def reset_lane(lane: str) -> None:
    target = LATEST / lane
    assert_export_target(target)
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)


def main() -> int:
    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
    LATEST.mkdir(parents=True, exist_ok=True)
    MANIFESTS.mkdir(parents=True, exist_ok=True)

    for lane in ("HTML", "EXCEL"):
        reset_lane(lane)

    rows: list[dict[str, str]] = []
    for lane, source in published_files():
        series, paper = series_and_paper(source)
        destination = LATEST / lane / series / paper / source.name
        assert_export_target(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        rows.append(
            {
                "lane": lane,
                "series": series,
                "paper": paper,
                "source": str(source),
                "destination": str(destination),
                "bytes": str(destination.stat().st_size),
            }
        )

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_root": str(FINAL),
        "export_root": str(LATEST),
        "html_count": sum(1 for row in rows if row["lane"] == "HTML"),
        "excel_count": sum(1 for row in rows if row["lane"] == "EXCEL"),
        "total_count": len(rows),
    }
    payload = {"summary": summary, "records": rows}

    manifest_json = MANIFESTS / f"published-outputs-{stamp}.json"
    manifest_csv = MANIFESTS / f"published-outputs-{stamp}.csv"
    latest_json = LATEST / "EXPORT_MANIFEST.json"
    latest_csv = LATEST / "EXPORT_MANIFEST.csv"
    readme = LATEST / "README.md"

    manifest_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    with manifest_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["lane", "series", "paper", "source", "destination", "bytes"])
        writer.writeheader()
        writer.writerows(rows)
    shutil.copy2(manifest_csv, latest_csv)

    readme.write_text(
        "\n".join(
            [
                "# Axioms Published Export Shelf",
                "",
                "This folder is the root-visible take-away shelf for published Axioms workflow outputs.",
                "",
                f"- Generated: `{summary['generated_at']}`",
                f"- Source: `{summary['source_root']}`",
                f"- HTML files: `{summary['html_count']}`",
                f"- Final review Excel files: `{summary['excel_count']}`",
                "",
                "Folders:",
                "",
                "- `HTML/` - published browser-ready HTML outputs, preserving series and paper folders.",
                "- `EXCEL/` - final `*.paper-grade.review.xlsx` workbooks, preserving series and paper folders.",
                "- `EXPORT_MANIFEST.json/csv` - exact source-to-export map.",
                "",
                "This shelf is safe to copy into the Z/Obsidian framework staging area.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps({"ok": True, **summary, "manifest": str(latest_json)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
