# Layer 6 - Mathematical / Lean Skeleton
## Codex Pass for Q02-Q25
### David Lowe | POF 2828 | 2026-05-18

## Scope

This is Codex's Layer 6 pass only. It does not write hooks, story, metaphysics,
theology, physics, or objections. It maps each question to the current Lean 4 T1
kernel and labels the claim honestly:

- **FORMAL** - directly supported by a proved Lean theorem under explicit premises.
- **BRIDGE** - structurally mapped to Lean, but the domain interpretation is not
  itself a theorem.
- **OPEN** - needs a new Lean module, Python/Colab model, historical argument, or
  domain premise before theorem-level status.

Active kernel: `lean_t1_kernel/T1Kernel.lean`

Clean build status: `lake clean; lake build T1Kernel` passes with 19 jobs.

Active imported Lean scan: no `sorry`, no `admit`, no `axiom`.

Freeze package SHA-256:
`51f1e6aa7fb52d6e8239eb7bbef14698f9c70a11664ff7dc40baa8ed0a745800`

## Current Lean Module Library

| Module | Use |
|---|---|
| `Closure.lean` | Error-preserving operation lists cannot reach reference. |
| `TraceCoupling.lean` | Restates closure in path/coupling language. |
| `OpennessGrace.lean` | Openness is reception posture, not transformation operation. |
| `TargetedOpenness.lean` | Actual/reference openness is distinct from false/counterfeit openness. |
| `ExternalOperator.lean` | Any error-to-reference path contains an external operation. |
| `StepExternality.lean` | The external operation can be localized in the path. |
| `StepReception.lean` | Received actual-target external step entails actual openness. |
| `NecessaryConditions.lean` | Failed necessary condition blocks integrated coherence. |
| `VariableNecessity.lean` | Candidate variables cannot enter product gate without evidence. |
| `RestorationProfile.lean` | Bundles minimum restoration skeleton. |
| `ContinuityIdentity.lean` | Restoration is distinguished from replacement by identity continuity. |
| `RivalModels.lean` | Generic rival failure gates. |
| `RivalModelInstances.lean` | Named rivals inherit gates only under explicit premise patterns. |
| `JusticeMercyTransform.lean` | Error-preserving self-generated operator cannot satisfy weak J/M/T. |
| `SignInvariance.lean` | Orientation/sign preservation under explicit sign-preserving assumptions. |

---

## Q02 - Ontological Rightness

**Core claim:** Righteousness is structural, not merely opinion.

**Lane status:** BRIDGE with FORMAL support.

**Lean mapping:** Model "rightness" as a `Reference : State -> Prop` and
"wrongness/error" as `Error : State -> Prop`, with disjointness supplied. Under
that structure, `Closure.lean` proves error-preserving operations cannot reach
reference.

**What is proven:** If moral failure is instantiated as an error class and
righteousness as a reference class, self-generated error-closed operations do
not produce righteousness.

**What is not proven:** Lean does not prove that morality is ontologically real
or that a specific moral reference exists. That is a metaphysical/theological
premise.

**Next target:** `MoralReference.lean` could define the exact premise package:
`MoralReference`, `MoralError`, disjointness, and any graded-vs-threshold moral
registers.

---

## Q03 - Error Correction

**Core claim:** Coherence precedes drift; correction requires reference.

**Lane status:** FORMAL for closure; OPEN for statistical/computational error
correction.

**Lean mapping:** `Closure.lean`, `ExternalOperator.lean`, and
`StepExternality.lean`.

**What is proven:** If all available correction operations preserve the error
class, no finite composition reaches reference. If a finite path does reach
reference, at least one operation in the path is external to error closure.

**What is not proven:** Lean has not yet modeled parity bits, checksums,
Reed-Solomon codes, DNA repair, Shannon channel correction, or probability of
life-permitting coherence.

**Next target:** Python/Colab first: simulate corruption/recovery with and
without a reference/checksum/backup. Later Lean target:
`ErrorCorrectionReference.lean`.

---

## Q04 - Resurrection Uniqueness

**Core claim:** Jesus's resurrection claim is structurally unique.

**Lane status:** OPEN / BRIDGE.

**Lean mapping:** `RestorationProfile.lean` can specify what a successful
restoration profile would need: external step, actual-target reception,
integrated coherence, J/M/T witness, and non-self-generated restoration.

**What is proven:** Only the profile structure is formalized. The kernel can say
what a restoration path must include if it exists.

**What is not proven:** Lean does not prove the resurrection, historical
uniqueness, witness reliability, or that Jesus satisfies the profile.

**Next target:** `ResurrectionFeatureProfile.lean` for a formal checklist only:
death boundary, identity continuity, public verification, non-replacement,
reference-carrying operator. Historical evidence remains outside Lean.

---

## Q05 - Death Defeat

