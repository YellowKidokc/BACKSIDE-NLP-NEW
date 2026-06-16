# 04_MODEL_STATIONS (Front Door)

This folder is intended to be the "front door" for the model/NLP stations.

## Current reality (before this scaffold)
- This folder previously held mostly *run output JSON files* like `*_grade.json`, `*_math_verify.json`, `*_contradiction.json`.
- The actual model assets are not centralized here; they are currently scattered (examples):
  - `X:\knowledge-refinery\13_SOURCE_SYSTEMS\D_brain\_MODELS`
  - In older local station workspaces: `...\NLP_ACTIONS\00_SHARED\models`

## New station packet scaffold (added)
- `STATIONS/<station_id>/{INPUT,OUTPUT,REVIEW,ARCHIVE,ERROR,CONFIG,PREFS,PROMPTS,SCRIPTS,LOGS}`

Stations scaffolded now:
- `paper_grader`
- `math_verify`
- `contradiction_detector`
- `lossless_summary`
- `claim_registry`
- `axiom_7qs`

## What to do next
1) Move/route future runs so they write into `STATIONS/<station_id>/OUTPUT/` (not the root).
2) Put model weights/caches under a single canonical lane (recommend): `X:\knowledge-refinery\13_SOURCE_SYSTEMS\D_brain\_MODELS` or create `X:\knowledge-refinery\_MODELS` and point all stations to it.
3) Add a validator that checks each station emits canonical filenames (scores.json, summary.lossless.md, claims.json, etc.) so downstream wiring becomes declarative.
