from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame

from ..widgets.status_pill import StatusPill


class OverviewView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.summary = QLabel("Queue: 0 | Engine: unknown | Last event: n/a")
        self.layout.addWidget(self.summary)
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)
        self.errors = QLabel("Recent errors: none")
        self.layout.addWidget(self.errors)

    def update_state(self, state: dict) -> None:
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        nlps = state.get("nlps", {})
        total_q = sum(v.get("queue_depth", 0) for v in nlps.values())
        engine = state.get("engine", {})
        self.summary.setText(
            f"Queue: {total_q} | Engine: {engine.get('running', False)} | Last event: {engine.get('last_event_time', 'n/a')}"
        )
        row = 0
        col = 0
        for name, payload in nlps.items():
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            v = QVBoxLayout(card)
            v.addWidget(QLabel(name))
            pill = StatusPill()
            pill.set_status(payload.get("status", "idle"))
            v.addWidget(pill)
            v.addWidget(QLabel(f"Queue depth: {payload.get('queue_depth', 0)}"))
            self.grid.addWidget(card, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1
        errs = state.get("errors", [])[:5]
        self.errors.setText("Recent errors:\n" + "\n".join(errs) if errs else "Recent errors: none")
