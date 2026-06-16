from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Axiom, AxiomMapping, Paper, PaperComparison, PaperModelItem, PaperScore
from app.routers import axioms, compare, exports, graph, papers
from app.services.classification import paper_classification

app = FastAPI(title="Treaties — Research Intelligence Engine", version="0.1.0")

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

app.include_router(papers.router)
app.include_router(axioms.router)
app.include_router(graph.router)
app.include_router(compare.router)
app.include_router(exports.router)


@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "papers": db.query(Paper).order_by(Paper.id.desc()).all(),
            "axioms": db.query(Axiom).order_by(Axiom.id).all(),
            "comparisons": db.query(PaperComparison)
            .order_by(PaperComparison.id.desc())
            .limit(20)
            .all(),
        },
    )


@app.get("/papers/{paper_id}/view", response_class=HTMLResponse)
def paper_view(paper_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    paper = db.get(Paper, paper_id)
    if paper is None:
        return HTMLResponse("<h1>404</h1>", status_code=404)
    items = db.query(PaperModelItem).filter(PaperModelItem.paper_id == paper.id).all()
    mappings = db.query(AxiomMapping).filter(AxiomMapping.paper_id == paper.id).all()
    score = db.query(PaperScore).filter(PaperScore.paper_id == paper.id).one_or_none()
    classification = paper_classification(paper, items, mappings, score)
    return templates.TemplateResponse(
        request,
        "paper_detail.html",
        {"paper": paper, "classification": classification},
    )


@app.get("/health")
def health() -> dict:
    return {"ok": True}
