from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.decomposition import PCA

from .embeddings import Embedder


def artifact_text(artifact: dict[str, Any]) -> str:
    parts: list[str] = [
        artifact.get("address", ""),
        artifact.get("vector_string", ""),
        " ".join(artifact.get("spine", [])[:20]),
    ]
    for item in artifact.get("claim_arch", [])[:20]:
        parts.append(item.get("surface_claim", ""))
        parts.append(item.get("buried_claim", ""))
        parts.append(item.get("operational_claim", ""))
    for item in artifact.get("domain_boundary", [])[:20]:
        parts.append(" ".join(str(item.get(key, "")) for key in ["term", "domain_usage_1", "domain_usage_2", "bridge_quality", "drift_risk"]))
    return "\n".join(part for part in parts if part)


def load_artifacts(input_root: Path) -> list[tuple[Path, dict[str, Any]]]:
    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(input_root.rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if "address" in data and "ids" in data:
            rows.append((path, data))
    return rows


def _semantic_vector_features(artifact: dict[str, Any]) -> list[float]:
    vector = artifact.get("semantic_vector", {})
    return [float(vector.get(key, 0)) for key in ["G", "M", "E", "S", "T", "K", "R", "Q", "F", "C"]]


def project_artifacts(input_root: Path, out_dir: Path, *, mode: str = "sbert") -> tuple[Path, Path]:
    rows = load_artifacts(input_root)
    if not rows:
        raise SystemExit(f"No lossless artifact JSON files found under {input_root}")

    if mode == "sbert":
        embedder = Embedder("sbert")
        matrix = np.array([embedder.embed(artifact_text(data)) for _, data in rows], dtype=float)
    elif mode == "semantic":
        matrix = np.array([_semantic_vector_features(data) for _, data in rows], dtype=float)
    else:
        raise ValueError(f"Unknown projection mode: {mode}")

    if len(rows) >= 3:
        coords = PCA(n_components=3, random_state=2828).fit_transform(matrix)
    else:
        coords = np.zeros((len(rows), 3), dtype=float)
        max_dims = min(3, matrix.shape[1])
        coords[:, :max_dims] = matrix[:, :max_dims]

    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "semantic-space.csv"
    json_path = out_dir / "semantic-space.json"

    output_rows: list[dict[str, Any]] = []
    for (path, data), coord in zip(rows, coords):
        item = {
            "artifact_path": str(path),
            "doc_id": data.get("ids", {}).get("doc_id"),
            "content_hash": data.get("ids", {}).get("content_hash"),
            "address": data.get("address"),
            "vector": data.get("vector_string"),
            "hash": data.get("hash"),
            "x": float(coord[0]),
            "y": float(coord[1]),
            "z": float(coord[2]),
        }
        output_rows.append(item)

    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(output_rows[0].keys()))
        writer.writeheader()
        writer.writerows(output_rows)
    json_path.write_text(json.dumps(output_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return csv_path, json_path
