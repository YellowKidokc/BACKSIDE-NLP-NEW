"""
13_WEB_INTAKE — FastAPI wrapper around the Theophysics Paper Intelligence pipeline.

Routes:
  GET  /                     intake form
  POST /submit               accept name/title/domain/paper, kick off pipeline
  GET  /status/<paper_id>    JSON job state {status, error?}
  GET  /report/<paper_id>    HTML report when ready, progress page while running
  GET  /raw/<paper_id>       the saved markdown source

Run locally:
  uvicorn app:app --host 0.0.0.0 --port 8088
  (or use run.bat)
"""
from __future__ import annotations

import io
import json
import re
import sys
import threading
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ── Wire up the pipeline modules from the parent suite ────────────────────────
HERE = Path(__file__).resolve().parent
SUITE = HERE.parent
ORCHESTRATOR = SUITE / "00_ORCHESTRATOR"
HTML_REPORT_DIR = SUITE / "11_HTML_REPORT"

for p in (ORCHESTRATOR, HTML_REPORT_DIR):
    sp = str(p)
    if sp not in sys.path:
        sys.path.insert(0, sp)

# Imported lazily inside the worker thread so a missing dep on app boot
# doesn't kill the form. (Pipeline pulls in spaCy / sentence-transformers.)

# ── Local storage layout ──────────────────────────────────────────────────────
UPLOADS = HERE / "uploads"
REPORTS = HERE / "reports"
META    = HERE / "meta"
TEMPLATES_DIR = HERE / "templates"
STATIC_DIR = HERE / "static"

for d in (UPLOADS, REPORTS, META, TEMPLATES_DIR, STATIC_DIR):
    d.mkdir(parents=True, exist_ok=True)

DOMAIN_OPTIONS = [
    "Theophysics",
    "Cosmology",
    "Quantum Mechanics",
    "Thermodynamics",
    "Information Theory",
    "Consciousness",
    "Theology / Physics Bridge",
    "Philosophy",
    "Other",
]

# ── In-memory job tracker (process-local; v2 promotes to a sqlite/redis store)
JOBS: Dict[str, dict] = {}
JOBS_LOCK = threading.Lock()


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="Theophysics Paper Intake", version="0.1.0")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ── Helpers ───────────────────────────────────────────────────────────────────
def _slug(s: str, n: int = 40) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", (s or "")).strip("_").lower()
    return (s[:n] or "untitled")


def _new_paper_id(author: str, title: str) -> str:
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    return f"{ts}_{_slug(author, 20)}_{_slug(title, 30)}"


def _load_meta(paper_id: str) -> Optional[dict]:
    p = META / f"{paper_id}.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _save_meta(paper_id: str, data: dict) -> None:
    (META / f"{paper_id}.json").write_text(
        json.dumps(data, indent=2, default=str), encoding="utf-8"
    )


def _extract_pdf_text(raw: bytes) -> str:
    """PDF → plain text. Falls back to a hint if pypdf can't parse."""
    try:
        from pypdf import PdfReader
    except ImportError:
        return "[pypdf not installed — PDF extraction unavailable]"
    try:
        reader = PdfReader(io.BytesIO(raw))
        chunks = []
        for page in reader.pages:
            try:
                chunks.append(page.extract_text() or "")
            except Exception:
                continue
        return "\n\n".join(c.strip() for c in chunks if c).strip()
    except Exception as e:
        return f"[PDF parse failed: {e}]"


def _build_markdown(author: str, title: str, domain: str, body: str) -> str:
    front = (
        f"# {title}\n\n"
        f"**Author:** {author}  \n"
        f"**Domain:** {domain}  \n"
        f"**Submitted:** {datetime.now().isoformat(timespec='seconds')}  \n\n"
        f"---\n\n"
    )
    return front + (body or "").strip() + "\n"


def _set_status(paper_id: str, **fields) -> None:
    with JOBS_LOCK:
        job = JOBS.setdefault(paper_id, {})
        job.update(fields)
    meta = _load_meta(paper_id) or {}
    meta.update(fields)
    _save_meta(paper_id, meta)


