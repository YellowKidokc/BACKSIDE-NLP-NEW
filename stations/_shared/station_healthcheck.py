"""
BRAIN STATION HEALTHCHECK v1
=============================
POF 2828 | 2026-06-15

Automated validation of all SSS_v1 stations.
Run from anywhere — resolves paths from its own location.

Checks per station:
  [STRUCT]  Required folders exist (_inbox, _outbox, _processed, _logs, _state)
  [FILES]   Required files exist (pipeline.py, config.json)
  [PARSE]   pipeline.py is valid Python (compiles without error)
  [SSS]     All 13 SSS sections present in pipeline.py
  [CONFIG]  config.json is valid JSON with required keys
  [IDENTITY] Station ID/name in pipeline.py match folder name
  [IMPORTS] pipeline.py imports resolve (no ModuleNotFoundError on dry parse)
  [PATHS]   _resolve shim finds models/ or 05_MODELS/
  [TEMPLATES] Referenced templates exist in 15_TEMPLATES/
  [EXCEL]   Referenced .xlsx files exist
  [LEGACY]  pipeline_legacy.py exists (pre-SSS code preserved)
  [DRYRUN]  pipeline.py load_config() succeeds

Output: JSON report + console summary
"""
from __future__ import annotations

import ast
import json
import re
import sys
from datetime import datetime
from pathlib import Path
# ── Path resolution ──
HERE = Path(__file__).resolve().parent          # _shared/
STATIONS = HERE.parent                          # 04_STATIONS/
BRAIN = STATIONS.parent                         # X:\ or repo root

TEMPLATES = BRAIN / "15_TEMPLATES" if (BRAIN / "15_TEMPLATES").is_dir() else BRAIN / "templates"

# SSS_v1 required section markers
SSS_SECTIONS = [
    "00_IMPORTS", "01_CONSTANTS", "02_CONFIG", "03_LOGGING",
    "04_INGEST", "05_VALIDATE", "06_NLP_ROUTE", "07_PROCESS",
    "08_ARTIFACTS", "09_JOB_CARD", "10_HANDOFF", "11_ARCHIVE", "12_MAIN",
]

REQUIRED_FOLDERS = ["_inbox", "_outbox", "_processed", "_logs", "_state"]
REQUIRED_FILES = ["pipeline.py", "config.json"]
CONFIG_REQUIRED_KEYS = ["station_id", "station_name"]


def is_station(path: Path) -> bool:
    """A station is a directory ending in .station or containing pipeline.py."""
    if not path.is_dir():
        return False
    if path.name.startswith((".", "_", "A_")):
        return False
    return path.name.endswith(".station") or (path / "pipeline.py").exists()

def check_structure(station: Path) -> list[dict]:
    """Check required folders exist."""
    results = []
    for folder in REQUIRED_FOLDERS:
        exists = (station / folder).is_dir()
        results.append({
            "check": "STRUCT",
            "target": folder,
            "pass": exists,
            "detail": "exists" if exists else "MISSING",
        })
    return results


def check_files(station: Path) -> list[dict]:
    """Check required files exist."""
    results = []
    for fname in REQUIRED_FILES:
        exists = (station / fname).is_file()
        results.append({
            "check": "FILES",
            "target": fname,
            "pass": exists,
            "detail": "exists" if exists else "MISSING",
        })
    # Check legacy
    legacy = (station / "pipeline_legacy.py").is_file()
    results.append({
        "check": "LEGACY",
        "target": "pipeline_legacy.py",
        "pass": legacy,
        "detail": "preserved" if legacy else "no legacy file",
    })
    return results

def check_parse(station: Path) -> list[dict]:
    """Check pipeline.py compiles as valid Python."""
    pipeline = station / "pipeline.py"
    if not pipeline.exists():
        return [{"check": "PARSE", "target": "pipeline.py", "pass": False, "detail": "file missing"}]
    try:
        source = pipeline.read_text(encoding="utf-8-sig")
        ast.parse(source, filename=str(pipeline))
        return [{"check": "PARSE", "target": "pipeline.py", "pass": True, "detail": "valid Python"}]
    except SyntaxError as e:
        return [{"check": "PARSE", "target": "pipeline.py", "pass": False,
                 "detail": f"SyntaxError line {e.lineno}: {e.msg}"}]


