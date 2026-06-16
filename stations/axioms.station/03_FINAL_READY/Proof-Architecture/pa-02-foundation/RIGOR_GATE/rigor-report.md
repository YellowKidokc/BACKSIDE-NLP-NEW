# Rigor Gate: pa-02-foundation

- Series: `Proof-Architecture`
- Verdict: `NEEDS_RIGOR`
- Generated: `2026-06-03T08:03:59`
- Source JSON: `\\dlowenas\brain\Backside\stations\axioms.station\03_FINAL_READY\Proof-Architecture\pa-02-foundation\JSON\pa-02-foundation.paper-grade.json`
- Claim count: 6
- Failing claim count: 6
- Formal marker count: 2

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

- weak:Q3_mechanism: 2
- weak:Q4_evidence: 6
- weak:Q5_falsifiability: 6
- weak:Q6_boundary: 6

## Claim Checks

### Claim 1

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: ::: :::::: ::::::::: :::::::::::::::::::: {.grid .two} ::::::::::::::: {} :::: {.node .axiom} ::: tag

### Claim 2

- Status: `FAIL`
- Failures: weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: Denial is self-refuting because denial itself presupposes a real act. :::: :::: {.node .derivation} ::: tag

### Claim 3

- Status: `FAIL`
- Failures: weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: Information is treated as primitive because every rival primitive borrows distinction-language to describe itself. :::: :::: {.node .definition} ::: tag

### Claim 4

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: It requires a real substrate in which distinctions are borne. :::: :::: {.node .commitment} ::: tag

### Claim 5

- Status: `FAIL`
- Failures: weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: **Matter primitive:** dead-ends because matter is only specified by properties, and properties are informational distinctions. **Math primitive:** dead-ends because abstract relations describe but do not instantiate a causal substrate. **Consciousness primitive:** dead-ends because consciousness itself requires an account of distinction, state, and substrate. **Emergent information:** dead-ends because emergence presupposes a more basic structure to emerge from. :::

### Claim 6

- Status: `FAIL`
- Failures: weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: ::: eq Existence → Distinction → Information → Substrate → Self-Grounding → Logos Field → Axiom System ::: ::: callout This page is the entry gate.
