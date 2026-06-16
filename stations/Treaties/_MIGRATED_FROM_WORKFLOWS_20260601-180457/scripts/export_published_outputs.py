from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOTS = ROOT / "snapshots"
EXPORT_ROOT = Path(r"\\dlowenas\brain\EXPORTS\Treaties")
LATEST = EXPORT_ROOT / "LATEST"
MANIFESTS = EXPORT_ROOT / "MANIFESTS"


def assert_export_target(path: Path) -> None:
    root = EXPORT_ROOT.resolve()
    target = path.resolve()
    if root != target and root not in target.parents:
        raise RuntimeError(f"Refusing to write outside export root: {target}")


def published_html_files() -> list[Path]:
    files = list(SNAPSHOTS.glob("*.html")) if SNAPSHOTS.exists() else []
    proof_explorer = ROOT / "proof-explorer-fp-005-enhanced.html"
    if proof_explorer.exists():
        files.append(proof_explorer)
    return sorted({path.resolve(): path for path in files}.values(), key=lambda path: path.name.lower())


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
    reset_lane("HTML")
    reset_lane("EXCEL")

    rows: list[dict[str, str]] = []
    for source in published_html_files():
        bucket = "proof-explorer" if source.parent == ROOT else "snapshots"
        destination = LATEST / "HTML" / bucket / source.name
        assert_export_target(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        rows.append(
            {
                "lane": "HTML",
                "bucket": bucket,
                "source": str(source),
                "destination": str(destination),
                "bytes": str(destination.stat().st_size),
            }
        )

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_root": str(ROOT),
        "export_root": str(LATEST),
        "html_count": len(rows),
        "excel_count": 0,
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
        writer = csv.DictWriter(f, fieldnames=["lane", "bucket", "source", "destination", "bytes"])
        writer.writeheader()
        writer.writerows(rows)
    shutil.copy2(manifest_csv, latest_csv)

    readme.write_text(
        "\n".join(
            [
                "# Treaties Published Export Shelf",
                "",
                "This folder is the root-visible take-away shelf for Treaties snapshot outputs.",
                "",
                f"- Generated: `{summary['generated_at']}`",
                f"- Source: `{summary['source_root']}`",
                f"- HTML files: `{summary['html_count']}`",
                f"- Final Excel files: `{summary['excel_count']}`",
                "",
                "Folders:",
                "",
                "- `HTML/snapshots/` - standalone paper snapshot HTML exports.",
                "- `HTML/proof-explorer/` - proof-explorer style reference HTML.",
                "- `EXCEL/` - reserved for a future Treaties workbook surface.",
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
