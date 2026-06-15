---
title: "Curry-Howard Correspondence"
author: "Unknown Author"
date: 2026-03-01
category: theory
tags:
  - theory
  - theory
  - canonical
source_file: Curry-Howard_Correspondence.md
restructured: 2026-03-01 15:52:18
---

# Curry-Howard Correspondence

**Author:** Unknown Author

**Date:** 2026-03-01

---

## Table of Contents

- [# Curry-Howard Correspondence](#-curry-howard-correspondence)
- [## Overview](#-overview)
- [## Historical Development](#-historical-development)
- [## Basic Correspondence](#-basic-correspondence)
- [### The Isomorphism](#-the-isomorphism)
- [## Core Principles](#-core-principles)
- [### 1. Propositions as Types](#-1-propositions-as-types)
- [### 2. Proofs as Programs](#-2-proofs-as-programs)
- [### 3. Normalization](#-3-normalization)
- [## Detailed Correspondence](#-detailed-correspondence)
- [### Implication (→)](#-implication-)
- [### Conjunction (∧)](#-conjunction-)
- [### Disjunction (∨)](#-disjunction-)
- [### Universal Quantification (∀)](#-universal-quantification-)
- [### Existential Quantification (∃)](#-existential-quantification-)

---

---
title: "Curry-Howard Correspondence"
domain: Logic & Type Theory
source: Web (Wikipedia)
url: https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence
downloaded: 2025-12-14
tags:
  - type-theory
  - proof-theory
  - logic
  - programming-languages
  - lambda-calculus
  - theophysics
---

# Curry-Howard Correspondence {#-curry-howard-correspondence}

## Overview {#-overview}

The **Curry-Howard correspondence** (also called Curry-Howard isomorphism) is a fundamental result showing that mathematical logic and type systems in programming languages are structurally identical. It establishes a deep connection between:
- **Propositions** in logic and **types** in programming
- **Proofs** in logic and **programs** (terms) in typed languages
- **Proof normalization** and **program execution**

## Historical Development {#-historical-development}

- **Haskell Curry** (1934): Noted connection between combinatory logic and implicational logic
- **William Howard** (1958, published 1980): Extended to full first-order logic and dependent types
- **Modern development**: Central to type theory, programming language design, and proof assistants

## Basic Correspondence {#-basic-correspondence}

### The Isomorphism {#-the-isomorphism}

| Logic | Programming |
|-------|-------------|
| Proposition | Type |
| Proof | Term/Program |
| Implication (P → Q) | Function type (A → B) |
| Conjunction (P ∧ Q) | Product type (A, B) |
| Disjunction (P ∨ Q) | Sum type (A ∣ B) |
| True | Unit type (()) |
| False | Empty type (∅) |
| Universal quantifier (∀) | Dependent function type |
| Existential quantifier (∃) | Dependent pair type |

## Core Principles {#-core-principles}

### 1. Propositions as Types {#-1-propositions-as-types}

A proposition is interpreted as a type. Asserting a proposition means the corresponding type is inhabited (non-empty).

**Example**:
- Proposition: "If it rains, the ground is wet"
- Type: `rain → ground_wet`

### 2. Proofs as Programs {#-2-proofs-as-programs}

A proof of a proposition corresponds to a program/term of the corresponding type. Constructing a proof means writing a program.

**Example**:
```haskell
proof : rain → ground_wet
proof = λ r → get_wet r
```

### 3. Normalization {#-3-normalization}

- **Logic**: A proof can be simplified by removing redundant steps (proof normalization)
- **Programming**: A program can be simplified by removing redundant computations (program normalization/evaluation)
- **Correspondence**: These processes are the same mechanism viewed differently

## Detailed Correspondence {#-detailed-correspondence}

### Implication (→) {#-implication-}

**Logic**: "If P then Q" (P → Q)
**Programming**: Function from type P to type Q

```haskell
-- A proof of (P → Q) is a function that takes a proof of P and produces a proof of Q
proof_of_implication : P → Q = \p -> q_proof
```

### Conjunction (∧) {#-conjunction-}

**Logic**: "P and Q" (P ∧ Q)
**Programming**: Pair type (P, Q)

```haskell
-- A proof of (P ∧ Q) pairs a proof of P with a proof of Q
proof_of_and : (P, Q) = (proof_p, proof_q)
```

### Disjunction (∨) {#-disjunction-}

**Logic**: "P or Q" (P ∨ Q)
**Programming**: Sum type (Either P Q) or tagged union

```haskell
-- A proof of (P ∨ Q) is either a proof of P or a proof of Q
proof_of_or : Either P Q = Left proof_p  -- or Right proof_q
```

### Universal Quantification (∀) {#-universal-quantification-}

**Logic**: "For all x, P(x)" (∀x. P(x))
**Programming**: Dependent function type (Π-type)

```haskell
-- A proof of ∀x. P(x) is a function from any x to a proof of P(x)
proof : ∀ (x : A) → P x = \x -> proof_of_p_x
```

### Existential Quantification (∃) {#-existential-quantification-}

**Logic**: "There exists x such that P(x)" (∃x. P(x))
**Programming**: Dependent pair type (Σ-type)

```haskell
-- A proof of ∃x. P(x) is a witness x together with a proof of P(x)
proof : Σ (x : A). P x = (witness, proof_of_p_witness)
```

## Examples {#-examples}

### Example 1: Simple Tautology {#-example-1-simple-tautology}

**Proposition**: P → P (identity)

**Proof**:
- Assume P
- Therefore P follows immediately

**Programming equivalent**:
```haskell
identity : P → P
identity = \p -> p  -- the identity function
```

### Example 2: De Morgan's Law {#-example-2-de-morgans-law}

**Proposition**: ¬(P ∨ Q) → (¬P ∧ ¬Q)

**Proof**:
1. Assume ¬(P ∨ Q)
2. Assume P to derive ¬P: would make P ∨ Q true, contradiction
3. So ¬P. Similarly derive ¬Q.
4. Therefore ¬P ∧ ¬Q

**Programming equivalent**:
```haskell
demorgan : ((P | Q) -> Void) -> (P -> Void, Q -> Void)
demorgan f = (\p -> f (inl p), \q -> f (inr q))
```

### Example 3: Composition {#-example-3-composition}

**Proposition**: (Q → R) → (P → Q) → (P → R)

**Proof/Program**: Function composition
```haskell
compose : (Q -> R) -> (P -> Q) -> (P -> R)
compose f g = \p -> f (g p)
```

## Applications {#-applications}

### 1. Proof Assistants and Automated Reasoning {#-1-proof-assistants-and-automated-reasoning}

- **Coq**: Based on Curry-Howard for constructive proofs
- **Agda**: Dependent type language using Curry-Howard
- **Lean**: Modern proof assistant using type theory
- **Isabelle/HOL**: Uses correspondence for formal verification

### 2. Programming Language Design {#-2-programming-language-design}

- **Dependent type languages**: Scala, Idris, Epigram
- **Type systems**: More expressive types enable stronger program correctness guarantees
- **Refinement types**: Encode domain-specific properties in types

### 3. Formal Verification {#-3-formal-verification}

- Proving program properties by writing proofs in corresponding logic
- Verified software: Coq-verified C compiler (CompCert)
- Security proofs: Cryptographic protocols verified as proofs

### 4. Program Synthesis {#-4-program-synthesis}

- Automatically generating programs from logical specifications
- The program is the proof; proof construction = synthesis

### 5. Theorem Proving {#-5-theorem-proving}

- Mechanized mathematics
- Formal verification of mathematics
- Proof checking and validation

## Constructive vs Classical Logic {#-constructive-vs-classical-logic}

### Constructive (Intuitionistic) Logic {#-constructive-intuitionistic-logic}

- Every proposition has a **computational interpretation**
- Holds strongly: Curry-Howard correspondence is direct
- Used in type theory and proof assistants

**Key difference**: No law of excluded middle (P ∨ ¬P)

### Classical Logic {#-classical-logic}

- Some theorems lack computational meaning
- Requires additional structure (continuations, classical logic in computational form)
- Weaker correspondence

## Advanced Topics {#-advanced-topics}

### Dependent Types {#-dependent-types}

The correspondence extends to dependent types where:
- Types can depend on values
- More expressive logical formulas
- Enables encoding mathematical theorems as types

### Linear Type Systems {#-linear-type-systems}

Corresponds to linear logic:
- Each assumption used exactly once
- Resource management
- Connection to quantum computing

### Homotopy Type Theory {#-homotopy-type-theory}

Recent development:
- Types have topological/homotopical structure
- Propositions as spaces, proofs as paths
- Connection between logic, topology, and computation

## Philosophical Implications {#-philosophical-implications}

### Programs as Proofs {#-programs-as-proofs}

- A program that typechecks is a constructive proof of a theorem
- Type correctness = logical consistency
- Termination = proof normalization

### Computational Content {#-computational-content}

- Every constructive proof contains computational meaning
- Not just existence proofs; actual algorithms
- Mathematics becomes computational

### Constructivism {#-constructivism}

- Validates constructivist philosophy in mathematics
- Meaningful alternative to classical mathematics
- Computational focus

## Limitations and Extensions {#-limitations-and-extensions}

### What the Correspondence Covers {#-what-the-correspondence-covers}

- Intuitionistic (constructive) logic
- Type systems in functional programming
- Formal semantics of proofs and programs

### What It Doesn't Cover {#-what-it-doesnt-cover}

- Classical logic (requires classical axioms beyond the correspondence)
- Non-terminating programs
- Effectful computation (I/O, side effects without extension)
- Full object-oriented programming (without type-theoretic extensions)

### Modern Extensions {#-modern-extensions}

- **Cubical type theory**: Even richer structure
- **Quantum type systems**: Connection to quantum computing
- **Differential type theory**: For calculus and analysis
- **Computational effects**: Monadic extensions

## Significance {#-significance}

The Curry-Howard correspondence reveals:
1. **Deep unity**: Logic and computation are two faces of the same phenomenon
2. **Constructivity**: Mathematical truth and computational implementation are intertwined
3. **Verification**: Can verify programs by proving logical theorems
4. **Synthesis**: Can generate programs by constructing proofs
5. **Foundations**: Provides new foundations for both mathematics and computer science

## Source {#-source}

[Full article at source](https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence)

---

Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]
## Related Theories {#-related-theories}

- [[00_Canonical/_QUARANTINE/_Documentation/LOGOS_V3_REV4_CANONICAL/LOGOS_V3_REV4_LONG_LOSSLESS_20260217_114247|LOGOS V3 Revision 4 Long Lossless Bundle]]
- [[00_Canonical/_QUARANTINE/_Documentation/LOGOS_V3_REV4_CANONICAL/LOGOS_V3_REV4_LONG_LOSSLESS_20260217_114353|LOGOS V3 Revision 4 Long Lossless Bundle]]
- [[00_Canonical/_QUARANTINE/_Documentation/LOGOS_V3_REV4_CANONICAL/LOGOS_V3_REV4_LONG_LOSSLESS_20260217_114658|LOGOS V3 Revision 4 Long Lossless Bundle]]
- [[00_Canonical/_QUARANTINE/_Documentation/LOGOS_V3_REV4_CANONICAL/LOGOS_V3_REV4_LONG_LOSSLESS_20260217_115124|LOGOS V3 Revision 4 Long Lossless Bundle]]


---

## Metadata

**Original File:** Curry-Howard_Correspondence.md

**Restructured:** 2026-03-01 15:52:18

**Format:** Canonical Theory Document (Lowe Standard v1.0)

**Status:** Cleaned and ready for evaluation

---

*This paper has been restructured for clarity and proper academic formatting. Original content preserved.*