**Core claim:** God defeats death, not merely avoids it.

**Lane status:** OPEN with BRIDGE support.

**Lean mapping:** `ContinuityIdentity.lean`, `RestorationProfile.lean`, and a
future `DeathBoundary.lean`.

**What is proven:** Identity-preserving paths preserve the subject; replacement
is formally distinct from restoration. A restoration profile can include a
terminal reference state.

**What is not proven:** Death is not yet modeled as a boundary operator or final
state transition in Lean.

**Next target:** `DeathBoundary.lean`:
`DeathBoundary state`, `SurvivesBoundary op state`, `DefeatsDeath op` as a
relation stronger than `AvoidsDeath`.

---

## Q06 - Board of Directors

**Core claim:** Character outranks raw power.

**Lane status:** BRIDGE with FORMAL support.

**Lean mapping:** `JusticeMercyTransform.lean` and `RestorationProfile.lean`.

**What is proven:** A self-generated error-preserving operator cannot enact weak
mercy and cannot satisfy the weak J/M/T triple. Restoration profile requires
justice, mercy, and transformation together.

**What is not proven:** Lean does not prove "character" as a complete divine
attribute set. It only encodes constraint satisfaction.

**Next target:** `CharacterConstraintProfile.lean` could package power,
justice, mercy, truth, and transformation as independent constraints and show
that raw power alone is under-specified.

---

## Q07 - Design God

**Core claim:** Moral profiles converge.

**Lane status:** OPEN.

**Lean mapping:** Possible connection to `RestorationProfile.lean`, but no
current theorem proves cross-cultural or interreligious convergence.

**What is proven:** The kernel gives a minimum restoration profile once the
problem is stated as error-to-reference restoration.

**What is not proven:** Convergence of human God-concepts is empirical and
comparative, not currently Lean-formal.

**Next target:** Python/Colab "moral profile convergence census" over texts or
traditions; later `ProfileConvergence.lean` can formalize the scoring schema,
not the empirical result.

---

## Q08 - Why Create

**Core claim:** Creation is relational.

**Lane status:** OPEN / BRIDGE.

**Lean mapping:** `TraceCoupling.lean`, `OpennessGrace.lean`, and
`StepReception.lean` provide relation/coupling vocabulary, but they do not prove
creation.

**What is proven:** Reception/coupling can be modeled separately from
transformation. Openness is a posture that enables relation.

**What is not proven:** Lean does not prove that God creates, that creation is
motivated by love, or that relation is metaphysically necessary.

**Next target:** `RelationalCreation.lean` only after exact premises are stated:
personhood, relation, otherness, voluntary coupling.

---

## Q09 - Worship Robots

**Core claim:** Free will is necessary for love/worship.

**Lane status:** OPEN with BRIDGE support.

**Lean mapping:** `OpennessGrace.lean` and `TargetedOpenness.lean`.

**What is proven:** Openness is a posture/reception condition, not the restoring
operation. Actual-target openness differs from false-target openness.

**What is not proven:** The kernel does not formalize free will, coercion,
love, worship, or libertarian-vs-compatibilist agency.

**Next target:** `AgencyOpenness.lean`: distinguish `Agency`, `CanRefuse`,
`ForcedPosture`, and `VoluntaryOpenTo`.

---

## Q10 - Paradise Test

**Core claim:** Universal failure under freedom and time.

**Lane status:** OPEN for probability; BRIDGE for post-failure closure.

**Lean mapping:** `NecessaryConditions.lean`, `VariableNecessity.lean`,
`Closure.lean`.

**What is proven:** If a necessary condition fails, integrated coherence fails.
If failure places the state in an error-closed class, self-generated operations
cannot restore reference.

**What is not proven:** The probability claim "failure approaches 1 under
freedom plus time" is not in Lean.

**Next target:** Python/Colab stochastic model first. Lean target later:
`FailureAbsorption.lean` for absorbing states and necessary-condition collapse.

---

## Q11 - Who Gets In

**Core claim:** Merit fails as a restoration mechanism.

**Lane status:** FORMAL under the self-repair premise.

**Lean mapping:** `Closure.lean`, `RivalModels.lean`, `JusticeMercyTransform.lean`.

**What is proven:** If merit/self-improvement is modeled as an error-preserving
self-repair operation, it cannot enact weak mercy and cannot satisfy weak J/M/T.

**What is not proven:** Lean does not prove that every actual merit system is
error-preserving. That premise must be supplied per model.

**Next target:** `MeritModelInstances.lean` could instantiate specific merit
models only when their premises are stated precisely.

---

## Q12 - Pure Mercy

**Core claim:** Mercy alone corrupts restoration if transformation is absent.

**Lane status:** BRIDGE / OPEN.