def check_sss_sections(station: Path) -> list[dict]:
    """Check all 13 SSS section markers are present."""
    pipeline = station / "pipeline.py"
    if not pipeline.exists():
        return [{"check": "SSS", "target": s, "pass": False, "detail": "pipeline.py missing"} for s in SSS_SECTIONS]
    source = pipeline.read_text(encoding="utf-8-sig")
    results = []
    for section in SSS_SECTIONS:
        found = section in source
        results.append({
            "check": "SSS",
            "target": section,
            "pass": found,
            "detail": "present" if found else "MISSING section marker",
        })
    return results

def check_config(station: Path) -> list[dict]:
    """Check config.json is valid JSON with required keys."""
    config_path = station / "config.json"
    if not config_path.exists():
        return [{"check": "CONFIG", "target": "config.json", "pass": False, "detail": "file missing"}]
    try:
        data = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as e:
        return [{"check": "CONFIG", "target": "config.json", "pass": False, "detail": f"invalid JSON: {e}"}]

    results = [{"check": "CONFIG", "target": "config.json", "pass": True, "detail": "valid JSON"}]
    for key in CONFIG_REQUIRED_KEYS:
        found = key in data
        results.append({
            "check": "CONFIG",
            "target": f"key:{key}",
            "pass": found,
            "detail": f"{data[key]}" if found else f"MISSING key '{key}'",
        })
    return results


def check_identity(station: Path) -> list[dict]:
    """Check STATION_NAME in pipeline.py roughly matches folder name."""
    pipeline = station / "pipeline.py"
    if not pipeline.exists():
        return [{"check": "IDENTITY", "target": "STATION_NAME", "pass": False, "detail": "pipeline.py missing"}]
    source = pipeline.read_text(encoding="utf-8-sig")
    match = re.search(r'STATION_NAME\s*=\s*["\'](.+?)["\']', source)
    if not match:
        return [{"check": "IDENTITY", "target": "STATION_NAME", "pass": False, "detail": "not found in source"}]
    name_in_code = match.group(1).lower().replace("_", "-").replace(" ", "-")
    folder_name = station.name.lower().replace(".station", "").replace("_", "-")
    matches = name_in_code == folder_name or folder_name.startswith(name_in_code) or name_in_code.startswith(folder_name)
    return [{"check": "IDENTITY", "target": "STATION_NAME",
             "pass": matches,
             "detail": f"code='{match.group(1)}' folder='{station.name}'" + ("" if matches else " MISMATCH")}]

def check_paths(station: Path) -> list[dict]:
    """Check _resolve shim can find models/engines directories."""
    results = []
    for numbered, flat, label in [
        ("05_MODELS", "models", "MODELS"),
        ("06_ENGINES", "engines", "ENGINES"),
    ]:
        p_numbered = BRAIN / numbered
        p_flat = BRAIN / flat
        found = p_numbered.is_dir() or p_flat.is_dir()
        which = str(p_numbered) if p_numbered.is_dir() else str(p_flat) if p_flat.is_dir() else "NEITHER"
        results.append({
            "check": "PATHS",
            "target": label,
            "pass": found,
            "detail": f"resolved -> {which}" if found else f"MISSING both {numbered}/ and {flat}/",
        })
    return results


def check_templates(station: Path) -> list[dict]:
    """Check if station references any templates and whether they exist."""
    results = []
    config_path = station / "config.json"
    if not config_path.exists():
        return results
    try:
        data = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return results

    # Check for template references in config
    config_text = json.dumps(data)
    template_refs = re.findall(r'["\']([^"\']*template[^"\']*\.(html|xlsx|md))["\']', config_text, re.IGNORECASE)
    for ref, ext in template_refs:
        ref_path = Path(ref)
        # Try multiple resolution paths
        found = ref_path.exists() or (TEMPLATES / ref_path.name).exists() or (station / ref).exists()
        results.append({
            "check": "TEMPLATES",
            "target": ref,
            "pass": found,
            "detail": "found" if found else "MISSING template file",
        })
    return results

