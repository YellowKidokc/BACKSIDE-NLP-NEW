# Movement And Trace Contract

Purpose: define how articles and sections move through the workflow and how each lane marks that it has processed the material.

## Core Rule

Every section and every page should be able to answer:

- where it started
- what lane it passed through
- when it passed through
- what outputs were created
- whether the lane passed cleanly
- whether loopback was requested

## Recommended Processing Order

Default order for HTML article production:

1. `07_MATH_TRANSLATION`
2. `01_LOSSLESS`
3. `02_SECTION_MAP`
4. `03_YAML_METADATA`
5. `04_TAGS`
6. `05_CLAIMS`
7. `06_CONTRADICTIONS`
8. `08_SECTION_VECTORS`
9. `09_GRAPH_LINKS`
10. `10_RIGOR`
11. `11_HTML_RENDER`
12. `16_FINAL_PAGE_ASSEMBLY`
13. `17_PUBLISH_READY`

Important:

- this is the default route, not a prison
- loopback is expected
- math may need to be revisited after claims or rigor

## Why Math First

Math translation changes how the rest of the article is interpreted.

If we wait too late:

- claims may be extracted from bad plain-English math
- summaries may flatten equation meaning
- readability rewriting may distort formal structure

So math should mark the article early, even if it is provisional.

## Pass Markers

Each page and section should carry lane markers in machine form.

Suggested page-level fields:

```json
{
  "page_id": "",
  "lane_passes": {
    "math_translation": {
      "status": "pending|passed|loopback|failed",
      "timestamp_utc": "",
      "worker": "",
      "notes": ""
    }
  }
}
```

Suggested section-level fields:

```json
{
  "section_id": "",
  "passes": {
    "math_translation": {
      "status": "pending|passed|loopback|failed",
      "raw_math_present": true,
      "translated_math_present": true,
      "confidence": 0.0,
      "notes": ""
    },
    "claims": {
      "status": "pending|passed|loopback|failed"
    },
    "vectors": {
      "status": "pending|passed|loopback|failed"
    },
    "rigor": {
      "status": "pending|passed|loopback|failed"
    }
  }
}
```

## Human-Facing Trace

During build and testing, it is acceptable to expose lane badges in Markdown or HTML so everyone can see what has passed through.

Examples:

```text
[MATH: passed]
[CLAIMS: passed]
[RIGOR: loopback]
```

Or in HTML:

```html
<div class="workflow-badges">
  <span data-lane="math" data-status="passed">MATH</span>
  <span data-lane="claims" data-status="passed">CLAIMS</span>
  <span data-lane="rigor" data-status="loopback">RIGOR</span>
</div>
```

These can be hidden or removed later, but they are useful while the workflow is stabilizing.

## Movement Shapes

There are three important movement levels:

### 1. Whole-page movement

- one source file enters
- one page packet moves lane to lane

### 2. Section movement

- each `section_id` moves independently
- loopback may happen for one section without blocking the entire page forever

### 3. Artifact movement

- Markdown
- HTML
- JSON
- CSV
- Excel rollup

All three must stay aligned.

## Loopback Conditions

Loopback should happen when:

- math translation loses structural meaning
- section boundaries are unstable
- metadata conflicts with visible structure
- claims depend on a broken source span
- contradiction lane finds a major internal break
- readability rewriting simplifies away the actual argument

## Movement Script Role

The movement logic probably belongs in the NLP/model-side scripting layer because it is cross-cutting and needs to attach to any lane or sequence of lanes.

That movement script should eventually support:

- run one lane
- run a custom subset of lanes
- run a default ordered sequence
- update `layer-ledger.json`
- update section pass markers
- write loopback artifacts
- regenerate workbook rollup inputs

## Excel Relation

The movement layer should not write only to Excel.

It should:

1. update machine packets first
2. regenerate Markdown/HTML side artifacts
3. emit CSV tables
4. then roll all summary rows into the Excel workbook

## Bottom Line

The workflow should never leave us guessing whether a page or section has been through math, claims, vectors, graph, or rigor.

That state must be explicit.
