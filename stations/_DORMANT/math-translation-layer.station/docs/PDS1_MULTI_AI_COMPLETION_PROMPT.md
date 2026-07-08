# PDS-1 Paper-Grader Multi-AI Completion Prompt

Repository:

```text
D:\Github\Math-Translation-Layer
```

Canon output root:

```text
\\dlowenas\z obsidian\_ __THEOPHYSICS_CANON\THEOPHYSICS_RESEARCH_PROGRAM
```

Canon paper-grader Markdown lane:

```text
\\dlowenas\z obsidian\_ __THEOPHYSICS_CANON\THEOPHYSICS_RESEARCH_PROGRAM\06_ADVERSARIAL_LAYER\Paper_Grader_PDS1
```

Canon paper-grader heavy data lane:

```text
\\dlowenas\z obsidian\_ __THEOPHYSICS_CANON\THEOPHYSICS_RESEARCH_PROGRAM\__THEOPHYSICS_CANON_DATA\06_ADVERSARIAL_LAYER\Paper_Grader_PDS1
```

## Mission

Finish the PDS-1 paper-grader workflow by splitting implementation across four AI partners with non-overlapping write ownership.

PDS-1 is a paper defensibility standard, not a truth score. Scores are audit trails, not verdicts.

The completed snapshot must preserve this order:

```text
CLAIM_ARCH
-> EVIDENCE_CHAIN
-> KILL_ARCH
-> EQ_SEM
-> DOMAIN_BOUNDARY
-> REVIEWER_SEEDS
-> LEDGER_SCHEMA
-> OVERSTATE_PATTERN
-> BENCHMARK_ANCHOR
-> CROSS_DEP
-> EIGHT_GAPS
```

## Read First

Each partner must read:

```text
docs/PDS_1_DEFENSIBILITY_STANDARD.md
docs/PDS_1_STATION_MAP.md
docs/PDS_1_CODEX_ONLINE_PROMPT.md
pipeline/models/types.py
pipeline/run.py
pipeline/stations/common.py
pipeline/stations/station_00_intake.py
pipeline/stations/station_03_claims.py
pipeline/stations/station_05_evidence.py
pipeline/stations/station_06_7q_forward.py
pipeline/stations/station_07_7q_reverse.py
pipeline/stations/station_09_objections.py
pipeline/stations/station_13_manifest.py
pipeline/tests/test_foundation.py
pipeline/tests/test_adversarial.py
```

## Non-Negotiable Guardrails

- Preserve station IDs.
- Keep outputs deterministic and JSON-first.
- No API calls.
- No blended final truth score.
- Keep four score tracks separate:
  - `Academic_Readiness`
  - `Framework_Coherence`
  - `Public_Communication`
  - `Risk`
- Runtime outputs stay under ignored output folders.
- Markdown final outputs can be copied to the Canon lane only after verification.
- Heavy/generated data goes to the data mirror, not the Markdown folders.
- Do not treat the Master Equation as a law-level physical equation.
- Do not force-push.

## Partner A: Text Normalization + Structure

Ownership:

```text
pipeline/stations/station_01_text_normalization.py
pipeline/stations/station_02_structure_map.py
pipeline/tests/test_pds1_station_01_02.py
```

Coordinate carefully if editing:

```text
pipeline/run.py
pipeline/stations/__init__.py
pipeline/models/types.py
pipeline/stations/station_13_manifest.py
```

Implement Station `01`:

- Input: `00_intake.json` and original document copy.
- Output:
  - `01_normalized_text.md`
  - `01_normalized_text.json`
- Must preserve title, detected format, source hash, normalization warnings.
- Must remove obvious HTML markup while preserving mathematical/textual content.

Implement Station `02`:

- Input: `01_normalized_text.md`
- Output:
  - `02_structure_map.json`
  - `02_structure_map_human.md`
