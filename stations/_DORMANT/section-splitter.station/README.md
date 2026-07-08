# section-splitter.station

Purpose: split a source document into stable, reusable sections for downstream HTML, claims, vectors, graph, and rigor work.

## Why this exists

Every later lane depends on section-level work. If sections are unstable, then tags, vectors, graph edges, math payloads, and HTML boxes drift.

## Inputs

- raw HTML
- Markdown
- canonical text

## Outputs

- ordered section list
- stable `section_id` values
- heading hierarchy
- section boundary offsets
- per-section text packets

## Required behavior

- preserve source order
- preserve headings when present
- infer headings when absent, but mark them as inferred
- keep equations attached to the nearest valid section
- keep citations attached to the section where they appear
- emit machine-readable JSON and a readable Markdown summary

## Downstream

- `03_YAML_METADATA`
- `04_TAGS`
- `05_CLAIMS`
- `07_MATH_TRANSLATION`
- `08_SECTION_VECTORS`
- `09_GRAPH_LINKS`
- `10_RIGOR`

## Status

Draft skeleton created 2026-05-22.
