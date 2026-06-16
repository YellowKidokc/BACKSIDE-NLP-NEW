# KnowledgeRefineryBackplane

Purpose: the repo-side control packet for the automated paper-to-vault
production line.

This is the back-of-house workflow. David-facing folders stay simple; this
packet describes the sequence that runs after a paper or source bundle enters
production.

## Intended Flow

```text
source in
-> source registry lookup
-> paper grading / claim extraction
-> model station checks
-> axiom and rigor gates
-> summary layers
-> Obsidian export
-> AI portal package
-> archive
```

## Folders

- `INPUT`: files waiting to be processed
- `OUTPUT`: finished outputs
- `REVIEW`: items needing review
- `ARCHIVE`: completed source/output bundles
- `ERROR`: failures or kicked-back items
- `CONFIG`: local config and config examples
- `FRONT_DOORS`: human-facing intake folders that should remain simple
- `SOURCE_SYSTEMS`: registered external systems the backplane calls into
- `MODEL_STATIONS`: station control folders in front of local models
- `PROMPTS`: LLM prompts used by this workflow
- `SCRIPTS`: implementation scripts
- `LOGS`: runtime logs

## Scripts

- `RUN_PIPELINE.bat`: run full workflow
- `RUN_THIS_STAGE.bat`: run this packet only
- `TROUBLESHOOT.bat`: dependency and folder checks

## Boundary

This repo does not store model weights, vector indexes, private vault dumps, or
runtime databases. It stores the contracts and entrypoints that let another AI
partner or local runner operate the live systems.
