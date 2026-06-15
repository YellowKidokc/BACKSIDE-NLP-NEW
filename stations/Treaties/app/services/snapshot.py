"""Render a paper to a standalone HTML snapshot.

Pulls everything from Postgres, walks claims/evidence/axioms/score, renders a
single Jinja2 template, persists the rendered HTML to html_snapshots, and also
writes a file under settings.snapshot_dir for easy sharing.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy.orm import Session

from app.config import settings
from app.models import (
    Axiom,
    AxiomMapping,
    EvidenceItem,
    HtmlSnapshot,
    Paper,
    PaperModelItem,
    PaperScore,
)
from app.services.classification import paper_classification

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def _slugify(value: str) -> str:
    keep = "-_."
    return "".join(c if c.isalnum() or c in keep else "-" for c in value)[:80] or "paper"


def render_paper_snapshot(db: Session, paper: Paper) -> HtmlSnapshot:
    items: list[PaperModelItem] = (
        db.query(PaperModelItem).filter(PaperModelItem.paper_id == paper.id).all()
    )
    items_by_category: dict[str, list[PaperModelItem]] = defaultdict(list)
    for item in items:
        items_by_category[item.category].append(item)

    evidence_by_claim: dict[int | None, list[EvidenceItem]] = defaultdict(list)
    for ev in db.query(EvidenceItem).filter(EvidenceItem.paper_id == paper.id):
        evidence_by_claim[ev.claim_id].append(ev)

    mappings: list[AxiomMapping] = (
        db.query(AxiomMapping).filter(AxiomMapping.paper_id == paper.id).all()
    )
    score: PaperScore | None = (
        db.query(PaperScore).filter(PaperScore.paper_id == paper.id).one_or_none()
    )
    classification = paper_classification(paper, items, mappings, score)

    template = _env.get_template("snapshot.html")
    html = template.render(
        paper=paper,
        classification=classification,
        items_by_category=items_by_category,
        evidence_by_claim=evidence_by_claim,
        mappings=mappings,
        score=score,
        rendered_at=datetime.utcnow().isoformat(timespec="seconds"),
    )

    snapshot = HtmlSnapshot(paper_id=paper.id, snapshot_type="paper", html_content=html)
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    filename = f"paper-{paper.id}-{_slugify(paper.title or 'paper')}.html"
    _write_html_artifact(filename, html)

    return snapshot


def render_axiom_snapshot(db: Session, axiom: Axiom) -> tuple[str, Path]:
    mappings: list[AxiomMapping] = (
        db.query(AxiomMapping)
        .filter(AxiomMapping.axiom_id == axiom.id)
        .order_by(AxiomMapping.confidence.desc().nullslast(), AxiomMapping.id)
        .all()
    )

    paper_ids = [mapping.paper_id for mapping in mappings]
    evidence_by_paper: dict[int, list[EvidenceItem]] = defaultdict(list)
    if paper_ids:
        for evidence in db.query(EvidenceItem).filter(EvidenceItem.paper_id.in_(paper_ids)):
            evidence_by_paper[evidence.paper_id].append(evidence)

    template = _env.get_template("axiom_snapshot.html")
    html = template.render(
        axiom=axiom,
        mappings=mappings,
        evidence_by_paper=evidence_by_paper,
        rendered_at=datetime.utcnow().isoformat(timespec="seconds"),
    )

    out_path = _write_html_artifact(f"axiom-{axiom.id}-{_slugify(axiom.name)}.html", html)
    return html, out_path


def _write_html_artifact(filename: str, html: str) -> Path:
    export_path = settings.export_dir / "html" / filename
    export_path.write_text(html, encoding="utf-8")

    legacy_path = settings.snapshot_dir / filename
    if legacy_path.resolve() != export_path.resolve():
        legacy_path.write_text(html, encoding="utf-8")

    return export_path
