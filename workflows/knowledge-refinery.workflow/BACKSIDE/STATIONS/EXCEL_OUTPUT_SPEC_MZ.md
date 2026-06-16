# Excel Output Spec (M–Z side): NLP + Substrate + Graph/Publish

Scope lanes: nlp, nli, embed, rerank, time, graph, pub, red

## Contract (joinable IDs)

- `run_id` (string): `YYYYMMDD-HHMMSSZ.<station_id>.<hash8>`
- `station_id` (string): from station.yml (e.g. `ST-NLP-004`)
- `doc_id` (string): stable source doc ID (if unknown, use `sha256:<hash>` of normalized source text)
- `source_path` (string): input filepath the station ran on
- `artifact_path` (string): primary JSON artifact written by station

## Where workbooks land

Write workbooks under the station folder so the station is self-contained:

`X:\knowledge-refinery\BACKSIDE\STATIONS\stations\<station_folder>\excel\<station_folder>.xlsx`

Each station owns exactly 1 workbook. Sheets below.

---

# Lane: embed

## Station: `sci_embed` (ST-EMBED-001)
Workbook: `sci_embed.xlsx`
- Sheet `runs`: run_id, station_id, started_utc, finished_utc, input_kind, source_path, doc_id, model_id, status, error
- Sheet `embeddings`: run_id, doc_id, chunk_id, text_sha256, embedding_dim, embedding_provider, embedding_model, embedding_b64_or_path
- Sheet `neighbors` (optional): run_id, doc_id, neighbor_doc_id, score_cosine, note

## Station: `embed_general` (ST-EMBED-002)
Workbook: `embed_general.xlsx`
- Sheet `runs`: same as above
- Sheet `embeddings`: same as above

---

# Lane: rerank

## Station: `rerank` (ST-RERANK-001)
Workbook: `rerank.xlsx`
- Sheet `runs`: run_id, station_id, started_utc, finished_utc, source_path, doc_id, model_id, status, error
- Sheet `pairs_scored`: run_id, doc_id, left_id, right_id, left_text_sha256, right_text_sha256, score, label, threshold, decision

---

# Lane: nli

## Station: `nli_strong` (ST-NLI-001)
Workbook: `nli_strong.xlsx`
- Sheet `runs`: run_id, station_id, started_utc, finished_utc, source_path, doc_id, model_id, status, error
- Sheet `pairs`: run_id, doc_id, premise_id, hypothesis_id, premise_sha256, hypothesis_sha256
- Sheet `predictions`: run_id, doc_id, premise_id, hypothesis_id, label, score_entail, score_neutral, score_contra, decision

## Station: `nli_claim` (ST-NLI-002)
Workbook: `nli_claim.xlsx`
- Sheets: same as `nli_strong`

## Station: `nli_alt` (ST-NLI-003)
Workbook: `nli_alt.xlsx`
- Sheets: same as `nli_strong`

## Station: `nli_base` (ST-NLI-004)
Workbook: `nli_base.xlsx`
- Sheets: same as `nli_strong`

---

# Lane: time

## Station: `timeline` (ST-TIME-001)
Workbook: `timeline.xlsx`
- Sheet `runs`: run_id, station_id, started_utc, finished_utc, source_path, doc_id, model_id, status, error
- Sheet `events`: run_id, doc_id, event_id, text_span_sha256, start_char, end_char, time_text, time_iso, granularity, confidence
- Sheet `anchors`: run_id, doc_id, anchor_id, anchor_type, anchor_value, note

---

# Lane: nlp (paper psychometrics layer)

Common sheet set for each NLP metric station:
- Sheet `runs`: run_id, station_id, started_utc, finished_utc, source_path, doc_id, status, error
- Sheet `scores`: run_id, doc_id, metric_name, score_0_1, band, rationale_short
- Sheet `findings`: run_id, doc_id, finding_id, finding_type, severity, section_hint, char_start, char_end, snippet_sha256, note

Apply the above to each station below (1 workbook per station, named after folder):
- `semantic_drift.xlsx`
- `retention_pressure.xlsx`
- `tone_consistency.xlsx`
- `epistemic_integrity.xlsx`
- `compression_density.xlsx`
- `cognitive_load_gradient.xlsx`
- `narrative_momentum.xlsx`
- `bridge_density.xlsx`
- `redundancy_compression.xlsx`
- `dependency_stability.xlsx`
- `reader_projection.xlsx`
- `novelty_gradient.xlsx`
- `argument_closure.xlsx`
- `symbol_consistency.xlsx`
- `rhetorical_temperature.xlsx`

---

# Lane: graph

## Station: `knowledge_graph` (ST-GRAPH-001)
Workbook: `knowledge_graph.xlsx`
- Sheet `runs`: run_id, station_id, started_utc, finished_utc, source_path, doc_id, status, error
- Sheet `nodes`: run_id, doc_id, node_id, node_type, label, text_sha256, lane, status
- Sheet `edges`: run_id, doc_id, edge_id, from_node_id, to_node_id, edge_type, weight, note
- Sheet `collapse_map` (optional): run_id, doc_id, trigger_id, affected_node_id, reason

## Station: `knowledge_graph_extractor` (if present as separate graph station)
Workbook: `knowledge_graph_extractor.xlsx`
- Sheets: same as above

---

# Lane: pub

## Station: `publication_gate` (ST-PUB-001)
Workbook: `publication_gate.xlsx`
- Sheet `runs`: run_id, station_id, started_utc, finished_utc, source_path, doc_id, status, error
- Sheet `gates`: run_id, doc_id, gate_id, gate_name, pass_bool, severity, reason, fix_hint
- Sheet `targets`: run_id, doc_id, target_kind, target_path, release_tier, hold_reason

---

# Lane: red

## Station: `cross_output_contradiction` (ST-RED-001)
Workbook: `cross_output_contradiction.xlsx`
- Sheet `runs`: run_id, station_id, started_utc, finished_utc, source_path, doc_id, status, error
- Sheet `contradictions`: run_id, doc_id, contradiction_id, left_artifact, right_artifact, claim_id, nli_label, nli_score, severity, note
- Sheet `weak_links`: run_id, doc_id, weak_link_id, claim_id, failure_mode, severity, note

---

## Next implementation move (tomorrow)

- Add a tiny shared helper `excel_writer.py` (openpyxl) in `_tools/` and import it from each station runner to emit these workbooks.
- Do NOT block station completion on Excel; emit Excel as a mirror of existing JSON/MD artifacts.
