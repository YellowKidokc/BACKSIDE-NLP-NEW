# Prompt: Execute X Drive Root Reorg Contract

**Date:** 2026-05-20
**Repo:** `D:\GitHub\theophysics-brain-map`
**Live root:** `X:\` = `\\dlowenas\brain`
**Contract docs:** `ROOT_REORG_TARGET_2026-05-20.md`, `Backside/ROOT_REORG_MOVE_MAP_2026-05-20.csv`

## Assignment

Clean the live `X:\` root so the visible outside folders are:

```text
X:\David
X:\GUI
X:\Conversions
X:\EXPORTS
X:\Backside
```

Keep root docs and click-buttons if needed:

```text
README.md
ARCHITECTURE.md
THEOPHYSICS_PRIMER.md
RUN_*.bat
```

Everything else should either move behind `Backside`, move into `EXPORTS`, or become a temporary compatibility pointer.

## Non-negotiables

1. Do not delete. Archive or move.
2. Do not silently break old paths. If a known script still references an old root path, patch it or leave a temporary compatibility pointer and log it.
3. `EXPORTS` is the final reproducible output shelf: HTML, Excel, metadata, manifests, and anything needed to rebuild or verify the artifact.
4. `Conversions` is a front door, not hidden machinery. It should expose the conversion layer that currently lives at `Backside\conversion_lib`.
5. `GUI` is a front door. Promote the Brain Dashboard surface that currently lives at `Backside\brain_dashboard`.
6. `Backside` owns runtimes: workflows, models, stations, services, control-plane repos, state, logs, archive, and corpus/data lanes.

## First pass

Run a dry-run inventory and report before moving live workflow folders:

```powershell
Get-ChildItem X:\ -Force | Select Mode,Length,LastWriteTime,Name,FullName
```

Then compare against:

```text
Backside\ROOT_REORG_MOVE_MAP_2026-05-20.csv
```

## Low-risk moves first

These can move before workflow path patching:

```text
X:\_brain_DEPRECATED_20260516 -> X:\Backside\_archive\root\_brain_DEPRECATED_20260516
X:\00_CONVERSION -> X:\Backside\_archive\root\00_CONVERSION
X:\_LOGS -> X:\Backside\_logs
X:\models -> X:\Backside\_models\downloaded
X:\Backside\models -> X:\Backside\_models\legacy-model-layer
X:\Backside\brain_dashboard -> X:\GUI\brain-dashboard
X:\Backside\conversion_lib -> X:\Conversions\conversion-layer
X:\proof-architecture -> X:\EXPORTS\proof-architecture
X:\proof-explorer -> X:\EXPORTS\proof-explorer
```

## Path-sensitive moves

Move these only after patching launchers/configs or creating temporary compatibility pointers:

```text
X:\knowledge-refinery -> X:\Backside\workflows\knowledge-refinery.workflow
X:\paper-proof-grader -> X:\Backside\workflows\paper-proof-grader.workflow
X:\session-handoff-drop -> X:\Backside\workflows\session-handoff.workflow
X:\link-pull-drop -> X:\Backside\workflows\link-pull.workflow
X:\ai-portal-generator -> X:\Backside\workflows\ai-portal-generator.workflow
X:\axioms -> X:\Backside\workflows\axioms.workflow
X:\Preference Engine Build -> X:\Backside\control-plane\Preference Engine Build
X:\github -> X:\Backside\control-plane\github
X:\ollama -> X:\Backside\services\ollama
```

## Required output

Write a migration log at:

```text
X:\Backside\_archive\root\ROOT_REORG_LOG_2026-05-20.md
```

The log must include:

- what moved,
- what stayed,
- what compatibility pointers remain,
- which commands were run,
- which health checks passed,
- which paths still need patching.

## Acceptance condition

Opening `X:\` should show the root as a front door:

```text
David
GUI
Conversions
EXPORTS
Backside
README / ARCHITECTURE / PRIMER / RUN buttons
```

No loose model folders, no loose workflow runtimes, no deprecated Brain root folder, no scattered repo/control-plane folders.
