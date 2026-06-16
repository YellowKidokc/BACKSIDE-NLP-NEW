# Full Workflow Verification - 2026-05-13

## Result

PASS. The Brain/root workflow surface and FAP article manufacturing lane were verified end to end.

## What Was Checked

- Comms HTTP API worked through PowerShell against `https://comms.dlowehomelab.com`.
- Brain root was reachable at `X:\` and `\\dlowenas\brain`.
- Public article refinery latest status was PASS.
- FAP article manufacturing pipeline was rerun with the paper grader enabled.
- Root workflow healthcheck was rerun after repair and returned 0 failures / 0 warnings.

## Full FAP Canary

Input:

```text
\\dlowenas\HPWorkstation\Desktop\Hero Tempalte bigger\articles\03-first-quantum-state\gtq-03-first-quantum-state.html
```

Latest output:

```text
X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\output\20260513-104812_gtq-03-first-quantum-state
```

Manifest:

```text
X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\output\20260513-104812_gtq-03-first-quantum-state\job_manifest.json
```

Grader output:

```text
X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\graded\20260513-104812_gtq-03-first-quantum-state\paper-proof-grader-run-20260513_104815.json
```

Status file:

```text
X:\knowledge-refinery\05_WORKFLOW_RUNS\FAP_ARTICLE_PIPELINE_STATUS.md
```

Log:

```text
X:\knowledge-refinery\05_WORKFLOW_RUNS\workflow-packets\FolderAutomationPipeline\LOGS\fap_article_pipeline_20260513-104811.log
```

## Repair Made

`X:\session-handoff-drop\pipeline.py` was restored as a compatibility entrypoint that delegates to `pipeline_combined.py`. This fixed the root healthcheck contract without changing the live combined pipeline.

`X:\knowledge-refinery\05_WORKFLOW_RUNS\workflow-packets\README.md` now lists `FolderAutomationPipeline` as a promoted workflow packet.

## Final Healthcheck

```text
Report: \\dlowenas\brain\00_WORKFLOWS\WORKFLOWS_HEALTHCHECK_REPORT_20260513_104905.md
Failures: 0
Warnings: 0
```

## Axioms / 7-Series Follow-Up

After David flagged the missing Axioms and 7-series gates, FAP station generation was expanded and rerun.

Latest verification run:

```text
X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\output\20260513-110725_gtq-03-first-quantum-state\job_manifest.json
```

Queued station requests now include:

```text
X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\_queue\pending\20260513-110725_gtq-03-first-quantum-state\axiom_rigor_gate.request.md
X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\_queue\pending\20260513-110725_gtq-03-first-quantum-state\seven_q_forward.request.md
X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\_queue\pending\20260513-110725_gtq-03-first-quantum-state\seven_r_reverse.request.md
X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\_queue\pending\20260513-110725_gtq-03-first-quantum-state\seven_e_evidence.request.md
X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\_queue\pending\20260513-110725_gtq-03-first-quantum-state\decision_tree_swap_test.request.md
```

Interpretation:

```text
7Q = forward Q0-Q7 paper classification
7R = reverse/negation pass over central and subsidiary claims
7E = evidence pass across Q0-Q7 dimensions
```

## Full Workflow Folder (executable stations)

After David asked to turn the queued station requests into an executable end-to-end pipeline,
the `full_workflow/` folder was built. It activates the queued stations through local Ollama
(qwen2.5:3b on this box — mistral was not installed; qwen2.5:7b was CPU-only with a 4096
context window and could not finish a station inside 240s, so qwen2.5:3b is the default).

Layout:

```text
X:\knowledge-refinery\full_workflow\
  README.md
  scripts\
    station_runner.py        # reads _queue/pending/*.request.md, calls Ollama, writes results
    paper_scorecard.py       # grader + 13 stations -> scorecard.{json,md}
    production_html.py       # Kimi-staging-shape draft HTML (paired markers, PAGE_META, data-component)
    batch_orchestrator.py    # one-shot end-to-end + batch index sorted by combined score
  templates\
  output\<batch-id>\<jobid>\
    scorecard.json
    scorecard.md
    production-draft.html
    stations\<station>.result.{json,md}
  logs\
```

Click target:

```text
X:\knowledge-refinery\RUN_FULL_WORKFLOW.bat
```

## Kimi Boundary

The draft HTML follows `_KIMI-READ-FIRST/HTML-MARKING-STANDARD.md` (paired
`<!-- BEGIN/END:COMPONENT:{type}:{name} -->` markers, `data-component`/`data-name`
attributes, `PAGE_META` block with `marked_by: claude-code-forge`) but is never written
into `\\dlowenas\HPWorkstation\Desktop\Master HTMl\`. Kimi pulls from
`full_workflow/output/<batch>/<jobid>/production-draft.html` and promotes into
`K-Production-Ready/` per the MDA → GTQ → Cross-Domain sequence.

## Scoring

```text
station_score   = PASS*1.0 + REVIEW*0.5 - FAIL*1.0
grader_norm     = min(claims,30)/30*0.4 + min(eqs,20)/20*0.3
                + min(sections,12)/12*0.2 + min(words,5000)/5000*0.1
combined_score  = grader_norm * 10 + station_score
```

Higher combined = more production-ready. `batch_index.md` ranks the whole run.

## Smoke Result (gtq-03 canary)

13 stations executed by `station_runner.py` (qwen2.5:3b CPU, num_ctx=4096, num_predict=800):

```text
PASS=11  REVIEW=1 (master_equation_map)  FAIL=1 (contradiction_check)
combined_score = 20.5
runtime ~18.5 minutes
```

Output:

```text
X:\knowledge-refinery\full_workflow\output\batch-20260513-123005\
  20260513-110725_gtq-03-first-quantum-state\
    scorecard.json
    scorecard.md
    production-draft.html   (21 BEGIN/END:COMPONENT markers, PAGE_META present)
    stations\               (13 result.json + 13 result.md)
  batch_index.json
  batch_index.md
_LATEST.txt                  ("batch-20260513-123005")
```

Comms id 760 posted to `workflow-1`.

## Build Notes

- mistral is not installed locally — defaulted to qwen2.5:3b.
- qwen2.5:7b CPU-only with 4096 context could not return a token in 240s; not viable on this box without a GPU.
- qwen2.5:3b initially parroted my JSON example placeholder text as the output field; preamble was rewritten with a concrete filled example and an explicit do-not-echo instruction. Re-ran clean.
- One non-fatal cosmetic bug: `→` in the runner's `log.info` arg trips Python's cp1252 console encoder when stdout is piped. Logging swallows the error; the UTF-8 log file is correct.
