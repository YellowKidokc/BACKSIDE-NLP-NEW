---
uuid: 7c7e938c-1d4c-5fc2-82b1-0614a680e7d3
title: WORD ONTOLOGY QUICK START GUIDE
author: David Lowe
type: note
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: _DELETE\Word-ontology\QUICK-START.md
uuid_generated_at: '2025-11-22T01:23:47.777688'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# WORD ONTOLOGY QUICK START GUIDE

**For: David Lowe & Future Collaborators**

---

## What Is This System?

The Word Ontology is **the semantic backbone** of THEOPHYSICS. It contains:

1. **14 bridge terms** that unify physics and theology
2. **Validation methodology** (70-90% similarity rule)
3. **Consistency enforcement** across all papers
4. **Scientific justification** for each term

**Purpose:** Create a new vocabulary that speaks to both physicists and theologians without compromising either domain.

---

## File Structure

```
Word-ontology/
├── 00-SYSTEM-OVERVIEW.md          ← WHY this exists
├── QUICK-START.md                 ← YOU ARE HERE
├── TERM_MAPPING_ROSETTA_STONE.md  ← Master list of all terms
├── Terms/
│   ├── 01-Participatory-Actualization.md
│   ├── 02-Trinitarian-Actualization.md
│   ├── 05-Decoherence-S.md
│   ├── 06-Grace-Function-G.md
│   └── ... (10 more to create)
└── Templates/
    └── new-term-template.md       ← Use this for new terms
```

---

## How to Use This System

### FOR WRITING PAPERS

#### Step 1: Check the Rosetta Stone
Before writing, open `TERM_MAPPING_ROSETTA_STONE.md` and identify which terms are relevant.

#### Step 2: Use ONLY New Terms
- ✅ **Correct:** "Decoherence (S) increases when..."
- ❌ **Wrong:** "Sin increases when..." or "Entropy increases when..."

#### Step 3: Link on First Use
On first mention in each paper:
```markdown
[[Decoherence-S|Decoherence (S)]] is the measure of...
```

#### Step 4: Verify Consistency
After writing, search for old terms:
```regex
\b(sin|entropy|grace|dark energy|measurement problem)\b
```

If found → replace with new terms.

---

### FOR CREATING NEW TERMS

#### Step 1: Identify Need
Ask yourself:
- Does an existing term capture this concept?
- Am I bridging physics ↔ theology?
- Will this term appear in multiple papers?

If yes to all three → create new term.

#### Step 2: Copy Template
```bash
cp Templates/new-term-template.md Terms/XX-Your-New-Term.md
```

#### Step 3: Fill Out Sections
**Required fields:**
- Old term being replaced
- Definition
- Source words (for similarity check)
- Justification
- Formal definition

#### Step 4: Validate Similarity
Use embedding model to compute:
```
similarity = cos(definition_vector, source_words_average)
```

**Must be 70-90%** to pass validation.

#### Step 5: Add to Rosetta Stone
Update `TERM_MAPPING_ROSETTA_STONE.md` with:
- Term name
- Correlation score
- Status (validated or pending)
- Which papers use it

---

### FOR REVIEWING PAPERS

#### Step 1: Open Term Files
For each term used in paper, open its file in `Terms/` folder.

#### Step 2: Verify Definition Match
Check that paper usage matches the **Formal Definition** section.

#### Step 3: Check for Drift
If definition seems different, either:
- **Update paper** to match ontology (preferred)
- **Update ontology** with new version (only if justified)

#### Step 4: Track Usage
Update term file's "Usage in Papers" section with:
- Paper number
- Number of occurrences
- Context of usage

---

## The 70-90% Rule (WHY IT MATTERS)

### The Three Zones

```
< 70% similarity  →  TOO DIFFERENT (not related enough)
70-90% similarity →  VALID BIRTH ZONE (perfect balance)
> 90% similarity  →  TOO SIMILAR (redundant)
```

