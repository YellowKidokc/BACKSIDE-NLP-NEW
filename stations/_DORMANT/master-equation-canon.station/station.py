from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from _shared.canon_index import main_for_station


# Sources relocated 2026-06: the old "OLD canonical\" folder was reorganized
# into "LEAN4\canonical\" (exact-same filenames). 00_FORMAL_THEORY_COMPLETE.md
# remains at the Cannon root. Override at runtime with --source if needed.
# NOTE for David: FORMAL_LAYER now has a PART2.md alongside PART1 — add it here
# if the formal-layer index should cover both parts.
DEFAULT_SOURCES = [
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\00_FORMAL_THEORY_COMPLETE.md",
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\LEAN4\canonical\MASTER_TEST_STACK.md",
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\LEAN4\canonical\FORMAL_LAYER_PART1.md",
    r"\\dlowenas\HPWorkstation\Desktop\Cannon\LEAN4\canonical\AXIOM_DERIVATION_CHAIN_CANONICAL.md",
]


if __name__ == "__main__":
    raise SystemExit(main_for_station("master-equation-canon", DEFAULT_SOURCES))
