from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
import uuid

import keyboard
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from core.data_store import JsonStore


@dataclass
class ClipboardEntry:
    id: str
    text: str
    created_at: str
    pinned: bool = False
    tags: list[str] = field(default_factory=list)
    hotkey: str = ""

    def label(self) -> str:
        prefix = "[PIN] " if self.pinned else ""
        tags = f" #{' #'.join(self.tags)}" if self.tags else ""
        return f"{prefix}{self.text[:90].replace(chr(10), ' ')}{tags}"


class ClipboardTab(QWidget):
    def __init__(self, bil_client: Any | None = None, store_path: Path | None = None) -> None:
        super().__init__()
        self.bil_client = bil_client
        self.store = JsonStore(store_path or Path(__file__).resolve().parents[2] / "config" / "clips.json")
        self.entries: list[ClipboardEntry] = []
        self.aggregate_mode = False
        self._last_text = ""
        self._build_ui()
        self._load_store()
        self._register_slot_hotkeys()
        QApplication.clipboard().dataChanged.connect(self._on_clipboard_changed)

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        header = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search clipboard")
        self.search.textChanged.connect(self._refresh)
        header.addWidget(self.search)
        self.aggregate = QCheckBox("Aggregate copy mode")
        self.aggregate.toggled.connect(self._set_aggregate)
        header.addWidget(self.aggregate)
        layout.addLayout(header)

        splitter = QSplitter(Qt.Horizontal)
        self.history = QListWidget()
        self.history.currentItemChanged.connect(self._preview_selected)
        splitter.addWidget(self.history)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        self.preview = QTextEdit()
        right_layout.addWidget(self.preview)
        buttons = QHBoxLayout()
        for label, handler in [
            ("Copy", self._copy_selected),
            ("Pin", self._pin_selected),
            ("Tag", self._tag_selected),
            ("Up", lambda: self._move_selected(-1)),
            ("Down", lambda: self._move_selected(1)),
            ("Clear", self._clear_unpinned),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            buttons.addWidget(btn)
        right_layout.addLayout(buttons)
        splitter.addWidget(right)
        splitter.setSizes([450, 550])
        layout.addWidget(splitter)
        self.status = QLabel("Ready")
        layout.addWidget(self.status)

    def _on_clipboard_changed(self) -> None:
        text = QApplication.clipboard().text()
        if not text or text == self._last_text:
            return
        self._last_text = text
        if self.aggregate_mode and self.entries:
            self.entries[0].text = f"{self.entries[0].text}\n{text}"
        else:
            self.entries.insert(0, ClipboardEntry(str(uuid.uuid4()), text, datetime.now().isoformat(timespec="seconds")))
        self.entries = self.entries[:200]
        self._save_store()
        self._post_copy(text)
        self._refresh()

    def _post_copy(self, text: str) -> None:
        if self.bil_client:
            self.bil_client.post_event("/bil/clipboard", {
                "event_type": "copied_text",
                "text": text,
                "signal_weight": 0.8,
                "created_at": datetime.now().isoformat(timespec="seconds"),
            })

    def _register_slot_hotkeys(self) -> None:
        keys = [str(i) for i in range(1, 10)] + ["0"]
        for idx, key in enumerate(keys):
            keyboard.add_hotkey(f"ctrl+shift+{key}", lambda i=idx: self._copy_slot(i))
            keyboard.add_hotkey(f"ctrl+alt+{key}", lambda i=idx + 10: self._copy_slot(i))

    def _refresh(self) -> None:
        query = self.search.text().lower().strip()
        self.history.clear()
        for entry in self.entries:
            if query and query not in entry.text.lower() and not any(query in tag.lower() for tag in entry.tags):
                continue
            item = QListWidgetItem(entry.label())
            item.setData(Qt.UserRole, entry.id)
            self.history.addItem(item)
        self.status.setText(f"{len(self.entries)} clipboard items")

    def _selected_entry(self) -> ClipboardEntry | None:
        item = self.history.currentItem()
        if not item:
            return None
        entry_id = item.data(Qt.UserRole)
        return next((entry for entry in self.entries if entry.id == entry_id), None)

    def _preview_selected(self) -> None:
        entry = self._selected_entry()
        self.preview.setPlainText(entry.text if entry else "")

    def _copy_selected(self) -> None:
        entry = self._selected_entry()
        if entry:
            QApplication.clipboard().setText(entry.text)

    def _copy_slot(self, index: int) -> None:
        if 0 <= index < len(self.entries):
            QApplication.clipboard().setText(self.entries[index].text)

    def copy_slot(self, index: int) -> None:
        self._copy_slot(index)

    def _pin_selected(self) -> None:
        entry = self._selected_entry()
        if entry:
            entry.pinned = not entry.pinned
            self.entries.sort(key=lambda item: (not item.pinned, item.created_at), reverse=False)
            self._save_store()
            self._refresh()

    def _tag_selected(self) -> None:
        entry = self._selected_entry()
        if not entry:
            return
        tags, ok = QInputDialog.getText(self, "Tags", "Comma-separated tags:", text=", ".join(entry.tags))
        if ok:
            entry.tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
            self._save_store()
            self._refresh()

    def _move_selected(self, delta: int) -> None:
        entry = self._selected_entry()
        if not entry:
            return
        old = self.entries.index(entry)
        new = max(0, min(len(self.entries) - 1, old + delta))
        self.entries.insert(new, self.entries.pop(old))
        self._save_store()
        self._refresh()

    def _clear_unpinned(self) -> None:
        if QMessageBox.question(self, "Clear", "Clear all unpinned clipboard entries?") == QMessageBox.Yes:
            self.entries = [entry for entry in self.entries if entry.pinned]
            self._save_store()
            self._refresh()

    def _set_aggregate(self, checked: bool) -> None:
        self.aggregate_mode = checked

    def _load_store(self) -> None:
        self.entries = [
            ClipboardEntry(
                id=str(item.get("id") or uuid.uuid4()),
                text=str(item.get("text") or item.get("content") or ""),
                created_at=str(item.get("created_at") or datetime.now().isoformat(timespec="seconds")),
                pinned=bool(item.get("pinned", False)),
                tags=list(item.get("tags", [])) if isinstance(item.get("tags", []), list) else [],
                hotkey=str(item.get("hotkey", "")),
            )
            for item in self.store.all()
            if item.get("text") or item.get("content")
        ]
        self._refresh()

    def _save_store(self) -> None:
        self.store.replace_all([
            {
                "id": entry.id,
                "text": entry.text,
                "created_at": entry.created_at,
                "pinned": entry.pinned,
                "tags": entry.tags,
                "hotkey": entry.hotkey,
            }
            for entry in self.entries
        ])
