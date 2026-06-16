# CODEX TASK: Generate wiring_spec.json for all stations with runner scripts

## Context

This repo (`D:\GitHub\BACKSIDE-NLP-NEW`) contains a Brain NLP pipeline with
~63 stations in `stations/`. Each station has a `pipeline.py` that follows a
13-section standard (SSS_v1). Section 07 is the processing step — currently
a passthrough stub in most stations.

Many stations have REAL processing scripts (Python files besides pipeline.py)
that contain the actual logic. These need to be connected to pipeline.py via
a `wiring_spec.json` file.

An automator script (`wire_section07.py`) reads wiring_spec.json files and
patches pipeline.py automatically. Your job: generate the wiring_spec.json
for every station that has runner scripts.

## What to do

For each station listed below:

1. Read ALL .py files in the station folder (except pipeline.py, pipeline_legacy.py)
2. Find the main entry point — look for:
   - A `run()` or `main()` function
   - A class with a clear `.process()`, `.run()`, `.embed()`, or similar method
   - A function that takes text/file input and returns results
3. Generate a `wiring_spec.json` following the schema below
4. Save it in the station folder: `stations/{station_name}/wiring_spec.json`

## Schema (see WIRING_SPEC_SCHEMA.md for full details)

```json
{
  "description": "One-line description of what this station does",
  "imports": ["import some_lib"],          // optional, module-level imports
  "init": {                                 // optional, for persistent clients
    "var_name": "client",
    "code": ["from runner import Client", "_client = Client(cfg['url'])"]
  },
  "process_code": [                         // required, runs inside try block
    "# Available: path, text, nlp_info, cfg, log, result",
    "# Available constants: STATION_ID, STATION_NAME, STATION_DESC",
    "output = some_function(text)",
    "result['data'] = {'key': output}",
    "log.info('Done: %s', path.name)"
  ]
}
```

## Rules

- `process_code` lines get indented 8 spaces (inside try block in process_one)
- `init.code` lines get indented 4 spaces (inside _get_{var_name} function)
- `text` variable contains the file contents as a string (auto-read)
- Set `result["data"]` with your output dict — this goes into the artifact JSON
- Don't include try/except — the automator wraps process_code automatically
- For errors, just let exceptions propagate (they get caught and logged)
- Import the runner module using a relative import: `from runner_name import func`
  (the station folder is on sys.path via HERE)
- If the runner needs config values not in the current config.json, note them
  in a comment but still generate the spec

## Reference Example

See `stations/sbert-embedder.station/wiring_spec.json` — this is the gold
standard. It wires InfinityClient from sbert_runner.py with lazy init.

## Stations to Process

Read the runner scripts in each of these stations and generate wiring_spec.json:

| Station folder | Runner file(s) to read |
|---|---|
| 7q-classifier.station | seven_q_core.py, seven_q_runner_refined.py, integration_pass_refined.py |
| 7q-engine.station | destroy.py, html_report.py, id_system.py (read all .py) |
| ai-portal-generator.station | generator.py |
| apologetic-pipeline.station | apologetics_pipeline.py |
| claim-extractor.station | extract.py, claims_7q_pass.py, export_excel.py |
| deberta-runner.station | deberta_runner.py |
| fruits-spirit-canon.station | fruits_coherence_engine.py, run_fruits_engine.py, station.py |
| hdbscan-cluster.station | cluster_runner.py |
| image-processor.station | image_classifier.py |
| master-equation-canon.station | station.py |
| mda-citation-spine.station | claim_inventory.py |
| operators-canon.station | station.py |
| paper-intelligence-suite.station | docker_entrypoint.py, fruit_dynamics.py |
| paper-proof-grader.station | expanded_report.py, formal_verification.py, fruits_of_spirit_bridge.py, run_axiom_7q_stations.py |
| postgres-sync.station | db_utils.py |
| trinity-canon.station | station.py |
| vault-rater-tsr100.station | lowe_scorer.py |
| whisper-transcribe.station | whisper_runner.py |
| youtube-fetch.station | transcript_puller.py, youtube_scraper.py |

## After Running

Once all wiring_spec.json files are generated, run:
```
python wire_section07.py scan    # verify specs are detected
python wire_section07.py wire --all   # patch all stations at once
```
