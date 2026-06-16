"""
ST-GRAPH-001 — Knowledge Graph builder.

Read every artifact produced upstream (claims.json, forward_7q.json,
reverse_7q.json, evidence_7q.json) and emit:

    graph.json   — full graph with typed nodes + edges
    nodes.csv    — flat node table for Neo4j / viewer import
    edges.csv    — flat edge table

Node types: paper, claim, axiom_candidate, evidence, equation, domain, objection.
Edge types: supports, contradicts, depends_on, derives_from, maps_to, cites.

Usage:
    python run.py --in <input_dir> --out <graph.json>

The input dir is expected to contain the upstream artifacts (or symlinks to them).
Missing artifacts are tolerated — the graph just won't include those nodes.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

STATION_ID = "ST-GRAPH-001"


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"WARN: could not parse {path}: {e}", file=sys.stderr)
        return None


def build_graph(input_dir: Path) -> dict:
    claims = load_json(input_dir / "claims.json") or {}
    forward = load_json(input_dir / "forward_7q.json") or {}
    reverse = load_json(input_dir / "reverse_7q.json") or {}
    evidence = load_json(input_dir / "evidence_7q.json") or {}

    nodes = []
    edges = []

    paper_id = "P-001"
    nodes.append({"id": paper_id, "type": "paper",
                  "label": str(claims.get("paper") or forward.get("paper") or input_dir.name)})

    # Claims
    claim_list = claims.get("claims", []) if isinstance(claims, dict) else []
    for i, c in enumerate(claim_list, 1):
        cid = c.get("id", f"C-{i:03d}")
        nodes.append({"id": cid, "type": "claim",
                      "label": (c.get("text") or c.get("claim") or "")[:120]})
        edges.append({"source": paper_id, "target": cid, "type": "depends_on"})

    # Forward 7Q — extract domains (q1) and central claim (q2)
    for domain_str in _as_list(forward.get("q1", [])):
        did = f"D-{_slug(domain_str)[:24]}"
        if not any(n["id"] == did for n in nodes):
            nodes.append({"id": did, "type": "domain", "label": domain_str})
        edges.append({"source": paper_id, "target": did, "type": "maps_to"})

    central = forward.get("q2") or ""
    if central:
        nodes.append({"id": "C-CENTRAL", "type": "axiom_candidate", "label": str(central)[:200]})
        edges.append({"source": paper_id, "target": "C-CENTRAL", "type": "derives_from"})

    # Reverse 7Q — kill conditions / weakest link as objections
    weakest = reverse.get("r4") or ""
    if weakest:
        oid = "O-WEAKEST"
        nodes.append({"id": oid, "type": "objection", "label": str(weakest)[:200]})
        edges.append({"source": oid, "target": "C-CENTRAL", "type": "contradicts"})

    counter = reverse.get("r5") or ""
    if counter:
        oid = "O-COUNTER"
        nodes.append({"id": oid, "type": "objection", "label": str(counter)[:200]})
        edges.append({"source": oid, "target": "C-CENTRAL", "type": "contradicts"})

    # Evidence — each item becomes an evidence node
    ev_items = evidence.get("evidence", []) if isinstance(evidence, dict) else []
    for i, e in enumerate(ev_items, 1):
        eid = f"E-{i:03d}"
        nodes.append({
            "id": eid,
            "type": "evidence",
            "label": (e.get("text") or e.get("citation") or "")[:160],
            "evidence_class": e.get("class", "unknown"),
        })
        edge_type = "contradicts" if e.get("class") == "conflicting" else "supports"
        edges.append({"source": eid, "target": "C-CENTRAL", "type": edge_type})

    return {
        "station":     STATION_ID,
        "paper_id":    paper_id,
        "node_count":  len(nodes),
        "edge_count":  len(edges),
        "nodes":       nodes,
        "edges":       edges,
        "built_at":    datetime.now().isoformat(timespec="seconds"),
    }


def _as_list(x):
    if isinstance(x, list):
        return [str(i) for i in x if i]
    if isinstance(x, str):
        return [p.strip() for p in x.split(",") if p.strip()]
    return []


def _slug(s: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in s.lower()).strip("_") or "x"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True,
                        help="Directory containing claims.json / forward_7q.json / etc.")
    parser.add_argument("--out", dest="out", required=True)
    args = parser.parse_args()

    inp_path = Path(args.inp)
    if inp_path.is_file():
        inp_path = inp_path.parent
    graph = build_graph(inp_path)
    Path(args.out).write_text(json.dumps(graph, indent=2), encoding="utf-8")

    nodes_csv = Path(args.out).with_name("nodes.csv")
    edges_csv = Path(args.out).with_name("edges.csv")
    with nodes_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "type", "label", "evidence_class"])
        w.writeheader()
        for n in graph["nodes"]:
            w.writerow({"id": n.get("id"), "type": n.get("type"),
                        "label": n.get("label", ""), "evidence_class": n.get("evidence_class", "")})
    with edges_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["source", "target", "type"])
        w.writeheader()
        for e in graph["edges"]:
            w.writerow(e)

    print(json.dumps({"status": "ok",
                      "nodes": graph["node_count"], "edges": graph["edge_count"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
