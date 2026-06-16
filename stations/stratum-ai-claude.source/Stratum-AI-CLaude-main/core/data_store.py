from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


def read_json(path: Path, default: Any) -> Any:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        pass
    return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


class JsonStore:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def all(self) -> list[dict[str, Any]]:
        data = read_json(self.path, [])
        if isinstance(data, dict):
            for key in ("items", "clips", "prompts", "bookmarks", "tasks"):
                if isinstance(data.get(key), list):
                    return data[key]
            return []
        return data if isinstance(data, list) else []

    def replace_all(self, items: list[dict[str, Any]]) -> None:
        write_json(self.path, items)

    def add(self, item: dict[str, Any]) -> dict[str, Any]:
        items = self.all()
        new_item = dict(item)
        new_item.setdefault("id", str(uuid.uuid4()))
        new_item.setdefault("created_at", datetime.now().isoformat(timespec="seconds"))
        items.insert(0, new_item)
        self.replace_all(items)
        return new_item

    def update(self, item_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
        items = self.all()
        for item in items:
            if str(item.get("id")) == str(item_id):
                item.update(patch)
                self.replace_all(items)
                return item
        return None

    def delete(self, item_id: str) -> bool:
        items = self.all()
        kept = [item for item in items if str(item.get("id")) != str(item_id)]
        if len(kept) == len(items):
            return False
        self.replace_all(kept)
        return True