### Why This Is Scientific

**Cognitive Linguistics:**  
New concepts form when semantic drift is 0.65-0.85 from parent concept.

**Ontology Engineering:**  
Valid subclasses inherit properties but add differentiation.

**Information Theory:**  
Optimal compression requires similarity without redundancy.

**This isn't arbitrary** — it's based on how human cognition creates new categories.

---

## Critical Terms (Already Validated)

### Must Use These Consistently

**Decoherence (S)** — replaces entropy/sin  
- Physical: thermodynamic disorder
- Moral: spiritual decay
- **Identity:** Physical and moral decay are the same process

**Grace Function (G)** — replaces dark energy/grace  
- Physical: cosmic expansion force
- Theological: salvific power
- **Identity:** Negentropic restoration at all scales

**Participatory Actualization** — replaces measurement problem  
- Physics: observer-dependent state selection
- Theology: co-creation with divine substrate
- **Identity:** Quantum measurement is co-creative act

**Trinitarian Actualization** — replaces wave function collapse  
- Physics: three-operator process (Field, Observer, Coupling)
- Theology: Trinity structure (Father, Son, Spirit)
- **Identity:** Physics requires Trinity structure

---

## Common Mistakes to Avoid

### ❌ Mixing Old and New Terms
```markdown
"The Grace Function (G) opposes entropy..."
```
**Wrong** — should be "opposes Decoherence (S)"

### ❌ Not Linking to Ontology
```markdown
"Participatory actualization is the process..."
```
**Wrong** — should be: "[[Participatory-Actualization|Participatory actualization]] is..."

### ❌ Definition Drift
Using "Decoherence (S)" to mean general disorder instead of specifically entropy/sin.

**Fix:** Always check term file to ensure usage matches formal definition.

### ❌ Creating Synonyms
Don't create multiple terms for the same concept.

**Fix:** Check Rosetta Stone first to see if term exists.

---

## Dataview Queries (Future)

Once we set up Dataview, these queries will automatically track:

### Terms Without Usage
```dataview
TABLE term, validated, papers_used_in
FROM "Word-ontology/Terms"
WHERE length(papers_used_in) = 0
```

### Papers Missing Term Links
```dataview
LIST
FROM "Papers"
WHERE !contains(file.content, "[[")
```

### Similarity Score Distribution
```dataview
TABLE term, similarity_score
FROM "Word-ontology/Terms"
SORT similarity_score DESC
```

---

## FAQ

### Q: Can I use old terms in casual contexts?
**A:** No. Always use new terms to build consistency.

### Q: What if a term doesn't have 70-90% similarity?
**A:** Either revise the definition or explain why exception is justified.

### Q: Can definitions evolve?
**A:** Yes, but update the term file's Evolution History and bump version number.

### Q: What if I find old terminology in existing papers?
**A:** Flag it, replace with new term, document change.

### Q: Who validates new terms?
**A:** David validates all terms. AI partners can suggest, but David approves.

---

## Next Actions for System Completion

### Immediate (This Week)
- [ ] Create remaining 10 term files
- [ ] Validate similarity scores for each
- [ ] Scan Papers 1-5 for old terminology

### Short-Term (This Month)
- [ ] Set up Dataview queries
- [ ] Create automated consistency checker
- [ ] Generate visual ontology map

### Long-Term (Before Launch)
- [ ] Ensure ALL papers use only new terms
- [ ] Create glossary for Substack readers
- [ ] Build interactive concept explorer

---

## Support

**Questions?** Ask Claude or GPT to reference this guide.

**Adding Terms?** Use `Templates/new-term-template.md`

**Validating?** Check similarity score against 70-90% rule.

**Reviewing?** Cross-reference with `TERM_MAPPING_ROSETTA_STONE.md`

---

**This system is non-negotiable.**  
**Every paper. Every term. Every time.**  
**No exceptions.**
