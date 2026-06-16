from __future__ import annotations

import os
import threading
from typing import Any
from urllib import request, error
import json


SIGNAL_WEIGHTS = {
    "manual_approval": 1.0,
    "file_reused": 0.9,
    "copied_text": 0.8,
    "bookmark_save": 0.7,
    "long_dwell_scroll": 0.5,
    "opened_tab": 0.2,
    "accidental_visit": 0.0,
}


class BILClient:
    def __init__(self, base_url: str | None = None, enabled: bool = True) -> None:
        self.base_url = (base_url or os.environ.get("BIL_SERVER") or "http://localhost:8420").rstrip("/")
        self.enabled = enabled

    def post_event(self, endpoint: str, data: dict[str, Any], async_: bool = True) -> None:
        if not self.enabled:
            return
        path = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        payload = dict(data)
        if "signal_weight" not in payload and payload.get("event_type") in SIGNAL_WEIGHTS:
            payload["signal_weight"] = SIGNAL_WEIGHTS[payload["event_type"]]
        if async_:
            threading.Thread(target=self._post, args=(path, payload), daemon=True).start()
        else:
            self._post(path, payload)

    def get_predictions(self) -> dict[str, Any]:
        return self._get("/bil/clipboard/predict")

    def get_status(self) -> dict[str, Any]:
        return self._get("/bil/status")

    def post_correction(self, correction: dict[str, Any]) -> None:
        payload = dict(correction)
        payload.setdefault("event_type", "human_correction")
        payload.setdefault("signal_weight", SIGNAL_WEIGHTS["manual_approval"])
        self.post_event("/bil/signal", payload)

    def _post(self, path: str, payload: dict[str, Any]) -> None:
        try:
            body = json.dumps(payload).encode("utf-8")
            req = request.Request(
                f"{self.base_url}{path}",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            request.urlopen(req, timeout=2).close()
        except (OSError, error.URLError):
            pass

    def _get(self, path: str) -> dict[str, Any]:
        if not self.enabled:
            return {}
        try:
            with request.urlopen(f"{self.base_url}{path}", timeout=2) as response:
                data = json.loads(response.read().decode("utf-8"))
            return data if isinstance(data, dict) else {"items": data}
        except (OSError, error.URLError, ValueError):
            return {}
