---
# OPERATOR TEMPLATE
# =================
# For: Grace Operator, Judgment Operator, Logos Gate, etc.
# Operators ACT on states/fields. They transform.
# Must define: symbol, action, domain, codomain, inverse (if exists).

uuid: {{UUID}}
type: operator
id: OP-{{SHORT_NAME}}
symbol: {{SYMBOL}}  # e.g., Ĵ, Ĝ, L̂
status: draft | review | canonical

# What this operator acts upon
domain: {{WHAT_IT_TAKES_AS_INPUT}}  # e.g., "moral superposition states"
codomain: {{WHAT_IT_PRODUCES}}      # e.g., "definite moral eigenstates"

# Operator properties
properties:
  linear: true | false
  hermitian: true | false
  unitary: true | false
  invertible: true | false
  idempotent: true | false  # Ô² = Ô ?

# Dependencies
requires_axioms: []
requires_fields: []  # e.g., [χ-field]

# Paper linkage
papers: []
primary_role: mechanism

created: {{DATE}}
last_reviewed: {{DATE}}
---

# {{SYMBOL}} — {{OPERATOR_NAME}}

## Definition

> **{{OPERATOR_NAME}}** is the operator that {{ACTION_DESCRIPTION}}.

**Symbol:** $\hat{ {{SYMBOL}} }$

---

## Mathematical Form

### Action on State

$$
\hat{ {{SYMBOL}} } | \psi \rangle = {{RESULT}}
$$

### Eigenvalue Equation

$$
\hat{ {{SYMBOL}} } | {{EIGENSTATE}} \rangle = {{EIGENVALUE}} | {{EIGENSTATE}} \rangle
$$

### Eigenstates

| Eigenstate | Eigenvalue | Physical/Theological Meaning |
|------------|------------|------------------------------|
| $|+\rangle$ | | |
| $|-\rangle$ | | |

---

## Domain and Codomain

| | Description |
|---|-------------|
| **Input (Domain)** | {{WHAT_IT_ACTS_ON}} |
| **Output (Codomain)** | {{WHAT_IT_PRODUCES}} |

---

## Operator Properties

| Property | Value | Implication |
|----------|-------|-------------|
| Linear | | |
| Hermitian | | Real eigenvalues = observable |
| Unitary | | Preserves probability |
| Invertible | | Can be undone? |
| Idempotent | | Applying twice = applying once |

---

## Inverse Operator

Does $\hat{ {{SYMBOL}} }^{-1}$ exist?

- [ ] Yes: $\hat{ {{SYMBOL}} }^{-1} = $ {{INVERSE}}
- [ ] No: Because {{REASON}}

**Theological significance of (non-)invertibility:**

> 

---

## Physics Parallel

| Operator Aspect | Physics Analog | Reference |
|-----------------|----------------|-----------|
| {{SYMBOL}} | | Griffiths § |
| Action | | |
| Eigenvalues | | |

---

## When This Operator Acts

**Trigger condition:**

> {{SYMBOL}} acts when {{CONDITION}}

**Examples:**

1. 
2. 

---

## Does NOT Claim

> ⚠️ **Explicit exclusions:**

- This operator does NOT represent...
- The eigenvalues do NOT imply...
- This is NOT equivalent to [common misconception]...

---

## Depends On

| Dependency | Type | Why Required |
|------------|------|--------------|
| | Axiom | |
| | Field | |
| | Operator | |

---

## Enables

| Downstream Element | How This Operator Enables It |
|--------------------|------------------------------|
| | |

---

%%semantic
{
  "uuid": "{{UUID}}",
  "type": "operator",
  "id": "OP-{{SHORT_NAME}}",
  "symbol": "{{SYMBOL}}",
  "classifications": [
    {"content": "{{OPERATOR_NAME}}", "type": "operator"},
    {"content": "{{SYMBOL}}", "type": "variable"}
  ]
}
%%
