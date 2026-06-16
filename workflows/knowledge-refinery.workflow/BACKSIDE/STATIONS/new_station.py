"""
new_station.py — scaffold a new station from stations/_TEMPLATE/.

Lives at BACKSIDE/STATIONS/. Mirror of how MODELS works.

Usage:
    python new_station.py <short_name> [flags]

Examples:
    python new_station.py html_to_md --lane CONV --model none
    python new_station.py claim_dedup --lane CLAIM --model M-EMB-GEN-001 \\
        --purpose "Dedup new claims against the existing claim store." --status draft

Folder name is the slugified short_name — NO number prefix. Ordering moved
into station.yml's `order:` field (auto-incremented per lane unless --order given).

The station_id is derived: ST-{LANE}-{NNN} where NNN is per-lane sequence,
computed by counting existing stations in the same lane.

Does NOT overwrite existing stations. Does NOT write the registry — run
registry_rebuilder.py after creating to register.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATIONS_DIR = ROOT / "stations"
TEMPLATE_DIR = STATIONS_DIR / "_TEMPLATE"
REGISTRY = ROOT / "stations_registry.yml"


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
    parser.add_argument("name", help="snake_case short name, e.g. claim_check. Becomes the folder name.")
    parser.add_argument("--lane", default="MISC",
                        help="Lane code (uppercase in id, lowercase in lane field). e.g. EMBED, NLI, SEVENQ")
    parser.add_argument("--model", default="M-TBD-000",
                        help="Bound model id (e.g. M-EMB-SCI-001) or LLM model name (gpt-4o-mini)")
    parser.add_argument("--model-fallback", default="")
    parser.add_argument("--provider", default="local_wrapper",
                        choices=["local_wrapper", "openai", "anthropic", "hf"])
    parser.add_argument("--purpose", default="TODO: describe what this station does.")
    parser.add_argument("--status", default="draft",
                        choices=["draft", "active", "paused", "retired"])
    parser.add_argument("--next-pass", default="ST-TBD-000",
                        help="Station id to route to on gate pass.")
    parser.add_argument("--input-file", default="source.md")
    parser.add_argument("--input-type", default="markdown_article")
    parser.add_argument("--order", type=int, default=None,
                        help="Order hint for sort/display. Default: max existing order + 1.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    name = slugify(args.name)
    lane = args.lane.strip().upper()
    folder_name = name                           # NO number prefix — David's decision 2026-05-16
    target = STATIONS_DIR / folder_name

    # Per-lane next-NNN + max order: scan disk truth.
    # Use max(NNN)+1 so non-contiguous IDs (e.g. CONV-001, 012, 013, ...) don't collide.
    max_lane_nnn = 0
    max_order = 0
    sid_re = re.compile(r"^\s*station_id:\s*ST-([A-Za-z]+)-(\d+)\b")
    if STATIONS_DIR.is_dir():
        for d in STATIONS_DIR.iterdir():
            if not d.is_dir() or d.name.startswith("_"):
                continue
            yml = d / "station.yml"
            if not yml.exists():
                continue
            text = yml.read_text(encoding="utf-8", errors="ignore")
            for line in text.splitlines():
                sid = sid_re.match(line)
                if sid and sid.group(1).upper() == lane:
                    max_lane_nnn = max(max_lane_nnn, int(sid.group(2)))
                m2 = re.match(r"^\s*order:\s*(\d+)", line)
                if m2:
                    max_order = max(max_order, int(m2.group(1)))
    station_id = f"ST-{lane}-{(max_lane_nnn + 1):03d}"
    order = args.order if args.order is not None else (max_order + 1)

    if not TEMPLATE_DIR.is_dir():
        print(f"ERROR: template missing at {TEMPLATE_DIR}", file=sys.stderr)
        return 2
    if target.exists():
        print(f"ERROR: target already exists: {target}", file=sys.stderr)
        return 3

    mapping = {
        "STATION_ID":       station_id,
        "STATION_NAME":     humanize(name),
        "LANE":             lane.lower(),
        "STATUS":           args.status,
        "ORDER":            str(order),
        "FOLDER_NAME":      folder_name,
        "PURPOSE":          args.purpose,
        "MODEL_PRIMARY":    args.model,
        "MODEL_FALLBACK":   args.model_fallback,
        "MODEL_PROVIDER":   args.provider,
        "PROMPT_PRIMARY":   "PROMPT_SYSTEM.md",
        "PROMPT_FALLBACK":  "",
        "SCRIPT_RUNNER":    "scripts/03_run_prompt.bat",
        "INPUT_TYPE":       args.input_type,
        "INPUT_FILE":       args.input_file,
        "OUTPUT_FILE_JSON": "result.json",
        "OUTPUT_FILE_MD":   "result.md",
        "GATE_RULE":        "TODO_gate_rule",
        "NEXT_STATION_PASS": args.next_pass,
    }

    if args.dry_run:
        print(f"[dry-run] would create: {target}")
        print(f"[dry-run] station_id: {station_id}")
        print(f"[dry-run] mapping: {mapping}")
        return 0

    shutil.copytree(TEMPLATE_DIR, target)

    # Substitute placeholders in every text file we know about.
    SUBSTITUTE_FILES = [
        "station.yml", "README.md", "PROMPT_SYSTEM.md", "PROMPT_TEST.md",
        "input/sample_input.md",
        "scripts/00_init.bat", "scripts/01_healthcheck.bat",
        "scripts/02_smoke_test.bat", "scripts/03_run_prompt.bat",
        "scripts/05_stop.bat",
    ]
    for rel in SUBSTITUTE_FILES:
        path = target / rel
        if path.exists():
            path.write_text(substitute(path.read_text(encoding="utf-8"), mapping),
                            encoding="utf-8")

    # NOTE: registry is NOT written here anymore.
    # Direct concurrent appends to stations_registry.yml on the SMB share
    # caused lost writes when two LLMs scaffolded in parallel. The registry
    # is now rebuilt deterministically from every folder's station.yml by
    # registry_rebuilder.py. This script only writes the folder.

    print(f"Created station: {target}")
    print(f"Registry NOT updated by this script.")
    print(f"Next steps:")
    print(f"  1. Fill in remaining TODOs in {target / 'station.yml'}")
    print(f"  2. Replace runner stub in {target / 'scripts' / '03_run_prompt.bat'}")
    print(f"     or drop a run.py beside it (the stub will call run.py if present).")
    print(f"  3. Flip status: draft -> active when ready.")
    print(f"  4. Run: python {ROOT / 'registry_rebuilder.py'}  to register.")
    print(f"  (created {datetime.now().isoformat(timespec='seconds')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
