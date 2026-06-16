#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


REQUIRED_NODE_TYPES = [
    "Paper",
    "Claim",
    "Tag",
    "Law",
    "Axiom",
    "Evidence",
    "DefeatCondition",
    "DerivationStep",
    "StationRun",
    "TranslatedSpan",
]

REQUIRED_EDGE_TYPES = [
    "PAPER_HAS_CLAIM",
    "PAPER_HAS_TAG",
    "CLAIM_MAPS_TO_LAW",
    "CLAIM_MAPS_TO_AXIOM",
    "CLAIM_SUPPORTED_BY",
    "CLAIM_DEPENDS_ON",
    "CLAIM_HAS_DEFEAT_CONDITION",
    "CLAIM_DERIVED_BY",
    "STATION_PROCESSED_PAPER",
    "TRANSLATED_SPAN_IN_CLAIM",
]


def slugify(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "unknown"


def ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_mapping(value: Any) -> List[str]:
    items = []
    for item in ensure_list(value):
        if isinstance(item, dict):
            candidate = item.get("id") or item.get("name") or item.get("label") or item.get("value")
            if candidate:
                items.append(str(candidate))
        elif item not in (None, ""):
            items.append(str(item))
    seen = set()
    ordered = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def get_claim_ref(value: Any) -> Optional[str]:
    if isinstance(value, dict):
        for key in ("claim_id", "id", "target_claim_id", "ref", "target_id"):
            if value.get(key):
                return str(value[key])
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


class GraphBuilder:
    def __init__(self, snapshot: Dict[str, Any], snapshot_path: Path) -> None:
        self.snapshot = snapshot
        self.snapshot_path = snapshot_path
        self.paper_id = str(snapshot.get("snapshot_id") or snapshot.get("source_id") or snapshot_path.stem)
        self.paper_node_id = f"paper::{slugify(self.paper_id)}"
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []
        self.warnings: List[str] = []
        self.claim_index: Dict[str, str] = {}
        self.translated_span_index: Dict[str, Dict[str, Any]] = {}
        self._add_paper_node()

    def _add_node(self, node_type: str, key: str, label: str, **attrs: Any) -> str:
        node_id = f"{node_type.lower()}::{slugify(key)}"
        payload = {"id": node_id, "label": label, "node_type": node_type}
        payload.update(attrs)
        self.nodes[node_id] = payload
        return node_id

    def _add_edge(self, edge_type: str, source: str, target: str, **attrs: Any) -> None:
        payload = {"source": source, "target": target, "edge_type": edge_type}
        payload.update(attrs)
        self.edges.append(payload)

    def _add_paper_node(self) -> None:
        identity_section = self.snapshot.get("identity", {})
        source_section = self.snapshot.get("source", {})
        identity = self.snapshot
        seven_qs = self.snapshot.get("seven_qs", {})
        q2 = seven_qs.get("q2_location", {}) if isinstance(seven_qs, dict) else {}
        canon_location = (
            identity.get("canon_location")
            or identity.get("canonical_location")
            or identity.get("canon_folder_route")
            or identity_section.get("canon_location")
            or identity_section.get("canonical_location")
            or identity_section.get("canon_folder_route")
            or q2.get("answer")
        )
        self.nodes[self.paper_node_id] = {
            "id": self.paper_node_id,
            "label": identity.get("title") or identity_section.get("title") or self.paper_id,
            "node_type": "Paper",
            "paper_id": self.paper_id,
            "snapshot_id": identity.get("snapshot_id"),
            "source_id": identity.get("source_id") or source_section.get("source_id"),
            "source_path": identity.get("source_path") or source_section.get("source_path") or source_section.get("selected_source_path"),
            "title": identity.get("title") or identity_section.get("title"),
            "series": identity.get("series") or identity_section.get("series"),
            "article_number": identity.get("article_number") or identity_section.get("article_number"),
            "author": identity.get("author") or identity_section.get("author"),
            "canonical_status": identity.get("canonical_status") or identity_section.get("canonical_status"),
            "input_format": identity.get("input_format") or source_section.get("input_format"),
            "output_formats": ensure_list(identity.get("output_formats") or source_section.get("output_formats")),
            "canon_location": canon_location,
            "source_file": str(self.snapshot_path),
        }

    def _collect_tags(self) -> None:
        tags = self.snapshot.get("tags") or self.snapshot.get("graph_tags") or {}
        if not isinstance(tags, dict):
            self.warnings.append("Snapshot tags section is missing or not an object.")
            return
        for group_name, values in tags.items():
            for raw in ensure_list(values):
                if not raw:
                    continue
                label = str(raw)
                tag_node_id = self._add_node(
                    "Tag",
                    f"{group_name}:{label}",
                    label,
                    tag_group=group_name,
                    canon_location=self.nodes[self.paper_node_id].get("canon_location"),
                )
                self._add_edge("PAPER_HAS_TAG", self.paper_node_id, tag_node_id, tag_group=group_name)

    def _collect_claims(self) -> None:
        claims = ensure_list(self.snapshot.get("claims"))
        if not claims:
            self.warnings.append("Snapshot has no claims array.")
            return
        claim_rows: List[Tuple[str, str, Dict[str, Any]]] = []
        for index, claim in enumerate(claims, start=1):
            claim_id = str(claim.get("claim_id") or f"{self.paper_id}-claim-{index}")
            node_id = self._add_node(
                "Claim",
                claim_id,
                claim.get("text") or claim_id,
                claim_id=claim_id,
                normalized_text=claim.get("normalized_text"),
                claim_type=claim.get("claim_type"),
                status=claim.get("status"),
                epistemic_tier=claim.get("epistemic_tier"),
                confidence=claim.get("confidence"),
                source_span=claim.get("source_span"),
                source_section=claim.get("source_section"),
            )
            self.claim_index[claim_id] = node_id
            self._add_edge("PAPER_HAS_CLAIM", self.paper_node_id, node_id)
            claim_rows.append((claim_id, node_id, claim))

        for claim_id, node_id, claim in claim_rows:

            for law in self._claim_law_mappings(claim):
                law_node_id = self._add_node("Law", law, law, law_id=law)
                self._add_edge("CLAIM_MAPS_TO_LAW", node_id, law_node_id)

            for axiom in self._claim_axiom_mappings(claim):
                axiom_node_id = self._add_node("Axiom", axiom, axiom, axiom_id=axiom)
                self._add_edge("CLAIM_MAPS_TO_AXIOM", node_id, axiom_node_id)

            for evidence_index, evidence in enumerate(ensure_list(claim.get("supporting_evidence")), start=1):
                evidence_id, evidence_label, evidence_attrs = self._normalize_supporting_item(
                    evidence, "evidence", claim_id, evidence_index
                )
                evidence_node_id = self._add_node("Evidence", evidence_id, evidence_label, **evidence_attrs)
                self._add_edge("CLAIM_SUPPORTED_BY", node_id, evidence_node_id)

            for dependency_index, dependency in enumerate(ensure_list(claim.get("dependencies")), start=1):
                target_id = self._resolve_dependency_target(dependency, claim_id, dependency_index)
                if target_id:
                    self._add_edge("CLAIM_DEPENDS_ON", node_id, target_id)

            for defeat_index, defeat in enumerate(ensure_list(claim.get("defeat_conditions")), start=1):
                defeat_id, defeat_label, defeat_attrs = self._normalize_supporting_item(
                    defeat, "defeat", claim_id, defeat_index
                )
                defeat_node_id = self._add_node("DefeatCondition", defeat_id, defeat_label, **defeat_attrs)
                self._add_edge("CLAIM_HAS_DEFEAT_CONDITION", node_id, defeat_node_id)

            for derivation_index, step in enumerate(ensure_list(claim.get("derivation_chain")), start=1):
                step_id, step_label, step_attrs = self._normalize_derivation_step(
                    step, claim_id, derivation_index, claim.get("source_section")
                )
                step_node_id = self._add_node("DerivationStep", step_id, step_label, **step_attrs)
                self._add_edge("CLAIM_DERIVED_BY", node_id, step_node_id)

    def _claim_law_mappings(self, claim: Dict[str, Any]) -> List[str]:
        claim_specific = (
            claim.get("law_mapping")
            or claim.get("law_mappings")
            or claim.get("laws")
            or claim.get("graph_nodes", {}).get("laws")
            if isinstance(claim.get("graph_nodes"), dict)
            else claim.get("law_mapping") or claim.get("law_mappings") or claim.get("laws")
        )
        paper_level = (
            self.snapshot.get("method_passes", {})
            .get("seven_q_forward", {})
            .get("law_mapping")
            if isinstance(self.snapshot.get("method_passes"), dict)
            else None
        )
        tags_level = claim.get("tags", {}).get("laws") if isinstance(claim.get("tags"), dict) else None
        return normalize_mapping(claim_specific) or normalize_mapping(tags_level) or normalize_mapping(paper_level)

    def _claim_axiom_mappings(self, claim: Dict[str, Any]) -> List[str]:
        claim_specific = (
            claim.get("axiom_mapping")
            or claim.get("axiom_mappings")
            or claim.get("axioms")
            or claim.get("graph_nodes", {}).get("axioms")
            if isinstance(claim.get("graph_nodes"), dict)
            else claim.get("axiom_mapping") or claim.get("axiom_mappings") or claim.get("axioms")
        )
        paper_level = (
            self.snapshot.get("method_passes", {})
            .get("seven_q_forward", {})
            .get("axiom_mapping")
            if isinstance(self.snapshot.get("method_passes"), dict)
            else None
        )
        tags_level = claim.get("tags", {}).get("axioms") if isinstance(claim.get("tags"), dict) else None
        return normalize_mapping(claim_specific) or normalize_mapping(tags_level) or normalize_mapping(paper_level)

    def _normalize_supporting_item(
        self, item: Any, kind: str, claim_id: str, index: int
    ) -> Tuple[str, str, Dict[str, Any]]:
        if isinstance(item, dict):
            item_id = str(item.get(f"{kind}_id") or item.get("id") or f"{claim_id}-{kind}-{index}")
            label = str(item.get("text") or item.get("label") or item.get("name") or item_id)
            attrs = {k: v for k, v in item.items() if k not in {"text", "label", "name"}}
            return item_id, label, attrs
        item_id = f"{claim_id}-{kind}-{index}"
        label = str(item)
        return item_id, label, {"text": label}

    def _normalize_derivation_step(
        self, step: Any, claim_id: str, index: int, source_section: Optional[str]
    ) -> Tuple[str, str, Dict[str, Any]]:
        if isinstance(step, dict):
            step_id = str(step.get("step_id") or step.get("id") or f"{claim_id}-derivation-{index}")
            label = str(step.get("output") or step.get("premise") or step.get("label") or step_id)
            attrs = dict(step)
            return step_id, label, attrs
        step_id = f"{claim_id}-derivation-{index}"
        label = str(step)
        return step_id, label, {"premise": label, "source_section": source_section}

    def _resolve_dependency_target(self, dependency: Any, claim_id: str, index: int) -> Optional[str]:
        dep_ref = get_claim_ref(dependency)
        if dep_ref and dep_ref in self.claim_index:
            return self.claim_index[dep_ref]

        if isinstance(dependency, dict):
            dep_type = str(dependency.get("type") or dependency.get("target_type") or "").lower()
            dep_label = str(dependency.get("label") or dependency.get("name") or dependency.get("target_id") or dep_ref or "")
            if dep_type == "axiom" and dep_label:
                return self._add_node("Axiom", dep_label, dep_label, axiom_id=dep_label)
            if dep_type == "law" and dep_label:
                return self._add_node("Law", dep_label, dep_label, law_id=dep_label)

        if dep_ref:
            self.warnings.append(
                f"Claim {claim_id} dependency '{dep_ref}' did not resolve to an existing claim, axiom, or law."
            )
        else:
            self.warnings.append(f"Claim {claim_id} dependency #{index} had no resolvable target.")
        return None

    def _collect_derivations(self) -> None:
        derivations = ensure_list(self.snapshot.get("derivations"))
        for derivation in derivations:
            claim_ref = str(derivation.get("conclusion_claim_id") or "")
            claim_node_id = self.claim_index.get(claim_ref)
            previous_step_node_id: Optional[str] = None
            for index, step in enumerate(ensure_list(derivation.get("steps")), start=1):
                step_id, step_label, step_attrs = self._normalize_derivation_step(step, claim_ref or "paper", index, None)
                step_node_id = self._add_node("DerivationStep", step_id, step_label, derivation_id=derivation.get("derivation_id"), **step_attrs)
                if claim_node_id:
                    self._add_edge("CLAIM_DERIVED_BY", claim_node_id, step_node_id, derivation_id=derivation.get("derivation_id"))
                if previous_step_node_id:
                    self._add_edge("DERIVATION_STEP_NEXT", previous_step_node_id, step_node_id, derivation_id=derivation.get("derivation_id"))
                previous_step_node_id = step_node_id

    def _collect_station_marks(self) -> None:
        for index, station in enumerate(ensure_list(self.snapshot.get("station_marks")), start=1):
            station_id = str(station.get("station_id") or f"{self.paper_id}-station-{index}")
            label = str(station.get("station_name") or station_id)
            station_node_id = self._add_node(
                "StationRun",
                station_id,
                label,
                status=station.get("status"),
                started_at=station.get("started_at"),
                completed_at=station.get("completed_at"),
                input_hash=station.get("input_hash"),
                output_hash=station.get("output_hash"),
                changed_fields=ensure_list(station.get("changed_fields")),
                warnings=ensure_list(station.get("warnings")),
            )
            self._add_edge("STATION_PROCESSED_PAPER", station_node_id, self.paper_node_id)

    def _collect_translated_spans(self) -> None:
        math_layer = self.snapshot.get("math_translation_layer", {})
        if not isinstance(math_layer, dict):
            return
        for index, span in enumerate(ensure_list(math_layer.get("translated_spans")), start=1):
            span_id = str(span.get("span_id") or f"{self.paper_id}-translated-span-{index}")
            label = str(span.get("translated") or span.get("original") or span_id)
            span_node_id = self._add_node(
                "TranslatedSpan",
                span_id,
                label,
                original=span.get("original"),
                translated=span.get("translated"),
                source_location=span.get("source_location"),
                dictionary_terms=ensure_list(span.get("dictionary_terms")),
                confidence=span.get("confidence"),
                needs_review=span.get("needs_review"),
            )
            self.translated_span_index[span_id] = {"node_id": span_node_id, "span": span}

            claim_ref = span.get("claim_id")
            claim_node_id = self.claim_index.get(str(claim_ref)) if claim_ref else None
            if not claim_node_id and span.get("source_location"):
                claim_node_id = self._match_claim_by_source_location(str(span["source_location"]))
            if claim_node_id:
                self._add_edge("TRANSLATED_SPAN_IN_CLAIM", span_node_id, claim_node_id)
            else:
                self.warnings.append(
                    f"Translated span {span_id} did not resolve to a claim; add claim_id or a matching source_location."
                )

    def _match_claim_by_source_location(self, source_location: str) -> Optional[str]:
        for node_id, node in self.nodes.items():
            if node.get("node_type") == "Claim" and str(node.get("source_span") or "") == source_location:
                return node_id
        return None

    def build(self) -> Dict[str, Any]:
        self._collect_tags()
        self._collect_claims()
        self._collect_derivations()
        self._collect_station_marks()
        self._collect_translated_spans()
        return {
            "graph_nodes": sorted(self.nodes.values(), key=lambda item: item["id"]),
            "graph_edges": sorted(
                self.edges,
                key=lambda item: (item["edge_type"], item["source"], item["target"]),
            ),
            "graph_json": {
                "directed": True,
                "multigraph": False,
                "graph": {
                    "snapshot_id": self.snapshot.get("snapshot_id"),
                    "source_path": str(self.snapshot_path),
                },
                "nodes": sorted(self.nodes.values(), key=lambda item: item["id"]),
                "links": [
                    {
                        "source": edge["source"],
                        "target": edge["target"],
                        "relation": edge["edge_type"],
                        "confidence": "EXTRACTED",
                        "weight": 1.0,
                        "confidence_score": 1.0,
                        "source_file": str(self.snapshot_path),
                        "source_location": edge.get("source_location"),
                    }
                    for edge in sorted(
                        self.edges,
                        key=lambda item: (item["edge_type"], item["source"], item["target"]),
                    )
                ],
                "hyperedges": [],
            },
            "warnings": self.warnings,
        }


def missing_section_report(snapshot: Dict[str, Any]) -> List[str]:
    missing = []
    source = snapshot.get("source", {}) if isinstance(snapshot.get("source"), dict) else {}
    identity = snapshot.get("identity", {}) if isinstance(snapshot.get("identity"), dict) else {}
    required_paths = {
        "snapshot_id": snapshot.get("snapshot_id"),
        "source_id": snapshot.get("source_id") or source.get("source_id") or identity.get("source_id"),
        "source_path": snapshot.get("source_path") or source.get("source_path") or source.get("selected_source_path"),
        "title": snapshot.get("title") or identity.get("title"),
        "claims": snapshot.get("claims"),
        "tags": snapshot.get("tags") or snapshot.get("graph_tags"),
        "seven_qs": snapshot.get("seven_qs"),
        "method_passes": snapshot.get("method_passes"),
        "epistemic_status": snapshot.get("epistemic_status"),
        "derivations": snapshot.get("derivations"),
        "station_marks": snapshot.get("station_marks"),
        "math_translation_layer.translated_spans": snapshot.get("math_translation_layer", {}).get("translated_spans")
        if isinstance(snapshot.get("math_translation_layer"), dict)
        else None,
    }
    for key, value in required_paths.items():
        if value in (None, "", [], {}):
            missing.append(key)
    return missing


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a deterministic graph from one .paper-snapshot.json file.")
    parser.add_argument("snapshot", help="Path to the input .paper-snapshot.json file")
    parser.add_argument(
        "--output-dir",
        help="Directory for graph_nodes.json, graph_edges.json, graph.json, and export_report.json. Defaults next to the snapshot.",
    )
    args = parser.parse_args()

    snapshot_path = Path(args.snapshot).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else snapshot_path.parent / "graph-export"
    output_dir.mkdir(parents=True, exist_ok=True)

    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    builder = GraphBuilder(snapshot=snapshot, snapshot_path=snapshot_path)
    result = builder.build()
    missing = missing_section_report(snapshot)

    write_json(output_dir / "graph_nodes.json", result["graph_nodes"])
    write_json(output_dir / "graph_edges.json", result["graph_edges"])
    write_json(output_dir / "graph.json", result["graph_json"])
    write_json(
        output_dir / "export_report.json",
        {
            "input_snapshot": str(snapshot_path),
            "output_dir": str(output_dir),
            "required_node_types": REQUIRED_NODE_TYPES,
            "required_edge_types": REQUIRED_EDGE_TYPES,
            "node_count": len(result["graph_nodes"]),
            "edge_count": len(result["graph_edges"]),
            "missing_snapshot_sections": missing,
            "warnings": result["warnings"],
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
