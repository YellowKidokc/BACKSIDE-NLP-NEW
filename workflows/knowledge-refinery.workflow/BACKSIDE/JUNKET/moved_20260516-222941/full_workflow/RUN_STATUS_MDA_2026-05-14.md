# MDA full workflow run status

Checked: 2026-05-14 00:47 local
Runner: codex-forge

## Workflow found

- Conductor: `X:\knowledge-refinery\RUN_FULL_WORKFLOW.bat`
- Direct runner: `X:\knowledge-refinery\full_workflow\scripts\batch_orchestrator.py`
- Output root: `X:\knowledge-refinery\full_workflow\output`
- FAP root: `X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP`

## Input staging

- Original Markdown bundle: `X:\knowledge-refinery\full_workflow\staged_intake\mda-complete-series-20260514\mda-complete-series.md`
- Markdown carrier failed because the GTQ public refinery only processes `.html` / `.htm` despite the full-workflow README saying `.md` is accepted.
- First HTML carrier from Markdown succeeded but included markup/class text noise from the old Markdown source.
- Clean carrier used for final run: `X:\knowledge-refinery\full_workflow\staged_intake\mda-complete-series-20260514-clean-html\mda-complete-series-clean.html`

## Final usable run

- Batch: `batch-20260514-002844`
- Job: `20260514-002844_mda-complete-series-clean`
- Batch index: `X:\knowledge-refinery\full_workflow\output\batch-20260514-002844\batch_index.md`
- Scorecard: `X:\knowledge-refinery\full_workflow\output\batch-20260514-002844\20260514-002844_mda-complete-series-clean\scorecard.md`
- Draft HTML: `X:\knowledge-refinery\full_workflow\output\batch-20260514-002844\20260514-002844_mda-complete-series-clean\production-draft.html`
- Station outputs: `X:\knowledge-refinery\full_workflow\output\batch-20260514-002844\20260514-002844_mda-complete-series-clean\stations`

## Results

- Combined score: `19.25`
- Grader normalized: `0.925`
- Stations: `PASS=10`, `REVIEW=2`, `FAIL=1`
- REVIEW stations: `axiom_rigor_gate`, `seven_e_evidence`
- FAIL station: `contradiction_check`

## Main flagged issue

`contradiction_check` failed because the station judged the sudden-collapse / phase-transition claim as under-supported by the provided evidence. It specifically asked for clearer mathematical or empirical basis and tighter internal consistency across the data points.

## Runtime note

The console emitted Unicode logging errors for an arrow character in `station_runner.py`, but the workflow returned exit code `0` and wrote the batch outputs.
