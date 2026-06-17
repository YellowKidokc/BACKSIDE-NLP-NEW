# Paper Proof Grader - Output Contract

Status: planned output map, drafted from the live grader plus `CDCM.xlsx`.

Purpose: define every artifact the paper-grader pipeline should produce before we build more stations. If an output is not listed here, it is optional or experimental.

## Design Rule

Every output must answer at least one of these questions:

1. What did we ingest?
2. What claims did we extract?
3. What supports or weakens each claim?
4. What formal route exists for the claim?
5. What should a human reviewer do next?
6. Can the run be reproduced later?

## Output Families

| Family | Audience | Format | Required |
|---|---|---:|---:|
| Provenance packet | machine / auditor | JSON + SHA-256 text | yes |
| Paper grade packet | machine | JSON | yes |
| Claim ledger | machine / reviewer | CSV + XLSX sheet | yes |
| Human report | reader / reviewer | Markdown + HTML | yes |
| Reviewer workbook | David / institution | XLSX | yes |
| Formal target map | Lean / proof partner | Markdown + JSON | yes |
| Objection ledger | adversarial review | Markdown + CSV/XLSX sheet | yes |
| Vector summary | search / Brain | JSONL / Markdown | yes, after core |
| Comms handoff | AI partners | Markdown text | yes |
| Public portal | public/institutional | static HTML | later |

## Canonical Per-Paper Folder Shape

The current grader writes flat files into `OUTPUT`. The target shape should move toward this:

```text
OUTPUT/
  runs/
    {run_uuid}/
      run-manifest.json
      run-summary.md
      batch-index.html
      papers/
        {paper_uuid}/
          source-manifest.json
          source.sha256
          normalized-text.md
          structure-map.json
          paper-grade.json
          paper-grade.md
          paper-grade.html
          claim-ledger.csv
          reviewer-workbook.xlsx
          formal-target-map.md
          formal-target-map.json
          objection-ledger.md
          vector-summary.jsonl
```

Keep backward-compatible flat exports until the new run folder is stable.

## Required Machine Outputs

### 1. `source-manifest.json`

Created by: `00 Intake Station`

```json
{
  "paper_uuid": "",
  "run_uuid": "",
  "source_file_name": "",
  "source_original_path": "",
  "source_archive_path": "",
  "source_sha256": "",
  "source_size_bytes": 0,
  "detected_format": "md|html|txt|pdf|docx|ocr",
  "ingested_at_utc": "",
  "grader_version": "",
  "rubric_version": ""
}
```

### 2. `normalized-text.md`

Created by: `01 Text Normalization Station`

Human-readable normalized text. This is the text all claim spans must point back to.

Required sections:

```text
---
paper_uuid:
source_sha256:
normalizer_version:
---

# Normalized Paper Text
```

### 3. `structure-map.json`

Created by: `02 Structure Station`

```json
{
  "paper_uuid": "",
  "sections": [
    {
      "section_id": "SEC-0001",
      "title": "",
      "level": 1,
      "char_start": 0,
      "char_end": 0,
      "paragraph_count": 0,
      "sentence_count": 0
    }
  ],
  "equations": [],
  "citations": [],
  "scripture_refs": [],
  "tables": []
}
```

### 4. `paper-grade.json`

Created by: main grading pipeline after all core stations.

This is the canonical machine packet.

Top-level shape:

```json
{
  "paper_uuid": "",
  "run_uuid": "",
  "paper_id": "",
  "generated_at_utc": "",
  "source_manifest": {},
  "metrics": {},
  "sections": [],
  "claims": [],
  "evidence": [],
  "formal_verification": {},
  "objections": [],
  "readiness": {},
  "boundaries": [],
  "output_paths": {}
}
```

### 5. `claim-ledger.csv`

Created by: `03 Claim Extraction` through `10 Score/Readiness`.

Required columns:

```text
paper_uuid
run_uuid
claim_uuid
claim_index
section_id
section_title
paragraph_index
sentence_index
char_start
char_end
quoted_span
claim_text
claim_type
claim_maturity_level
claim_maturity_label
evidence_required
evidence_found_count
support_status
falsifiability_status
kill_condition
formal_status
formal_target
objection_count
overclaim_risk
category_error_risk
readiness_label
recommended_action
```

### 6. `formal-target-map.json`

Created by: `08 Formal Routing Station`

```json
{
  "paper_uuid": "",
  "run_uuid": "",
  "targets": [
    {
      "claim_uuid": "",
      "claim_text": "",
      "formal_status": "proven|formalizable|bridge|speculative|not_formal",
      "lean_module_target": "",
      "lean_theorem_name": "",
      "candidate_dependencies": [],
      "missing_axioms": [],
      "alloy_candidate": false,
      "state_model_candidate": false,
      "boundary_note": ""
    }
  ]
}
```

### 7. `run-manifest.json`

Created by: `13 Manifest/Provenance Station`

```json
{
  "run_uuid": "",
  "started_at_utc": "",
  "completed_at_utc": "",
  "grader_version": "",
  "rubric_version": "",
  "station_versions": {},
  "input_count": 0,
  "output_count": 0,
  "papers": [],
  "output_hashes": [
    {
      "path": "",
      "sha256": ""
    }
  ],
  "warnings": [],
  "errors": []
}
```

## Required Human Outputs

### 1. `paper-grade.md`

Created by: `11 Report Export Station`

Required headings:

```text
# {Paper Title} - Paper Grade
## Executive Summary
## Identity and Provenance
## Readiness Label
## Claim Inventory
## Evidence Ledger
## 7Q Forward/Reverse Summary
## Formal Verification Targets
## Strongest Objections
## Kill Conditions
## Recommended Rewrites
## Boundaries / Not Claimed
## Output Manifest
```

