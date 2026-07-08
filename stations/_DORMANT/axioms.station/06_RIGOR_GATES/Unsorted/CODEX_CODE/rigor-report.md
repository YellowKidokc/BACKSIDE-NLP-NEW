# Rigor Gate: CODEX_CODE

- Series: `Unsorted`
- Verdict: `NEEDS_RIGOR`
- Generated: `2026-06-03T08:04:00`
- Source JSON: `\\dlowenas\brain\Backside\stations\axioms.station\03_FINAL_READY\Unsorted\CODEX_CODE\JSON\CODEX_CODE.paper-grade.json`
- Claim count: 2
- Failing claim count: 2
- Formal marker count: 15

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

- weak:Q3_mechanism: 1
- weak:Q4_evidence: 1
- weak:Q5_falsifiability: 2
- weak:Q6_boundary: 2

## Claim Checks

### Claim 1

- Status: `FAIL`
- Failures: weak:Q3_mechanism, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: This package contains the Codex Lean 4 work for the narrow Master Equation product test only.

### Claim 2

- Status: `FAIL`
- Failures: weak:Q4_evidence, weak:Q5_falsifiability, weak:Q6_boundary
- Claim: Version B is the cleaner formalization target for the Master Equation product layer because it removes the sign-instability caused by raw signed `M`.
