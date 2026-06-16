# Paper Proof Grader - Process Index

Status: routing map for what exists, what is missing, and where each process belongs.

## Live Entry Points

| Process | Current file/folder | Status | Notes |
|---|---|---|---|
| Drop input | `X:\paper-proof-grader\DROP_PAPERS_HERE` | Working | `.txt`, `.md`, `.html`, `.htm` first-pass formats. |
| Main run | `X:\paper-proof-grader\RUN_NOW_NO_PAUSE.bat` | Working | Calls the deterministic paper grader. |
| Main engine | `X:\paper-proof-grader\pipeline.py` | Working | Intake, metrics, claims, formal annotations, exports. |
| Config | `X:\paper-proof-grader\config.json` | Working | Points to Brain NAS paths and model/service locations. |
| Formal layer | `X:\paper-proof-grader\formal_verification.py` | Working annotation | Conservative proof-routing layer, not proof generation. |
| Expanded report | `X:\paper-proof-grader\expanded_report.py` | Present | Report enhancement layer. |
| Axiom + 7Q station | `X:\paper-proof-grader\run_axiom_7q_stations.py` | Working | Produces station-runs and Excel workbook. |
| Fruits bridge | `X:\paper-proof-grader\fruits_of_spirit_bridge.py` | Working auxiliary | Lexical/semantic coherence lens, not canonical proof. |
| Outputs | `X:\paper-proof-grader\OUTPUT` | Working | JSON, MD, HTML, CSV, XLSX, station-runs. |
| Archive | `X:\paper-proof-grader\ARCHIVE` | Working | Processed originals move here. |

## Current Supporting Specs

| Spec | Purpose |
|---|---|
| `X:\paper-proof-grader\README.md` | Existing user-facing workflow summary. |
| `X:\paper-proof-grader\GRADING_WORKFLOW.md` | New operating workflow and build order. |
| `X:\paper-proof-grader\PAPER_SNAPSHOT_SCHEMA.md` | One-screen paper triage schema. |
| `X:\paper-proof-grader\MASTER_VARIABLE_SCHEMA.md` | Full variable inventory for grading. |
| `X:\paper-proof-grader\WORKFLOW_POINTER.md` | Points to knowledge-refinery Axiom + 7Q station. |
| `X:\paper-proof-grader\AXIOM_7Q_STATION_STATUS_20260518.md` | Latest Axiom + 7Q station status. |
| `X:\paper-proof-grader\SETUP_STATUS_2026-05-18.md` | Working canary verification and known conductor gap. |

## Artifact Contract

A complete graded-paper packet should eventually contain:

```text
/input/{paper_uuid}/source.ext
/input/{paper_uuid}/source.sha256
/output/{run_uuid}/{paper_id}.paper-grade.json
/output/{run_uuid}/{paper_id}.paper-grade.md
/output/{run_uuid}/{paper_id}.paper-grade.html
/output/{run_uuid}/{paper_id}.claim-audit.csv
/output/{run_uuid}/{paper_id}.paper-grade.xlsx
/output/{run_uuid}/{paper_id}.axiom-7q-stations.json
/output/{run_uuid}/{paper_id}.axiom-7q-stations.md
/output/{run_uuid}/run-manifest.json
/archive/{paper_uuid}/source.ext
```

Current implementation is close but not yet UUID/run-folder strict.

## Grading Lanes

| Lane | Purpose | Current state | Next work |
|---|---|---|---|
| Provenance | Identify input and run | Partial | Add UUID + SHA-256 manifest. |
| Metrics | Count structure and density | Working | Add citation/reference counts. |
| Claim extraction | Find candidate claims | Working deterministic | Add typed taxonomy and source spans. |
| Evidence ledger | Attach support to claims | Weak/partial | Create explicit evidence rows. |
| 7Q | Forward/reverse pressure | Working station | Tighten Q0 and kill-condition scoring. |
| Formal | Route to Lean/Alloy/state models | Annotation working | Add theorem target export and stubs. |
| Objections | Strongest attack per claim | Partial through 7Q reverse | Add adversarial objection rows. |
| Exports | Human/machine reports | Working | Add manifest and review portal. |
| Vectorization | Search/retrieval | Configured | Confirm Qdrant/Infinity runtime before relying on it. |

## Immediate Build Tickets

### PPG-001 - UUID and Hash Manifest

Add stable IDs:

- `paper_uuid`
- `run_uuid`
- `claim_uuid`
- `source_sha256`
- `grader_version`
- `rubric_version`

Output:

```text
OUTPUT\{paper_id}.run-manifest.json
```

### PPG-002 - Claim Type Taxonomy

Classify claims into:

```text
rhetorical
metaphysical
theological
mathematical
formal
empirical
historical
bridge/isomorphism
prediction
boundary/not-claimed
```

### PPG-003 - Source Span Ledger

For every claim, store:

```text
source_file
section_title
paragraph_index
sentence_index
char_start
char_end
quoted_span
```

### PPG-004 - Evidence Rows

Add explicit support rows:

```text
evidence_id
claim_uuid
evidence_type
source_span_or_citation
support_strength
support_boundary
```

### PPG-005 - Lean Target Export

For every formalizable claim, export:

```text
lean_module_target
lean_theorem_name
current_status
missing_axioms
candidate_dependencies
```

### PPG-006 - Reviewer Portal

Static index over one run:

```text
batch-index.html
claim-ledger.html
formalization-targets.html
objections.html
manifest.html
```

## Known Blockers

| Blocker | Severity | Note |
|---|---:|---|
| Full knowledge-refinery conductor path missing | Medium | Direct paper grader works; larger conductor needs repointing. See `SETUP_STATUS_2026-05-18.md`. |
| PDF/DOCX extraction not primary | Medium | Declared in config but current verified lane is text/markdown/html. |
| No strict UUID/hash manifest yet | High | Needed before public/institutional reproducibility claims. |
| Evidence ledger not span-level | High | Scores need exact support pointers. |
| Formal proof generation not automated | Expected | Current layer is proof routing, not theorem synthesis. |

## Tomorrow's Correct First Move

Do not add broad AI grading first.

Build `PPG-001` and `PPG-003` first. UUIDs plus source spans make every later AI/rubric score accountable.
