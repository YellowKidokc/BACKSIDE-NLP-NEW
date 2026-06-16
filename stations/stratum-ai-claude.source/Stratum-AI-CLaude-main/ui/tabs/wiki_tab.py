from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QTextBrowser, QVBoxLayout, QWidget


class WikiTab(QWidget):
    def __init__(self, settings: Any | None = None) -> None:
        super().__init__()
        self.settings = settings
        self.files: list[Path] = []
        self._build_ui()
        self._load_files()

    def wiki_root(self) -> Path:
        configured = ""
        if self.settings is not None:
            configured = self.settings.config.get("forge", "vault_path", fallback="")
        vault = Path(os.environ.get("THEOPHYSICS_VAULT") or configured or r"O:\_Theophysics_v4")
        return vault / "wiki"

    def _build_ui(self) -> None:
        layout = QHBoxLayout(self)
        left = QVBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search wiki")
        self.search.textChanged.connect(self._filter)
        left.addWidget(self.search)
        self.list_widget = QListWidget()
        self.list_widget.currentItemChanged.connect(self._open_current)
        left.addWidget(self.list_widget)
        layout.addLayout(left, 1)
        self.viewer = QTextBrowser()
        self.viewer.anchorClicked.connect(lambda url: self._navigate(url.toString()))
        layout.addWidget(self.viewer, 3)

    def _load_files(self) -> None:
        root = self.wiki_root()
        self.files = sorted(root.rglob("*.md")) if root.exists() else []
        self._filter("")

    def _filter(self, text: str) -> None:
        query = text.lower().strip()
        self.list_widget.clear()
        for path in self.files:
            rel = path.relative_to(self.wiki_root()).as_posix()
            if not query or query in rel.lower():
                item = QListWidgetItem(rel)
                item.setData(Qt.UserRole, str(path))
                self.list_widget.addItem(item)

    def _open_current(self) -> None:
        item = self.list_widget.currentItem()
        if item:
            self._open_path(Path(item.data(Qt.UserRole)))

    def _open_path(self, path: Path) -> None:
        try:
            self.viewer.setMarkdown(path.read_text(encoding="utf-8", errors="replace"))
        except OSError as exc:
            self.viewer.setPlainText(f"Could not open {path}: {exc}")

    def _navigate(self, href: str) -> None:
        target = href.strip().strip("[]")
        if not target:
            return
        if not target.endswith(".md"):
            target += ".md"
        matches = [path for path in self.files if path.name.lower() == target.lower()]
        if matches:
            self._open_path(matches[0])
