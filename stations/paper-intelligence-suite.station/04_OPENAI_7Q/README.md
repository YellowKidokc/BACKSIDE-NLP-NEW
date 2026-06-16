# 04_OPENAI_7Q

Canonical 7Q lane for the Paper Intelligence suite.

## What Lives Here

- `engine_v2/` — imported core from the verified standalone `7q-main` engine.
- `seven_q_runner.py` — suite compatibility runner for OpenAI-backed forward/reverse 7Q.
- `ollama_7q_runner.py` — local-model runner for 7Q + snapshot + peer-review sections.
- `extract_text.py` — shared text cleaning so HTML and markdown use one ingestion path.
- `prompts/` — snapshot and peer-review section prompts used by the suite's richer report path.

## Canonical Rule

If there is overlap between older suite 7Q logic and the standalone 7Q engine,
`engine_v2/` is the source of truth for the 7Q scoring/report vocabulary.

The suite runners remain as adapters so the broader paper-intelligence pipeline
does not need to change all its entrypoints at once.

## Archived Legacy

Legacy filler scripts that were not part of the active run path were moved to:

- `_archive/20260522_legacy_7q/`
