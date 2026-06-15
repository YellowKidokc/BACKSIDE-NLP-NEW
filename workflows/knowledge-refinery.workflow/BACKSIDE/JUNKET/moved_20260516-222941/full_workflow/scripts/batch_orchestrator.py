"""
batch_orchestrator.py
End-to-end runner for full_workflow.

Sequence:
  1. (optional) For each file in intake, run FAP article pipeline -> jobid in output/
  2. station_runner.process_job(jobid) for each jobid -> _queue/completed/<jobid>/
  3. paper_scorecard.write_scorecard(jobid) -> batch/<jobid>/scorecard.{json,md}
  4. production_html.write_draft(jobid) -> batch/<jobid>/production-draft.html
  5. treaties_handoff.write_handoff(jobid) -> batch/<jobid>/treaties-handoff.json
  6. Build batch_index.{json,md} sorted by combined_score descending

A batch is a single run identified by timestamp. The script always creates one new batch
folder. Existing _queue/completed entries from prior runs are reused (not regenerated) —
to force re-run, delete the completed dir for that jobid first.

Usage:
  python batch_orchestrator.py                                 # process all pending jobs
  python batch_orchestrator.py --intake "<dir>"               # FAP-process files in dir first
  python batch_orchestrator.py --paper <jobid>                # single jobid
  python batch_orchestrator.py --skip-fap                     # no new FAP runs; use existing jobids
  python batch_orchestrator.py --no-html                      # skip draft HTML
  python batch_orchestrator.py --no-treaties                  # skip Treaties handoff package
"""
from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
ROOT = THIS_DIR.parent
sys.path.insert(0, str(THIS_DIR))

import station_runner  # noqa: E402
import paper_scorecard  # noqa: E402
import production_html  # noqa: E402
import treaties_handoff  # noqa: E402

FAP_ROOT = Path(r"X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP")
FAP_OUTPUT = FAP_ROOT / "output"
FAP_INTAKE = FAP_ROOT / "intake"
RUN_FAP_BAT = Path(r"X:\knowledge-refinery\RUN_FAP_ARTICLE_PIPELINE.bat")
FAP_PS1 = Path(r"X:\knowledge-refinery\scripts\run_fap_article_pipeline.ps1")

BATCH_ROOT = ROOT / "output"
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / f"orchestrator_{datetime.now():%Y%m%d-%H%M%S}.log",
            encoding="utf-8",
        ),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("orchestrator")


def list_intake_files(intake: Path) -> list[Path]:
    if not intake.exists():
        return []
    exts = {".html", ".htm", ".md", ".txt"}
    return sorted(
        f for f in intake.iterdir()
        if f.is_file() and f.suffix.lower() in exts and not f.name.startswith(("_", "."))
    )


def latest_jobid_for_source(source_path: Path) -> str | None:
    """Find the most recent FAP output jobid whose manifest references this source."""
    if not FAP_OUTPUT.exists():
        return None
    src_norm = str(source_path).lower()
    candidates = []
    for d in FAP_OUTPUT.iterdir():
        if not d.is_dir():
            continue
        mf = d / "job_manifest.json"
        if not mf.exists():
            continue
        try:
            manifest = json.loads(mf.read_text(encoding="utf-8"))
        except Exception:
            continue
        ms = (manifest.get("source") or "").lower().replace("\\\\", "\\")
        if src_norm in ms or Path(ms).name == source_path.name:
            candidates.append((mf.stat().st_mtime, d.name))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def run_fap(source: Path) -> str | None:
    """Invoke the existing FAP pipeline PS1 for one source. Returns the new jobid or None."""
    log.info("FAP: %s", source.name)
    if not FAP_PS1.exists():
        log.error("FAP PS1 missing: %s", FAP_PS1)
        return None
    cmd = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(FAP_PS1),
        "-InputPath",
        str(source),
    ]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=600, check=False
        )
    except subprocess.TimeoutExpired:
        log.error("FAP timed out for %s", source)
        return None
    if proc.returncode != 0:
        log.error("FAP returncode=%s for %s\n%s", proc.returncode, source, proc.stderr[-500:])
        return None
    return latest_jobid_for_source(source)


def list_pending_jobids() -> list[str]:
    return station_runner.list_pending_jobids()


def list_output_jobids() -> list[str]:
    if not FAP_OUTPUT.exists():
        return []
    return sorted(d.name for d in FAP_OUTPUT.iterdir() if d.is_dir())


