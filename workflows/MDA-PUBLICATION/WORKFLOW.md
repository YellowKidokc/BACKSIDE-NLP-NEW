# MDA Publication Workflow
## First Production Spine Instance
Created: 2026-05-30
Parent Architecture: `X:\Backside\workflows\BACKSIDE_WORKFLOW_SPINE_DRAFT_2026-05-22.md`

---

## Problem This Solves

Tonight's NLP run dropped MDA-037 through MDA-041 (the mathematical backbone).
306 files in input_md — duplicates, system docs, old naming, actual articles all mixed.
No defined process from "pipeline scored it" to "it's on the website."
This workflow fixes all three.

---

## The Rule

**Nothing moves forward without a manifest count match.**

Before any pipeline runs, the manifest says how many articles exist.
After staging, if `staged_count != manifest_count`, the run aborts.
This is the lossless guarantee. It's why MDA-037-041 won't get dropped again.

## Root Export Rule

All judged outputs sync to:

`X:\WORKFLOWS\MDA-PUBLICATION\EXPORTS`

Station folders are working surfaces. `EXPORTS` is the inspection and handoff surface.

Use two command-line lanes:

- Lane A repairs or generates station outputs.
- Lane B runs the harness, syncs root `EXPORTS`, and judges readiness.

Semantic names must be tied to `EXPORTS\EXPORT_LEXICON.md`. Manifest-scoped article outputs stay in judged export folders. Non-manifest extras such as `MDA-000-series-map` are preserved under `EXPORTS\00_CONTROL\non_manifest` so they do not occupy manifest article counts.

