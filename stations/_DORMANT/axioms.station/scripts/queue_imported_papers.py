from __future__ import annotations

import csv
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORT_ROOT = ROOT / "papers" / "_import_2026-05-11"
INBOX = ROOT / "00_INBOX_DROP_PAPERS_HERE"
MANIFESTS = ROOT / "05_MANIFESTS"

def should_queue(path: Path) -> bool:
    parts = path.parts
    if not parts:
        return False
    if any(part.startswith("_") for part in parts):
        return False
    if parts[0] == "session_handoffs":
        return False
    if parts[0] == "gtq_articles":
        return len(parts) == 3 and path.name.lower().startswith("gtq-") and path.suffix.lower() in {".html", ".htm"}
    if parts[0] in {"proof_architecture", "cannon"}:
        return path.suffix.lower() in {".txt", ".md", ".html", ".htm"}
    return False


def unique_target(name: str) -> Path:
    target = INBOX / name
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return INBOX / f"{stem}_{stamp}{suffix}"


def main() -> int:
    INBOX.mkdir(parents=True, exist_ok=True)
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    rows = []

    candidates = sorted(
        p for p in IMPORT_ROOT.rglob("*")
        if p.is_file() and p.suffix.lower() in {".txt", ".md", ".html", ".htm"}
    )
    for src in candidates:
        rel = src.relative_to(IMPORT_ROOT)
        if not should_queue(rel):
            rows.append({"status": "skipped_noncanonical", "source": str(src), "destination": "", "bytes": str(src.stat().st_size)})
            continue
        target = unique_target(src.name)
        shutil.copy2(src, target)
        rows.append({"status": "queued", "source": str(src), "destination": str(target), "bytes": str(src.stat().st_size)})

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest = MANIFESTS / f"queued-imported-papers-{stamp}.csv"
    with manifest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["status", "source", "destination", "bytes"])
        writer.writeheader()
        writer.writerows(rows)

    queued = sum(1 for row in rows if row["status"] == "queued")
    skipped = sum(1 for row in rows if row["status"] != "queued")
    print(f"Queued imported papers: {queued}")
    print(f"Skipped backups/system files: {skipped}")
    print(f"Manifest: {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
