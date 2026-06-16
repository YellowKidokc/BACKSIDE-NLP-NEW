# Brain Graph Layer Decision - 2026-05-20

**What this is:** Decision note for adding an Open-Brain-Map-style semantic graph over the Brain.
**Status:** approved direction / not yet implemented
**Reference:** `https://github.com/mgiesen/Open-Brain-Map`

## Decision

The Brain needs a graph layer.

This layer should map the relationships between:

- Postgres tables and row families,
- X-drive folders,
- Backside workflows,
- Backside stations,
- models,
- prompt packs,
- exports,
- Obsidian vaults,
- comms rooms,
- GitHub repos,
- vector collections,
- dashboards and conversion surfaces.

The graph layer is not the source of truth. It is a navigation and relationship layer over the sources of truth.

## Why Now

The root cleanup and station/workflow contracts created enough structure that a graph layer can be generated instead of hand-drawn.

Major-scale prompt work is still useful here because the graph needs ubiquitous extraction across many folders:

```text
folder -> node
README/frontmatter -> node metadata
dependencies/configs -> calls/depends_on edges
EXPORTS manifests -> exports_to / derived_from edges
Postgres schema -> table/entity nodes
station/workflow configs -> calls edges
prompt banks -> documents / instructs edges
```

## Not A Workflow Replacement

Individual workflows still need to be built one by one.

The graph pass sits above them:

1. establish graph schema,
2. extract nodes/edges broadly,
3. use graph gaps to decide which individual workflow to build next.

## Next Prompt

Use:

```text
00_WORKFLOWS\prompts\brain-graph-layer\00_BRIEF.md
```
