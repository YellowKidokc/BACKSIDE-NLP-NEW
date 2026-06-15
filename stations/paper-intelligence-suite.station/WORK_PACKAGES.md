# THEOPHYSICS PAPER INTELLIGENCE — Work Packages

**Status:** Foundation laid 2026-04-29 by Claude (Opus 4.7). Two to three agents can now pick up the remaining packages in parallel without stepping on each other.

**Goal:** Expand the existing 12-layer pipeline so it produces a unified `ProofExplorerSnapshot` per paper — covering David's full structural-peer-review spec — and ship it through (a) Excel, (b) JSON for the front-end, (c) HTML scorecard, (d) a web intake page.

---

## What's already done

- **Pipeline engine** — 12 modules, master orchestrator, multiple completed runs in `OUTPUT/`. Don't rebuild.
- **`lib/snapshot_schema.py`** — master Pydantic-style dataclass schema. Single source of truth for snapshot shape. Every package targets this.
- **`04_OPENAI_7Q/prompts/`** — 10 single-purpose prompt files matching the schema's missing sections. Each has SYSTEM/USER/EXPECTED_SHAPE and a `run()` function.
- **`04_OPENAI_7Q/prompts/_runner.py`** — generic OpenAI caller + `run_all()` that fans out across all 10 prompts.
- **`04_OPENAI_7Q/prompts/_README.md`** — house style for adding new prompts.

## What's NOT done (the work packages)

---

## Package A — Orchestrator integration ✅ DONE

**Owner:** Opus-B (this session, 2026-04-29)
**Depends on:** nothing (the prompts and schema are in place)
**Estimated effort:** 30 min

Wire the 10 new prompts into the existing pipeline.

1. In `00_ORCHESTRATOR/run_pipeline.py`, add a new layer (suggest L13 or extend L4) that calls `prompts.run_all(content, client)`.
2. Merge the result into a `ProofExplorerSnapshot` instance per paper.
3. Existing layer outputs (L1-L10) pour into `snapshot.pipeline_metrics` as a flat dict.
4. Save the snapshot as JSON next to the existing run output, filename `<paper_id>_snapshot.json`.

**Acceptance criteria:**
- Running `python 00_ORCHESTRATOR/run_pipeline.py --paper <some_paper.md>` produces both the existing Excel row AND a new `<paper_id>_snapshot.json` matching the schema.
- If `OPENAI_API_KEY` is not set, the new layer skips gracefully (status `skipped`, snapshot still emitted with empty section values).

**Hint:** Steal the layer-skip pattern from the existing L4 handling.

**Implementation summary:**
- New `lib/snapshot_merge.py` with `build_snapshot()` and
  `merge_sections_into_snapshot()`. Drops prompt-extra fields like
  `ai_confidence` (on AssumptionStack) and `justifications` (on
  CoherenceScore) that aren't in the schema.
- `analyze_paper()` gained `snapshot_dir` and `identity_overrides`
  kwargs. L13 block runs `prompts.run_all()` only when `--openai` is
  passed AND `OPENAI_API_KEY` is set; otherwise marks `_layer_status['L13']`
  as `skipped`. Snapshot is always written.
- `analyze_series()` writes per-paper snapshots into
  `<out_dir>/snapshots/<paper_id>_snapshot.json` and seeds
  `snapshot.identity.series` from the folder name.
- Verified end-to-end on `OUTPUT/_test_tiny_paper.md` without API key:
  L1-L10 ran, L13 skipped, snapshot JSON emitted with empty section
  defaults and a fully populated `pipeline_metrics`.

**Notes for downstream packages (B/C/D):**
- L13 only fires with `--openai`; without the flag, the snapshot is
  still produced (just empty sections). B/C/D can rely on the JSON
  always being present.
- `snapshot.identity` has `series` set in series mode; everything else
  starts blank. Package D's web intake form should pass
  `identity_overrides={"title": ..., "author": ..., "domain": ...}`
  through to `analyze_paper`.
- `snapshot.thesis` is *not yet populated by any prompt*. If Package
  C's HTML report wants a one-liner thesis, either pull it from
  `pipeline_metrics['L5_key_sentence']` as a fallback or add an 11th
  prompt (`thesis_extractor.py`) — easy follow-on.
- `coherence_score` returns a `justifications` dict the schema doesn't
  carry. Currently dropped on merge; if useful for the report, add a
  `justifications: dict` field to `CoherenceScore` and the merge
  picks it up automatically.

---

## Package B — Excel writer expansion

**Owner:** unclaimed
**Depends on:** Package A (or coordinate — A and B can run in parallel if you agree on column naming first)
**Estimated effort:** 45 min

