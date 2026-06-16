---
# AXIOM TEMPLATE
# ==============
# The most fundamental unit. Cannot be derived. Must be assumed.
# Maximum discipline: One statement, clear tier, minimal metadata.

uuid: {{UUID}}
type: axiom
id: A{{TIER}}.{{NUMBER}}
tier: {{TIER}}  # 0=Primordial, 1=Ontological, 2=Informational, 3=Consciousness, 4=Moral, 5=Eschatological, 6=Relational
status: draft | review | canonical

# Lexical Load Rule: Axioms introduce AT MOST 1 new primitive
new_primitives_introduced:
  - 

# Dependencies (what must be true for this axiom to be meaningful)
upstream_axioms: []

# What this enables
downstream:
  theorems: []
  claims: []
  boundary_conditions: []

# Paper linkage
papers: []

created: {{DATE}}
last_reviewed: {{DATE}}
---

# A{{TIER}}.{{NUMBER}}: {{AXIOM_TITLE}}

## Statement

> **{{SINGLE_SENTENCE_AXIOM_STATEMENT}}**

---

## Necessity Argument

Why this cannot be otherwise:

1. 

---

## What Breaks Without This

If this axiom is false or removed:

- 

---

## Domain Expression

| Domain | How This Manifests |
|--------|-------------------|
| Physics | |
| Information | |
| Consciousness | |
| Theology | |

---

## Does NOT Claim

> ⚠️ **Explicit exclusions to prevent misreading:**

- This does NOT claim...
- This does NOT require belief in...
- This is NOT equivalent to...

---

## Falsification Criteria

This axiom would be falsified if:

1. 

---

## Notes

<!-- Working notes, historical development, open questions -->

---

%%semantic
{
  "uuid": "{{UUID}}",
  "type": "axiom",
  "id": "A{{TIER}}.{{NUMBER}}",
  "tier": {{TIER}},
  "classifications": [
    {"content": "{{AXIOM_TITLE}}", "type": "axiom"}
  ]
}
%%
