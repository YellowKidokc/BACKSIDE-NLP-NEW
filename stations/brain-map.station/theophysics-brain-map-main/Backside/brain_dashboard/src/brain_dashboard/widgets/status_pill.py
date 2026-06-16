from PySide6.QtWidgets import QLabel

COLOR_MAP = {
    "healthy": "#2e7d32",
    "queued": "#f9a825",
    "errored": "#c62828",
    "idle": "#6b7280",
}


class StatusPill(QLabel):
    def set_status(self, status: str) -> None:
        color = COLOR_MAP.get(status, COLOR_MAP["idle"])
        self.setText(status.upper())
        self.setStyleSheet(f"background:{color}; color:white; border-radius:8px; padding:2px 8px;")
