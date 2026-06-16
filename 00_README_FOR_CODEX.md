# Theophysics Brain — Codex Task Queue
**Updated: 2026-06-17 | POF 2828**

## Architecture Summary
- **stations/** — 63 processing stations (Python SSS_v1 template + runner scripts)
- **workflows/** — Multi-station workflow definitions with dependency chains
- **models/** — NLP model shells (M01-M16)
- **engines/** — Preference engine shells (P01-P07)
- **templates/** — 40+ Excel + 10+ HTML templates (input data + output formats)
- **orchestrator/** — Top-level orchestration scripts

## Codex Tasks — Execute in Order

### Task 1: Generate wiring_spec.json files
**Prompt:** `CODEX_WIRING_PROMPT.md`
**Schema:** `WIRING_SPEC_SCHEMA.md`
**Example:** `stations/sbert-embedder.station/wiring_spec.json`

Read each station's runner scripts, generate a wiring_spec.json that
describes how to import and call the runner from pipeline.py Section 07.
19 stations have runner scripts ready to wire.

After generating specs, David runs:
```
python wire_section07.py wire --all
```

### Task 2: Wire template references into configs
**Prompt:** `CODEX_TEMPLATE_WIRING_PROMPT.md`
**Registry:** `templates/TEMPLATE_REGISTRY.json`
**Map:** `stations/_shared/TEMPLATE_WIRING_MAP.md`

Add `templates` key to each station's config.json mapping input/output
templates. Add `TEMPLATES = _resolve("15_TEMPLATES", "templates")`
to pipeline.py Section 01 for stations with template dependencies.

### Task 3 (next): Classification station + workflow tracker
**Prompt:** `CODEX_CLASSIFY_AND_TRACKER_PROMPT.md`

Two pieces:
- Part A: Write `classify_runner.py` for classify-documents station — reads
  a paper, classifies across 7 dimensions (doc_type, tags, spine mappings,
  dependencies, reading level), outputs classification artifact JSON.
- Part B: Write `tracker.py` in orchestrator/ — creates traveler JSONs that
  follow papers through the pipeline, aggregates into PIPELINE_TRACKER.xlsx.

### Task 4 (future): Write processing logic for stations without runners
~40 stations have no runner scripts at all. These need actual processing
logic written. This is a bigger task — each station does something different.
Not yet prompted.

### DEPRECATED — Do NOT use
- `PHASE2_CODEX_PROMPT.md` — Older approach that reads pipeline_legacy.py.
  Superseded by Task 1 (reads actual runner scripts instead of legacy stubs).

## Key Rules
- Station = one action. Workflow = many stations in order.
- Every pipeline.py follows SSS_v1 (13 sections). Only 06 and 07 change per station.
- Standard: `stations/_shared/SSS_v1_STANDARD.md` and `SSS_TEMPLATE_v1.py`
- Templates resolve via `_resolve("15_TEMPLATES", "templates")` for NAS/repo portability
- Station identity in config.json: station_id, station_name, station_type
- Runner scripts live alongside pipeline.py in the station folder
- Config.json holds all station settings — don't hardcode paths in Python

## Wire Automator
`wire_section07.py` at repo root:
- `python wire_section07.py scan` — show all station status (stub/wired/spec)
- `python wire_section07.py wire --station X` — wire one station
- `python wire_section07.py wire --all` — wire all stations with specs
- `python wire_section07.py wire --all --force` — re-wire even already-wired stations
