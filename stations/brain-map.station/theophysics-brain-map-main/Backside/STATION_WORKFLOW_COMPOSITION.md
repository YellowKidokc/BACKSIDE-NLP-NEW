# Station / Workflow Composition Contract

**What this is:** The rule that keeps Backside from becoming 20 duplicated mini-pipelines.
**Owner:** David Lowe + Codex
**Status:** live architecture contract
**Last updated:** 2026-05-20

## Decision

Stations do one task. Workflows aggregate stations.

```text
station = reusable single-task capability
workflow = ordered recipe that calls stations
packet = shared work unit that stations read/write
export = final reproducible package produced from packet state
```

The station is the reusable unit. Do not copy a station into each workflow folder. A workflow references station IDs in configuration, then calls the canonical station implementation.

## Why

Copying station logic into every workflow creates drift: one workflow fixes `seven-questions`, another keeps the old version, and the outputs stop being comparable. The durable pattern is one canonical station implementation plus many workflow recipes.

## Allowed Duplication

Duplicate these when useful:

- small workflow-specific prompt overlays,
- workflow configs,
- sample packets,
- README examples,
- compatibility launchers.

Do not duplicate these:

- station implementation code,
- station input/output schemas,
- station scoring rules,
- station health checks,
- station model routing.

## Canonical Station Folder

```text
X:\Backside\stations\<station-id>.station\
  README.md
  station.json
  station.py
  prompt.md
  health_check.bat
  tests\
```

`station.json` is the source of truth for:

- station ID,
- task boundary,
- accepted inputs,
- produced outputs,
- paths it must not touch,
- required model/service dependencies,
- verification commands.

## Workflow Folder

```text
X:\Backside\workflows\<workflow-id>.workflow\
  README.md
  dependencies.json
  configs\
    default.json
  00_DROP\
  OUTPUT\
  ARCHIVE\
  STATE\
```

`dependencies.json` lists what the workflow may call. `configs/*.json` says what it actually calls in a specific recipe.

## Composition Files

### `dependencies.json`

```json
{
  "schema": "theophysics.workflow.dependencies.v1",
  "workflow": "grade-paper",
  "stations": [
    "claim-extract",
    "seven-questions",
    "axiom-candidates",
    "contradiction-scan",
    "lossless-summarize"
  ],
  "models": ["deberta_nli", "sbert_minilm"],
  "external_services": [],
  "sinks": ["EXPORTS", "Backside/_state"]
}
```

### `configs/default.json`

```json
{
  "schema": "theophysics.workflow.config.v1",
  "workflow": "grade-paper",
  "name": "default",
  "packet_contract": "PACKETS_CONVENTION.md",
  "steps": [
    {
      "station": "claim-extract",
      "enabled": true,
      "input": "WORKING/source.md",
      "output": "WORKING/station-outputs/claim-extract/"
    },
    {
      "station": "seven-questions",
      "enabled": true,
      "input": "WORKING/station-outputs/claim-extract/",
      "output": "WORKING/station-outputs/seven-questions/"
    },
    {
      "station": "axiom-candidates",
      "enabled": true,
      "input": "WORKING/station-outputs/seven-questions/",
      "output": "WORKING/station-outputs/axiom-candidates/"
    }
  ],
  "exports": [
    "PUBLIC/index.html",
    "PUBLIC/workbook.xlsx",
    "MACHINE/manifest.json"
  ]
}
```

## Runtime Rule

A workflow runner resolves stations by ID:

```text
station id -> X:\Backside\stations\<station-id>.station
```

The workflow can wrap the station call, pass parameters, and decide ordering. It cannot fork the station into its own private copy unless the fork is explicitly promoted as a new station ID.

## Fork Rule

If a workflow needs different behavior, do one of these:

1. add params to the existing station if the task boundary is unchanged,
2. create a new station ID if the task boundary changes,
3. add a workflow prompt overlay if only wording changes.

Do not silently edit a copied station inside a workflow folder.

## Prompt Placement

Reusable prompts live with the station:

```text
Backside\stations\<station-id>.station\prompt.md
```

Workflow-specific orchestration prompts live with the workflow:

```text
Backside\workflows\<workflow-id>.workflow\prompts\
```

Assignment prompts for AI partners live in:

```text
00_WORKFLOWS\prompts\
Backside\prompts\
```

## Acceptance Check

Before a workflow is called "wired":

- every step references an existing station ID,
- every referenced station has `station.json`,
- every workflow dependency is declared in `dependencies.json`,
- every enabled step appears in `configs/default.json`,
- station outputs land inside the packet or declared export folder,
- no station implementation is copied into the workflow folder.
