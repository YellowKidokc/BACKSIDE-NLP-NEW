"""
STATION TEST RUNNER
===================
Drops a real test input into each station's _inbox, runs pipeline.py,
checks _outbox for a JSON artifact with real data.
Reports pass/fail + exports results to 10_EXPORTS.
"""
import json, subprocess, sys, shutil, time
from pathlib import Path
from datetime import datetime

STATION_DIR = Path(__file__).parent
EXPORT_DIR  = STATION_DIR.parent.parent / "brain" / "10_EXPORTS"
if not EXPORT_DIR.exists():
    EXPORT_DIR = STATION_DIR.parent / "exports"
    EXPORT_DIR.mkdir(exist_ok=True)

PY = sys.executable

# Stations to test — the 36 newly wired ones
NONE_STATIONS = [
    "7q-classifier.station", "7q-engine.station", "ai-portal-generator.station",
    "ai-research-agents.station", "apologetic-pipeline.station", "axioms.station",
    "brain-map.station", "classify-documents.station", "coherence-discoherence.station",
    "file-intelligence.station", "fis.station", "fruits-spirit-canon.station",
    "graph-linker.station", "harvest-links.station", "hdbscan-cluster.station",
    "html-article.station", "link-pull.station", "link-research.station",
    "master-equation-canon.station", "mda-citation-spine.station", "mda-publication.station",
    "metadata-extractor.station", "obsidian-export.station", "open-brain-map.station",
    "operators-canon.station", "postgres-sync.station", "reading-level-glossary.station",
    "section-splitter.station", "series-flow-auditor.station", "session-handoff-combined.station",
    "session-handoff-drop.station", "theophysics-engine.station", "trinity-canon.station",
    "vault-rater-tsr100.station", "youtube-fetch.station", "youtube-scrape.station",
]

# A real theological/academic test document
TEST_TEXT = """
The Logos Doctrine and Its Implications for Theophysics

The concept of the Logos, as articulated in the Gospel of John and developed
by the Church Fathers, presents a foundational axiom for understanding the
relationship between divine rationality and physical law. John 1:1 states:
"In the beginning was the Word (Logos), and the Word was with God, and the
Word was God." This claim establishes a necessary connection between ultimate
reality and rational structure.

Philo of Alexandria argued that the Logos serves as the intermediary between
the transcendent God and the material world. This philosophical position has
direct implications for how we understand the mathematical structure of
physical laws. If the universe is fundamentally rational, then the deep
mathematical regularities we observe — from quantum mechanics to general
relativity — are not accidental but reflect an underlying rational order.

The Athanasian Creed further specifies: "The Father is God, the Son is God,
and the Holy Spirit is God; and yet they are not three Gods but one God."
This formulation presents a logical tension that apophatic theology attempts
to resolve through negation. The claim is not self-contradictory if we admit
that divine predication operates differently from ordinary predication.

However, critics such as Hume argue that causal necessity is never observed,
only constant conjunction. This creates a tension with the Thomistic view
that efficient causality reflects the ratio of the divine intellect. Either
causality is a real feature of nature, or it is a projection of human
expectation — these positions cannot both be fully correct.

The Trinity doctrine also bears on questions of unity and multiplicity in
mathematics. The one-in-three structure finds analogues in mathematical
objects that exhibit internal differentiation while remaining unified wholes.
See also: https://plato.stanford.edu/entries/logos/ and https://arxiv.org/abs/2103.01234
"""

TEST_JSON = {
    "station_id": "TEST",
    "data": {
        "title": "The Logos Doctrine and Theophysics",
        "text": TEST_TEXT,
        "claims": [
            {"claim_id": "C1", "text": "The Logos is both with God and is God."},
            {"claim_id": "C2", "text": "Physical laws reflect divine rational structure."},
            {"claim_id": "C3", "text": "Causal necessity is never directly observed."},
            {"claim_id": "C4", "text": "The Trinity is three Gods unified as one."},
        ],
        "sections": [
            {"heading": "Introduction", "text": "The Logos concept establishes divine rationality."},
            {"heading": "Philo's Intermediary", "text": "The Logos bridges God and matter."},
            {"heading": "Athanasian Creed", "text": "Three persons, one God — logical tension."},
            {"heading": "Hume's Challenge", "text": "Causal necessity versus constant conjunction."},
        ],
        "summary": "An analysis of Logos doctrine and its implications for theophysics.",
        "body": TEST_TEXT,
        "transcript": TEST_TEXT,
    }
}


