# Rigor Gate: 01_FORMAL_LAYER_Definition10

- Series: `Unsorted`
- Verdict: `NEEDS_RIGOR`
- Generated: `2026-05-11T18:24:08`
- Source JSON: `\\dlowenas\brain\axioms\03_FINAL_READY\Unsorted\01_FORMAL_LAYER_Definition10\JSON\01_FORMAL_LAYER_Definition10.paper-grade.json`
- Claim count: 7
- Failing claim count: 7
- Formal marker count: 16

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

- weak:Q3_mechanism: 7
- weak:Q4_evidence: 6
- weak:Q5_falsifiability: 7
- weak:Q6_boundary: 7

## Claim Checks

### Claim 1

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: This is the typed, formal mathematical specification of the Master Equation.

### Claim 2

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: | # | Symbol | Domain | Formal Definition | |---|--------|--------|-------------------| | 1 | G | ℝ≥0 | External negentropy influx rate | | 2 | M | [-1, 1] | Alignment cosine between system state vector and reference vector | | 3 | E | ℝ≥0 | Signal propagation fidelity (channel capacity) | | 4 | S_prod | ℝ≥0 | Entropy production rate (raw disorder accumulation) | | 5 | T | ℝ>0 | Temporal integration parameter | | 6 | K | ℝ≥0 | Information compression ratio (Kolmogorov complexity) | | 7 | R | {0, 1} | Phase transition indicator (irreversible state change) | | 8 | Q | [0, 1] | Superposition measure (unresolved state space) | | 9 | F | [0, 1] | Non-local correlation strength (entanglement measure) | | 10 | C | [0, 1] | Total integration measure (global coherence) | ---

### Claim 3

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: The specific analytic form (exponential vs. rational) requires Mathlib for full verification but is structurally interchangeable inside the product. ---

### Claim 4

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: The companion kernel `CorrectedEntropyKernel.lean` formally proves: 1. **Antitone entropy.** `S_eff` is antitone in `S_prod`.

### Claim 5

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: 2. **Zero collapse on numeric factors.** If any of G, M, E, T, K, Q, F, C is zero, then `χ_local = 0`.

### Claim 6

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: 3. **Zero collapse on phase gate.** If R = 0 (no phase transition), then `χ_local = 0`.

### Claim 7

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: 4. **Strict positivity.** If all numeric factors are positive AND R = 1, then `χ_local > 0`.
