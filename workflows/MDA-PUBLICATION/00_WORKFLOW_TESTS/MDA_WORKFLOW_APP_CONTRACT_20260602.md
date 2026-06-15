# MDA Workflow App Contract

Created: 2026-06-02
Root: `X:\WORKFLOWS\MDA-PUBLICATION`

## Starting Point

Start at the workflow root:

`X:\WORKFLOWS\MDA-PUBLICATION`

Use `WORKFLOW.md` as the canonical spine and `MANIFEST.json` as the article source of truth.

Do not start by changing article content. Start by testing station contracts.

## Cue Decision

Best base cue:

`09_EXPORT_PACKET\09_PROMPTS_FOR_COLLABORATORS\PROMPT_PORTABLE_REPO_REWRITE.md`

Reason: it is the only cue that already thinks like an app. It has config, path aliases, stations, health checks, portability, and acceptance tests.

Merged cues:

- `PROMPT_NEXT_AI.md` becomes Operator Mode: what to run next and what to report.
- `PROMPT_PROOF_GATE.md` becomes Proof Gate: claim promotion, 7Q, evidence, assumptions, kill conditions.
- `PROMPT_READING_LEVELS.md` becomes Reading QA Gate: Easy/Academic drift, overclaim, definition coverage.
- `MDA_PORTABLE_REPO_MERMAID.md` becomes the architecture map.
- `WORKFLOW.md` remains the production station order and hard-gate authority.

## One-App Principle

The app is not seven separate workflows. It is one workflow with seven station families.

Every station must expose the same interface:

```text
Station:
Inputs:
Outputs:
Run command:
Pass test:
Fail signal:
Repair action:
Next station:
```

If a station cannot define those fields, it is not wired yet.

## Root Export Principle

All judged outputs sync to:

`X:\WORKFLOWS\MDA-PUBLICATION\EXPORTS`

Station folders are working surfaces. `EXPORTS` is the inspection and handoff surface.

Two command-line split:

- Lane A repairs or generates station outputs.
- Lane B runs the harness, syncs root `EXPORTS`, and judges readiness.

Semantic names must be tied to `EXPORTS\EXPORT_LEXICON.md`. Manifest-scoped article outputs stay in judged export folders; non-manifest extras such as `MDA-000-series-map` are preserved under `EXPORTS\00_CONTROL\non_manifest` so they do not poison manifest counts.

## Station Families

### 0. Health / Harness

Station: `00_WORKFLOW_TESTS`

Purpose: test current state before mutation.

