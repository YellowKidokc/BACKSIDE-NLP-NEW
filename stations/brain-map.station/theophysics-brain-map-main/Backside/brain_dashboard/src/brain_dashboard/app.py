from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .main_window import MainWindow


def run_app(headless_smoke_test: bool = False) -> int:
    app = QApplication(sys.argv)
    icon_path = Path(__file__).resolve().parents[2] / "assets" / "icon.svg"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    state_path = Path("intake_engine/state.json")
    logs_dir = Path("_LOGS")

    window = MainWindow(state_path=state_path, logs_dir=logs_dir)
    window.show()

    if headless_smoke_test:
        QTimer.singleShot(5000, app.quit)
    return app.exec()
