# Backside Architecture — the workhorse layer

**Owner:** David Lowe · canon-locked 2026-05-16
**Status:** live · phased migration from current X:\ layout
**Last updated:** 2026-05-20

The topology under `X:\Backside\`. Models are atoms, stations are reusable skills, workflows are end-to-end pipelines, services are local runtime dependencies, and control-plane folders hold repos/configuration. All are bound by env-var portability and a uniform state contract.

As of 2026-05-20, `Backside` is no longer only the archive/system bucket. It is the canonical home for machine-facing runtime. The X root is the front door; `GUI`, `Conversions`, `EXPORTS`, and `David` are the main outside surfaces.

---

## Working grammar

```text
station = reusable capability
workflow = ordered use of stations
packet = thing being transformed
```

Build verified stations first. Workflows compose stations rather than cloning their logic. Packets carry the source, public artifacts, working remnants, and machine metadata through the station chain.

The packet folder can be public-addressable, but only its `PUBLIC/` layer is consumer-facing.

See `PACKETS_CONVENTION.md` for the packet contract and `Backside\STATION_WORKFLOW_COMPOSITION.md` for the station/workflow composition contract.

---

## The three tiers

```
X:\Backside\                                  ← env-var: BRAIN_ROOT\Backside
│
├── _models/                                  ← model cards + local weight/runtime contracts
│     ├── moon-streak.model/                  ← e.g. theopoetic-style fine-tune
│     │     ├── moon-streak.gguf
│     │     ├── tokenizer.json
│     │     └── card.json                     ← {name, size, quant, license, anchor_role}
│     ├── deepseek-coder.model/
│     ├── clip-vision.model/
│     ├── deberta-v3-large.model/
│     ├── mistral-7b-instruct.model/
│     ├── whisper-large-v3.model/
│     ├── timeline.model/                    ← event/date/entity chronology builder
│     ├── facts.model/                       ← provenance-first fact ledger, no unsupported claims
│     └── paper-citation.model/              ← paper proximity, cite/represent/compare routing
│
├── stations/                                 ← reusable skill services (called by workflows)
│     ├── claim-extract.station/
│     ├── ME-tag-paragraph.station/           ← paragraph-level Master Equation tagger
│     ├── axiom-hit.station/
│     ├── fruits-score.station/
│     ├── seven-q-score.station/
│     ├── contradiction-scan.station/
│     ├── describe-figure.station/            ← clip-vision + Mistral describer
│     ├── deconstruct-picture.station/        ← look at picture → return prompt to replicate
│     ├── math-clarify.station/               ← Math Translation Layer as service
│     ├── theopoetic-format.station/          ← moon-streak-driven style emitter
│     └── lossless-summarize.station/         ← canonical lossless format
│
├── workflows/                                ← end-to-end pipelines (clicked from GUI)
│     ├── grade-paper.workflow/               ← what PPG becomes
│     ├── refresh-axiom-snapshot.workflow/    ← what axioms NLP becomes
│     ├── route-and-convert.workflow/         ← what knowledge-refinery becomes
│     ├── build-ai-portal.workflow/
│     ├── handoff-session.workflow/
│     ├── pull-link.workflow/
│     └── deconstruct-picture.workflow/       ← one-for-one workflows live here too
│
├── prompts/                                  ← reusable prompt packs, not runtime chatter
│     └── x-drive-reorg.prompt-pack/
│
├── _state/                                   ← cross-workflow run registry
│     ├── active_runs.json                    ← list of in-flight runs (GUI polls this)
│     └── history/                            ← finalized run records (date-rolled)
│
└── _archive/                                 ← what X:\Backside\ holds today
      ├── phase-logs/
      ├── scratch/
      ├── apps/
      └── root-leftovers/
```

---

## Packets tier addendum

`X:\Backside\packets\` is the portable-work-unit tier. It sits beside models, stations, and workflows.

```text
packets/
  <year>/<month>/<packet-name>/
    PUBLIC/     reader-facing pages and final exports
    WORKING/    source, drafts, station outputs, remnants
    MACHINE/    metadata, provenance, station logs, tags
    ARCHIVE/    superseded/raw/failed-run artifacts