Run command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File X:\WORKFLOWS\MDA-PUBLICATION\00_WORKFLOW_TESTS\test_mda_workflow.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File X:\WORKFLOWS\MDA-PUBLICATION\00_WORKFLOW_TESTS\sync_root_exports.ps1
```

Pass test:

- Manifest has 61 articles.
- Lossless has all 61 source Markdown files.
- Classified has all 61 source Markdown files in expected type buckets.
- Two-lane reports cover all 61 manifest articles.
- Reader HTML covers all 61 manifest articles.
- Deploy packet covers all 61 manifest articles.

Known fail/review signals:

- `series-flow` is `review_required`.
- `MDA-045-amish-control-group-THE-DATA_EASY.md` is missing.

### 1. Lossless Source

Station: `01_LOSSLESS`

Inputs:

- Original article Markdown sources.
- `MANIFEST.json`.

Outputs:

- `01_LOSSLESS\articles\*.md`
- duplicates/system docs separated away from canonical article set.

Pass test:

- One canonical Markdown file per manifest article.
- No missing `MDA-037` through `MDA-041`.
- No extra article-like duplicates in `articles`.

### 2. Classification

Station: `02_CLASSIFIED`

Inputs:

- `01_LOSSLESS\articles`
- manifest type/range rules.

Outputs:

- `02_CLASSIFIED\narrative`
- `02_CLASSIFIED\mechanism`
- `02_CLASSIFIED\mathematical`
- `02_CLASSIFIED\empirical`
- `02_CLASSIFIED\resolution`
- `02_CLASSIFIED\appendix`

Pass test:

- narrative = 19
- mechanism = 17
- mathematical = 5
- empirical = 8
- resolution = 5
- appendix = 7

### 3. Scoring / Series Flow

Station: `03_SCORED`

Inputs:

- `01_LOSSLESS\articles`
- paper intelligence outputs.
- two-lane reports.

Outputs:

- `03_SCORED\openai\article-reports`
- `03_SCORED\series-flow\mda_series_flow_report.md`
- updated `MANIFEST.json.series_flow`

Pass test:

- Two-lane reports cover all manifest articles.
- Series flow is `pass` or explicitly `waived`.

Current status:

- Two-lane reports: pass.
- Series flow: review required.

Export rule:

- Manifest-scoped reports sync to `EXPORTS\03_TWO_LANE_REPORTS`.
- Non-manifest reports sync to `EXPORTS\00_CONTROL\non_manifest`.

Decision rule:

- If we are testing wiring, proceed with `review_required` clearly marked.
- If we are publishing, either repair flagged transitions and rerun, or explicitly waive.

### 4. Proof / Math Gates

Stations:

- `04_PROOF_PACKET`
- `04_MATH_NLP_REVIEW`
- `04_EDIT_QUEUE`

Inputs:

- two-lane reports.
- pipeline analytics.
- citation maps.
- claims-needed maps.
- methodology/isomorphism appendix.
- math translation spans where present.

Outputs:

- promoted claim packets.
- citation-status CSVs.
- axiom/isomorphism maps.
- math NLP review rows.
- edit queue files for failed spans or claims.

Pass test:

- No public proof tab promotes a claim without claim status, evidence, assumptions, kill condition, and 7Q result.
- Math translations preserve equation structure.
- Unmapped symbols are marked, not invented.

Current status:

- Not fully wired. Treat Proof tabs as structural unless claims are actually promoted.

### 5. Reading Levels

Station: `05_READING_LEVELS`

Inputs:

- Standard Markdown article.
- term inventory.
- Academic pass.
- Easy pass.

Outputs:

- `{article}_ACADEMIC.md`
- `{article}_EASY.md`
- `{article}_TERM_INVENTORY.json`

Pass test:

- 61 Academic files.
- 61 Easy files.
- 61 term inventories.
- Easy lowers reading burden without changing thesis.
- Academic adds caveats without overclaiming.

Current status:

- Academic: 61.
- Easy: 60.
- Missing Easy: `MDA-045-amish-control-group-THE-DATA`.

### 6. HTML Build

Station: `06_HTML_BUILD`

Inputs:

- `01_LOSSLESS\articles`
- `05_READING_LEVELS`
- proof data when available.
- two-lane reports.

Outputs:

- `06_HTML_BUILD\reader_combined\*.html`

Pass test:

- all 61 manifest articles have HTML.
- reader mode controls exist: Easy, Standard, Academic, Proof.
- fallback is visible when Easy or Academic is missing.

Current status:

- Reader HTML coverage passes.
- `MDA-045` has Easy fallback because source Easy Markdown is missing.

### 7. Series Home / Deploy Packet

Stations:

- `07_SERIES_HOME`
- `08_DEPLOY_READY`
- `09_EXPORT_PACKET`

Inputs:

- reader HTML.
- proof packets.
- paper intelligence dashboard.
- methodology appendix.
- isomorphism explorer.
- black axiom snapshot.
- keyword graph overlay.

Outputs:

- deploy-ready HTML packet.
- export packet.
- series proof hub.

Pass test:

- all 61 article pages present.
- index and series map present.
- no stale `TEMPLATE:SLOT` when real packet data exists.
- black axiom snapshot dependency resolved.
- deploy packet has a current finish-status note.

Current status:

- Deploy packet article coverage passes.
- Publication lock is still held by series-flow review and missing MDA-045 Easy file.

## Test-Then-Wire Rule

Use this order for the shakedown:

1. Run `00_WORKFLOW_TESTS`.
2. Fix only mechanical wiring bugs first.
3. Generate or repair missing station output.
4. Rerun tests.
5. Wire the next station only after the previous station has a clear pass/review/fail state.
6. Do not reorder the full publication sequence until every station runs.

## App Shape

The eventual app should expose one screen with station cards:

```text
[Health] -> [Lossless] -> [Classified] -> [Scored/Flow] -> [Proof/Math] -> [Reading] -> [HTML] -> [Deploy]
```

Each card needs:

- status: PASS / REVIEW / FAIL / NOT WIRED
- counts
- latest artifact
- run button
- open folder button
- next repair action

The first real app command is not deploy. It is health check.

## Current Next Best Action

Generate the missing Easy file for:

`MDA-045-amish-control-group-THE-DATA`

Then rebuild:

```powershell
python X:\WORKFLOWS\MDA-PUBLICATION\05_HTML_BUILD\combine_mda_reader_html.py --one MDA-045-amish-control-group-THE-DATA.md
```

Then rerun:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File X:\WORKFLOWS\MDA-PUBLICATION\00_WORKFLOW_TESTS\test_mda_workflow.ps1
```

After that, decide whether to repair or waive series-flow.
