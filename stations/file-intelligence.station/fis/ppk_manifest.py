"""Bridge FIS results into the Portable Preference Kernel package.

This keeps the model package read-only and writes generated manifests into the
station runtime folder so the file watcher does not recursively ingest them.
"""

from __future__ import annotations

import json
import os
import sys
import importlib.util
from pathlib import Path
from typing import Any, Dict, Optional

from fis.db.connection import get_config
from fis.log import get_logger


log = get_logger("ppk")

STATION_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PPK_PACKAGE = Path(
    r"\\dlowenas\brain\Backside\_models\_Models\P05_ppk"
)
DEFAULT_MODEL_PATH = STATION_ROOT / "_ppk_runtime" / "portable_preference_kernel.json"
DEFAULT_MANIFEST_DIR = STATION_ROOT / "_ppk_runtime" / "manifests"


def _config_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class PPKManifestBridge:
    """Build artifact manifests and route predictions for processed files."""

    def __init__(self):
        config = get_config()
        self.enabled = _config_bool(
            config.get("ppk", "enabled", fallback="true"),
            default=True,
        )
        self.package_path = Path(
            config.get("ppk", "package_path", fallback=str(DEFAULT_PPK_PACKAGE))
        )
        self.model_path = Path(
            config.get("ppk", "model_path", fallback=str(DEFAULT_MODEL_PATH))
        )
        self.manifest_dir = Path(
            config.get("ppk", "manifest_dir", fallback=str(DEFAULT_MANIFEST_DIR))
        )
        self.top_k = int(config.get("ppk", "top_k", fallback="8"))

    @property
    def addon_path(self) -> Path:
        return self.package_path / "fis_addons"

    def _load_builder(self):
        if not self.addon_path.exists():
            raise FileNotFoundError(f"PPK fis_addons not found: {self.addon_path}")

        addon_path = str(self.addon_path)
        if addon_path not in sys.path:
            sys.path.insert(0, addon_path)

        os.environ.setdefault("PYTHONUTF8", "1")
        os.environ.setdefault("PYTHONIOENCODING", "utf-8")

        artifact_manifest_path = self.addon_path / "artifact_manifest.py"
        spec = importlib.util.spec_from_file_location(
            "fis_ppk_artifact_manifest",
            artifact_manifest_path,
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Unable to load PPK artifact manifest: {artifact_manifest_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.build_manifest

    def build_for_file(
        self,
        file_path: Path,
        fis_result: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        if not self.enabled:
            return None

        build_manifest = self._load_builder()
        manifest = build_manifest(
            Path(file_path),
            fis_result=fis_result,
            model_path=self.model_path,
        )
        manifest["fis_ppk_bridge"] = {
            "package_path": str(self.package_path),
            "model_path": str(self.model_path),
            "manifest_dir": str(self.manifest_dir),
            "selected_preference_spine": "P05_ppk",
            "support_engines": [
                "P01_implicit",
                "P06_river",
                "P07_markovify",
            ],
        }

        self.manifest_dir.mkdir(parents=True, exist_ok=True)
        out_path = self.manifest_dir / f"{manifest['artifact_id']}.fis_manifest.json"
        out_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        prediction = manifest.get("preference_prediction") or {}
        recommendations = prediction.get("recommendations", [])
        return {
            "artifact_id": manifest.get("artifact_id"),
            "manifest_path": str(out_path),
            "route_count": len(manifest.get("routes", [])),
            "top_routes": manifest.get("routes", [])[: self.top_k],
            "ppk_prediction_count": len(recommendations),
            "ppk_top_recommendations": recommendations[: self.top_k],
            "stored_raw_content": False,
        }


def attach_ppk_manifest(
    bridge: PPKManifestBridge,
    file_path: Path,
    result: Dict[str, Any],
) -> Dict[str, Any]:
    """Attach PPK manifest metadata without allowing PPK failures to break FIS."""
    try:
        handoff = bridge.build_for_file(file_path, result)
        if handoff:
            result["ppk_manifest"] = handoff
    except Exception as exc:
        log.warning("PPK manifest skipped for %s: %s", file_path, exc)
        result["ppk_manifest_error"] = str(exc)
    return result