```

Do not create top-level folders for every remnant. Remnants stay inside the packet that produced them.

---

## Every workflow folder has this shape

```
workflows/<workflow-name>.workflow/
  README.md                  ← human-facing (Layer 1 + Layer 2)
  _AGENT_BRIEF.md            ← AI-facing mission card
  RUN.bat                    ← click-button entry (defaults to configs/default.json)
  RUN_AGENT.bat              ← loads PRIMER + AGENT_BRIEF → LLM session
  health_check.bat           ← read-only probe (0=pass, 1=fail, 2=warn)
  pipeline.py                ← reads --config <name>, orchestrates stations
  dependencies.json          ← static declaration of what stations COULD be called
  configs/                   ← saved compositions (named workflow variants)
    default.json
    minus-lossless.json
    deep.json                ← any number, user-creatable from the GUI
  STATE/                     ← per-run state.json files, polled by GUI
    <run_id>.json
  prompts/                   ← prompt templates this workflow's pipeline.py loads
  00_DROP/                   ← intake
  OUTPUT/                    ← results
  ARCHIVE/                   ← processed inputs
```

## Every station folder has this shape

```
stations/<station-name>.station/
  README.md
  _AGENT_BRIEF.md
  station.py                 ← the service (callable from any workflow)
  prompt.md                  ← the prompt template
  health_check.bat
  uses-model.txt             ← single line: which model this station uses (e.g. "moon-streak.model")
  config.json
```

## Every model folder has this shape

```
_models/<model-name>.model/
  <weights>.gguf             ← or .safetensors, .bin, etc.
  tokenizer.json             ← or equivalent
  card.json                  ← metadata
```

`card.json` schema:
```json
{
  "name": "moon-streak.model",
  "anchor_role": "theopoetic-style-emitter",
  "base_model": "mistral-7b-instruct-v0.3",
  "quant": "Q4_K_M",
  "size_gb": 4.1,
  "license": "Apache-2.0",
  "fine_tuned": true,
  "fine_tune_dataset": "X:\\Backside\\_models\\moon-streak.model\\dataset-200-theopoetic-examples.jsonl",
  "trained_at": "2026-05-XX"
}
```

---

## Portability — drive-agnostic by contract

No hardcoded `X:\` anywhere. Every script reads `BRAIN_ROOT`.

**Batch script preamble:**
```batch
@echo off
if not defined BRAIN_ROOT (
  for %%i in ("%~dp0..\..\..\..") do set "BRAIN_ROOT=%%~fi"
)
:: now use %BRAIN_ROOT%\Backside\_models\..., etc.
```

**Python preamble:**
```python
import os, pathlib
BRAIN_ROOT = pathlib.Path(os.environ.get(
    "BRAIN_ROOT",
    pathlib.Path(__file__).resolve().parents[3]
))
```

Move `Backside/` to `B:\` or `D:\` — set `BRAIN_ROOT=B:\Backside` once, everything keeps working.

---

## State manifest — the contract that powers the GUI

Every workflow run writes one JSON to `STATE/<run_id>.json` and updates `_state/active_runs.json`.

```json
{
  "run_id": "2026-05-16T20-15-04_grade-paper_a7f3",
  "workflow": "grade-paper",
  "config": "default",
  "started_at": "2026-05-16T20:15:04Z",
  "ended_at": null,
  "status": "running",
  "inputs": [{"path": "00_DROP/foo.pdf", "type": "pdf", "size": 12345}],
  "outputs": [],
  "stations_called": [
    {"id": "claim-extract", "started_at": "...", "status": "done"},
    {"id": "axiom-hit", "started_at": "...", "status": "running"}
  ],
  "metrics": {},
  "errors": []
}
```

GUI polls `_state/active_runs.json` for the dashboard view, drills into individual run JSONs for detail.

---

## Workflow config schema — named compositions

`workflows/<workflow>/configs/<name>.json`:

```json
{
  "name": "default",
  "description": "Full grading with lossless summary and figure descriptions",
  "extends": null,
  "stations": [
    {"id": "claim-extract", "enabled": true, "params": {}},
    {"id": "ME-tag-paragraph", "enabled": true, "params": {"confidence_floor": 0.6}},
    {"id": "axiom-hit", "enabled": true},
    {"id": "fruits-score", "enabled": true},
    {"id": "seven-q-score", "enabled": true},
    {"id": "describe-figure", "enabled": true},
    {"id": "math-clarify", "enabled": true},
    {"id": "contradiction-scan", "enabled": true, "scope": ["internal", "canon"]},
    {"id": "lossless-summarize", "enabled": true}
  ],
  "outputs": ["html-axioms", "html-7q", "excel-workbook", "lossless-md", "vault-md"]
}
```

`minus-lossless.json` extends `default.json` and toggles one station off:
```json
{"name": "minus-lossless", "extends": "default",
 "stations": [{"id": "lossless-summarize", "enabled": false}],
 "outputs": ["html-axioms", "html-7q", "excel-workbook", "vault-md"]}
