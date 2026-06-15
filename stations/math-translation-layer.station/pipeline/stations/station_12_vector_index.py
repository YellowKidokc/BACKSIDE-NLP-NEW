from __future__ import annotations

import json
from typing import Any

from pipeline.stations.common import paper_output_dir, read_json, utc_now


def _summary_text(component_name: str, findings: list[dict[str, Any]]) -> str:
    if not findings:
        return f"{component_name}: no findings recorded."
    snippets = []
    for item in findings[:5]:
        label = item.get("surface_claim") or item.get("gap") or item.get("track") or item.get("voice") or item.get("claim_uuid") or "item"
        snippets.append(str(label))
    return f"{component_name}: " + " | ".join(snippets)


def run(paper_uuid: str) -> list[dict[str, Any]]:
    output_dir = paper_output_dir(paper_uuid)
    report = read_json(output_dir / "11_paper_grade.json")
    rows: list[dict[str, Any]] = []
    for index, component_name in enumerate(report["snapshot_order"], start=1):
        component = report["components"][component_name]
        rows.append(
            {
                "paper_uuid": paper_uuid,
                "component": component_name,
                "component_order": index,
                "text": _summary_text(component_name, component.get("findings", [])),
                "metadata": {
                    "station": "12_vector_index",
                    "source_file": "11_paper_grade.json",
                    "embedding_ready": True,
                    "external_embedding_api_called": False,
                    "timestamp": utc_now(),
                },
            }
        )
    path = output_dir / "12_vector_summary.jsonl"
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    return rows
