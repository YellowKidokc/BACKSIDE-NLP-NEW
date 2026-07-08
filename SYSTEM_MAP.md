# SYSTEM MAP — read this first

One-page orientation for any human or AI model working in this repo.

## The system in one sentence
Drop a document in the front door, run a station chain, collect outputs — everything else is plumbing.

## Layout
| Where | What |
|---|---|
| `stations/` | 12 ACTIVE processing stations (`<name>.station/` each with `pipeline.py` + `RUN.bat` + `_inbox/_outbox/_processed`) |
| `stations/_DORMANT/` | 63 scaffolded-but-unused stations. Revive by moving one out and registering it. |
| `engines/preference-engine-*` | 7 recommender/preference engines (implicit, recbole, lightfm, paper-recommender, ppk, river, markovify) |
| `nlp_api/` | FastAPI model service, port 8700 (`/nlp/summarize,/ner,/sentiment,/classify,/qa`). Models load from `D:\nlp_models` per its `MODEL_REGISTRY.json`. |
| `orchestrator/` | legacy orchestration scripts |
| `templates/`, `workflows/` | HTML/xlsx templates and saved workflow packets |

## Control layer (separate repo)
`D:\GitHub\brain-station-runner` — the console. Single entry point:
```
python console.py doctor              # health check
python console.py stations            # list
python console.py run <station> --execute -i <file>
python console.py run-chain <workflow> --execute
```
Canonical station registry: `X:\14_CONFIG\STATION_REGISTRY.json`
(`X:\` = `\\192.168.2.50\brain` — the NAS "brain" share; the console normalizes all path spellings).

## Data locations
- NAS `X:\01_FRONT_DOOR\_inbox` — where humans drop input files
- NAS `X:\04_STATIONS` — LIVE station instances (this repo's `stations/` mirrors it, 12 active + _DORMANT)
- `D:\nlp_models` — model weights for the API service (live store)
- NAS `X:\05_MODELS` — older model mirror, audit pending

## Rules for AI workers
1. Never edit a station you weren't assigned.
2. Never hardcode a new path spelling; use `X:\...` and let the console normalize.
3. Outputs go to a station's `_outbox`; never write into `_processed`.
4. Worker task prompts live in `brain-station-runner/*_PROMPT.md` — one station/task per run.
