from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def ensure_dirs() -> None:
    for name in ["INPUT", "OUTPUT", "REVIEW", "ARCHIVE", "ERROR", "CONFIG", "PROMPTS", "SCRIPTS", "LOGS"]:
        (ROOT / name).mkdir(exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["pipeline", "stage"], default="stage")
    parser.add_argument("--input", help="Article file to run through the FAP manufacturing line.")
    parser.add_argument("--skip-paper-grader", action="store_true")
    args = parser.parse_args()
    ensure_dirs()
    inputs = sorted((ROOT / "INPUT").glob("*"))
    target = Path(args.input) if args.input else (inputs[0] if inputs else None)
    log = ROOT / "LOGS" / "last_run.log"
    if not target:
        log.write_text(f"mode={args.mode}\ninputs=0\nstatus=no-input\n", encoding="utf-8")
        print(f"{ROOT.name}: no input found. Put a file in INPUT or pass --input.")
        return 2
    command = [
        sys.executable,
        str(ROOT / "SCRIPTS" / "run_article_manufacturing_line.py"),
        "--input",
        str(target),
    ]
    if args.skip_paper_grader:
        command.append("--skip-paper-grader")
    result = subprocess.run(command, capture_output=True, text=True)
    log.write_text(
        "\n".join(
            [
                f"mode={args.mode}",
                f"inputs={len(inputs)}",
                f"target={target}",
                f"command={' '.join(command)}",
                f"returncode={result.returncode}",
                "stdout:",
                result.stdout,
                "stderr:",
                result.stderr,
            ]
        ),
        encoding="utf-8",
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