### 2. `paper-grade.html`

Same content as Markdown, but navigable and public-review ready.

Required UI blocks:

- top summary cards
- readiness badge
- claim table
- formal target table
- objection table
- boundary / not-claimed panel
- source/provenance panel

### 3. `formal-target-map.md`

Lean/proof partner handoff.

Required headings:

```text
# Formal Target Map
## Proven / Already Covered
## Formalizable Next
## Bridge Only
## Speculative / Do Not Formalize Yet
## Missing Axioms
## Suggested Lean File Targets
```

### 4. `objection-ledger.md`

Adversarial review surface.

Required headings:

```text
# Objection Ledger
## Paper-Level Objections
## Claim-Level Objections
## Category Error Risks
## Overclaim Risks
## Rival Explanations
## Required Rewrites
```

### 5. `run-summary.md`

Human handoff for David and AI partners.

Required sections:

```text
# Paper Grader Run Summary
## What Ran
## What Passed
## What Failed
## Strongest Papers / Claims
## Weakest Papers / Claims
## Formalization Queue
## Rewrite Queue
## Next Actions
```

## Required Reviewer Workbook

Inspired by `CDCM.xlsx`, the paper-grader workbook should be the high-control review surface.

Workbook name:

```text
{paper_id}.reviewer-workbook.xlsx
```

Required sheets:

| Sheet | Purpose |
|---|---|
| `Dashboard` | one-screen summary and top vulnerabilities |
| `Source_Manifest` | UUIDs, hashes, source path, run metadata |
| `Claim_Index` | every claim with type, status, and source span |
| `Structure_Map` | sections, paragraphs, equations, citations |
| `Evidence_Ledger` | support rows tied to claim UUIDs |
| `7Q_Forward` | forward 7Q fields and scores |
| `7Q_Reverse` | kill conditions, rival explanations, downgrade tests |
| `Formal_Targets` | Lean/Alloy/state-model routing |
| `Objections` | adversarial objections and risk flags |
| `Constraint_Matrix` | -1/0/+1 constraint scoring inspired by CDCM |
| `Global_Metrics` | paper-level metrics and readiness formulas |
| `Claim_Total_Score` | combined descriptive/pressure/readiness scores |
| `Readiness_Decision` | final status and recommended next action |
| `Output_Manifest` | produced files and hashes |

Optional later sheets from CDCM-style framework scoring:

| Sheet | Purpose |
|---|---|
| `Theory_Mapping` | map claims against rival frameworks |
| `Domain_Mapping` | cross-domain invariants and proxies |
| `XDTI_Score` | cross-domain transfer integrity |
| `Constraint_Density` | falsifiers, boundaries, parameters |
| `Directional_Asymmetry` | entropy/coherence directionality |
| `Coverage_Analysis` | support/contradiction by framework |
| `Comparative_Analysis` | compare Theophysics with rivals |

## Score Families

Do not reduce the paper to one score too soon.

### Descriptive Scores

What is present?

- section completeness
- claim count
- equation count
- citation count
- boundary count
- kill-condition count

### Pressure Scores

What survives attack?

- evidence support ratio
- falsifiability completeness
- objection severity
- category-error risk
- overclaim risk
- reverse-test survival

### Formal Scores

What can be proved or routed?

- proven Lean claims
- formalizable claims
- bridge-only claims
- speculative claims
- missing theorem dependencies

### Readiness Scores

What should happen next?

Allowed labels:

```text
DRAFT
INTERNAL_REVIEW
FRAMEWORK_STRONG
PUBLIC_SAFE_WITH_BOUNDARIES
FORMALIZATION_REQUIRED
EMPIRICAL_SUPPORT_REQUIRED
READY_FOR_INSTITUTIONAL_REVIEW
DO_NOT_PUBLISH_YET
```

## Station-to-Output Map

| Station | Primary outputs |
|---|---|
| `00 Intake` | `source-manifest.json`, `source.sha256` |
| `01 Text Normalization` | `normalized-text.md` |
| `02 Structure` | `structure-map.json`, workbook `Structure_Map` |
| `03 Claim Extraction` | `claim-ledger.csv`, workbook `Claim_Index` |
| `04 Claim Typing` | enriched `claim-ledger.csv` |
| `05 Evidence Ledger` | evidence rows, workbook `Evidence_Ledger` |
| `06 7Q Forward` | workbook `7Q_Forward`, JSON claim fields |
| `07 7Q Reverse` | workbook `7Q_Reverse`, kill conditions |
| `08 Formal Routing` | `formal-target-map.json/.md`, workbook `Formal_Targets` |
| `09 Objection` | `objection-ledger.md`, workbook `Objections` |
| `10 Score/Readiness` | workbook `Claim_Total_Score`, `Readiness_Decision` |
| `11 Report Export` | `paper-grade.md/.html/.json/.xlsx` |
| `12 Vector/Index` | `vector-summary.jsonl` |
| `13 Manifest/Provenance` | `run-manifest.json`, hashes |
| `14 Comms/Handoff` | `run-summary.md`, comms post |

## Build Order

Build in this order:

1. `source-manifest.json` and `run-manifest.json`
2. `normalized-text.md`
3. source spans in claim rows
4. `claim-ledger.csv`
5. reviewer workbook skeleton
6. evidence ledger
7. 7Q forward/reverse sheets
8. formal target map
9. objection ledger
10. readiness decision
11. static HTML portal
12. vector summaries

## Non-Negotiable Boundary

No claim may receive a high readiness label unless it has:

- stable `claim_uuid`
- exact source span
- typed claim category
- evidence requirement
- support status
- kill condition or explicit reason none applies
- overclaim/category-error check
- formal route or explicit boundary note

If any of those are missing, the paper can still be valuable, but it is not institution-ready.
