from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

from PySide6.QtCore import QThread, Signal


def pipeline_root(settings: Any | None = None) -> Path:
    configured = ""
    if settings is not None:
        configured = settings.config.get("forge", "pipeline_repo", fallback="")
    if configured:
        return Path(os.path.expandvars(configured))
    stations = os.environ.get("STATIONS_ROOT")
    if stations:
        return Path(stations).parent / "pipeline-workflows"
    return Path.cwd() / "pipeline-workflows"


def read_json(path: Path, default: Any) -> Any:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        pass
    return default


class PipelineRunThread(QThread):
    output = Signal(str)
    finished_ok = Signal(int)

    def __init__(self, workflow_name: str, settings: Any | None = None) -> None:
        super().__init__()
        self.workflow_name = workflow_name
        self.settings = settings

    def run(self) -> None:
        root = pipeline_root(self.settings)
        orchestrator = root / "orchestrator.py"
        if not orchestrator.exists():
            self.output.emit(f"orchestrator.py not found at {orchestrator}")
            self.finished_ok.emit(1)
            return

        cmd = ["python", str(orchestrator), self.workflow_name]
        self.output.emit(f"Running: {' '.join(cmd)}")
        process = subprocess.Popen(
            cmd,
            cwd=str(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        assert process.stdout is not None
        for line in process.stdout:
            self.output.emit(line.rstrip())
        self.finished_ok.emit(process.wait())
