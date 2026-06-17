# Field Mapping: Snapshot JSON → PaperMaster Excel → HTML Proof Explorer

## Legend
- ✅ Direct mapping exists
- ⚠️ Partial/derivable mapping
- ❌ No source — needs LLM or manual entry

---

## SECTION 1: METADATA (Excel cols 1–11)

| Excel Column | Snapshot JSON Path | HTML Template Location | Status |
|---|---|---|---|
| Article_ID | `identity.paper_id` | `theophysics-structure.uuid`, breadcrumb | ✅ |
| UUID | `identity.paper_id` | right sidebar Metadata | ✅ |
| Hash | `pipeline_metrics.source_sha256` (from grader) | — | ⚠️ |
| Title | `identity.title` | `<h1>` paper title | ✅ |
| Author | `identity.author` | right sidebar Author | ✅ |
| Series | `identity.series` | breadcrumb parent | ✅ |
| Doc_Type | classify_runner → `doc_type` | `theophysics-structure.doc_type` | ✅ |
| Classification | classify_runner → `classification` | right sidebar Classification | ✅ |
| Status | — | `theophysics-structure.status` | ❌ manual |
| Last_Updated | — | `theophysics-structure.last_updated` | ❌ manual |
| Word_Count | `pipeline_metrics.L1_word_count` | `theophysics-structure.word_count` | ✅ |

## SECTION 2: VECTOR χ (Excel cols 12–21) — ALL WIRED ✅

G, M, E, S, T, K, R, Q, F, C → `pipeline_metrics.L3_me_*`

## SECTION 3: SPINE % (Excel cols 22–27) — ALL WIRED ✅

6 domains → classify_runner `spine_mappings` → HTML sidebar spine bars

## SECTION 4: NLP SCORES (Excel cols 28–32) — 4/5 WIRED ✅