- Must identify headings, paragraphs, equation-looking blocks, citation-looking lines, tables if obvious.

Verification:

```bash
python -m pytest pipeline/tests/test_foundation.py pipeline/tests/test_pds1_station_01_02.py -v
python -m pipeline.run --input pipeline/tests/fixtures/sample-paper.html --stations 00,01,02,13
```

Done means:

- Station 01 and 02 files exist.
- Manifest records 01 and 02 when run.
- Tests pass.

## Partner B: Claim Typing

Ownership:

```text
pipeline/stations/station_04_claim_typing.py
pipeline/tests/test_pds1_station_04.py
```

Coordinate carefully if editing:

```text
pipeline/run.py
pipeline/stations/__init__.py
pipeline/models/types.py
pipeline/stations/station_13_manifest.py
```

Implement Station `04`:

- Input:
  - `03_claims.json`
  - optionally `02_structure_map.json` if present
- Output:
  - `04_claim_typing.json`
  - `04_claim_typing_human.md`

Each claim should get:

- `claim_uuid`
- `claim_type`
- `domain_badges`
- `overstatement_flags`
- `equation_semantics_needed`
- `evidence_requirement`
- `public_comm_risk`
- `recommended_next_station`

Heuristics:

- Mathematical/equation language -> equation semantics needed.
- Experimental/statistical claims -> evidence requirement high.
- Words like proves, impossible, always, never, definitive -> overstatement flag unless supported.
- Theology-only, physics-only, bridge, historical, methodological, and public-facing claims should be distinguishable.

Verification:

```bash
python -m pytest pipeline/tests/test_foundation.py pipeline/tests/test_adversarial.py pipeline/tests/test_pds1_station_04.py -v
python -m pipeline.run --input pipeline/tests/fixtures/sample-paper.html --stations 00,03,04,13
```

Done means:

- Station 04 writes JSON and human Markdown.
- Overstatement flags are tested.
- Domain badges are tested.

## Partner C: Formal Routing + Score/Readiness

Ownership:

```text
pipeline/stations/station_08_formal_routing.py
pipeline/stations/station_10_score_readiness.py
pipeline/tests/test_pds1_station_08_10.py
```

Coordinate carefully if editing:

```text
pipeline/run.py
pipeline/stations/__init__.py
pipeline/models/types.py
pipeline/stations/station_13_manifest.py
```

Implement Station `08` Formal Routing:

- Input:
  - `03_claims.json`
  - `04_claim_typing.json`
- Output:
  - `08_formal_targets.json`
  - `08_formal_targets_human.md`

Route claims to:

- `Lean`
- `Python/state-model`
- `Alloy/TLA-style spec`
- `Bridge-only / not formal yet`

Special note:

The no-drift Lean topology kernel is relevant for law-order/topology/signature claims. Do not route the Master Equation as a law-level equation.

Likely Lean dependency hints:

- no-drift topology
- canonical law order
- physical equation signature
- spiritual side signature
- approved alias normalization
- terminal asymmetry of Law 9 and Law 10

Implement Station `10` Score/Readiness:

- Input:
  - `03_claims.json`
  - `04_claim_typing.json`
  - `05_evidence.json`
  - `06_7q_forward.json`
  - `07_7q_reverse.json`
  - `08_formal_targets.json`
  - `09_objections.json`
- Output:
  - `10_score_ledger.json`
  - `10_score_ledger_human.md`

Must produce exactly four independent tracks:

- `Academic_Readiness`
- `Framework_Coherence`
- `Public_Communication`
- `Risk`

Each track must include:

- positive score events
- deductions
- evidence/source reference
- reason
- fix-to-improve

No blended final truth score.

Verification:

```bash
python -m pytest pipeline/tests/test_adversarial.py pipeline/tests/test_pds1_station_08_10.py -v
python -m pipeline.run --input pipeline/tests/fixtures/sample-paper.html --stations 00,03,04,05,06,07,08,09,10,13
```

