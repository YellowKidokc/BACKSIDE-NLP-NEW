# Excel Output Plan — claude-code owned lanes

**Author:** claude-code
**Date:** 2026-05-17
**Lanes covered:** `nlp` (15) · `nli` (5) · `embed` (2) · `rerank` (1) · `time` (1) · `graph` (2) · `pub` (2) · `red` (1) = **29 stations**

This is a spec (no code). All workbooks land per-station in that station's existing `output/` folder. Per-lane roll-up dashboards land in `STATIONS/_dashboards/`. Schemas are stable within a lane so workbooks join cleanly on shared IDs.

---

## 1. Universal conventions

### 1.1 Shared ID system

Every sheet across every workbook uses these keys when present. Same column name = same meaning across stations.

| Column         | Format                                  | Notes |
|----------------|------------------------------------------|-------|
| `run_id`       | `R-YYYYMMDD-HHMMSS-<hash6>`              | unique per station invocation; e.g. `R-20260517-101523-a3f491` |
| `station_id`   | `ST-LANE-NNN`                            | per-lane sequence, from registry |
| `doc_id`       | `D-<sha256[0:10]>` of source file        | stable across runs and stations |
| `claim_id`     | `C-NNN`                                  | from `claim_extractor` (ST-CLAIM-001); never re-minted by downstream |
| `axiom_id`     | native (`A1.1`, `D2.1`, `BC4`, `E13.1`)  | from STRAIGHT.md when corpus consolidation completes |
| `pair_id`      | `P-<run_id>-<NNN>`                       | NLI pair index within a run |
| `sentence_id`  | `S-<doc_id>-<NNN>`                       | EMBED per-sentence index, stable per-doc |
| `node_id`      | `<TYPE>-<NNN>` (e.g. `C-001`, `E-001`)   | graph nodes; reuses `claim_id` where claim-typed |
| `edge_id`      | `E-<run_id>-<NNN>`                       | graph edges, run-scoped |
| `event_id`     | `EV-<doc_id>-<NNN>`                      | temporal events, doc-scoped |
| `started_at` / `ended_at` | ISO 8601 (`2026-05-17T10:15:23`) | UTC; no timezone suffix |
| `status`       | `ok` \| `error` \| `partial` \| `stub`   | runner exit state |

### 1.2 File location pattern

Two locations per station, one optional:

- **Required (detail workbook):** `stations/<folder>/output/<short_name>.xlsx` — same folder as `result.json` and `result.md`. Rolling append across runs.
- **Optional (per-lane dashboard):** `STATIONS/_dashboards/lane_<lane>.xlsx` — cross-station aggregate for the lane. Maintained by a separate `_tools/dashboard_rebuilder.py` (not in scope for this spec).

### 1.3 Workbook naming

`<short_folder_name>.xlsx` — e.g. `nli_strong.xlsx`, `semantic_drift.xlsx`. No `station_id` in filename; the ID is in every sheet's `station_id` column.

### 1.4 Universal `RUNS` sheet (every workbook)

Always present. One row per invocation. Stable across all 29 stations.

| Column          | Type   | Notes |
|-----------------|--------|-------|
| `run_id`        | string | PK |
| `station_id`    | string | from registry |
| `doc_id`        | string | nullable for queries without a doc (rerank) |
| `model_used`    | string | resolved model id/name (`M-NLI-STRONG-001`, `gpt-4o-mini`, etc.) |
| `started_at`    | datetime | |
| `ended_at`      | datetime | |
| `status`        | string | `ok`/`error`/`partial`/`stub` |
| `error`         | string | nullable; error message if status != `ok` |
| `input_path`    | string | absolute path to input file |
| `output_json_path` | string | absolute path to `result.json` (or station-specific name) |
| `output_md_path`   | string | absolute path to `result.md` |
| `notes`         | string | freeform, optional |

### 1.5 What is NOT in Excel

- **Vectors.** Embedding vectors stay in `.npy` or JSON. Excel sheets carry a reference path + offset, not the float arrays.
- **Full source text.** Source markdown stays in `source.md` / `input/`. Sheets carry doc_id + path, plus short text spans where useful (≤ 500 chars).
- **Prompts.** Prompts live in `PROMPT_SYSTEM.md` / `PROMPT_TEST.md`. Sheets reference filename only.

