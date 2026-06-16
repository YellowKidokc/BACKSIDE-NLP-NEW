from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


EXPORT_ROOT = Path(r"\\dlowenas\brain\EXPORTS\Treaties\LATEST")
HTML_ROOT = EXPORT_ROOT / "HTML"
MARKDOWN_ROOT = EXPORT_ROOT / "MARKDOWN"
MANIFESTS = EXPORT_ROOT / "MANIFESTS"
AXIOMS_INBOX = Path(r"\\dlowenas\brain\Backside\workflows\axioms.workflow\00_INBOX_DROP_PAPERS_HERE")


def clean_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._ -]+", "-", value).strip(" .-_")
    value = re.sub(r"\s+", "-", value)
    return value or "untitled"


def relative_markdown_path(html_path: Path) -> Path:
    rel = html_path.relative_to(HTML_ROOT)
    return rel.with_suffix(".md")


def convert_one(html_path: Path, md_path: Path) -> None:
    md_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "markitdown", str(html_path), "-o", str(md_path)]
    subprocess.run(cmd, check=True, text=True)


def main() -> int:
    if not HTML_ROOT.exists():
        raise SystemExit(f"HTML root not found: {HTML_ROOT}")
    MARKDOWN_ROOT.mkdir(parents=True, exist_ok=True)
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    AXIOMS_INBOX.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    for html_path in sorted(HTML_ROOT.rglob("*.html"), key=lambda p: str(p).lower()):
        md_path = MARKDOWN_ROOT / relative_markdown_path(html_path)
        convert_one(html_path, md_path)

        inbox_name = clean_name("-".join(md_path.relative_to(MARKDOWN_ROOT).with_suffix("").parts)) + ".md"
        inbox_path = AXIOMS_INBOX / inbox_name
        inbox_path.write_text(md_path.read_text(encoding="utf-8"), encoding="utf-8")

        rows.append(
            {
                "source_html": str(html_path),
                "markdown": str(md_path),
                "axioms_inbox": str(inbox_path),
                "bytes": str(md_path.stat().st_size),
            }
        )

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "html_root": str(HTML_ROOT),
        "markdown_root": str(MARKDOWN_ROOT),
        "axioms_inbox": str(AXIOMS_INBOX),
        "converted_count": len(rows),
    }
    payload = {"summary": summary, "records": rows}
    manifest_json = MANIFESTS / f"markitdown-to-axioms-{stamp}.json"
    manifest_csv = MANIFESTS / f"markitdown-to-axioms-{stamp}.csv"
    manifest_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    with manifest_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source_html", "markdown", "axioms_inbox", "bytes"])
        writer.writeheader()
        writer.writerows(rows)
    (EXPORT_ROOT / "MARKDOWN_MANIFEST.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(json.dumps({"ok": True, **summary, "manifest": str(manifest_json)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
