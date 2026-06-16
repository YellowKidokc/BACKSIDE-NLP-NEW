# Excel Output Plan — lanes: route, conv, claim, sum, sevenq

*Spec only. No code. 22 stations covered.*
*Author: claude-code-forge · 2026-05-16*

---

## Design principles

**1. Stable joinable keys.** Every workbook in every lane has these columns wherever applicable, so cross-station joins work without remapping:

| Key | Type | Meaning |
|---|---|---|
| `run_id` | uuid | one pipeline invocation (set by workflow tier, propagates) |
| `doc_id` | `sha256(source_bytes)[:16]` | stable across re-runs of the same source |
| `source_path` | text | original file location (audit only — never join on this) |
| `station_id` | text | `ST-LANE-NNN` |
| `station_run_id` | uuid | one execution of this station (one per row in `runs` sheet) |
| `ts_utc` | iso-8601 | when the row was written |
| `status` | enum | `pass` \| `fail` \| `review` \| `error` |
| `claim_id` | `sha1(doc_id + claim_text)[:16]` | stable across CLAIM → SUM → SEVENQ |

**2. Two-sheet floor.** Every workbook has at minimum `runs` (one row per station execution) and `errors` (one row per error, may be empty). Lane-specific detail sheets sit alongside.

**3. Per-station workbook + per-lane rollup.** The station writes its own `output/workbook.xlsx`. A separate `xlsx_rebuilder.py` (out of scope for this spec) concatenates per-station workbooks into per-lane and master rollups at `X:\knowledge-refinery\BACKSIDE\exports\workbooks\`.

**4. Mirrors, not replacements.** Each workbook MIRRORS the station's existing JSON/MD outputs. JSON stays the machine truth; XLSX is the human/analyst surface.

**5. xlsxwriter, not openpyxl.** Already installed via MarkItDown deps. Faster. Single-pass writer. No formula evaluation.

---

## Station → workbook mapping (22 stations)

| Station ID | Folder | Workbook (in `<folder>/output/`) | Sheets | Mirrors |
|---|---|---|---|---|
| ST-ROUTE-001 | `route_classifier` | `route_classifier.xlsx` | runs, decisions, errors | `routing.yml`, `routing.md` |
| ST-CONV-001 | `document_converter` | `conv__dispatcher.xlsx` | runs, routing_decisions, errors | `conversion_report.yml`, `source.md` |
| ST-CONV-012 | `html_to_md` | `conv__html_to_md.xlsx` | runs, errors | `result.json`, `result.md` |
| ST-CONV-013 | `pdf_to_md` | `conv__pdf_to_md.xlsx` | runs, pages, errors | `result.json`, `result.md` |
| ST-CONV-014 | `docx_to_md` | `conv__docx_to_md.xlsx` | runs, errors | `result.json`, `result.md` |
| ST-CONV-015 | `pptx_to_md` | `conv__pptx_to_md.xlsx` | runs, slides, errors | `result.json`, `result.md` |
| ST-CONV-016 | `audio_to_txt` | `conv__audio_to_txt.xlsx` | runs, segments, errors | `result.json`, `result.md` |
| ST-CONV-017 | `video_to_txt` | `conv__video_to_txt.xlsx` | runs, segments, errors | `result.json`, `result.md` |
| ST-CONV-018 | `youtube_to_txt` | `conv__youtube_to_txt.xlsx` | runs, segments, errors | `result.json`, `result.md` |
| ST-CONV-019 | `md_cleaner` | `conv__md_cleaner.xlsx` | runs, changes, errors | `result.json`, `result.md` |
| ST-CONV-020 | `md_to_plaintext` | `conv__md_to_plaintext.xlsx` | runs, errors | `result.json`, `result.md` |
| ST-CONV-021 | `equation_extract` | `conv__equation_extract.xlsx` | runs, equations, errors | `result.json`, `result.md` |
| ST-CONV-022 | `table_extract` | `conv__table_extract.xlsx` | runs, tables, errors | `result.json`, `result.md` |
| ST-CONV-023 | `image_extract` | `conv__image_extract.xlsx` | runs, images, errors | `result.json`, `result.md` |
| ST-CONV-024 | `ocr_scan` | `conv__ocr_scan.xlsx` | runs, pages, ocr_quality, errors | `result.json`, `result.md` |
| ST-CONV-025 | `frontmatter_builder` | `conv__frontmatter.xlsx` | runs, frontmatter, errors | `result.json`, `result.md` |
| ST-CONV-026 | `asset_packager` | `conv__asset_packager.xlsx` | runs, assets, link_rewrites, errors | `result.json`, `result.md` |
| ST-CLAIM-001 | `claim_extractor` | `claim__extractor.xlsx` | runs, claims, errors | `claims.json`, `claims.md` |
| ST-SUM-001 | `lossless_summary` | `sum__lossless.xlsx` | runs, summary_sections, claim_refs, gap_flags, errors | `summary.lossless.json`, `summary.lossless.md` |
| ST-SEVENQ-001 | `7q_forward` | `sevenq__forward.xlsx` | runs, answers, errors | `forward_7q.json`, `forward_7q.md` |
| ST-SEVENQ-002 | `7q_reverse` | `sevenq__reverse.xlsx` | runs, answers, errors | `reverse_7q.json`, `reverse_7q.md` |
| ST-SEVENQ-003 | `7q_evidence` | `sevenq__evidence.xlsx` | runs, evidence_items, citation_targets, errors | `evidence_7q.json`, `evidence_7q.md` |

**Workbook write path (exact):** `X:\knowledge-refinery\BACKSIDE\STATIONS\stations\<folder>\output\<workbook>.xlsx`

**Aggregate rollups path:** `X:\knowledge-refinery\BACKSIDE\exports\workbooks\` (built later by `xlsx_rebuilder.py`)

---

## Common sheet schemas

### `runs` (universal — every workbook)

```
run_id | doc_id | source_path | station_id | station_run_id | ts_utc | status |
input_path | input_sha256 | output_paths | duration_ms | error_code | notes
```

Primary key: `station_run_id`. Joinable to other lanes on `run_id` and `doc_id`.

### `errors` (universal — every workbook, may be empty)

```
station_run_id | error_code | error_msg | error_class | stack_trace_path | retry_count | ts_utc
```

Primary key: `(station_run_id, error_code)`. Joinable to `runs`.

---

## Per-lane detail schemas

### ROUTE — 1 station

**ST-ROUTE-001 `route_classifier` — `route_classifier.xlsx`**

`decisions` sheet:
```
station_run_id | doc_id | source_path | file_ext | mime_type | magika_label |
magika_confidence | target_lane | target_station_id | fallback_station_id | reason
```
Primary key: `(station_run_id, doc_id)`.

### CONV — 17 stations

All CONV stations share the universal `runs` + `errors`. The `runs` sheet in CONV adds these columns:

```
... universal ... | backend_used | backend_version | conversion_tool |
char_count | word_count | confidence | source_byte_size
```

`backend_used` values: `markitdown` | `docling` | `marker` | `faster_whisper` | `yt_dlp` | `markdown_it_py` | `strip_markdown` | `python_stdlib` | `ffmpeg`.

Lane-specific detail sheets:

**ST-CONV-001 `document_converter` (dispatcher)** — `routing_decisions` sheet:
```
station_run_id | doc_id | file_ext | magika_label | picked_station_id |
fallback_station_id | reason
```

**ST-CONV-013 `pdf_to_md` + ST-CONV-024 `ocr_scan`** — `pages` sheet:
```
station_run_id | doc_id | page_number | char_count | has_tables |
has_equations | has_images | layout_confidence
```

**ST-CONV-024 `ocr_scan`** also gets `ocr_quality` sheet:
```
station_run_id | doc_id | page_number | avg_word_confidence |
low_conf_word_count | requires_review
```

**ST-CONV-015 `pptx_to_md`** — `slides` sheet:
```
station_run_id | doc_id | slide_number | slide_title | char_count | note_count
```

**ST-CONV-016/017/018 `audio/video/youtube_to_txt`** — `segments` sheet:
```
station_run_id | doc_id | segment_index | start_sec | end_sec | text |
avg_logprob | no_speech_prob | language | requires_review
```
`requires_review = true` when `no_speech_prob > 0.6` or `avg_logprob < -1.0` (Whisper hallucination guard).

`youtube_to_txt.runs` additionally carries: `video_url, video_id, channel, title, duration_sec, view_count`.

**ST-CONV-019 `md_cleaner`** — `changes` sheet:
```
station_run_id | doc_id | change_type | count_before | count_after | notes
```
`change_type` values: `heading_normalize` | `dedupe_header` | `nav_strip` | `link_repair` | `footnote_renumber` | `whitespace_collapse`.

**ST-CONV-021 `equation_extract`** — `equations` sheet:
```
station_run_id | doc_id | equation_id | page_or_section | latex | mathml | char_count
```
`equation_id = sha1(doc_id + latex)[:12]`.

**ST-CONV-022 `table_extract`** — `tables` sheet:
```
station_run_id | doc_id | table_id | page_or_section | row_count | col_count |
csv_path | md_path | caption
```
`table_id = sha1(doc_id + page_or_section + csv_path)[:12]`.

**ST-CONV-023 `image_extract`** — `images` sheet:
```
station_run_id | doc_id | image_id | asset_path | page_or_section | width |
height | format | alt_text | byte_size
```
`image_id = sha1(doc_id + asset_path)[:12]`.

**ST-CONV-025 `frontmatter_builder`** — `frontmatter` sheet:
```
station_run_id | doc_id | source_type | source_path | sha256 | conversion_tool |
converted_at_utc | language | word_count | lineage_chain | custom_fields_json
```

**ST-CONV-026 `asset_packager`** — `assets` + `link_rewrites` sheets:
```
assets: station_run_id | doc_id | asset_id | asset_type | original_path |
        canonical_path | sha256 | byte_size
