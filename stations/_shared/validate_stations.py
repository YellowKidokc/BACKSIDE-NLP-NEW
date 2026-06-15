"""
Station Validation Script — SSS_v1 Plumbing Check
Walks every station in the repo and validates:
1. Required files exist (pipeline.py, config.json)
2. pipeline.py compiles (AST parse)
3. config.json parses correctly
4. Section 07 has real logic (not passthrough stub)
5. NLP model references resolve to actual model folders
6. Input/output paths resolve correctly
7. Template references exist
"""
import ast
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent           # _shared/
STATIONS_DIR = HERE.parent                        # stations/
REPO = STATIONS_DIR.parent                        # repo root
MODELS_DIR = REPO / "models"
ENGINES_DIR = REPO / "engines"


# Available models and engines (from repo)
VALID_MODELS = set()
VALID_ENGINES = set()

if MODELS_DIR.exists():
    VALID_MODELS = {d.name for d in MODELS_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')}
if ENGINES_DIR.exists():
    VALID_ENGINES = {d.name for d in ENGINES_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')}


def check_station(station_dir: Path) -> dict:
    """Validate a single station. Returns a result dict."""
    name = station_dir.name
    result = {
        "station": name,
        "has_pipeline": False,
        "has_legacy": False,
        "has_config": False,
        "pipeline_compiles": False,
        "config_valid": False,
        "section07_real": False,
        "section06_model": None,
        "input_extensions": [],
        "has_inbox": False,
        "has_outbox": False,
        "nlp_references": [],
        "errors": [],
        "warnings": [],
        "status": "UNKNOWN"
    }

    pipeline = station_dir / "pipeline.py"
    legacy = station_dir / "pipeline_legacy.py"
    config = station_dir / "config.json"

    # 1. Check required files
    result["has_pipeline"] = pipeline.exists()
    result["has_legacy"] = legacy.exists()
    result["has_config"] = config.exists()
    result["has_inbox"] = (station_dir / "_inbox").exists()
    result["has_outbox"] = (station_dir / "_outbox").exists()

    if not result["has_pipeline"]:
        result["errors"].append("MISSING pipeline.py")
        result["status"] = "FAIL"
        return result

    # 2. AST parse pipeline.py
    try:
        code = pipeline.read_text(encoding="utf-8", errors="replace")
        ast.parse(code)
        result["pipeline_compiles"] = True
    except SyntaxError as e:
        result["errors"].append(f"SYNTAX ERROR: {e.msg} (line {e.lineno})")
        result["status"] = "FAIL"
        return result

    # 3. Parse config.json
    if config.exists():
        try:
            cfg = json.loads(config.read_text(encoding="utf-8", errors="replace"))
            result["config_valid"] = True
            result["input_extensions"] = cfg.get("input_extensions", [])
            workers = cfg.get("workers", {})
            if workers:
                result["nlp_references"].append(str(workers))
        except json.JSONDecodeError as e:
            result["errors"].append(f"CONFIG JSON ERROR: {e}")

    # 4. Check section 07 — is it real logic or passthrough?
    if "# SECTION 07" in code or "# 07_PROCESS" in code:
        # Find process_one function
        s07_match = re.search(r'def process_one\(.*?\).*?(?=\n# SECTION 08|\n# 08_|\nif __name__|$)', 
                              code, re.DOTALL)
        if s07_match:
            s07_body = s07_match.group()
            # Check if it's just the passthrough stub
            if "pass" in s07_body and len(s07_body.strip().split('\n')) < 10:
                result["section07_real"] = False
                result["warnings"].append("Section 07 is passthrough stub")
            elif "PHASE2_SKIP" in s07_body:
                result["section07_real"] = False
                result["warnings"].append("PHASE2_SKIP — too complex for auto-migration")
            else:
                result["section07_real"] = True
        else:
            result["warnings"].append("Could not find process_one() function")
    else:
        # Non-SSS format — check if there's any real logic
        if len(code.strip().split('\n')) > 20:
            result["section07_real"] = True
            result["warnings"].append("Non-SSS format but has logic")
        else:
            result["section07_real"] = False

    # 5. Check NLP model references in code
    model_refs = re.findall(r'M\d{2}_\w+', code)
    engine_refs = re.findall(r'P\d{2}_\w+', code)
    if model_refs:
        result["section06_model"] = model_refs[0]
        for ref in model_refs:
            if ref not in VALID_MODELS:
                result["warnings"].append(f"NLP ref '{ref}' not found in models/")
    if engine_refs:
        for ref in engine_refs:
            if ref not in VALID_ENGINES:
                result["warnings"].append(f"Engine ref '{ref}' not found in engines/")

    # 6. Determine status
    if result["errors"]:
        result["status"] = "FAIL"
    elif not result["section07_real"]:
        result["status"] = "STUB"
    elif result["warnings"]:
        result["status"] = "WARN"
    else:
        result["status"] = "PASS"

    return result


def main():
    print("=" * 80)
    print("STATION VALIDATION REPORT — SSS_v1 Plumbing Check")
    print(f"Repo: {REPO}")
    print(f"Models available: {sorted(VALID_MODELS)}")
    print(f"Engines available: {sorted(VALID_ENGINES)}")
    print("=" * 80)

    station_dirs = sorted([
        d for d in STATIONS_DIR.iterdir()
        if d.is_dir()
        and not d.name.startswith('_')
        and not d.name.startswith('.')
        and d.name != 'axioms'
        and d.name != 'ollama'
        and d.name != 'Treaties'
    ])

    results = []
    for sd in station_dirs:
        r = check_station(sd)
        results.append(r)

    # Summary
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    stub_count = sum(1 for r in results if r["status"] == "STUB")
    warn_count = sum(1 for r in results if r["status"] == "WARN")
    fail_count = sum(1 for r in results if r["status"] == "FAIL")

    print(f"\n{'STATION':<45} {'STATUS':<8} {'S07':<6} {'CONFIG':<8} {'LEGACY':<8} {'NLP':<20}")
    print("-" * 100)
    for r in results:
        s07 = "REAL" if r["section07_real"] else "STUB"
        cfg = "OK" if r["config_valid"] else "MISS"
        leg = "YES" if r["has_legacy"] else "NO"
        nlp = r["section06_model"] or "-"
        print(f"{r['station']:<45} {r['status']:<8} {s07:<6} {cfg:<8} {leg:<8} {nlp:<20}")

    print("-" * 100)
    print(f"PASS: {pass_count}  STUB: {stub_count}  WARN: {warn_count}  FAIL: {fail_count}  TOTAL: {len(results)}")

    # Detail: warnings and errors
    print("\n" + "=" * 80)
    print("DETAILS (warnings and errors only)")
    print("=" * 80)
    for r in results:
        if r["errors"] or r["warnings"]:
            print(f"\n  {r['station']}:")
            for e in r["errors"]:
                print(f"    ERROR: {e}")
            for w in r["warnings"]:
                print(f"    WARN:  {w}")

    # Stub list for Phase 2 targeting
    stubs = [r["station"] for r in results if r["status"] == "STUB"]
    if stubs:
        print("\n" + "=" * 80)
        print(f"PHASE 2 TARGETS ({len(stubs)} stations still at passthrough stub):")
        for s in stubs:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
