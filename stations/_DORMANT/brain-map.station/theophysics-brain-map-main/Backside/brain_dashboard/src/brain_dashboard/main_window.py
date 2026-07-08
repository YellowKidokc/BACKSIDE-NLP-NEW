from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QAction, QKeySequence, QShortcut
from PySide6.QtWidgets import QMainWindow, QTabWidget

from .data.log_tail import tail_lines
from .data.state_reader import read_state
from .data.task_scheduler import read_tasks
from .views.logs import LogsView
from .views.nlp_detail import NLPDetailView
from .views.overview import OverviewView
from .views.pipeline_state import PipelineStateView
from .views.schedule import ScheduleView


class MainWindow(QMainWindow):
    def __init__(self, state_path: Path, logs_dir: Path) -> None:
        super().__init__()
        self.state_path = state_path
        self.logs_dir = logs_dir
        self.setWindowTitle("Brain Dashboard")
        self.resize(1280, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.overview = OverviewView()
        self.nlp_detail = NLPDetailView()
        self.pipeline_state = PipelineStateView()
        self.schedule = ScheduleView()
        self.logs = LogsView()

        self.tabs.addTab(self.overview, "Overview")
        self.tabs.addTab(self.nlp_detail, "NLP Detail")
        self.tabs.addTab(self.pipeline_state, "Pipeline State")
        self.tabs.addTab(self.schedule, "Schedule")
        self.tabs.addTab(self.logs, "Logs")

        for idx in range(5):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{idx+1}"), self)
            shortcut.activated.connect(lambda i=idx: self.tabs.setCurrentIndex(i))
        QShortcut(QKeySequence("F5"), self).activated.connect(self.refresh)

        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        quit_action.triggered.connect(self.close)
        self.addAction(quit_action)

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.refresh)
        self.timer.start()
        self.refresh()

    def refresh(self) -> None:
        state = read_state(self.state_path)
        self.overview.update_state(state)
        self.schedule.update_tasks(read_tasks())
        log_files = sorted(self.logs_dir.glob("*.log"))
        if log_files:
            self.logs.update_lines(tail_lines(log_files[-1], 200))
