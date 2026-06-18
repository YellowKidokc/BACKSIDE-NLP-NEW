#!/usr/bin/env python
"""
smoke_test.py - One-command demo/test harness for the Theophysics Brain stations.

Because every station is SSS_v1 (same _inbox/_outbox, same pipeline.py entry, same
artifact envelope), one runner can test them all the same way:

  1. ensure the NLP service is up (start it if not)
  2. for each station: wipe its folders, drop the SAME demo input, run pipeline.py
  3. read the newest _outbox artifact, check success == true AND data is non-empty
  4. print a PASS/FAIL table

Same demo every run -> results are comparable over time.

Usage:
  python smoke_test.py                       # the Core 8 pipeline stations
  python smoke_test.py --all                 # every station that has a pipeline.py
  python smoke_test.py exec-summary claim-classification   # named stations
"""
import json, subprocess, sys, time, urllib.request
from pathlib import Path

REPO        = Path(__file__).resolve().parent
STATIONS    = REPO / "stations"
SERVICE_DIR = REPO / "nlp_api"
PY          = sys.executable                 # run stations under THIS interpreter
HEALTH      = "http://localhost:8700/health"

CORE8 = ["exec-summary", "plain-language", "claim-extraction", "claim-classification",
         "load-bearing-claims", "falsification", "evidence-map", "contradiction-scan"]

DEMO = """# The Physics of Coherence

Coherence is the degree to which a system's parts stay aligned under stress. In
thermodynamics a coherent system resists entropy by holding internal correlations that
would otherwise decay.

## Claim
Shared truth lowers internal drift. As drift rises, the channel capacity for meaning
collapses and the system decoheres toward disorder. We model social decline the same way.

## Evidence
Measured coherence tracks stability across physical and social systems, which suggests a
single underlying law rather than a loose analogy.
"""

def service_up() -> bool:
    try:
        with urllib.request.urlopen(HEALTH, timeout=5) as r:
            return json.load(r).get("status") == "ok"
    except Exception:
        return False

def ensure_service() -> bool:
    if service_up():
        return True
    print("NLP service down -> starting it...")
    subprocess.Popen([PY, "main.py"], cwd=str(SERVICE_DIR),
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):
        time.sleep(2)
        if service_up():
            print("  service up.")
            return True
    print("  service did NOT come up.")
    return False

def clean(station: Path) -> None:
    for sub in ("_inbox", "_outbox", "_logs", "_state", "_processed"):
        d = station / sub
        if d.exists():
            for f in d.glob("*"):
                if f.is_file() and f.name != ".gitkeep":
                    f.unlink()

def run_station(name: str) -> dict:
    station = STATIONS / f"{name}.station"
    if not (station / "pipeline.py").exists():
        return {"station": name, "status": "SKIP", "secs": "", "note": "no pipeline.py"}
    clean(station)
    (station / "_inbox").mkdir(exist_ok=True)
    (station / "_inbox" / "demo.md").write_text(DEMO, encoding="utf-8")
    t0 = time.time()
    try:
        p = subprocess.run([PY, "pipeline.py"], cwd=str(station),
                           capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return {"station": name, "status": "FAIL", "secs": round(time.time()-t0, 1), "note": "timeout (180s)"}
    dt = round(time.time() - t0, 1)
    arts = sorted((station / "_outbox").glob("ART_*.json"), key=lambda f: f.stat().st_mtime)
    if not arts:
        tail = (p.stderr or p.stdout or "").strip().splitlines()
        return {"station": name, "status": "FAIL", "secs": dt,
                "note": (tail[-1][:60] if tail else f"no artifact, rc={p.returncode}")}
    art = json.loads(arts[-1].read_text(encoding="utf-8"))
    data = art.get("data") or {}
    ok = bool(art.get("success")) and bool(data)
    if ok:
        note = "data: " + ",".join(list(data.keys())[:4])
    else:
        errs = art.get("errors") or []
        note = "errors: " + (errs[0][:55] if errs else "empty data")
    return {"station": name, "status": "PASS" if ok else "FAIL", "secs": dt, "note": note}

def main(argv) -> int:
    if "--all" in argv:
        names = sorted(d.name[:-8] for d in STATIONS.glob("*.station") if (d / "pipeline.py").exists())
    elif len(argv) > 1:
        names = argv[1:]
    else:
        names = CORE8

    if not ensure_service():
        print("Aborting: NLP service unavailable.")
        return 1

    print(f"\nSmoke test: {len(names)} stations | same demo input each\n" + "=" * 70)
    results = [run_station(n) for n in names]
    print(f"{'STATION':26} {'RESULT':6} {'SECS':>6}  NOTE")
    print("-" * 70)
    for r in results:
        print(f"{r['station']:26} {r['status']:6} {str(r.get('secs','')):>6}  {r.get('note','')}")
    print("=" * 70)
    n_pass = sum(1 for r in results if r["status"] == "PASS")
    n_skip = sum(1 for r in results if r["status"] == "SKIP")
    print(f"{n_pass}/{len(results) - n_skip} passed" + (f" ({n_skip} skipped)" if n_skip else ""))
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