---

## 2. NLI lane (5 stations)

**Stations:** `ST-NLI-001` nli_strong · `ST-NLI-002` nli_claim · `ST-NLI-003` nli_alt · `ST-NLI-004` nli_base · `ST-NLI-005` contradiction_scan

**Schema is shared across all 5.** Stations 001-004 are pure pair classifiers; 005 (contradiction_scan) extracts claims first then runs NLI against the axiom canon — same pair shape, plus two extra sheets.

### Workbook: `<station_folder>/output/<short>.xlsx`

| Sheet | Purpose | Columns |
|-------|---------|---------|
| `RUNS` | universal | (see §1.4) + `n_pairs` (int), `n_contradictions` (int), `n_entailments` (int), `n_neutrals` (int) |
| `PAIRS` | one row per (premise, hypothesis) pair | `run_id`, `pair_id`, `premise` (≤500 chars), `premise_full_ref` (path:line), `hypothesis` (≤500 chars), `hypothesis_full_ref`, `label` (`entailment`/`neutral`/`contradiction`), `score_entailment` (float), `score_neutral` (float), `score_contradiction` (float), `top_label_confidence` (float), `pair_source` (`input_file`/`auto_generated`) |
| `SUMMARY` | per-run aggregates | `run_id`, `n_pairs`, `pct_entailment`, `pct_neutral`, `pct_contradiction`, `mean_entail_score`, `mean_contradict_score`, `max_contradict_score`, `min_entail_score` |
| `LABEL_HIST` | distribution per run (long form) | `run_id`, `label`, `count`, `pct` |

### Mirrors JSON/MD

- JSON: `result.json` → fields `{station, model, n, results: [...], computed_at}` → `RUNS` + `PAIRS`
- MD: `result.md` (human summary) → mirrored by `SUMMARY` + `LABEL_HIST`

### ST-NLI-005 (contradiction_scan) adds two sheets

| Sheet | Purpose | Columns |
|-------|---------|---------|
| `CLAIMS` | claims extracted from source.md | `run_id`, `claim_id`, `doc_id`, `claim_text` (≤500), `claim_full_ref` |
| `CONTRADICTIONS` | filtered contradictions vs canon | `run_id`, `claim_id`, `axiom_id`, `axiom_text` (≤500), `contradiction_score` (float), `severity` (`high`/`medium`/`low`), `requires_review` (bool) |

---

## 3. EMBED lane (2 stations)

**Stations:** `ST-EMBED-001` sci_embed (SPECTER2, paper-level CLS, dim=768) · `ST-EMBED-002` embed_general (MiniLM, per-sentence, dim=384)

### Workbook: `<station_folder>/output/<short>.xlsx`

| Sheet | Purpose | Columns |
|-------|---------|---------|
| `RUNS` | universal | (§1.4) + `dim` (int), `n_sentences` (int), `vector_file_path` (.npy), `vector_format` (`npy`/`json`) |
| `SENTENCES` | one row per embedded unit (paper for sci_embed, sentence for embed_general) | `run_id`, `sentence_id`, `doc_id`, `ordinal` (int), `text` (≤500), `text_full_ref`, `char_count`, `token_count_est`, `dim`, `vector_offset` (int — row index in `.npy`), `is_title` (bool, sci_embed only) |
| `DOCS` | per-doc rollup | `doc_id`, `doc_path`, `n_sentences`, `total_chars`, `first_seen_run_id`, `last_seen_run_id`, `embedding_count` |
| `SIM_SAMPLES` | optional self-similarity diagnostic | `run_id`, `sentence_id_a`, `sentence_id_b`, `cosine`, `sample_kind` (`adjacent`/`random`) |

### Mirrors JSON/MD

- JSON: `result.json` → `{station, model, n_sentences, dim, embeddings: [[...]], sentences: [...]}` → `RUNS` + `SENTENCES` (vectors written to sibling `.npy`)
- MD: `result.md` → `RUNS` + `DOCS`

