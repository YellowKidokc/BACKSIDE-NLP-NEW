from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_files(path: Path, recursive: bool) -> Iterable[Path]:
    if path.is_file():
        yield path
        return
    pattern = "**/*" if recursive else "*"
    for item in path.glob(pattern):
        if item.is_file():
            yield item


@dataclass
class TransportRecord:
    source: str
    destination: str
    operation: str
    status: str
    size: int
    source_hash: str | None
    destination_hash: str | None
    conflict_policy: str
    message: str


def destination_for(source_root: Path, source_file: Path, dest_root: Path) -> Path:
    if source_root.is_file():
        return dest_root / source_file.name
    return dest_root / source_file.relative_to(source_root)


def transport(
    source: Path,
    destination: Path,
    operation: str,
    recursive: bool,
    conflict_policy: str,
    apply: bool,
    manifest: Path,
) -> list[TransportRecord]:
    records: list[TransportRecord] = []
    files = list(iter_files(source, recursive))
    destination.mkdir(parents=True, exist_ok=True)

    for src in files:
        dst = destination_for(source, src, destination)
        src_hash = sha256(src)
        dst_hash = sha256(dst) if dst.exists() and dst.is_file() else None
        status = "planned"
        message = "dry-run"

        if dst.exists():
            if dst_hash == src_hash:
                status = "skipped"
                message = "destination already matches source"
            elif conflict_policy == "skip":
                status = "conflict_skipped"
                message = "destination exists and differs"
            elif conflict_policy == "version":
                stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                dst = dst.with_name(f"{dst.stem}.{stamp}{dst.suffix}")
                status = "planned_versioned"
                message = "destination exists; versioned target selected"
            elif conflict_policy in {"overwrite", "source_wins"}:
                status = "planned_overwrite"
                message = "destination exists; overwrite selected"
            else:
                status = "conflict_review"
                message = f"unsupported conflict policy for existing file: {conflict_policy}"

        if apply and not status.startswith("conflict_review") and not status.endswith("skipped") and status != "skipped":
            dst.parent.mkdir(parents=True, exist_ok=True)
            if operation == "copy":
                shutil.copy2(src, dst)
                status = "copied"
                message = "copied"
            elif operation == "move":
                shutil.move(str(src), str(dst))
                status = "moved"
                message = "moved"
            else:
                status = "error"
                message = f"unsupported operation: {operation}"
        elif not apply and status.startswith("planned"):
            message = "dry-run would transfer"

        final_hash = sha256(dst) if dst.exists() and dst.is_file() else None
        records.append(
            TransportRecord(
                source=str(src),
                destination=str(dst),
                operation=operation,
                status=status,
                size=src.stat().st_size if src.exists() else 0,
                source_hash=src_hash,
                destination_hash=final_hash,
                conflict_policy=conflict_policy,
                message=message,
            )
        )

    payload = {
        "schema_version": "fap.transport.v1",
        "generated_at": now(),
        "source": str(source),
        "destination": str(destination),
        "operation": operation,
        "recursive": recursive,
        "conflict_policy": conflict_policy,
        "apply": apply,
        "file_count": len(records),
        "records": [asdict(record) for record in records],
    }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Tracked FAP file transport engine.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--operation", choices=["copy", "move"], default="copy")
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--conflict-policy", choices=["skip", "overwrite", "source_wins", "version", "review"], default="version")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    records = transport(
        source=Path(args.source),
        destination=Path(args.dest),
        operation=args.operation,
        recursive=args.recursive,
        conflict_policy=args.conflict_policy,
        apply=args.apply,
        manifest=Path(args.manifest),
    )
    print(f"{'Applied' if args.apply else 'Planned'} {len(records)} file(s). Manifest: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
