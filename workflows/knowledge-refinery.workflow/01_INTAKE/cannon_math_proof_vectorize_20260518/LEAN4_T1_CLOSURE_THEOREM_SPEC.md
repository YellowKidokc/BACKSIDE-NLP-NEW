# Lean 4 Spec — T1 Closure Theorem

Run context: 2026-05-18  
Status: Lean-facing spec before implementation  
Purpose: define the first kernel theorem for the OT diagnostic chain.

## Core Theorem

T1 is the spine theorem:

> Reference states are not constructible from error states using only error-closed operations.

This is not theology yet. It is a closure theorem.

## Informal Statement

If a system is inside the error/corruption class, and every operation available from inside that class maps error states back into error states, then no finite composition of those operations produces an uncorrupted reference state.

Plain version:

> You cannot build the standard from the failures.

## Mathematical Shape

Let:

```text
R = ReferenceClass
E = ErrorClass
R ∩ E = ∅
```

Let:

```text
ErrorClosed(f) := ∀ x, E x -> E (f x)
```

Then:

```text
∀ f_i : State -> State,
  all f_i are ErrorClosed ->
  x ∈ E ->
  compose([f_1, ..., f_n], x) ∉ R
```

## Lean Skeleton

```lean
universe u

namespace OTDiagnostic

variable {State : Type u}

variable (Error : State -> Prop)
variable (Reference : State -> Prop)

def ErrorClosed (f : State -> State) : Prop :=
  forall x : State, Error x -> Error (f x)

def ComposeList : List (State -> State) -> State -> State
  | [], x => x
  | f :: fs, x => ComposeList fs (f x)

theorem error_closed_compose
    (ops : List (State -> State))
    (hops : forall f, f ∈ ops -> ErrorClosed Error f)
    {x : State}
    (hx : Error x) :
    Error (ComposeList ops x) := by
  induction ops generalizing x with
  | nil =>
      exact hx
  | cons f fs ih =>
      apply ih
      intro g hg
      exact hops g (by simp [hg])
      exact hops f (by simp)

theorem not_reference_after_error_closed_compose
    (ops : List (State -> State))
    (hops : forall f, f ∈ ops -> ErrorClosed Error f)
    (disjoint : forall x, Error x -> not (Reference x))
    {x : State}
    (hx : Error x) :
    not (Reference (ComposeList ops x)) := by
  exact disjoint (ComposeList ops x)
    (error_closed_compose Error ops hops hx)

end OTDiagnostic
```

## Important Lean Notes

The above skeleton may require minor syntax fixes depending on Lean imports and list membership notation.

The logical content is simple:

1. `ErrorClosed` operations preserve `Error`.
2. finite composition of preserving operations preserves `Error`.
3. `Error` and `Reference` are disjoint.
4. therefore error-closed operations cannot produce `Reference`.

## Case A — Pure Closure

Formal assumption:

```text
All self-generated operations are ErrorClosed.
```

Theorem:

```text
SelfGenerated operations cannot restore Reference.
```

Bridge:

> human moral effort, law, philosophy, education, and willpower can rearrange brokenness but cannot reconstruct the uncorrupted reference state by themselves.

Status:

> cleanest first Lean target

## Case B — Trace Coupling / Prevenient Grace

Problem:

Human beings appear able to recognize good partially:

- conscience
- moral intuition
- creation testimony
- law written on the heart
- repentance

So not every moral recognition should be treated as purely self-generated `E -> E`.

Formal distinction:

```text
SelfGenerated(f) -> ErrorClosed(f)
TraceCoupled(g) -> carries partial Reference signal
```

Trace coupling is received, not generated from `E`.

### Proposed Additional Objects

```lean
variable (Trace : State -> Prop)
variable (Openness : State -> Prop)

def EnablesOpenness (g : State -> State) : Prop :=
  forall x, Error x -> Openness (g x)

def NotRestoring (g : State -> State) : Prop :=
  forall x, Error x -> not (Reference (g x))
```

Conceptual axiom:

```text
background trace signal can enable O > 0
but does not by itself produce Reference membership
```

Bridge:

> conscience and creation testimony orient the person toward the reference, but do not restore the person to the reference.

Theological label:

> prevenient/background grace

## Case B Formal Target

```lean
def EnablesOpenness (Error Openness : State -> Prop) (g : State -> State) : Prop :=
  forall x, Error x -> Openness (g x)

def NotReferenceRestoring (Error Reference : State -> Prop) (g : State -> State) : Prop :=
  forall x, Error x -> not (Reference (g x))
```

Then the bridge theorem is not:

```text
trace coupling restores
```

but:

```text
trace coupling may orient without restoring
```

## Why Case B Matters

Case B prevents a false dilemma:

- If humans recognize good, T1 is false.
- If T1 is true, humans cannot recognize good.

Correct distinction:

> recognition can be trace-coupled without being self-restorative.

This explains:

- conscience is real
- repentance is real
- moral insight is real
- natural law is real
- but none of these equal full restoration

## Relation To T8 / T9 / T10

### T8 — Sign Invariance

T8 becomes a corollary:

> error-closed operations preserve the error/orientation class.

### T9 — Openness Is Not Restoration

T9 becomes the Case B distinction:

> `O > 0` can be enabled without `Reference` being restored.

### T10 — External Grace Required

T10 follows:

> reference restoration requires a non-error-closed, reference-bearing operation.

## Physics Bridge

Goldstone / phase-transition mapping:

- broken phase = `ErrorClass`
- symmetric phase = `ReferenceClass`
- Goldstone modes = internal operations within `ErrorClass`
- external critical input = non-error-closed operation
- phase transition = restoration

Use as:

> physics instance of the abstract closure theorem

Not as:

> imported theological proof

## What This Proves

Under definitions:

> closed operations cannot leave the class they are closed over.

With disjoint reference/error classes:

> error-closed operations cannot produce reference states.

## What This Does Not Prove

It does not prove:

- product form
- Christianity
- incarnation
- resurrection
- that every human operation is error-closed
- that conscience is self-generated
- that grace is personal

Those are bridge or later-module questions.

## First Implementation Recommendation

Implement in this order:

1. `ReferenceState.lean`
2. `T1SpineClosure.lean`
3. `TraceCoupling.lean`
4. only then `SignInvariance.lean` / `OpennessGrace.lean`

## Review Gate

Before coding, reviewers must answer:

1. Are `Error` and `Reference` cleanly disjoint?
2. Are `SelfGenerated` and `ErrorClosed` equivalent, or does self-generation need a stricter definition?
3. Does conscience belong to Case A or Case B?
4. Is trace coupling enough to explain moral recognition without restoration?
5. What would falsify the closure mapping?

## Status

> `LEAN SPEC READY FOR REVIEW / FIRST KERNEL TARGET`
