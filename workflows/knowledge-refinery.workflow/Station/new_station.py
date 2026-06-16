"""
new_station.py — scaffold a new station from _TEMPLATE.

Usage:
    python new_station.py <LANE> <NUMBER> <name_with_underscores>

Example:
    python new_station.py AXIOM 002 canon_writer
    -> creates 10_STATIONS/ST-AXIOM-002_canon_writer/
       copied from _TEMPLATE with placeholders substituted,
       and appends an entry to station_registry.yml.

The script does NOT overwrite existing stations. If the target folder already
exists it aborts so you don't clobber work in progress.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATIONS_DIR = ROOT / "10_STATIONS"
TEMPLATE_DIR = STATIONS_DIR / "_TEMPLATE"
REGISTRY = STATIONS_DIR / "station_registry.yml"


def slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def humanize(name: str) -> str:
    return name.replace("_", " ").replace("-", " ").strip().title()


def substitute(text: str, mapping: dict[str, str]) -> str:
    for key, val in mapping.items():
        text = text.replace("{{" + key + "}}", val)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new station from _TEMPLATE.")
    parser.add_argument("lane", help="Lane code, e.g. AXIOM, 7QS, ROUTE, CONV")
    parser.add_argument("number", help="Three-digit station number, e.g. 002")
    parser.add_argument("name", help="Snake_case name, e.g. canon_writer")
    parser.add_argument("--purpose", default="TODO: describe what this station does.")
    parser.add_argument("--model-primary", default="M-REASON-001")
    parser.add_argument("--model-fallback", default="M-REASON-002")
    parser.add_argument("--next-pass", default="ST-TBD-000",
                        help="Station id to route to on gate pass.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be created, but don't write anything.")
    args = parser.parse_args()

    lane = args.lane.strip().upper()
    number = args.number.strip().zfill(3)
    name = slugify(args.name)

    station_id = f"ST-{lane}-{number}"
    folder_name = f"{station_id}_{name}"
    target = STATIONS_DIR / folder_name

    if not TEMPLATE_DIR.is_dir():
        print(f"ERROR: template missing at {TEMPLATE_DIR}", file=sys.stderr)
        return 2

    if target.exists():
        print(f"ERROR: target already exists: {target}", file=sys.stderr)
        return 3

    mapping = {
        "STATION_ID": station_id,
        "STATION_NAME": humanize(name),
        "LANE": lane.lower(),
        "FOLDER_NAME": folder_name,
        "PURPOSE": args.purpose,
        "MODEL_PRIMARY": args.model_primary,
        "MODEL_FALLBACK": args.model_fallback,
        "PROMPT_PRIMARY": f"P-{lane}-{number}",
        "PROMPT_FALLBACK": "",
        "SCRIPT_RUNNER": f"S-{lane}-{number}",
        "INPUT_TYPE": "TODO_input_type",
        "INPUT_FILE": "source.md",
        "OUTPUT_FILE_JSON": "result.json",
        "OUTPUT_FILE_MD": "result.md",
        "GATE_RULE": "TODO_gate_rule",
        "NEXT_STATION_PASS": args.next_pass,
    }

    if args.dry_run:
        print(f"[dry-run] would create: {target}")
        print(f"[dry-run] substitutions: {mapping}")
        return 0

    shutil.copytree(TEMPLATE_DIR, target)

    for filename in ("station.yml", "README.md"):
        path = target / filename
        if path.exists():
            path.write_text(substitute(path.read_text(encoding="utf-8"), mapping),
                            encoding="utf-8")

    registry_entry = (
        f"\n"
        f"  - id: {station_id}\n"
        f"    name: {humanize(name)}\n"
        f"    lane: {lane.lower()}\n"
        f"    status: draft\n"
        f"    folder: 10_STATIONS/{folder_name}\n"
        f"    inputs: [source.md]\n"
        f"    outputs: [result.json, result.md]\n"
        f"    next: [{args.next_pass}]\n"
    )

    if REGISTRY.exists():
        with REGISTRY.open("a", encoding="utf-8") as fh:
            fh.write(registry_entry)
    else:
        REGISTRY.write_text("stations:" + registry_entry, encoding="utf-8")

    print(f"Created station: {target}")
    print(f"Registered in:   {REGISTRY}")
    print(f"Next steps:")
    print(f"  1. Fill in remaining TODOs in {target / 'station.yml'}")
    print(f"  2. Drop prompt file into {target / 'prompts'}")
    print(f"  3. Drop runner into {target / 'scripts'}")
    print(f"  4. Flip status: draft -> active in station.yml and registry")
    print(f"  (created {datetime.now().isoformat(timespec='seconds')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
