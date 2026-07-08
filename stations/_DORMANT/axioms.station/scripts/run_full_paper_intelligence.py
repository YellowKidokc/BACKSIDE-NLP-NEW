from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


DEFAULT_SUITE = Path(r"X:\apps\paper-intelligence-suite-python")
DEFAULT_OUTPUT_ROOT = Path(__file__).resolve().parents[1] / "07_FULL_PAPER_INTELLIGENCE"


def resolve_python() -> str:
    # Prefer the caller Python. The suite-local venv may exist but be only
    # partially hydrated; the active system Python has the verified stack.
    candidates = [
        Path(sys.executable),
        Path(r"C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe"),
        Path(r"C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe"),
        Path(r"C:\Users\lowes\AppData\Local\Programs\Python\Python311\python.exe"),
        DEFAULT_SUITE / ".venv" / "Scripts" / "python.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return "python"


def slugify(value: str) -> str:
    import re

    return re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()[:90] or "paper"


def run_command(cmd: list[str], cwd: Path) -> int:
    print("RUN:", " ".join(f'"{part}"' if " " in part else part for part in cmd))
    process = subprocess.run(cmd, cwd=str(cwd), text=True)
    return int(process.returncode)


def summarize_output(run_dir: Path) -> dict:
    latest_json = sorted(run_dir.glob("*_pipeline_results_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    latest_xlsx = sorted(run_dir.glob("*_PAPER_INTELLIGENCE_*.xlsx"), key=lambda p: p.stat().st_mtime, reverse=True)
    summary: dict = {
        "run_dir": str(run_dir),
        "pipeline_json": str(latest_json[0]) if latest_json else None,
        "workbook": str(latest_xlsx[0]) if latest_xlsx else None,
        "column_count": None,
        "layer_status": None,
    }
    if latest_json:
        rows = json.loads(latest_json[0].read_text(encoding="utf-8"))
        row = rows[0] if rows else {}
        summary["column_count"] = len(row)
        summary["layer_status"] = row.get("_layer_status")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Axioms workflow bridge to the full Paper Intelligence suite."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--paper", type=Path, help="Single .md/.txt/.html paper to score.")
    group.add_argument("--series", type=Path, help="Folder of papers to score as a series.")
    parser.add_argument("--suite-root", type=Path, default=DEFAULT_SUITE)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--openai", action="store_true", help="Enable OpenAI 7Q / peer review layers.")
    parser.add_argument("--copy-input", action="store_true", help="Copy the input paper/folder into the run folder for provenance.")
    args = parser.parse_args()

    suite_root = args.suite_root
    pipeline = suite_root / "00_ORCHESTRATOR" / "run_pipeline.py"
    if not pipeline.exists():
        raise FileNotFoundError(pipeline)

    source = (args.paper or args.series).resolve()
    if not source.exists():
        raise FileNotFoundError(source)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"{slugify(source.stem if source.is_file() else source.name)}-{stamp}"
    run_dir = args.output_root / run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    if args.copy_input:
        provenance_dir = run_dir / "source_input"
        provenance_dir.mkdir(parents=True, exist_ok=True)
        if source.is_file():
            shutil.copy2(source, provenance_dir / source.name)
        else:
            target = provenance_dir / source.name
            if target.exists():
                raise FileExistsError(target)
            shutil.copytree(source, target)

    cmd = [
        resolve_python(),
        str(pipeline),
        "--paper" if args.paper else "--series",
        str(source),
        "--output",
        str(run_dir),
    ]
    if args.openai:
        cmd.append("--openai")

    rc = run_command(cmd, suite_root)
    summary = summarize_output(run_dir)
    summary["ok"] = rc == 0
    summary["return_code"] = rc
    summary["source"] = str(source)
    summary["openai_enabled"] = args.openai
    manifest = run_dir / "full_paper_intelligence_bridge_manifest.json"
    manifest.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
