---
# FIELD TEMPLATE
# ==============
# For: χ-field, Logos Field, Grace Field, etc.
# Fields PERMEATE space/reality. They have values at every point.
# Must define: symbol, what it represents, equations of motion, sources, boundary behavior.

uuid: {{UUID}}
type: field
id: FIELD-{{SHORT_NAME}}
symbol: {{SYMBOL}}  # e.g., χ, Φ, Ψ
status: draft | review | canonical

# Field classification
field_type: scalar | vector | tensor | spinor
real_or_complex: real | complex

# What generates/sources this field
sources: []  # e.g., ["divine intent", "consciousness"]

# Dependencies
requires_axioms: []
requires_fields: []  # Other fields this depends on

# Paper linkage
papers: []
primary_role: mechanism

created: {{DATE}}
last_reviewed: {{DATE}}
---

# {{SYMBOL}} — {{FIELD_NAME}}

## Definition

> **{{FIELD_NAME}}** is the {{FIELD_TYPE}} field that {{DESCRIPTION}}.

**Symbol:** ${{SYMBOL}}$ or ${{SYMBOL}}(\mathbf{x}, t)$

---

## Field Properties

| Property | Value | Significance |
|----------|-------|--------------|
| Type | scalar / vector / tensor | |
| Real/Complex | | |
| Dimensionality | | |
| Units | | |

---

## Source Equation

What generates this field:

$$
\nabla^2 {{SYMBOL}} = {{SOURCE_TERM}}
$$

| Source | Mathematical Form | Meaning |
|--------|-------------------|---------|
| | | |

---

## Equations of Motion

### Static Case

$$
{{STATIC_EQUATION}}
$$

### Dynamic Case

$$
\frac{\partial {{SYMBOL}}}{\partial t} = {{DYNAMIC_EQUATION}}
$$

### Wave Equation (if applicable)

$$
\nabla^2 {{SYMBOL}} - \frac{1}{c^2}\frac{\partial^2 {{SYMBOL}}}{\partial t^2} = {{SOURCE}}
$$

---

## Boundary Conditions

| Boundary | Condition | Physical/Theological Meaning |
|----------|-----------|------------------------------|
| At infinity | ${{SYMBOL}} \to $ | |
| At source | ${{SYMBOL}} = $ | |
| At interface | | |

---

## Field Strength and Gradient

### Magnitude

$$
|{{SYMBOL}}| = {{MAGNITUDE_EXPRESSION}}
$$

### Gradient (if scalar)

$$
\nabla {{SYMBOL}} = {{GRADIENT_MEANING}}
$$

### Divergence (if vector)

$$
\nabla \cdot \mathbf{ {{SYMBOL}} } = {{DIVERGENCE_MEANING}}
$$

### Curl (if vector)

$$
\nabla \times \mathbf{ {{SYMBOL}} } = {{CURL_MEANING}}
$$

---

## Conservation Laws

Is there a conserved quantity associated with this field?

$$
\frac{\partial \rho}{\partial t} + \nabla \cdot \mathbf{J} = 0
$$

Where:
- $\rho = $ {{DENSITY_MEANING}}
- $\mathbf{J} = $ {{CURRENT_MEANING}}

---

## Coupling to Other Fields

| Other Field | Coupling Type | Interaction Term |
|-------------|---------------|------------------|
| | | |

---

## Physics Parallel

| {{SYMBOL}} Aspect | Physics Analog | Griffiths Reference |
|-------------------|----------------|---------------------|
| Field itself | | § |
| Source equation | | § |
| Boundary behavior | | § |

---

## Observable Effects

How does this field manifest in measurable/experiential ways?

| Domain | Observable Effect |
|--------|-------------------|
| Physics | |
| Consciousness | |
| Behavior | |
| Society | |

---

## Does NOT Claim

> ⚠️ **Explicit exclusions:**

- This field is NOT the same as [common confusion]...
- The {{SYMBOL}} field does NOT imply...
- Measurability does NOT require...

---

## Depends On

| Dependency | Type | Why Required |
|------------|------|--------------|
| | Axiom | |
| | Field | |

---

## Enables

| Downstream Element | How This Field Enables It |
|--------------------|---------------------------|
| | |

---

%%semantic
{
  "uuid": "{{UUID}}",
  "type": "field",
  "id": "FIELD-{{SHORT_NAME}}",
  "symbol": "{{SYMBOL}}",
  "field_type": "{{FIELD_TYPE}}",
  "classifications": [
    {"content": "{{FIELD_NAME}}", "type": "field"},
    {"content": "{{SYMBOL}}", "type": "variable"}
  ]
}
%%
