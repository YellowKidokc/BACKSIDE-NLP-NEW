#!/usr/bin/env python3
"""
Container entrypoint for Theophysics Paper Intelligence.

Mount papers into /data/input and write outputs to /data/output.
The deterministic grader is local. The 7Q/snapshot layer can call an Ollama
server through OLLAMA_URL, usually http://host.docker.internal:11434/api/generate.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = Path("/data/input")
DEFAULT_OUTPUT = Path("/data/output")


def run(cmd: list[str], env: dict[str, str] | None = None) -> int:
    print("\n$ " + " ".join(str(part) for part in cmd), flush=True)
    completed = subprocess.run(cmd, cwd=str(ROOT), env=env)
    return completed.returncode


def find_papers(input_dir: Path, pattern: str) -> list[Path]:
    papers = sorted(input_dir.glob(pattern))
    return [p for p in papers if p.is_file()]


def load_orchestrator():
    orchestrator_path = ROOT / "00_ORCHESTRATOR" / "run_pipeline.py"
    spec = importlib.util.spec_from_file_location("theophysics_run_pipeline", orchestrator_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load orchestrator: {orchestrator_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def layer_health(rows: list[dict]) -> dict:
    counts: dict[str, dict[str, int]] = {}
    for row in rows:
        for layer, status in row.get("_layer_status", {}).items():
            counts.setdefault(layer, {"ok": 0, "error": 0, "skipped": 0})
            counts[layer][status] = counts[layer].get(status, 0) + 1
    return counts


def grade_series(input_dir: Path, output_dir: Path, pattern: str, openai: bool = False) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    papers = find_papers(input_dir, pattern)
    if not papers:
        print(f"No papers matched {pattern!r} under {input_dir}", flush=True)
        return 2

    orchestrator = load_orchestrator()
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    series_id = f"SERIES-{hashlib.sha1(str(input_dir).lower().encode('utf-8')).hexdigest()[:10]}"
    snapshot_dir = output_dir / "snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for index, paper in enumerate(papers, 1):
        print(f"\n[{index}/{len(papers)}] deterministic grade: {paper.name}", flush=True)
        row = orchestrator.analyze_paper(
            str(paper),
            run_openai=openai,
            vault_output=str(output_dir),
            series_id=series_id,
            run_id=run_id,
            snapshot_dir=str(snapshot_dir),
            identity_overrides={"series": input_dir.name},
        )
        rows.append(row)

    json_path = output_dir / f"paper_intelligence_rows_{run_id}.json"
    json_path.write_text(json.dumps(rows, indent=2, default=str), encoding="utf-8")
    print(f"\nRows JSON: {json_path}", flush=True)

    if getattr(orchestrator, "HAS_EXCEL", False):
        excel_path = output_dir / f"paper_intelligence_master_{run_id}.xlsx"
        orchestrator.write_excel(rows, excel_path)
        print(f"Excel: {excel_path}", flush=True)
    else:
        print("Excel skipped: openpyxl unavailable in this environment", flush=True)

    summary = {
        "schema_version": getattr(orchestrator, "SCHEMA_VERSION", ""),
        "run_id": run_id,
        "series_id": series_id,
        "input_dir": str(input_dir),
        "pattern": pattern,
        "paper_count": len(rows),
        "openai_enabled": bool(openai),
        "layer_health": layer_health(rows),
        "papers": [
            {"paper_id": row.get("paper_id"), "file": row.get("file"), "status": row.get("_layer_status", {})}
            for row in rows
        ],
    }
    summary_path = output_dir / f"paper_intelligence_summary_{run_id}.json"
    summary_path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(f"Summary: {summary_path}", flush=True)
    return 0


def run_ollama_7q(
    input_dir: Path,
    output_dir: Path,
    pattern: str,
    model: str,
    sections: str,
    head: int,
    tail: int,
    timeout: int,
    classic_tokens: int,
    section_tokens: int,
) -> int:
    papers = find_papers(input_dir, pattern)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, str | int]] = []

    if not papers:
        print(f"No papers matched {pattern!r} under {input_dir}", flush=True)
        return 2

    env = os.environ.copy()
    for index, paper in enumerate(papers, 1):
        print(f"\n[{index}/{len(papers)}] 7Q snapshot: {paper.name}", flush=True)
        cmd = [
            sys.executable,
            str(ROOT / "04_OPENAI_7Q" / "ollama_7q_runner.py"),
            "--paper",
            str(paper),
            "--output",
            str(output_dir),
            "--model",
            model,
            "--sections",
            sections,
            "--head",
            str(head),
            "--tail",
            str(tail),
            "--timeout",
            str(timeout),
            "--classic-tokens",
            str(classic_tokens),
            "--section-tokens",
            str(section_tokens),
        ]
        rc = run(cmd, env=env)
        manifest.append({"paper": paper.name, "return_code": rc})
        if rc != 0:
            print(f"Stopping after failed paper: {paper}", flush=True)
            break

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest_path = output_dir / f"ollama_7q_manifest_{stamp}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\n7Q manifest: {manifest_path}", flush=True)
    return 0 if all(item["return_code"] == 0 for item in manifest) else 1


def write_schema_copy(output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    schema = ROOT / "schema" / "schema_concept_system.sql"
    if not schema.exists():
        print(f"Schema not found: {schema}", flush=True)
        return 1
    target = output_dir / "schema_concept_system.sql"
    target.write_text(schema.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Schema copied to {target}", flush=True)
    return 0


def generate_html_report(json_path: Path | None, output_dir: Path, single: bool = False) -> int:
    if json_path is None:
        candidates = sorted((output_dir / "grader").glob("paper_intelligence_rows_*.json"))
        if not candidates:
            print("No grader JSON found. Run `grade` first or pass --json.", flush=True)
            return 2
        json_path = candidates[-1]

    report_dir = output_dir / "html_reports"
    cmd = [
        sys.executable,
        str(ROOT / "11_HTML_REPORT" / "generate_report.py"),
        "--json",
        str(json_path),
        "--output",
        str(report_dir),
    ]
    if single:
        cmd.append("--single")
    return run(cmd)


def main() -> int:
    parser = argparse.ArgumentParser(description="Theophysics Paper Intelligence Docker entrypoint")
    parser.add_argument("command", choices=["grade", "7q", "all", "schema", "report"], help="What to run")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Folder containing HTML/Markdown/text papers")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Folder for generated outputs")
    parser.add_argument("--json", default=None, help="Pipeline JSON to render as HTML report")
    parser.add_argument("--pattern", default="*.html", help="Paper file glob for 7Q batch runs")
    parser.add_argument("--openai", action="store_true", help="Use paid OpenAI L4 in deterministic pipeline")
    parser.add_argument("--single", action="store_true", help="Generate one combined HTML report when supported")
    parser.add_argument("--model", default=os.environ.get("OLLAMA_MODEL", "qwen2.5:3b"))
    parser.add_argument("--sections", default="classic,snapshot")
    parser.add_argument("--head", type=int, default=1800)
    parser.add_argument("--tail", type=int, default=400)
    parser.add_argument("--timeout", type=int, default=210)
    parser.add_argument("--classic-tokens", type=int, default=950)
    parser.add_argument("--section-tokens", type=int, default=1100)
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.command == "schema":
        return write_schema_copy(output_dir)
    if args.command == "report":
        return generate_html_report(Path(args.json) if args.json else None, output_dir, single=args.single)
    if args.command == "grade":
        return grade_series(input_dir, output_dir / "grader", pattern=args.pattern, openai=args.openai)
    if args.command == "7q":
        return run_ollama_7q(
            input_dir,
            output_dir / "ollama_7q",
            args.pattern,
            args.model,
            args.sections,
            args.head,
            args.tail,
            args.timeout,
            args.classic_tokens,
            args.section_tokens,
        )
    if args.command == "all":
        rc = grade_series(input_dir, output_dir / "grader", pattern=args.pattern, openai=args.openai)
        if rc != 0:
            return rc
        return run_ollama_7q(
            input_dir,
            output_dir / "ollama_7q",
            args.pattern,
            args.model,
            args.sections,
            args.head,
            args.tail,
            args.timeout,
            args.classic_tokens,
            args.section_tokens,
        )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
