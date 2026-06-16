# Brain Snapshot Overview

## Purpose
Generate a reproducible, read-only snapshot of known Brain surfaces and produce three outputs:
- `EXPORTS/brain-overview/brain-overview.json`
- `EXPORTS/brain-overview/index.html`
- `EXPORTS/brain-overview/README.md`

## Scope
This generator inventories paths, metadata, ownership hints, and references from files (README/config/prompt docs). It does not run workflows, mutate files, or build a control plane.

## Inputs
- `X:\David`
- `X:\GUI`
- `X:\Conversions`
- `X:\EXPORTS`
- `X:\Backside`
- `D:\GitHub\theophysics-brain-map`
- Optional Postgres schema at `192.168.1.177:2665` if local credentials are available.

## Output Schema (high-level)
- `generated_at_utc`
- `host`
- `surfaces[]`
  - `label`
  - `source_of_truth_path`
  - `resolved_path`
  - `status` (`ok` or `unavailable`)
  - `last_modified_utc`
  - `items[]`
- `warnings[]`
- `connections[]`
- `postgres`

## Reproducibility
Run one command:

```bash
python Backside/overview_generator/generate_brain_overview.py
```

The command rewrites JSON/HTML/Markdown outputs from current filesystem state.
