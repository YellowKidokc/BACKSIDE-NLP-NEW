# Axiom + 7Q Station Status - 2026-05-18

Status: station runner works and now writes Excel review output.

## What Was Tested

Command:

```powershell
python X:\paper-proof-grader\run_axiom_7q_stations.py
```

Latest output:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260518_024929
```

Generated:

- `batch-index.md`
- `batch-index.json`
- `axiom-7q-review.xlsx`
- per-paper `axiom-7q-stations.md`
- per-paper `axiom-7q-stations.json`

## Excel Review Workbook

Workbook:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260518_024929\axiom-7q-review.xlsx
```

Sheets:

- `Batch Summary`
- `Claim Review`
- `Axiom Rules`

The `Claim Review` sheet has one row per claim with:

- paper id
- claim index
- section
- 7Q forward score
- reverse verdict
- weakness flags
- matched axiom/concept node ids
- matched axiom/concept labels
- matched terms
- claim text
- blank review note column for human scoring

## Current Finding

The station is picking plausible coarse axiom/concept buckets:

- RCH maps heavily to `model_coupling`, `information_substrate`,
  `experiment_protocol`, and `truth_ground`.
- QRNG/MVE maps to `model_coupling`, `experiment_protocol`,
  `entropy_thermo`, `falsifiability`, and `observer_actualization`.
- Fourfold Truth maps mostly to `truth_ground`.
- Turtles/Terminal Node maps to `master_equation`, `falsifiability`,
  `information_substrate`, and `truth_ground`.

This is directionally sensible for a smoke test.

## Important Boundary

The current axiom mapping is keyword-rule based. It is not yet wired to the
full canonical axiom registry.

This file was converted for inspection:

```text
X:\paper-proof-grader\REFERENCE\7H7hypothesis.converted.xlsx
```

Source:

```text
\\dlowenas\HPWorkstation\Desktop\EXCEL_FROM_TRANSFER\7H7hypothesis  (1).xlsb
```

It is a 7Q Deficit Closure Protocol workbook, not a canonical axiom registry.
Its sheets are:

- Dashboard
- Intake & Scoring
- Evidence Ledger
- Deficit Workbook
- Closure & Execution
- Gate & Proof

Use it later for deficit closure/gate scoring. Do not treat it as the axiom
source table.

## Next Fix

Wire the station to the real canonical axiom registry, likely one of:

```text
X:\knowledge-refinery\20_REGISTRIES
X:\knowledge-refinery\07_OBSIDIAN_EXPORT\axiom_registry\THEOPHYSICS_AXIOM_REGISTRY.xlsx
```

Then replace or supplement the current `AXIOM_RULES` keyword buckets with
registry-backed rows.

## OpenAI Verifier Wire

`run_axiom_7q_stations.py` now has an optional OpenAI verifier lane.

Default deterministic run, no API calls:

```text
python X:\paper-proof-grader\run_axiom_7q_stations.py
```

Bounded OpenAI smoke test:

```text
python X:\paper-proof-grader\run_axiom_7q_stations.py --openai --openai-model o3 --file-limit 1 --openai-limit 1
```

Safe sample launcher:

```text
X:\paper-proof-grader\RUN_AXIOM_7Q_OPENAI_SAMPLE.bat
```

Verified output:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260518_025841\axiom-7q-review.xlsx
```

The workbook `Claim Review` sheet now includes:

- `openai_enabled`
- `openai_model`
- `openai_candidate`
- `openai_confidence`
- `openai_axiom_ids`
- `openai_suggested_registry_terms`
- `openai_required_evidence`
- `openai_failure_conditions`
- `openai_rationale`
- `openai_error`

First verifier result tested successfully on RCH claim 1:

- candidate: `repair`
- confidence: `0.4`
- axiom ids: `truth_ground`, `information_substrate`

This is the correct posture for the station: it did not rubber-stamp the claim;
it accepted the likely axiom direction while requiring evidence and explicit
kill conditions.

## Four-Hypothesis OpenAI Spread Test

Ran:

```text
python X:\paper-proof-grader\run_axiom_7q_stations.py --openai --openai-limit 1
```

Latest verified spread output:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260518_030132\axiom-7q-review.xlsx
```

