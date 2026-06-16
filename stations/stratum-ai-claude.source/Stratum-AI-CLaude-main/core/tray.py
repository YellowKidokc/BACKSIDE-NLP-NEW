from __future__ import annotations

from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon


class ForgeTrayIcon(QSystemTrayIcon):
    def __init__(self, app: QApplication, window, pipeline_tab=None, comms_tab=None) -> None:
        icon = app.style().standardIcon(QStyle.SP_ComputerIcon)
        super().__init__(icon)
        self.app = app
        self.window = window
        self.pipeline_tab = pipeline_tab
        self.comms_tab = comms_tab
        self.setToolTip("FORGE - 0 packets in flight, 0 in review")
        self.activated.connect(self._on_activated)
        self._build_menu()

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_tooltip)
        self.timer.start(5000)
        self.refresh_tooltip()

    def _build_menu(self) -> None:
        menu = QMenu()
        show_action = QAction("Show")
        show_action.triggered.connect(self.show_window)
        menu.addAction(show_action)

        pipeline_action = QAction("Pipeline Status")
        pipeline_action.triggered.connect(lambda: self._show_tab("Pipeline"))
        menu.addAction(pipeline_action)

        comms_action = QAction("Comms")
        comms_action.triggered.connect(lambda: self._show_tab("Comms"))
        menu.addAction(comms_action)

        settings_action = QAction("Settings")
        settings_action.triggered.connect(lambda: self._show_tab("Settings"))
        menu.addAction(settings_action)

        menu.addSeparator()
        quit_action = QAction("Quit")
        quit_action.triggered.connect(self._quit)
        menu.addAction(quit_action)
        self.setContextMenu(menu)

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()

    def show_window(self) -> None:
        self.window.showNormal()
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

    def _show_tab(self, name: str) -> None:
        self.show_window()
        for i in range(self.window.tab_widget.count()):
            if self.window.tab_widget.tabText(i) == name:
                self.window.tab_widget.setCurrentIndex(i)
                break

    def refresh_tooltip(self) -> None:
        in_flight = getattr(self.pipeline_tab, "in_flight_count", lambda: 0)()
        review = getattr(self.pipeline_tab, "review_count", lambda: 0)()
        self.setToolTip(f"FORGE - {in_flight} packets in flight, {review} in review")

    def _quit(self) -> None:
        self.window.allow_close = True
        self.hide()
        self.app.quit()