Done means:

- Formal routing produces target map.
- Score ledger has exactly four tracks.
- Each track has events/reasons/fixes.

## Partner D: Report Export + Vector/Index + Comms/Handoff + HTML Overlay

Ownership:

```text
pipeline/stations/station_11_report_export.py
pipeline/stations/station_12_vector_index.py
pipeline/stations/station_14_comms_handoff.py
pipeline/tests/test_pds1_station_11_12_14.py
templates/pds1_audit_overlay.html
```

Coordinate carefully if editing:

```text
pipeline/run.py
pipeline/stations/__init__.py
pipeline/models/types.py
pipeline/stations/station_13_manifest.py
```

Implement Station `11` Report Export:

- Input: all prior station outputs.
- Output:
  - `11_paper_grade.json`
  - `11_paper_grade.md`
  - `11_paper_grade.html`
  - optional `11_paper_grade.csv`
  - optional `11_paper_grade.xlsx` only if dependencies already exist.

The Markdown/HTML report must begin with `CLAIM_ARCH` and end with `EIGHT_GAPS`.

Implement Station `12` Vector/Index:

- Output:
  - `12_vector_summary.jsonl`
- Include one JSONL row per major snapshot component.
- Keep it embedding-ready, but do not call external embedding APIs.

Implement Station `14` Comms/Handoff:

- Output:
  - `14_run_summary.md`
  - `14_comms_ready_post.md`
- Include what ran, files produced, warnings, next action.

Implement HTML Audit Overlay:

- Add a simple deterministic HTML template for the PDS-1 audit view.
- No decorative UI work. This is a review surface.
- Preserve separate score tracks.

Verification:

```bash
python -m pytest pipeline/tests/test_foundation.py pipeline/tests/test_adversarial.py pipeline/tests/test_pds1_station_11_12_14.py -v
python -m pipeline.run --input pipeline/tests/fixtures/sample-paper.html --stations 00,03,04,05,06,07,08,09,10,11,12,13,14
```

Done means:

- Final report files exist.
- Vector summary exists.
- Handoff post exists.
- HTML audit starts with `CLAIM_ARCH` and ends with `EIGHT_GAPS`.

## Integrator: Final Merge / Verification

After partner branches land, run:

```bash
python -m pytest tests/test_rewrite_layer.py tests/test_extract_figures_math.py pipeline/tests/test_foundation.py pipeline/tests/test_adversarial.py pipeline/tests/test_pds1_station_01_02.py pipeline/tests/test_pds1_station_04.py pipeline/tests/test_pds1_station_08_10.py pipeline/tests/test_pds1_station_11_12_14.py -v
python -m pipeline.run --input pipeline/tests/fixtures/sample-paper.html --stations 00,01,02,03,04,05,06,07,08,09,10,11,12,13,14
```

Then copy reviewed final Markdown outputs to:

```text
\\dlowenas\z obsidian\_ __THEOPHYSICS_CANON\THEOPHYSICS_RESEARCH_PROGRAM\06_ADVERSARIAL_LAYER\Paper_Grader_PDS1
```

And copy heavy/generated data to:

```text
\\dlowenas\z obsidian\_ __THEOPHYSICS_CANON\THEOPHYSICS_RESEARCH_PROGRAM\__THEOPHYSICS_CANON_DATA\06_ADVERSARIAL_LAYER\Paper_Grader_PDS1
```

Run the Canon data mirror after folder changes:

```text
\\dlowenas\z obsidian\_ __THEOPHYSICS_CANON\THEOPHYSICS_RESEARCH_PROGRAM\SYNC_CANON_DATA_TREE.bat
```

## Final Response Required From Each Partner

Each partner must report:

- Stations implemented.
- Files changed.
- Exact tests run.
- Pass/fail result.
- Any skipped dependency.
- Any contract risk.
- Whether station outputs are ready for integration.

