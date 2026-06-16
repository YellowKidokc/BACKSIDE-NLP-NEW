# Backside structure probe and consolidation recommendation

Date: 2026-05-16
Context: Follow-up response to reviewer concern that sibling-pair layouts create top-level sprawl and reduce 10-second openability.

## Probe: failure mode in sibling-pair pattern

A sibling-pair design (`thing/` + `thing-intro/`) doubles visible entries for every model and workflow. At projected scale (~10–15 models, ~20 workflows), this yields 60–70 top-level folders in `Backside/`, which undermines the "open folder, understand quickly" contract.

## Consolidated topology (recommended)

Use three concept layers inside `Backside/`:

- `_models/` — model artifacts only (weights, tokenizer/config, model card metadata)
- `stations/` — reusable services/skills called by workflows
- `workflows/` — human-invoked or orchestration pipelines
- `_archive/` — existing Backside historical material moved out of top-level eyeline

This keeps one folder per thing while preserving contract-at-root readability.

## Why this topology fits the folder-convention contract

- L1 clarity: each folder has a single unambiguous purpose.
- L2 workflow consistency: each workflow keeps `README.md`, `_AGENT_BRIEF.md`, `RUN*.bat`, `health_check.bat`, prompt(s), and `00_DROP/OUTPUT/ARCHIVE`.
- Reuse boundary: stations are explicitly reusable units, rather than hidden logic inside each workflow.
- Dependency visibility: workflows declare `uses-stations`; stations declare `uses-model`.

## Canonical skeleton

```text
Backside/
  _models/
    moon-streak/
      moon-streak.gguf
      tokenizer.json
      card.json
    deepseek-coder/
    clip-vision/
    deberta-v3-large/
    mistral-7b-instruct/
    whisper-large-v3/

  stations/
    math-clarify/
      README.md
      _AGENT_BRIEF.md
      prompt.md
      station.py
      health_check.bat
      uses-model
    claim-extract/
    contradiction-scan/
    ME-tag-paragraph/
    describe-figure/
    deconstruct-picture/
    seven-q-score/
    fruits-score/
    axiom-hit/
    lossless-summarize/

  workflows/
    grade-paper/
      README.md
      _AGENT_BRIEF.md
      RUN.bat
      RUN_AGENT.bat
      health_check.bat
      prompt.md
      pipeline.py
      uses-stations
      00_DROP/
      OUTPUT/
      ARCHIVE/
    refresh-axiom-snapshot/
    route-and-convert/
    build-ai-portal/
    handoff-session/
    pull-link/
    deconstruct-picture/

  _archive/
    phase-logs/
    scratch/
    apps/
    root-leftovers/
```

## Mapping from current X:\ root workflows

- `X:\paper-proof-grader\` -> `Backside/workflows/grade-paper/`
- `X:\axioms\` -> `Backside/workflows/refresh-axiom-snapshot/`
- `X:\knowledge-refinery\` -> `Backside/workflows/route-and-convert/`
- `X:\ai-portal-generator\` -> `Backside/workflows/build-ai-portal/`
- `X:\session-handoff-drop\` -> `Backside/workflows/handoff-session/`
- `X:\link-pull-drop\` -> `Backside/workflows/pull-link/`
- `X:\models\` -> `Backside/_models/`

Publish-only sinks remain at root:

- `X:\proof-architecture\`
- `X:\proof-explorer\`

## Decision calls requested

1) Backside naming:
- Recommendation: repurpose `Backside/` as the workhorse layer and move current contents under `Backside/_archive/`.

2) stations concept:
- Recommendation: keep `stations/` distinct from `workflows/` to preserve reuse and avoid duplicated model-bound logic.

3) Moon-Streak naming:
- Recommendation: treat `moon-streak` as a callsign alias until pinned to a concrete model in `card.json` (`base_model`, `quant`, `license`, `checksum`).

## Implementation notes for a follow-up execution prompt

- No deletions: move + junction compatibility for legacy paths.
- Preserve current run buttons while introducing `Backside/workflows/*/RUN.bat`.
- Add root-level aggregate health check that validates:
  - all workflow local health checks
  - station health checks used by each workflow
  - model availability for every `uses-model` declaration.
