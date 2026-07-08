from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from _shared.canon_index import main_for_station


DEFAULT_SOURCES = [
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\Resurrection_CLEAN.md",
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\MAXWELL_TRINITY_FORMAL_LOG_2026-05-10.md",
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\MAXWELL_TRINITY_LEAN_SPEC.md",
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\IsomorphismTest.lean",
]


if __name__ == "__main__":
    raise SystemExit(main_for_station("trinity-canon", DEFAULT_SOURCES))
