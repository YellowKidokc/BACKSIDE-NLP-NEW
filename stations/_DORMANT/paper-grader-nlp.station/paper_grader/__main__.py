"""Local (no-Docker) entry point for the paper-grader-nlp station.

This station does not reimplement grading. It drives the proven, pure-stdlib
``paper-proof-grader`` engine against this station's own local INPUT / EXPORTS /
ARCHIVE folders. The engine path is resolved from STATION_REGISTRY.json (the
single source of truth) with a sibling-folder fallback.

Usage:
    python -m paper_grader            # grade everything in .\\INPUT
    set PAPER_GRADER_INPUT=...        # optional dir overrides (env)
    set PAPER_GRADER_OUTPUT=...
    set PAPER_GRADER_ARCHIVE=...
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATION = HERE.parent
STATIONS_ROOT = STATION.parent
REGISTRY = STATIONS_ROOT / "STATION_REGISTRY.json"


def _resolve_engine() -> Path:
    """Locate the paper-proof-grader engine folder."""
    candidates: list[Path] = []
    if REGISTRY.exists():
        try:
            reg = json.loads(REGISTRY.read_text(encoding="utf-8-sig"))
            entry = reg.get("stations", {}).get("paper-proof-grader", {})
            if entry.get("path"):
                candidates.append(Path(entry["path"]))
        except Exception as exc:  # noqa: BLE001 - registry is advisory
            print(f"[paper-grader-nlp] could not read registry: {exc}")
    candidates.append(STATIONS_ROOT / "paper-proof-grader.station")

    for path in candidates:
        if (path / "pipeline.py").is_file():
            return path
    raise SystemExit(
        "[paper-grader-nlp] engine not found. Expected paper-proof-grader.station "
        "with pipeline.py (checked registry + sibling folder)."
    )


def _mirror_exports(output_dir: Path) -> None:
    """Copy run artifacts into typed root EXPORTS folders for easy pickup."""
    typed_dirs = {
        ".xlsx": STATION / "EXPORTS" / "excel",
        ".xls": STATION / "EXPORTS" / "excel",
        ".csv": STATION / "EXPORTS" / "csv",
        ".json": STATION / "EXPORTS" / "json",
        ".html": STATION / "EXPORTS" / "html",
        ".htm": STATION / "EXPORTS" / "html",
        ".md": STATION / "EXPORTS" / "reports",
    }
    for path in output_dir.rglob("*"):
        if not path.is_file():
            continue
        target_dir = typed_dirs.get(path.suffix.lower(), STATION / "EXPORTS" / "source_copies")
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / f"paper_grade_runs_{path.name}"
        shutil.copy2(path, target)


def main() -> int:
    input_dir = Path(os.environ.get("PAPER_GRADER_INPUT", STATION / "INPUT"))
    output_dir = Path(os.environ.get("PAPER_GRADER_OUTPUT", STATION / "EXPORTS" / "paper_grade_runs"))
    archive_dir = Path(os.environ.get("PAPER_GRADER_ARCHIVE", STATION / "ARCHIVE"))
    for path in (input_dir, output_dir, archive_dir):
        path.mkdir(parents=True, exist_ok=True)

    engine = _resolve_engine()
    print(f"[paper-grader-nlp] engine: {engine}")
    print(f"[paper-grader-nlp] input:  {input_dir}")
    print(f"[paper-grader-nlp] output: {output_dir}")

    # Import the engine and point it at this station's local folders.
    sys.path.insert(0, str(engine))
    import pipeline  # noqa: E402 - path is set up above

    pipeline.CFG["input_dir"] = str(input_dir)
    pipeline.CFG["output_dir"] = str(output_dir)
    pipeline.CFG["archive_dir"] = str(archive_dir)
    pipeline.CFG.pop("report_dir", None)  # don't mirror into the engine's exports
    # Core pipeline is pure-stdlib; ensure no network sinks are assumed on.
    for key in ("qdrant", "embedding"):
        if isinstance(pipeline.CFG.get(key), dict):
            pipeline.CFG[key]["enabled"] = False

    rc = pipeline.main()

    # Roll every paper's metrics up onto one Excel sheet.
    try:
        from paper_grader.consolidate_metrics import consolidate

        consolidate(output_dir)
    except Exception as exc:  # noqa: BLE001 - consolidation is a bonus, never fatal
        print(f"[paper-grader-nlp] consolidation skipped: {exc}")

    try:
        _mirror_exports(output_dir)
    except Exception as exc:  # noqa: BLE001 - mirror is non-fatal, report clearly
        print(f"[paper-grader-nlp] export mirror skipped: {exc}")

    return rc


if __name__ == "__main__":
    raise SystemExit(main())
