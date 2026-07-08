from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from _shared.canon_index import main_for_station


DEFAULT_SOURCES = [
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\00_FORMAL_THEORY_COMPLETE.md",
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\OLD canonical\MASTER_TEST_STACK.md",
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\OLD canonical\FORMAL_LAYER_PART1.md",
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\OLD canonical\AXIOM_DERIVATION_CHAIN_CANONICAL.md",
]


if __name__ == "__main__":
    raise SystemExit(main_for_station("master-equation-canon", DEFAULT_SOURCES))
