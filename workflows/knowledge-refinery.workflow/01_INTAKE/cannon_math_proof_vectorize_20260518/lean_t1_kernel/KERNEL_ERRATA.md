# T1Kernel Errata and Build Log

## Current Status — 2026-05-18 Final Lean Pass

Active root module: `T1Kernel.lean`

Clean verification:

```powershell
lake clean
lake build T1Kernel
```

Result: build completed successfully with 19 jobs.

Active imported modules:

- `ReferenceState.lean`
- `Closure.lean`
- `TraceCoupling.lean`
- `OpennessGrace.lean`
- `TargetedOpenness.lean`
- `ExternalOperator.lean`
- `StepExternality.lean`
- `StepReception.lean`
- `NecessaryConditions.lean`
- `VariableNecessity.lean`
- `RestorationProfile.lean`
- `ContinuityIdentity.lean`
- `RivalModels.lean`
- `RivalModelInstances.lean`
- `SignInvariance.lean`
- `JusticeMercyTransform.lean`

Current active-code inventory:

- Lean `sorry`: 0
- Lean `admit`: 0
- Lean `axiom`: 0

Latest addition: `VariableNecessity.lean` blocks product-form candidate
smuggling by requiring every variable entering the product gate to be either
theorem-level proven necessary or explicitly assumed necessary by a supplied
domain model premise.

Latest addition: `RivalModelInstances.lean` lets named rival labels inherit
formal failure gates only after their exact premise pattern is supplied. A
label alone has no theorem power.

Important: older notes below preserve the historical failure log. They mention
past `sorry`/axiom placeholders that have since been removed or replaced with
weaker provable statements.

---

## Intellectual Honesty Protocol

**Rule:** Every `sorry`, every axiom, every unstated assumption, and every
fix must be explicitly logged with:
1. What was attempted
2. What failed
3. Why it is marked as `sorry`/axiom
4. What would be required to remove the marker

**No silent fixes. No hidden assumptions. No "try until it passes."**

---

## Build History

### 2026-05-13 — Session: Structural Reset to Lean 4 Kernel

**Objective:** Establish kernel file sequence: ReferenceState → T1SpineClosure →
TraceCoupling → OpennessGrace → SignInvariance → JusticeMercyTransform.

**CRITICAL DISCOVERY:** The existing `Closure.lean` (the supposedly "proven"
T1 theorem) did NOT compile with Lean 4 v4.29.1. It was written for an earlier
version of Lean where `List.mem_cons_self` took explicit arguments. In v4.29.1,
all arguments are implicit. This means the prior claim that `lake build` was
verified was either using cached artifacts from an older toolchain or was not
actually building the file.

**What was done:**

1. **Created `T1SpineClosure.lean` from existing `Closure.lean` content.**
   - Copied the proven T1 closure theorem.
   - **ERROR ENCOUNTERED:** Build failed with:
     ```
     Function expected at List.mem_cons_self but this term has type ?m.47 ∈ ?m.47 :: ?m.48
     ```
   - **ROOT CAUSE:** Lean 4 API change. `List.mem_cons_self` previously took
     explicit arguments `(a : α) (l : List α)` but in v4.29.1 has signature
     `{α : Type u_1} {a : α} {l : List α} : a ∈ a :: l` (all implicit).
   - **FIX:** Changed `List.mem_cons_self op rest` → `List.mem_cons_self`.
     Similarly, `List.mem_cons_of_mem op nextOpInRest` →
     `List.mem_cons_of_mem op nextOpInRest` was already correct (only `y` is
     explicit in v4.29.1).
   - **VERIFICATION:** `lake build T1Kernel.T1SpineClosure` now passes.
   - **Status:** ✅ PROVEN — compiles without `sorry`.

2. **Created `ReferenceState.lean` as foundational vocabulary module.**
   - **ERROR ENCOUNTERED:** Initially attempted to define `Error` and `Reference`
     as concrete predicates with `sorry`. This was WRONG — they must remain
     abstract parameters to each theorem, not fixed definitions.
   - **FIX:** Rewrote to use documentation-only abbreviations; actual predicates
     remain parameters. The `reference_not_error` lemma restates disjointness.
   - **Status:** ✅ PROVEN — compiles without `sorry`.

3. **Created `TraceCoupling.lean` as dependency/coupling module.**
   - **ERROR ENCOUNTERED:** `invalid 'import' command, it must be used in the
     beginning of the file` — module docstring `/-! ... -/` was placed BEFORE
     the `import` statement.
   - **FIX:** Moved all `import` statements to the absolute beginning of each
     file, before the module docstring. Applied to ALL stub files.
   - **Status:** ✅ PROVEN — compiles without `sorry`.

4. **Created `OpennessGrace.lean` as posture vs. operation module.**
   - `reception_implies_openness` uses `sorry`.
     **Blocker:** Need formal definition of "reception" — what does it mean
     for an external operation to be "received" by a state? Requires richer
     state structure (possibly a coupling relation or accessibility predicate).
   - `grace_external` is an AXIOM, not a `sorry`.
     **Rationale:** This is a definitional commitment. In this framework,
     "Grace" is DEFINED as external to the error class. It is not something
     to be proven from more basic axioms at this level.
   - **Warnings:** 2 unused variables in `openness_compatible_with_error`.
     **Fix needed:** Remove unused hypotheses or use them in the proof body.
   - **Status:** PARTIAL — 1 `sorry`, 1 axiom, 2 linter warnings.

