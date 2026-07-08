# FIS — File Intelligence System

Station: `ST-FIS-001` | Extension: `.fcard` | POF 2828

## What It Does

Scans a folder, classifies every file, and drops a `_manifest.fcard` into that folder.
Each file gets a **classification card** with 8 fields:

1. **domain** — big bucket (theophysics, development, trading, etc.)
2. **file_type_meaning** — semantic type (research_paper, code_file, notes, etc.)
3. **summary** — one sentence
4. **tags** — max 5 category tags
5. **keywords** — words pulled from the file
6. **rename_preview** — baseline + slug + 3 naming presets
7. **suggested_action** — what to do next (review, rename, move, etc.)
8. **confidence** — per-field confidence scores

## Rule

NLP **suggests**. David **approves** domain, rename, move, delete.

## Baseline Before NLP

Mechanical rename always runs first (no model):

```
Clipboard Text (2).txt  →  clipboard-text-2.txt
My Report_FINAL v3.docx →  my-report-final-v3.docx
```

Then NLP adds the richer layer on top.

## Model Stack

| Engine | Model | Size | Required |
|--------|-------|------|----------|
| YAKE | none (statistical) | 0 | yes |
| spaCy | en_core_web_sm | 12MB | yes |
| DeBERTa NLI | `X:\05_MODELS\deberta_nli` | 900MB | no (rule-based fallback) |
| BART | `X:\05_MODELS\M13_bart_summarizer` | 1.6GB | no (extractive fallback) |

**Minimum download for someone else: ~12MB** (spaCy only, rule-based + extractive).
**Full quality: ~2.5GB** (add DeBERTa + BART).

## Usage

```bash
# Classify a folder
python -m fis "X:\01_FRONT_DOOR\_inbox"

# Single file
python -m fis --file "X:\some\file.txt"

# Without heavy models
python -m fis --no-bart --no-deberta "X:\01_FRONT_DOOR\_inbox"

# Initialize SQLite
python -m fis --init-db
```

## Output

`_manifest.fcard` — YAML file dropped into the scanned folder.
Opens in any text editor. Extension `.fcard` prevents accidental deletion.

## SQLite

`fis.db` stores all cards for search, dashboard, and audit.
The `.fcard` file is portable; SQLite is the queryable index.
