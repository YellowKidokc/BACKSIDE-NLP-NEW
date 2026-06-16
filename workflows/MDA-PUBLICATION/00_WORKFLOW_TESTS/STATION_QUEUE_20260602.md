# MDA Station Queue

Created: 2026-06-02

This is the working queue for testing and wiring the MDA workflow app one station at a time.

## Current Start

Start at:

`X:\WORKFLOWS\MDA-PUBLICATION\00_WORKFLOW_TESTS`

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File X:\WORKFLOWS\MDA-PUBLICATION\00_WORKFLOW_TESTS\test_mda_workflow.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File X:\WORKFLOWS\MDA-PUBLICATION\00_WORKFLOW_TESTS\sync_root_exports.ps1
```

## Root Export Rule

The judged surface is now:

`X:\WORKFLOWS\MDA-PUBLICATION\EXPORTS`

Use two command-line lanes:

- Lane A: repair/generate station outputs.
- Lane B: run harness, sync root exports, and judge `EXPORTS`.

If a station uses semantic names, bind them to `EXPORTS\EXPORT_LEXICON.md`.
Manifest-scoped outputs go in the judged export folders. Non-manifest extras are preserved under `EXPORTS\00_CONTROL\non_manifest`.

## Station Results From First Harness Run

PASS:

- `01_LOSSLESS`
- `02_CLASSIFIED`
- `06_HTML_BUILD`
- `08_DEPLOY_READY`

REVIEW:

- `03_SCORED\series-flow`
- `05_READING_LEVELS`

FAIL:

- `03_SCORED` two-lane report coverage

## Next Repair Queue

### 1. Repair `03_SCORED` report coverage

Break:

- Missing manifest report: `MDA-004-facts-framework_TWO_LANE_REPORT.md`
- Extra non-manifest report occupying the count: `MDA-000-series-map_TWO_LANE_REPORT.md`

Repair:

- Generate or recover the two-lane report for `MDA-004-facts-framework`.
- Keep `MDA-000-series-map` as a series-map report if useful, but do not count it as manifest article coverage.

Pass test:

- `03_SCORED` reports cover all 61 manifest articles.

### 2. Repair `05_READING_LEVELS` Easy coverage

Break:

- Missing Easy file: `MDA-045-amish-control-group-THE-DATA_EASY.md`

Repair:

- Generate Easy version from Standard + Academic + term inventory.
- Rebuild the single article HTML.
- Copy rebuilt page into deploy packet if this packet remains the active inspection packet.

Pass test:

- 61 Easy files.
- `MDA-045` reader HTML shows `Easy: ready`, not fallback.

### 3. Decide `series-flow`

Break:

- `order_verdict=review_required`
- pass ratio `0.6415`
- required `0.8`
- 19 flagged handoffs.

Repair choices:

- Repair transition sentences and rerun series-flow.
- Explicitly waive series-flow for inspection/deploy if David chooses the current order.

Pass test:

- `order_verdict=pass` or `order_verdict=waived`.

## App Rule

Do not wire a later station as final until the previous station is either:

- PASS
- REVIEW with explicit waiver
- FAIL with named repair action

This prevents false-green deploys.
