# Agent Brief — axioms

**Workflow type:** <TBD — David to confirm>
**Owner:** shared
**Last updated:** 2026-05-16

---

## Mission

<TBD — David to confirm from X:\axioms\README.md + pipeline.py + config.json>

---

## When to use this

- <TBD — David to confirm>
- <TBD — David to confirm>
- <TBD — David to confirm>

---

## Available jobs

| Job | What it does | When to run |
|---|---|---|
| `RUN.bat` | <TBD — David to confirm> | <TBD — David to confirm> |
| `RUN_AGENT.bat` | Launches an LLM with this brief loaded as system context | When workflow-specific reasoning is needed |
| `health_check.bat` | Verifies required files/dirs and endpoint reachability | Before session start and before pipeline execution |

## Inputs

- **Accepted types:** <TBD — David to confirm>
- **Drop location:** `./00_DROP/`
- **Naming:** <TBD — David to confirm>

## Outputs

- **Lands in:** `./OUTPUT/`
- **Shape:** <TBD — David to confirm>
- **Downstream consumers:** <TBD — David to confirm>

## Archive

- Processed inputs move to `./ARCHIVE/` after success
- Failures stay in `./00_DROP/` with a `.error.json` sibling

## Prompts this workflow uses

Located in `./prompts/`:

- `<TBD — David to confirm>.md` — <TBD — David to confirm>

## Models / external services

- `<TBD — David to confirm>`

If any of these are unreachable, `health_check.bat` will report — do not bypass.

## Framework anchoring

This workflow operates inside the Theophysics framework. Load `X:\THEOPHYSICS_PRIMER.md` before reasoning steps.

- <TBD — David to confirm relevant law mapping>

If a workflow output contradicts canon: stop, flag contradiction artifact, and do not propagate.

## When you're stuck

1. Read `README.md` for the human-facing contract
2. Read `config.json` for paths and model names
3. Read `_LOGS/` for recent successful runs
4. Run `health_check.bat`
5. Escalate to comms hub with a one-line block report

## Don't do

- Don't write to `ARCHIVE/` manually
- Don't bypass `00_DROP/` by injecting to `OUTPUT/`
- Don't modify `config.json` without testing
- Don't delete files
- Don't introduce hardcoded `D:\` paths
- Don't push past the Feb 14, 2026 Boundary Proof
