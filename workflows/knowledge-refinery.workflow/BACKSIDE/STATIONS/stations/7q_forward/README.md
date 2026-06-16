# ST-7QS-009 — 7Q Forward

**Lane:** 7qs
**Status:** draft
**Folder:** `stations/09_7q_forward`
**Wraps model:** `gpt-4o-mini`

## Purpose

Forward 7-Question Scientific Method -- classification pass on a paper (Q0..Q7).

## Mental model

```
WORKFLOW -> STATION -> MODEL -> PROMPT -> SCRIPT -> OUTPUT -> GATE -> NEXT STATION
```

## Layout (mirrors MODELS wrapper)

| Path                | What                                                       |
|---------------------|-------------------------------------------------------------|
| `station.yml`       | Contract — model binding, IO, gate, next.                   |
| `PROMPT_SYSTEM.md`  | System prompt (if station calls an LLM).                    |
| `PROMPT_TEST.md`    | Health-check prompt with expected output.                   |
| `cache/`            | Caches (model outputs, intermediate state).                 |
| `input/`            | Drop incoming work here. `sample_input.md` for smoke tests. |
| `output/`           | Results land here. Files listed in `output.produces`.       |
| `review/`           | Items needing human review before gate.                     |
| `logs/`             | One log per invocation, append-only.                        |
| `errors/`           | Gate failures + trace.                                      |
| `scripts/00_init.bat`        | Create required folders.                          |
| `scripts/01_healthcheck.bat` | Liveness check.                                   |
| `scripts/02_smoke_test.bat`  | Smoke test using `input/sample_input.md`.         |
| `scripts/03_run_prompt.bat`  | Main entry — wraps the runner.                    |
| `scripts/05_stop.bat`        | Teardown.                                         |

## Activation checklist

1. Fill in remaining `{{PLACEHOLDER}}` tokens in `station.yml`.
2. Drop the real runner into `scripts/` (Python or shell).
3. Flip `status: draft` → `status: active` in both `station.yml` AND `stations_registry.yml`.
4. Smoke test: `scripts\02_smoke_test.bat`.
