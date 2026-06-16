"""
paper_scorecard.py
Roll a paper's station results + paper-grader output into a single scorecard.

Inputs:
  X:\\knowledge-refinery\\13_SOURCE_SYSTEMS\\FAP\\_queue\\completed\\<jobid>\\*.result.json
  X:\\knowledge-refinery\\13_SOURCE_SYSTEMS\\FAP\\graded\\<jobid>\\paper-proof-grader-run-*.json
  X:\\knowledge-refinery\\13_SOURCE_SYSTEMS\\FAP\\output\\<jobid>\\job_manifest.json

Outputs:
  <output_root>/<jobid>/scorecard.json
  <output_root>/<jobid>/scorecard.md
  <output_root>/<jobid>/stations/<station>.result.json  (copies, for portability)

Score formula:
  station_score   = pass*1.0 + review*0.5 - fail*1.0
  grader_score    = normalized grader weighted_score, 0..1 range, defaults 0.5
  combined_score  = (grader_score * 10) + station_score

Usage:
  python paper_scorecard.py <jobid> [--out <batch-dir>]
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from glob import glob
from pathlib import Path


FAP_ROOT = Path(r"X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP")
COMPLETED_ROOT = FAP_ROOT / "_queue" / "completed"
GRADED_ROOT = FAP_ROOT / "graded"
OUTPUT_ROOT_FAP = FAP_ROOT / "output"
DEFAULT_BATCH_ROOT = Path(r"X:\knowledge-refinery\full_workflow\output")


def load_station_results(jobid: str) -> list[dict]:
    job_dir = COMPLETED_ROOT / jobid
    if not job_dir.exists():
        return []
    results = []
    for p in sorted(job_dir.glob("*.result.json")):
        try:
            results.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception as e:
            results.append({"station": p.stem, "error": str(e)})
    return results


def load_grader(jobid: str) -> dict | None:
    paths = sorted(glob(str(GRADED_ROOT / jobid / "paper-proof-grader-run-*.json")))
    if not paths:
        return None
    try:
        data = json.loads(Path(paths[-1]).read_text(encoding="utf-8"))
    except Exception:
        return None
    if isinstance(data, list) and data:
        return data[0]
    if isinstance(data, dict):
        return data
    return None


def load_job_manifest(jobid: str) -> dict | None:
    p = OUTPUT_ROOT_FAP / jobid / "job_manifest.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def station_tallies(station_results: list[dict]) -> dict:
    tallies = {"PASS": 0, "REVIEW": 0, "FAIL": 0}
    for s in station_results:
        status = (s.get("result") or {}).get("status", "REVIEW")
        if status in tallies:
            tallies[status] += 1
    return tallies


def station_score(tallies: dict) -> float:
    return tallies["PASS"] * 1.0 + tallies["REVIEW"] * 0.5 - tallies["FAIL"] * 1.0


def grader_normalized(grader: dict | None) -> tuple[float, dict]:
    """Pull a 0..1 score plus the raw stats. Defaults to 0.5 if absent."""
    if not grader:
        return 0.5, {}
    metrics = grader.get("metrics") or {}

    # The grader doesn't always emit a single weighted score; build one from metrics.
    # Use claim_candidate_count, equation_count, section_count as positive signals.
    claims = float(metrics.get("claim_candidate_count") or 0)
    eqs = float(metrics.get("equation_count") or 0)
    sections = float(metrics.get("section_count") or 0)
    words = float(metrics.get("word_count") or 0)

    # crude normalization — caps each component at a sane ceiling
    score = (
        min(claims, 30) / 30 * 0.4
        + min(eqs, 20) / 20 * 0.3
        + min(sections, 12) / 12 * 0.2
        + min(words, 5000) / 5000 * 0.1
    )
    return round(min(max(score, 0.0), 1.0), 3), metrics


def build_scorecard(jobid: str) -> dict:
    station_results = load_station_results(jobid)
    grader = load_grader(jobid)
    manifest = load_job_manifest(jobid)
    tallies = station_tallies(station_results)
    s_score = station_score(tallies)
    g_score, g_metrics = grader_normalized(grader)
    combined = round(g_score * 10 + s_score, 2)

    # title from manifest source path
    title = "(unknown)"
    if grader:
        title = grader.get("paper_id") or grader.get("title") or title
    if manifest:
        src = manifest.get("source", "")
        if src and title == "(unknown)":
            title = Path(src.replace("\\\\", "\\")).stem

    return {
        "schema_version": "fap.scorecard.v1",
        "jobid": jobid,
        "title": title,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "station_tallies": tallies,
        "station_count": len(station_results),
        "station_score": round(s_score, 2),
        "grader_score_normalized": g_score,
        "grader_metrics": g_metrics,
        "combined_score": combined,
        "stations": [
            {
                "station": s.get("station"),
                "status": (s.get("result") or {}).get("status"),
                "evidence_count": len((s.get("result") or {}).get("evidence") or []),
                "blocker_count": len((s.get("result") or {}).get("blockers") or []),
                "elapsed_sec": (s.get("ollama_meta") or {}).get("elapsed_sec"),
            }
            for s in station_results
        ],
    }


def render_markdown(scorecard: dict, station_results: list[dict]) -> str:
    lines = [
        f"# Scorecard — {scorecard['title']}",
        "",
        f"- Job: `{scorecard['jobid']}`",
        f"- Generated: {scorecard['generated_at']}",
        f"- **Combined score: {scorecard['combined_score']}**",
        f"- Station score: {scorecard['station_score']}  "
        f"(PASS={scorecard['station_tallies']['PASS']}, "
        f"REVIEW={scorecard['station_tallies']['REVIEW']}, "
        f"FAIL={scorecard['station_tallies']['FAIL']})",
        f"- Grader (normalized): {scorecard['grader_score_normalized']}",
        "",
        "## Grader metrics",
        "",
    ]
    for k, v in (scorecard.get("grader_metrics") or {}).items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Stations", "", "| Station | Status | Evidence | Blockers | Sec |", "|---|---|---:|---:|---:|"]
    for s in scorecard["stations"]:
        lines.append(
            f"| {s['station']} | {s['status']} | {s['evidence_count']} | {s['blocker_count']} | {s['elapsed_sec'] or '-'} |"
        )
    lines += ["", "## Station outputs", ""]
    for sr in station_results:
        r = sr.get("result") or {}
        lines += [
            f"### {sr.get('station')} — {r.get('status', '?')}",
            "",
            (r.get("output") or "(empty)").strip(),
            "",
        ]
        if r.get("evidence"):
            lines.append("**Evidence:**")
            lines.append("")
            for e in r["evidence"]:
                lines.append(f"- `{e['paragraph_id']}` — {e.get('quote','')}")
            lines.append("")
        if r.get("blockers"):
            lines.append("**Blockers:**")
            lines.append("")
            for b in r["blockers"]:
                lines.append(f"- {b}")
            lines.append("")
    return "\n".join(lines)


def write_scorecard(jobid: str, out_root: Path) -> Path:
    out_dir = out_root / jobid
    out_dir.mkdir(parents=True, exist_ok=True)

    station_results = load_station_results(jobid)
    scorecard = build_scorecard(jobid)

    json_path = out_dir / "scorecard.json"
    json_path.write_text(json.dumps(scorecard, indent=2, ensure_ascii=False), encoding="utf-8")

    md = render_markdown(scorecard, station_results)
    (out_dir / "scorecard.md").write_text(md, encoding="utf-8")

    # mirror station results for self-contained output
    stations_dir = out_dir / "stations"
    stations_dir.mkdir(exist_ok=True)
    for p in (COMPLETED_ROOT / jobid).glob("*.result.*"):
        try:
            shutil.copy2(str(p), str(stations_dir / p.name))
        except Exception:
            pass

    return json_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("jobid", help="Job id (folder name from FAP output)")
    ap.add_argument(
        "--out",
        default=str(DEFAULT_BATCH_ROOT),
        help="Output root (default: full_workflow/output)",
    )
    args = ap.parse_args()
    out = write_scorecard(args.jobid, Path(args.out))
    print(f"Scorecard written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