---

## 4. RERANK lane (1 station)

**Station:** `ST-RERANK-001` rerank (cross-encoder; scores `(query, passage)` pairs)

### Workbook: `rerank/output/rerank.xlsx`

| Sheet | Purpose | Columns |
|-------|---------|---------|
| `RUNS` | universal | (§1.4) + `query_id`, `n_passages`, `top_score`, `score_spread` |
| `QUERIES` | one row per query | `run_id`, `query_id`, `query_text` (≤500), `query_full_ref`, `n_passages`, `top_passage_id`, `top_score` |
| `RANKED` | one row per (query, passage) — sorted by score desc within query | `run_id`, `query_id`, `passage_id`, `rank` (int, 1-based), `score` (float), `passage_text` (≤500), `passage_full_ref`, `passage_chars`, `from_source` (`input_json`/`upstream_embed`) |
| `SUMMARY` | per-run aggregates | `run_id`, `query_id`, `n_passages`, `top_score`, `median_score`, `bottom_score`, `spread` |

### Mirrors JSON/MD

- JSON: `result.json` → `{station, query, ranked: [{passage, score}]}` → `RUNS` + `QUERIES` + `RANKED`
- MD: `result.md` (top-N ordered list) → `RANKED` filtered by `rank <= 10`

---

## 5. TIME lane (1 station — stub today)

**Station:** `ST-TIME-001` timeline (currently a stub awaiting model/library decision; schema reserved)

### Workbook: `timeline/output/timeline.xlsx`

| Sheet | Purpose | Columns |
|-------|---------|---------|
| `RUNS` | universal | (§1.4) + `n_events`, `date_range_start`, `date_range_end` |
| `EVENTS` | one row per extracted event | `run_id`, `event_id`, `doc_id`, `span_start` (int, char offset), `span_end` (int), `raw_text` (≤500), `normalized_date` (ISO date or range), `date_precision` (`year`/`month`/`day`/`time`), `event_type` (string), `confidence` (float) |
| `DOC_STATS` | per-doc rollup | `doc_id`, `latest_run_id`, `n_events`, `date_range_start`, `date_range_end`, `min_confidence`, `mean_confidence` |
| `STUB_NOTES` | until wired, one row | `run_id`, `status` (`stub`), `note`, `awaiting` |

### Mirrors JSON/MD

- JSON: `result.json` → eventually `{events: [{text, date, type}]}` → `RUNS` + `EVENTS`
- MD: stub notes → `STUB_NOTES`

---

## 6. GRAPH lane (2 stations)

**Stations:** `ST-GRAPH-001` knowledge_graph (deterministic — reads all upstream artifacts) · `ST-GRAPH-018` knowledge_graph_extractor (model-backed, M-GRAPH-001)

**Shared schema** — both emit nodes + edges with the same type vocabulary.

### Workbook: `<station_folder>/output/<short>.xlsx`

| Sheet | Purpose | Columns |
|-------|---------|---------|
| `RUNS` | universal | (§1.4) + `node_count`, `edge_count`, `paper_id`, `sourced_from` (comma list: `claims.json,forward_7q.json,reverse_7q.json,evidence_7q.json`) |
| `NODES` | one row per node | `run_id`, `node_id`, `node_type` (`paper`/`claim`/`axiom_candidate`/`evidence`/`equation`/`domain`/`objection`), `label` (≤500), `doc_id`, `evidence_class` (nullable: `direct`/`indirect`/`analogical`/`weak`/`conflicting`), `source_station_id` (where this node came from), `confidence` (float, nullable) |
| `EDGES` | one row per edge | `run_id`, `edge_id`, `source_node_id`, `target_node_id`, `edge_type` (`supports`/`contradicts`/`depends_on`/`derives_from`/`maps_to`/`cites`), `weight` (float, default 1.0), `provenance` (source artifact path) |
| `NODE_TYPE_STATS` | per-run histogram | `run_id`, `node_type`, `count` |
| `EDGE_TYPE_STATS` | per-run histogram | `run_id`, `edge_type`, `count` |
| `ORPHANS` | nodes with no edges | `run_id`, `node_id`, `node_type`, `label` |

