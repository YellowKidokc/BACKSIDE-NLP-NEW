# Lean 4 T1 Kernel Corollary Build Report

Date: 2026-05-18

## Result

`lake build T1Kernel` succeeds on Lean `4.29.1`.

## What Changed

- `OpennessGrace.lean` no longer asserts the impossible claim that external
  restoration itself proves openness. It now defines `Receives` so openness is
  an explicit reception condition.
- `JusticeMercyTransform.lean` now proves the weak but real kernel claim:
  self-generated error-preserving operators cannot enact mercy, therefore cannot
  satisfy the weak `JusticePreserving ∧ MercyEnacting ∧ Transforming` triple.
- `TraceCoupling.lean` imports `Closure.lean` directly and restates T1 as a
  coupling theorem.
- `T1Kernel.lean` imports the active `Closure.lean` module instead of the older
  duplicate `T1SpineClosure.lean`.
- `TargetedOpenness.lean` adds the `O_R` vs `O_F` skeleton: untargeted openness
  is too weak; actual/reference reception requires openness to the actual target.
- `ExternalOperator.lean` proves that any finite path from error to reference
  must contain at least one operation external to the error class.
- `StepExternality.lean` proves that the external operation can be localized as
  a concrete prefix/operation/suffix step in the path.
- `StepReception.lean` proves that a localized external step received through
  the actual/reference target entails actual openness, and absent actual
  openness blocks such reception.
- `NecessaryConditions.lean` gates product-form reasoning behind explicit joint
  necessity and proves the binary zero-gate for integrated coherence.
- `VariableNecessity.lean` distinguishes proven, assumed, and candidate
  variables so candidate variables cannot be silently smuggled into the product
  gate.
- `RestorationProfile.lean` bundles localized external reception, actual
  openness, integrated coherence, and weak J/M/T constraints into one minimum
  restoration skeleton.
- `ContinuityIdentity.lean` defines identity preservation vs replacement and
  proves that identity-preserving paths preserve start-to-terminal identity.
- `RivalModels.lean` adds minimal failure gates for self-repair, decree-only,
  replacement, false-openness, and necessary-condition failures.
- `RivalModelInstances.lean` maps labels to those failure gates only when the
  exact premise pattern is supplied; labels alone prove nothing.

## Current Boundary

The build proves local formal skeletons. It does not prove:

- Christianity uniqueness;
- mediator uniqueness;
- incarnation;
- atonement uniqueness;
- resurrection;
- Pentecost;
- specific-variable product-form necessity for any named theological variable;
- whole-system defeat of named religions or traditions;
- `O_R/O_F` target correctness.

## Verification Commands

```powershell
rg -n "sorry|admit|axiom" .\T1Kernel .\T1Kernel.lean
lake clean
lake build T1Kernel
```

The string scan may still find historical documentation in non-imported legacy
files. The active imported modules contain no `sorry`, no `admit`, and no Lean
`axiom` declarations.

## Clean Build Result

`lake clean; lake build T1Kernel` completed successfully with 19 jobs after the
named-rival instance gate was added.

## Package Hash Note

The full-folder ZIP is stored outside this intake folder so it can be hashed
after packaging without a self-changing embedded hash record.
