from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from _shared.canon_index import main_for_station


DEFAULT_SOURCES = [
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\JUSTICE_MERCY_OPERATOR.md",
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\GRACE_OPERATOR.md",
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\GRACE_IN_THE_DATA.md",
]


if __name__ == "__main__":
    raise SystemExit(main_for_station("operators-canon", DEFAULT_SOURCES))