The Excel SUMMARY sheet currently has `L1_*`, `L2_*`, `L3_*`, ... columns. Expand to include the new schema sections.

1. For SCALAR fields (e.g., `coherence.review_readiness`), add one column: `L13_coherence_review_readiness`.
2. For LIST fields with a small upper bound (e.g., `kill_conditions`, `claim_inventory`), flatten with index prefix:
   - `L13_claim_01_text`, `L13_claim_01_type`, `L13_claim_01_importance`, ...
   - Cap at 12 claims, 10 equations, 10 kill conditions, 12 evidence entries.
3. For LIST fields where order doesn't matter (e.g., assumptions categories), join with `; ` into one cell per category.
4. Add a new sheet **PEER_REVIEW** mirroring the structure for readability — one row per paper, columns grouped by section.

**Acceptance criteria:**
- Existing Excel columns unchanged.
- New columns populated from the snapshot's new sections.
- A 5-paper test run produces a valid `.xlsx` that opens in Excel without warnings.

---

## Package C — HTML report upgrade

**Owner:** Claude (Opus 4.7) — claimed 2026-04-29
**Status:** ✅ DONE 2026-04-29 (awaiting cross-agent QA per coordination protocol)
**Depends on:** Package A
**Estimated effort:** 2 hours

**Implementation notes (for the QA agent):**
- `11_HTML_REPORT/generate_report.py` is now snapshot-aware: detects `pipeline_metrics + claim_inventory/coherence/identity` and falls back to legacy flat-row rendering otherwise. No regression for existing pipeline output.
- The 8 peer-review tabs sit between the key-metrics grid and the existing Fruits/Emotions/Master-Equation sections, in a single in-page tabbed component (`.pr-tabs` + `.pr-panels`). One panel visible at a time; click-to-switch via `prSwitch()`.
- Each tab body is rendered by `_tab_*()` helpers — see top of file. Empty sections render `"Not extracted — confidence low"` placeholder instead of a blank panel.
- Coherence rubric (8 metrics) shown as small bars below the tab strip, with `coherence.review_readiness` surfaced as a headline metric card at the top of the dashboard (gold/green/red threshold).
- Quick Actions strip with **Download JSON** appears only when a snapshot is detected; href = `<paper_id>_snapshot.json` (matches Package A's filename convention).
- All new CSS uses existing CSS variables — no new colors introduced.
- Smoke artifacts: `11_HTML_REPORT/_test_fixture.py` builds two fixtures (one fully populated FP-005, one empty); `_test_output/` holds rendered HTML for visual review. Tag-balance check passes (div/table/tr/td/span all balanced).
- One known cosmetic limitation: when run on legacy flat rows, `prSwitch()` is still inlined but harmless (no `.pr-tab` elements exist to target).

Update `11_HTML_REPORT/generate_report.py` to render the new sections as 8 peer-review tabs in the existing dark/gold aesthetic.

The reference target is `\\YellowkidNas\desktop\faiththruphysics.com\proof-explorer\fp-005-enhanced.html` (also copied to `D:\GitHub\Treaties\snapshots\fp-005-enhanced.html`). Match its structure:

- Top: existing 7-layer verification strip (Axioms / 7Q / Decision Tree / Swap Test / CKG / Fruits / Iron Chain). Keep as-is — reads from existing pipeline metrics.
- Middle: NEW — 8 peer-review tabs from the snapshot's new sections:
  1. Claims (table from `claim_inventory`)
  2. Equations (table from `equations`)
  3. Assumptions (categorized lists from `assumptions`)
  4. Evidence (table from `evidence_map`)
  5. Falsifiability (table from `kill_conditions`)
  6. Comparison (table from `physics_comparison`)
  7. Weak Points (`overstatement.overstated_passages` + `revision.weakest_part`)
  8. Revision Plan (`revision.must_fix_before_publication` + `best_next_test`)
- Right sidebar: existing metadata + add `coherence.review_readiness` as the headline score.
- Existing "Quick Actions" bar gets a new button: **Download JSON** (links to the snapshot JSON).

**Acceptance criteria:**
- Renders against a sample snapshot JSON without breakage.
- Aesthetic matches existing Theophysics dark/gold (use existing CSS variables, don't introduce new colors).
- Empty sections render as "Not extracted — confidence low" rather than crashing.

---

## Package D — Web intake wrapper

**Owner:** Opus-B (in progress, 2026-04-29)
**Depends on:** Package A (otherwise the form runs but produces only existing-layer output)
**Estimated effort:** 1 hour

New folder: `13_WEB_INTAKE/`. A small FastAPI app that wraps the orchestrator.

1. `13_WEB_INTAKE/app.py` — FastAPI with three routes:
   - `GET /` — intake form (Jinja template)
   - `POST /submit` — accept name, paper title, domain, paper content (text or PDF upload)
   - `GET /report/<paper_id>` — serve the generated HTML report
2. `13_WEB_INTAKE/templates/intake.html` — form with: Author Name (text), Paper Title (text), Domain (dropdown), Paper Content (textarea OR file upload).
3. Domain dropdown options:
   - Theophysics
   - Cosmology
   - Quantum Mechanics
   - Thermodynamics
   - Information Theory
   - Consciousness
   - Theology / Physics Bridge
   - Philosophy
   - Other
4. On submit:
   - Save paper to `13_WEB_INTAKE/uploads/<paper_id>.md`
   - Subprocess: `python 00_ORCHESTRATOR/run_pipeline.py --paper <path>`
   - Redirect to `/report/<paper_id>` once complete (or show a progress page if pipeline >30s).
5. `13_WEB_INTAKE/run.bat` — `uvicorn app:app --host 0.0.0.0 --port 8088`.

**Acceptance criteria:**
- Submitting a paper through the form produces the same output as running the CLI pipeline.
- Form validates required fields client-side.
- Works locally; deferred to v2: Cloudflare Tunnel exposure.

---

## Package E — Validation pass on David's papers

**Owner:** unclaimed (likely David himself or a quality-check agent)
**Depends on:** A, B, C all complete
**Estimated effort:** 1-2 hours review time

Run the full upgraded pipeline against 5-10 of David's papers and compare AI output against David's own intuitions. Goal: tighten prompts where the engine disagrees with him.

1. Pick a mix: one formal paper (e.g., `FP-005`), one framework paper (`THEOPHYSICS_MASTER_PAPER.md`), one philosophical (a Convergence article), one with weak math, one already known to be strong.
2. For each, capture: does `claim_inventory` match what David would list? Does `kill_conditions` get the real vulnerabilities? Does `coherence_score` track David's own grading?
3. Where the engine drifts, edit the relevant prompt in `04_OPENAI_7Q/prompts/<section>.py` and re-run.
4. Document drift patterns in `04_OPENAI_7Q/prompts/CALIBRATION_NOTES.md`.

**Acceptance criteria:**
- 5+ papers evaluated.
- Calibration notes file checked in with concrete prompt deltas suggested.
- David has signed off on the rubric for at least one paper.

---

## Optional / Later

### Package F — Migrate from OpenAI to local
Once the prompts produce good output on OpenAI, the system migrates to local Ollama via `lib/ollama_client.py` (already exists in Treaties — could be ported here). Same prompt strings, different transport. Defer until Packages A-E are stable.

### Package G — Cloudflare deployment
Front-end on Cloudflare Pages. Submission API on Cloudflare Workers. Tunnel to David's mini PC for the heavy LLM calls. Defer until pipeline is stable AND the public-vs-private architecture decision is made.

### Package H — Theophysics overlay layers
The optional `TheophysicsOverlay` block in the schema (Decision Tree Q0-Q12, Swap Test, Fruits Scorer 5-dimension, Spine Mappings) is currently empty. If desired, write parallel prompt files in `04_OPENAI_7Q/prompts/theophysics/` for these. Defer — the universal peer-review surface is higher leverage right now.

---

## Coordination protocol

- **Claim a package** by setting `Owner:` to your name in the section above and committing.
- **Do not edit `lib/snapshot_schema.py`** without explicitly noting it in your commit AND telling the other active agents (it's the contract everything else depends on).
- **Adding a new prompt** = follow `04_OPENAI_7Q/prompts/_README.md` style + register in `_runner.py`'s `_import_prompt_modules()`.
- **Cross-agent QA**: when an agent finishes a package, the other agent reviews before David sees it. Catches stupid bugs and reduces David's review burden.

## Smoke test (run this first, before claiming a package)

```bash
cd T:\THEOPHYSICS_PAPER_INTELLIGENCE
python -c "from lib.snapshot_schema import ProofExplorerSnapshot; s = ProofExplorerSnapshot(); print(s.to_dict().keys())"
```

If that prints the section names, your environment is ready. Then run the prompt smoke test:

```bash
python 04_OPENAI_7Q/prompts_smoketest.py "path/to/short/paper.md"
```

(See `04_OPENAI_7Q/prompts_smoketest.py` — written alongside this doc.)

---

**Authored:** Claude (Opus 4.7), this session
**For:** David Lowe + 2-3 collaborating agents
**Last updated:** 2026-04-29