**Lean mapping:** `RestorationProfile.lean` requires justice, mercy, and
transformation together in its profile. `JusticeMercyTransform.lean` proves
self-generated J/M/T failure under error preservation.

**What is proven:** The current profile packages transformation as required for
restoration. Self-generated error-preserving operations cannot satisfy the
triple.

**What is not proven:** A theorem specifically showing `Mercy AND NOT
Transforming -> CorruptionReturns` is not yet written.

**Next target:** `PartialConstraintFailure.lean` with theorems for
`mercy_without_transform_fails`, `justice_without_mercy_fails`, and
`justice_mercy_without_transform_fails`.

---

## Q13 - Pure Justice

**Core claim:** Justice alone empties the system.

**Lane status:** OPEN / BRIDGE.

**Lean mapping:** `JusticeMercyTransform.lean` and `RestorationProfile.lean`.

**What is proven:** Restoration profile includes mercy and transformation; the
kernel does not treat justice alone as sufficient.

**What is not proven:** Lean does not yet define punishment, destruction,
people-lost, or "empty heaven/system" states.

**Next target:** `JusticeAlone.lean`: define `Penalty`, `Destroyed`,
`Restored`, and prove that a justice-only operator lacking mercy is not a
restoration operator.

---

## Q14 - Resume vs Posture

**Core claim:** Posture matters more than performance.

**Lane status:** BRIDGE with FORMAL support.

**Lean mapping:** `OpennessGrace.lean`, `TargetedOpenness.lean`,
`StepReception.lean`.

**What is proven:** Openness is a reception posture. Actual-target reception
requires actual-target openness. False-target openness is insufficient for
actual reception.

**What is not proven:** Lean does not evaluate human motives, humility, pride,
or "resume" as social performance.

**Next target:** `PostureVsPerformance.lean`: model `BehaviorOutput` separately
from `OpenTo actual`.

---

## Q15 - Righteousness Sees

**Core claim:** Divine holiness is thresholded.

**Lane status:** OPEN with BRIDGE support.

**Lean mapping:** `NecessaryConditions.lean` and `VariableNecessity.lean`.

**What is proven:** If holiness/compatibility is supplied as a necessary
condition, failure of that condition blocks integrated coherence.

**What is not proven:** Lean does not prove the holiness threshold itself. That
threshold is a theological premise unless separately formalized.

**Next target:** `HolinessThreshold.lean`: distinguish graded human severity
from binary compatibility with perfect holiness.

---

## Q16 - Why Blood

**Core claim:** Life-cost is real; wrong is not costless.

**Lane status:** OPEN.

**Lean mapping:** Current J/M/T modules speak of justice and mercy, but there is
no formal moral ledger, debt, life-cost, blood, or substitution currency yet.

**What is proven:** Self-generated error-preserving operations cannot satisfy
weak J/M/T.

**What is not proven:** The necessity of blood/life-cost is not in the current
kernel.

**Next target:** `MoralLedger.lean`: define debt, cost-bearing, transfer,
non-erasure, and satisfaction. This is a new layer, not T1 kernel.

---

## Q17 - Temporary Covering

**Core claim:** Covering is not completion.

**Lane status:** OPEN / BRIDGE.

**Lean mapping:** `NecessaryConditions.lean`, `RestorationProfile.lean`.

**What is proven:** Completion can be represented as terminal reference plus
integrated coherence under necessary conditions.

**What is not proven:** Repetition, covering coefficient alpha, provisionality,
or annual sacrifice are not formalized.

**Next target:** `CoveringCompletion.lean`: define `Covers`, `Completes`,
`RequiresRepetition`, and prove `RequiresRepetition op -> Not (Completes op)`
under exact definitions.

---

## Q18 - Parent Calls

**Core claim:** Trust can precede full comprehension.

**Lane status:** BRIDGE / OPEN.

**Lean mapping:** `OpennessGrace.lean` and `StepReception.lean`.

**What is proven:** Reception posture is separable from the transforming
operation. A state may be open before it understands or performs transformation.

**What is not proven:** Trust, obedience, parental authority, danger, and
partial knowledge are not yet modeled.

**Next target:** `TrustUnderPartialKnowledge.lean`: distinguish `KnowsAll`,
`TrustsSource`, `ReceivesInstruction`, and `ActsBeforeFullComprehension`.

---

## Q19 - Honest Obedience

**Core claim:** True posture is not the same as emotional enthusiasm.

**Lane status:** BRIDGE with FORMAL support.

**Lean mapping:** `TargetedOpenness.lean` and `StepReception.lean`.

**What is proven:** Actual-target openness is the relevant reception condition,
not generic openness or false-target openness.

**What is not proven:** Lean does not model reluctance, emotional state,
Gethsemane, or sincerity.

**Next target:** `HonestPosture.lean`: model `EmotionState` as distinct from
`OpenTo actual`, so reluctance need not negate true openness.

