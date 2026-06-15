# CODEX MASTER PROMPT — Theophysics Brain System
## POF 2828 | June 2026

You are working on the Theophysics Brain — a local NLP + preference engine
infrastructure on a Windows machine. The brain lives at X:\ (network share
mapped to \\192.168.2.50\brain).

## FOLDER STRUCTURE (locked, do not renumber)

```
X:\
01_FRONT_DOOR      — Manual file drop point (human entry)
02_HUMAN_REVIEW    — Items needing David's eyes
03_JOB_CARDS       — Machine-managed truth layer (JSON job tickets)
04_STATIONS        — Processing stations (~50 .station folders)
05_MODELS          — M01-M16 NLP models (weights excluded from repo)
06_ENGINES         — P01-P07 preference learning engines
07_ORCHESTRATOR    — Watcher, router, dispatcher, front-doors, scripts
08_DASHBOARDS      — Local web UIs
09_DATABASES       — DB schemas, configs
10_EXPORTS         — Dated run folders (YYYY-MM-DD__RUN_NNN__module)
11_LOGS            — All logs, health reports
12_JUNK            — Auto-cleanup quarantine
13_ARCHIVE         — Cold storage, legacy structures
14_CONFIG          — JSON registries, route rules, configs
15_TEMPLATES       — Reusable reference files, scoring rubrics
16_VECTOR_INDEXES  — Embedding/search memory
17_KNOWLEDGE_GRAPHS — Relationship maps
18_APPS            — Full independent systems (paper grader, BIL, etc.)
conversion_station — Pre-processor (converts files before station routing)
```


## ARCHITECTURE RULES

1. **Universal pattern:** inbox → job card → route → process → outbox
2. **Station = one action.** If it does 5 things, split it.
3. **Workflow = ordered chain of stations.**
4. **App = standalone system that may call workflows/stations.**
5. **Model = NLP worker (M01-M16).** Called by stations, never called directly by humans.
6. **Engine = preference learner (P01-P07).** Learns David's patterns over time.
7. **Job card = truth record.** JSON file tracking: input, intent, workflow, stations used, artifacts, status.
8. **All configs are JSON.** No YAML anywhere. Hard rule.
9. **conversion_station runs BEFORE any other station** (markdown, TTS, audio format conversion).

## HIERARCHY

```
Model = worker
Preference engine = learner
Station = one processing step
Workflow = ordered task chain
App = full independent system
Job card = truth record
Export = packaged human output
```

## TASK 1: STATION SCRIPT STANDARD (SSS_v1)

Every station Python script must follow this section order:

```
00_IMPORTS
01_CONSTANTS_AND_PATHS
02_CONFIG_LOADING
03_LOGGING
04_INGEST (read inbox)
05_VALIDATE
06_ROUTE_OR_CALL_WORKER (pick which M-model to use)
07_PROCESS (the station's ONE action)
08_WRITE_ARTIFACTS (save raw output)
09_UPDATE_JOB_CARD (update truth record)
10_EXPORT_OR_HANDOFF (pass to next station or export)
11_ARCHIVE_INPUTS (move processed input to _processed)
12_MAIN
```


Each station folder must contain:
```
station-name.station/
  config.json           — paths, worker assignment, input extensions
  pipeline.py           — SSS_v1 format script
  START.bat             — launches pipeline.py
  HEALTHCHECK.bat       — verifies dependencies + paths
  PROCESS_INBOX.bat     — one-shot inbox processing
  TROUBLESHOOT.md       — what this station does, common errors
  _inbox/
  _outbox/
  _processed/
  _state/
  _logs/
```

For every existing .station folder, Codex should:
1. Read existing scripts/prompts to understand what the station does
2. Write a new `pipeline.py` in SSS_v1 format
3. Write `config.json` with relative paths (use ./ not absolute)
4. Write `config.example.json` (same but sanitized for repo)
5. Write START.bat, HEALTHCHECK.bat, PROCESS_INBOX.bat
6. Write TROUBLESHOOT.md

## TASK 2: JOB CARD SYSTEM

Build `X:\03_JOB_CARDS\job_card_manager.py`:
- create_job_card(source_file, intent, workflow) → JSON file
- update_job_card(job_id, station_id, artifact_path, status)
- get_pending() → list of pending job cards
- get_failed() → list of failed job cards

Job card JSON schema:
```json
{
  "job_id": "JOB_2026-06-14_0001",
  "source_file": "path",
  "source_type": "pdf",
  "user_intent": "paper_grader",
  "workflow": "WF_001",
  "status": "pending|running|failed|done|needs_review",
  "created_at": "ISO timestamp",
  "work_orders": [],
  "artifacts": [],
  "errors": [],
  "review_required": true
}
```

Subfolder structure:
```
03_JOB_CARDS/
  _pending/
  _running/
  _done/
  _failed/
  _needs_review/
```


## TASK 3: ROUTER / ORCHESTRATOR

Build `X:\07_ORCHESTRATOR\router.py`:
- Watches `01_FRONT_DOOR/_inbox/`
- Identifies file type + user intent (from filename or drop subfolder)
- Creates a job card in `03_JOB_CARDS/_pending/`
- Routes to the correct workflow or station
- If file needs conversion first → send to conversion_station

## TASK 4: EXPORT SYSTEM

Dated run folders in `10_EXPORTS/`:
```
10_EXPORTS/
  2026-06-14__RUN_001__paper_grader_internal/
    00_MANIFEST.json
    01_INPUTS/
    02_WORK_ORDERS/
    03_ARTIFACTS/
    04_REPORTS/
    05_REVIEW/
    06_FINAL_EXPORT/
    07_LOGS/
```

Build `X:\07_ORCHESTRATOR\create_run_folder.py`:
- create_run_folder(module_name, mode) → creates dated folder from template
- Templates live in `15_TEMPLATES/run_templates/`

## TASK 5: HEALTHCHECK

Build `X:\07_ORCHESTRATOR\brain_healthcheck.py`:
- Checks every numbered folder exists
- Checks each station has config.json + pipeline.py
- Checks each model folder has weights
- Checks each engine has config.json
- Reports missing/broken items
- Writes report to `11_LOGS/`

## MODELS (reference only, weights excluded)

M01_summarizer, M02_embedder, M03_contradiction, M04_imager,
M05_transcriber, M06_llm, M07_fact_verify, M08_contradiction_deep,
M09_claim_extract, M10_timeline, M11_math_verify, M12_paper_review,
M13_bart_summarizer, M14_clip_vision, M15_mistral_7b, M16_whisper_large_v3

## ENGINES (reference only)

P01_implicit, P02_recbole, P03_lightfm, P04_paper_recommender,
P05_ppk, P06_river, P07_markovify

## CHANGE TARGETS

Codex MAY edit: station scripts, batch launchers, config files,
orchestrator code, README/TROUBLESHOOT docs, tests.

Codex MUST NOT edit: model folders, real exports, logs, trained state,
production configs with live paths, private notes.

Primary mission: Standardize every station to SSS_v1 format,
wire the job card system, build the router, build the export system.

