# OPUS SESSION HANDOFF — FIS Build
## 2026-06-14 | POF 2828 | For Codex Cross-Review

---

## What Was Built This Session

**FIS (File Intelligence System) v2** — a complete NLP classification + GUI action system for file organization.

### Location: `X:\04_STATIONS\_front_door\fis.station\`

```
fis.station/
├── station.json          # Station metadata, model paths, card extension
├── config.json           # Domains, file_type_meanings, thresholds, model toggles
├── requirements.txt      # PySide6, yake, spacy, transformers, pdfplumber, etc.
├── RUN.bat               # Launch: --gui | folder_path | --file | --init-db
├── README.md             # Full docs
├── fis/
│   ├── __init__.py
│   ├── __main__.py       # CLI entry: python -m fis "X:\path"
│   ├── pipeline.py       # 10-step NLP classification pipeline (178 lines)
│   ├── engines.py        # YAKE + spaCy + DeBERTa + BART + rule-based fallbacks (207 lines)
│   ├── extractor.py      # Text extraction: txt, pdf, docx, code (86 lines)
│   ├── baseline.py       # Mechanical rename + slug + rename presets (59 lines)
│   ├── card.py           # Classification card schema + .fcard YAML writer (91 lines)
│   ├── actions.py        # 8 filesystem actions with preview/approve (503 lines)
│   ├── gui.py            # PySide6 desktop app, data-driven panels (302 lines)
│   └── db.py             # SQLite schema + insert (100 lines)
├── INPUT/
├── OUTPUT/
└── _LOGS/
```

### Job Card: `X:\03_JOB_CARDS\_front_door\fis-classify.job\job.json`

10-step workflow definition with approval rules.

### Contract: `X:\08_DASHBOARDS\FILE SORTER\NLP_OUTPUT_CONTRACT.md`

David's spec for what NLP should output (written before this session, I built to match it).

### Station Registry Updated: `X:\04_STATIONS\_front_door\STATION_REGISTRY.json`

Added `fis` entry alongside legacy `file-intelligence`.

---

## Architecture

### Classification Card (8 fields)

NLP processes each file and produces a classification card:

1. `domain` — big bucket (theophysics, development, trading, etc.) + confidence
2. `file_type_meaning` — semantic type (research_paper, code_file, notes) + confidence
3. `summary` — one sentence
4. `tags` — max 5 category tags
5. `keywords` — words pulled from the file
6. `rename_preview` — baseline + slug + 3 naming presets (short/descriptive/archive)
7. `suggested_action` — what to do next
8. `confidence` — per-field scores

### Processing Flow

```
file arrives
    → baseline rename (mechanical: lowercase + hyphens, NO model)
    → extract text (txt/pdf/docx/code)
    → YAKE keywords (statistical, no model)
    → spaCy entities (12MB model)
    → DeBERTa zero-shot domain + file_type (900MB, optional)
    → BART 1-sentence summary (1.6GB, optional)
    → build classification card
    → write _manifest.fcard to folder (YAML)
    → store in SQLite (optional)
```

### Model Stack

| Engine | Model | Path | Size | Required |
|--------|-------|------|------|----------|
| YAKE | none (statistical) | pip | 0 | yes |
| spaCy | en_core_web_sm | pip download | 12MB | yes |
| DeBERTa NLI | zero-shot classifier | `X:\05_MODELS\deberta_nli` | 900MB | no |
| BART | abstractive summarizer | `X:\05_MODELS\M13_bart_summarizer` | 1.6GB | no |

Fallbacks when heavy models disabled: rule-based domain classification + extractive summary.
M01_summarizer is a duplicate of M13 — safe to delete M01.

### GUI (PySide6)

8 actions, one dynamic panel:
1. Combine — bring related files/folders together
2. Separate — split messy folder into groups
3. Rename — clean identity
4. Move — relocate
5. Copy — duplicate without changing original
6. Archive — remove from active, preserve
7. Delete Later — quarantine with retention
8. Link / Hub — connect without merging

Universal flow: Pick items → Pick action → Pick target/name → Preview → Approve → Record

Each action defined as data in `ACTION_DEFS` dict. GUI renders options dynamically.
All actions log to `_LOGS/actions_YYYYMMDD.jsonl`.

### Extension: `.fcard`

One `_manifest.fcard` per scanned folder. YAML inside. Opens as text.
Watcher/pipeline skips `.fcard` files to avoid self-classification.

---

## What Is NOT Done Yet

1. **SQLite persistence call** — `db.insert_card()` exists but pipeline.py doesn't call it yet (one line)
2. **File watcher** — watchdog service to auto-trigger pipeline on new files (phase 2)
3. **Separate by domain** — needs to read .fcard manifest first (currently falls back to "unknown")
4. **GUI reading .fcard** — GUI can execute actions but doesn't pre-populate from classification cards yet
5. **Windows shortcuts** in Link/Hub — needs `win32com` or `pylnk3` for .lnk creation
6. **Testing** — needs a test run on a real folder

---

## Potential Overlap With Codex

### KNOWN OVERLAP AREAS:
- `file-intelligence.station` (legacy FIS) — Codex may have touched this
- Station registry — both of us edit `STATION_REGISTRY.json`
- `X:\05_MODELS` — model paths referenced by both systems
- Pipeline workflows — if Codex built any file processing workflows

### CODEX SHOULD CHECK:
- Does anything in Codex's work depend on the OLD `file-intelligence.station`?
- Are there any station.json or job.json schemas that conflict?
- Is Codex using `_manifest.fcard` or any similar sidecar file pattern?
- Any SQLite schemas that should share tables with FIS?

---

## Files To Give Codex (read these in order)

1. `X:\04_STATIONS\_front_door\fis.station\station.json`
2. `X:\04_STATIONS\_front_door\fis.station\config.json`
3. `X:\04_STATIONS\_front_door\fis.station\fis\pipeline.py`
4. `X:\04_STATIONS\_front_door\fis.station\fis\actions.py`
5. `X:\04_STATIONS\_front_door\fis.station\fis\gui.py`
6. `X:\04_STATIONS\_front_door\fis.station\fis\db.py`
7. `X:\03_JOB_CARDS\_front_door\fis-classify.job\job.json`
8. `X:\08_DASHBOARDS\FILE SORTER\NLP_OUTPUT_CONTRACT.md`