---

## Q20 - OT Triage

**Core claim:** Pre-cure containment is different from final cure.

**Lane status:** OPEN.

**Lean mapping:** Current static kernel supports externality and restoration
profiles, but has no historical phase/dynamics model.

**What is proven:** Restoration from error to reference requires externality
under T1 premises.

**What is not proven:** Flood, Sodom, conquest, exile, covenant preservation,
containment, or phase-era distinction are not formalized.

**Next target:** Python/Colab dynamics first; Lean later:
`TriageContainment.lean` with `ContainsSpread`, `CuresCondition`, and
`PreCureRegime`.

---

## Q21 - Same God

**Core claim:** Character constant; operating conditions change.

**Lane status:** OPEN / BRIDGE.

**Lean mapping:** Could reuse the same operator/profile with different regime
parameters, but no regime model exists yet.

**What is proven:** None directly. Existing kernel can keep requirements
constant across paths, but does not model historical covenants or epochs.

**What is not proven:** OT/NT continuity, covenant-history, and changing
conditions are theological/historical claims outside the current kernel.

**Next target:** `RegimeChange.lean`: same `RequiredSolution` constraints under
different `AvailableOperations` or `CouplingRegime`.

---

## Q22 - Why Not Teacher

**Core claim:** Information does not fix nature.

**Lane status:** FORMAL under the information-as-error-preserving premise.

**Lean mapping:** `Closure.lean`, `RivalModels.lean`,
`JusticeMercyTransform.lean`.

**What is proven:** If teaching/information is modeled as an operation that
preserves the error class, it cannot restore reference and cannot satisfy weak
J/M/T.

**What is not proven:** Lean does not prove that all teaching is
error-preserving; that premise must be defended by theology/psychology.

**Next target:** `LawDiagnosis.lean`: define diagnostic information separately
from regenerative transformation.

---

## Q23 - Why Death

**Core claim:** The cross is mechanism, not theater.

**Lane status:** OPEN / BRIDGE.

**Lean mapping:** `JusticeMercyTransform.lean`, `RestorationProfile.lean`, and
future `DeathBoundary.lean` / `MoralLedger.lean`.

**What is proven:** Restoration profile requires externality, actual reception,
integrated coherence, and weak J/M/T. The J/M/T witness cannot be
self-generated/error-preserving.

**What is not proven:** The cross, substitution, death-as-debt, atonement
mechanism, or uniqueness of Christ are not proved by the T1 kernel.

**Next target:** `AtonementMechanism.lean` after `MoralLedger.lean` and
`DeathBoundary.lean` exist.

---

## Q24 - Why Rise

**Core claim:** Resurrection verifies completion.

**Lane status:** OPEN / BRIDGE.

**Lean mapping:** `RestorationProfile.lean`, `ContinuityIdentity.lean`,
`NecessaryConditions.lean`.

**What is proven:** A terminal reference state can be part of a restoration
profile. Identity preservation distinguishes restoration from replacement.
Integrated coherence follows if listed conditions are necessary and terminal
reference holds.

**What is not proven:** Historical resurrection, empirical witness, death
reversal, or verification protocol are not formalized.

**Next target:** `VerificationAfterBoundary.lean`: define post-boundary witness,
identity continuity, and terminal reference as a formal verification profile.

---

## Q25 - Final Trust

**Core claim:** Faith is rational trust, not blind proof-denial.

**Lane status:** BRIDGE / OPEN.

**Lean mapping:** `OpennessGrace.lean`, `TargetedOpenness.lean`,
`StepReception.lean`.

**What is proven:** Actual-target openness is required for actual-target
reception. Openness is not itself the restoring operation.

**What is not proven:** Faith, rational warrant, testimony, evidence, love, and
trust are not formalized in the T1 kernel.

**Next target:** `FaithAsTrust.lean`: model `Evidence`, `TrustsSource`,
`OpenTo actual`, and `ReceivesActual` without collapsing faith into certainty.

---

## Summary

The current T1 kernel directly supports the earliest structural claims and the
restoration-impossibility spine. Later questions increasingly become NT
fulfillment, moral ledger, death-boundary, dynamics, history, and faith/trust
modules.

The honest map is:

- **Q02-Q03:** closest to T1 and error-correction formalization.
- **Q10-Q15 and Q22:** strongest current Lean support under explicit premises.
- **Q04-Q05 and Q23-Q24:** require a future NT fulfillment layer.
- **Q16-Q17:** require moral-ledger and covering/completion modules.
- **Q20-Q21:** require dynamics/regime modeling.
- **Q25:** requires faith/trust epistemology formalization.

Do not present this layer as proving the full chain. Present it as the formal
skeleton map: where Lean already holds, where bridge claims sit, and where the
next formal modules must be built.
