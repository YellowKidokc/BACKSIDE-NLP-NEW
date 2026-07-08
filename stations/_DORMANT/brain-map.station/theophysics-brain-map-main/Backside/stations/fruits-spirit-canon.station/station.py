from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from _shared.canon_index import main_for_station


DEFAULT_SOURCES = [
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\FRUITS_OF_SPIRIT.md",
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\fruits_of_the_spirit_equations.md",
]


if __name__ == "__main__":
    raise SystemExit(main_for_station("fruits-spirit-canon", DEFAULT_SOURCES))
