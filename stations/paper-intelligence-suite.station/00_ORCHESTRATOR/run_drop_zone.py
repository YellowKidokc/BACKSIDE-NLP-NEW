from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SUITE_DIR = HERE.parent

if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from run_brain_alignment import run_alignment, run_brain_only, run_paper_only  # noqa: E402


def _slugify(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    return cleaned[:80] or "source"


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")


def _iter_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current_root, dir_names, file_names in os.walk(root):
        dir_names[:] = [d for d in dir_names if d.lower() not in {".git", ".obsidian", "__pycache__", "node_modules"}]
        base = Path(current_root)
        for file_name in file_names:
            if file_name.lower().endswith(".md"):
                files.append(base / file_name)
    return sorted(files)


def _read_fetch_source(path: Path) -> str:
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped.strip("\"'")
    return ""


def _resolve_input(zone_dir: Path) -> dict[str, Any]:
    inbox = zone_dir / "INBOX"
    inbox.mkdir(parents=True, exist_ok=True)
    inbox_markdown = _iter_markdown_files(inbox)
    if inbox_markdown:
        return {
            "mode": "inbox",
            "kind": "folder",
            "path": inbox,
            "markdown_count": len(inbox_markdown),
        }

    fetch_value = _read_fetch_source(zone_dir / "FETCH_SOURCE.txt")
    if not fetch_value:
        raise FileNotFoundError(
            f"No markdown files found in {inbox} and FETCH_SOURCE.txt is empty.",
        )

    source = Path(fetch_value).expanduser()
    if not source.exists():
        raise FileNotFoundError(f"FETCH_SOURCE.txt points to a missing path: {source}")

    if source.is_dir():
        markdown = _iter_markdown_files(source)
        return {
            "mode": "fetch-folder",
            "kind": "folder",
            "path": source,
            "markdown_count": len(markdown),
        }

    if source.is_file():
        return {
            "mode": "fetch-file",
            "kind": "file",
            "path": source,
            "markdown_count": 1 if source.suffix.lower() == ".md" else 0,
        }

    raise ValueError(f"Unsupported source path: {source}")


def _stage_file(file_path: Path, run_dir: Path) -> Path:
    staged_dir = run_dir / "WORKING_SOURCE"
    staged_dir.mkdir(parents=True, exist_ok=True)
    target = staged_dir / file_path.name
    shutil.copy2(file_path, target)
    return staged_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Autonomous drop-zone runner for Paper Intelligence / Brain Arm / Alignment.",
    )
    parser.add_argument("--zone", required=True, help="Drop-zone folder path.")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["paper", "brain", "both"],
        help="Which autonomous pipeline to run.",
    )
    parser.add_argument("--openai", action="store_true", help="Enable OpenAI-backed layers where supported.")
    args = parser.parse_args()

    zone_dir = Path(args.zone).resolve()
    runs_dir = zone_dir / "RUNS"
    runs_dir.mkdir(parents=True, exist_ok=True)

    input_info = _resolve_input(zone_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    source_name = input_info["path"].stem if input_info["kind"] == "file" else input_info["path"].name
    run_dir = runs_dir / f"{args.mode}_{_slugify(source_name)}_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    if input_info["kind"] == "file":
        working_source = _stage_file(input_info["path"], run_dir)
    else:
        working_source = input_info["path"]

    output_dir = run_dir / "OUTPUT"
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "paper":
        result = run_paper_only(
            folder_path=str(working_source),
            output_path=str(output_dir),
            run_openai=args.openai,
        )
    elif args.mode == "brain":
        result = run_brain_only(
            folder_path=str(working_source),
            output_path=str(output_dir),
        )
    else:
        result = run_alignment(
            folder_path=str(working_source),
            output_path=str(output_dir),
            run_openai=args.openai,
        )

    manifest = {
        "zone_dir": str(zone_dir),
        "mode": args.mode,
        "openai_enabled": args.openai,
        "input": {
            "source_mode": input_info["mode"],
            "kind": input_info["kind"],
            "original_path": str(input_info["path"]),
            "working_source": str(working_source),
            "markdown_count": input_info["markdown_count"],
        },
        "run_dir": str(run_dir),
        "output_dir": str(output_dir),
        "result": result,
    }
    manifest_path = run_dir / "run_manifest.json"
    _write_json(manifest_path, manifest)

    print(json.dumps({
        "status": "ok",
        "mode": args.mode,
        "run_dir": str(run_dir),
        "manifest": str(manifest_path),
        "result_summary": result,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