def _run_pipeline_job(paper_id: str, paper_path: Path) -> None:
    """Background worker — runs analyze_paper, then generates the HTML report."""
    try:
        _set_status(paper_id, status="running", started_at=datetime.now().isoformat())

        # Import inside the worker so app boot stays cheap
        from run_pipeline import analyze_paper  # type: ignore
        from generate_report import generate_paper_html  # type: ignore

        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        row = analyze_paper(
            str(paper_path),
            run_openai=False,
            vault_output=str(REPORTS),
            series_id=f"WEB-{paper_id[:14]}",
            run_id=run_id,
        )

        # Persist the raw row JSON (so package C / B can reuse it later)
        row_path = REPORTS / f"{paper_id}_row.json"
        row_path.write_text(json.dumps(row, indent=2, default=str), encoding="utf-8")

        # Render the HTML scorecard
        html = generate_paper_html(row)
        html_path = REPORTS / f"{paper_id}.html"
        html_path.write_text(html, encoding="utf-8")

        _set_status(
            paper_id,
            status="complete",
            finished_at=datetime.now().isoformat(),
            html=str(html_path),
            row_json=str(row_path),
        )
    except Exception as e:
        tb = traceback.format_exc()
        _set_status(
            paper_id,
            status="error",
            error=str(e),
            traceback=tb,
            finished_at=datetime.now().isoformat(),
        )


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def intake_form(request: Request):
    return templates.TemplateResponse(
        "intake.html",
        {"request": request, "domains": DOMAIN_OPTIONS},
    )


@app.post("/submit")
async def submit(
    author: str = Form(...),
    title: str = Form(...),
    domain: str = Form(...),
    paper_text: str = Form(""),
    paper_file: Optional[UploadFile] = File(None),
):
    author = (author or "").strip() or "Anonymous"
    title  = (title or "").strip()  or "Untitled"
    domain = domain if domain in DOMAIN_OPTIONS else "Other"

    body = paper_text or ""
    if paper_file is not None and paper_file.filename:
        raw = await paper_file.read()
        if raw:
            name_low = paper_file.filename.lower()
            if name_low.endswith(".pdf"):
                body = _extract_pdf_text(raw)
            else:
                try:
                    body = raw.decode("utf-8", errors="replace")
                except Exception:
                    body = raw.decode("latin-1", errors="replace")

    if not body.strip():
        raise HTTPException(
            status_code=400,
            detail="Paper content is empty — paste text or upload a file.",
        )

    paper_id = _new_paper_id(author, title)
    md_path = UPLOADS / f"{paper_id}.md"
    md_path.write_text(_build_markdown(author, title, domain, body), encoding="utf-8")

    _save_meta(paper_id, {
        "paper_id":   paper_id,
        "author":     author,
        "title":      title,
        "domain":     domain,
        "submitted":  datetime.now().isoformat(timespec="seconds"),
        "source_md":  str(md_path),
        "status":     "queued",
    })
    with JOBS_LOCK:
        JOBS[paper_id] = {"status": "queued"}

    threading.Thread(
        target=_run_pipeline_job,
        args=(paper_id, md_path),
        daemon=True,
        name=f"pipeline-{paper_id}",
    ).start()

    return RedirectResponse(url=f"/report/{paper_id}", status_code=303)


@app.get("/status/{paper_id}")
def status(paper_id: str):
    with JOBS_LOCK:
        job = dict(JOBS.get(paper_id, {}))
    if not job:
        meta = _load_meta(paper_id) or {}
        if not meta:
            raise HTTPException(status_code=404, detail="unknown paper_id")
        job = {"status": meta.get("status", "unknown")}
    job.pop("traceback", None)  # keep the wire payload small
    return JSONResponse(job)


@app.get("/report/{paper_id}", response_class=HTMLResponse)
def report(request: Request, paper_id: str):
    meta = _load_meta(paper_id)
    with JOBS_LOCK:
        job = dict(JOBS.get(paper_id, {}))
    if not meta and not job:
        raise HTTPException(status_code=404, detail="unknown paper_id")

    state = (job.get("status") or (meta or {}).get("status") or "queued")

    if state == "complete":
        html_path = REPORTS / f"{paper_id}.html"
        if html_path.exists():
            return HTMLResponse(html_path.read_text(encoding="utf-8"))
        # Inconsistent state — fall through to progress so worker can finish writing
        state = "running"

    if state == "error":
        return templates.TemplateResponse(
            "error.html",
            {
                "request":  request,
                "paper_id": paper_id,
                "meta":     meta or {},
                "error":    job.get("error") or (meta or {}).get("error") or "unknown",
                "trace":    job.get("traceback") or (meta or {}).get("traceback") or "",
            },
            status_code=500,
        )

    return templates.TemplateResponse(
        "progress.html",
        {
            "request":  request,
            "paper_id": paper_id,
            "meta":     meta or {},
            "state":    state,
        },
    )


@app.get("/raw/{paper_id}")
def raw_markdown(paper_id: str):
    md_path = UPLOADS / f"{paper_id}.md"
    if not md_path.exists():
        raise HTTPException(status_code=404, detail="not found")
    return Response(
        md_path.read_text(encoding="utf-8"),
        media_type="text/markdown; charset=utf-8",
    )


@app.get("/healthz")
def healthz():
    return {"ok": True, "uploads": UPLOADS.exists(), "reports": REPORTS.exists()}
