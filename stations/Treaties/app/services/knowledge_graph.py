from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Iterable

from sqlalchemy.orm import Session

from app.models import AxiomMapping, EvidenceItem, Paper, PaperModelItem
from app.services.classification import paper_classification


GRAPH_CONTRACT_VERSION = "treaties.knowledge_graph.v0"


def build_paper_knowledge_graph(
    paper: Paper,
    items: list[PaperModelItem],
    evidence: list[EvidenceItem],
    mappings: list[AxiomMapping],
) -> dict:
    """Build the JSON graph surface consumed by the axiom-page UI."""

    classification = paper_classification(paper, items, mappings, None)
    nodes: list[dict] = []
    edges: list[dict] = []
    seen_nodes: set[str] = set()
    seen_edges: set[tuple[str, str, str]] = set()

    def add_node(node_id: str, node_type: str, label: str, **attrs: object) -> None:
        if node_id in seen_nodes:
            return
        seen_nodes.add(node_id)
        payload = {"id": node_id, "type": node_type, "label": label}
        payload.update(attrs)
        nodes.append(payload)

    def add_edge(source: str, target: str, edge_type: str, **attrs: object) -> None:
        key = (source, target, edge_type)
        if key in seen_edges:
            return
        seen_edges.add(key)
        payload = {"source": source, "target": target, "type": edge_type}
        payload.update(attrs)
        edges.append(payload)

    paper_id = f"paper:{paper.id}"
    add_node(
        paper_id,
        "Paper",
        paper.title or f"Paper {paper.id}",
        paper_id=paper.id,
        canonical_filename=classification.canonical_filename,
        uuid=classification.uuid,
        series=classification.series,
    )

    evidence_by_claim: dict[int | None, list[EvidenceItem]] = {}
    for row in evidence:
        evidence_by_claim.setdefault(row.claim_id, []).append(row)

    for item in items:
        claim_id = f"claim:{item.id}"
        add_node(
            claim_id,
            "Claim",
            _trim(item.claim, 140),
            claim_id=item.id,
            category=item.category,
            confidence=item.confidence,
            source_quote=_trim(item.source_quote, 300),
            uncertainty_note=_trim(item.uncertainty_note, 240),
        )
        add_edge(paper_id, claim_id, "PAPER_HAS_CLAIM", category=item.category)

        category_id = f"category:{_slug(item.category)}"
        add_node(category_id, "Category", item.category)
        add_edge(claim_id, category_id, "CLAIM_IN_CATEGORY")

        for row in evidence_by_claim.get(item.id, []):
            evidence_id = f"evidence:{row.id}"
            add_node(
                evidence_id,
                "Evidence",
                _trim(row.evidence_text, 140),
                evidence_id=row.id,
                evidence_type=row.evidence_type,
                strength_score=row.strength_score,
                weakness_note=_trim(row.weakness_note, 240),
                source_quote=_trim(row.source_quote, 300),
            )
            add_edge(
                claim_id,
                evidence_id,
                "CLAIM_SUPPORTED_BY_EVIDENCE",
                strength=row.strength_score,
            )

    for row in evidence_by_claim.get(None, []):
        evidence_id = f"evidence:{row.id}"
        add_node(
            evidence_id,
            "Evidence",
            _trim(row.evidence_text, 140),
            evidence_id=row.id,
            evidence_type=row.evidence_type,
            strength_score=row.strength_score,
        )
        add_edge(paper_id, evidence_id, "PAPER_HAS_UNLINKED_EVIDENCE")

    for mapping in mappings:
        axiom_id = f"axiom:{mapping.axiom_id}"
        add_node(
            axiom_id,
            "Axiom",
            mapping.axiom.name,
            axiom_id=mapping.axiom_id,
            category=mapping.axiom.category,
            description=_trim(mapping.axiom.description, 300),
        )
        add_edge(
            paper_id,
            axiom_id,
            "PAPER_MAPS_TO_AXIOM",
            confidence=mapping.confidence,
            interpretation=_trim(mapping.interpretation, 300),
            source_quote=_trim(mapping.source_quote, 300),
        )

        for item in _claim_matches_mapping(items, mapping):
            add_edge(
                f"claim:{item.id}",
                axiom_id,
                "CLAIM_MAPS_TO_AXIOM",
                confidence=mapping.confidence,
            )

    for keyword, weight in _keyword_counts(items, evidence).most_common(24):
        keyword_id = f"keyword:{_slug(keyword)}"
        add_node(keyword_id, "Keyword", keyword, weight=weight)
        add_edge(paper_id, keyword_id, "PAPER_HAS_KEYWORD", weight=weight)
        for item in items:
            text = f"{item.claim} {item.source_quote or ''}".lower()
            if keyword in text:
                add_edge(f"claim:{item.id}", keyword_id, "CLAIM_HAS_KEYWORD")

    return {
        "contract_version": GRAPH_CONTRACT_VERSION,
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "scope": "paper",
        "paper_id": paper.id,
        "paper_title": paper.title,
        "canonical_filename": classification.canonical_filename,
        "uuid": classification.uuid,
        "source_adapters": {
            "treaties": {
                "status": "active",
                "source": "Postgres paper model, evidence, axiom mappings, and classifier output",
            },
            "graphify": {
                "status": "available_not_ingested",
                "path_hint": r"\\dlowenas\brain\graphify",
            },
            "understand_anything": {
                "status": "available_not_ingested",
                "path_hint": r"\\dlowenas\brain\Understand-Anything",
            },
        },
        "counts": {
            "nodes": len(nodes),
            "edges": len(edges),
            "claims": len(items),
            "evidence": len(evidence),
            "axiom_mappings": len(mappings),
        },
        "nodes": nodes,
        "edges": edges,
    }


