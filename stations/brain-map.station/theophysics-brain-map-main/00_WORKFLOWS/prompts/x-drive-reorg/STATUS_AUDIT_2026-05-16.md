# X-drive reorg prompt completion audit

Date: 2026-05-16 (UTC)
Scope audited: `00_WORKFLOWS/prompts/x-drive-reorg`

## Summary
This audit checks what has verifiable implementation evidence in this repository for prompts 4a–5.

Status legend:
- DONE: clear implementation evidence exists in-repo.
- PARTIAL: some implementation exists, but acceptance requirements are not all evidenced here.
- NOT VERIFIED: no direct implementation evidence found in this repository snapshot.

## Prompt-by-prompt

### 4a — Folder convention rollout
Status: **PARTIAL**
- Prompt exists and defines acceptance checks.
- In-repo artifact pack exists under `4a-output/`.
- `4a-output/apply_4a.ps1` is now a dry-run-first safe migrator rather than a direct `mklink` script.
- Live X:\ application is still not verified here; do not call 4a complete until the prompt acceptance checks pass on X:\.

### 4b — Root simplification
Status: **NOT VERIFIED**
- Prompt exists and expects filesystem moves + junctions on X:.
- This repository snapshot does not include runtime X: junction validation output.

### 4c — Batch-script path sweep
Status: **NOT VERIFIED**
- Prompt exists and references D:/X: rewrite across BIL paths.
- No local BIL tree or resulting sweep log is present in this repository snapshot.

### 4d — Intake engine program
Status: **NOT VERIFIED**
- Prompt exists.
- No `Backside/intake_engine` package is present in this repository snapshot.

### 4e — Brain Dashboard / Workflow Composer
Status: **PARTIAL**
- A dashboard scaffold was added at `Backside/brain_dashboard` with tabs, readers, and tests.
- The scoped prompt in this folder is now `4e_pyside_workflow_composer.md` (revised and broader than dashboard-only).
- Current implementation is dashboard-MVP, not full workflow composer scope.
- Smoke evidence: `python -m pytest Backside/brain_dashboard/tests` passed 3 tests on 2026-05-16.

### 4f — Conversion layer
Status: **PARTIAL**
- Prompt exists.
- `Backside/conversion_lib` now contains the `theophysics_conversion` package.
- `00_WORKFLOWS/conversion-layer` now contains the standalone workflow wrapper.
- Smoke evidence: `python -m theophysics_conversion.convert --detect README.md` returned `MARKDOWN`.
- Smoke evidence: conversion of `README.md` to canonical Markdown succeeded.
- Test evidence: `python -m pytest Backside/conversion_lib/tests` passed 6 tests on 2026-05-16.
- Remaining gap: full prompt coverage for MarkItDown office/PDF, Whisper audio/video, OCR images, and YouTube transcript fallback is not verified.

### Station lab sidecar
Status: **PARTIAL**
- `Backside/station_lab` exists as a safe tuning bench for individual paper-grader stations.
- Smoke evidence: `paper_grader_station_lab.py --input README.md --station overview` produced an overview export.
- This is useful, but it is sidecar work; do not confuse it with 4d intake engine completion.

### Backside model/workflow registry
Status: **PARTIAL**
- `Backside/_models` now defines typed `.model` folders and model cards.
- New conceptual lanes exist for `timeline.model`, `facts.model`, and `paper-citation.model`.
- `Backside/workflows`, `Backside/stations`, and `Backside/prompts` now document typed folder naming: `.workflow`, `.station`, `.prompt-pack`.
- This is a map/contract only. Live workflow moves still depend on 4b/4c path sweep and junction planning.

### 4g — Root checks master
Status: **NOT VERIFIED**
- Prompt exists and expects `X:/CHECKS/RUN_ALL.bat` plus report output.
- No in-repo evidence of that deliverable found.

### 5 — BIL + FAP migration
Status: **NOT VERIFIED**
- Prompt exists and depends on 4c completion on live D:/X: paths.
- No in-repo migration execution log or post-move verification artifact found.

## Recommended next actions
1. Treat 4e dashboard scaffold as a separate deliverable and align with the revised 4e workflow-composer prompt before calling 4e complete.
2. Treat 4f as a working first pass, not complete. Add the missing adapter tests before asking another AI partner to wire it into 4d.
3. Add/commit per-prompt completion logs (or stubs linking to external logs) so status is traceable from this repository.
4. Run acceptance checks in each prompt on the target Windows host and attach outputs under `_LOGS` with stable filenames.
