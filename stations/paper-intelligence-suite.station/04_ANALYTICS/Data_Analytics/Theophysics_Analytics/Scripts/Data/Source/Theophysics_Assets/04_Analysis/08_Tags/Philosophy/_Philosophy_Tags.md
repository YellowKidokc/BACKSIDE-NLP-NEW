---
uid: TAG-philosophy-index
type: tag-category
category: philosophy
created: 2025-11-29
---

# Philosophy Tags

> Tags for consciousness, ontology, and epistemology concepts.

---

## Consciousness & Mind

- `consciousness` - Subjective experience
- `observer` - Conscious agent
- `qualia` - Subjective qualities
- `hard-problem` - Chalmers' hard problem
- `free-will` - Volitional agency
- `agency` - Causal power
- `intentionality` - Aboutness

---

## Ontology (What Exists)

- `ontology` - Study of being
- `metaphysics` - Beyond physics
- `dualism` - Mind-matter separation
- `idealism` - Mind-primary
- `materialism` - Matter-primary
- `panpsychism` - Universal consciousness
- `emergence` - Novel properties arising

---

## Epistemology (How We Know)

- `epistemology` - Study of knowledge
- `phenomenology` - First-person experience
- `measurement` - Knowledge acquisition
- `observation` - Conscious perception

---

## Mind-Body Problem

The relationship between consciousness and physical reality:

| Position | View | Theophysics Analog |
|----------|------|-------------------|
| Dualism | Separate substances | Trinity distinction |
| Idealism | Mind is fundamental | Information substrate |
| Materialism | Matter is fundamental | (Rejected) |
| Panpsychism | Mind is universal | Logos field |

---

## Notes Using Philosophy Tags

```dataview
TABLE file.tags AS Tags, coherence_score AS Coherence
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine"
WHERE any(file.tags, (t) => contains(t, "consciousness") OR contains(t, "ontology") OR contains(t, "epistemology"))
SORT coherence_score DESC
```