link_rewrites: station_run_id | doc_id | original_link | rewritten_link |
        link_type
```

### CLAIM — 1 station

**ST-CLAIM-001 `claim_extractor` — `claim__extractor.xlsx`**

`runs` adds: `model_used | total_claims_extracted | total_input_tokens | total_output_tokens | cost_estimate_usd | source_word_count`.

`claims` sheet — **central join table for downstream lanes**:
```
station_run_id | doc_id | claim_id | claim_text | gradient_label | section_or_anchor |
evidence_required | source_offset_start | source_offset_end | confidence | claim_index
```
`gradient_label` enum: `load-bearing` | `suggestive` | `overclaimed` (per the contract).
`claim_id` is the canonical identifier referenced by SUM and SEVENQ.

### SUM — 1 station

**ST-SUM-001 `lossless_summary` — `sum__lossless.xlsx`**

`runs` adds: `model_used | input_chars | output_chars | retention_ratio | gap_count | claim_ref_count`.

`summary_sections` sheet:
```
station_run_id | doc_id | section_index | section_title | summary_text | source_anchor
```

`claim_refs` sheet — joins to CLAIM:
```
station_run_id | doc_id | claim_id | preserved | rephrased_text
```

`gap_flags` sheet:
```
station_run_id | doc_id | gap_type | description | source_anchor | severity
```
`gap_type` enum: `unsupported_claim` | `missing_definition` | `broken_arc` | `dangling_reference`.

### SEVENQ — 3 stations

**ST-SEVENQ-001 `7q_forward`, ST-SEVENQ-002 `7q_reverse` — both `sevenq__{forward,reverse}.xlsx`**

`runs` adds: `model_used | q0_score | q1_score | q2_score | q3_score | q4_score | q5_score | q6_score | q7_score | total_score | pass_threshold | passed`.

`answers` sheet:
```
station_run_id | doc_id | question_num | question_text | answer_text | score |
evidence_anchor | confidence
```
`question_num` 0..7 (Q0 = humility/surrender per the contract).

**ST-SEVENQ-003 `7q_evidence` — `sevenq__evidence.xlsx`**

`evidence_items` sheet — joins to CLAIM via `claim_id`:
```
station_run_id | doc_id | evidence_id | evidence_class | claim_id | citation_target_id |
strength | notes
```
`evidence_class` enum: `direct` | `corroborating` | `circumstantial` | `absent`.

`citation_targets` sheet:
```
station_run_id | doc_id | citation_target_id | target_text | target_url | target_type
```
`target_type` enum: `paper` | `book` | `dataset` | `experiment` | `scripture` | `web`.

---

## Aggregate rollups (built later by `xlsx_rebuilder.py`)

Path: `X:\knowledge-refinery\BACKSIDE\exports\workbooks\`

| Rollup | Source | Join keys | Purpose |
|---|---|---|---|
| `_master_runs.xlsx` | every station's `runs` sheet | `run_id, doc_id` | "what happened to doc X across all stations" |
| `_master_errors.xlsx` | every station's `errors` sheet | `station_run_id` | error triage across the pipeline |
| `_master_claims.xlsx` | CLAIM.claims + SUM.claim_refs + SEVENQ.evidence_items | `claim_id` | claim provenance — extracted → summarized → evidenced |
| `_master_route.xlsx` | ROUTE.decisions + CONV-001.routing_decisions | `doc_id` | routing audit (2 hops: lane pick, then within-lane station pick) |
| `_master_conv_quality.xlsx` | CONV.runs filtered to `requires_review = true` + OCR low_confidence + Whisper hallucination flags | `doc_id` | "what needs human review before the refinery sees it" |

---

## Open items (deferred — not blocking station wiring)

1. **xlsx_rebuilder.py** — concatenator for per-station → per-lane → master rollups. Same write protocol as `registry_rebuilder.py` (lock + atomic tmp+replace).
2. **Append-vs-rewrite strategy.** At 14k pages, each station may have N runs per doc over time. Decision: each station's workbook is APPEND-ONLY for `runs`; the `*_latest` view is a separate sheet sorted by `ts_utc desc`, deduped on `(doc_id, station_id)`. Keep both — analyst wants history + latest snapshot.
3. **Cell type discipline.** Force `ts_utc` as ISO string (not Excel date) to avoid timezone breakage. Force `*_id` columns as text (not number) so leading zeros and hex hashes survive.
4. **Size cap per workbook.** xlsxwriter handles ~1M rows per sheet. At 14k docs × N runs, plan to rotate `runs` sheets at 500k rows: `runs`, `runs_002`, `runs_003`. Master rollups will need that from day one.
5. **No formulas, no charts.** Workbooks are data drops, not dashboards. Analysis happens in Power Query, pandas, or a separate dashboarding station.
6. **Workbook checksum.** Write `<workbook>.xlsx.sha256` next to each one — lets the rollup builder skip unchanged files.

---

## What this spec does NOT do

- Does not define run.py code for any station.
- Does not specify the `xlsx_rebuilder.py` implementation.
- Does not touch the 32 stations outside these 5 lanes (nlp, nli, embed, graph, rerank, time, pub, etc. — separate spec passes).
- Does not address the legacy `7qs` lane (2 stations) — assume they merge into `sevenq` per STATION_INVENTORY note.
