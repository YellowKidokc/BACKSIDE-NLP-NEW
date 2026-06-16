from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.config import settings
from app.models import (
    PAPER_MODEL_CATEGORIES,
    Axiom,
    AxiomMapping,
    EvidenceItem,
    GraphEdge,
    GraphNode,
    Paper,
    PaperModelItem,
    PaperScore,
)
from app.services.classification import paper_classification
from app.services.knowledge_graph import (
    build_paper_knowledge_graph,
    build_series_knowledge_graph,
)

STOPWORDS = {
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


def write_structured_export(db: Session) -> Path:
    payload = build_structured_payload(db)
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_dir = settings.export_dir / "json"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"treaties-structured-export-{stamp}.json"
    latest_path = out_dir / "latest.json"
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    out_path.write_text(text, encoding="utf-8")
    latest_path.write_text(text, encoding="utf-8")
    _write_seven_q_artifacts(payload, stamp)
    _write_knowledge_graph_artifacts(db, payload, stamp)
    return out_path


def build_structured_payload(db: Session) -> dict:
    papers = db.query(Paper).order_by(Paper.id).all()
    axioms = db.query(Axiom).order_by(Axiom.id).all()
    nodes = db.query(GraphNode).order_by(GraphNode.id).all()
    edges = db.query(GraphEdge).order_by(GraphEdge.id).all()

    items_by_paper: dict[int, list[PaperModelItem]] = defaultdict(list)
    for item in db.query(PaperModelItem).order_by(PaperModelItem.id):
        items_by_paper[item.paper_id].append(item)

    evidence_by_paper: dict[int, list[EvidenceItem]] = defaultdict(list)
    for evidence in db.query(EvidenceItem).order_by(EvidenceItem.id):
        evidence_by_paper[evidence.paper_id].append(evidence)

    mappings_by_paper: dict[int, list[AxiomMapping]] = defaultdict(list)
    mappings_by_axiom: dict[int, list[AxiomMapping]] = defaultdict(list)
    for mapping in db.query(AxiomMapping).order_by(AxiomMapping.id):
        mappings_by_paper[mapping.paper_id].append(mapping)
        mappings_by_axiom[mapping.axiom_id].append(mapping)

    scores_by_paper = {
        score.paper_id: score for score in db.query(PaperScore).order_by(PaperScore.id)
    }

    return {
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "export_root": str(settings.export_dir),
        "html_dir": str(settings.export_dir / "html"),
        "json_dir": str(settings.export_dir / "json"),
        "cache_dir": str(settings.export_dir / "cache"),
        "counts": {
            "papers": len(papers),
            "axioms": len(axioms),
            "paper_model_items": sum(len(rows) for rows in items_by_paper.values()),
            "evidence_items": sum(len(rows) for rows in evidence_by_paper.values()),
            "axiom_mappings": sum(len(rows) for rows in mappings_by_paper.values()),
            "graph_nodes": len(nodes),
            "graph_edges": len(edges),
            "seven_q_survivor_claims": sum(
                1
                for paper in papers
                for item in items_by_paper[paper.id]
                if _seven_q_check(
                    item,
                    items_by_paper[paper.id],
                    _evidence_for_claim(item, evidence_by_paper[paper.id]),
                    mappings_by_paper[paper.id],
                )["survived"]
            ),
        },
        "papers": [
            _paper_payload(
                paper,
                items_by_paper[paper.id],
                evidence_by_paper[paper.id],
                mappings_by_paper[paper.id],
                scores_by_paper.get(paper.id),
            )
            for paper in papers
        ],
        "axioms": [
            _axiom_payload(axiom, mappings_by_axiom[axiom.id])
            for axiom in axioms
        ],
        "graph": {
            "nodes": [
                {
                    "id": node.id,
                    "type": node.node_type,
                    "label": node.label,
                    "description": node.description,
                    "paper_id": node.paper_id,
                    "ref_table": node.ref_table,
                    "ref_id": node.ref_id,
                }
                for node in nodes
            ],
            "edges": [
                {
                    "id": edge.id,
                    "source_node_id": edge.source_node_id,
                    "target_node_id": edge.target_node_id,
                    "relationship_type": edge.relationship_type,
                    "strength": edge.strength,
                    "confidence": edge.confidence,
                    "explanation": edge.explanation,
                    "source_quote": edge.source_quote,
                }
                for edge in edges
            ],
        },
    }


def _write_knowledge_graph_artifacts(db: Session, payload: dict, stamp: str) -> None:
    out_dir = settings.export_dir / "json"
    paper_graphs = []
    for paper_payload in payload["papers"]:
        paper = db.get(Paper, paper_payload["id"])
        if paper is None:
            continue
        items = (
            db.query(PaperModelItem)
            .filter(PaperModelItem.paper_id == paper.id)
            .order_by(PaperModelItem.id)
            .all()
        )
        evidence = (
            db.query(EvidenceItem)
            .filter(EvidenceItem.paper_id == paper.id)
            .order_by(EvidenceItem.id)
            .all()
        )
        mappings = (
            db.query(AxiomMapping)
            .filter(AxiomMapping.paper_id == paper.id)
            .order_by(AxiomMapping.id)
            .all()
        )
        graph = build_paper_knowledge_graph(paper, items, evidence, mappings)
        paper_graphs.append(graph)
        graph_text = json.dumps(graph, indent=2, ensure_ascii=False)
        (out_dir / f"paper-{paper.id}-knowledge-graph-latest.json").write_text(
            graph_text, encoding="utf-8"
        )
        (out_dir / f"paper-{paper.id}-knowledge-graph-{stamp}.json").write_text(
            graph_text, encoding="utf-8"
        )

    series_graph = build_series_knowledge_graph(db)
    series_text = json.dumps(series_graph, indent=2, ensure_ascii=False)
    (out_dir / "knowledge-graph-latest.json").write_text(series_text, encoding="utf-8")
    (out_dir / f"knowledge-graph-{stamp}.json").write_text(series_text, encoding="utf-8")

    contract = {
        "generated_at": payload["generated_at"],
        "status": "ready",
        "contract_version": series_graph["contract_version"],
        "files": {
            "structured_export": "latest.json",
            "series_knowledge_graph": "knowledge-graph-latest.json",
            "seven_q_claims": "seven-q-claims-latest.json",
            "paper_knowledge_graphs": [
                {
                    "paper_id": graph["paper_id"],
                    "paper_title": graph["paper_title"],
                    "file": f"paper-{graph['paper_id']}-knowledge-graph-latest.json",
                }
                for graph in paper_graphs
            ],
        },
        "page_consumes": [
            "paper_snapshot",
            "graph_nodes",
            "graph_edges",
            "axiom_map",
            "classification",
            "seven_q_claims",
            "understand_anything",
        ],
        "adapter_boundaries": {
            "treaties": "active source for this export",
            "graphify": "known path, import adapter still pending",
            "understand_anything": "known path, import adapter still pending",
        },
    }
    contract_text = json.dumps(contract, indent=2, ensure_ascii=False)
    (out_dir / "graph-contract-latest.json").write_text(contract_text, encoding="utf-8")
    (out_dir / f"graph-contract-{stamp}.json").write_text(contract_text, encoding="utf-8")


def _paper_payload(
    paper: Paper,
    items: list[PaperModelItem],
    evidence: list[EvidenceItem],
    mappings: list[AxiomMapping],
    score: PaperScore | None,
) -> dict:
    classification = paper_classification(paper, items, mappings, score)
    return {
        "id": paper.id,
        "title": paper.title,
        "authors": paper.authors,
        "year": paper.year,
        "doi": paper.doi,
        "source_path": paper.source_path,
        "uuid_metadata": classification.as_dict(),
        "html_file": f"html/paper-{paper.id}-{_slugify(paper.title or 'paper')}.html",
        "derived_keywords": _derived_keywords(items, evidence, limit=20),
        "seven_q_claims": _seven_q_claims(items, evidence, mappings),
        "model_items": [
            {
                "id": item.id,
                "category": item.category,
                "claim": item.claim,
                "source_quote": item.source_quote,
                "confidence": item.confidence,
                "uncertainty_note": item.uncertainty_note,
            }
            for item in items
        ],
        "evidence": [
            {
                "id": row.id,
                "claim_id": row.claim_id,
                "evidence_type": row.evidence_type,
                "evidence_text": row.evidence_text,
                "source_quote": row.source_quote,
                "strength_score": row.strength_score,
                "weakness_note": row.weakness_note,
            }
            for row in evidence
        ],
        "axiom_mappings": [
            {
                "id": mapping.id,
                "axiom_id": mapping.axiom_id,
                "axiom_name": mapping.axiom.name,
                "interpretation": mapping.interpretation,
                "source_quote": mapping.source_quote,
                "confidence": mapping.confidence,
            }
            for mapping in mappings
        ],
        "score": None
        if score is None
        else {
            "overall_score": score.overall_score,
            "methodological_rigor": score.methodological_rigor,
            "evidence_strength": score.evidence_strength,
            "reproducibility": score.reproducibility,
            "clarity": score.clarity,
            "bias_risk": score.bias_risk,
            "signals": score.signals,
            "scoring_notes": score.scoring_notes,
        },
    }


def _write_seven_q_artifacts(payload: dict, stamp: str) -> None:
    out_dir = settings.export_dir / "json"
    survivors = []
    rejected = []
    for paper in payload["papers"]:
        seven_q = paper["seven_q_claims"]
        for row in seven_q["survivors"]:
            survivors.append(
                {
                    "paper_id": paper["id"],
                    "paper_title": paper["title"],
                    **row,
                }
            )
        for row in seven_q["rejected"]:
            rejected.append(
                {
                    "paper_id": paper["id"],
                    "paper_title": paper["title"],
                    **row,
                }
            )

    seven_q_payload = {
        "generated_at": payload["generated_at"],
        "method": "deterministic_proxy_from_extracted_fields",
        "status_note": (
            "Claims listed under survivors are what the current export layer thinks made it "
            "through the 7Q gauntlet. This is not yet the canonical NLP 7Q worker."
        ),
        "candidate_count": len(survivors) + len(rejected),
        "survivor_count": len(survivors),
        "rejected_count": len(rejected),
        "survivors": survivors,
        "rejected": rejected,
    }
    text = json.dumps(seven_q_payload, indent=2, ensure_ascii=False)
    (out_dir / "seven-q-claims-latest.json").write_text(text, encoding="utf-8")
    (out_dir / f"seven-q-claims-{stamp}.json").write_text(text, encoding="utf-8")


def _seven_q_claims(
    items: list[PaperModelItem],
    evidence: list[EvidenceItem],
    mappings: list[AxiomMapping],
) -> dict:
    rows = [
        _seven_q_check(item, items, _evidence_for_claim(item, evidence), mappings)
        for item in items
    ]
    survivors = [row for row in rows if row["survived"]]
    return {
        "method": "deterministic_proxy_from_extracted_fields",
        "status_note": (
            "This is the export-side 7Q gate over extracted claim rows. "
            "Replace with canonical NLP 7Q adjudication when that workflow is wired."
        ),
        "candidate_count": len(rows),
        "survivor_count": len(survivors),
        "survivors": survivors,
        "rejected": [row for row in rows if not row["survived"]],
    }


def _seven_q_check(
    item: PaperModelItem,
    paper_items: list[PaperModelItem],
    evidence: list[EvidenceItem],
    mappings: list[AxiomMapping],
) -> dict:
    categories = {row.category for row in paper_items}
    mapping_names = [mapping.axiom.name for mapping in mappings]
    text = " ".join(
        [
            item.claim or "",
            item.source_quote or "",
            item.uncertainty_note or "",
            " ".join(row.evidence_text for row in evidence),
            " ".join(row.source_quote or "" for row in evidence),
            " ".join(mapping.interpretation for mapping in mappings),
        ]
    ).lower()

    checks = [
        _q("Q1_claim", item.category in PAPER_MODEL_CATEGORIES and len(item.claim.strip()) >= 20),
        _q("Q2_attribution", bool((item.source_quote or "").strip())),
        _q("Q3_evidence", bool(evidence)),
        _q(
            "Q4_mechanism_or_operational_context",
            item.category in {"method", "variables", "mechanism"}
            or bool(categories & {"method", "variables", "mechanism"})
            or _contains_any(text, ("mechanism", "method", "variable", "measured", "experiment")),
        ),
        _q(
            "Q5_limitation_or_kill_condition",
            item.category == "limitations"
            or bool((item.uncertainty_note or "").strip())
            or "limitations" in categories
            or _contains_any(text, ("falsif", "refute", "kill condition", "would fail", "uncertain")),
        ),
        _q("Q6_axiom_or_framework_mapping", bool(mappings)),
        _q(
            "Q7_exportable_confidence",
            (item.confidence or 0.0) >= 0.6 and (bool(evidence) or bool(item.source_quote)),
        ),
    ]
    failed = [check["question"] for check in checks if not check["pass"]]

    return {
        "claim_id": item.id,
        "category": item.category,
        "claim": item.claim,
        "source_quote": item.source_quote,
        "confidence": item.confidence,
        "uncertainty_note": item.uncertainty_note,
        "mapped_axioms": mapping_names,
        "evidence": [
            {
                "id": row.id,
                "evidence_type": row.evidence_type,
                "evidence_text": row.evidence_text,
                "source_quote": row.source_quote,
                "strength_score": row.strength_score,
                "weakness_note": row.weakness_note,
            }
            for row in evidence
        ],
        "seven_q": checks,
        "survived": not failed,
        "failed_questions": failed,
    }


def _evidence_for_claim(
    item: PaperModelItem, evidence: list[EvidenceItem]
) -> list[EvidenceItem]:
    linked = [row for row in evidence if row.claim_id == item.id]
    if linked:
        return linked

    claim_tokens = _token_set(item.claim)
    fuzzy_matches = []
    for row in evidence:
        row_tokens = _token_set(" ".join([row.evidence_text, row.source_quote or ""]))
        if not claim_tokens or not row_tokens:
            continue
        overlap = len(claim_tokens & row_tokens) / max(1, len(claim_tokens))
        if overlap >= 0.35:
            fuzzy_matches.append(row)
    return fuzzy_matches


def _q(question: str, passed: bool) -> dict:
    return {"question": question, "pass": bool(passed)}


def _contains_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(needle in text for needle in needles)


def _token_set(text: str) -> set[str]:
    return {
        word
        for word in re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", text.lower())
        if word not in STOPWORDS
    }


def _axiom_payload(axiom: Axiom, mappings: list[AxiomMapping]) -> dict:
    return {
        "id": axiom.id,
        "name": axiom.name,
        "category": axiom.category,
        "description": axiom.description,
        "html_file": f"html/axiom-{axiom.id}-{_slugify(axiom.name)}.html",
        "mapped_papers": [
            {
                "paper_id": mapping.paper_id,
                "paper_title": mapping.paper.title,
                "interpretation": mapping.interpretation,
                "source_quote": mapping.source_quote,
                "confidence": mapping.confidence,
            }
            for mapping in mappings
        ],
    }


def _derived_keywords(
    items: list[PaperModelItem], evidence: list[EvidenceItem], limit: int
) -> list[str]:
    text = " ".join(
        [item.claim for item in items]
        + [item.source_quote or "" for item in items]
        + [row.evidence_text for row in evidence]
        + [row.source_quote or "" for row in evidence]
    )
    words = [
        word
        for word in re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", text.lower())
        if word not in STOPWORDS
    ]
    return [word for word, _ in Counter(words).most_common(limit)]


def _slugify(value: str) -> str:
    keep = "-_."
    return "".join(c if c.isalnum() or c in keep else "-" for c in value)[:80] or "item"
