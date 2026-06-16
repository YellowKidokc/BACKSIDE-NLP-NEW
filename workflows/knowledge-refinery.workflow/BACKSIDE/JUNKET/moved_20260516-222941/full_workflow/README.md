# Full Workflow — Paper to Production-Ready Draft

Single-command, end-to-end manufacturing line. Drop papers into FAP intake, run one batch script, get scored + sorted papers with full station outputs and Kimi-staging-shape HTML drafts.

## What it does

```text
intake (FAP)
  -> classified -> media-routed -> lossless -> vectorized
  -> graded (paper-proof-grader)
  -> axiom-mapped
  -> output  (manifest exists)
  -> stations executed via Ollama (axiom_rigor_gate, 7Q forward, 7R reverse, 7E evidence,
     decision_tree_swap_test, executive_summary, explain_it_simply, math_translation,
     contradiction_check, bible_reference_check, master_equation_map,
     axiom_derivation_review, post_summary)
  -> executable 7Q engine can fill Q0-Q7 markdown + HTML report panels
  -> per-paper scorecard.json + scorecard.md
  -> production-draft.html (Kimi-staging shape — NOT a final commit to Master HTMl)
  -> treaties-handoff.json (Treaties/proof-explorer snapshot input)
  -> batch index sorted by score
```

## Run it

```text
X:\knowledge-refinery\RUN_FULL_WORKFLOW.bat
```

Or programmatic:

```text
python X:\knowledge-refinery\full_workflow\scripts\batch_orchestrator.py
```

Options:

- `--intake <dir>` — override intake source (defaults to FAP intake folder)
- `--skip-fap` — assume papers already through FAP, only run stations + scorecard + HTML
- `--paper <slug>` — single paper instead of full batch
- `--no-html` — skip draft HTML render
- `--no-treaties` — skip Treaties/proof-explorer handoff package

## Folder layout

```text
full_workflow/
  scripts/
    station_runner.py        # Ollama executor — turns _queue/pending into _queue/completed
    paper_scorecard.py       # Per-paper rollup: grader stats + 13 station results
    production_html.py       # Kimi-staging-shape draft HTML renderer
    treaties_handoff.py      # Treaties/proof-explorer snapshot handoff builder
    batch_orchestrator.py    # One-shot: FAP -> stations -> scorecards -> HTML -> Treaties handoff -> batch index
  templates/
    station_prompts.json     # Per-station Ollama prompt overrides
    production_draft.html    # Kimi-shape skeleton with PAGE_META + component markers
  output/
    <batch-id>/
      <paper-slug>/
        scorecard.json
        scorecard.md
        production-draft.html
        treaties-handoff.json
        stations/<station>.result.json
      batch_index.md         # All papers sorted by score
      batch_index.json
  logs/
    full_workflow_<ts>.log
```

## Kimi boundary (hard line)

This workflow produces `production-draft.html` in the **draft staging shape** — paired
`<!-- BEGIN:COMPONENT:{type}:{name} -->` markers, `data-component` attrs, `PAGE_META`
block — but **never writes to `\\dlowenas\HPWorkstation\Desktop\Master HTMl\` directly**.
That tree is Kimi's authority (`_KIMI-READ-FIRST/HTML-MARKING-STANDARD.md` is law).

Drafts land here:

```text
X:\knowledge-refinery\full_workflow\output\<batch-id>\<paper-slug>\production-draft.html
```

For promotion to production, Kimi pulls from this folder and lands the cleaned version in
`K-Production-Ready/` per the MDA → GTQ → Cross-Domain sequence.

## Ollama dependency

Requires Ollama running locally with `mistral` pulled:

```text
ollama serve            (RUN_OLLAMA.bat starts it)
ollama pull mistral     (first-run only)
```

The orchestrator does a single health probe to `http://localhost:11434` and bails clean if
it can't reach the server. Each station call has a 180s timeout. 13 stations per paper at
~30-90s each = 7-20 minutes per paper. Plan accordingly.

## Multi-paper

Drop multiple files into the FAP intake folder. The orchestrator processes them
sequentially through FAP (the spine is single-threaded by design), then runs stations
per paper. Scorecards land in their own subfolder, and the batch index ranks all papers
in the run by combined score:

```text
batch_score = grader.weighted_score
            + station_pass_count * 1.0
            + station_review_count * 0.5
            - station_fail_count * 1.0
```

Highest score = most production-ready.

## What this is NOT

- Not a replacement for Kimi's production HTML — it's the draft stage.
- Not a replacement for human review on REVIEW/FAIL stations — those need a partner pass.
- Not autonomous publishing — output sits in `full_workflow/output/`, no auto-promote.
- Not the canonical 7Q source — the in-house source lives at `X:\knowledge-refinery\13_SOURCE_SYSTEMS\7Q`.

## Status convention

Each station returns `PASS` / `REVIEW` / `FAIL`. Scorecard surfaces:

```text
PASS    — Ollama is confident the station task succeeded with evidence
REVIEW  — partial; needs a partner (Codex/Opus/David) to confirm
FAIL    — station blocker; usually missing evidence or contradiction found
```

`FAIL` does not block downstream stations — they all run. That way one bad station
doesn't blackhole the whole paper. The scorecard tells you where to look.
