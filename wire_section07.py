"""
SECTION 07 WIRING AUTOMATOR
============================
Patches Section 07 (the processing stub) in any station's pipeline.py
using a wiring_spec.json that defines what to import and call.

Usage:
  python wire_section07.py --station sbert-embedder        # wire one station
  python wire_section07.py --scan                          # scan all, show status
  python wire_section07.py --all                           # wire all that have specs

POF 2828 | June 2026
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────
NAS_STATIONS = Path(r"X:\04_STATIONS")
REPO_STATIONS = Path(r"D:\GitHub\BACKSIDE-NLP-NEW\stations")

SEC07_START = "# 07_PROCESS"
SEC08_START = "# 08_ARTIFACTS"

STUB_SIGNATURE = "content"  # the stub puts raw file content in result["data"]


def find_stations(root: Path) -> list[Path]:
    """Find all .station folders."""
    return sorted(p for p in root.iterdir()
                  if p.is_dir() and p.name.endswith(".station"))


def is_stub(pipeline_path: Path) -> bool:
    """Check if Section 07 is still the passthrough stub."""
    if not pipeline_path.exists():
        return False
    text = pipeline_path.read_text(encoding="utf-8", errors="replace")
    # Find Section 07 block
    m_start = text.find(SEC07_START)
    m_end = text.find(SEC08_START)
    if m_start < 0 or m_end < 0:
        return False
    sec07 = text[m_start:m_end]
    # Stub signature: stores raw content, references legacy
    return '"content": payload' in sec07 or '"content": payload,' in sec07 or 'legacy_reference' in sec07


def find_runners(station_dir: Path) -> list[str]:
    """Find real processing scripts (not pipeline.py or pipeline_legacy.py)."""
    skip = {"pipeline.py", "pipeline_legacy.py", "__init__.py", "wire_section07.py"}
    return sorted(
        p.name for p in station_dir.glob("*.py")
        if p.name not in skip and not p.name.startswith("_")
    )


def load_wiring_spec(station_dir: Path) -> dict | None:
    """Load wiring_spec.json if it exists."""
    spec_path = station_dir / "wiring_spec.json"
    if not spec_path.exists():
        return None
    return json.loads(spec_path.read_text(encoding="utf-8-sig"))


def generate_section07(spec: dict) -> str:
    """Generate Section 07 Python code from a wiring spec."""
    lines = []
    lines.append("# ============================================================")
    lines.append("# 07_PROCESS  *** STATION-SPECIFIC ***")
    lines.append("# ============================================================")
    lines.append(f"# {spec.get('description', 'Station processing logic')}")
    lines.append("")

    # Imports at module level
    if spec.get("imports"):
        for imp in spec["imports"]:
            lines.append(imp)
        lines.append("")

    # Lazy init block (if station needs a client/model)
    if spec.get("init"):
        init = spec["init"]
        lines.append(f"_{init['var_name']} = None")
        lines.append("")
        lines.append("")
        lines.append(f"def _get_{init['var_name']}(cfg: dict[str, Any], log: logging.Logger):")
        lines.append(f'    """Lazy-init {init["var_name"]} — created once per run."""')
        lines.append(f"    global _{init['var_name']}")
        lines.append(f"    if _{init['var_name']} is not None:")
        lines.append(f"        return _{init['var_name']}")
        lines.append("")
        for line in init.get("code", []):
            lines.append(f"    {line}")
        lines.append("")
        lines.append(f"    return _{init['var_name']}")
        lines.append("")

    # Text reader
    lines.append("")
    lines.append("def _read_text(path: Path) -> str:")
    lines.append('    """Read file content as text. JSON files get string values concatenated."""')
    lines.append("    if path.suffix.lower() == '.json':")
    lines.append("        data = json.loads(path.read_text(encoding='utf-8-sig'))")
    lines.append("        if isinstance(data, str):")
    lines.append("            return data")
    lines.append("        if isinstance(data, dict):")
    lines.append("            parts = [str(v) for v in data.values() if v and isinstance(v, str)]")
    lines.append("            return '\\n'.join(parts) if parts else json.dumps(data)")
    lines.append("        return json.dumps(data)")
    lines.append("    return path.read_text(encoding='utf-8', errors='replace')")
    lines.append("")

    # process_one function
    lines.append("")
    lines.append("def process_one(path: Path, nlp_info: dict, cfg: dict[str, Any],")
    lines.append("                log: logging.Logger) -> dict[str, Any]:")
    lines.append(f'    """{spec.get("description", "Process one input file.")}"""')
    lines.append("    result = {")
    lines.append('        "input_file": str(path.name),')
    lines.append('        "station_id": STATION_ID,')
    lines.append('        "station_name": STATION_NAME,')
    lines.append('        "nlp_used": nlp_info.get("nlp_id", "NONE"),')
    lines.append('        "processed_at": datetime.now().isoformat(timespec="seconds"),')
    lines.append('        "success": True,')
    lines.append('        "artifacts": [],')
    lines.append('        "errors": [],')
    lines.append('        "data": {},')
    lines.append("    }")
    lines.append("")
    lines.append("    try:")
    lines.append("        text = _read_text(path)")

    # The actual processing — custom per station
    for line in spec.get("process_code", []):
        lines.append(f"        {line}")

    lines.append("")
    lines.append("    except Exception as exc:")
    lines.append('        log.exception("Processing failed for %s", path.name)')
    lines.append('        result["success"] = False')
    lines.append('        result["errors"].append(str(exc))')
    lines.append("")
    lines.append("    return result")
    lines.append("")

    return "\n".join(lines)


def patch_pipeline(pipeline_path: Path, new_section07: str) -> bool:
    """Replace Section 07 in pipeline.py with new code."""
    text = pipeline_path.read_text(encoding="utf-8", errors="replace")

    # Find the Section 07 block boundaries
    # Start: the line containing "# 07_PROCESS"
    # End: the line containing "# 08_ARTIFACTS" (and its preceding separator)
    lines = text.split("\n")
    start_idx = None
    end_idx = None

    for i, line in enumerate(lines):
        if SEC07_START in line and start_idx is None:
            # Back up to include the separator line above
            start_idx = i - 1 if i > 0 and lines[i-1].startswith("# ==") else i
        if SEC08_START in line and start_idx is not None:
            # Include the separator line above Section 08
            end_idx = i - 1 if i > 0 and lines[i-1].startswith("# ==") else i
            break

    if start_idx is None or end_idx is None:
        print(f"  ERROR: Could not find Section 07 markers in {pipeline_path}")
        return False

    # Backup
    bak = pipeline_path.with_suffix(".py.bak07")
    if not bak.exists():
        shutil.copy2(pipeline_path, bak)

    # Replace
    new_lines = lines[:start_idx] + [new_section07, ""] + lines[end_idx:]
    pipeline_path.write_text("\n".join(new_lines), encoding="utf-8")
    return True


def sync_to_repo(station_name: str) -> bool:
    """Copy pipeline.py and config.json from NAS to repo."""
    nas_dir = NAS_STATIONS / station_name
    repo_dir = REPO_STATIONS / station_name
    if not repo_dir.exists():
        repo_dir.mkdir(parents=True)

    synced = False
    for fname in ["pipeline.py", "config.json", "wiring_spec.json"]:
        src = nas_dir / fname
        dst = repo_dir / fname
        if src.exists():
            shutil.copy2(src, dst)
            synced = True
    return synced


def cmd_scan(args):
    """Scan all stations and report status."""
    stations = find_stations(NAS_STATIONS)
    print(f"\n{'Station':<40} {'Stub?':<8} {'Runners':<40} {'Spec?':<6}")
    print("-" * 94)

    stub_count = 0
    spec_count = 0
    wired_count = 0

    for sd in stations:
        name = sd.name
        pipeline = sd / "pipeline.py"
        stub = is_stub(pipeline) if pipeline.exists() else None
        runners = find_runners(sd)
        has_spec = (sd / "wiring_spec.json").exists()

        if stub is None:
            status = "NO PY"
        elif stub:
            status = "STUB"
            stub_count += 1
        else:
            status = "WIRED"
            wired_count += 1

        if has_spec:
            spec_count += 1

        runners_str = ", ".join(runners[:3])
        if len(runners) > 3:
            runners_str += f" (+{len(runners)-3})"

        print(f"{name:<40} {status:<8} {runners_str:<40} {'YES' if has_spec else '':<6}")

    print("-" * 94)
    print(f"Total: {len(stations)} stations | {stub_count} stubs | {wired_count} wired | {spec_count} specs ready")


def cmd_wire(args):
    """Wire one or all stations."""
    if args.all:
        stations = find_stations(NAS_STATIONS)
    else:
        sd = NAS_STATIONS / args.station
        if not sd.exists():
            # Try with .station suffix
            sd = NAS_STATIONS / f"{args.station}.station"
        if not sd.exists():
            print(f"Station not found: {args.station}")
            return 1
        stations = [sd]

    wired = 0
    skipped = 0
    failed = 0

    for sd in stations:
        name = sd.name
        pipeline = sd / "pipeline.py"

        if not pipeline.exists():
            print(f"  SKIP {name}: no pipeline.py")
            skipped += 1
            continue

        spec = load_wiring_spec(sd)
        if spec is None:
            if not args.all:
                print(f"  SKIP {name}: no wiring_spec.json")
            skipped += 1
            continue

        if not is_stub(pipeline) and not args.force:
            print(f"  SKIP {name}: already wired (use --force to overwrite)")
            skipped += 1
            continue

        print(f"  WIRING {name}...")
        sec07_code = generate_section07(spec)
        if patch_pipeline(pipeline, sec07_code):
            print(f"    Section 07 patched.")
            if sync_to_repo(name):
                print(f"    Synced to repo.")
            wired += 1
        else:
            print(f"    FAILED to patch.")
            failed += 1

    print(f"\nDone: {wired} wired, {skipped} skipped, {failed} failed")


def main():
    ap = argparse.ArgumentParser(description="Section 07 Wiring Automator")
    sub = ap.add_subparsers(dest="cmd")

    scan_p = sub.add_parser("scan", help="Scan all stations and show status")
    scan_p.set_defaults(func=cmd_scan)

    wire_p = sub.add_parser("wire", help="Wire Section 07 for a station")
    wire_p.add_argument("--station", help="Station name (e.g. sbert-embedder.station)")
    wire_p.add_argument("--all", action="store_true", help="Wire all stations with specs")
    wire_p.add_argument("--force", action="store_true", help="Overwrite already-wired stations")
    wire_p.set_defaults(func=cmd_wire)

    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        return 0
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
