---
# BOUNDARY CONDITION TEMPLATE
# ===========================
# BCs constrain what is possible. They are the guardrails.
# Must define: what it constrains, what happens at violation, what depends on it.

uuid: {{UUID}}
type: boundary_condition
id: BC-{{NUMBER}}
status: draft | review | canonical

# What this BC constrains
constrains:
  fields: []      # e.g., [χ-field]
  operators: []   # e.g., [Judgment Operator]
  axioms: []      # Which axioms this BC enforces

# Where this BC applies
domain_of_application: {{WHERE_IT_APPLIES}}  # e.g., "at moral singularities"

# Dependencies
requires_axioms: []

# Paper linkage
papers: []

created: {{DATE}}
last_reviewed: {{DATE}}
---

# BC-{{NUMBER}}: {{BOUNDARY_CONDITION_TITLE}}

## Statement

> **At {{BOUNDARY_LOCATION}}, {{WHAT_IS_CONSTRAINED}} must satisfy {{CONSTRAINT}}.**

---

## Mathematical Form

$$
{{SYMBOL}} \big|_{ {{BOUNDARY}} } = {{VALUE_OR_CONDITION}}
$$

Or:

$$
\lim_{ {{VARIABLE}} \to {{LIMIT}} } {{EXPRESSION}} = {{VALUE}}
$$

---

## What This Constrains

| Constrained Element | How It Is Constrained |
|---------------------|----------------------|
| | |

---

## Why This BC Is Necessary

Without this boundary condition:

1. {{WHAT_GOES_WRONG_1}}
2. {{WHAT_GOES_WRONG_2}}
3. System becomes {{UNBOUNDED/UNDEFINED/INCONSISTENT}}

---

## Physical Parallel

| BC Aspect | Physics Analog | Example |
|-----------|----------------|---------|
| Boundary type | Dirichlet / Neumann / Mixed | |
| Location | | |
| Effect | | |

**Griffiths Reference:** §{{SECTION}}

---

## Violation Behavior

What happens if this BC is violated?

| Violation Type | Consequence |
|----------------|-------------|
| {{SYMBOL}} exceeds limit | |
| {{SYMBOL}} undefined at boundary | |
| Discontinuity at boundary | |

---

## Does NOT Claim

> ⚠️ **Explicit exclusions:**

- This BC does NOT prevent...
- This BC does NOT require...
- Satisfying this BC does NOT guarantee...

---

## Theological Interpretation

| Mathematical Constraint | Theological Meaning |
|------------------------|---------------------|
| {{CONSTRAINT}} | |

---

## Depends On

| Dependency | Type | Why Required |
|------------|------|--------------|
| | Axiom | |
| | Field | |

---

## What Depends On This

| Downstream Element | Why It Needs This BC |
|--------------------|---------------------|
| | |

---

## Verification

How can we check if this BC is satisfied?

1. 
2. 

---

%%semantic
{
  "uuid": "{{UUID}}",
  "type": "boundary_condition",
  "id": "BC-{{NUMBER}}",
  "classifications": [
    {"content": "{{BOUNDARY_CONDITION_TITLE}}", "type": "boundary_condition"}
  ]
}
%%