### Mirrors JSON/MD/CSV

- JSON: `graph.json` → `RUNS` + `NODES` + `EDGES`
- CSV: `nodes.csv`, `edges.csv` → identical content to `NODES` + `EDGES` (Excel adds run-scoping)
- MD: `graph.md` (summary) → `NODE_TYPE_STATS` + `EDGE_TYPE_STATS`

---

## 7. PUB lane (2 stations)

**Stations:** `ST-PUB-001` publication_gate (rule-based readiness check + destination rec) · `ST-PUB-002` rubric_lsdp_formatter (LLM-backed rubric scoring + formatted output)

### 7.1 ST-PUB-001 publication_gate

**Workbook:** `publication_gate/output/publication_gate.xlsx`

| Sheet | Purpose | Columns |
|-------|---------|---------|
| `RUNS` | universal | (§1.4) + `destination`, `passed`, `total`, `pass_ratio`, `decided_at` |
| `DECISIONS` | one row per run | `run_id`, `doc_id`, `destination` (`website`/`substack`/`zenodo`/`proof_explorer`/`obsidian_canon`/`review`/`archive`), `rationale` (≤500), `confidence` (`high`/`medium`/`low`), `decided_at` |
| `CHECKS` | one row per (run, check) | `run_id`, `doc_id`, `check_name` (string), `passed` (bool), `details` (≤500) |
| `METRICS` | one row per (run, metric) | `run_id`, `doc_id`, `metric_name`, `value` (numeric or string), `unit`, `source_artifact` |
| `DEST_HIST` | aggregate destination distribution across runs | `destination`, `count`, `last_run_id`, `last_decided_at` |

### 7.2 ST-PUB-002 rubric_lsdp_formatter

**Workbook:** `rubric_lsdp_formatter/output/rubric_lsdp_formatter.xlsx`

| Sheet | Purpose | Columns |
|-------|---------|---------|
| `RUNS` | universal | (§1.4) + `rubric_version`, `total_score`, `max_score`, `pct_score` |
| `RUBRIC_SCORES` | one row per (run, rubric item) | `run_id`, `doc_id`, `rubric_item_id`, `rubric_item_label`, `score` (float), `max_score` (float), `weight` (float), `comment` (≤500) |
| `OUTPUT` | references to generated formatted text | `run_id`, `doc_id`, `formatted_text_path`, `format_kind` (`lsdp`/`theopoetic`/`raw`), `chars_in`, `chars_out` |
| `SUMMARY` | per-run | `run_id`, `doc_id`, `total_score`, `max_score`, `pct_score`, `weakest_item_id`, `strongest_item_id` |

### Mirrors JSON/MD

- ST-PUB-001 JSON: `publication_status.yml` → `RUNS` + `DECISIONS` + `CHECKS` + `METRICS`. MD: `release_recommendation.md` → `DECISIONS`.
- ST-PUB-002 JSON: `result.json` → `RUNS` + `RUBRIC_SCORES` + `OUTPUT`. MD: `result.md` → `SUMMARY`.

---

## 8. RED lane (1 station)

**Station:** `ST-RED-028` cross_output_contradiction (red-team: NLI between outputs of different stations on the same doc)

### Workbook: `cross_output_contradiction/output/cross_output_contradiction.xlsx`

| Sheet | Purpose | Columns |
|-------|---------|---------|
| `RUNS` | universal | (§1.4) + `n_outputs_scanned`, `n_pairs_checked`, `n_contradictions_found` |
| `OUTPUT_INVENTORY` | what was scanned this run | `run_id`, `doc_id`, `station_id`, `output_path`, `output_kind` (`claim`/`summary`/`forward_7q`/etc.), `n_claims_extracted`, `extracted_at` |
| `CONTRADICTIONS` | one row per detected contradiction between station outputs | `run_id`, `doc_id`, `contradiction_id`, `source_station_id`, `source_claim` (≤500), `source_claim_ref`, `target_station_id`, `target_claim` (≤500), `target_claim_ref`, `contradiction_score` (float), `severity` (`high`/`medium`/`low`), `requires_review` (bool) |
| `STATION_AGREEMENT_MATRIX` | pairwise agreement count for diagnostics | `run_id`, `station_a`, `station_b`, `pairs_compared`, `n_contradictions`, `n_agreements` |