Result pattern:

- `01-RESONANT-COUPLING-HYPOTHESIS-RCH`: `repair`, confidence `0.4`,
  axiom ids `truth_ground`, `information_substrate`
- `02-REGISTERED-REPORT-MVE-QRNG`: `repair`, confidence `0.65`,
  axiom ids `information_substrate`, `experiment_protocol`, `model_coupling`
- `03-THE-FOURFOLD-NATURE-OF-TRUTH`: `repair`, confidence `0.4`,
  axiom ids `truth_ground`, `moral_conservation`
- `04-TURTLES-TERMINAL-NODE-HYPOTHESES`: `repair`, confidence `0.4`,
  axiom ids `model_coupling`

Prompt/schema correction made after the first spread test:

- `openai_axiom_ids` must now use only station-supplied ids.
- New column `openai_suggested_registry_terms` captures extra registry ideas
  without pretending they already exist as station nodes.
- Re-verified that the latest run produced no invalid invented axiom ids.

## O3 Verifier Run

David specified: use `o3` for this station, not `4o`.

Wrapper fix:

- `o3` rejects `temperature=0`, so the runner now omits the temperature
  parameter for OpenAI reasoning models whose names start with `o`.
- Default verifier model changed to `o3`.
- `RUN_AXIOM_7Q_OPENAI_SAMPLE.bat` now passes `--openai-model o3`.

Ran:

```text
python X:\paper-proof-grader\run_axiom_7q_stations.py --openai --openai-model o3 --openai-limit 1
```

Verified output:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260518_030500\axiom-7q-review.xlsx
```

O3 result pattern:

- `01-RESONANT-COUPLING-HYPOTHESIS-RCH`: `repair`, confidence `0.34`
- `02-REGISTERED-REPORT-MVE-QRNG`: `repair`, confidence `0.45`
- `03-THE-FOURFOLD-NATURE-OF-TRUTH`: `repair`, confidence `0.25`
- `04-TURTLES-TERMINAL-NODE-HYPOTHESES`: `repair`, confidence `0.27`

No invalid invented axiom ids were produced.

## HTML Report Layer

`run_axiom_7q_stations.py` now writes HTML automatically on every run.

Generated artifacts per station run:

- `index.html`: batch front door
- `{paper_id}\axiom-7q-stations.html`: per-paper claim review page
- existing JSON, Markdown, and Excel artifacts remain unchanged

Latest verified O3 + HTML run:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260518_031243\index.html
```

Verified HTML files:

- `index.html`
- `01-RESONANT-COUPLING-HYPOTHESIS-RCH\axiom-7q-stations.html`
- `02-REGISTERED-REPORT-MVE-QRNG\axiom-7q-stations.html`
- `03-THE-FOURFOLD-NATURE-OF-TRUTH\axiom-7q-stations.html`
- `04-TURTLES-TERMINAL-NODE-HYPOTHESES\axiom-7q-stations.html`

Sanity checks passed:

- Python compile passed.
- Deterministic no-API run generated HTML.
- O3 verifier run generated HTML.
- Batch `index.html` links resolve to the expected Excel, JSON, Markdown, and
  per-paper HTML files.
- Per-paper HTML includes deterministic 7Q, axiom hits, O3 verifier result,
  required evidence, and failure conditions.

## Sequence-Aware Axiom Wiring

