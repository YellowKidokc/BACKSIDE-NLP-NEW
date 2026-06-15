from __future__ import annotations

from collections import deque
from pathlib import Path


def tail_lines(path: Path, lines: int = 200) -> list[str]:
    if not path.exists() or lines <= 0:
        return []
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        return [line.rstrip("\n") for line in deque(fh, maxlen=lines)]
