"""
migrate_drop_numbers.py — one-shot migration: strip the NN_ folder-number
prefix and migrate the number into station.yml's `order:` field.

Run ONCE. Idempotent — re-running on already-migrated folders is a no-op.

Steps per folder:
  1. Extract NN from folder name (NN_short_name).
  2. Read station.yml.
  3. If `order:` field is missing, insert `order: <NN>` after the `status:` line.
  4. Rename folder NN_short_name -> short_name (after the yml edit).

Concurrency:
  Holds stations_registry.lock for the duration so registry_rebuilder.py
  can't race. Does NOT block new_station.py — David has frozen scaffolding
  for this migration per the message of 2026-05-16.

After this completes, run:  python registry_rebuilder.py
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIONS_DIR = ROOT / "stations"
LOCK = ROOT / "stations_registry.lock"

NN_PREFIX = re.compile(r"^(\d{2})_(.+)$")


def insert_order_field(yml_text: str, order: int) -> tuple[str, bool]:
    """Insert `order: NN` after the `status:` line if not already present.
    Returns (new_text, was_inserted)."""
    # Skip if order already there
    if re.search(r"^\s*order:\s*\d+", yml_text, flags=re.MULTILINE):
        return yml_text, False

    # Insert after the status: line (preserving line ending style)
    pattern = re.compile(r"^(status:\s*\S+.*)$", flags=re.MULTILINE)
    new_text, n = pattern.subn(rf"\1\norder: {order}", yml_text, count=1)
    if n == 0:
        # No status line — append at end of top-level scalars (after `lane:` if found)
        pattern2 = re.compile(r"^(lane:\s*\S+.*)$", flags=re.MULTILINE)
        new_text, n = pattern2.subn(rf"\1\norder: {order}", yml_text, count=1)
    if n == 0:
        # Last resort: prepend
        new_text = f"order: {order}\n" + yml_text
    return new_text, True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not STATIONS_DIR.is_dir():
        print(f"ERROR: {STATIONS_DIR} missing", file=sys.stderr)
        return 2

    if LOCK.exists() and not args.dry_run:
        print(f"ERROR: lock exists at {LOCK}. Another rebuild is running.", file=sys.stderr)
        print("If stale, remove manually.", file=sys.stderr)
        return 2

    if not args.dry_run:
        LOCK.write_text(f"migration_started={datetime.now().isoformat(timespec='seconds')}\n",
                        encoding="utf-8")

    renamed = []
    skipped = []
    order_added = []
    collisions = []

    try:
        folders = sorted(d for d in STATIONS_DIR.iterdir() if d.is_dir())
        for folder in folders:
            m = NN_PREFIX.match(folder.name)
            if not m:
                if not folder.name.startswith("_"):
                    skipped.append(f"{folder.name}: no NN_ prefix (already migrated?)")
                continue

            order_num = int(m.group(1))
            new_name = m.group(2)
            new_path = STATIONS_DIR / new_name

            if new_path.exists():
                collisions.append(f"{folder.name} -> {new_name} (target exists)")
                continue

            # Add order: field to station.yml if present
            yml = folder / "station.yml"
            inserted = False
            if yml.exists():
                text = yml.read_text(encoding="utf-8")
                new_text, inserted = insert_order_field(text, order_num)
                if inserted and not args.dry_run:
                    yml.write_text(new_text, encoding="utf-8")

            if args.dry_run:
                renamed.append(f"{folder.name} -> {new_name} (order={order_num}, yml updated: {inserted})")
            else:
                folder.rename(new_path)
                renamed.append(f"{folder.name} -> {new_name} (order={order_num}, yml updated: {inserted})")
                if inserted:
                    order_added.append(new_name)
    finally:
        if not args.dry_run:
            LOCK.unlink(missing_ok=True)

    print(f"\n=== Migration {'(dry-run) ' if args.dry_run else ''}summary ===")
    print(f"Renamed:       {len(renamed)}")
    for r in renamed:
        print(f"  {r}")
    if skipped:
        print(f"\nSkipped:       {len(skipped)}")
        for s in skipped:
            print(f"  {s}")
    if collisions:
        print(f"\n!! COLLISIONS: {len(collisions)} — these were NOT renamed:")
        for c in collisions:
            print(f"  {c}")
        return 1

    if not args.dry_run:
        print(f"\nNext: python registry_rebuilder.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
