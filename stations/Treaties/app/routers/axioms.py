from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Axiom
from app.schemas import AxiomCreate, AxiomOut
from app.services.snapshot import render_axiom_snapshot

router = APIRouter(prefix="/axioms", tags=["axioms"])


@router.get("", response_model=list[AxiomOut])
def list_axioms(db: Session = Depends(get_db)) -> list[Axiom]:
    return db.query(Axiom).order_by(Axiom.id).all()


@router.post("", response_model=AxiomOut)
def create_axiom(payload: AxiomCreate, db: Session = Depends(get_db)) -> Axiom:
    axiom = Axiom(
        name=payload.name.strip(),
        category=payload.category,
        description=payload.description,
    )
    db.add(axiom)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(409, "axiom name already exists") from e
    db.refresh(axiom)
    return axiom


@router.delete("/{axiom_id}")
def delete_axiom(axiom_id: int, db: Session = Depends(get_db)) -> dict:
    axiom = db.get(Axiom, axiom_id)
    if axiom is None:
        raise HTTPException(404, "axiom not found")
    db.delete(axiom)
    db.commit()
    return {"ok": True}


@router.post("/{axiom_id}/snapshot")
def make_axiom_snapshot(axiom_id: int, db: Session = Depends(get_db)) -> dict:
    axiom = db.get(Axiom, axiom_id)
    if axiom is None:
        raise HTTPException(404, "axiom not found")
    html, out_path = render_axiom_snapshot(db, axiom)
    return {"ok": True, "bytes": len(html), "path": str(out_path)}


@router.get("/{axiom_id}/snapshot", response_class=HTMLResponse)
def view_axiom_snapshot(axiom_id: int, db: Session = Depends(get_db)) -> HTMLResponse:
    axiom = db.get(Axiom, axiom_id)
    if axiom is None:
        raise HTTPException(404, "axiom not found")
    html, _ = render_axiom_snapshot(db, axiom)
    return HTMLResponse(html)
