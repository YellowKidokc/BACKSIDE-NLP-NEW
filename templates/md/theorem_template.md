---
# THEOREM TEMPLATE
# ================
# Derived from axioms. Requires proof chain. 
# Must show: what it derives from, the derivation, what it enables.

uuid: {{UUID}}
type: theorem
id: T{{NUMBER}}
status: draft | review | canonical

# What this theorem derives from (REQUIRED - no orphan theorems)
derives_from:
  axioms: []      # e.g., [A1.1, A2.3]
  theorems: []    # e.g., [T4, T7]

# What this enables downstream
enables:
  theorems: []
  claims: []
  predictions: []

# Lexical Load Rule: Theorems introduce AT MOST 1 new primitive
new_primitives_introduced:
  - 

# Paper linkage
papers: []
primary_role: mechanism | mapping | implication  # Pick ONE

created: {{DATE}}
last_reviewed: {{DATE}}
---

# T{{NUMBER}}: {{THEOREM_TITLE}}

## Statement

> **{{FORMAL_THEOREM_STATEMENT}}**

---

## Proof Chain

### Given (Premises)

From upstream axioms and theorems:

1. **A{{X}}.{{Y}}**: [statement]
2. **T{{Z}}**: [statement]

### Derivation

```
Step 1: [logical step]
Step 2: [logical step]
Step 3: [logical step]
∴ {{THEOREM_STATEMENT}}
```

### QED Marker

☐ Proof complete and verified

---

## What This Establishes

Once proven, this theorem guarantees:

1. 

---

## What Breaks Without This

If this theorem fails:

- Downstream claim [X] loses support
- Prediction [Y] becomes unjustified

---

## Mathematical Form

$$
{{EQUATION}}
$$

| Symbol | Meaning | Units/Type |
|--------|---------|------------|
| | | |

---

## Does NOT Claim

> ⚠️ **Explicit exclusions:**

- This does NOT prove...
- This does NOT extend to...
- This requires [X] which is established separately in...

---

## Falsification

This theorem would be falsified if:

1. Any premise (A{{X}}.{{Y}}, T{{Z}}) is falsified
2. A logical error is found in the derivation
3. A counterexample is demonstrated where premises hold but conclusion fails

---

## Connection to Physics

| Theorem Component | Physics Parallel |
|-------------------|------------------|
| | |

---

%%semantic
{
  "uuid": "{{UUID}}",
  "type": "theorem",
  "id": "T{{NUMBER}}",
  "derives_from": [],
  "classifications": [
    {"content": "{{THEOREM_TITLE}}", "type": "theorem"}
  ]
}
%%
