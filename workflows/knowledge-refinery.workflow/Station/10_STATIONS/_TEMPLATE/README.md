# {{STATION_ID}} — {{STATION_NAME}}

**Lane:** {{LANE}}
**Status:** draft
**Folder:** `10_STATIONS/{{FOLDER_NAME}}`

## Purpose

{{PURPOSE}}

## Mental model

```
WORKFLOW -> STATION -> MODEL -> PROMPT -> SCRIPT -> OUTPUT -> GATE -> NEXT STATION
```

This is one station. The contract lives in `station.yml`.

## Folders

| Folder    | What goes here                                                       |
|-----------|-----------------------------------------------------------------------|
| `prompts/`| Prompt files referenced by `prompt.primary` / `prompt.fallback`.      |
| `scripts/`| Runner code referenced by `script.runner`.                            |
| `input/`  | Drop incoming work items here. Each item is its own subfolder or file.|
| `output/` | Station writes results here. Files listed in `output.produces`.       |
| `review/` | Items that need a human eye before passing the gate.                  |
| `logs/`   | Run logs — one file per invocation, append-only.                      |
| `errors/` | Items that failed the gate, with the error trace alongside.           |

## Gate

Pass criteria are defined in `station.yml` under `gate.pass_if`. Anything failing the gate moves to `errors/` and routes to `gate.fail_to`. Anything needing human review moves to `review/`.

## Wiring

- Upstream stations: whoever lists this id under their `next.pass`.
- Downstream on pass: `{{NEXT_STATION_PASS}}`.
- Downstream on fail: `ST-ERR-001`.

## Activating

1. Fill in every `{{PLACEHOLDER}}` in `station.yml`.
2. Add the prompt file(s) to `prompts/`.
3. Add the runner to `scripts/`.
4. Flip `status: draft` to `status: active`.
5. Register in `10_STATIONS/station_registry.yml`.