def build_batch_index(batch_dir: Path, scorecards: list[dict]) -> tuple[Path, Path]:
    scorecards = sorted(
        scorecards, key=lambda s: s.get("combined_score", 0), reverse=True
    )
    index = {
        "schema_version": "fap.batch_index.v1",
        "batch_id": batch_dir.name,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "paper_count": len(scorecards),
        "papers": scorecards,
    }
    json_path = batch_dir / "batch_index.json"
    json_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    md = [
        f"# Batch index — {batch_dir.name}",
        "",
        f"Generated: {index['generated_at']}  ·  Papers: {len(scorecards)}",
        "",
        "Sorted by combined score (highest = most production-ready).",
        "",
        "| Rank | Score | Title | Job | PASS | REVIEW | FAIL |",
        "|---:|---:|---|---|---:|---:|---:|",
    ]
    for i, s in enumerate(scorecards, 1):
        t = s.get("station_tallies") or {}
        md.append(
            f"| {i} | {s.get('combined_score')} | {s.get('title','?')} | "
            f"`{s.get('jobid')}` | {t.get('PASS',0)} | {t.get('REVIEW',0)} | {t.get('FAIL',0)} |"
        )
    md += ["", "## Files per paper", ""]
    for s in scorecards:
        jid = s.get("jobid", "")
        md += [
            f"### {s.get('title','?')}",
            "",
            f"- `output/{batch_dir.name}/{jid}/scorecard.md`",
            f"- `output/{batch_dir.name}/{jid}/scorecard.json`",
            f"- `output/{batch_dir.name}/{jid}/production-draft.html`",
            f"- `output/{batch_dir.name}/{jid}/stations/`",
            "",
        ]
    md_path = batch_dir / "batch_index.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    return json_path, md_path


def ollama_health() -> bool:
    return station_runner.health_check()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--intake", help="Process files from a custom intake dir through FAP first")
    ap.add_argument("--paper", help="Single jobid (skip FAP, skip intake walk)")
    ap.add_argument("--skip-fap", action="store_true", help="Do not run FAP; use pending+completed jobids")
    ap.add_argument("--no-html", action="store_true", help="Skip draft HTML render")
    ap.add_argument("--no-treaties", action="store_true", help="Skip Treaties/proof-explorer handoff package")
    args = ap.parse_args()

    if not ollama_health():
        log.error("Ollama not reachable. Start it via RUN_OLLAMA.bat or `ollama serve`.")
        return 1

    batch_id = datetime.now().strftime("batch-%Y%m%d-%H%M%S")
    batch_dir = BATCH_ROOT / batch_id
    batch_dir.mkdir(parents=True, exist_ok=True)
    log.info("Batch: %s", batch_id)
    log.info("Output dir: %s", batch_dir)

    # Step 1: optional FAP feed
    targets: list[str] = []
    if args.paper:
        targets = [args.paper]
    elif args.skip_fap:
        # use everything that has either pending station requests OR a FAP output dir
        targets = sorted(set(list_pending_jobids()) | set(list_output_jobids()))
    else:
        intake_dir = Path(args.intake) if args.intake else FAP_INTAKE
        intake_files = list_intake_files(intake_dir)
        if intake_files:
            log.info("Feeding %d file(s) into FAP from %s", len(intake_files), intake_dir)
            for src in intake_files:
                jid = run_fap(src)
                if jid:
                    targets.append(jid)
                    log.info("  -> jobid %s", jid)
                else:
                    log.warning("  -> failed: %s", src)
        else:
            log.info("Intake empty; processing existing pending+output jobids.")
            targets = sorted(set(list_pending_jobids()) | set(list_output_jobids()))

    if not targets:
        log.error("No targets found.")
        return 2

    log.info("Targets: %s", ", ".join(targets))

    # Step 2: stations per paper
    for jid in targets:
        try:
            station_runner.process_job(jid)
        except Exception as e:
            log.error("Station runner failed for %s: %s", jid, e)

    # Step 3 + 4: scorecard + draft HTML
    scorecards: list[dict] = []
    for jid in targets:
        try:
            paper_scorecard.write_scorecard(jid, batch_dir)
            sc = json.loads((batch_dir / jid / "scorecard.json").read_text(encoding="utf-8"))
            scorecards.append(sc)
            log.info("Scorecard: %s combined=%s", jid, sc.get("combined_score"))
        except Exception as e:
            log.error("Scorecard failed for %s: %s", jid, e)
            continue
        if not args.no_html:
            try:
                production_html.write_draft(jid, batch_dir)
                log.info("Draft HTML: %s", jid)
            except Exception as e:
                log.error("HTML render failed for %s: %s", jid, e)
        if not args.no_treaties:
            try:
                local_handoff, queue_handoff = treaties_handoff.write_handoff(jid, batch_dir)
                log.info("Treaties handoff: %s -> %s", local_handoff, queue_handoff)
            except Exception as e:
                log.error("Treaties handoff failed for %s: %s", jid, e)

    # Step 6: batch index
    json_idx, md_idx = build_batch_index(batch_dir, scorecards)
    log.info("Batch index: %s", md_idx)

    # promote to "latest" pointer
    latest = BATCH_ROOT / "_LATEST.txt"
    latest.write_text(batch_id + "\n", encoding="utf-8")

    log.info("=" * 60)
    log.info("BATCH DONE: %s", batch_id)
    log.info(
        "%d paper(s). Top: %s",
        len(scorecards),
        scorecards[0].get("title") if scorecards else "(none)",
    )
    log.info("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
