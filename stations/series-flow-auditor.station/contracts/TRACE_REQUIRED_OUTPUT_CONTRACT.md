# TRACE REQUIRED OUTPUT CONTRACT

Version: 2026-05-25
Status: draft-contract
Applies to: claim extraction, 7Q passes, fruits scoring, Master Equation scoring, epistemic integrity, contradiction scans, proof packet rendering.

## Core Rule

Every station output must answer:

- Where did this come from?
- What exact source span caused it?
- What kind of signal is it?
- How confident is the station?
- What should happen next?

Every extracted claim, score, objection, question answer, contradiction, fruit signal, axiom match, or Master Equation signal must include either:

```json
{
  "trace_status": "anchored"
}
```

or:

```json
{
  "trace_status": "missing-span"
}
```

No silent blanks are valid.

## Required Trace Block

Use this block for any output item tied to a local source span:

```json
{
  "trace_id": "trace-000000",
  "trace_scope": "sentence",
  "section_id": "SEC-001",
  "paragraph_index": 3,
  "sentence_index": 2,
  "char_start": 1842,
  "char_end": 1927,
  "quoted_span": "Exact text from the source goes here.",
  "trace_status": "anchored"
}
```

Allowed `trace_scope` values:

- `sentence`
- `paragraph`
- `section`
- `document`
- `multi_span`

Use the narrowest scope that honestly contains the signal.

## Missing Span Rule

If the station cannot anchor a result to an existing `trace_id`, place it under `unanchored_candidates` and include:

```json
{
  "trace_status": "missing-span",
  "reason": "The claim is inferred from the document as a whole, not directly stated in a local span.",
  "required_followup": "route_to_document_level_trace"
}
```

The station may not promote an unanchored candidate into the main ledger.

## Inherited Output Fields

Every station-specific output item must include:

```json
{
  "item_id": "station-item-000000",
  "trace_id": "trace-000000",
  "trace_status": "anchored",
  "signal_type": "claim",
  "confidence": 0.82,
  "recommended_action": "keep"
}
```

Allowed `signal_type` values:

- `claim`
- `evidence`
- `definition`
- `method`
- `objection`
- `contradiction`
- `severity`
- `axiom`
- `7q`
- `fruit`
- `master_equation`
- `reader_burden`
- `series_order`
- `other`

Allowed `recommended_action` values:

- `keep`
- `revise`
- `merge`
- `move`
- `appendix`
- `cut`
- `needs_evidence`
- `needs_definition`
- `needs_bridge`
- `route_to_document_level_trace`
- `human_review`

## Invalid Output

An item is invalid if:

- It has no `trace_status`.
- It has `trace_status: anchored` but no `trace_id`.
- It includes a paraphrase where `quoted_span` is required.
- It invents source location fields not present in the `trace-ledger.json`.
- It collapses multiple non-overlapping spans into one sentence-level trace.
- It makes a document-level inference without marking `trace_status: missing-span` or `trace_scope: document`.

## Pipeline Rule

The trace ledger is created before smart interpretation:

```text
HTML / Markdown
-> span-trace.station
-> trace-ledger.json
-> claim-extractor.station
-> 7q-classifier.station
-> fruits-spirit-canon.station
-> master-equation-canon.station
-> epistemic-integrity.station
-> contradiction-scan.station
-> proof-packet renderer
```

Later stations reference trace IDs. They do not invent locations.

## Cost Rule

Full-document reasoning should be minimized.

Preferred order:

1. Parse once into stable spans.
2. Run cheap deterministic span ledger.
3. Run NLP/LLM stations against the ledger and only the needed span windows.
4. Escalate to document-level reasoning only for `missing-span`, dependency, contradiction, and synthesis cases.

The claim workbook is an index over trace-backed results, not the reasoning engine itself.
