# Prompt: Brain Graph Layer / Knowledge System Map

**Date:** 2026-05-20
**Reference pattern:** `mgiesen/Open-Brain-Map`
**Repo:** `D:\GitHub\theophysics-brain-map`
**Live root:** `X:\` = `\\dlowenas\brain`

## Assignment

Design the Brain graph layer: a map of knowledge systems, folders, workflows, stations, prompts, exports, models, and database-backed entities.

This is not a replacement for Postgres, Obsidian, files, or workflow folders. It is the visible semantic map over them.

## Why this exists

The Brain now has multiple storage systems:

- X-drive folders
- Backside workflows
- Backside stations
- models
- exports
- prompt banks
- Postgres tables
- Obsidian vaults
- comms records
- GitHub repos
- vector/embedding stores

Each system knows part of the truth. The graph layer shows how they relate.

## Reference Pattern

`Open-Brain-Map` is useful because it treats knowledge as nodes with descriptions and links. It supports local/browser use, saved map files, general links, and rich node extensions.

The Theophysics version should keep that spirit but point at our actual runtime systems.

## Required Output

Create these repo artifacts:

```text
GRAPH_LAYER_SPEC.md
Backside\graph_layer\
  README.md
  schema\
    brain_node.schema.json
    brain_edge.schema.json
    graph_export.schema.json
  examples\
    x_root_sample.graph.json
    station_workflow_sample.graph.json
  prompts\
    extract_graph_from_folder.md
    extract_graph_from_workflow.md
    extract_graph_from_postgres.md
```

## Node Types

At minimum:

```text
folder
workflow
station
model
prompt_pack
export_package
postgres_table
postgres_row_family
obsidian_vault
canon_doc
comms_room
github_repo
vector_collection
service
dashboard
conversion_surface
```

## Edge Types

At minimum:

```text
contains
calls
depends_on
reads_from
writes_to
exports_to
indexes
mirrors
documents
supersedes
blocks
verifies
promotes_to
derived_from
owned_by
```

## Contract

Every graph node must have:

```json
{
  "id": "stable-human-readable-id",
  "type": "workflow",
  "label": "Paper Proof Grader",
  "summary": "Grades papers and emits audit artifacts.",
  "primary_path": "X:\\Backside\\workflows\\paper-proof-grader.workflow",
  "source_of_truth": "filesystem",
  "status": "live",
  "owner": "shared",
  "links": []
}
```

Every graph edge must have:

```json
{
  "from": "paper-proof-grader.workflow",
  "to": "seven-questions.station",
  "type": "calls",
  "evidence": "dependencies.json",
  "confidence": "high"
}
```

## Major-Scale Sweep

This is the next useful ubiquitous prompt pass.

Apply the graph extraction prompt across:

```text
X:\David
X:\GUI
X:\Conversions
X:\EXPORTS
X:\Backside
D:\GitHub\theophysics-brain-map
```

Then expand to:

```text
Postgres at 192.168.1.177:2665
O:\_Theophysics_v4 or v5
comms rooms
GitHub repos
vector collections / embeddings
```

## What Not To Do

Do not build a giant diagram by hand.

Do not make the graph layer the source of truth. It is an index and navigation layer over existing sources of truth.

Do not duplicate workflow/station logic into the graph layer.

Do not promote guessed relationships as confirmed. Use confidence labels:

```text
high       directly declared in config/schema/file
medium     inferred from README/path naming plus local evidence
low        plausible but needs human review
```

## Acceptance Condition

The first pass is done when:

- `GRAPH_LAYER_SPEC.md` exists,
- graph node/edge schemas exist,
- sample graph JSON validates,
- at least one folder-level map and one station/workflow map exist,
- the graph distinguishes actual source-of-truth systems from navigation/index layers,
- the next sweep can ingest additional folders without rewriting the schema.

## /PROBE

The failure mode is making a pretty map that is not operationally binding. The graph must be anchored to actual paths, actual database tables, actual workflow configs, and actual export manifests. If the graph cannot route a future AI partner from "what is this?" to "where is the source of truth?" it is decorative and should be rejected.
