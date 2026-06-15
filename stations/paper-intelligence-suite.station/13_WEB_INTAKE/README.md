# 13_WEB_INTAKE — Theophysics Paper Intake (Package D)

A small FastAPI app that wraps the 12-layer pipeline so anyone can submit a
paper through a browser instead of the CLI.

## Run it

```bash
cd 13_WEB_INTAKE
run.bat                # Windows
# or
python -m uvicorn app:app --host 0.0.0.0 --port 8088
```

Open http://localhost:8088/.

## Routes

| Method | Path                  | Purpose                                   |
| ------ | --------------------- | ----------------------------------------- |
| GET    | `/`                   | Intake form                               |
| POST   | `/submit`             | Accept author/title/domain/content        |
| GET    | `/status/{paper_id}`  | JSON job state (poll target)              |
| GET    | `/report/{paper_id}`  | HTML report when ready, progress page mid |
| GET    | `/raw/{paper_id}`     | The saved markdown source                 |
| GET    | `/healthz`            | Liveness                                  |

## What happens on submit

1. Form values + uploaded text/PDF are normalized into a markdown file at
   `uploads/<paper_id>.md` with a small front-matter block (title, author,
   domain, submitted timestamp).
2. A `paper_id` is minted: `YYYYMMDDTHHMMSS_<author-slug>_<title-slug>`.
3. A daemon thread runs `00_ORCHESTRATOR/run_pipeline.analyze_paper()`
   in-process (faster than re-spawning Python per submission, and lets us
   surface tracebacks). The `--openai` layer is OFF by default — flip the
   `run_openai` flag in `_run_pipeline_job` if you want it.
4. When the row dict comes back, `11_HTML_REPORT/generate_report.generate_paper_html()`
   renders a self-contained HTML scorecard at `reports/<paper_id>.html`.
5. The browser is on a 2.5s polling loop against `/status/<paper_id>` from
   the progress page; the page reloads itself when status flips to
   `complete` (HTML is served inline) or `error` (traceback page).

## Storage layout

```
13_WEB_INTAKE/
├── app.py
├── run.bat
├── README.md
├── templates/
│   ├── intake.html
│   ├── progress.html
│   └── error.html
├── static/                # reserved for future assets
├── uploads/<paper_id>.md  # normalized paper text
├── reports/
│   ├── <paper_id>.html    # rendered scorecard
│   └── <paper_id>_row.json
└── meta/<paper_id>.json   # form metadata + final status
```

## Notes for downstream packages

- **Package A**: once the orchestrator emits a `ProofExplorerSnapshot`, write
  it to `reports/<paper_id>_snapshot.json` alongside the row JSON. The
  intake doesn't care what's inside — it just serves the HTML the report
  generator returns.
- **Package C**: the upgraded `generate_paper_html()` will be called as-is
  from `_run_pipeline_job`. No app.py changes needed.

## Deferred to v2

- Multi-process job runner (current build is single-server, in-memory job
  registry — fine for one user, dies if the process restarts mid-run).
- Cloudflare Tunnel exposure.
- Auth (currently anonymous).
- File-size cap on uploads.