def build_series_knowledge_graph(db: Session) -> dict:
    papers = db.query(Paper).order_by(Paper.id).all()
    nodes: list[dict] = []
    edges: list[dict] = []
    seen_nodes: set[str] = set()
    seen_edges: set[tuple[str, str, str]] = set()

    def add_node(node_id: str, node_type: str, label: str, **attrs: object) -> None:
        if node_id in seen_nodes:
            return
        seen_nodes.add(node_id)
        payload = {"id": node_id, "type": node_type, "label": label}
        payload.update(attrs)
        nodes.append(payload)

    def add_edge(source: str, target: str, edge_type: str, **attrs: object) -> None:
        key = (source, target, edge_type)
        if key in seen_edges:
            return
        seen_edges.add(key)
        payload = {"source": source, "target": target, "type": edge_type}
        payload.update(attrs)
        edges.append(payload)

    add_node("series:all", "Series", "Treaties Paper Series")
    for paper in papers:
        items = db.query(PaperModelItem).filter(PaperModelItem.paper_id == paper.id).all()
        evidence = db.query(EvidenceItem).filter(EvidenceItem.paper_id == paper.id).all()
        mappings = db.query(AxiomMapping).filter(AxiomMapping.paper_id == paper.id).all()
        graph = build_paper_knowledge_graph(paper, items, evidence, mappings)
        paper_node = f"paper:{paper.id}"
        add_node(
            paper_node,
            "Paper",
            paper.title or f"Paper {paper.id}",
            paper_id=paper.id,
            canonical_filename=graph["canonical_filename"],
            uuid=graph["uuid"],
        )
        add_edge("series:all", paper_node, "SERIES_HAS_PAPER")
        for node in graph["nodes"]:
            add_node(**_node_kwargs(node))
        for edge in graph["edges"]:
            add_edge(edge["source"], edge["target"], edge["type"], **_edge_attrs(edge))

    return {
        "contract_version": GRAPH_CONTRACT_VERSION,
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "scope": "series",
        "series": "all",
        "counts": {"papers": len(papers), "nodes": len(nodes), "edges": len(edges)},
        "nodes": nodes,
        "edges": edges,
    }


def _node_kwargs(node: dict) -> dict:
    attrs = {key: value for key, value in node.items() if key not in {"id", "type", "label"}}
    return {"node_id": node["id"], "node_type": node["type"], "label": node["label"], **attrs}


def _edge_attrs(edge: dict) -> dict:
    return {key: value for key, value in edge.items() if key not in {"source", "target", "type"}}


def _claim_matches_mapping(
    items: Iterable[PaperModelItem], mapping: AxiomMapping
) -> list[PaperModelItem]:
    mapping_text = f"{mapping.interpretation} {mapping.source_quote or ''}".lower()
    matches = []
    for item in items:
        item_tokens = set(_words(f"{item.claim} {item.source_quote or ''}"))
        if not item_tokens:
            continue
        overlap = item_tokens & set(_words(mapping_text))
        if len(overlap) >= 3:
            matches.append(item)
    return matches[:5]


def _keyword_counts(items: list[PaperModelItem], evidence: list[EvidenceItem]) -> Counter:
    text = " ".join(
        [item.claim for item in items]
        + [item.source_quote or "" for item in items]
        + [row.evidence_text for row in evidence]
        + [row.source_quote or "" for row in evidence]
    )
    return Counter(_words(text))


def _words(text: str) -> list[str]:
    import re

    stopwords = {
        "about",
        "after",
        "also",
        "because",
        "between",
        "from",
        "into",
        "paper",
        "that",
        "their",
        "there",
        "these",
        "this",
        "through",
        "with",
        "would",
    }
    return [
        word
        for word in re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", text.lower())
        if word not in stopwords
    ]


def _slug(value: object) -> str:
    import re

    text = str(value or "unknown").lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-") or "unknown"


def _trim(value: object, limit: int) -> str | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."
