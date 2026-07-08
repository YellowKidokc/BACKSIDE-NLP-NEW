# MDA Pipeline Outputs — Permanent Home

This is the canonical landing zone for all MDA (Moral Decline of America) series
pipeline outputs. Parallel structure to `X:\Backside\axioms\`.

## Folder Map

| Folder | Contents | Source |
|---|---|---|
| `01_OUTBOX_REPORTS` | Claim audits + paper grades (csv/html/json/md/xlsx) | Math Translation Layer |
| `02_HTML_OUTPUTS` | Paper grade HTML dashboards | Math Translation Layer |
| `03_FINAL_READY` | Combined final bundles (all formats per article) | Math Translation Layer |
| `04_ARCHIVE_ORIGINALS` | Source markdown articles (61 MDA docs) | Math Translation Layer |
| `05_MANIFESTS` | Run manifests (csv/json) | Math Translation Layer |
| `06_RIGOR_GATES` | Rigor gate outputs + axiom manifest | Math Translation Layer |
| `07_NLP_SCORECARDS` | NLP HTML scorecards (PI_MDA-xxx.html) | Local NLP Layer |
| `08_NLP_WORKBOOKS` | Master workbook (xlsx) + summary JSONs | Local NLP Layer |
| `09_NLP_SNAPSHOTS` | Per-article NLP snapshots | Local NLP Layer |
| `_RUNS` | Route receipts (one per dispatch) | This script |
| `_LOGS` | Route logs | This script |

## Canon Vault Mirror

Publication-grade subset also routed to:
`Z:\_ __THEOPHYSICS_CANON\03_SERIES\MDA\`
- `articles/` — 61 source MDs
- `grades/` — 61 paper grade MDs
- `nlp/` — 61 NLP scorecards
- `claim-audits/` — 61 claim audit CSVs

## How To Re-Run After a New Pipeline Pass

1. Edit `ROUTE_MDA_OUTPUTS.ps1` — change `$SourceMathGrader` and `$SourceNLP`
2. `.\ROUTE_MDA_OUTPUTS.ps1 -WhatIf` to verify
3. `.\ROUTE_MDA_OUTPUTS.ps1` to execute
