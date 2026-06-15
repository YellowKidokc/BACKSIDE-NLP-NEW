# D:\brain — NLP Workstation

A folder-per-tool architecture for chaining ML models into reliable pipelines.

> **North star:** see `ARCHITECTURE_V2.md` for the locked target architecture
> (document-centric, run-centric, artifact-centric). V1 is a working tool rack;
> V2 is the factory model around it. Phase plan there too — do not cross
> phases in a single session.

## Layout

| Folder | Purpose |
|---|---|
| `00_WORKFLOWS\` | Multi-model pipelines (harvest-links, classify-documents, transcribe-and-classify, youtube-scrape) |
| `01_WHISPER\` | Speech-to-text via faster-whisper |
| `02_SBERT\` | Sentence embeddings via sentence-transformers |
| `03_DEBERTA\` | Zero-shot classification via DeBERTa-v3 NLI |
| `04_HDBSCAN\` | Density-based clustering |
| `05_YOUTUBE\` | YouTube Data API v3 scraper |
| `06_IMAGES\` | OCR (EasyOCR) + zero-shot image tagging (CLIP) |
| `07_POSTGRES\` | Database connect / export / import utilities |
| `_MODELS\` | Downloaded model weights (shared across tools, populated on first run) |
| `_LOGS\` | All runtime logs (`<tool>_YYYYMMDD.log`) |

## Per-tool contract

Every numbered folder has the same files:

- `INSTALL.bat` — installs Python deps for that tool (idempotent)
- `RUN.bat` — runs the tool against paths in its `config.json`
- `TEST.bat` — quick smoke test with synthetic data
- `TROUBLESHOOT.md` — common errors and fixes
- `config.json` — all settings (edit here, not in code)
- `<tool>_runner.py` — actual Python; importable as a module by workflows

`07_POSTGRES\` swaps `RUN/TEST` for `CONNECT/EXPORT/IMPORT`, but follows the same rules.

## First-time setup

1. Run `INSTALL_ALL.bat` (calls every tool's `INSTALL.bat`). Or install one at a time.
2. For tools that need API keys (`05_YOUTUBE`), edit that folder's `config.json` or set the env var.
3. Run each folder's `TEST.bat` to verify install.
4. Pick a workflow in `00_WORKFLOWS\`, edit its `config.json`, double-click `RUN.bat`.

## Workflow contract

Pipelines in `00_WORKFLOWS\<name>\`:

- `pipeline.py` adds the relevant model folders to `sys.path` and imports their runners as modules.
- Steps are logged step-by-step to `_LOGS\workflow_<name>_YYYYMMDD.log`.
- Output goes to Postgres AND a local output dir (per the workflow's `config.json`).

## Python

All scripts use:

```
C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
```

If you move Python, edit each `*.bat` and `config.json` `python_path` field. (Or set `PYTHON_EXE` env var — RUN.bat respects it if set.)

## Stack endpoints (NAS Brain — 192.168.1.177)

The NAS hosts the canonical embedding service and vector store. Vectors live
in Qdrant (artifact layer); Postgres holds source rows and scalar metadata.

| Service   | URL                              | Role                                              |
|-----------|----------------------------------|---------------------------------------------------|
| Infinity  | `http://192.168.1.177:7997`      | Embedding-as-a-service, `all-MiniLM-L6-v2` (dim=384) |
| Qdrant    | `http://192.168.1.177:6333`      | Vector DB; one collection per source corpus       |
| PIL API   | `http://192.168.1.177:8420`      | FastAPI for capture/rate/describe events          |
| Ollama    | `http://192.168.1.177:11434`     | Vision (`moondream`) + general (`mistral`, `llama3.2`) |
| Postgres  | `192.168.1.177:2665/crawlab_data` | Crawl/Brain/YouTube corpora (user `root`)         |

Quick health checks:
```
curl http://192.168.1.177:7997/health
curl http://192.168.1.177:6333/collections
curl http://192.168.1.177:8420/status
```

NAS service deployment script: `\\192.168.1.177\brain\deploy\deploy.sh`
(run as root on the Synology). NAS Brain layout and deploy gotchas live in
the cross-session memory under `reference_nas_brain_architecture`.

### Other Postgres instance

TikTok work uses a **separate** Postgres at `192.168.1.97:5432/theophysics`
(schema `tiktok`). Not yet unified with `crawlab_data`. Eventual unification
happens in `\\YellowkidNas\github\TRUTH_ENGINE_UNIFIED\05_tie_graph` —
both corpora must share the same embedding space (Infinity all-MiniLM-L6-v2)
to be comparable in that stage.

## Postgres

Default connection (set in `07_POSTGRES\config.json`):

- host: `192.168.1.177`
- port: `2665`
- user: `root`
- database: `crawlab_data`
- password: resolved from `BRAIN_PG_PASSWORD` env var (in `.env`), never literal

Override per-tool via that tool's `config.json`.

## Secrets

Live secrets are no longer meant to live in shared JSON.

- Put machine-local secrets in `D:\brain\.env`
- Use `D:\brain\.env.example` as the template
- Current env vars:
  - `BRAIN_PG_PASSWORD`
  - `BRAIN_YOUTUBE_API_KEY`

Non-secret defaults can stay in `config.json`, but secret values should resolve
from environment first.

## Adding a new tool

Copy any existing numbered folder, rename, and edit:

1. `INSTALL.bat` — change pip packages
2. `<tool>_runner.py` — implement `run(config)` and a `__main__` block
3. `config.json` — add tool-specific settings under `model_settings`
4. `TEST.bat` — synthetic fixture exercising the runner
5. `TROUBLESHOOT.md` — write known failures as you hit them

## Logs

`_LOGS\` is gitignored by convention. Logs rotate by day (`<tool>_YYYYMMDD.log`); old logs are retained — clear manually when convenient.
