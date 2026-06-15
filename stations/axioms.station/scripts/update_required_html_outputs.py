from __future__ import annotations

import csv
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "papers" / "required_html_outputs_2026-05-11"
HTML_BOX = ROOT / "02_HTML_OUTPUTS" / "required_reference_outputs"

SOURCES = [
    Path(r"\\dlowenas\brain\snapshot\html-view\00_GENESIS-TO-QUANTUM-black-axiom-snapshot.html"),
    Path(r"\\dlowenas\brain\proof-explorer\axioms-closure.html"),
    Path(r"\\dlowenas\brain\proof-explorer\axioms-layer-0-core.html"),
    Path(r"\\dlowenas\brain\proof-explorer\axioms-layer-0-core.backup-before-semantic-anchor-20260507.html"),
    Path(r"\\dlowenas\brain\proof-explorer\axioms-layer-2-derived.html"),
    Path(r"\\dlowenas\brain\proof-explorer\axioms-layer-3-extended.html"),
    Path(r"\\dlowenas\brain\proof-explorer\fp-005.html"),
    Path(r"\\dlowenas\brain\proof-explorer\fp-005-enhanced.html"),
    Path(r"\\dlowenas\brain\proof-explorer\index.html"),
    Path(r"\\dlowenas\brain\proof-explorer\index.backup-before-ai-portal-20260507.html"),
    Path(r"\\dlowenas\brain\proof-explorer\paper-snapshot-prototype.html"),
]

FALLBACK_SOURCES = {
    "00_GENESIS-TO-QUANTUM-black-axiom-snapshot.html": [
        Path(r"\\dlowenas\brain\Backside\EXPORTS\proof-explorer\reports\gtq_full_20260507_180345\defensibility_snapshot_python\GTQ-07A.defensibility.snapshot.html"),
        Path(r"\\dlowenas\brain\#recycle\knowledge-refinery.workflow\root-leftovers\snapshot\html-view\00_GENESIS-TO-QUANTUM-black-axiom-snapshot.html"),
    ],
    "axioms-closure.html": [
        Path(r"\\dlowenas\brain\Backside\EXPORTS\proof-explorer\axioms-closure.html"),
        Path(r"\\dlowenas\brain\#recycle\paper-proof-grader.workflow\REFERENCE\axiom_sequence_sources\axioms-closure.html"),
    ],
    "axioms-layer-0-core.html": [
        Path(r"\\dlowenas\brain\Backside\EXPORTS\proof-explorer\axioms-layer-0-core.html"),
        Path(r"\\dlowenas\brain\#recycle\paper-proof-grader.workflow\REFERENCE\axiom_sequence_sources\axioms-layer-0-core.html"),
    ],
    "axioms-layer-0-core.backup-before-semantic-anchor-20260507.html": [
        Path(r"\\dlowenas\brain\Backside\EXPORTS\proof-explorer\axioms-layer-0-core.html"),
        Path(r"\\dlowenas\brain\#recycle\paper-proof-grader.workflow\REFERENCE\axiom_sequence_sources\axioms-layer-0-core.html"),
    ],
    "axioms-layer-2-derived.html": [
        Path(r"\\dlowenas\brain\Backside\EXPORTS\proof-explorer\axioms-layer-2-derived.html"),
        Path(r"\\dlowenas\brain\#recycle\paper-proof-grader.workflow\REFERENCE\axiom_sequence_sources\axioms-layer-2-derived.html"),
    ],
    "axioms-layer-3-extended.html": [
        Path(r"\\dlowenas\brain\Backside\EXPORTS\proof-explorer\axioms-layer-3-extended.html"),
        Path(r"\\dlowenas\brain\#recycle\paper-proof-grader.workflow\REFERENCE\axiom_sequence_sources\axioms-layer-3-extended.html"),
    ],
    "fp-005.html": [
        Path(r"\\dlowenas\brain\Backside\EXPORTS\proof-explorer\fp-005.html"),
        Path(r"\\dlowenas\brain\#recycle\paper-proof-grader.workflow\REFERENCE\axiom_sequence_sources\fp-005.html"),
    ],
    "fp-005-enhanced.html": [
        Path(r"\\dlowenas\brain\Backside\EXPORTS\proof-explorer\fp-005-enhanced.html"),
        Path(r"\\dlowenas\brain\#recycle\paper-proof-grader.workflow\REFERENCE\axiom_sequence_sources\fp-005-enhanced.html"),
    ],
    "index.html": [
        Path(r"\\dlowenas\brain\Backside\EXPORTS\proof-explorer\index.html"),
    ],
    "index.backup-before-ai-portal-20260507.html": [
        Path(r"\\dlowenas\brain\Backside\EXPORTS\proof-explorer\index.html"),
    ],
    "paper-snapshot-prototype.html": [
        Path(r"\\dlowenas\brain\Backside\EXPORTS\proof-explorer\paper-snapshot-prototype.html"),
        Path(r"\\dlowenas\brain\#recycle\paper-proof-grader.workflow\ONLINE_CODEX_PACKAGE\paper-snapshot-prototype.html"),
    ],
}


def resolve_source(src: Path) -> tuple[Path | None, str]:
    if src.exists():
        return src, "primary"
    for fallback in FALLBACK_SOURCES.get(src.name, []):
        if fallback.exists():
            return fallback, "fallback"
    return None, "missing"


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    HTML_BOX.mkdir(parents=True, exist_ok=True)
    rows = []
    for src in SOURCES:
        resolved, status = resolve_source(src)
        bytes_written = ""
        if resolved is not None:
            for folder in (DEST, HTML_BOX):
                shutil.copy2(resolved, folder / src.name)
            status = "copied" if status == "primary" else "copied-fallback"
            bytes_written = str(resolved.stat().st_size)
        rows.append({
            "status": status,
            "source": str(src),
            "resolved_source": str(resolved or ""),
            "archive_destination": str(DEST / src.name),
            "html_box_destination": str(HTML_BOX / src.name),
            "bytes": bytes_written,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        })

    manifest = DEST / "REQUIRED_HTML_OUTPUTS_MANIFEST.csv"
    with manifest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    copied = sum(1 for row in rows if row["status"] in {"copied", "copied-fallback"})
    fallback = sum(1 for row in rows if row["status"] == "copied-fallback")
    missing = sum(1 for row in rows if row["status"] == "missing")
    print(f"Required HTML outputs updated: {copied} copied ({fallback} fallback), {missing} missing.")
    print(f"Archive: {DEST}")
    print(f"HTML box copy: {HTML_BOX}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
