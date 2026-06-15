# Lean 4 T1 Kernel Boundary Audit

Date: 2026-05-18

## Purpose

This audit labels what the active Lean kernel proves, what it merely specifies,
what remains a bridge claim, and what is blocked from theorem status.

The goal is to prevent the prose from implying more than the Lean files prove.

## Active Root

Root module:

`lean_t1_kernel/T1Kernel.lean`

Active imported modules:

1. `ReferenceState.lean`
2. `Closure.lean`
3. `TraceCoupling.lean`
4. `OpennessGrace.lean`
5. `TargetedOpenness.lean`
6. `ExternalOperator.lean`
7. `StepExternality.lean`
8. `StepReception.lean`
9. `NecessaryConditions.lean`
10. `VariableNecessity.lean`
11. `RestorationProfile.lean`
12. `ContinuityIdentity.lean`
13. `RivalModels.lean`
14. `RivalModelInstances.lean`
15. `SignInvariance.lean`
16. `JusticeMercyTransform.lean`

Legacy/non-root module:

- `T1SpineClosure.lean` remains present but is not imported by the root.

## Theorem Lane: Proven Local Skeletons

These are genuine Lean results in the active root import chain.

| Module | Proven Content |
|---|---|
| `Closure.lean` | Error-preserving finite operation lists cannot carry an error state to reference when `Error` and `Reference` are disjoint. |
| `TraceCoupling.lean` | The closure theorem restated in path/coupling language. |
| `OpennessGrace.lean` | Openness is a reception condition/posture, not a transformation operation. Error and openness are compatible. |
| `TargetedOpenness.lean` | Openness can be target-indexed; actual-target reception entails actual openness; false-target openness is insufficient when actual openness is absent/excluded. |
| `ExternalOperator.lean` | Any finite path from error to reference contains at least one operation external to the error class. |
| `StepExternality.lean` | The external operation witness can be localized as `before ++ op :: after`. |
| `StepReception.lean` | A localized external step received through the actual target entails actual openness; absent actual openness blocks that reception. |
| `NecessaryConditions.lean` | If integrated coherence is defined as the conjunction of listed necessary conditions, any failed listed condition blocks integrated coherence. |
| `VariableNecessity.lean` | Product-gate variables are separated into proven, assumed, and candidate status; candidates cannot enter the gate without usable necessity evidence. |
| `SignInvariance.lean` | Sign/orientation preservation holds under explicit sign-preserving assumptions; error-to-reference sign crossing is blocked under explicit error-negative/reference-positive assumptions. |
| `JusticeMercyTransform.lean` | A self-generated error-preserving operator cannot enact weak mercy and therefore cannot satisfy the weak J/M/T triple. |
| `RestorationProfile.lean` | A bundled minimum profile entails localized external step, actual openness, integrated coherence, weak J/M/T, and non-self-generated J/M/T witness. |
| `ContinuityIdentity.lean` | Identity-preserving paths preserve start-to-terminal identity; paths that change identity contain a replacement operation. |
| `RivalModels.lean` | Minimal rival failure gates: self-repair/decree-only fail weak mercy/JMT, replacement fails continuity, false openness blocks actual reception, failed necessary condition blocks integrated coherence. |
| `RivalModelInstances.lean` | Named rival records inherit failure gates only when their exact formal premise pattern is supplied; labels alone prove nothing. |

## Specification Lane: Named Structures, Not Existence Proofs

These definitions package requirements. They do not prove that a concrete
theological candidate satisfies them.

| Structure/Definition | Status |
|---|---|
| `OTSolutionProfile` | Specification of externality, compatibility, voluntary coupling, continuity, justice, mercy, transformation. |
| `RestorationProfile` | Type-valued evidence package bundling the local restoration skeleton. |
| `IntegratedCoherence` | Logical conjunction of listed conditions, not yet numeric `chi = product C_i`. |
| `VariableSpec` | Named variable proposal with status marker; does not prove any named variable belongs in the product form. |
| `RivalLabel` | Human-readable rival label with no theorem power by itself. |
| `ExternalStepReceivedActual` | Packaging of localized external operation plus actual-target reception. |

## Bridge Lane: Interpretive Claims

These are supported by the formal shape but are not themselves Lean theorems.

| Bridge Claim | Lean Support | Boundary |
|---|---|---|
| Self-salvation is impossible | `Closure`, `ExternalOperator` | Only under the premise that self-generated operations preserve `Error`. |
| Grace is required | `ExternalOperator` | Lean proves externality required, not that grace exists or who/what grace is. |
| Repentance is posture, not repair | `OpennessGrace` | Lean models reception posture; theological repentance is bridge language. |
| Lord-Lord / false vacuum problem | `TargetedOpenness`, `StepReception` | Lean proves target distinction, not divine heart-knowledge. |
| Product-form severity | `NecessaryConditions`, `VariableNecessity` | Lean proves logical conjunction/zero-gate and candidate gating, not numeric product severity or named-variable necessity. |
| J/M/T profile narrows candidates | `JusticeMercyTransform`, `RestorationProfile`, `RivalModelInstances` | Lean proves weak premise-pattern failures, not final rival-system defeat. |

## Blocked From Theorem Status

Do not present these as proven by the current kernel.

- Christianity uniqueness.
- Trinity.
- Incarnation.
- Cross necessity.
- Atonement uniqueness.
- Resurrection.
- Pentecost.
- Hiddenness.
- Soul speculation.
- Specific identity of the external operator.
- Specific variable list for the product form.
- Numeric convergence or dynamical-system claims.
- Physics isomorphism claims such as Goldstone/phase transition as theorem.

## Current Strongest Formal Claim

The current kernel proves:

> Given disjoint `Error` and `Reference` predicates, any finite restoration path
> from an error state to a reference state must include a path-localized operation
> external to the error class; if that operation is received through an actual
> target, the receiving state must be actually open to that target; and if
> integrated coherence is modeled as a conjunction of necessary conditions, any
> failed necessary condition blocks integrated coherence.

That is the safe theorem-level spine.

## Current Weakest Remaining Links

1. **Named-variable necessity** — `VariableNecessity.lean` blocks candidate
   smuggling, but does not prove which theological variables are necessary.
2. **Operator identity** — `ExternalOperator.lean` proves an external operation
   exists in the path, not that it is Christ, grace, incarnation, or any named
   theological operator.
3. **J/M/T richness** — current J/M/T definitions are intentionally weak.
   `RivalModelInstances.lean` maps exact premise patterns, not full rival systems.
4. **Continuity richness** — `ContinuityIdentity.lean` handles identity labels,
   but not memory, embodiment, resurrection body, or personal-history metaphysics.
5. **Dynamics** — no differential equation or convergence proof is in this
   kernel yet.

## Recommended Next Move

Do not widen to NT uniqueness yet.

The next Lean target should be one of:

1. `NamedVariablePremises.lean` — only if the framework supplies exact
   necessity premises for specific variables.
2. `Dynamics.lean` — only after the static skeleton remains stable.
3. NT fulfillment modules — only after a separate boundary document is written.

Recommended order:

1. Freeze and publish the T1 kernel.
2. `NamedVariablePremises.lean`
3. `Dynamics.lean`

Reason: the static T1 kernel now has closure, externality, reception,
continuity, variable gating, and rival-instance gating. Further work should be
versioned as a new layer, not silently mixed into the kernel.
