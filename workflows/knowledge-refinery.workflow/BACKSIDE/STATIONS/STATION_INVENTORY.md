# Station Inventory

*Snapshot 2026-05-16 post-migration. For the live count and per-station detail, run `python registry_rebuilder.py` and read `stations_registry.yml`.*

Canonical location: `X:\knowledge-refinery\BACKSIDE\STATIONS\`

## Counts

| Total stations | 54 |
|----------------|----|
| Lanes          | 17 |

| Lane    | Count | What                                            |
|---------|-------|--------------------------------------------------|
| `conv`  | 16    | Format converters (md, pdf, html, docx, audio, video, etc.) |
| `nlp`   | 15    | Content-analysis (semantic_drift, tone, density, etc.) |
| `nli`   | 4     | Natural language inference (substrate)           |
| `sevenq`| 3     | 7-Question pipeline (forward/reverse/evidence)   |
| `embed` | 2     | Embedding wrappers (SPECTER2, MiniLM)            |
| `graph` | 2     | Knowledge graph builders                          |
| `7qs`   | 2     | Legacy lane (drift — same role as `sevenq`; resolve later) |
| `route` | 1     | File-type routing                                 |
| `claim` | 1     | Claim extraction                                  |
| `sum`   | 1     | Lossless summary                                  |
| `pub`   | 1     | Publication gate                                  |
| `rerank`| 1     | Cross-encoder reranker                            |
| `time`  | 1     | Temporal extraction                               |
| `cite`  | 1     | (other AI's lane)                                 |
| `code`  | 1     | (other AI's lane)                                 |
| `lctx`  | 1     | (other AI's lane)                                 |
| `red`   | 1     | (other AI's lane)                                 |

## Naming conventions (in force as of 2026-05-16)

| Thing       | Format                  | Example                |
|-------------|--------------------------|------------------------|
| Folder      | `snake_case_role`        | `route_classifier`     |
| Station id  | `ST-LANE-NNN` (per-lane) | `ST-SEVENQ-001`        |
| Runner      | `scripts/run.py`         | called by template's `03_run_prompt.bat` |
| Sample input| `input/sample_input.md`  |                        |
| Sort order  | `order:` field in `station.yml` | not strict, just a hint |

**No folder number prefixes** — dropped 2026-05-16 after they caused collisions when multiple AIs scaffolded in parallel.

## Spine — refinery pipeline (9 stations)

Executes in this order:

| # | Station ID      | Folder                | Runner status | Notes |
|---|-----------------|-----------------------|---------------|-------|
| 1 | ST-ROUTE-001    | route_classifier      | wired         | extension → file_type → lane dispatch |
| 2 | ST-CONV-001     | document_converter    | wired         | dispatches to MarkItDown/Docling/Marker |
| 3 | ST-CLAIM-001    | claim_extractor       | wired         | LLM (gpt-4o-mini), claims+gradient labels |
| 4 | ST-SUM-001      | lossless_summary      | wired         | LLM, preserves argument arc + claims + gaps |
| 5 | ST-SEVENQ-001   | 7q_forward            | wired         | extracted from `seven_q_runner.py` |
| 6 | ST-SEVENQ-002   | 7q_reverse            | wired         | takes optional `--forward` for context |
| 7 | ST-SEVENQ-003   | 7q_evidence           | wired         | evidence classes + gaps + citation targets |
| 8 | ST-GRAPH-001    | knowledge_graph       | wired         | builds nodes+edges + nodes.csv/edges.csv |
| 9 | ST-PUB-001      | publication_gate      | wired         | rule-based readiness check + destination rec |

## Substrate — model wrappers (8 stations)

| Station ID      | Folder           | Wraps                            | Runner status |
|-----------------|------------------|----------------------------------|---------------|
| ST-EMBED-001    | sci_embed        | M-EMB-SCI-001 (SPECTER2)         | wired |
| ST-EMBED-002    | embed_general    | M-EMB-GEN-001 (MiniLM)           | wired |
| ST-NLI-001      | nli_strong       | M-NLI-STRONG-001 (DeBERTa lg)    | NOT wired (low priority — copy from rerank) |
| ST-NLI-002      | nli_claim        | M-NLI-CLAIM-001 (MNLI/FEVER/ANLI)| NOT wired |
| ST-NLI-003      | nli_alt          | M-NLI-ALT-001 (RoBERTa lg)       | NOT wired |
| ST-NLI-004      | nli_base         | M-NLI-BASE-001 (legacy)          | NOT wired |
| ST-RERANK-001   | rerank           | M-RERANK-001 (cross-encoder)     | wired |
| ST-TIME-001     | timeline         | M-TIME-001                        | stub — awaiting recipe |

## Other families (38 stations)

Other workers have been scaffolding additional families in parallel. These are NOT my work — I haven't verified their runner status:

- **Format converters (conv lane, 16 stations):** html_to_md, pdf_to_md, docx_to_md, pptx_to_md, audio_to_txt, video_to_txt, youtube_to_txt, md_cleaner, md_to_plaintext, markitdown_converter, marker_pdf_converter, equation_extract, table_extract, image_extract, ocr_scan, frontmatter_builder, asset_packager, etc.
- **Content analysis (nlp lane, 15 stations):** semantic_drift, retention_pressure, tone_consistency, epistemic_integrity, compression_density, cognitive_load_gradient, narrative_momentum, bridge_density, redundancy_compression, dependency_stability, reader_projection, novelty_gradient, argument_closure, symbol_consistency, rhetorical_temperature, etc.
- **Stragglers (one-off lanes):** code, lctx, cite, red — likely owned by other AIs; check their station.yml.

Use `python registry_rebuilder.py` to get the current authoritative list. The registry sorts by lane then ID.

## Open issues

1. **`7qs` vs `sevenq` lane drift.** Two stations still use the legacy `7qs` lane code; my migration moved my 3 stations to `sevenq`. Pick one and unify — flag to whoever owns those 2 stations.
2. **Folder-number `order:` collisions.** Multiple stations share an `order:` value (e.g. three with `order: 12`). That's fine for now (order is a hint, not strict), but if you need a stable display sort, disambiguate by lane.
3. **NLI substrate runners missing.** 4 of 8 substrate runners aren't written. Copy `rerank/scripts/run.py`, swap the model path + label decoder.
4. **Stragglers not registered.** Some folders without `station.yml` are skipped by the rebuilder. They won't be callable from a workflow until they're filled in.

## How to add a new station

```cmd
new_station.bat name --lane LANE --model M-XXX --purpose "..." --status draft
python registry_rebuilder.py
```

Folder name = role. ID = auto-derived per-lane. Order = auto-incremented. No number prefix.