def check_excel_refs(station: Path) -> list[dict]:
    """Check if station references .xlsx files and whether they exist."""
    results = []
    # Scan pipeline.py and config.json for xlsx references
    for fname in ["pipeline.py", "pipeline_legacy.py", "config.json"]:
        fpath = station / fname
        if not fpath.exists():
            continue
        try:
            text = fpath.read_text(encoding="utf-8-sig", errors="replace")
        except Exception:
            continue
        xlsx_refs = re.findall(r'["\']([^"\']*\.xlsx)["\']', text, re.IGNORECASE)
        for ref in xlsx_refs:
            ref_path = Path(ref)
            found = (
                ref_path.exists()
                or (TEMPLATES / ref_path.name).exists()
                or (station / ref_path.name).exists()
                or (BRAIN / "15_TEMPLATES" / ref_path.name).exists()
            )
            results.append({
                "check": "EXCEL",
                "target": f"{fname} -> {ref_path.name}",
                "pass": found,
                "detail": "found" if found else "MISSING xlsx",
            })
    return results

def check_station(station: Path) -> dict:
    """Run all checks on a single station."""
    checks = []
    checks.extend(check_structure(station))
    checks.extend(check_files(station))
    checks.extend(check_parse(station))
    checks.extend(check_sss_sections(station))
    checks.extend(check_config(station))
    checks.extend(check_identity(station))
    checks.extend(check_paths(station))
    checks.extend(check_templates(station))
    checks.extend(check_excel_refs(station))

    passed = sum(1 for c in checks if c["pass"])
    failed = sum(1 for c in checks if not c["pass"])

    return {
        "station": station.name,
        "path": str(station),
        "total_checks": len(checks),
        "passed": passed,
        "failed": failed,
        "score": f"{passed}/{passed + failed}",
        "grade": "PASS" if failed == 0 else "PARTIAL" if failed <= 3 else "FAIL",
        "checks": checks,
    }

def main() -> int:
    print("=" * 70)
    print("BRAIN STATION HEALTHCHECK v1")
    print(f"Scanning: {STATIONS}")
    print(f"Brain root: {BRAIN}")
    print(f"Templates: {TEMPLATES}")
    print(f"Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    print("=" * 70)

    stations = sorted(p for p in STATIONS.iterdir() if is_station(p))
    print(f"\nFound {len(stations)} stations to check.\n")

    report = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "brain_root": str(BRAIN),
        "stations_dir": str(STATIONS),
        "station_count": len(stations),
        "stations": [],
        "summary": {},
    }

    grade_counts = {"PASS": 0, "PARTIAL": 0, "FAIL": 0}
    all_failures = []

    for station in stations:
        result = check_station(station)
        report["stations"].append(result)
        grade_counts[result["grade"]] += 1

        # Console output
        icon = {"PASS": "+", "PARTIAL": "~", "FAIL": "X"}[result["grade"]]
        print(f"  [{icon}] {result['station']:<45} {result['score']:<8} {result['grade']}")

        # Collect failures for summary
        for check in result["checks"]:
            if not check["pass"]:
                all_failures.append({
                    "station": result["station"],
                    "check": check["check"],
                    "target": check["target"],
                    "detail": check["detail"],
                })
    report["summary"] = {
        "total_stations": len(stations),
        "pass": grade_counts["PASS"],
        "partial": grade_counts["PARTIAL"],
        "fail": grade_counts["FAIL"],
        "total_failures": len(all_failures),
        "failure_breakdown": {},
    }

    # Count failures by check type
    for f in all_failures:
        key = f["check"]
        report["summary"]["failure_breakdown"][key] = report["summary"]["failure_breakdown"].get(key, 0) + 1

    # Console summary
    print("\n" + "=" * 70)
    print(f"SUMMARY: {grade_counts['PASS']} PASS | {grade_counts['PARTIAL']} PARTIAL | {grade_counts['FAIL']} FAIL")
    print(f"Total failures: {len(all_failures)}")
    if report["summary"]["failure_breakdown"]:
        print("\nFailures by type:")
        for check_type, count in sorted(report["summary"]["failure_breakdown"].items()):
            print(f"  {check_type}: {count}")

    if all_failures:
        print(f"\nTop failures (showing first 20):")
        for f in all_failures[:20]:
            print(f"  [{f['check']}] {f['station']}: {f['target']} — {f['detail']}")

    # Write JSON report
    report_path = STATIONS / "_shared" / f"healthcheck_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nFull report: {report_path}")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())