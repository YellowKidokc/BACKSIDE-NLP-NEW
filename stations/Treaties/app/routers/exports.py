from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.exporter import write_structured_export

router = APIRouter(prefix="/exports", tags=["exports"])


@router.post("/structured")
def make_structured_export(db: Session = Depends(get_db)) -> dict:
    out_path = write_structured_export(db)
    return {"ok": True, "path": str(out_path)}
