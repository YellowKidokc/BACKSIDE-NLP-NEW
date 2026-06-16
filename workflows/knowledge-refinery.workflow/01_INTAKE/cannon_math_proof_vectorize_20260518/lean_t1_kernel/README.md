# T1 Kernel Lean Package

Status: first-pass Lean 4 kernel for the T1 closure theorem and immediate
corollaries.

Lean version: `4.29.1`

## Scope

This package proves local formal skeletons only:

> Given one abstract state space with disjoint `Error` and `Reference`
> predicates, any finite list of error-preserving operations maps an error start
> state to another error state; therefore it cannot produce a reference state.

It also proves the first corollary layer:

- error-closed traces preserve error through coupling;
- openness is a posture/reception condition, not an operation;
- actual/reference openness is distinct from false/counterfeit openness;
- any finite restoration path from error to reference contains an operation
  external to the error class;
- that external operation can be localized as a prefix/operation/suffix step;
- received localized external steps entail actual/reference openness;
- product-form reasoning is gated behind explicit joint necessity;
- variable candidates cannot enter the product gate until they are proven
  necessary or explicitly assumed necessary by a domain model;
- minimum restoration profile bundles external step, actual openness,
  integrated coherence, and weak J/M/T constraints;
- identity-preserving paths cannot replace the subject they restore;
- rival failure gates cover self-repair, decree-only, replacement,
  false-openness, and necessary-condition failure patterns;
- named rival instances inherit those gates only when their exact formal
  premises are supplied;
- sign invariance holds under explicitly sign-preserving operations;
- a self-generated error-preserving operator cannot enact mercy or satisfy the
  weak J/M/T triple.

## Not In Scope

- Numeric product form.
- Specific-variable necessity for any named theological variable.
- Whole-system defeat of named religions or traditions.
- Mediator uniqueness.
- Incarnation, cross, resurrection, Pentecost.
- Science-arm proof.
- Theology as theorem.

## Build

```powershell
lake build T1Kernel
```

## Core Files

- `T1Kernel/Closure.lean`
- `T1Kernel/TraceCoupling.lean`
- `T1Kernel/OpennessGrace.lean`
- `T1Kernel/TargetedOpenness.lean`
- `T1Kernel/ExternalOperator.lean`
- `T1Kernel/StepExternality.lean`
- `T1Kernel/StepReception.lean`
- `T1Kernel/NecessaryConditions.lean`
- `T1Kernel/VariableNecessity.lean`
- `T1Kernel/RestorationProfile.lean`
- `T1Kernel/ContinuityIdentity.lean`
- `T1Kernel/RivalModels.lean`
- `T1Kernel/RivalModelInstances.lean`
- `T1Kernel/SignInvariance.lean`
- `T1Kernel/JusticeMercyTransform.lean`
