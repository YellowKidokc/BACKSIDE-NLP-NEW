from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from PySide6.QtWidgets import QLabel, QPushButton, QTextBrowser, QVBoxLayout, QWidget

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    from PySide6.QtCore import QUrl
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False


class CommsTab(QWidget):
    def __init__(self, settings: Any | None = None) -> None:
        super().__init__()
        self.settings = settings
        self.unread_count = 0
        self._build_ui()
        self.refresh()

    def hub_url(self) -> str:
        configured = ""
        if self.settings is not None:
            configured = self.settings.config.get("comms", "hub_url", fallback="")
        return os.environ.get("COMMS_HUB") or configured or "https://comms.dlowehomelab.com"

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        refresh = QPushButton("Refresh")
        refresh.clicked.connect(self.refresh)
        layout.addWidget(refresh)
        if WEBENGINE_AVAILABLE:
            self.view = QWebEngineView()
            layout.addWidget(self.view)
        else:
            self.view = QTextBrowser()
            layout.addWidget(QLabel("QWebEngineView unavailable; showing local cache."))
            layout.addWidget(self.view)

    def refresh(self) -> None:
        if WEBENGINE_AVAILABLE:
            self.view.load(QUrl(self.hub_url()))
            return
        cache = Path(os.environ.get("THEOPHYSICS_VAULT", "")) / "comms_cache.md"
        if cache.exists():
            self.view.setMarkdown(cache.read_text(encoding="utf-8", errors="replace"))
        else:
            self.view.setPlainText("Comms hub offline and no local cache found.")
