# Model: 09_reasoning (qwen3_reasoning_worker)

Purpose: general reasoning worker for 7QS synthesis, station decisions, and structured outputs.

Used by stations (expected):
- `10_STATIONS/06_7qs_forward`
- `10_STATIONS/07_7qs_reverse`
- `10_STATIONS/12_axiom_promotion`

Good at:
- multi-step reasoning
- JSON-first structured responses

Do not use for:
- embedding generation
- heavy PDF conversion

How to run:
- `scripts\\01_healthcheck.bat`
- `scripts\\02_smoke_test.bat`

Last known status:
- wrapper created; runtime wiring pending (choose provider: Ollama/OpenAI/other).