```

---

## Dependencies declaration

`workflows/<workflow>/dependencies.json`:

```json
{
  "stations": ["claim-extract", "ME-tag-paragraph", "axiom-hit", "fruits-score",
               "seven-q-score", "describe-figure", "math-clarify",
               "contradiction-scan", "lossless-summarize"],
  "models": [],
  "external_services": [
    {"name": "qdrant", "endpoint": "http://192.168.1.177:6333"},
    {"name": "postgres", "endpoint": "192.168.1.177:2665"}
  ],
  "sinks": ["proof-explorer", "qdrant:paper_proof_grader", "vault:O:\\_Theophysics_v5\\"]
}
```

The root health-check (`X:\CHECKS\RUN_ALL.bat`) reads every `dependencies.json` and verifies every claimed station/service is reachable.

Workflow configs must reference station IDs, not station folders copied into workflow folders. A workflow can add orchestration and prompt overlays, but station implementation stays canonical under `Backside\stations\<station-id>.station\`.

---

## Migration map (current → new)

| Current path | New path |
|---|---|
| `X:\Backside\brain_dashboard\` | `X:\GUI\brain-dashboard\` |
| `X:\Backside\conversion_lib\` | `X:\Conversions\conversion-layer\` |
| `X:\paper-proof-grader\` | `Backside/workflows/grade-paper.workflow/` |
| `X:\axioms\` | `Backside/workflows/refresh-axiom-snapshot.workflow/` (logic → `stations/axiom-hit.station/`) |
| `X:\knowledge-refinery\` | `Backside/workflows/route-and-convert.workflow/` (model-stations → real `stations/`) |
| `X:\ai-portal-generator\` | `Backside/workflows/build-ai-portal.workflow/` |
| `X:\session-handoff-drop\` | `Backside/workflows/handoff-session.workflow/` |
| `X:\link-pull-drop\` | `Backside/workflows/pull-link.workflow/` |
| `X:\models\` | `Backside/_models/downloaded/` |
| `X:\Backside\models\` | `Backside/_models/legacy-model-layer/` |
| `X:\Preference Engine Build\` | `Backside/control-plane/Preference Engine Build/` |
| `X:\github\` | `Backside/control-plane/github/` |
| `X:\ollama\` | `Backside/services/ollama/` |
| `X:\proof-architecture\`, `X:\proof-explorer\` | `X:\EXPORTS\proof-architecture`, `X:\EXPORTS\proof-explorer` |
| `X:\Backside\` (current archive) | `Backside/_archive/` |
| `D:\GitHub\Math-Translation-Layer\` | `Backside/stations/math-clarify.station/` (move + repackage) |

---

## Related

- `THEOPHYSICS_PRIMER.md` — framework anchor (load first in every AI session)
- `FOLDER_CONVENTIONS.md` — universal 3-layer folder contract
- `ARCHITECTURE.md` — the wider X:\ system map (Mermaid diagrams)
- `00_WORKFLOWS/prompts/x-drive-reorg/4e_pyside_workflow_composer.md` — the GUI spec that consumes this architecture
