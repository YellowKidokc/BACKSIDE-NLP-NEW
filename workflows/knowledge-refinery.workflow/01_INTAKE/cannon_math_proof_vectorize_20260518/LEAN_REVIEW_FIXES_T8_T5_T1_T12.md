# Lean Review Fixes - T8, T5, T1, T12

Run context: 2026-05-18  
Status: reviewer patch applied to Lean transfer draft  
Primary file updated: `LEAN4_PROOF_TRANSFER_DRAFT_OT_DIAGNOSTIC.md`

## Why This Patch Exists

The external review identified three fixable pre-Lean weaknesses and one honest boundary:

1. `T8` could collapse if repentance/openness were treated as a self-generated restoring operation.
2. `T5` named rival models but did not yet construct their failure modes formally.
3. `T1` prose overreached beyond the formal closure theorem unless supported by the science register.
4. `T12` correctly stops at the love/covenant axiom and should not pretend to derive why grace is offered.

## Fix 1 - T8 Operation/Posture Distinction

New definition:

```text
SelfGenerated(Op, state) :=
  Op is computable from state-data alone
  and Op references no source/entity not already present in state
  and Op's output is fully determined by the state's internal structure.

Openness(state) :=
  state has receptive posture toward external input.
```

Interpretive lock:

> `SelfGenerated` names an operation that transforms state. `Openness` names a posture/property of state that permits reception.

This saves the repentance issue:

> Repentance can be `O > 0` without being the restoring operation. The subject can face the doctor, but the facing is not the surgery.

Lean consequence:

> T8 should formalize that self-generated restoring operations preserve the error/orientation class. T9 separately proves that openness without grace has no restoring product: `O > 0 and G = 0 -> O*G*(1-C) = 0`.

## Fix 2 - T5 Rival Model Construction Requirement

Added formal rival table:

| Rival model | Construction | Failure target |
| --- | --- | --- |
| Decree-forgiveness | `AuthorityPardon -> J and M`; orientation unchanged | `not T` if transformation is ontological/orientational |
| Annihilationism | `J` destroys wicked, `M` preserves good, no `T` for destroyed subjects | Violates T11 if destruction replaces restoration; conflicts with covenant persistence if accepted |
| Universalism | `M` applies to all; `J` weakened/deferred or transformation unavoidable | Violates T4 if unmediated sin admitted; risks violating voluntary coupling if coerced |
| Purgatory | `J and M and T` over time through purifying suffering | Must answer T6 provisionality, T4 threshold, and T11 continuity |
| Karma/reincarnation | `J` and `M` distributed across lives/consequences | Requires strong continuity theory; lacks external `G` under T9/T10 |
| Restorative justice without substitution | Offender/community repair harm internally | Fails T4 threshold or T8/T10 if no external reference-bearing operator enters |

Reviewer rule:

> Do not merely name rivals. Build each rival as a formal profile and show which constraint it violates.

## Fix 3 - T1 Formal/Empirical/Bridge Alignment

T1 is now separated into three layers:

```text
T1_FORMAL:
  Error-closed/self-generated operations preserve the error class.

T1_EMPIRICAL:
  The Convergent Coherence Census and error-compounding patch support the claim
  that the observed substrate is coherence-preserving rather than drift-founded.

T1_BRIDGE:
  Only after the formal and empirical layers are kept distinct may the prose argue
  that error is not foundational and coherence-preservation is prior.
```

This prevents the proof from pretending that Lean alone proves ontological priority.

Pointer files:

- `T1_SPINE_THEOREM_REFERENCE_NOT_RECONSTRUCTIBLE.md`
- `LEAN4_T1_CLOSURE_THEOREM_SPEC.md`
- `CONVERGENT_COHERENCE_CENSUS_SCIENCE_ARM_DRAFT.md`
- `PHASE_0_CENSUS_INTEGRATION_REVISION.md`

## Fix 4 - T12 Honest Boundary Preserved

The draft now explicitly says:

> The chain can derive the required profile of grace if grace is offered; it cannot force the divine act of offering grace without a love/covenant axiom or revelation-layer premise.

This is not a weakness to hide. It is the correct stopping line for the OT diagnostic proof.

## Updated Lean Priority

Run the Lean implementation in this order:

1. `ReferenceState.lean`
2. `T1SpineClosure.lean`
3. `TraceCoupling.lean`
4. `OpennessGrace.lean`
5. `SignInvariance.lean`
6. `JusticeMercyTransform.lean` with rival profiles clearly separated from proved constraints

Do not promote product-form, mediator uniqueness, Trinity, incarnation, atonement uniqueness, resurrection, Pentecost, hiddenness, or soul/information claims to theorem status in this kernel pass.

