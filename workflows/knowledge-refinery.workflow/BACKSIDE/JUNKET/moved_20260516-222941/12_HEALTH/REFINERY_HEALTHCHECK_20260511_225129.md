# Knowledge Refinery Healthcheck

- Generated: 2026-05-11T22:51:29
- Root: `\\dlowenas\brain\knowledge-refinery`
- Failures: 0
- Warnings: 0

| Area | Check | Status | Detail |
|---|---|---|---|
| refinery | 00_INTAKE | OK | `\\dlowenas\brain\knowledge-refinery\00_INTAKE` |
| refinery | 01_CONVERSION | OK | `\\dlowenas\brain\knowledge-refinery\01_CONVERSION` |
| refinery | 02_NORMALIZATION | OK | `\\dlowenas\brain\knowledge-refinery\02_NORMALIZATION` |
| refinery | 03_ROUTING | OK | `\\dlowenas\brain\knowledge-refinery\03_ROUTING` |
| refinery | 04_MODEL_STATIONS | OK | `\\dlowenas\brain\knowledge-refinery\04_MODEL_STATIONS` |
| refinery | 05_WORKFLOW_RUNS | OK | `\\dlowenas\brain\knowledge-refinery\05_WORKFLOW_RUNS` |
| refinery | 06_HTML_REPORTS | OK | `\\dlowenas\brain\knowledge-refinery\06_HTML_REPORTS` |
| refinery | 07_OBSIDIAN_EXPORT | OK | `\\dlowenas\brain\knowledge-refinery\07_OBSIDIAN_EXPORT` |
| refinery | 08_ARCHIVE | OK | `\\dlowenas\brain\knowledge-refinery\08_ARCHIVE` |
| refinery | 09_MEMORY | OK | `\\dlowenas\brain\knowledge-refinery\09_MEMORY` |
| refinery | 10_PROMPTS | OK | `\\dlowenas\brain\knowledge-refinery\10_PROMPTS` |
| refinery | 11_CONFIG | OK | `\\dlowenas\brain\knowledge-refinery\11_CONFIG` |
| refinery | 12_HEALTH | OK | `\\dlowenas\brain\knowledge-refinery\12_HEALTH` |
| refinery | scripts | OK | `\\dlowenas\brain\knowledge-refinery\scripts` |
| config | station_registry.json | OK | `\\dlowenas\brain\knowledge-refinery\11_CONFIG\station_registry.json` |
| root_workflow | session-handoff-drop | OK | `\\dlowenas\brain\session-handoff-drop` |
| root_workflow | paper-proof-grader | OK | `\\dlowenas\brain\paper-proof-grader` |
| root_workflow | link-pull-drop | OK | `\\dlowenas\brain\link-pull-drop` |
| root_workflow | ai-portal-generator | OK | `\\dlowenas\brain\ai-portal-generator` |
| root_workflow | axioms | OK | `\\dlowenas\brain\axioms` |
| root_workflow | ollama | OK | `\\dlowenas\brain\ollama` |
| root_workflow | models | OK | `\\dlowenas\brain\models` |
| model_station | math_verify | OK | `\\dlowenas\brain\models\math_verify items=0` |
| model_station | claim_extract | OK | `\\dlowenas\brain\models\claim_extract items=1` |
| model_station | fact_verify | OK | `\\dlowenas\brain\models\fact_verify items=1` |
| model_station | contradiction_detect | OK | `\\dlowenas\brain\models\contradiction_detect items=1` |
| model_station | timeline_verify | OK | `\\dlowenas\brain\models\timeline_verify items=1` |
| model_station | paper_review | OK | `\\dlowenas\brain\models\paper_review items=0` |
| python | refinery_healthcheck.py | OK | `\\dlowenas\brain\knowledge-refinery\scripts\refinery_healthcheck.py` |
| service | Ollama | OK | `OK HTTP 200` |
| service | Qdrant | OK | `OK HTTP 200` |
| service | Infinity | OK | `OK HTTP 200` |
