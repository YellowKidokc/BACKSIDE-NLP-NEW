# MDA Deploy Packet Finish Status

Checked: 2026-06-02
Location: `X:\WORKFLOWS\MDA-PUBLICATION\08_DEPLOY_READY\merged-styled-reader-20260601-175431`

## What Was Fixed

- Restored missing deploy-ready page:
  - Source: `X:\WORKFLOWS\MDA-PUBLICATION\06_HTML_BUILD\reader_combined\MDA-004-facts-framework.html`
  - Destination: `02-method-and-metrics\MDA-004-facts-framework.html`
- Rebuilt and replaced two warning pages with reader-mode versions:
  - `04-collapse-mechanisms\MDA-036-regulatory-impulse-1900.html`
  - `05-amish-and-case-studies\MDA-045-amish-control-group-THE-DATA.html`

## Current Packet State

- `01_LOSSLESS\articles`: 61 Markdown articles.
- `02_CLASSIFIED`: 61 classified Markdown articles.
- `03_SCORED\openai\article-reports`: 61 two-lane reports.
- `05_READING_LEVELS`: 61 Academic files, 60 Easy files.
- `06_HTML_BUILD\reader_combined`: 62 HTML files, including `index.html`.
- This deploy-ready packet: 63 HTML files after the MDA-004 patch, including:
  - 61 MDA article pages.
  - `00-entry-and-series-map\index.html`.
  - `00-entry-and-series-map\MDA-000-series-map.html`.

## Remaining Non-Clean Gates

1. Series-flow gate is not passed.
   - Report: `03_SCORED\series-flow\mda_series_flow_report.md`
   - Verdict: `review_required`
   - Handoff threshold: 0.35
   - Pass ratio: 0.6415
   - Required pass ratio: 0.8
   - Flagged handoffs: 19 of 53
   - This means the packet can be inspected, but should not be called canon-clean deploy-ready unless David explicitly waives the series-flow gate or the flagged transitions are repaired and rescored.

2. `MDA-045-amish-control-group-THE-DATA` is missing its Easy reading-level source.
   - Present: Academic file and term inventory.
   - Missing: `05_READING_LEVELS\MDA-045-amish-control-group-THE-DATA_EASY.md`
   - The HTML builder falls back to Standard text for Easy when Easy is missing, so the page exists, but the Easy tab is not a true Easy rewrite.

3. Original merge report had two warnings:
   - `MDA-036-regulatory-impulse-1900.html`: `missing_easy_panel`
   - `MDA-045-amish-control-group-THE-DATA.html`: `missing_easy_panel`
   - Both files have now been replaced with rebuilt reader-mode pages.
   - MDA-036 now has Easy: ready.
   - MDA-045 still has Easy: fallback because the Easy source Markdown is missing.

## Verdict

This X-drive packet is now mechanically complete enough for inspection: all 61 article pages are present in the deploy-ready folder. It is not yet a clean final deployment because the corpus-order gate remains `review_required` and one article lacks a true Easy version.
