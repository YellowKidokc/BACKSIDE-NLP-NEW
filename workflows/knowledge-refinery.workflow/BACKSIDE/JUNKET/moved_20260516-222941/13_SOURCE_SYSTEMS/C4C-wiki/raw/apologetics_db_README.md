# Apologetics Recon Database
**David Lowe / POF 2828**

## Target DB
- Host: 192.168.1.177:2665
- DB: theophysics (or create: `CREATE DATABASE apologetics;`)
- Schema: apologetics

## Setup (run once)
```sql
psql -h 192.168.1.177 -p 2665 -U postgres theophysics -f schema.sql
psql -h 192.168.1.177 -p 2665 -U postgres theophysics -f hud_data.sql
```

## Load Transcripts
```bash
# First edit load_transcripts.py line 17: add your postgres password
# Dry run first to see what it finds:
python load_transcripts.py --dry-run

# Then for real:
python load_transcripts.py
```

## What gets loaded
- **hud_data.sql**: 642 catalogued contradictions, all refuted, 10 categories
- **load_transcripts.py**: Reads all 177 transcripts, extracts:
  - Arguments by category (7 categories, 21 move types)
  - Scripture references (book/chapter/verse + context)
  - Channel breakdown

## Key Queries (see queries.sql)
1. Top 20 argument moves by frequency
2. Top 20 scriptures attacked
3. OT attacks specifically
4. Per-channel focus areas
5. Exact quotes on any topic
6. Category distribution

## Argument Categories
| Code | What It Covers |
|------|----------------|
| EPISTEMOLOGICAL | Evidence, falsifiability, God of gaps |
| TEXTUAL | Bible reliability, contradictions, cherry-picking |
| LOGICAL | Which god, problem of evil, hiddenness |
| MORAL | Morality without God, religion causes harm, OT violence |
| SCIENTIFIC | Evolution, science vs religion |
| PSYCHOLOGICAL | Upbringing, cope/wish fulfillment |
| EVIDENTIAL | Resurrection, prayer, historical Jesus |

## HUD Codes (642 contradictions)
| Code | What It Means |
|------|---------------|
| META | Logical fallacy (36.6%) — not a real contradiction |
| SCRIBE | Copyist variant (17.9%) |
| STRIPPING | Context stripped (16%) |
| VANTAGE | Different witnesses, same event (8.3%) |
| COVENANT | OT law vs NT fulfillment (6.9%) |
| SEMANTIC | Translation issue (5.5%) |
| DISTINCT | Two different events confused (3.4%) |
| ROUNDING | Ancient approximation (2%) |
| AUDIENCE | Different audience, different emphasis (1.9%) |
| PHENOM | Observational/poetic language (1.6%) |
