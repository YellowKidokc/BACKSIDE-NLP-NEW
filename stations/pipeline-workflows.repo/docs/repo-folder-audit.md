# Repo Folder Audit

Rule: Git is the governor/spec layer. NAS/Z/X drives are runtime/body. Keep only durable source, schema, registry, workflow definitions, reusable templates, tests, and durable docs.

## Current Map

| Path | Decision | Reason |
| --- | --- | --- |
| `.gitignore` | KEEP | Source control boundary for runtime artifacts. |
| `docs/` | KEEP | Durable documentation. |
| `docs/imported/` | KEEP | Imported reference docs; audit later for staleness, but content is durable. |
| `engines/` | KEEP | Executable source. |
| `models/` | KEEP | Top-level model registry only; model weights stay out. |
| `preferences/` | KEEP | Preference defaults and profiles. |
| `preferences/1defaults.json` | REMOVE | Duplicate of `preferences/defaults.json`. |
| `preferences/engines/` | REMOVE | Not present; do not add until real preference engines exist. |
| `prompts/` | KEEP | Reusable prompt templates. |
| `schemas/` | KEEP | Single schema/contract home. |
| `contracts/schemas/` | REMOVE | Not present; avoid duplicate schema boundary. |
| `scripts/` | KEEP | Executable source/launch utilities. |
| `signals/` | MERGE | README-only taxonomy already lives in `docs/reciprocal-signals.md`. |
| `stations/` | KEEP | Station registry plus meaningful station configs. |
| `stations/source/` | NEEDS_DAVID_CALL | Not present. Keep audit-only if approved snapshots appear; otherwise do not add. |
| `stations/<category>/` | KEEP | Category folders contain meaningful station configs. |
| `templates/` | KEEP | Reusable packet/sandbox templates. |
| `tests/` | KEEP | Tests and small fixtures. |
| `workflows/*.json` | KEEP | Workflow definitions. |
| `workflows/WORKFLOW_REGISTRY.json` | KEEP | Registry. |
| `workflows/<Packet>/CONFIG` | KEEP | Example config contracts. |
| `workflows/<Packet>/PREFS` | KEEP | Workflow preference contracts. |
| `workflows/<Packet>/PROMPTS` | KEEP | Workflow prompt templates. |
| `workflows/<Packet>/SCRIPTS` | KEEP | Executable workflow source. |
| `workflows/<Packet>/README.md` | KEEP | Durable packet docs. |
| `workflows/<Packet>/INPUT` | REMOVE | Runtime body, created locally. |
| `workflows/<Packet>/OUTPUT` | REMOVE | Runtime body, created locally. |
| `workflows/<Packet>/REVIEW` | REMOVE | Runtime body, created locally. |
| `workflows/<Packet>/ARCHIVE` | REMOVE | Runtime body, created locally. |
| `workflows/<Packet>/ERROR` | REMOVE | Runtime body, created locally. |
| `workflows/<Packet>/LOGS` | REMOVE | Runtime body, created locally. |
| `pipeline.config.json` | REMOVE | Local runtime config, not source truth. |
| `pipeline.config.example.json` | KEEP | Reusable local config template. |
| `MANIFEST.json` | REMOVE | Runtime state, not source truth. |
| `logs/` | REMOVE | Runtime logs, not source truth. |
| `docs/reorg/` | REMOVE | Not present; do not add permanent reorg clutter. |

## PR Shape

- Remove committed runtime `.gitkeep` files from real workflow packet bodies.
- Keep packet skeletons in `templates/`, where folder placeholders are reusable templates.
- Collapse `signals/` into `docs/reciprocal-signals.md`.
- Replace committed `pipeline.config.json` with `pipeline.config.example.json`.
- Keep `schemas/` as the only schema/contract boundary.
- Remove duplicate `preferences/1defaults.json`.
