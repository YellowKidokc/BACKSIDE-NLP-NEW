# HTML Workflow Swarm Work Order - Round 1

Use this as the single prompt for worker partners.

Replace only the worker number and callsign if needed.

---

You are `worker-{N}` assigned to the HTML article workflow.

Workflow root:

`\\dlowenas\brain\Backside\workflows\html-article.workflow`

Station root:

`\\dlowenas\brain\Backside\stations`

Read first:

- `prompts/WORKER_DISPATCH.md`
- `prompts/LLM_SWARM_EXECUTION_PROMPT.md`
- `configs/ARTICLE_OUTPUT_REGISTRY.md`
- `configs/MASTER_INDEX_WORKBOOK_CONTRACT.md`
- `configs/SEMANTIC_ADDRESS_AND_ROUTING.md`
- `configs/MOVEMENT_AND_TRACE_CONTRACT.md`

## Mission

Do not redesign the architecture.

Do not fork the schema.

Get your assigned lane family testable against:

- `00_DROP/CALIBRATION_pilot-preflight-checklist.md`
- `00_DROP/gtq-03-free-will-two-frames.html`

Your job is to produce:

1. `contract.json`
2. `README.md`
3. `sample_output/`
4. `run.py` or `run_prompt.md`

If upstream is missing, mock input and document it.

If your output fails structurally, write a loopback artifact into:

`14_LOOPBACK_REVIEW`

## Global Rules

- Semantic address identifies the artifact.
- Grade/readiness do not become the permanent filename.
- `story_flag` must stay explicit.
- One persistent workbook exists for the whole workflow:
  `12_EXPORTS/MASTER_ARTICLE_INDEX.xlsx`
- Excel is a rollup surface, not the only source of truth.
- JSON first, Markdown/HTML second, Excel third.
- Math translation is revisitable, not final authority.
- Every section is a first-class unit.

## Current Coordination Assumptions

Use these unless Opus posts a change:

1. HTML workflow can run in parallel with FAP and does not need to block on FAP to start.
2. If FAP outputs already exist, they may be consumed as upstream artifacts rather than rebuilt.
3. Shared field vocabulary should converge centrally; do not invent synonyms for the same field.
4. Current workbook columns are provisional canon for this round, not final forever.

## Worker Assignments

### If you are `worker-1`

Own:

- `02_SECTION_MAP`
- `03_YAML_METADATA`
- `configs/shared_lib` support if needed

Primary station targets:

- `section-splitter.station`
- `metadata-extractor.station`

Main deliverable:

- stable section packets with section ids
- routing-ready metadata and YAML candidate

### If you are `worker-2`

Own:

- `04_TAGS`
- `05_CLAIMS`

Primary station targets:

- `claim-extractor.station`
- existing embedder/tagging infrastructure

Main deliverable:

- section tags
- claim packets
- Excel-ready claim columns

### If you are `worker-3`

Own:

- `07_MATH_TRANSLATION`
- `14_LOOPBACK_REVIEW`

Primary targets:

- `Math-Translation-Layer` app
- loopback contract enforcement

Main deliverable:

- math payload
- raw-vs-translated math trace
- loopback triggers when translation breaks structure

### If you are `worker-4`

Own:

- `08_SECTION_VECTORS`
- `09_GRAPH_LINKS`

Primary station targets:

- `sbert-embedder.station`
- `graph-linker.station`

Main deliverable:

- per-section vectors
- edge candidates
- graph-ready exports without over-owning storage/rendering

### If you are `worker-5`

Own:

- `10_RIGOR`
- `13_LAYER_LEDGER`
- workbook append contract alignment

Primary targets:

- `7q-classifier.station`
- `deberta-runner.station`
- workbook + layer ledger integration

Main deliverable:

- rigor packet
- readiness decision packet
- section/page pass markers
- append/update rows for `MASTER_ARTICLE_INDEX.xlsx`

## If More Workers Join

### `worker-6`

Own:

- `11_HTML_RENDER`
- `16_FINAL_PAGE_ASSEMBLY`

### `worker-7`

Own:

- `readability-rewriter.station`
- `accessible` and `academic` mode outputs

## Reporting Format

Post progress to `workflow-4`:

`[worker-{N}] STATUS: active|blocked|testable. Lanes: .... Files: .... Gaps: ....`

When blocked, say exactly what you need.

When testable, point to the deliverables folder and sample output.

## Quality Bar

Testable means another partner can pick up your lane without guessing:

- inputs are explicit
- outputs are explicit
- sample output exists
- loopback conditions exist
- downstream dependencies are named

Bottom line:

Align now. Refine centrally. Do not fork.