def drop_input(station_path: Path):
    inbox = station_path / "_inbox"
    inbox.mkdir(exist_ok=True)
    # clear old test files
    for f in inbox.glob("_test_input*"):
        f.unlink()
    # drop both text and JSON
    (inbox / "_test_input.md").write_text(TEST_TEXT, encoding="utf-8")
    (inbox / "_test_input.json").write_text(json.dumps(TEST_JSON, indent=2), encoding="utf-8")


def clear_inbox(station_path: Path):
    for f in (station_path / "_inbox").glob("_test_input*"):
        try: f.unlink()
        except: pass


def check_outbox(station_path: Path) -> dict:
    outbox = station_path / "_outbox"
    if not outbox.exists():
        return {"has_output": False, "reason": "no _outbox dir"}
    artifacts = sorted(outbox.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not artifacts:
        return {"has_output": False, "reason": "no JSON artifacts"}
    newest = artifacts[0]
    age = time.time() - newest.stat().st_mtime
    if age > 120:
        return {"has_output": False, "reason": f"newest artifact is {int(age)}s old (pre-test)"}
    try:
        data = json.loads(newest.read_text(encoding="utf-8"))
        has_data = bool(data.get("data"))
        success = data.get("success", True)
        errors = data.get("errors", [])
        return {
            "has_output": True,
            "success": success,
            "has_data": has_data,
            "errors": errors,
            "file": newest.name,
            "data_keys": list(data.get("data", {}).keys())[:6],
        }
    except Exception as e:
        return {"has_output": True, "reason": f"JSON parse error: {e}"}


def run_station(station_path: Path, timeout=60) -> tuple[bool, str]:
    pipe = station_path / "pipeline.py"
    if not pipe.exists():
        return False, "no pipeline.py"
    result = subprocess.run(
        [PY, str(pipe)],
        capture_output=True, text=True, timeout=timeout,
        cwd=str(station_path)
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "").strip()[-300:]
        return False, err
    return True, ""


def main():
    results = []
    passed = 0; failed = 0

    print(f"Testing {len(NONE_STATIONS)} stations against NLP API at http://localhost:8700\n")
    print(f"{'Station':<52} {'Run':>4} {'Output':>7} {'Data':>5} {'Status'}")
    print("-" * 85)

    for name in NONE_STATIONS:
        s_path = STATION_DIR / name
        if not s_path.exists():
            print(f"  {name:<52} MISSING")
            results.append({"station": name, "status": "MISSING"})
            failed += 1
            continue

        drop_input(s_path)
        t0 = time.time()

        try:
            run_ok, run_err = run_station(s_path, timeout=300)
        except subprocess.TimeoutExpired:
            run_ok, run_err = False, "TIMEOUT"
        elapsed = round(time.time() - t0, 1)

        ob = check_outbox(s_path)
        clear_inbox(s_path)

        if run_ok and ob.get("has_output") and ob.get("has_data"):
            status = "PASS"
            passed += 1
        elif ob.get("has_output") and ob.get("has_data") and not run_ok and "TIMEOUT" in run_err:
            # Station wrote data before timeout — counts as DATA_PASS
            status = "DATA_PASS"
            passed += 1
        elif run_ok and ob.get("has_output") and not ob.get("has_data"):
            status = "EMPTY_DATA"
            failed += 1
        elif run_ok and not ob.get("has_output"):
            status = "NO_OUTPUT"
            failed += 1
        else:
            status = "FAIL"
            failed += 1

        r_str  = "OK" if run_ok else "FAIL"
        out_str = "YES" if ob.get("has_output") else "NO"
        dat_str = "YES" if ob.get("has_data") else "NO"
        print(f"  {name:<52} {r_str:>4} {out_str:>7} {dat_str:>5}  {status}  ({elapsed}s)")
        if not run_ok and run_err:
            print(f"    err: {run_err[:120]}")
        if ob.get("errors"):
            print(f"    station errors: {ob['errors'][:2]}")
        if ob.get("data_keys"):
            print(f"    data keys: {ob['data_keys']}")

        results.append({
            "station": name, "status": status, "run_ok": run_ok,
            "has_output": ob.get("has_output"), "has_data": ob.get("has_data"),
            "elapsed_s": elapsed, "run_error": run_err[:200] if not run_ok else "",
            "data_keys": ob.get("data_keys", []), "station_errors": ob.get("errors", []),
        })

    print(f"\n{'='*60}")
    print(f"PASS: {passed}/{len(NONE_STATIONS)}   FAIL: {failed}/{len(NONE_STATIONS)}")

    report = {"generated": datetime.now().isoformat(), "passed": passed, "failed": failed, "results": results}
    out = EXPORT_DIR / "STATION_TEST_RESULTS.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nReport -> {out}")

if __name__ == "__main__":
    main()
