from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.pipeline_runner import PipelineRunThread, pipeline_root, read_json


STATUS_COLORS = {
    "running": QColor("#2d7ff9"),
    "review": QColor("#d59600"),
    "error": QColor("#c93c37"),
    "done": QColor("#2f9d55"),
}


class PipelineTab(QWidget):
    def __init__(self, settings: Any, bil_client: Any | None = None) -> None:
        super().__init__()
        self.settings = settings
        self.bil_client = bil_client
        self.runner: PipelineRunThread | None = None
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        top = QHBoxLayout()

        workflow_group = QGroupBox("Workflow")
        workflow_layout = QVBoxLayout(workflow_group)
        self.workflow_combo = QComboBox()
        workflow_layout.addWidget(self.workflow_combo)
        run_btn = QPushButton("Run Workflow")
        run_btn.clicked.connect(self._run_workflow)
        workflow_layout.addWidget(run_btn)
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh)
        workflow_layout.addWidget(refresh_btn)
        top.addWidget(workflow_group, 1)

        packet_group = QGroupBox("Packets In Flight")
        packet_layout = QVBoxLayout(packet_group)
        self.packet_table = QTableWidget(0, 5)
        self.packet_table.setHorizontalHeaderLabels(["Name", "Workflow", "Stage", "Status", "Elapsed"])
        packet_layout.addWidget(self.packet_table)
        top.addWidget(packet_group, 2)

        review_group = QGroupBox("Review Queue")
        review_layout = QVBoxLayout(review_group)
        self.review_list = QListWidget()
        self.review_list.currentItemChanged.connect(self._load_review_item)
        review_layout.addWidget(self.review_list)
        self.route_combo = QComboBox()
        self.route_combo.setEditable(True)
        review_layout.addWidget(self.route_combo)
        self.reason = QLineEdit()
        self.reason.setPlaceholderText("Optional correction reason")
        review_layout.addWidget(self.reason)
        buttons = QHBoxLayout()
        for label, handler in [("Approve", self._approve), ("Reject", self._reject), ("Reclassify", self._reclassify)]:
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            buttons.addWidget(btn)
        review_layout.addLayout(buttons)
        top.addWidget(review_group, 2)
        layout.addLayout(top, 3)

        bottom = QHBoxLayout()
        station_group = QGroupBox("Station Health")
        self.station_grid = QGridLayout(station_group)
        bottom.addWidget(station_group, 2)
        log_group = QGroupBox("Runner Log")
        log_layout = QVBoxLayout(log_group)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        log_layout.addWidget(self.log)
        bottom.addWidget(log_group, 3)
        layout.addLayout(bottom, 2)

    def refresh(self) -> None:
        self._load_workflows()
        self._load_packets()
        self._load_review()
        self._load_stations()

    def in_flight_count(self) -> int:
        return self.packet_table.rowCount()

    def review_count(self) -> int:
        return self.review_list.count()

    def _stations_root(self) -> Path:
        configured = self.settings.config.get("forge", "stations_root", fallback="")
        return Path(os.environ.get("STATIONS_ROOT") or configured or r"X:\Backside\stations")

    def _manifest_path(self) -> Path:
        return self._stations_root().parent / "MANIFEST.json"

    def _review_dir(self) -> Path:
        return self._stations_root().parent / "REVIEW"

    def _load_workflows(self) -> None:
        self.workflow_combo.clear()
        root = pipeline_root(self.settings)
        registry = read_json(root / "WORKFLOW_REGISTRY.json", {})
        names = list(registry.keys()) if isinstance(registry, dict) else []
        workflows_dir = root / "workflows"
        if workflows_dir.exists():
            names.extend(path.stem for path in workflows_dir.glob("*.json"))
        for name in sorted(set(names)):
            self.workflow_combo.addItem(name)

    def _load_packets(self) -> None:
        manifest = read_json(self._manifest_path(), {})
        packets = manifest.get("packets", manifest if isinstance(manifest, list) else [])
        self.packet_table.setRowCount(len(packets))
        for row, packet in enumerate(packets):
            values = [
                packet.get("name", packet.get("file", "")),
                packet.get("workflow", ""),
                packet.get("stage", packet.get("current_stage", "")),
                packet.get("status", ""),
                self._elapsed(packet),
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                color = STATUS_COLORS.get(str(packet.get("status", "")).lower())
                if color:
                    item.setBackground(color)
                self.packet_table.setItem(row, col, item)

    def _elapsed(self, packet: dict[str, Any]) -> str:
        started = packet.get("started_at") or packet.get("created_at")
        if not started:
            return ""
        try:
            start = datetime.fromisoformat(started.replace("Z", "+00:00")).replace(tzinfo=None)
            delta = datetime.now() - start
            return str(delta).split(".")[0]
        except ValueError:
            return ""

    def _load_review(self) -> None:
        self.review_list.clear()
        review_dir = self._review_dir()
        if not review_dir.exists():
            return
        for path in sorted(review_dir.glob("*")):
            if path.is_file():
                item = QListWidgetItem(path.name)
                item.setData(Qt.UserRole, str(path))
                self.review_list.addItem(item)

    def _load_review_item(self) -> None:
        self.route_combo.clear()
        item = self.review_list.currentItem()
        if not item:
            return
        path = Path(item.data(Qt.UserRole))
        meta = read_json(path.with_suffix(path.suffix + ".meta.json"), {})
        for route in [meta.get("proposed_route", ""), meta.get("fis_classification", "")]:
            if route:
                self.route_combo.addItem(route)

    def _load_stations(self) -> None:
        while self.station_grid.count():
            child = self.station_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        root = pipeline_root(self.settings)
        registry = read_json(root / "STATION_REGISTRY.json", {})
        stations = registry.items() if isinstance(registry, dict) else []
        for idx, (name, data) in enumerate(stations):
            status = str(data.get("status", "active")).lower() if isinstance(data, dict) else "active"
            label = QLabel(str(name))
            label.setAlignment(Qt.AlignCenter)
            color = {"active": "#2f9d55", "degraded": "#d59600", "dead": "#c93c37"}.get(status, "#777")
            label.setStyleSheet(f"background:{color}; color:white; padding:6px;")
            self.station_grid.addWidget(label, idx // 4, idx % 4)

    def _run_workflow(self) -> None:
        workflow = self.workflow_combo.currentText().strip()
        if not workflow:
            return
        self.runner = PipelineRunThread(workflow, self.settings)
        self.runner.output.connect(self.log.append)
        self.runner.finished_ok.connect(lambda code: self.log.append(f"Exit code: {code}"))
        self.runner.finished_ok.connect(lambda _code: self.refresh())
        self.runner.start()

    def _selected_review_path(self) -> Path | None:
        item = self.review_list.currentItem()
        return Path(item.data(Qt.UserRole)) if item else None

    def _approve(self) -> None:
        self._move_review("OUTPUT", "approved")

    def _reject(self) -> None:
        self._move_review(Path("ERROR") / "kickout", "rejected")

    def _reclassify(self) -> None:
        path = self._selected_review_path()
        if not path:
            return
        self._post_correction(path, "reclassified")
        self.refresh()

    def _move_review(self, destination: str | Path, action: str) -> None:
        path = self._selected_review_path()
        if not path:
            return
        target_dir = self._stations_root().parent / destination
        target_dir.mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(str(path), str(target_dir / path.name))
            self._post_correction(path, action)
            self.refresh()
        except OSError as exc:
            QMessageBox.warning(self, "Pipeline", f"Move failed: {exc}")

    def _post_correction(self, path: Path, action: str) -> None:
        if self.bil_client:
            self.bil_client.post_correction({
                "action": action,
                "file": str(path),
                "proposed_route": self.route_combo.currentText(),
                "reason": self.reason.text().strip(),
            })
