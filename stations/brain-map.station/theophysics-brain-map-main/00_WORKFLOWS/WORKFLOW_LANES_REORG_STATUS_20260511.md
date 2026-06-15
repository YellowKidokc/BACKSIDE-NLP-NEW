# Workflow Lanes Reorg Status

Generated: 2026-05-11

## What Changed

The active workflow folders were promoted to the Brain root so the working folders are visible immediately when opening:

`\\dlowenas\brain`

Shared healthcheck scripts remain in:

`\\dlowenas\brain\00_WORKFLOWS\01_SHARED_SCRIPTS`

## Active Root Workflows

- `\\dlowenas\brain\ai-portal-generator`
- `\\dlowenas\brain\link-pull-drop`
- `\\dlowenas\brain\paper-proof-grader`
- `\\dlowenas\brain\session-handoff-drop`
- `\\dlowenas\brain\theophysics-comms-hub`

## Verification

`RUN_WORKFLOWS_HEALTHCHECK.bat` was updated to check the root-level workflow folders.

Latest healthcheck after the move:

- Failures: 0
- Warnings: 0

## Entry Point

Keep `\\dlowenas\brain\00_WORKFLOWS` as the map and healthcheck hub.

The working workflow folders are now at the Brain root.
