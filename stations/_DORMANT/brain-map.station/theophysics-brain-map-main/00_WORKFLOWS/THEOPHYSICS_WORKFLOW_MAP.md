# Theophysics Workflow Map

This is the quick orientation map for partner sessions working inside the Theophysics workspace.

Primary location:

```text
\\dlowenas\brain
```

Comms Hub local orientation:

```text
\\dlowenas\brain\theophysics-comms-hub\README_COMMS_HUB_QUICK_START.md
```

## What This Workspace Is Doing

The Theophysics research program is a multi-lane system for turning papers, articles, equations, proofs, and public-facing material into inspectable research artifacts.

The main distinction:

- Paper intelligence asks whether a paper is defensible, evidenced, clear, and honest.
- NLP snapshots extract claims, evidence, equations, risks, attack points, and repair targets.
- Formal verification asks what is actually mathematically proven.
- Public/report/TTS layers make the work readable, reviewable, and usable by humans.

## Workflow 1 - Paper Proof Grader / Paper Intelligence

Location:

```text
\\dlowenas\brain\paper-proof-grader
```

Main intake:

```text
\\dlowenas\brain\paper-proof-grader\DROP_PAPERS_HERE
```

Main output:

```text
\\dlowenas\brain\paper-proof-grader\OUTPUT
```

Purpose:

Take a paper or article and produce a structured defensibility report.

Intended flow:

```text
paper in
-> text extraction
-> raw metrics
-> section detection
-> claim extraction
-> 7QS forward/reverse analysis
-> DeBERTa zero-shot scoring
-> axiom/proof snapshot
-> polished HTML / Markdown / JSON / Excel report
-> vectorized report summary
```

Typical outputs:

- claim inventory
- equation inventory
- overstatement flags
- academic readiness score
- framework coherence score
- public communication score
- risk score
- HTML scorecards
- JSON snapshots
- Excel rows and summaries

Vectorization status:

The workflow is configured for vectorization, but the current `pipeline.py` writes files and does not yet perform the final Qdrant upsert.

Configured services:

```text
Embedding server: http://192.168.1.177:7997
Embedding endpoint: POST /embeddings
Model: sentence-transformers/all-MiniLM-L6-v2

Qdrant: http://192.168.1.177:6333
Target collection: paper_proof_grader
```

Expected vector path:

```text
paper-grade JSON / snapshot JSON
-> build compact summary text
-> send summary text to Infinity /embeddings
-> receive embedding vector
-> upsert vector + metadata into Qdrant collection paper_proof_grader
```

Metadata should include at least:

- `paper_id`
- `source_file`
- `generated_at`
- `report_json`
- `report_html`
- key scores
- top claims
- equation count
- risk label
- domain labels

As of this map update, `paper_proof_grader` may need to be created in Qdrant before first use.

## Workflow 2 - Fast NLP Defensibility Snapshot

Purpose:

Quickly identify what a paper claims, what supports it, where it can be attacked, and what should be repaired.

Common sections:

- `CLAIM_ARCH`
- `EVIDENCE_CHAIN`
- `KILL_ARCH`
- `EQ_SEM`
- `DOMAIN_BOUNDARY`
- `REVIEWER_SEEDS`
- `OVERSTATE_PATTERN`
- `BENCHMARK_ANCHOR`
- `CROSS_DEP`
- `FOUR_SCORE_DASHBOARD`

Use this lane when the question is:

```text
Where is this paper strong, where will a hostile reviewer attack it, and what needs repair before release?
```

## Workflow 3 - HTML Report / Scorecard Generator

Purpose:

Turn grader JSON or snapshot JSON into a polished scorecard or dashboard.

It supports:

- legacy flat pipeline rows
- richer proof-explorer snapshot objects

Typical report tabs:

- claims
- equations
- assumptions
- evidence
- kill conditions
- comparison
- risk
- peer-review notes

Use this lane when the output needs to be readable by David, reviewers, public readers, or another AI partner.

## Workflow 4 - Formal Verification / Lean

Typical locations observed in prior sessions:

```text
X:\proof-architecture
\\dlowenas\brain\proof-explorer
```

Codex session copies have also existed under:

```text
C:\Users\lowes\Documents\Codex\2026-05-06\theophysics-lean-verification-package
C:\Users\lowes\Documents\Codex\2026-05-06\theophysics-local-lean-run
```

Purpose:

Separate proved mathematical structure from interpretive theology, physics, or metaphysics.

Formalized themes:

- product collapse
- nonzero product behavior
- entropy attenuation
- `R` gate collapse
- grace as reset
- zero-preserving operators
- law-isomorphism burden

Important boundary:

Lean proves only the structure that is encoded. It does not prove theology, empirical physics, or a canonical Lagrangian unless those claims are explicitly formalized.

## Workflow 5 - Python / Colab Numerical Mirror

Purpose:

Make the formal structures executable and easier to test, demonstrate, or challenge numerically.

Use this lane for:

- runnable Master Equation mirrors
- sanity checks
- counterexamples
- Colab-friendly demonstrations
- tests that help readers understand what Lean statements do and do not say

## Workflow 6 - Fruits of the Spirit Bridge

Location:

```text
\\dlowenas\brain\paper-proof-grader\fruits_of_spirit_bridge.py
\\dlowenas\brain\paper-proof-grader\fruits_of_spirit_config.json
```

Purpose:

Connect the Truth Engine / Fruits scorer into the paper workflow.

Outputs include:

- lexical truth/coherence/fruit/anti-fruit/grounding/contradiction scores
- semantic fruit alignment
- semantic anti-alignment
- semantic net alignment

Boundary:

This measures alignment to a defined coherence ontology. It is not proof of spiritual truth.

## Workflow 7 - Math / TTS Translation

Purpose:

Turn equations and LaTeX into natural language that can be read aloud without misleading the listener.

Review questions:

- Does it sound like a person explaining the equation?
- Can a listener understand the structure without seeing the equation?
- Are symbol meanings stated only when known?
- Does it avoid overclaiming physics, theology, proof, or evidence?
- Is it short enough for TTS or under-equation narration?

Use this lane for public-facing audio, equation cards, narrated pages, and accessibility.

## Workflow 8 - Batch / Docker GTQ Runs

Location inside the paper grader:

```text
\\dlowenas\brain\paper-proof-grader\DOCKER_PACKAGE_20260507_191530
```

Purpose:

Run paper intelligence across a corpus, especially Genesis to Quantum articles, and produce consistent artifacts.

Typical outputs:

- per-paper snapshots
- corpus summaries
- HTML report folders
- JSON rows
- Excel workbooks
- public report assets

## Current Mental Model

```text
content / papers
-> NLP extraction
-> paper defensibility scoring
-> claim/evidence/equation/risk snapshots
-> HTML/Excel/JSON reports
-> optional vector summary
-> formal proof lane checks what is actually mathematically proven
-> public communication / TTS / report layers make it readable
```

## Where To Start

For a new paper:

```text
\\dlowenas\brain\paper-proof-grader\DROP_PAPERS_HERE
```

For another AI or Codex session joining the workspace:

```text
\\dlowenas\brain\theophysics-comms-hub\README_COMMS_HUB_QUICK_START.md
```

For handoffs between sessions:

```text
\\dlowenas\brain\session-handoff-drop
```

For this map:

```text
\\dlowenas\brain\THEOPHYSICS_WORKFLOW_MAP.md
```




