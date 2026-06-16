# 00_WORKFLOWS — Multi-tool pipelines

Each subfolder is a chain of model calls. Workflows import the runner modules from the numbered tool folders directly — they don't shell out, so failure messages and config edits propagate cleanly.

## Workflows

| Folder | Inputs | Steps | Outputs |
|---|---|---|---|
| `youtube-scrape\` | `05_YOUTUBE\config.json` queries | 05_YOUTUBE → 02_SBERT → 03_DEBERTA → 04_HDBSCAN | rows in `youtube_apologetics`, cluster summary CSV |
| `harvest-links\` | Excel/CSV/Postgres URL list | requests → BS4 → 02_SBERT → 03_DEBERTA → Postgres → 04_HDBSCAN | rows in `harvest_results`, summary CSV |
| `classify-documents\` | dir of `.txt`/`.md` | 02_SBERT (file) → 03_DEBERTA (file) | per-file JSON sidecars + embeddings.npz + summary CSV |
| `transcribe-and-classify\` | dir of audio/video | 01_WHISPER → 02_SBERT → 03_DEBERTA | per-file `.txt` + JSON sidecar + summary CSV |

## How to run

```
cd 00_WORKFLOWS\<workflow>\
notepad config.json     # set input_dir / paths / queries
RUN.bat
```

Each workflow's logs go to `D:\brain\_LOGS\workflow_<name>_YYYYMMDD.log`.

## Resumability

The Postgres-touching workflows (`youtube-scrape`, `harvest-links`) are resumable: kill the process, re-run, and the next `IS NULL` query picks up where it left off.

The file-mode workflows (`classify-documents`, `transcribe-and-classify`) overwrite their output files. To resume cleanly, move already-processed inputs out of the input dir, or extend the pipeline to skip when an output JSON already exists.

## Adding a new workflow

1. Copy any subfolder, rename to your workflow name.
2. Edit `pipeline.py` to import the runners you need (`sys.path` is already wired for any tool folder).
3. Edit `config.json` for input/output paths.
4. RUN.bat needs no changes — it just calls `pipeline.py`.
