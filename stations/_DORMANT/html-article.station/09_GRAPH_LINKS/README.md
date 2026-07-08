# 09_GRAPH_LINKS - Graph Links Lane

Owner this round: **worker-4**. Pipeline step: **11**. Upstream: `08_SECTION_VECTORS` (hard), `02_SECTION_MAP` (hard), `03_YAML_METADATA` (hard). Preferred upstream: `04_TAGS`, `05_CLAIMS`, `07_MATH_TRANSLATION`. Downstream: `10_RIGOR`, `12_EXPORTS`, `15_SECTION_PACKETS`, `16_FINAL_PAGE_ASSEMBLY`.

## What this lane does

Produces graph-ready edge candidates between sections using the strongest signals already available:

- vector similarity
- claim overlap
- chi/law tag overlap
- structural dependencies visible in the section map

This lane does **not** own graph storage. It only emits candidate edges in a stable, machine-readable shape so downstream lanes can review or persist them.

## Inputs

| Required | Source |
|---|---|
| `section-vectors.jsonl` | `08_SECTION_VECTORS/` |
| `section-map.json` | `02_SECTION_MAP/` |
| `metadata.json` | `03_YAML_METADATA/` |

Preferred when present:

- `04_TAGS/tags.json`
- `05_CLAIMS/claim-packets.json`
- `07_MATH_TRANSLATION/math-payload.json`

If tags or claims are absent for the current article, lane 09 derives lightweight local signals from section headings + packet text and records `provenance.mocked = true`. That follows the round rule: mock, document, keep moving.

## Outputs

| Artifact | Form |
|---|---|
| `graph-edges.json` | Machine-readable source of truth |
| `graph-edges.csv` | Excel/workbook-friendly flat projection |
| `graph-review.md` | Human QA note with top edges and gap notes |

## Edge vocabulary

This lane keeps edge types narrow:

- `THEMATIC_SIMILARITY`
- `CLAIM_OVERLAP`
- `VARIABLE_OVERLAP`
- `LAW_FAMILY`
- `CROSS_DOMAIN`
- `STRUCTURAL_DEPENDENCY`

Calibration specifically expects:

- `checklist -> kill_condition`
- `checklist -> risk`

Those can land as `STRUCTURAL_DEPENDENCY` edges as long as the evidence notes make the relationship explicit.

## How to run

```powershell
py -3 "X:\Backside\workflows\html-article.workflow\09_GRAPH_LINKS\run.py" --article calibration
py -3 "X:\Backside\workflows\html-article.workflow\09_GRAPH_LINKS\run.py" --article gtq-03
```

Optional overrides:

- `--vectors <path>`
- `--section-map <path>`
- `--metadata <path>`
- `--tags <path>`
- `--claims <path>`
- `--math <path>`
- `--output-dir <path>`

## Design stance

- JSON first, CSV second, Markdown third.
- Sort and dedupe edges so reruns stay idempotent.
- Do not invent a second graph persistence layer inside this lane.

## Known gaps

- `graph-linker.station` is still a skeleton, so round-1 uses a workflow-native deterministic wrapper here.
- GTQ-03 claims are not yet present from worker-2 at the time this lane was wired. The GTQ sample output therefore uses documented local claim signals rather than pretending full claim packets already exist.
- Contradiction-based edges stay out of round-1 because lane 06 owns that signal.

## Loopback conditions

Written to `14_LOOPBACK_REVIEW/09_graph_links_loopback.json` when:

1. Lane 08 vectors are missing or do not cover all `section_id` values.
2. A multi-section article produces zero edges.
3. Edge count explodes above `5 x section_count`.
4. Duplicate edge ids survive dedup.

## Excel columns

Tab: `Graph_Edges`. Columns: `paper_uuid`, `page_id`, `edge_id`, `source_id`, `target_id`, `edge_type`, `weight`, `evidence`, `provenance`.
