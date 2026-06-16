# Rigor Gate: pa-09-propagation-map

- Series: `Proof-Architecture`
- Verdict: `NEEDS_RIGOR`
- Generated: `2026-06-03T08:04:00`
- Source JSON: `\\dlowenas\brain\Backside\stations\axioms.station\03_FINAL_READY\Proof-Architecture\pa-09-propagation-map\JSON\pa-09-propagation-map.paper-grade.json`
- Claim count: 11
- Failing claim count: 11
- Formal marker count: 11

## Meaning

- `FORMALIZED` is reserved for a verified Lean/Lake build artifact. This gate does not award it automatically.
- `FORMALIZATION_CANDIDATE` means the paper has formal-looking material and no detected audit gaps.
- `AUDIT_READY` means the paper has enough claim/evidence/boundary structure for downstream use, but is not Lean-formalized.
- `NEEDS_RIGOR` means it should not be treated as accepted or reusable without repair.

## Rejection-First Requirements

- State the positive claim.
- Name the exact dependency chain.
- Name close false positives.
- Explain why each false positive fails.
- Keep evidence, boundary, and kill conditions separate.
- Log mistakes and overclaims instead of smoothing them away.

## Failure Counts

- weak:Q3_mechanism: 10
- weak:Q4_evidence: 8
- weak:Q5_falsifiability: 11
- weak:Q6_boundary: 9

## Claim Checks

### Claim 1

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: Coherence measure C\[χ\] ≥ 0. ::: ::::::: ::::::: track :::: track-label ::: {.track-dot style="background:var(--math)"} :::

### Claim 2

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: But this is redundant --- \"structure requires structure.\" No explanatory power added. ::: ::::::: ::::::: {.track .eliminated} :::: track-label ::: {.track-dot style="background:var(--rel)"} :::

### Claim 3

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability
- Claim: ::: ::: track-text --- ::: ::::::: ::::::::::::::::::::::::::::::::: ::::::::::::::: panels :::::::: {.panel .theory-panel} ::: panel-label Published Theories --- Secular Physics\' Own Stopping Point ::: ::: p-item **Hawking/Mlodinow (2010)** --- \"Model-dependent realism.\" Physics describes, doesn\'t explain ground. ::: ::: p-item **Tegmark (2014)** --- Mathematical Universe Hypothesis.

### Claim 4

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability
- Claim: But causation gap. ::: ::: p-item **Penrose (2004)** --- Three-world model: physical, mental, mathematical.

### Claim 5

- Status: `FAIL`
- Failures: weak:Q5_falsifiability, weak:Q6_boundary
- Claim: What terminates it? ::: :::::::: :::::::: {.panel .question-panel} ::: panel-label Questions Left Open → These ARE the Form of God ::: ::: p-item Why these laws and not others? → **Self-grounding, non-arbitrary substrate** ::: ::: p-item Why is math \"unreasonably effective\"? (Wigner 1960) → **Because math describes the substrate** ::: ::: p-item What breaks the regress? → **Self-reference.

### Claim 6

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: Self-grounding requires transcendence. ::: ::: p-item **Noether (1918)** --- Conservation laws follow from symmetries.

### Claim 7

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: :::: ::: {.track-status .pass} ✓ PASS ::: ::: track-text **Participatory actualization.** Potential → actual requires observer.

### Claim 8

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: Born rule implies it. ::: ::::::: ::::::: {.track .eliminated} :::: track-label ::: {.track-dot style="background:var(--math)"} :::

### Claim 9

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: ::: ::: p-item **Von Neumann Chain (1932)** --- Measurement requires observer → observer requires observer → where does it end? ::: ::: p-item **Penrose-Hameroff Orch-OR** --- Consciousness as quantum gravity collapse.

### Claim 10

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: Points to BC7 (info conservation). ::: ::: p-item **No-Cloning Theorem** --- Quantum info can\'t be copied.

### Claim 11

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: Points to BC7 (soul uniqueness). ::: ::: p-item **Boltzmann Brains / Fine-Tuning** --- Points to BC6 (infinite energy source) and non-accidental order. ::: ::: p-item **Bell\'s Theorem (1964)** --- No local hidden variables.
