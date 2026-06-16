# 03_YAML_METADATA

Owner: worker-1 (claude-code) — Round 1.

## What this lane does

Produces page-level and section-level metadata from the source document plus the 02 section ledger. This is the routing-ready filing layer: it answers "what is this artifact, where does it belong, who is it for, how mature is it" without computing the semantic vector or hash (those are owned by 04_TAGS).

## What it consumes

- `00_DROP/{article}.(html|md)` — raw source, for page meta extraction (title, slug, frontmatter, authors)
- `02_SECTION_MAP/{article}/section-map.json` — section ledger, for section-level metadata and rollup counts

## What it produces

Under `03_YAML_METADATA/{article-slug}/`:

- `frontmatter.yaml` — Obsidian-compatible YAML block, copy-pasteable into the final page
- `metadata.json` — machine-readable page metadata (canonical artifact)
- `metadata.md` — human-readable mirror with provenance ledger
- `section_metadata.json` — per-section metadata for downstream lanes and the Section_Metadata workbook tab

## Field families

### Identity

`paper_uuid`, `page_id`, `title`, `source_file_name`, `paper_slug`.

The `paper_uuid` is inherited from `02_SECTION_MAP/section-map.json` so it is identical across lanes.

### Routing (per `SEMANTIC_ADDRESS_AND_ROUTING.md`)

`primary_bucket`, `secondary_bucket`, `type`, `story_flag`, `series`, `series_article_number`, `status`, `maturity`, `website_layers`.

`story_flag` is explicit. The system confuses narrative content with generic notes if this is implicit, per the pinned naming rule.

### Address candidate (D/N/V/A/U/R only)

`domain`, `named_entity`, `state`, `audience`, `use`, `risk` plus a composed `address_string` of the form `D/N/V/A/U/R`. The vector portion (`G3M3...`) and the dominant/absent hash are owned by 04_TAGS — this lane sets `vector_string=null`, `hash=null`, and labels `vector_owner_lane="04_TAGS"` so the downstream join is explicit.

`candidate_confidence` is `high` when all six components are explicitly extracted from frontmatter or `<meta>` tags, `medium` when at least one is inferred from `<meta paper-slug>` series convention, `low` when more than one is inferred from heuristics over the title and first sections.

### Rollups

Inherited from `02_SECTION_MAP/section-map.json`: `section_count`, `equation_count`, `citation_count`, `inferred_section_count`. This lane does not recount — single source of truth lives in 02.

### Provenance

`extracted_fields`, `derived_fields`, `inferred_fields` list which field went which way. Required by station prompt: "Distinguish `extracted`, `derived`, and `inferred`."

## Routing heuristic

The lane resolves routing in this order, recording how each field was set:

1. **Frontmatter / `<meta>` direct.** If the source already exposes `domain`, `state`, `audience`, `risk`, or `series`, take them verbatim. Field marked `extracted`.
2. **Series convention.** `<meta name="paper-slug" content="gtq-03">` → `series=GTQ`, `series_article_number=03`, `primary_bucket=03_SERIES`. Marked `derived`.
3. **File-naming convention.** Filename matching `{SERIES}-{ARTICLE}[-{SUFFIX}].{ext}` per FILE-NAMING-SYSTEM.md gets parsed for series + article number. Marked `derived`.
4. **Story flag.** Type = `story` when `series` is in the known story series set (`GTQ`, `MDA`, `CROSS_DOMAIN`) OR when the title contains narrative markers. Marked `inferred` unless 1–3 made it explicit.
5. **Audience.** Default `GENERAL` for series pieces, `TEAM` for calibration/operational docs, `INTERNAL` for drafts. Marked `inferred`.
6. **Risk.** Defaults to `R1` (informational) unless the source declares R-tier explicitly. Marked `inferred`.
7. **Website layers.** Defaults to `[reader, academic, accessible, lossless_ai]`. Override when the source declares its own layer set.

## Calibration result (expected vs produced)

`CALIBRATION_pilot-preflight-checklist.md` has explicit frontmatter (`domain: AVIATION`, `state: F`, `audience: TEAM`, `risk: R4`) and all six address components extract cleanly:

| Field | Value | How |
|-------|-------|-----|
| domain | AVIATION | extracted |
| named_entity | PILOT_PRE_FLIGHT_CHECKLIST | derived from title |
| state | F | extracted |
| audience | TEAM | extracted |
| use | I | inferred (informational/instructional) |
| risk | R4 | extracted |
| address_string | AVIATION/PILOT_PRE_FLIGHT_CHECKLIST/F/TEAM/I/R4 | composed |
| candidate_confidence | medium | one inferred (`use`) |

Matches `configs/CALIBRATION_EXPECTED.md` exactly except for `use=I` being inferred (the calibration source does not declare it). 04_TAGS still owns the vector + hash; this lane records `vector_owner_lane=04_TAGS`.

## GTQ-03 result

| Field | Value | How |
|-------|-------|-----|
| paper_slug | gtq-03 | extracted (`<meta name="paper-slug">`) |
| series | GTQ | derived |
| series_article_number | 03 | derived |
| primary_bucket | 03_SERIES | derived |
| secondary_bucket | GTQ | derived |
| type | story | derived (series in story set) |
| story_flag | true | derived |
| state | F | inferred (article is on production layer) |
| website_layers | reader, academic, accessible, lossless_ai | default |

## How to run

```
python run.py --in 00_DROP/gtq-03-free-will-two-frames.html \
              --section-map 02_SECTION_MAP/gtq-03/section-map.json \
              --out 03_YAML_METADATA/gtq-03
```

The runner auto-locates the section-map next to it (sibling lane directory) when `--section-map` is omitted.

## Known gaps / drift to flag

1. `use` and `risk` defaults for narrative articles are heuristic. The real source of truth is David's editorial intent; this lane records them as `inferred` so 04 can flag mismatch.
2. Tags, chi-vars, law references are explicitly out of scope. They go to 04_TAGS.
3. `vector_string`, `hash` are NULL by design. Same drift note as 02 README.

## Files in this folder

- `contract.json`
- `README.md`
- `run.py`
- `run_prompt.md`
- `sample_output/CALIBRATION/` + `sample_output/gtq-03/`
