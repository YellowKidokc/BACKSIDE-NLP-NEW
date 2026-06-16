# Paper Proof Grader - Operating Workflow

Status: live workflow rails, 2026-05-19.

Purpose: turn a paper/article/proof essay into a machine-checkable research packet: claims, evidence, maturity level, 7Q pressure, formalization path, falsification rules, and human-readable outputs.

This is a research refinery, not a single score script.

## North Star

A graded paper should answer five questions without anyone trusting the author or the grader blindly:

1. What is the paper actually claiming?
2. What kind of claim is each claim: rhetorical, theological, mathematical, empirical, historical, formal, or bridge?
3. What evidence or theorem family would have to carry the claim?
4. What would falsify or downgrade it?
5. What output artifact lets a human, AI partner, or institution inspect the result?

## Current Canonical Runtime

```text
X:\paper-proof-grader
\\dlowenas\brain\paper-proof-grader
```

These currently mirror the same live folder. Prefer `X:\paper-proof-grader` for local commands and `\\dlowenas\brain\paper-proof-grader` for durable NAS references.

## Current Inputs

Drop first-pass files here:

```text
X:\paper-proof-grader\DROP_PAPERS_HERE
```

Working today:

```text
.txt
.md
.html
.htm
```

Declared/planned but not yet primary:

```text
.pdf
.docx
```

## Current Outputs

Primary output folder:

```text
X:\paper-proof-grader\OUTPUT
```

For each paper, the main pipeline can emit:

```text
{paper_id}.paper-grade.json
{paper_id}.paper-grade.md
{paper_id}.paper-grade.html
{paper_id}.claim-audit.csv
{paper_id}.paper-grade.xlsx
paper-proof-grader-run-{timestamp}.json
```

The Axiom + 7Q station emits timestamped batches under:

```text
X:\paper-proof-grader\OUTPUT\station-runs
```

## What We Have Now

### Working Deterministic Grader

Entrypoint:

```text
X:\paper-proof-grader\pipeline.py
X:\paper-proof-grader\RUN_NOW_NO_PAUSE.bat
```

Currently performs:

- text intake for supported formats
- section detection
- equation-ish pattern extraction
- deterministic claim candidate extraction
- maturity ladder classification
- 7Q mini-grid flags
- forward/reverse test text
- kill-condition prompt text
- formal verification status attachment
- JSON/Markdown/HTML/CSV/Excel export
- archive movement for processed inputs

Verified canary status is recorded in:

```text
X:\paper-proof-grader\SETUP_STATUS_2026-05-18.md
```

### Formal Verification Layer

Entrypoint/module:

```text
X:\paper-proof-grader\formal_verification.py
```

Current status: conservative annotation layer.

It does not prove new claims. It attaches proof status, theorem-family candidates, and intended Lean/Alloy/state-model lanes so a reviewer can see where proof pressure belongs.

Canonical statuses:

```text
lean: proven | formalizable | counterexample_found | not_attempted | speculative
alloy: not_configured | no_counterexample | counterexample_found
state_model: not_applicable | not_configured | clean | bad_path_found
bridge_status: formal_candidate | bridge | unclassified
```

### Axiom + 7Q Station

Entrypoint:

```text
X:\paper-proof-grader\run_axiom_7q_stations.py
```

Workflow pointer:

```text
X:\paper-proof-grader\WORKFLOW_POINTER.md
X:\knowledge-refinery\10_STATIONS\12_axiom_promotion\WORKFLOW.md
```

Currently performs:

- reads existing `*.paper-grade.json` outputs
- loads canonical chain/axiom reference material
- gives deterministic chain-node / axiom hits
- runs 7Q forward score
- runs reverse-collapse verdict
- optionally calls OpenAI verifier if configured
- emits Markdown, JSON, HTML, and Excel review workbooks

### Fruits / Coherence Bridge

Entrypoint:

```text
X:\paper-proof-grader\fruits_of_spirit_bridge.py
```

Current role: separate semantic/lexical alignment scorer. Useful as an auxiliary lens, not a proof engine.

### Schemas Already Present

```text
X:\paper-proof-grader\MASTER_VARIABLE_SCHEMA.md
X:\paper-proof-grader\PAPER_SNAPSHOT_SCHEMA.md
```

These are the right vocabulary floor for scores, snapshots, claims, evidence, and UI/report expectations.

## What We Do Not Have Yet

### Intake Gaps

- robust PDF extraction
- robust DOCX extraction
- OCR lane for scanned PDFs/images
- durable paper UUID assignment independent of filename
- source hash manifest for every input
- duplicate-paper detection by hash and semantic similarity

