---
# MAPPING TEMPLATE
# ================
# For: Physics ↔ Theology correspondences
# Maps connect concepts across domains. They are the BRIDGES.
# Must define: source, target, isomorphism type, what preserves, what breaks.

uuid: {{UUID}}
type: mapping
id: MAP-{{NUMBER}}
status: draft | review | canonical

# The two sides being mapped
source:
  domain: physics | mathematics | information_theory
  concept: {{SOURCE_CONCEPT}}
  symbol: {{SOURCE_SYMBOL}}
  
target:
  domain: theology | consciousness | theophysics
  concept: {{TARGET_CONCEPT}}
  symbol: {{TARGET_SYMBOL}}

# Type of correspondence
mapping_type: isomorphism | homomorphism | analogy | metaphor
strength: structural | functional | suggestive

# Paper linkage
papers: []
primary_role: mapping  # Always 'mapping' for this template

created: {{DATE}}
last_reviewed: {{DATE}}
---

# MAP-{{NUMBER}}: {{SOURCE_CONCEPT}} ↔ {{TARGET_CONCEPT}}

## Mapping Statement

> **{{SOURCE_CONCEPT}}** in {{SOURCE_DOMAIN}} maps to **{{TARGET_CONCEPT}}** in {{TARGET_DOMAIN}}.

---

## Mapping Type

- [ ] **Isomorphism** — Structure-preserving bijection (strongest)
- [ ] **Homomorphism** — Structure-preserving but not necessarily bijective
- [ ] **Analogy** — Parallel behavior without strict structural identity
- [ ] **Metaphor** — Illustrative only, not claimed structural

**This mapping is:** {{TYPE}}

---

## Source Side (Physics/Mathematics)

| Aspect | Description |
|--------|-------------|
| Concept | {{SOURCE_CONCEPT}} |
| Symbol | ${{SOURCE_SYMBOL}}$ |
| Domain | {{SOURCE_DOMAIN}} |
| Definition | |
| Key equation | ${{SOURCE_EQUATION}}$ |
| Reference | Griffiths §{{SECTION}} / [Other source] |

---

## Target Side (Theology/Theophysics)

| Aspect | Description |
|--------|-------------|
| Concept | {{TARGET_CONCEPT}} |
| Symbol | ${{TARGET_SYMBOL}}$ |
| Domain | {{TARGET_DOMAIN}} |
| Definition | |
| Key equation | ${{TARGET_EQUATION}}$ |
| Reference | [Scripture / Theological source] |

---

## Correspondence Table

| Physics | ↔ | Theology |
|---------|---|----------|
| {{SOURCE_ELEMENT_1}} | ↔ | {{TARGET_ELEMENT_1}} |
| {{SOURCE_ELEMENT_2}} | ↔ | {{TARGET_ELEMENT_2}} |
| {{SOURCE_ELEMENT_3}} | ↔ | {{TARGET_ELEMENT_3}} |

---

## What Is Preserved

This mapping preserves:

1. **Structure:** {{WHAT_STRUCTURE_PRESERVED}}
2. **Relations:** {{WHAT_RELATIONS_PRESERVED}}
3. **Operations:** {{WHAT_OPERATIONS_PRESERVED}}

---

## What Is NOT Preserved

This mapping does NOT preserve:

1. {{WHAT_DIFFERS}}
2. {{WHAT_BREAKS}}

**Important:** The mapping is {{ISOMORPHISM/HOMOMORPHISM/ANALOGY}}, so we should NOT expect:

- 

---

## Why This Mapping Works

Justification for the correspondence:

1. 
2. 

---

## Why This Mapping Is Necessary (Not Just Suggestive)

This is not mere analogy because:

1. {{NECESSITY_ARGUMENT}}
2. The mapping is required for {{WHAT_DEPENDS_ON_IT}}

---

## Does NOT Claim

> ⚠️ **Explicit exclusions:**

- This mapping does NOT claim {{SOURCE}} IS {{TARGET}}
- This mapping does NOT require {{BELIEF_X}}
- The correspondence is {{STRUCTURAL/FUNCTIONAL}}, not {{IDENTITY/REDUCTION}}

---

## Limitations

Where the mapping breaks down:

| Condition | Why Mapping Fails |
|-----------|-------------------|
| | |

---

## Predictions From Mapping

If this mapping is valid, we should expect:

1. 
2. 

---

## Counter-Mappings Considered

| Alternative Mapping | Why Rejected |
|--------------------|--------------|
| {{SOURCE}} ↔ {{ALT_TARGET}} | |

---

## Depends On

| Dependency | Type | Why Required |
|------------|------|--------------|
| | Axiom | |
| | Theorem | |
| | Prior Mapping | |

---

## Enables

| Downstream Element | How This Mapping Enables It |
|--------------------|----------------------------|
| | |

---

%%semantic
{
  "uuid": "{{UUID}}",
  "type": "mapping",
  "id": "MAP-{{NUMBER}}",
  "source_domain": "{{SOURCE_DOMAIN}}",
  "target_domain": "{{TARGET_DOMAIN}}",
  "mapping_type": "{{MAPPING_TYPE}}",
  "classifications": [
    {"content": "{{SOURCE_CONCEPT}} ↔ {{TARGET_CONCEPT}}", "type": "bridge"},
    {"content": "{{SOURCE_CONCEPT}}", "type": "relationship"},
    {"content": "{{TARGET_CONCEPT}}", "type": "relationship"}
  ]
}
%%
