# Span Trace Station

`span_trace` is the trace-first station. It runs before claim extraction and all grader passes.

Its job is to create:

- `trace-ledger.json`
- `trace-ledger.csv`
- `trace-ledger.md`

Later stations should reference `trace_id` instead of inventing paragraph, sentence, or character locations.

Contract:

`X:\Backside\workflows\series-flow-auditor.workflow\contracts\TRACE_REQUIRED_OUTPUT_CONTRACT.md`
