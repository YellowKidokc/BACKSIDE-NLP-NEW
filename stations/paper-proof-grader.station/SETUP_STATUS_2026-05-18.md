# Paper Proof Grader Setup Status - 2026-05-18

Status: working canary passed.

## Fixed

`config.json` had stale share paths:

- `\\dlowenas\paper-proof-grader\...`
- `\\dlowenas\_LOGS`

Those shares were not reachable. The live root-visible Brain path is:

- `\\dlowenas\brain\paper-proof-grader\...`
- `\\dlowenas\brain\_LOGS`

## Verified

Empty-drop smoke test:

```powershell
python X:\paper-proof-grader\pipeline.py
```

Result:

```text
found 0 candidate paper files
nothing to do
```

Canary run:

```text
DROP_PAPERS_HERE\codex-canary-paper.md
```

Generated:

- `OUTPUT\codex-canary-paper.paper-grade.json`
- `OUTPUT\codex-canary-paper.paper-grade.md`
- `OUTPUT\codex-canary-paper.paper-grade.html`
- `OUTPUT\codex-canary-paper.claim-audit.csv`
- `OUTPUT\codex-canary-paper.paper-grade.xlsx`
- `OUTPUT\paper-proof-grader-run-20260518_024204.json`

Archived source:

- `ARCHIVE\codex-canary-paper.md`

Log:

- `\\dlowenas\brain\_LOGS\workflow_paper-proof-grader_20260518.log`

7Q/axiom station rerun over existing graded hypothesis outputs:

```powershell
python X:\paper-proof-grader\run_axiom_7q_stations.py
```

Generated:

- `OUTPUT\station-runs\axiom-7q-20260518_024401\batch-index.md`
- `OUTPUT\station-runs\axiom-7q-20260518_024401\batch-index.json`
- per-paper `axiom-7q-stations.md/.json` folders for the four existing
  hypothesis runs.

Later station update:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260518_024929\axiom-7q-review.xlsx
```

The Axiom + 7Q runner now produces an Excel review workbook in addition to
JSON and Markdown. See `AXIOM_7Q_STATION_STATUS_20260518.md`.

## How To Use

Drop `.txt`, `.md`, `.html`, or `.htm` files into:

```text
X:\paper-proof-grader\DROP_PAPERS_HERE
```

Run:

```powershell
X:\paper-proof-grader\RUN_NOW_NO_PAUSE.bat
```

Outputs appear in:

```text
X:\paper-proof-grader\OUTPUT
```

Originals are moved to:

```text
X:\paper-proof-grader\ARCHIVE
```

## Boundary

This verifies the deterministic paper-grader export lane. It does not prove
that the separate `X:\knowledge-refinery\RUN_FULL_WORKFLOW.bat` conductor is
active.

Read-only inspection found the full conductor currently points at:

```text
X:\knowledge-refinery\full_workflow\scripts\batch_orchestrator.py
```

That script path is missing after a prior move. A likely moved copy exists
under:

```text
X:\knowledge-refinery\BACKSIDE\JUNKET\moved_20260516-222941\full_workflow\scripts\batch_orchestrator.py
```

So the direct paper grader is working tonight; the larger knowledge-refinery
full workflow needs a separate path restoration/repointing pass.
