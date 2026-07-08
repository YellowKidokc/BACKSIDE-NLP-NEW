# 03_YAML_METADATA — Run Prompt (AI fallback)

Use this only if `run.py` is not available. Field names are mandatory; do not invent synonyms.

## Inputs

- Source file (HTML or Markdown).
- `02_SECTION_MAP/{article}/section-map.json`.

## Task

Emit four files in `03_YAML_METADATA/{article-slug}/`:

1. `frontmatter.yaml` — Obsidian-compatible YAML block.
2. `metadata.json` — full page metadata, canonical artifact.
3. `metadata.md` — human-readable mirror.
4. `section_metadata.json` — array of per-section metadata.

## Required fields

### Identity
`paper_uuid`, `page_id`, `title`, `source_file_name`, `paper_slug`.

`paper_uuid` must equal `section-map.json.paper_uuid` exactly.

### Routing (per SEMANTIC_ADDRESS_AND_ROUTING.md)
`primary_bucket` ∈ {01_CANON, 02_THEORIES, 03_SERIES, 04_FRAMEWORKS, 05_EVIDENCE, 06_DRAFTS, 07_PUBLISH, 08_ARCHIVE, 09_MEDIA}
`secondary_bucket`, `type` ∈ {paper, note, axiom, claim, evidence, dashboard, story}
`story_flag` (boolean, REQUIRED EXPLICIT), `series`, `series_article_number`, `status`, `maturity`,
`website_layers` (list).

### Address candidate (D/N/V/A/U/R only — vector/hash belong to 04)
`domain`, `named_entity`, `state`, `audience`, `use`, `risk`, `address_string` (composed), `vector_string=null`, `hash=null`, `vector_owner_lane="04_TAGS"`, `candidate_confidence` ∈ {high, medium, low}.

### Rollups (copy from section-map.json, do not recount)
`section_count`, `equation_count`, `citation_count`, `inferred_section_count`.

### Provenance
`extracted_fields`, `derived_fields`, `inferred_fields` — three string lists naming which fields landed which way. Required by station prompt.

## Routing logic (in order)

1. Use frontmatter/`<meta>` values verbatim when present (extracted).
2. `<meta name="paper-slug">` like `gtq-NN`, `mda-NN`, `cd-NN` → series + article + primary_bucket=03_SERIES (derived).
3. Parse the filename pattern `{SERIES}-{ARTICLE}[-{SUFFIX}].{ext}` (derived).
4. `story_flag=true` when series ∈ {GTQ, MDA, CROSS_DOMAIN} or title carries narrative markers (inferred).
5. Audience default `GENERAL` for series, `TEAM` for operational, `INTERNAL` for drafts (inferred).
6. Risk default `R1`. Calibration-style frontmatter overrides.
7. Website layers default `[reader, academic, accessible, lossless_ai]`.

## section_metadata.json shape

Array of:
```
section_id, stable_uuid, ordinal, heading_level, heading_text, heading_path,
parent_section_id, source_anchor, inferred, equation_count, citation_count,
word_count, type_hint, yaml_anchor, passes_pointer
```

`type_hint` ∈ {body, callout, equation, kill_condition, risk, summary, tangent, media, nav}.
Heuristic: heading_text matches `kill|risk|summary|tangent|media` → corresponding type_hint; equation_count > 5 → `equation`; otherwise `body`.

## Loopback triggers

Write to `14_LOOPBACK_REVIEW/03_yaml-metadata_loopback.json` and set `loopback.triggered=true` when:

- `02_SECTION_MAP/{article}/section-map.json` missing.
- Frontmatter declares routing fields conflicting with derived ones.
- `primary_bucket` cannot be resolved to a canonical bucket.
- `story_flag=true` but `type` is not `story`.

## When done

```
[worker-1] Lane 03 YAML+Filing — STATUS: testable. Article: {slug}. address_candidate: {addr}. Confidence: {h|m|l}. Sample: 03_YAML_METADATA/{slug}/metadata.json
```
