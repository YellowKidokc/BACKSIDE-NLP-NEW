# Axiom Rigor Protocol

The Axioms folder is not a confidence folder. It is a proof-discipline folder.

## Core Rule

No paper, claim, axiom, theorem, mapping, or proof is treated as accepted merely because it has a generated report.

Generated reports are intake artifacts. The rigor gate decides whether they are usable downstream.

## Status Levels

- `FORMALIZED` - reserved for a verified Lean/Lake build artifact or equivalent machine-checkable proof record.
- `FORMALIZATION_CANDIDATE` - has formal structure and passes the audit gate, but still needs Lean work.
- `AUDIT_READY` - structured enough for downstream use, but not formalized.
- `NEEDS_RIGOR` - do not reuse as accepted; repair missing evidence, mechanism, boundary, falsification, or overclaim issues first.

## Rejection-First Standard

Every serious axiom/theorem candidate needs:

- the positive claim,
- dependency chain,
- named close false positives,
- why each false positive fails,
- evidence boundary,
- kill conditions,
- mistake/overclaim log.

## Lean-Inspired Boundary

This workflow cannot make something Lean 4 true.

It can enforce the discipline around Lean-style work:

- no silent acceptance,
- no label-only theorem claims,
- no marker-shaped proofs,
- no missing false-positive tests,
- no erasing mistakes after the fact.

## Operational Rule

After grading papers, run:

```text
RUN_AXIOM_RIGOR_GATE.bat
```

Then use:

```text
06_RIGOR_GATES\AXIOM_RIGOR_MANIFEST.md
```

as the gatekeeper before moving claims into `claims`, `proofs`, or `mappings`.
