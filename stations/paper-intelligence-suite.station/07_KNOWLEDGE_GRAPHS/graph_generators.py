from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

GRAPH_TYPES = ("tag_graph", "axiom_dependency", "master_equation", "paper_to_paper")


def _slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_") or "graph"


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        for key in ("papers", "rows", "records", "nodes"):
            if isinstance(payload.get(key), list):
                return [x for x in payload[key] if isinstance(x, dict)]
        return [payload]
    return []


def _tags(record: dict) -> list[str]:
    value = record.get("tags") or record.get("keywords") or record.get("concepts") or []
    if isinstance(value, str):
        return [v.strip() for v in re.split(r"[,;|]", value) if v.strip()]
    if isinstance(value, dict):
        return [str(k) for k, v in value.items() if v]
    return [str(v) for v in value if str(v).strip()]


def _paper_id(record: dict, idx: int = 0) -> str:
    return str(record.get("paper_id") or record.get("id") or record.get("file") or record.get("title") or f"paper_{idx+1}")


def tag_graph(records: list[dict]) -> dict:
    counts = Counter()
    edges = Counter()
    for record in records:
        tags = sorted(set(_tags(record)))
        counts.update(tags)
        for i, left in enumerate(tags):
            for right in tags[i + 1:]:
                edges[(left, right)] += 1
    return {
        "type": "tag_graph",
        "nodes": [{"id": tag, "label": tag, "weight": count} for tag, count in counts.most_common()],
        "edges": [{"source": a, "target": b, "weight": w} for (a, b), w in edges.items()],
        "summary": {"tag_count": len(counts), "edge_count": len(edges), "paper_count": len(records)},
    }


def axiom_dependency(records: list[dict]) -> dict:
    nodes = Counter()
    edges = Counter()
    for record in records:
        deps = record.get("dependency_chain", {}) if isinstance(record.get("dependency_chain"), dict) else {}
        upstream = deps.get("upstream", []) or record.get("upstream", []) or record.get("dependencies", []) or []
        downstream = deps.get("downstream", []) or record.get("downstream", []) or []
        for node in upstream + downstream:
            nodes[str(node)] += 1
        for up in upstream:
            for down in downstream or [_paper_id(record)]:
                edges[(str(up), str(down))] += 1
    return {
        "type": "axiom_dependency",
        "nodes": [{"id": k, "label": k, "weight": v} for k, v in nodes.items()],
        "edges": [{"source": a, "target": b, "weight": w} for (a, b), w in edges.items()],
        "summary": {"dependency_nodes": len(nodes), "dependency_edges": len(edges)},
    }


def master_equation(records: list[dict]) -> dict:
    variables = ["χ", "G", "M", "E", "S", "T", "K", "R", "Q", "F", "C"]
    counts = Counter()
    edges = Counter()
    for record in records:
        text = json.dumps(record, ensure_ascii=False).lower()
        present = []
        for var in variables:
            aliases = [var.lower()]
            if var == "χ": aliases += ["chi", "master equation"]
            if any(alias in text for alias in aliases):
                counts[var] += 1
                present.append(var)
        for i, left in enumerate(present):
            for right in present[i + 1:]:
                edges[(left, right)] += 1
    return {
        "type": "master_equation",
        "nodes": [{"id": v, "label": v, "weight": counts.get(v, 0)} for v in variables],
        "edges": [{"source": a, "target": b, "weight": w} for (a, b), w in edges.items()],
        "summary": {"variables": len(variables), "active_variables": sum(1 for v in variables if counts.get(v, 0)), "edge_count": len(edges)},
    }


def paper_to_paper(records: list[dict]) -> dict:
    nodes = []
    edges = []
    tag_sets = []
    for i, record in enumerate(records):
        pid = _paper_id(record, i)
        tags = set(_tags(record))
        tag_sets.append((pid, tags))
        nodes.append({"id": pid, "label": str(record.get("title") or pid), "weight": len(tags)})
    for i, (left, left_tags) in enumerate(tag_sets):
        for right, right_tags in tag_sets[i + 1:]:
            overlap = left_tags & right_tags
            if overlap:
                edges.append({"source": left, "target": right, "weight": len(overlap), "overlap": sorted(overlap)})
    return {"type": "paper_to_paper", "nodes": nodes, "edges": edges, "summary": {"paper_count": len(nodes), "edge_count": len(edges)}}


def _render_html(graph: dict) -> str:
    data = json.dumps(graph, ensure_ascii=False)
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    width, height = 980, 680
    n = max(len(nodes), 1)
    positions = {}
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / n
        positions[node["id"]] = (width / 2 + math.cos(angle) * 260, height / 2 + math.sin(angle) * 240)
    edge_svg = []
    for edge in edges:
        if edge.get("source") in positions and edge.get("target") in positions:
            x1, y1 = positions[edge["source"]]
            x2, y2 = positions[edge["target"]]
            edge_svg.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#94a3b8" stroke-width="{max(1, min(8, edge.get("weight", 1)))}" opacity="0.55"/>')
    node_svg = []
    for node in nodes:
        x, y = positions[node["id"]]
        size = max(8, min(32, 8 + int(node.get("weight", 1))))
        node_svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size}" fill="#f59e0b" stroke="#111827" stroke-width="2"><title>{node.get("label", node["id"])}</title></circle><text x="{x+size+4:.1f}" y="{y+4:.1f}" font-size="12">{node.get("label", node["id"])}</text>')
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>{graph.get('type')} graph</title><style>body{{font-family:system-ui;background:#0f172a;color:#e5e7eb}}svg{{background:#f8fafc;border-radius:16px}}pre{{white-space:pre-wrap}}</style></head><body><h1>{graph.get('type')}</h1><p>{graph.get('summary')}</p><svg viewBox="0 0 {width} {height}" width="100%" height="{height}">{''.join(edge_svg)}{''.join(node_svg)}</svg><script type="application/json" id="graph-data">{data}</script><h2>Summary</h2><pre>{json.dumps(graph.get('summary', {}), indent=2)}</pre></body></html>'''


def generate_all(input_json: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    records = _records(_load(input_json))
    builders = [tag_graph, axiom_dependency, master_equation, paper_to_paper]
    manifest = {"input": str(input_json), "generated_at": datetime.now().isoformat(timespec="seconds"), "graphs": []}
    for builder in builders:
        graph = builder(records)
        base = output_dir / graph["type"]
        json_path = base.with_suffix(".json")
        html_path = base.with_suffix(".html")
        md_path = base.with_suffix(".summary.md")
        json_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
        html_path.write_text(_render_html(graph), encoding="utf-8")
        md_path.write_text(f"# {graph['type']}\n\n```json\n{json.dumps(graph['summary'], indent=2)}\n```\n", encoding="utf-8")
        manifest["graphs"].append({"type": graph["type"], "json": str(json_path), "html": str(html_path), "summary": str(md_path), "stats": graph["summary"]})
    (output_dir / "knowledge_graph_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate BACKSIDE knowledge graphs from paper JSON.")
    ap.add_argument("input_json", type=Path)
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "_outbox" / "graphs")
    args = ap.parse_args()
    manifest = generate_all(args.input_json, args.out)
    print(json.dumps({"graphs": len(manifest["graphs"]), "output": str(args.out)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
