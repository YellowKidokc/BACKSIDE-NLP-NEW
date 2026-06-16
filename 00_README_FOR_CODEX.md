# Theophysics Brain — Codex Export
**Generated: 2026-06-14 21:23**
**POF 2828**

## What This Is
Clean export of the Theophysics Brain processing system for Codex.
Contains station code, workflow definitions, model/engine shells, and orchestrator scripts.

## What's Included
- **stations/** — 74 processing stations (Python, configs, batch files, prompts)
- **workflows/** — Multi-station workflow definitions
- **models/** — NLP model folder shells (README/config only, NO weights)
- **engines/** — Preference engine shells (README/config only, NO trained state)
- **orchestrator/** — Top-level orchestration scripts

## What's Excluded
Model weights, vector indexes, runtime state, logs, exports, private data, databases.

## Station Script Standard (SSS_v1)
Every station should follow this flow:
`ingest -> validate -> route/call NLP -> process -> write artifact -> update job card -> export/handoff -> archive/log`

Standard sections in every pipeline.py:
00_IMPORTS, 01_CONSTANTS_AND_PATHS, 02_CONFIG_LOADING, 03_LOGGING, 04_INGEST,
05_VALIDATE, 06_ROUTE_OR_CALL_WORKER, 07_PROCESS, 08_WRITE_ARTIFACTS,
09_UPDATE_JOB_CARD, 10_EXPORT_OR_HANDOFF, 11_ARCHIVE_INPUTS, 12_MAIN

## Architecture Layers
- Layer 0: Intake (drop folder, auto-route)
- Layer 1: Conversion (format normalization)
- Layer 2: NLPs/Models (processing horsepower)
- Layer 3: Stations (atomic 1:1 operations, 30-50 of them)
- Layer 4: Workflows (stations chained in sequence)
- Layer 5: Apps (self-contained independent systems)

## Key Rule
Station = one action. Workflow = many stations in order. App = whole independent system.
If a station does five things, split it.
