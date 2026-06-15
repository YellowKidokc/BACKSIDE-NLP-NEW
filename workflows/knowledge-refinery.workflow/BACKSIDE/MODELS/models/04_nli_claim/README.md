# Model: mnli_fever_anli

Purpose: NLI tuned for claim verification style tasks (MNLI/FEVER/ANLI blend).

Used by stations:
- `10_STATIONS/02_dedup` (optional rerank)
- `10_STATIONS/06_7qs_forward` (claim framing sanity)
- `10_STATIONS/08_7qs_evidence` (evidence entailment scoring)
- `10_STATIONS/09_science_checker` (overclaim audit)

Local assets:
- `_MODELS/HF_SNAPSHOTS/mnli_fever_anli`