5. **Created `SignInvariance.lean` as orientation preservation module.**
   - **ERROR ENCOUNTERED:** Build failed with:
     ```
     Unknown identifier `ℤ`
     stuck at solving universe constraint imax (u+1) ?u.14 =?= u+1
     Function expected at Sign but this term has type SignFunction State
     ```
   - **ROOT CAUSE:** Two issues:
     1. `ℤ` is not a built-in identifier in Lean 4 core — must use `Int`.
     2. `def SignFunction (State : Type u) : Type u := State → ℤ` creates an
        opaque type definition that Lean does not automatically unfold when
        checking function application.
   - **FIX:**
     1. Changed `ℤ` → `Int`.
     2. Changed `def SignFunction` → `abbrev SignFunction` so it unfolds
        transparently during type checking.
   - `self_generated_preserves_sign` uses `sorry`.
     **Blocker:** The proof requires showing that `PreservesError` implies
     `PreservesSign`. This needs a bridge axiom connecting `Error` to negative
     sign. Currently `hSignCompat` provides the local premise but the global
     implication is not yet formalized.
   - `no_self_generated_error_to_reference` uses `sorry`.
     **Blocker:** Depends on `self_generated_preserves_sign`. Once that is
     proven, this follows by combining with sign-to-predicate mapping.
   - **Status:** STUB — 2 `sorry`.

6. **Created `JusticeMercyTransform.lean` as constraint incompatibility module.**
   - All constraint definitions compile.
   - `self_generated_cannot_satisfy_all_three` uses `sorry`.
     **Blocker:** This is the core T5 claim. The proof requires combining
     T1 (self-generated ops preserve Error) with the constraint definitions
     to show that MercyEnacting + Transforming contradicts PreservesError.
     The intuition is clear but the formal argument needs careful statement.
   - **Warnings:** 2 unused variables in constraint definitions.
     **Fix needed:** Either use the variables or remove them.
   - **Status:** STUB — 1 `sorry`, 2 linter warnings.

**Files deleted/modified:** None deleted. `Closure.lean` retained for reference
but superseded by `T1SpineClosure.lean`.

---

## `sorry` Inventory

| File | Line | Theorem | Blocker | Path to Resolution |
|------|------|---------|---------|-------------------|
| OpennessGrace.lean | 53 | `reception_implies_openness` | No formal "reception" relation | Add `Receives : State → (State→State) → Prop` |
| SignInvariance.lean | 56 | `self_generated_preserves_sign` | Bridge axiom Error↔Sign needed | Formalize `Sign` as derivable from `Error` |
| SignInvariance.lean | 68 | `no_self_generated_error_to_reference` | Depends on previous `sorry` | Prove previous, then this follows |
| JusticeMercyTransform.lean | 118 | `self_generated_cannot_satisfy_all_three` | T5 core claim | Formalize MercyEnacting ∧ Transforming as contradicting PreservesError |

**Total:** 4 `sorry` across 6 files.

---

## Axiom Inventory

| File | Line | Axiom | Rationale | Can it be derived? |
|------|------|-------|-----------|-------------------|
| OpennessGrace.lean | 64 | `grace_external` | Definitional: Grace is defined as external | No — this is a naming convention, not a theorem |

**Total:** 1 axiom.

---

## Linter Warnings Inventory

| File | Line | Warning | Severity | Fix |
|------|------|---------|----------|-----|
| OpennessGrace.lean | 78 | unused variable `hError` | minor | Remove or use in proof |
| OpennessGrace.lean | 79 | unused variable `hOpen` | minor | Remove or use in proof |
| JusticeMercyTransform.lean | 53 | unused variable `G` | minor | Remove or use in definition |
| JusticeMercyTransform.lean | 81 | unused variable `G` | minor | Remove or use in definition |

---

## Boundary Violations Log

**None.** No Christianity uniqueness, Trinity, incarnation, atonement,
resurrection, hiddenness, or soul speculation has been promoted to theorem
status.

---

## Verification Command

```bash
lake clean && lake build T1Kernel --verbose
```

Expected result: `Build completed successfully (9 jobs).`
Warnings about `sorry` and unused variables are expected and logged above.

---

## Lessons Learned

1. **Do not trust cached builds.** `lake build` with `0 jobs` can mean the
   build system is not actually compiling changed files. Always force a clean
   build when verifying.

2. **Lean 4 API changes between versions.** `List.mem_cons_self` changed from
   explicit to implicit arguments between versions. The original `Closure.lean`
   was NOT valid Lean 4 v4.29.1 code despite prior claims.

3. **Import ordering matters.** Module docstrings (`/-! ... -/`) must come
   AFTER `import` statements in Lean 4 v4.29.1.

4. **Type aliases need `abbrev`, not `def`.** When defining function-type
   aliases that need to participate in function application, use `abbrev`
   (transparent definition) rather than `def` (opaque definition).

5. **Unicode identifiers are version-dependent.** `ℤ` works in some contexts
   (e.g., with Mathlib) but not in Lean 4 core. Use `Int` for portability.