David added the actual proof-explorer axiom outputs into:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260518_031243
```

Those source HTML files were copied into the repeatable reference lane:

```text
X:\paper-proof-grader\REFERENCE\axiom_sequence_sources
```

Files used:

- `axioms-layer-0-core.html`
- `axioms-layer-2-derived.html`
- `axioms-layer-3-extended.html`
- `axioms-closure.html`
- `fp-005.html`
- `fp-005-enhanced.html`

`run_axiom_7q_stations.py` now extracts visible axiom cards from those pages and
sorts matched axioms by real proof-explorer sequence:

- primitives before the numbered chain
- `Chain Position n/188` where present
- layer/card order where no chain position is present

Latest verified sequence-aware deterministic run:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260518_032155\index.html
```

Excel update:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260518_032155\axiom-7q-review.xlsx
```

New `Claim Review` columns:

- `axiom_sequences`
- `axiom_display_ids`
- `axiom_layers`
- `axiom_sources`

The `Chain Nodes` sheet now lists the extracted proof-explorer registry with:

- sequence
- chain position
- display id
- node id
- label
- source layer
- source file
- matched terms

Boundary:

The copied proof-explorer pages expose 29 visible sequence nodes, not the full
188-position chain. The station now honors the real sequence for those visible
nodes and keeps fallback buckets clearly labeled as `fallback`.

Terminology correction:

Do not call all 188 positions "axioms." The live structure is a small axiom
floor plus a larger chain of derivations, definitions, lemmas, theorems,
boundary conditions, identifications, equations, closure nodes, and terminal
nodes. Reports should say `chain nodes` when referring to the larger stack.

## Canonical Hierarchy Registry

David pasted the April 16, 2026 canonical hierarchy reference. It was encoded as:

```text
X:\paper-proof-grader\REFERENCE\canonical_chain_nodes.psv
```

The runner now loads this registry first, before the proof-explorer HTML scrape.

Canonical registry includes:

- `PRE-TRUTH`: Truth below the floor
- Level 0 primitives: Existence, Distinction, Information
- Level 1 presuppositions
- Iron Chain blocks
- Definitions
- Theorems
- Chain-proved derived claims
- Predictions / empirical claims
- Parallel theological postulates
- Strengthened clusters: `A81`, `A82-99`, `A110-114`
- New April nodes: `A189` through `A193`
- Soteriology spine: `T8.1`, `SOT-LIMIT`, `SOT-PHASE`
- `ME-GENERATOR`
- `FEB14-BOUNDARY`

Latest verified canonical-registry run:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260518_033356\index.html
```

Excel:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260518_033356\axiom-7q-review.xlsx
```

`Chain Nodes` now has:

- `node_type`
- `level`
- `family`
- `depends_on`
- `kill_condition`
- `source`

`Claim Review` now includes:

- `node_types`
- `node_families`
- `kill_conditions`

Boundary:

The ontology is now correct, but matching is still lexical. Broad nodes such as
Truth, Information, and Grace can match too often. The next refinement is
family-aware scoring so the station ranks strongest matches instead of listing
every plausible lexical match.

## Workflow Placement

The station is now wired into the knowledge-refinery workflow map.

Workflow entrypoint:

```text
X:\knowledge-refinery\10_STATIONS\12_axiom_promotion\WORKFLOW.md
```

Launchers:

```text
X:\knowledge-refinery\10_STATIONS\12_axiom_promotion\RUN_AXIOM_7Q_STATION.bat
X:\knowledge-refinery\10_STATIONS\12_axiom_promotion\RUN_AXIOM_7Q_O3_SAMPLE.bat
```

Latest output pointers:

```text
X:\knowledge-refinery\10_STATIONS\12_axiom_promotion\LATEST_OUTPUT_POINTER.txt
X:\paper-proof-grader\OUTPUT\station-runs\LATEST_AXIOM_7Q_RUN.txt
```

Verified launcher run:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260518_040621
```

Routing decision:

Keep the runtime in `X:\paper-proof-grader`. Use
`X:\knowledge-refinery\10_STATIONS\12_axiom_promotion` as the workflow
entrypoint, launcher, and map. This avoids duplicate runtimes and lets the next
station read one latest-output pointer.
