# Station Script Standard v1 (SSS_v1)
**POF 2828 | 2026-06-14**

## The Rule
Every station Python script follows the same 13-section structure, in the same order, every time. If you open any station, you know where everything is.

## Section Map

| Section | Name | Changes per station? | What it does |
|---------|------|---------------------|--------------|
| 00 | IMPORTS | Rarely | Standard library + station-specific deps |
| 01 | CONSTANTS | YES (identity + resolvers) | STATION_ID, STATION_NAME, STATION_DESC, TEMPLATES resolver |
| 02 | CONFIG | Never | Load config.json or station.yaml |
| 03 | LOGGING | Never | Setup logger (file + console) |
| 04 | INGEST | Never | Read _inbox/, find files by extension |
| 05 | VALIDATE | Rarely | Check inputs exist, readable, right format |
| 06 | NLP_ROUTE | **YES** | Which NLP model to call (M01-M16) |
| 07 | PROCESS | **YES** | The station's ONE action |
| 08 | ARTIFACTS | Never | Write result to _outbox/ as JSON |
| 09 | JOB_CARD | Never | Update job card in 03_JOB_CARDS |
| 10 | HANDOFF | Rarely | Pass to next station or export |
| 11 | ARCHIVE | Never | Move input to _processed/ |
| 12 | MAIN | Never | Wire it all together |

## The Key Insight
10 of 13 sections are IDENTICAL across all stations. Only 3 change:
- 01: Station identity (ID, name, description)
- 06: Which NLP to call
- 07: What the station actually does
This means:
1. You can GENERATE a new station from the template in seconds
2. You can BATCH-UPDATE all stations with a script targeting one section
3. You can AUDIT all stations by checking section structure
4. Codex can STANDARDIZE existing stations by mapping old code to SSS sections

## Path Architecture
All paths are RELATIVE to the script location. Never hardcode X:\.

```python
HERE      = Path(__file__).resolve().parent     # this station
STATIONS  = HERE.parent                         # 04_STATIONS or stations/
BRAIN     = STATIONS.parent                     # brain root (X:\ or repo root)

def _resolve(numbered, flat):
    p = BRAIN / numbered
    return p if p.is_dir() else BRAIN / flat

MODELS    = _resolve("05_MODELS",    "models")
ENGINES   = _resolve("06_ENGINES",   "engines")
JOB_CARDS = _resolve("03_JOB_CARDS", "job_cards")
EXPORTS   = _resolve("10_EXPORTS",   "exports")
TEMPLATES = _resolve("15_TEMPLATES", "templates")
```

If the brain moves from X:\ to D:\brain, NOTHING changes in any station.
The `_resolve` shim also handles the GitHub repo layout (flat folder names
like `models/` instead of `05_MODELS/`), so stations work in both environments.

## Template Resolver
Stations that consume or render templates MUST reference filenames from `config.json` under `templates`, grouped by role:

```json
{
  "templates": {
    "input_lexicon": ["paper_grader_lexicons_master_enhanced.xlsx"],
    "input_data": ["citation_map.xlsx"],
    "input_rubric": ["paper_intelligence.xlsx"],
    "output_template": ["mda-grades.html"],
    "output_excel": ["OUTREACH_TRACKER.xlsx"]
  }
}
```

Resolve every configured filename through `TEMPLATES = _resolve("15_TEMPLATES", "templates")`. Markdown templates may live below `templates/md/`. The JSON artifact remains the always-present baseline even when HTML or Excel renderings are emitted.

## Standard Station Folder
```
station-name.station/
  _inbox/          ← inputs land here
  _outbox/         ← artifacts go here
  _processed/      ← archived inputs
  _logs/           ← execution logs
  _state/          ← persistent state
  _exports/        ← final exports (terminal stations only)
  pipeline.py      ← the station script (SSS_v1 format)
  config.json      ← station config
  START.bat         ← launcher
  HEALTHCHECK.bat   ← self-test
  TROUBLESHOOT.md   ← common issues
  AI_README.md      ← living doc for AI sessions
```
## NLP Model Registry
```
X:\05_MODELS\
  M01_summarizer         M09_claim_extract
  M02_embedder           M10_timeline
  M03_contradiction      M11_math_verify
  M04_imager             M12_paper_review
  M05_transcriber        M13_bart_summarizer
  M06_llm                M14_clip_vision
  M07_fact_verify        M15_mistral_7b
  M08_contradiction_deep M16_whisper_large_v3
```

## Preference Engine Registry
```
X:\06_ENGINES\
  P01_implicit    P05_ppk
  P02_recbole     P06_river
  P03_lightfm     P07_markovify
  P04_paper_recommender
```

## Section 08 Template-Aware Artifact Rule
Section 08 always writes the canonical JSON artifact to `_outbox/`. If `config.json` declares `templates.output_template`, Section 08 may additionally render an HTML artifact by loading the configured HTML file from `TEMPLATES` and replacing station-provided placeholders. If `config.json` declares `templates.output_excel`, Section 08 may additionally create an Excel-compatible artifact using the configured workbook filename as the export contract.

The required baseline is never optional:
1. JSON artifact: always present, machine-readable, complete.
2. HTML render: optional companion when an HTML output template is configured.
3. Excel render/export: optional companion when an Excel output template is configured.

## Batch Update Script Pattern
Because every station has the same structure, you can write:

```python
# Example: update all stations to use new NLP path convention
for station_dir in (BRAIN / "04_STATIONS").iterdir():
    pipeline = station_dir / "pipeline.py"
    if pipeline.exists():
        code = pipeline.read_text()
        # Find section 06, replace NLP routing logic
        # Find section 01, update constants
        # etc.
```

## Hierarchy
```
Station = one action
Workflow = many stations in order
App = whole independent system
NLP = worker (model)
Engine = learner (preference)
Job Card = truth record
Export = packaged human output
```

If a station does five things, split it.