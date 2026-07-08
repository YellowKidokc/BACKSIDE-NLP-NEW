# COWORK: Verification Registry v2
## Build the definitive inventory of every verified claim in Theophysics

---

## CONTEXT

David has 445 claims published on faiththruphysics.com and ~5,200 claim-level blocks extracted from canonical documents. The verification work is scattered across:

1. **Lean 4 proofs** — 18 source files, ~106 theorems, 3 sorry (Float limitations). Strongest type of verification but narrowest coverage (~30 claims). Located at `C:\Users\lowes\Desktop\Theophysics_Lean`

2. **Python/SymPy/JAX tests** — `T:\MASTER_EQUATION_TEST` folder with 8 math modules, 7 computational tests, 10 law notebooks, 16-consistency test audit, evolution inverse solver, biblical data tests. This covers far more territory (~150+ claims) but hasn't been systematically mapped.

3. **The Master Claims List** — 445 claims compiled from the site. Available as an uploaded document in this project.

4. **The Lean Verification Registry v1** — First-pass mapping of Lean theorems to claims. Available in this project.

5. **The Canonical Axiom Registry** — Reclassification of the 188 "axioms" into their real types: 2 axioms, 1 presupposition, 54 definitions, 94 theorems, 18 predictions, 23 theological postulates, 3 drops. Done May 2, 2026. The `public.axioms` table in Postgres (192.168.1.97:5432, database `theophysics`) has the canonical `euclid_label` column.

6. **Claim extraction pipeline** — `D:\brain\08_CLAIMS\` with `extract.py` and `export_excel.py`. Run via `EXTRACT.bat`. Reads from `targets.txt`, produces JSON then Excel.

---

## YOUR JOB

### Phase 1: Inventory all verification artifacts

Read every file in `T:\MASTER_EQUATION_TEST`:
- `theophysics-math/` — 8 sub-modules, each with README.md
- `theophysics-verification/` — 7 tests + 10 law notebooks + WHAT_THESE_TESTS_PROVE.md
- `_CANONICAL_BUILD/` — 9 sub-folders with formal statements
- `COLAB_MASTER_EQUATION/` — 14 notebooks
- `COLAB_BIBLICAL/` — biblical tests
- `test03` through `test09` — individual tests with `_results.json`
- `Evolution/` — evolution data
- `COMPLETE_VERIFICATION.py` and `FRESH_VERIFICATION_2026_03_26.py`

For each verified result, record:
- Source file
- Method (Lean proof / SymPy derivation / JAX simulation / consistency test / structural encoding)
- What was proved/computed/tested — stated precisely
- Strength: UNIVERSAL_PROOF / FORMAL_DERIVATION / COMPUTATIONAL_VERIFICATION / CONSISTENCY_TEST / STRUCTURAL_ENCODING

### Phase 2: Map to the 445 Master Claims

For each verified result, identify which claims from the Master Claims List it supports. Rate each:
- **DIRECT** — the verification IS this claim stated formally
- **STRUCTURAL** — proves a structural property the claim depends on
- **PARTIAL** — proves part of what the claim asserts
- **ENCODED** — claim is represented but not proved

### Phase 3: Produce the Registry

Output a single document (markdown + Excel) that answers:
- How many of 445 claims have formal backing? (breakdown by strength)
- What's the strongest result?
- What's NOT verified?
- Where does math end and interpretation begin?

### Phase 4: Update the claim extraction pipeline

Add the verification status to the `08_CLAIMS` pipeline so future extraction runs tag each claim with its verification status from the registry.

---

## KEY FILES (Priority Order)

### Must read first
- `T:\MASTER_EQUATION_TEST\theophysics-math\README.md`
- `T:\MASTER_EQUATION_TEST\theophysics-math\01_lagrangian\README.md`
- `T:\MASTER_EQUATION_TEST\theophysics-math\08_consistency_tests\README.md`
- `T:\MASTER_EQUATION_TEST\theophysics-verification\WHAT_THESE_TESTS_PROVE.md`
- `K:\Folders\LEAN4\canonical\AXIOM_DERIVATION_CHAIN_CANONICAL.md`

### Then process systematically
- All other `theophysics-math/*/README.md` files
- All `test0X_results.json` files
- `_CANONICAL_BUILD/INDEX.md` and sub-folders
- `COLAB_MASTER_EQUATION/*.ipynb` notebook results

---

## RULES

1. **Honesty over count.** Lower number + genuine = better than inflated count.
2. **Method matters.** Lean proof ≠ Python computation. Label accurately.
3. **The interpretation boundary.** Verification confirms structure, not interpretation. Always separate.
4. **Self-audit items are gold.** Where the framework identifies its own weaknesses, catalogue those too.
5. **The Master Equation was updated.** The canonical 10-law table was locked April 17, 2026 (v2.0). Some older tests may have run against a previous version. Flag version mismatches.

---

## POSTGRES ACCESS

- Host: 192.168.1.97
- Port: 5432
- Database: theophysics
- User: postgres
- Password: Moss9pep28$
- Key tables: `public.axioms` (197 rows, `euclid_label` = canonical type), `public.canonical_nodes` (189 rows)

---

## TOOLS ALREADY BUILT

- `D:\brain\08_CLAIMS\extract.py` — extracts claims from MD/HTML folders
- `D:\brain\08_CLAIMS\export_excel.py` — produces review Excel from claims JSON
- `D:\brain\08_CLAIMS\EXTRACT.bat` — menu-driven batch script
- `D:\brain\08_CLAIMS\targets.txt` — folder list for batch processing
- `D:\brain\08_CLAIMS\config.json` — classification config

---

*POF 2828 | May 2, 2026*
