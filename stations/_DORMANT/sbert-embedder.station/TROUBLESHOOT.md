# 02_SBERT — Troubleshooting

## `ModuleNotFoundError: sentence_transformers`

Run `INSTALL.bat`. If it fails, run manually:

```
C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe -m pip install sentence-transformers numpy
```

## First run is slow

It downloads `all-MiniLM-L6-v2` (~90 MB) into `_MODELS\hub\`. Subsequent runs are instant.

## `OSError: [WinError 1314] A required privilege is not held by the client`

HuggingFace caches use symlinks by default on Windows. Either:

- Run the terminal as Administrator once to populate the cache, OR
- Set `HF_HUB_DISABLE_SYMLINKS_WARNING=1` (warning is cosmetic; it falls back to copies).

## CUDA out of memory

Reduce `model_settings.batch_size` in `config.json`. 32 is fine for most GPUs; drop to 8 or 4 for older cards. Or set `device` = `"cpu"`.

## Embeddings look wrong / zero

Check input files aren't empty. The runner reads UTF-8 then falls back to latin-1; if your files are something else (UTF-16 with BOM), convert first.

## Choosing a different model

Common picks (edit `config.json` → `model_settings.model_name`):

| Model | Dim | Speed | Use case |
|---|---|---|---|
| `all-MiniLM-L6-v2` | 384 | very fast | default, semantic search |
| `all-mpnet-base-v2` | 768 | fast | higher quality, ~3× slower |
| `BAAI/bge-large-en-v1.5` | 1024 | medium | best general English |
| `intfloat/multilingual-e5-large` | 1024 | medium | multilingual |

## Postgres mode hangs after "rows pending: 0"

There aren't any rows where the embedding column is NULL. Either the work is already done, or your `source.where` filter excluded everything. Check from `07_POSTGRES\CONNECT.bat`:

```python
db.query("SELECT COUNT(*) FROM youtube_apologetics WHERE sbert_embedding IS NULL")
```

## A specific row crashes the embedder

The runner falls back to per-row mode after a batch failure and skips just the bad row(s). Look in `_LOGS\sbert_*.log` for `row embed failed:`. Common cause: a `description` field with embedded null bytes — clean upstream or set the value to NULL before re-running.

## How to re-embed everything

`UPDATE youtube_apologetics SET sbert_embedding = NULL` from `psql`, then re-run.