Sync command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File X:\WORKFLOWS\MDA-PUBLICATION\00_WORKFLOW_TESTS\sync_root_exports.ps1
```

---

## Folder Structure

```
X:\WORKFLOWS\MDA-PUBLICATION\
├── WORKFLOW.md                    ← this file
├── MANIFEST.json                  ← canonical article registry (source of truth)
├── EXPORTS\                       ← judged export / handoff surface
│
├── 01_LOSSLESS\                   ← preserved originals, one copy per article
│   ├── articles\                  ← clean MDs, canonical names only
│   ├── system-docs\               ← audits, specs, integrity reports
│   └── duplicates\                ← (1) (2) copies, old naming — kept but separated
│
├── 02_CLASSIFIED\                 ← articles sorted by content type (symlinks or copies)
│   ├── narrative\                 ← MDA-001–019: historical arc (Samuel→Jacob)
│   ├── mechanism\                 ← MDA-020–036: phase transition, entropy, cascade
│   ├── mathematical\              ← MDA-037–041: formal proofs, statistical spine
│   ├── empirical\                 ← MDA-042–049: Amish control group series
│   ├── resolution\                ← MDA-050–054: Korea, recovery, conclusion
│   └── appendix\                  ← MDA-900–906: reference material
│
├── 03_SCORED\                     ← pipeline output lands here
│   ├── local-nlp\                 ← readability, evidence, coherence, emotion
│   ├── openai\                    ← 7Q, claims, thesis, peer-review (needs key)
│   ├── scorecards\                ← HTML report per article
│   └── series-flow\              ← REQUIRED gate: corpus-level flow/ordering
│
├── 04_EDIT_QUEUE\                 ← articles flagged for work
│   ├── voice-fix\                 ← voice/tone issues
│   ├── evidence-gap\              ← missing citations or data
│   ├── structure-fix\             ← formatting, scaffold problems
│   └── stt-artifacts\             ← speech-to-text junk detected
│
├── 05_HTML_BUILD\                 ← markdown → site-ready HTML
│
└── 06_DEPLOY_READY\               ← final files for faiththruphysics.com
```

---

## Content Type Classification

| Type | Range | Count | Description | Website Section |
|------|-------|-------|-------------|-----------------|
| narrative | MDA-001–019 | 19 | Historical arc: five Lowe generations | Main series reading |
| mechanism | MDA-020–036 | 17 | Phase transition, entropy, cascade analysis | Deep dive / analysis |
| mathematical | MDA-037–041 | 5 | Biaxiosum, coherence metric, statistical spine | Academic / proofs |
| empirical | MDA-042–049 | 8 | Amish control group series | Evidence section |
| resolution | MDA-050–054 | 5 | Korea experiment, recovery, conclusion | Series conclusion |
| appendix | MDA-900–906 | 7 | Timeline, index, sample, reference | Appendices |
| **TOTAL** | | **61** | | |

Note: Tonight's pipeline scored 56. The 5 mathematical articles (037-041) were lost at staging.

---

## The Process (step by step)

### Step 1: Lossless Intake
- Source: wherever MDs currently live (input_md, Obsidian export, Codex output)
- Action: copy ONE canonical-named copy of each article to `01_LOSSLESS\articles\`
- Duplicates go to `01_LOSSLESS\duplicates\`
- System docs go to `01_LOSSLESS\system-docs\`
- Generate/update `MANIFEST.json` with article count, filenames, checksums
- **Gate: manifest_count must equal file count in articles\. No exceptions.**

### Step 2: Classify
- Read each article, assign content type from the table above
- Copy (not move) to appropriate `02_CLASSIFIED\{type}\` folder
- Update MANIFEST.json with classification
- This step can be automated: filename range → type mapping is deterministic

### Step 3: Score
- Run Paper Intelligence pipeline against `01_LOSSLESS\articles\`
- Local NLP first (no key needed): readability, evidence density, coherence, emotion
- OpenAI second (needs key): 7Q, claims, thesis, peer-review
- Output to `03_SCORED\{layer}\`
- Copy HTML scorecards to `03_SCORED\scorecards\`
- **Gate: scored_count must equal manifest_count**

#### Step 3b: Series Flow Gate (REQUIRED)
- Run `03_SCORED\series-flow\RUN.bat` (or `python run_series_flow.py`)
- Vectorizes all articles with sentence-transformers (local, no API key)
- Computes handoff scores between consecutive articles in manifest order
- Runs greedy optimal-ordering analysis and compares to manifest
- Writes outputs to `03_SCORED\series-flow\`:
  - `mda_series_flow_report.md` — human-readable report with flagged handoffs
  - `mda_handoff_scores.csv` — per-handoff scores
  - `mda_suggested_order.csv` — NLP-suggested reading order
  - `mda_series_flow_run.json` — machine-readable full dump
- **Mutates MANIFEST.json** with `series_flow` block (scored, verdict, stats)
- **HARD GATE:** Nothing enters 04_PROOF_PACKET, 05_READING_LEVELS, 06_HTML_BUILD,
  or 08_DEPLOY_READY unless `series_flow.series_flow_scored=true` AND
  (`series_flow.order_verdict=pass` OR `series_flow.order_verdict=waived`).
- To force waiver: `python run_series_flow.py --waive`

### Step 4: Triage → Edit Queue
- Review scorecards for flags
- Route flagged articles to appropriate `04_EDIT_QUEUE\{reason}\` subfolder
- Each queued article gets a `{filename}.fix-notes.md` with specific issues
- Articles that pass scoring go directly to Step 5

### Step 5: HTML Build
- Convert publication-ready MD → site HTML using MDA template
- Apply GTQ-HTML-REPAIR skill rules (55-rule standard)
- Output to `05_HTML_BUILD\`
- **Gate: visual QA on at least 3 articles per content type**

### Step 6: Deploy
- Copy QA-passed HTML to `06_DEPLOY_READY\`
- Push to faiththruphysics.com via Cloudflare Pages
- Update MANIFEST.json with deploy timestamp per article

---

## Spine Layer Mapping

| Workflow Step | Backside Spine Layer | Status |
|---------------|---------------------|--------|
| 01_LOSSLESS | Layer 01: Lossless | **Active — this run** |
| 02_CLASSIFIED | Layer 05: Claim (classification subset) | **Active — this run** |
| 03_SCORED | Layer 06: Rigor | **Active — tonight's NLP run** |
| 04_EDIT_QUEUE | (manual + skill-assisted) | Draft |
| 05_HTML_BUILD | Layer 09: Publication | Draft |
| 06_DEPLOY_READY | Layer 09: Publication (deploy) | Draft |

---

## Immediate Next Actions

1. Sort the 306 input_md files into 01_LOSSLESS (articles vs system-docs vs duplicates)
2. Recover MDA-037 through MDA-041 into the clean article set
3. Rerun pipeline on the complete 61-article set
4. Set OpenAI key and run with `--openai` for full scoring
5. Build triage report from scorecards → populate edit queue

6. Run Reading Level Generator on edited articles → populate 05_HTML_BUILD with three versions per article

---

## Reading Level Generator (added 2026-05-30)

Location: `X:\WORKFLOWS\MDA-PUBLICATION\READING_LEVEL_GENERATOR\`

**Entry point:** `RUN.bat`

**Sequence:**
1. Takes Standard article (David's voice) from `01_LOSSLESS\articles\`
2. Pulls paper-grade.json from Codex's MTL run (auto-detected or manual path)
3. **Stage 1 → Academic:** Enriches terms, adds citation markers, formalizes equations, classifies claims
4. Outputs `TERM_INVENTORY.json` — every hard term with definition
5. **Stage 2 → Easy:** Consumes term inventory, builds analogies, simplifies to 8th grade
6. Output lands in `{article}_reading_levels\` folder

**The key dependency:** Academic enrichment feeds Easy simplification. The Academic pass identifies what needs explaining. The Easy pass uses that inventory to build analogies. Run them in order — never Easy without Academic first.

**Without API key:** Outputs prompt .txt files for manual paste into any LLM.
**With API key:** `RUN.bat article.md --api openai` or `--api anthropic`

**Files:**
- `STAGE1_ACADEMIC.txt` — Academic generation prompt
- `STAGE2_EASY.txt` — Easy generation prompt
- `generate_reading_levels.py` — orchestrator script
- `RUN.bat` — batch entry point

**Fits the three-tier HTML architecture:**
- Standard (free) = David's original voice
- Easy (free) = automated from term inventory
- Academic (paid) = formalized with claims overlay

---

## Proof / Citation / Series-Home Work Order (added 2026-05-30)

This section supersedes the older six-step shorthand where proof data, reading levels, HTML build, and deploy were collapsed together. The workflow now has explicit stations for proof packets and the Proof Explorer series home.

### Canonical Station Order

1. `01_LOSSLESS` - preserve one canonical article copy, with manifest count match.
2. `02_CLASSIFIED` - sort articles into narrative, mechanism, mathematical, empirical, resolution, appendix.
3. `03_SCORED` - paper intelligence, local NLP, OpenAI/o3 grader outputs, HTML scorecards.
3b. `03_SCORED/series-flow` - **REQUIRED** corpus-level vectorization + ordering gate. Blocks all downstream stages.
4. `04_EDIT_QUEUE` - voice, evidence, structure, and STT-artifact repair queues.
5. `04_PROOF_PACKET` - build proof/citation/axiom/isomorphism packets from existing outputs.
6. `04_MATH_NLP_REVIEW` - review Math Translation Layer spans before reading levels or HTML.
7. `05_READING_LEVELS` - generate Standard / Easy / Academic variants after proof packets and math review exist.
8. `06_HTML_BUILD` - build article HTML with Easy / Standard / Academic / Proof tabs.
9. `07_SERIES_HOME` - populate `proof-explorer-index.html` as the series proof hub.
10. `08_DEPLOY_READY` - deploy-ready files only after article tabs and series home pass QA.

### Step 5 Inputs: Proof Packet Build

Do not re-grade if the needed output already exists. The proof packet station consumes:

- `\\dlowenas\HPWorkstation\Desktop\Moral_Decay_of_America\90_Data\citation_map.csv`
- `\\dlowenas\HPWorkstation\Desktop\Moral_Decay_of_America\90_Data\claims_needed.csv`
- `X:\apps\paper-intelligence-suite-python\OUTPUT\mda_full_local_nlp_20260530_011839\grader\paper_intelligence_rows_*.json`
- per-article paper-intelligence snapshots when populated
- o3 `scores_*.json` and `integration_*.md` packets when present
- vector evidence appendices when present
- `\\dlowenas\HPWorkstation\Desktop\Moral_Decay_of_America\02_Formal_Papers\MDA_Methodology_and_Isomorphism_Appendix.md`
- Isomorphism Explorer: `\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready\subdomains\isomorphism\`
- black axiom snapshot page/artifact once restored
- `paper-intelligence.html` / scorecard outputs for reader-facing grade panels

### Step 5 Outputs: Proof Packet Build

Write these to `04_PROOF_PACKET\`:

- `article-packets\{article}.proof-packet.json`
- `article-packets\{article}.proof-fragment.html`
- `citation-resolution\{article}.citation-status.csv`
- `axiom-map\{article}.axiom-map.json`
- `isomorphism-map\{article}.isomorphism-map.json`
- `series-packets\mda-series-grade.json`
- `series-packets\mda-proof-packet.html`

Gate: every promoted claim must have `claim_level`, `claim_status`, `source_status`, `citation_quality`, `methodology_dependency`, `proof_destination`, and a kill condition or explicit "not yet falsifiable" flag. Source-map rows must not be labeled as primary citations.

### Step 5b: Math NLP Review Gate

This gate exists for the Math Translation Layer. It is not a proof engine and not a rewrite engine. Its job is to verify that every translated math span preserves the original equation structure while making the terms readable to a layman.

Inputs:

- Math Translation Layer JSON or snapshot field `math_translation_layer.translated_spans`
- original Markdown/HTML equation span
- same-structure word equation emitted by MTL
- plain-language explanation emitted by MTL or reviewed Easy Math text
- dictionary/canon version used for the translation

For every translated span, write a row to `04_MATH_NLP_REVIEW\math_nlp_review.csv` with:

- `article_id`
- `source_span_id`
- `original_equation`
- `word_equation`
- `plain_explanation`
- `structure_callouts`
- `structure_preserved` (`pass`, `fail`, `needs_review`)
- `layman_terms_clear` (`pass`, `fail`, `needs_review`)
- `added_meaning_risk` (`none`, `low`, `high`)
- `dictionary_coverage`
- `review_notes`

Hard gate:

- The word equation must keep the same operator/order/term structure as the original equation.
- Symbols may be translated only from reviewed dictionary/canon entries or marked `unmapped`.
- Plain-language explanation may simplify, but must not add a new claim, causal mechanism, certainty level, or theological/math conclusion not present in the source/dictionary/proof packet.
- The explanation must refer back to the visible equation structure at least once, and preferably two or three times for larger equations.
- `structure_callouts` must identify the load-bearing parts of the equation. For small equations, call out the one or two decisive parts. For large equations, call out the five or so parts that control interpretation, such as the term that multiplies everything, the denominator that suppresses output, the threshold term, the exponent, the derivative, or the conserved/remainder term.
- The callouts must explain why those structural parts matter: multiplication means collapse/propagation through all factors; division means suppression or normalization; exponent/threshold terms mean nonlinear transition; derivative terms mean rate of change; source/sink terms mean what adds or removes from the system.
- Any span with `structure_preserved=fail`, `added_meaning_risk=high`, or unreviewed invented wording goes to `04_EDIT_QUEUE\math-layer\` and cannot enter `05_READING_LEVELS` or `06_HTML_BUILD`.
- HTML output must expose all three layers where applicable: original equation, same-structure word equation, and simple explanation.

### HTML / Proof Tab Scripts

The article HTML station must include these scripts where applicable:

- `mda_reader_tabs_v2_patch.py` - Easy / Standard / Academic / Proof tab structure
- `mda_nav_v2_patch.py` - MDA navigation and previous/next links
- `mda_proof_layer_inject.py` - inject vetted proof panels
- `html_rewrite_variation_engine.py` - produce review/proof/citation suggestion blocks
- `html_rewrite_folder_runner.py` - batch folder processing and processed-source movement
- `source_methods_resolver.py` - citation/source resolution where registry input is present
- `openai_vectorize_mda_packet.py` - temporary vector retrieval for evidence packets

### Series Home / Proof Explorer

`proof-explorer-index.html` is the series/proof-system hub, not the public landing homepage.

Working copy:

`\\dlowenas\HPWorkstation\Desktop\Master HTMl\proof-explorer-index.html`

Deploy copy:

`\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready\subdomains\proof-explorer-index.html`

This page must aggregate or link:

- MDA series proof packet
- article proof packets
- domain pages from `\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready\subdomains\`
- Paper Intelligence dashboard and scorecards
- methodology appendix
- isomorphism explorer
- axiom architecture and the black axiom snapshot page
- evidence, claims, falsification, graph, and domain maps

Gate: no `TEMPLATE:SLOT` or generator prompt should remain stale where packet data exists.

### Black Axiom Page Dependency

The Proof Explorer template references `00_GENESIS-TO-QUANTUM-black-axiom-snapshot.html`. The workflow must treat that as a required axiom artifact. If the file is missing from `K-Production-Ready`, recover or regenerate it before final series-home QA.