### Mirrors JSON/MD

- JSON: `result.json` → `RUNS` + `OUTPUT_INVENTORY` + `CONTRADICTIONS` + `STATION_AGREEMENT_MATRIX`
- MD: `result.md` (top-N most severe) → `CONTRADICTIONS` filtered by `severity = high`

---

## 9. NLP lane (15 stations) — unified schema

**Stations:** `ST-NLP-001` semantic_drift · `ST-NLP-002` retention_pressure · `ST-NLP-003` tone_consistency · `ST-NLP-004` epistemic_integrity · `ST-NLP-005` compression_density · `ST-NLP-006` cognitive_load_gradient · `ST-NLP-007` narrative_momentum · `ST-NLP-008` bridge_density · `ST-NLP-009` redundancy_compression · `ST-NLP-010` dependency_stability · `ST-NLP-011` reader_projection · `ST-NLP-012` novelty_gradient · `ST-NLP-013` argument_closure · `ST-NLP-014` symbol_consistency · `ST-NLP-015` rhetorical_temperature

**All 15 share the same workbook schema** so a single pivot at the lane level shows every metric across every doc.

### Workbook: `<station_folder>/output/<short>.xlsx` (one per station)

| Sheet | Purpose | Columns |
|-------|---------|---------|
| `RUNS` | universal | (§1.4) + `metric_name` (= station's primary metric, e.g. `semantic_drift`), `score` (float, 0-1 normalized), `score_raw` (float, native scale), `score_label` (`low`/`medium`/`high`/`critical`) |
| `SCORES` | one row per run — the canonical lane-joinable row | `run_id`, `station_id`, `doc_id`, `metric_name`, `score`, `score_raw`, `score_label`, `computed_at` |
| `DETAILS` | per-span / per-segment detail (station-specific sub-metrics) | `run_id`, `doc_id`, `segment_id` (`SEG-NNN`), `span_start` (int), `span_end` (int), `evidence_text` (≤500), `sub_metric_name`, `sub_metric_value` (numeric or string) |
| `DOC_STATS` | latest score per doc | `doc_id`, `station_id`, `latest_run_id`, `latest_score`, `latest_label`, `n_runs`, `first_run_id`, `last_computed_at` |

**Why the unified schema:** `SCORES` rows from any of the 15 NLP workbooks UNION cleanly into a single table keyed by `(doc_id, station_id)` — perfect for a per-doc dashboard showing all 15 metrics side by side.

### Mirrors JSON/MD

- JSON: `result.json` → `{station, doc_id, metric_name, score, score_raw, label, details: [...]}` → `RUNS` + `SCORES` + `DETAILS`
- MD: `result.md` (top issues + interpretation) → `DETAILS` filtered by significance + `DOC_STATS`

### Per-station `sub_metric_name` vocabulary (DETAILS sheet)

| Station                       | Expected `sub_metric_name` values                            |
|-------------------------------|--------------------------------------------------------------|
| `ST-NLP-001` semantic_drift   | `drift_delta`, `drift_window`, `cosine_drop`                  |
| `ST-NLP-002` retention_pressure | `working_memory_load`, `reference_distance`, `pronoun_chain_length` |
| `ST-NLP-003` tone_consistency | `tone_variance`, `register_shift`, `formality_delta`          |
| `ST-NLP-004` epistemic_integrity | `hedging_count`, `unsupported_claim`, `overclaim_count`     |
| `ST-NLP-005` compression_density | `lz_ratio`, `entropy_per_char`, `tokens_per_concept`        |
| `ST-NLP-006` cognitive_load_gradient | `parse_depth`, `flesch_kincaid`, `concept_density`     |
| `ST-NLP-007` narrative_momentum | `tension_arc_position`, `pace_per_paragraph`, `stall_count` |
| `ST-NLP-008` bridge_density   | `inter_section_bridges`, `transition_strength`, `missing_bridge` |
| `ST-NLP-009` redundancy_compression | `dup_ngram`, `paraphrase_pair`, `redundancy_score`     |
| `ST-NLP-010` dependency_stability | `forward_ref`, `dangling_ref`, `circular_dep`            |
| `ST-NLP-011` reader_projection | `assumed_knowledge`, `audience_drift`, `register_mismatch`  |
| `ST-NLP-012` novelty_gradient | `novelty_score`, `prior_overlap_pct`, `new_concept_count`     |
| `ST-NLP-013` argument_closure | `unclosed_premise`, `dangling_conclusion`, `closure_score`    |
| `ST-NLP-014` symbol_consistency | `symbol`, `first_def`, `inconsistent_use`, `undefined_use`  |
| `ST-NLP-015` rhetorical_temperature | `heat_score`, `polarity_shift`, `intensity_spike`       |

---

## 10. Station → Workbook mapping (full)

| station_id      | folder                          | workbook (relative to BACKSIDE)                                                          | sheets                                          | mirrors                          |
|-----------------|----------------------------------|-------------------------------------------------------------------------------------------|-------------------------------------------------|----------------------------------|
| ST-NLI-001      | nli_strong                      | `STATIONS/stations/nli_strong/output/nli_strong.xlsx`                                     | RUNS, PAIRS, SUMMARY, LABEL_HIST                | result.json, result.md           |
| ST-NLI-002      | nli_claim                       | `STATIONS/stations/nli_claim/output/nli_claim.xlsx`                                       | RUNS, PAIRS, SUMMARY, LABEL_HIST                | result.json, result.md           |
| ST-NLI-003      | nli_alt                         | `STATIONS/stations/nli_alt/output/nli_alt.xlsx`                                           | RUNS, PAIRS, SUMMARY, LABEL_HIST                | result.json, result.md           |
| ST-NLI-004      | nli_base                        | `STATIONS/stations/nli_base/output/nli_base.xlsx`                                         | RUNS, PAIRS, SUMMARY, LABEL_HIST                | result.json, result.md           |
| ST-NLI-005      | contradiction_scan              | `STATIONS/stations/contradiction_scan/output/contradiction_scan.xlsx`                     | RUNS, PAIRS, SUMMARY, LABEL_HIST, CLAIMS, CONTRADICTIONS | result.json, result.md  |
| ST-EMBED-001    | sci_embed                       | `STATIONS/stations/sci_embed/output/sci_embed.xlsx`                                       | RUNS, SENTENCES, DOCS, SIM_SAMPLES              | result.json, result.md, *.npy    |
| ST-EMBED-002    | embed_general                   | `STATIONS/stations/embed_general/output/embed_general.xlsx`                               | RUNS, SENTENCES, DOCS, SIM_SAMPLES              | result.json, result.md, *.npy    |
| ST-RERANK-001   | rerank                          | `STATIONS/stations/rerank/output/rerank.xlsx`                                             | RUNS, QUERIES, RANKED, SUMMARY                  | result.json, result.md           |
| ST-TIME-001     | timeline                        | `STATIONS/stations/timeline/output/timeline.xlsx`                                         | RUNS, EVENTS, DOC_STATS, STUB_NOTES             | result.json, result.md (stub)    |
| ST-GRAPH-001    | knowledge_graph                 | `STATIONS/stations/knowledge_graph/output/knowledge_graph.xlsx`                           | RUNS, NODES, EDGES, NODE_TYPE_STATS, EDGE_TYPE_STATS, ORPHANS | graph.json, graph.md, nodes.csv, edges.csv |
| ST-GRAPH-018    | knowledge_graph_extractor       | `STATIONS/stations/knowledge_graph_extractor/output/knowledge_graph_extractor.xlsx`       | RUNS, NODES, EDGES, NODE_TYPE_STATS, EDGE_TYPE_STATS, ORPHANS | result.json, result.md  |
| ST-PUB-001      | publication_gate                | `STATIONS/stations/publication_gate/output/publication_gate.xlsx`                         | RUNS, DECISIONS, CHECKS, METRICS, DEST_HIST     | publication_status.yml, release_recommendation.md |
| ST-PUB-002      | rubric_lsdp_formatter           | `STATIONS/stations/rubric_lsdp_formatter/output/rubric_lsdp_formatter.xlsx`               | RUNS, RUBRIC_SCORES, OUTPUT, SUMMARY            | result.json, result.md           |
| ST-RED-028      | cross_output_contradiction      | `STATIONS/stations/cross_output_contradiction/output/cross_output_contradiction.xlsx`     | RUNS, OUTPUT_INVENTORY, CONTRADICTIONS, STATION_AGREEMENT_MATRIX | result.json, result.md |
| ST-NLP-001      | semantic_drift                  | `STATIONS/stations/semantic_drift/output/semantic_drift.xlsx`                             | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-002      | retention_pressure              | `STATIONS/stations/retention_pressure/output/retention_pressure.xlsx`                     | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-003      | tone_consistency                | `STATIONS/stations/tone_consistency/output/tone_consistency.xlsx`                         | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-004      | epistemic_integrity             | `STATIONS/stations/epistemic_integrity/output/epistemic_integrity.xlsx`                   | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-005      | compression_density             | `STATIONS/stations/compression_density/output/compression_density.xlsx`                   | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-006      | cognitive_load_gradient         | `STATIONS/stations/cognitive_load_gradient/output/cognitive_load_gradient.xlsx`           | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-007      | narrative_momentum              | `STATIONS/stations/narrative_momentum/output/narrative_momentum.xlsx`                     | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-008      | bridge_density                  | `STATIONS/stations/bridge_density/output/bridge_density.xlsx`                             | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-009      | redundancy_compression          | `STATIONS/stations/redundancy_compression/output/redundancy_compression.xlsx`             | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-010      | dependency_stability            | `STATIONS/stations/dependency_stability/output/dependency_stability.xlsx`                 | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-011      | reader_projection               | `STATIONS/stations/reader_projection/output/reader_projection.xlsx`                       | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-012      | novelty_gradient                | `STATIONS/stations/novelty_gradient/output/novelty_gradient.xlsx`                         | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-013      | argument_closure                | `STATIONS/stations/argument_closure/output/argument_closure.xlsx`                         | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-014      | symbol_consistency              | `STATIONS/stations/symbol_consistency/output/symbol_consistency.xlsx`                     | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |
| ST-NLP-015      | rhetorical_temperature          | `STATIONS/stations/rhetorical_temperature/output/rhetorical_temperature.xlsx`             | RUNS, SCORES, DETAILS, DOC_STATS                | result.json, result.md           |

**29 stations · 29 workbooks · stable lane schemas · all keys join cross-lane on `run_id`, `doc_id`, `station_id`, `claim_id`.**

---

## 11. Optional per-lane dashboards (for later)

Not in scope to build now, but the schemas above support these natively:

| Dashboard                          | Path                                          | Pivot |
|------------------------------------|------------------------------------------------|-------|
| `STATIONS/_dashboards/lane_nlp.xlsx` | union all 15 NLP `SCORES` sheets             | `doc_id` × `station_id` → `score`; conditional formatting by `score_label` |
| `STATIONS/_dashboards/lane_nli.xlsx` | union all 5 NLI `SUMMARY` sheets             | `run_id` × `station_id` → `pct_contradiction` |
| `STATIONS/_dashboards/lane_graph.xlsx` | union both GRAPH `NODE_TYPE_STATS` + `EDGE_TYPE_STATS` | `doc_id` × `node_type` → `count` |
| `STATIONS/_dashboards/master.xlsx`   | per-doc rollup — every station's latest result | `doc_id` × `station_id` → `latest_score` / `latest_label` / `latest_decision` |

A future `_tools/dashboard_rebuilder.py` would read every per-station workbook and rewrite the dashboards in place.

---

*End of spec. Owned by claude-code. 29 stations. Schemas designed for cross-station join via `run_id`, `doc_id`, `station_id`, `claim_id`, `axiom_id`. No code in this deliverable — implementation goes in each station's `scripts/run.py` (`xlsx_path = output_dir / "<short>.xlsx"`; use `openpyxl` for append-row pattern).*
