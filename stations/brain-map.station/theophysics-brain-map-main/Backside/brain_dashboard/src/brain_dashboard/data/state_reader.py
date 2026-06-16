from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"engine": {}, "nlps": {}, "errors": []}
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def nlp_cards(state: dict[str, Any]) -> list[dict[str, Any]]:
    nlps = state.get("nlps", {})
    cards = []
    for name, payload in nlps.items():
        runs = payload.get("recent_runs", [])
        last = runs[0] if runs else {}
        cards.append(
            {
                "name": name,
                "status": payload.get("status", "idle"),
                "queue_depth": payload.get("queue_depth", 0),
                "last_run": last,
                "trend": [r.get("exit_code", 0) for r in runs[:10]],
            }
        )
    return cards