### Claim/Evidence Gaps

- span-level evidence pointers back to exact source line/paragraph
- typed claim taxonomy strong enough for public/institutional review
- citation extraction and source-quality scoring
- equation-to-explanation alignment checks
- explicit scripture/reference extraction where relevant
- overclaim detector that distinguishes internal-framework claims from public proof claims

### Formalization Gaps

- automatic Lean target generation from formalizable claims
- Alloy counterexample harness for finite/state claims
- TLA+/Maude-style state-machine runner for phase-transition claims
- proof dependency graph that links each claim to actual Lean files, theorem names, or missing theorem stubs
- result gate that separates `proved`, `formalizable`, `bridge only`, and `rhetorical only`

### Report/Workflow Gaps

- stable per-run UUIDs
- stable per-paper UUIDs
- stable per-claim UUIDs
- machine-readable manifest tying input hash -> grader version -> rubric version -> outputs
- report diffing across paper revisions
- publishable static portal for institutional review
- CI-style reproducibility command

## Required Grading Layers

Each paper should eventually pass through these layers in order.

### Layer 0 - Identity and Provenance

Outputs:

- paper UUID
- source path
- source SHA-256
- title/author/date/version if extractable
- grader version
- rubric version
- run timestamp

Failure condition: no stable identity or no source hash.

### Layer 1 - Raw Text Metrics

Outputs:

- word count
- section count
- heading map
- equation count
- citation/reference count
- readability and density metrics

Boundary: raw metrics are facts, not judgments.

### Layer 2 - Claim Inventory

Outputs:

- claim IDs
- claim text
- source section
- claim type
- maturity level
- nearby equations/references
- evidence required

Failure condition: major thesis claims not captured.

### Layer 3 - Evidence Ledger

Outputs:

- evidence spans
- citation/source quality
- equation support
- formal theorem support
- empirical support
- theological/scriptural support where applicable

Failure condition: claim gets a strong score without visible support.

### Layer 4 - 7Q Forward/Reverse

Outputs:

- Q0 posture/boundary
- Q1 identity
- Q2 scope/domain
- Q3 mechanism
- Q4 support/evidence
- Q5 dependencies/falsifiability
- Q6 consequences
- Q7 kill conditions/listener risk
- reverse-collapse condition

Failure condition: no stated kill condition for a claim above maturity 3.

### Layer 5 - Formal Verification Routing

Outputs:

- theorem dependency candidates
- Lean file target
- theorem/stub name target
- Alloy/state-model candidate where appropriate
- formal status
- bridge status

Failure condition: a public proof claim has no formal route or boundary note.

### Layer 6 - Objection / Adversarial Review

Outputs:

- strongest objection
- category-error risk
- overclaim risk
- missing definition risk
- rival explanation
- recommended rewrite or downgrade

Failure condition: public-facing report contains only affirming scores.

### Layer 7 - Export and Archive

Outputs:

- JSON packet
- Markdown report
- HTML report
- CSV claim ledger
- Excel workbook
- source archive
- run manifest
- optional vector summary

Failure condition: outputs cannot be reproduced or traced back to the input.

## Score Philosophy

Do not collapse everything into one magic number too early.

Use three score families:

1. **Descriptive scores** - what is present.
2. **Pressure scores** - what survives attack.
3. **Readiness scores** - what the paper is ready for.

Recommended readiness labels:

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

## Minimum Useful v1.0

Before adding more intelligence, lock this reproducible minimum:

1. Drop one `.md`/`.html` paper into `DROP_PAPERS_HERE`.
2. Run `RUN_NOW_NO_PAUSE.bat`.
3. Emit JSON/MD/HTML/CSV/XLSX.
4. Archive source.
5. Run Axiom + 7Q station over the result.
6. Emit station JSON/MD/HTML/XLSX.
7. Produce a manifest with hashes, versions, and output paths.

## Near-Term Build Order

1. Add UUID/hash manifest layer.
2. Add stronger claim type taxonomy.
3. Add exact source-span references for claims.
4. Add citation/reference extraction.
5. Add paper revision diffing.
6. Add Lean target map export.
7. Add static review portal.

## Boundary Rules

- The grader may identify formalizable claims; it must not pretend Lean has proved them until a Lean theorem compiles.
- The grader may score empirical support; it must not manufacture citations.
- The grader may classify theological structure; it must distinguish framework-internal coherence from public proof.
- The grader may recommend publishing; it must state what still has to be checked by humans.
- Any high-level score must be traceable to claim rows and evidence rows.

## One-Sentence Operating Rule

Every score must be able to answer: what text caused this score, what rule interpreted it, and what would make the score go down?
