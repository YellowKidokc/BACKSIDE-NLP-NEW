# 08_SECTION_VECTORS - Section Vectors Lane

Owner this round: **worker-4**. Pipeline step: **3** in `lane_registry.json`. Upstream: `02_SECTION_MAP` (hard), `03_YAML_METADATA` (soft). Downstream: `09_GRAPH_LINKS`, `10_RIGOR`, `15_SECTION_PACKETS`, `16_FINAL_PAGE_ASSEMBLY`.

## What this lane does

Turns each stable `section_id` into a reusable vector object. This is the first machine-semantic pass over the article body: section text becomes a normalized embedding payload other lanes can compare without reparsing the source file.

This lane should **prefer the existing SBERT station path** (`sbert-embedder.station` -> Infinity -> all-MiniLM-L6-v2). But HTML workflow does not stall on infrastructure. If the station or embedding service is unavailable, the lane emits deterministic hash-based fallback vectors and marks them honestly instead of pretending they are real SBERT embeddings.

## Inputs

| Required | Source |
|---|---|
| `section-map.json` | `02_SECTION_MAP/` |
| `section_packets/*.md` | `02_SECTION_MAP/sample_output/<article>/section_packets/` when present |
| `metadata.json` | `03_YAML_METADATA/` (page_id, paper_uuid, title, address candidate) |
| station config | `\\dlowenas\brain\Backside\stations\sbert-embedder.station\config.json` |

If the packet file is missing, lane 08 falls back to `text_excerpt`. If lane 02 is absent entirely, it builds a minimal synthetic section ledger from the raw `00_DROP` file and records `provenance.mocked = true`.

## Outputs

| Artifact | Form |
|---|---|
| `section-vectors.jsonl` | Machine-readable. One object per section. |
| `vector-metadata.json` | Page-level summary, embedding source, counts, nearest-neighbor hints, loopback state. |

JSONL is the source of truth. The workbook `Vector_Index` sheet is just a rollup of these rows.

## Vector object shape

Each JSONL row includes:

- `paper_uuid`
- `page_id`
- `section_id`
- `stable_uuid`
- `ordinal`
- `heading_path`
- `text_hash`
- `vector_dim`
- `vector_source`
- `embedding_norm`
- `embedding`
- `provenance`

`vector_source` is one of:

- `infinity` - real embedding service path succeeded
- `hash-fallback` - deterministic local fallback
- `mocked-upstream` - synthetic section input had to be built first

## How to run

```powershell
py -3 "X:\Backside\workflows\html-article.workflow\08_SECTION_VECTORS\run.py" --article calibration
py -3 "X:\Backside\workflows\html-article.workflow\08_SECTION_VECTORS\run.py" --article gtq-03
```

Optional overrides:

- `--section-map <path>`
- `--metadata <path>`
- `--output-dir <path>`
- `--prefer-fallback` to skip the Infinity call and emit deterministic vectors immediately

## Calibration target

Per `configs/CALIBRATION_EXPECTED.md`, the calibration article should emit **4 section embeddings**. That is the minimum structural pass condition.

## Known gaps

- The station folder exists, but it is repo-general and not yet wrapped for this workflow's section-map contract.
- FAP embedding overlap has not been harvested yet. If FAP already has per-section vectors for GTQ-03, this lane should consume them next round rather than duplicating work.
- Vector sheet columns are only lightly specified in the workbook contract, so this lane keeps JSONL rich and lets downstream export flatten it later.

## Loopback conditions

Written to `14_LOOPBACK_REVIEW/08_section_vectors_loopback.json` when:

1. Output row count differs from lane 02 section count.
2. Any section resolves to empty text.
3. Embedding dimensions drift inside one run.
4. All non-empty sections collapse to the same vector.

## Excel columns

Tab: `Vector_Index`. Columns: `paper_uuid`, `page_id`, `section_id`, `stable_uuid`, `heading_path`, `vector_dim`, `vector_source`, `embedding_norm`, `text_hash`, `provenance`.
