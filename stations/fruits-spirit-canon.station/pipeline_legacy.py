#!/usr/bin/env python3
r"""
run_fruits_engine.py — wired launcher for fruits_coherence_engine.py

Station wiring (so the engine stays portable but exports land in one place):
  * INPUT   : a path passed on the command line, else everything in DROP_HERE\
  * LEXICON : auto-discovered from LEXICON\ (newest *.xlsx, names containing
              "lexicon" preferred), unless you pass --lexicon PATH
  * OUTPUT  : EXPORTS\fruits_reports\run_<timestamp>\  (always station-root EXPORTS)
  * XLSX    : always on

Examples:
  RUN_FRUITS_ENGINE.bat                         # score everything in DROP_HERE
  RUN_FRUITS_ENGINE.bat "X:\\path\\paper.md"      # score one file/folder
  RUN_FRUITS_ENGINE.bat --lexicon "my_lex.xlsx" # force a specific lexicon
  RUN_FRUITS_ENGINE.bat --context-window 70     # passthrough engine option

Nothing here changes the engine's analysis logic; it only sets paths by
convention so new lexicons/inputs route themselves without editing code.
"""
from __future__ import annotations

import sys
import os
from datetime import datetime
from pathlib import Path

STATION = Path(__file__).resolve().parent
DROP_HERE = STATION / "DROP_HERE"
LEXICON_DIR = STATION / "LEXICON"
EXPORTS_ROOT = STATION / "EXPORTS" / "fruits_reports"
CANONICAL_LEXICON = Path(os.environ.get(
    "PAPER_GRADER_LEXICON_XLSX",
    r"\\dlowenas\HPWorkstation\Desktop\paper_grader_lexicons_master_enhanced.xlsx",
))

sys.path.insert(0, str(STATION))
import fruits_coherence_engine as engine  # noqa: E402


def find_lexicon(*dirs: Path) -> Path | None:
    """Newest .xlsx across the given dirs; prefer filenames containing 'lexicon'."""
    candidates: list[Path] = []
    for d in dirs:
        if d and d.is_dir():
            candidates += [p for p in d.glob("*.xlsx") if not p.name.startswith("~$")]
    if not candidates:
        return None
    preferred = [c for c in candidates if "lexicon" in c.name.lower()]
    pool = preferred or candidates
    return max(pool, key=lambda p: p.stat().st_mtime)


def main() -> int:
    raw = sys.argv[1:]

    # Pull the few options we care about; everything else is treated as the input path.
    input_path: str | None = None
    lexicon: str | None = None
    context_window: str | None = None
    i = 0
    while i < len(raw):
        arg = raw[i]
        if arg == "--lexicon" and i + 1 < len(raw):
            lexicon = raw[i + 1]; i += 2; continue
        if arg == "--context-window" and i + 1 < len(raw):
            context_window = raw[i + 1]; i += 2; continue
        if not arg.startswith("-"):
            input_path = arg; i += 1; continue
        i += 1  # ignore unknown flags

    if input_path is None:
        input_path = str(DROP_HERE)

    # Friendly guard: nothing to score.
    in_p = Path(input_path)
    if in_p.is_dir():
        has_files = any(
            p.is_file() and p.suffix.lower() in {".md", ".txt", ".html", ".htm"}
            for p in in_p.rglob("*")
        )
        if not has_files:
            print(f"[fruits-engine] No .md/.txt/.html files found in {in_p}")
            print(f"[fruits-engine] Drop papers into {DROP_HERE} (or pass a path) and re-run.")
            return 0
    elif not in_p.exists():
        print(f"[fruits-engine] Input not found: {in_p}")
        return 2

    if lexicon is None:
        found = find_lexicon(LEXICON_DIR, STATION)
        if found:
            lexicon = str(found)
        elif CANONICAL_LEXICON.exists():
            lexicon = str(CANONICAL_LEXICON)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = EXPORTS_ROOT / f"run_{stamp}"

    engine_argv = [input_path, "--outdir", str(outdir), "--xlsx"]
    if lexicon:
        engine_argv += ["--lexicon", lexicon]
    if context_window:
        engine_argv += ["--context-window", context_window]

    print(f"[fruits-engine] input   = {input_path}")
    print(f"[fruits-engine] lexicon = {lexicon or 'built-in only (drop an .xlsx in LEXICON\\ to enrich)'}")
    print(f"[fruits-engine] outdir  = {outdir}")

    sys.argv = ["fruits_coherence_engine.py"] + engine_argv
    return engine.main()


if __name__ == "__main__":
    raise SystemExit(main())
