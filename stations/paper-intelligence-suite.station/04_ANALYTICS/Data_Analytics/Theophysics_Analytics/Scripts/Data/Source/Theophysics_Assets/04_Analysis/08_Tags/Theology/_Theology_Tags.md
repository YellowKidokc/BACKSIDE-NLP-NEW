---
uid: TAG-theology-index
type: tag-category
category: theology
created: 2025-11-29
---

# Theology Tags

> Tags for theological concepts in Theophysics research.

---

## Trinity Structure

| Tag | Related Atom | Trinity Aspect |
|-----|--------------|----------------|
| [[father]] | [[Information (I)]] | Source, Origin |
| [[son]] | [[Form (F)]], [[Logos (L)]] | Manifestation, Word |
| [[spirit]] | [[Dynamics (D)]] | Relationship, Process |
| [[Logos zright/Misc/trinity]] | - | Unified Godhead |

---

## Core Theological Concepts

### God & Trinity
- `god` - The divine being
- `trinity` - Three-in-one nature
- `father` - First person, Source
- `son` - Second person, Logos
- `spirit` - Third person, Breath
- `logos` - Divine Word/Reason

### Christ & Salvation
- `jesus` - Historical person
- `christ` - Messiah/Anointed
- `incarnation` - Word made flesh
- `redemption` - Buying back
- `atonement` - At-one-ment
- `resurrection` - Rising from death

### Grace & Sin
- `grace` - Unmerited favor
- `sin` - Missing the mark
- `fall` - Original corruption
- `salvation` - Deliverance

### Kingdom & Covenant
- `kingdom` - God's reign
- `covenant` - Binding agreement
- `prophecy` - Divine revelation
- `eschatology` - End things
- `revelation` - Unveiling

---

## Notes Using Theology Tags

```dataview
TABLE file.tags AS Tags, trinity_aspect AS "Trinity Aspect", coherence_score AS Coherence
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"
WHERE any(file.tags, (t) => contains(t, "grace") OR contains(t, "trinity") OR contains(t, "logos") OR contains(t, "resurrection"))
SORT coherence_score DESC
```

---

## Scripture References

```dataview
TABLE scriptures AS Scriptures
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine"
WHERE scriptures
FLATTEN scriptures
LIMIT 20
```
