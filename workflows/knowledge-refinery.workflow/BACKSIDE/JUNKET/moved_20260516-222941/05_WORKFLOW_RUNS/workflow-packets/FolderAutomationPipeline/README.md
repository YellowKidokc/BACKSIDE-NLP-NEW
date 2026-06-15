# FolderAutomationPipeline

FAP is the folder nervous system for Brain / BIL / Theophysics production.

This packet turns the existing FAP lane structure into a reusable, promptable workflow:

```text
folder event -> station -> verdict -> route -> manifest -> signal -> next station
```

## Runtime Home

```text
X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP
```

## Core Lanes

```text
intake
classified
media-routed
lossless
vectorized
graded
axiom-mapped
output
_review
_rejected
_queue
logs
wiki
```

## First Manufacturing Line

```text
INTAKE
-> CLASSIFY
-> MEDIA ROUTE
-> LOSSLESS
-> VECTORIZE
-> PAPER GRADE
-> AXIOM RIGOR / AXIOM MAP
-> AI PORTAL / FINAL PACKAGE
```

## Rules

1. File movement must be tracked by manifest.
2. Every station has pass/review/fail routes.
3. Lossless output is required for AI website / portal use.
4. Postgres is the durable ledger.
5. Local JSONL can record immediate actions before Postgres sync.
6. No station should silently overwrite or silently move files.

## What This Packet Provides

- visible workflow contract
- prompt bank for worker AIs
- path registry for X runtime lanes
- future home for transport/manifest/Postgres scripts

This does not replace the FAP runtime folder. It is the control-plane wrapper around it.
