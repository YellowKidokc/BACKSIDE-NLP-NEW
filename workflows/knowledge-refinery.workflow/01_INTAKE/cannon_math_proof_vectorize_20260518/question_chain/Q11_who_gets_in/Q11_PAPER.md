<!--
PAPER STATUS: consolidated draft for review.
Layer ownership (per broadcast 980):
  L1 hook         = David
  L2 human story  = Jim/Gemini
  L3 metaphysics  = Opus
  L4 theology     = Kimi
  L5 physics      = Opus
  L6 math / Lean  = Codex
  L7 objections   = GPT

Layer-owners: open this file. If you can improve YOUR layer, do it. Replace, don't append. Mark with a single-line edit note at the top of your section: "Polished by <name> on <date>".
-->

# Q11 — Which "Good People" Get In?

## Layer 1: The Hook

**[PENDING: David]**

> *Seed (from index): "Good people go to heaven." Which good people? By whose standard?*

---

## Layer 2: The Human Story

**[PENDING: Jim/Gemini]**

---

## Layer 3: Metaphysical Structure

The claim "good people go to heaven" assumes a threshold and a measurement procedure for goodness. Both are unspecified, and the specification problem is exactly where the claim collapses.

If the threshold is set at "typical human," it is a moving target — the average shifts with population. If the threshold is set at "better than the median," half are below by definition; this is sociology, not justice. If the threshold is set at "any positive net of good acts over bad," the cumulative argument of Q10 over time makes the net unstable. If the threshold is set at "perfect," everyone fails (Q10 again).

The deeper problem: the standard cannot be calibrated from within the population being judged. Agents in the error class cannot ground the reference from inside the error class. To know what "good enough" means requires access to the reference, and access to the reference is what the corruption blocks.

**T1 extension:** Calibration of the reference state cannot be performed by members of the error class using only error-class operations. This is the closure theorem applied to the standard-setting problem. The standard has to come from outside the population being measured, or the measurement is circular.

---

## Layer 4: Theological Register

**[PENDING: Kimi]**

---

## Layer 5: Physics / Science Isomorphism

**Primary standards in metrology.** NIST and BIPM maintain primary physical standards (the kilogram prototype until 2019, atomic clocks for the second) because secondary standards drift relative to each other without an external anchor. The chain of measurement traces back to an absolute reference; any system of measurements that tries to ground itself internally accumulates drift. (BRIDGE: metrological grounding is the same architecture as moral grounding — both require an external primary standard for non-arbitrary measurement.)

**Calibration drift.** Any instrument calibrated against a peer instrument inherits and amplifies the peer's drift. Closed networks of mutual calibration converge on a *consistent* but not *accurate* result. Moral standards calibrated entirely against social consensus have the same architecture — internally consistent, externally untethered.

**Bootstrapping in self-referential systems.** A system that defines its own success criterion can always satisfy itself. The criterion has no purchase against the system unless something external constrains it. Gödel-style limits on self-grounding apply: a sufficiently rich system cannot prove its own consistency from within.

**Status flag:** The metrology analogy is a tight process-isomorphism — both domains genuinely require an external anchor for non-circular measurement. The Gödel reference is illustrative on the structural shape; the formal theorem applies to arithmetic, not to moral grounding directly.

---

## Layer 6: Mathematical / Lean Skeleton

**Source:** Codex (forge) pass -- see `LAYER6_MATHEMATICAL_LEAN_SKELETON_CODEX_Q02_Q25.md` for full kernel mapping.


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

## Layer 7: Objections / Kill Conditions

**[PENDING: GPT]**

> Anticipated rivals: "moral consensus across cultures provides the standard" (response: Q07 convergence argument applies, but consensus is recovery of a shared reference, not the reference itself), "evolutionary fitness provides the standard" (response: evolutionary fitness is descriptive, not normative — gives "what survives," not "what is good"; see Q02).
