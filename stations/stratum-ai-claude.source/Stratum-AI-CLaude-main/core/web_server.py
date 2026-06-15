from __future__ import annotations

import json
import mimetypes
import os
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib import error, request
from urllib.parse import unquote, urlparse

from PySide6.QtCore import QThread, Signal

from .data_store import JsonStore


class ForgeWebServer(QThread):
    started_ok = Signal(str)
    failed = Signal(str)

    def __init__(self, host: str, port: int, data_dir: Path, web_dir: Path, settings: Any | None = None) -> None:
        super().__init__()
        self.host = host
        self.port = port
        self.data_dir = Path(data_dir)
        self.web_dir = Path(web_dir)
        self.settings = settings
        self.httpd: ThreadingHTTPServer | None = None

    def run(self) -> None:
        handler = self._make_handler()
        try:
            self.httpd = ThreadingHTTPServer((self.host, self.port), handler)
            self.started_ok.emit(f"http://{self.host}:{self.port}/")
            self.httpd.serve_forever(poll_interval=0.2)
        except OSError as exc:
            self.failed.emit(str(exc))

    def stop(self) -> None:
        if self.httpd:
            self.httpd.shutdown()

    def _make_handler(self):
        data_dir = self.data_dir
        web_dir = self.web_dir
        settings = self.settings

        class Handler(BaseHTTPRequestHandler):
            routes = {
                "/api/clips": data_dir / "clips.json",
                "/api/items": data_dir / "clips.json",
                "/api/prompts": data_dir / "prompts.json",
                "/api/bookmarks": data_dir / "research_links.json",
                "/api/tasks": data_dir / "tasks.json",
            }
            pages = {
                "/": "clipboard.html",
                "/prompts": "prompt_picker.html",
                "/links": "research_links.html",
                "/calendar": "task-calendar.html",
                "/comms": "comms-dashboard.html",
                "/nexus": "nexus-dashboard.html",
            }

            def log_message(self, _format: str, *_args) -> None:
                return

            def do_GET(self) -> None:
                parsed = urlparse(self.path)
                if parsed.path == "/api/status":
                    self._json({"ok": True, "service": "FORGE Hub", "port": self.server.server_port})
                    return
                if parsed.path in ("/api/window-state", "/window-state"):
                    self._json({"position": {}, "pin": {"pinned": False}})
                    return
                if parsed.path.startswith("/api/files/"):
                    self._json(self._file_listing(parsed.path.removeprefix("/api/files/")))
                    return
                if parsed.path in self.routes:
                    self._json(self._items_payload(parsed.path))
                    return
                page = self.pages.get(parsed.path)
                if page:
                    self._serve_file(web_dir / page)
                    return
                self._serve_file(web_dir / unquote(parsed.path.lstrip("/")))

            def do_POST(self) -> None:
                path = urlparse(self.path).path
                if path in ("/window/position", "/window/pin"):
                    self._json({"ok": True})
                    return
                if path == "/api/files/open":
                    payload = self._read_body()
                    target = payload.get("path", "")
                    if target:
                        try:
                            subprocess.Popen(["explorer", target])
                        except OSError:
                            pass
                    self._json({"ok": bool(target)})
                    return
                self._write_item("post")

            def do_PUT(self) -> None:
                self._write_item("put")

            def do_PATCH(self) -> None:
                self._write_item("put")

            def do_DELETE(self) -> None:
                parsed = urlparse(self.path)
                api_path, item_id = self._split_api_path(parsed.path)
                if api_path not in self.routes or not item_id:
                    self._json({"error": "not found"}, 404)
                    return
                deleted = JsonStore(self.routes[api_path]).delete(item_id)
                self._json({"deleted": deleted})

            def do_OPTIONS(self) -> None:
                self.send_response(204)
                self._cors()
                self.end_headers()

            def _write_item(self, method: str) -> None:
                parsed = urlparse(self.path)
                api_path, item_id = self._split_api_path(parsed.path)
                if api_path not in self.routes:
                    self._json({"error": "not found"}, 404)
                    return
                payload = self._read_body()
                store = JsonStore(self.routes[api_path])
                if method == "put" and item_id:
                    item = store.update(item_id, payload)
                    if item is None:
                        self._json({"error": "not found"}, 404)
                        return
                elif method == "put" and isinstance(payload.get("items"), list):
                    store.replace_all(payload["items"])
                    item = {"items": payload["items"]}
                else:
                    item = store.add(payload)
                if api_path in ("/api/clips", "/api/items"):
                    self._queue_cloudflare_sync(item)
                self._json(item)

            def _items_payload(self, api_path: str) -> Any:
                items = JsonStore(self.routes[api_path]).all()
                if api_path == "/api/items":
                    return {"items": [self._compat_item(item) for item in items]}
                return items

            def _compat_item(self, item: dict[str, Any]) -> dict[str, Any]:
                out = dict(item)
                if "content" not in out and "text" in out:
                    out["content"] = out["text"]
                if "text" not in out and "content" in out:
                    out["text"] = out["content"]
                out.setdefault("type", "clip")
                return out

            def _file_listing(self, folder: str) -> list[dict[str, Any]]:
                roots = {
                    "vault": os.environ.get("THEOPHYSICS_VAULT", ""),
                    "stations": os.environ.get("STATIONS_ROOT", ""),
                    "models": os.environ.get("MODELS_ROOT", ""),
                    "forge": os.environ.get("FORGE_REPO", ""),
                    "gtq": os.environ.get("GTQ_BUILD", ""),
                }
                root = Path(roots.get(folder, "") or folder)
                if not root.exists() or not root.is_dir():
                    return []
                items: list[dict[str, Any]] = []
                for path in sorted(root.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))[:500]:
                    items.append({
                        "name": path.name,
                        "path": str(path),
                        "is_dir": path.is_dir(),
                        "size": path.stat().st_size if path.is_file() else 0,
                    })
                return items

            def _split_api_path(self, path: str) -> tuple[str, str | None]:
                parts = path.strip("/").split("/")
                if len(parts) >= 2:
                    api_path = "/" + "/".join(parts[:2])
                    item_id = "/".join(parts[2:]) or None
                    return api_path, item_id
                return path, None

            def _read_body(self) -> dict[str, Any]:
                length = int(self.headers.get("Content-Length", "0") or 0)
                if not length:
                    return {}
                try:
                    return json.loads(self.rfile.read(length).decode("utf-8"))
                except ValueError:
                    return {}

            def _serve_file(self, path: Path) -> None:
                if not path.exists() or not path.is_file():
                    self._json({"error": "not found"}, 404)
                    return
                content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
                data = path.read_bytes()
                self.send_response(200)
                self._cors()
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def _json(self, payload: Any, status: int = 200) -> None:
                data = json.dumps(payload).encode("utf-8")
                self.send_response(status)
                self._cors()
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def _cors(self) -> None:
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type,Authorization")

            def _queue_cloudflare_sync(self, clip: dict[str, Any]) -> None:
                if settings is None or not settings.config.getboolean("cloudflare_sync", "enabled", fallback=False):
                    return
                worker_url = settings.config.get("cloudflare_sync", "worker_url", fallback="")
                token = settings.config.get("cloudflare_sync", "token", fallback="")
                if not worker_url or not token:
                    return

                def run() -> None:
                    body = json.dumps(clip).encode("utf-8")
                    req = request.Request(worker_url, data=body, headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {token}",
                    }, method="POST")
                    try:
                        request.urlopen(req, timeout=5).close()
                    except (OSError, error.URLError):
                        pass

                threading.Thread(target=run, daemon=True).start()

        return Handler
