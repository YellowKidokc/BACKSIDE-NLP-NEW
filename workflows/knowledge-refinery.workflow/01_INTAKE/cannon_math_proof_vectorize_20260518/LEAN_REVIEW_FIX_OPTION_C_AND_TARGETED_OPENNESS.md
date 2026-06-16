# Lean Review Fix - Option C and Targeted Openness

Run context: 2026-05-18  
Status: added to Lean transfer draft  
Primary file updated: `LEAN4_PROOF_TRANSFER_DRAFT_OT_DIAGNOSTIC.md`

## Fix 1 - T1 Is Not Category Collapse

The correct repair is Option C:

> State the abstraction explicitly.

T1 is not claiming that technical error, propositional lying, moral sin, and ontological corruption are the same thing.

That would be a category error.

T1 claims that all four instantiate the same formal skeleton:

```text
Deviation requires a reference.
Operations closed inside the deviation class cannot produce the reference class.
```

## T1 Instantiation Table

| Domain | Deviation class | Reference class | Self-generated operations | Why closure matters |
| --- | --- | --- | --- | --- |
| Technical | error | specification | debugging from corrupted code/state only | cannot reconstruct the original specification without a clean reference/backup |
| Propositional | lie/false premise | truth/reality | rationalization from false premises | cannot derive truth merely by internally elaborating falsehood |
| Moral | sin/misalignment | righteousness | self-improvement from corrupted orientation | preserves or refines orientation unless an external reference-bearing operator enters |
| Ontological | corruption/decoherence | created/coherent order | closed entropy-driven processes | disorder is not self-restoring in a closed system |

One-sentence lock:

> The isomorphism is the structure, not the substance.

## Fix 2 - Openness Must Be Target-Indexed

The prior equation distinguished:

```text
O > 0
G > 0
O*G*(1-C)
```

But it did not yet ask:

> What is `O` open to?

That creates the "Lord Lord" failure mode.

A person may have high subjective openness, religious language, visible works, and sincere devotion while the target of openness is a counterfeit reference rather than the true reference.

## Formal Refinement

```text
ReferenceTarget := true_reference | false_reference

O_R(state) := openness directed toward the actual reference
O_F(state) := openness directed toward a counterfeit reference

RestorationTerm := O_R * G * (1-C)
O_F * G * (1-C) = 0
```

Meaning:

> Grace couples to openness toward the actual reference, not merely to religious intensity, moral performance, or sincere openness toward a false reference.

## False Vacuum Bridge

In phase-transition language:

> `O_F` is a false vacuum. It is locally stable, behaviorally convincing, and subjectively sincere, but it is not the true restored phase.

This explains why behavior alone cannot classify the system.

Same visible behavior may belong to:

1. `O_R` restored-but-incomplete trajectory.
2. Locally ordered but uncoupled trajectory.
3. `O_F` counterfeit/anti-coherent trajectory.

## Theological Boundary

This does not authorize humans to declare final state from behavior.

It does the opposite:

> Humans can observe behavior and partial fruit; only God can measure final orientation basis.

The death/judgment boundary resolves what behavior-basis observation cannot.

## Lean Implication

Do not formalize `O` as a simple scalar only.

Use either:

```text
Openness : State -> ReferenceTarget -> Prop
```

or:

```text
O : State -> ReferenceTarget -> Scalar
```

Then the restoration theorem must require the true-reference target:

```text
Restores(G, state) requires O state true_reference > 0
```

This keeps T9 from accidentally validating counterfeit religious coupling.

