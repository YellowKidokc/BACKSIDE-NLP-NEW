# 04_TAGS — Tags Lane

Owner this round: **worker-2** (claude-code-worker-2) — round-1 swarm.
Pipeline step: **6**. Upstream: `02_SECTION_MAP`, `03_YAML_METADATA`. Downstream: `09_GRAPH_LINKS`, `10_RIGOR`, `15_SECTION_PACKETS`.

## What this lane does

Attaches a semantic tag layer on top of upstream section structure. Tag layer is the lightweight, fast surface that lets graph-links, rigor, and per-section packets target the right Master Equation variables, the right Laws (1–10), the right axioms, and the right workflow conditions (needs-math, needs-citation, needs-rigor, etc.).

The semantic address is composed here: **lane 04 mints the 10-variable vector + semantic_hash** via `configs/shared_lib/address.py` (`score_vector`, `vector_string`, `semantic_hash`) and joins them with the D/N/V/A/U/R `address_candidate` emitted by **lane 03_YAML_METADATA**. Lane 02 is narrow (section structure only) per `lane_registry.json` notes and `CALIBRATION_EXPECTED.md`. Do not fork the hash format — call `semantic_hash()` from shared_lib, do not hand-roll. *(Contract text updated 2026-05-22 review pass; prior README incorrectly said lane 02 owned the address.)*

## Inputs

| Required | Source |
|---|---|
| `section-map.json` | `02_SECTION_MAP/` (worker-1 round-1) |
| `frontmatter.yaml` + `metadata.json` | `03_YAML_METADATA/` (worker-1 round-1) |
| `normalized-text.md` | `01_LOSSLESS/` |
| `address.py`, `schemas.py:SemanticTag` | `configs/shared_lib/` |

If `02` or `03` outputs aren't present yet, the lane mocks a minimal section_map from the raw drop file and records the mock under `tags.json.provenance.mocked = true`. The lane does not block waiting for upstream — David's round-1 call: *"If upstream is missing, mock the input, document it, and keep going."*

## Outputs

| Artifact | Form |
|---|---|
| `tags.json` | Machine-readable. Page-level + per-section tag arrays. SemanticTag-shaped. |
| `section-tags.csv` | Excel-ready flat projection. Columns mirror `excel_columns.Tags`. |
| `page-tag-summary.md` | Human-readable rollup. |
| `semantic-address.json` | Confirmation copy of lane 02's address + recomputed vector + drift status. |

JSON first, Markdown/HTML second, CSV third. Excel `Tags` sheet is a rollup of `section-tags.csv`, not the source of truth.

## Tag taxonomy

- **chi_vars** — `chi_G`, `chi_M`, `chi_E`, `chi_S`, `chi_T`, `chi_K`, `chi_R`, `chi_Q`, `chi_F`, `chi_C`. One tag per dominant variable in the section.
- **laws** — `Law_1` … `Law_10`. Tag when a section names or operates on a Law.
- **master_equation_uuid** — populated when section invokes the Master Equation.
- **axiom refs** — when sections reference axioms from the 188-axiom corpus or 22 PUB axioms.
- **workflow tags** — `needs-math`, `needs-citation`, `needs-rigor`, `needs-evidence`, `calibration-input`, `story`, `operational`, `kill-condition`.
- **domain badges** — pulled from `shared_lib/schemas.py:DomainBadge`. Extends with `AVIATION`, `SAFETY`, `PROCEDURE` for the calibration article.

## How to run

This lane is LLM-first-pass for round-1. See `run_prompt.md` for the copy-paste prompt. The `7q-classifier.station` is the intended long-term home but it currently scores rigor, not tags — wiring it for tags is round-2 work.

For calibration:

1. Read `00_DROP/CALIBRATION_pilot-preflight-checklist.md`.
2. Read `configs/CALIBRATION_EXPECTED.md` to know the target.
3. Produce `sample_output/calibration/{tags.json,section-tags.csv,semantic-address.json,page-tag-summary.md}`.
4. Verify the recomputed vector is exactly `G3M3E0S0T3K3R3Q0F0C0`.

## Known gaps

- `02_SECTION_MAP` and `03_YAML_METADATA` are not produced yet (worker-1 round-1 owns these). Sample output uses mocked upstream derived from the raw drop file. When worker-1 lands real outputs, this lane consumes them and the mock provenance flag flips off.
- `7q-classifier.station` does rigor scoring, not tag classification — a tag-classifier model wiring is a round-2 item.
- `chi-tagging.workflow` exists in `\\dlowenas\brain\Backside\workflows\` and may already have chi-var heuristics worth pulling in. Not consumed this round.
- FAP outputs at `\\dlowenas\brain\Backside\knowledge-refinery\13_SOURCE_SYSTEMS\FAP` not yet inspected for tag overlap — flagged but not blocking per round-1 call.

## Loopback conditions

Written to `14_LOOPBACK_REVIEW/04_tags_loopback.json` when:

1. Vector cannot be deterministically computed from upstream `section_map` (block_types missing or section text empty).
2. Section text yields zero recognizable signals (chi/law/workflow) AND domain = `THEOPHYSICS` — implies upstream lossless or section-split failure.
3. Tag count exceeds 50 per section (prompt drift / over-tagging).

## Excel columns

Tab: `Tags`. Columns: `paper_uuid`, `page_id`, `section_id`, `tag_id`, `tag_type`, `label`, `chi_vars`, `master_equation_uuid`, `source_quote`, `confidence`, `provenance`. Aligned to `MASTER_INDEX_WORKBOOK_CONTRACT.md`.
