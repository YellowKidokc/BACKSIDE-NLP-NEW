# Paper Proof Grader

This workflow is the planned intake for Genesis to Quantum and other formal papers.

## Intended Flow

```text
paper in
-> text extraction
-> raw metrics
-> section detection
-> claim extraction
-> 7QS forward/reverse analysis
-> formal verification status layer
-> DeBERTa zero-shot scoring
-> axiom proof snapshot
-> polished HTML / Markdown / JSON / Excel report
-> vectorized report summary
```

## Main Inputs

Drop papers here:

```text
\\dlowenas\brain\paper-proof-grader\DROP_PAPERS_HERE
```

Supported first-pass formats:

```text
.txt
.md
.html
.htm
```

Planned formats:

```text
.pdf
.docx
```

## Main Outputs

Workflow outputs:

```text
\\dlowenas\brain\paper-proof-grader\OUTPUT
```

Archived originals:

```text
\\dlowenas\brain\paper-proof-grader\ARCHIVE
```

Readable report copies:

```text
O:\Vault\AI Chats\Paper Proof Grader Reports
```

Vector collection:

```text
Qdrant: http://192.168.1.177:6333
collection: paper_proof_grader
```

## Fruits of the Spirit Bridge

Truth Engine's Fruits of the Spirit scorer is available from this workflow:

```text
\\dlowenas\brain\paper-proof-grader\fruits_of_spirit_bridge.py
```

Configuration:

```text
\\dlowenas\brain\paper-proof-grader\fruits_of_spirit_config.json
```

Quick run:

```text
\\dlowenas\brain\paper-proof-grader\RUN_FRUITS_OF_SPIRIT.bat
```

Run against a specific folder or paper:

```powershell
python \\dlowenas\brain\paper-proof-grader\fruits_of_spirit_bridge.py --input "O:\_Theophysics_v5\00_Canonical\TH_Physics" --output "\\dlowenas\brain\paper-proof-grader\OUTPUT\fruits_of_spirit" --pattern "*.md" --no-excel
```

Outputs:

```text
fruits_scores.json
fruits_scores.csv
fruits_summary.json
fruits_errors.json
```

The bridge now emits two lanes:

```text
lexical scores: truth, coherence, fruit, anti_fruit, grounding, contradiction
semantic-anchor scores: semantic_fruit_alignment, semantic_anti_alignment, semantic_net_alignment
```

The semantic-anchor lane measures alignment to an explicit coherence ontology, not proof of spiritual truth. It uses `sentence-transformers` when available and falls back to a deterministic hashed n-gram vectorizer when embedding packages are unavailable.

Per-paper Fruits Template Excel export is supported when the local Python environment has `openpyxl` available; otherwise the bridge still produces JSON and CSV.

## Formal Verification Layer

The grader now emits a conservative formal-status panel for each claim:

```text
formal_verification:
  lean: proven | formalizable | counterexample_found | not_attempted | speculative
  alloy: not_configured | no_counterexample | counterexample_found
  state_model: not_applicable | not_configured | clean | bad_path_found
  bridge_status: formal_candidate | bridge | unclassified
```

Lean remains the canonical proof kernel. The current layer does not pretend to prove new claims; it attaches candidate theorem families and intended Lean files so a reviewer can see exactly where formal work would have to land.

Alloy is reserved for counterexample search before Lean. TLA+/Maude-style state modeling is reserved for phase/state-transition claims. This keeps the station from becoming prover soup while still giving the paper grader a real attack/proof lane.

Generated dependency map:

```text
\\dlowenas\brain\paper-proof-grader\OUTPUT\formal-verification-dependency-map.md
```

## Existing Tools To Reuse

```text
D:\brain\03_DEBERTA
D:\brain\08_CLAIMS
\\dlowenas\brain\link-pull-drop
```

## Build Order

1. Deterministic raw metrics.
2. Claim extractor bridge.
3. DeBERTa scoring labels for paper/axiom/7QS review.
4. Markdown and JSON report.
5. Polished HTML report.
6. Excel export.
7. Vectorized report summary.
## Current Workflow Rails

The grading process is now mapped in two operational docs:

```text
X:\paper-proof-grader\GRADING_WORKFLOW.md
X:\paper-proof-grader\PAPER_GRADER_PROCESS_INDEX.md
X:\paper-proof-grader\OUTPUT_CONTRACT.md
X:\paper-proof-grader\OUTPUT_ARTIFACT_MAP.json
```

Use `GRADING_WORKFLOW.md` for the philosophy, layers, boundaries, and build order. Use `PAPER_GRADER_PROCESS_INDEX.md` for the concrete file map, current gaps, and next build tickets. Use `OUTPUT_CONTRACT.md` and `OUTPUT_ARTIFACT_MAP.json` to decide what every station must emit before adding more grader logic.

