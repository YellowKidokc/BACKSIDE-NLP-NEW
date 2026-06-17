"""
job_card.py — Workflow tracking for documents through the pipeline.
POF 2828 | 2026-06-17

Tracks which stations a document has passed through, what succeeded,
what failed, and where it currently is in the pipeline.
"""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

JOB_CARDS_DIR = Path(__file__).resolve().parent / "job_cards"


class JobCard:
    def __init__(self, doc_id: str, doc_path: str,
                 workflow: str = "article-production"):
        self.doc_id = doc_id
        self.doc_path = doc_path
        self.workflow = workflow
        self.created_at = datetime.now().isoformat(timespec="seconds")
        self.updated_at = self.created_at
        self.stations_completed: list[dict] = []
        self.stations_failed: list[dict] = []
        self.current_station: Optional[dict] = None
        self.status = "IN_PROGRESS"  # IN_PROGRESS | COMPLETE | FAILED | PAUSED

    def check_in(self, station_id: str, station_name: str):
        """Mark a station as currently processing this doc."""
        self.current_station = {
            "id": station_id,
            "name": station_name,
            "started": datetime.now().isoformat(timespec="seconds"),
        }
        self.updated_at = datetime.now().isoformat(timespec="seconds")
        self.save()

    def check_out(self, station_id: str, success: bool,
                  artifact_path: Optional[str] = None,
                  error: Optional[str] = None):
        """Mark a station as finished processing this doc."""
        entry = {
            "id": station_id,
            "completed": datetime.now().isoformat(timespec="seconds"),
            "success": success,
            "artifact": artifact_path,
            "error": error,
        }
        if success:
            self.stations_completed.append(entry)
        else:
            self.stations_failed.append(entry)
        self.current_station = None
        self.updated_at = datetime.now().isoformat(timespec="seconds")
        self.save()

    def mark_complete(self):
        self.status = "COMPLETE"
        self.updated_at = datetime.now().isoformat(timespec="seconds")
        self.save()

    def mark_failed(self, reason: str = ""):
        self.status = "FAILED"
        self.updated_at = datetime.now().isoformat(timespec="seconds")
        self.save()

    def progress(self) -> dict:
        """Return a summary of pipeline progress."""
        completed_ids = {s["id"] for s in self.stations_completed}
        failed_ids = {s["id"] for s in self.stations_failed}
        pipeline = ["ST_001", "ST_002", "ST_003", "ST_004",
                     "ST_005", "ST_006", "ST_007", "ST_008"]
        steps = []
        for sid in pipeline:
            if sid in completed_ids:
                steps.append({"station": sid, "status": "DONE"})
            elif sid in failed_ids:
                steps.append({"station": sid, "status": "FAILED"})
            elif self.current_station and self.current_station["id"] == sid:
                steps.append({"station": sid, "status": "RUNNING"})
            else:
                steps.append({"station": sid, "status": "PENDING"})
        return {
            "doc_id": self.doc_id,
            "status": self.status,
            "completed": len(self.stations_completed),
            "failed": len(self.stations_failed),
            "total": len(pipeline),
            "steps": steps,
        }

    def save(self, directory: Optional[Path] = None):
        d = directory or JOB_CARDS_DIR
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"JOB_{self.doc_id}.json"
        path.write_text(json.dumps(self.to_dict(), indent=2, default=str),
                        encoding="utf-8")
        return path

    def to_dict(self) -> dict:
        return {
            "doc_id": self.doc_id,
            "doc_path": self.doc_path,
            "workflow": self.workflow,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "current_station": self.current_station,
            "stations_completed": self.stations_completed,
            "stations_failed": self.stations_failed,
            "progress": self.progress(),
        }

    @classmethod
    def load(cls, path: Path) -> "JobCard":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        card = cls(data["doc_id"], data["doc_path"], data.get("workflow", ""))
        card.created_at = data.get("created_at", "")
        card.updated_at = data.get("updated_at", "")
        card.status = data.get("status", "IN_PROGRESS")
        card.current_station = data.get("current_station")
        card.stations_completed = data.get("stations_completed", [])
        card.stations_failed = data.get("stations_failed", [])
        return card

    @classmethod
    def load_or_create(cls, doc_id: str, doc_path: str,
                       directory: Optional[Path] = None) -> "JobCard":
        d = directory or JOB_CARDS_DIR
        path = d / f"JOB_{doc_id}.json"
        if path.exists():
            return cls.load(path)
        return cls(doc_id, doc_path)
