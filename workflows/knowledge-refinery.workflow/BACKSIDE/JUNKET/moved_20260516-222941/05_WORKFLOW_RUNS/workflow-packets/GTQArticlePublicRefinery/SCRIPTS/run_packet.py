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
    args = parser.parse_args()
    ensure_dirs()
    inputs = sorted((ROOT / "INPUT").glob("*"))
    command = [
        sys.executable,
        str(ROOT / "SCRIPTS" / "run_refinery.py"),
        "--input",
        str(ROOT / "INPUT"),
        "--output",
        str(ROOT / "OUTPUT"),
        "--review",
        str(ROOT / "REVIEW"),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    log = ROOT / "LOGS" / "last_run.log"
    log.write_text(
        "\n".join(
            [
                f"mode={args.mode}",
                f"inputs={len(inputs)}",
                f"command={' '.join(command)}",
                f"returncode={result.returncode}",
                "stdout:",
                result.stdout.strip(),
                "stderr:",
                result.stderr.strip(),
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(result.stdout.strip())
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
