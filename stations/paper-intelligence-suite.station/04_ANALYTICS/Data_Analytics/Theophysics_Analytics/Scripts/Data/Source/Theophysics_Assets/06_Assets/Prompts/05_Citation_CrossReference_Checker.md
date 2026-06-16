---
uuid: d47d30b7-7b96-5cb9-b749-ded80563d8bf
title: Citation & Cross-Reference Checker for Logos Papers
author: David Lowe
type: note
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\Assets\Prompts\05_Citation_CrossReference_Checker.md
uuid_generated_at: '2025-11-22T01:23:03.449375'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# Citation & Cross-Reference Checker for Logos Papers

## Purpose
Ensure all citations, cross-references, and inter-paper links in the Logos Papers series are:
- Complete and properly formatted
- Accurate and verifiable
- Consistent across papers
- Up to academic standards

## Context
The Logos Papers synthesize physics, theology, mathematics, and consciousness studies, requiring:
- Citations to scientific literature
- Citations to theological/philosophical works
- Cross-references between papers in the series
- Cross-references within each paper (figures, equations, sections)

This prompt provides systematic checking of all reference types.

## Instructions

You are tasked with validating citations and references in a Logos Paper. Follow this systematic approach:

## Phase 1: Bibliography Verification

### Step 1: Catalog All Citations

Go through the paper and list every citation in the text:

**Format:**
```markdown
## Citations Catalog

### In-Text Citations
1. (Einstein, 1905) - Line 45
2. (Wheeler, 1990) - Line 67
3. (Chalmers, 1996) - Line 123
...

### Reference List Entries
1. Einstein, A. (1905). "On the Electrodynamics of Moving Bodies"...
2. Wheeler, J.A. (1990). "Information, Physics, Quantum"...
...
```

### Step 2: Match Citations to References

For each in-text citation, verify:
- [ ] Matching entry in References section
- [ ] Author name spelled correctly (both locations)
- [ ] Year matches
- [ ] Citation format consistent

**Common Issues:**
- Citation (Wheeler, 1990) but reference says (Wheeler, 1989)
- Author name variations: "von Neumann" vs "Von Neumann"
- Missing reference for cited work
- Reference entry without any citation in text

### Step 3: Verify Reference Completeness

Each reference must include:

**For Journal Articles:**
- Author(s)
- Year
- Title (in quotes)
- Journal name (italicized)
- Volume(Issue)
- Page numbers
- DOI (if available)

**Example:**
```
Chalmers, D. J. (1995). "Facing Up to the Problem of Consciousness." 
*Journal of Consciousness Studies*, 2(3), 200-219.
```

**For Books:**
- Author(s)
- Year
- *Title* (italicized)
- Publisher
- Location (optional for major publishers)

**Example:**
```
Penrose, R. (1989). *The Emperor's New Mind: Concerning Computers, Minds, 
and the Laws of Physics*. Oxford University Press.
```

**For Book Chapters:**
- Author(s)
- Year
- "Chapter Title" (in quotes)
- In Editor(s) (Ed.), *Book Title* (italicized)
- Pages (pp. X-Y)
- Publisher

**Example:**
```
Stapp, H. P. (2007). "Quantum Mechanical Theories of Consciousness." 
In M. Velmans & S. Schneider (Eds.), *The Blackwell Companion to Consciousness* 
(pp. 300-312). Blackwell Publishing.
```

### Step 4: Check Citation Style Consistency

Logos Papers use a hybrid format. Verify:

**In-text citations:**
- Parenthetical: (Author, Year)
- Narrative: Author (Year)
- Multiple authors: (Author et al., Year)
- Multiple works: (Author1, Year1; Author2, Year2)

**References section:**
- Alphabetical by first author
- Hanging indent
- Consistent punctuation
- Italics used properly

## Phase 2: Cross-References Within Paper

### Step 5: Figure References

List all figures and their references:

**Format:**
```markdown
## Figure Inventory

Figure 1: Logos Field Schematic (Line 89)
  Referenced at: Lines 45, 67, 102
  ✓ All references valid
  
Figure 2: Grace Function Graph (Line 156)
  Referenced at: Line 150
  ⚠ Referenced BEFORE it appears - reorder needed
  
Figure 3: (Line 234)
  ❌ Never referenced in text - add reference or remove figure
```

**Check:**
- [ ] All figures numbered sequentially
- [ ] All figures referenced in text
- [ ] References appear after or near figure
- [ ] Figure captions are complete
- [ ] Image files exist

### Step 6: Equation References

For equations that are numbered or referenced:

**Example Check:**
```markdown
Text says: "As shown in Equation (3)..."
✓ Equation 3 exists at line 145
✓ Equation is numbered (3)
✓ Reference is after equation

Text says: "From the Master Equation..."
✓ Master Equation defined in Section 2.1
✓ Proper context provided
```

**Common Issues:**
- Wrong equation number
- Reference before equation is introduced
- Equation numbered but never referenced
- Missing equation number for important equation

### Step 7: Section Cross-References

Check all section references:

**Example:**
```markdown
Text: "As discussed in Section 3.2..."
✓ Section 3.2 exists
✓ Content matches reference
✓ Section not significantly later in paper

Text: "See the Appendix for derivation"
❌ No Appendix present - remove reference or add appendix
```

**Check:**
- [ ] Section numbers accurate
- [ ] Section titles match if mentioned
- [ ] Forward references acknowledged ("as we will see")
- [ ] No circular references

## Phase 3: Inter-Paper References

### Step 8: References to Other Logos Papers

List all references to other papers in the series:

**Format:**
```markdown
## Inter-Paper References

"As established in Paper 1..." (Line 34)
✓ Paper 1 covers this topic
✓ Specific claim is accurate
⚠ Could add page/section reference for precision

"See Paper 5 for details on soul field theory" (Line 189)
✓ Paper 5 is about soul field
✓ Reference appropriate
✓ Could link to specific section

"Paper 11 provides experimental protocols" (Line 267)
✓ Accurate
✓ Appropriately phrased
```

### Step 9: Verify Cross-Paper Claims

When a paper claims something from another paper, verify:

**Example:**
```markdown
Paper 7 states: "As shown in Paper 3, the Master Equation requires..."

Check Paper 3:
✓ Master Equation is derived in Paper 3
✓ The specific requirement IS established
✓ No contradiction
```

**If contradiction found:**
```markdown
Paper 9 states: "Paper 5 demonstrates coupling constant g ~ 10⁻¹²"
Paper 5 actually says: "g ~ 10⁻¹⁵ to 10⁻¹⁸"

❌ INCONSISTENCY - Update Paper 9 to match Paper 5
```

### Step 10: Notation Consistency Check

Verify symbols mean the same thing across papers:

**Create symbol table:**
```markdown
## Symbol Usage Across Papers

χ (chi):
- Paper 1: Logos Field coherence ✓
- Paper 3: Logos Field coherence ✓
- Paper 5: Coherence ✓
- Consistent across series ✓

g (coupling constant):
- Paper 5: Soul-matter coupling ~ 10⁻¹⁵ ✓
- Paper 7: Grace efficiency (κ used instead) ✓
- Different meanings, different symbols ✓

F (Faith):
- Paper 2: Faith parameter [0,1] ✓
- Paper 7: Faith parameter [0,1] ✓
- Paper 9: Faith parameter [0,1] ✓
- Consistent across series ✓
```

## Phase 4: External Reference Verification

### Step 11: Spot-Check Key Citations

For critical claims based on external sources, verify accuracy:

**High Priority to Check:**
- Quantitative claims (e.g., "Hubble constant H₀ = 73 km/s/Mpc")
- Controversial claims
- Foundations of arguments
- Recent results
- Cited experiments

**Verification Process:**
1. Look up the cited paper (DOI, journal, etc.)
2. Verify claim is accurately represented
3. Check year and details are correct
4. Note if citation is secondary (citing a review, not original)

**Flag for correction:**
```markdown
❌ Paper states: "Tononi (2012) defines Φ as complexity"
    Actual: Tononi defines Φ as "integrated information," 
            NOT just "complexity"
    Correction needed: Update description
```

### Step 12: Check for Link Rot

If paper includes web links:
- [ ] Test that URLs still work
- [ ] For crucial links, note archive.org backup
- [ ] For broken links, find replacement or remove

**Better Practice:**
- Prefer DOI links over direct URLs
- Use permanent links (handle.net, etc.)
- Include access date for web resources

## Phase 5: Citation Style Specific Checks

### Step 13: Stanford Encyclopedia of Philosophy Links

The papers link to Stanford Encyclopedia entries:

**Standard format:**
```markdown
[quantum mechanics](https://plato.stanford.edu/entries/qm/)
[hard problem of consciousness](https://iep.utm.edu/hard-problem-of-consciousness/)
```

**Check:**
- [ ] URL is correct
- [ ] Link text matches article title
- [ ] Entry is relevant to discussion
- [ ] Not overused (1-3 per paper is plenty)

### Step 14: Scripture References

For biblical citations:

**Format:**
```markdown
"In the beginning was the Word..." (John 1:1)
"stretches out the heavens" (Isaiah 42:5)
```

**Check:**
- [ ] Book name spelled correctly
- [ ] Chapter:verse format correct
- [ ] Quote is accurate (compare to translation)
- [ ] Translation noted if non-standard (ESV, NIV, KJV, etc.)

**For Hebrew/Greek terms:**
```markdown
The Hebrew verb נָטָה (*natah*) means "to stretch out"
```

**Check:**
- [ ] Original language text correct
- [ ] Transliteration accurate
- [ ] Definition accurate
- [ ] Source for language claim (lexicon, etc.)

## Output Format

### Citation Report Template

```markdown
# Citation & Cross-Reference Report: Paper [#] - [Title]

## Summary
- Total in-text citations: [##]
- Total reference entries: [##]
- Orphaned citations: [##] (cited but not in references)
- Orphaned references: [##] (in references but never cited)
- Cross-paper references: [##]
- Figure cross-references: [##]
- Equation cross-references: [##]

## Issues Found

### Critical (Must Fix)
1. [Issue description and location]
2. [Issue description and location]

### Important (Should Fix)
1. [Issue description and location]
2. [Issue description and location]

### Minor (Optional Improvement)
1. [Issue description and location]
2. [Issue description and location]

## Verification Results

### In-Text → References Matching
- [##] citations properly matched
- [##] citations missing references
- [List missing]

### References → In-Text Matching
- [##] references properly cited
- [##] references never cited in text
- [List uncited]

### Figure References
- [##] figures total
- [##] figures properly referenced
- [List problems]

### Equation References
- [##] numbered equations
- [##] referenced in text
- [List unreferenced or mis-referenced]

### Inter-Paper Consistency
- [##] claims cross-checked
- [##] inconsistencies found
- [List inconsistencies]

## Recommendations

1. [Specific action needed]
2. [Specific action needed]
3. [Specific action needed]

## Verified Accurate

[List of citations/references that were spot-checked and verified correct]
```

## Common Citation Errors

1. **Author name misspelling**
   - "Penrose" vs "Penrose"
   - "von Neumann" vs "Von Neumann"
   - "et al" vs "et al."

2. **Year mismatches**
   - Text: (Einstein, 1905)
   - Ref: Einstein, A. (1906)...

3. **Incomplete references**
   - Missing journal name
   - Missing page numbers
   - Missing DOI

4. **Formatting inconsistencies**
   - Some titles in quotes, others not
   - Inconsistent italicization
   - Mixed citation styles

5. **Broken cross-references**
   - "See Figure 3" but only 2 figures
   - "Equation (5)" but equation not numbered
   - "Section 4.2" doesn't exist

6. **Circular or forward references**
   - Referencing a concept before it's defined
   - Paper A cites Paper B which cites Paper A for same claim

7. **Outdated information**
   - Citing preliminary results when final paper available
   - Using old parameter values contradicted by recent papers

## Best Practices

### For Citations:
- Cite primary sources when possible
- Include DOIs for all papers that have them
- Use consistent citation style throughout
- Cite generously but not excessively
- Balance classic and recent references

### For Cross-References:
- Reference figures near where they appear
- Explain what reader should notice in figure
- Number only equations that will be referenced
- Use descriptive section titles that can be referenced clearly

### For Inter-Paper References:
- Be specific: "Paper 3, Section 2.1" not just "Paper 3"
- Verify claim before referencing
- Update if earlier paper changes
- Don't over-reference—assume readers have context

## Validation Checklist

Before approving citations:
- [ ] Every in-text citation has reference entry
- [ ] Every reference entry is cited in text
- [ ] All references complete and properly formatted
- [ ] All figures referenced in text
- [ ] All numbered equations referenced in text
- [ ] All section cross-references valid
- [ ] All inter-paper claims verified
- [ ] Symbol usage consistent across papers
- [ ] Key citations spot-checked for accuracy
- [ ] Web links tested
- [ ] Scripture references accurate
- [ ] No citation style inconsistencies

## Notes

- Academic credibility depends on proper citations
- Inconsistencies between papers undermine series coherence
- Readers should be able to follow and verify all claims
- Citation errors are embarrassing and easy to fix
- When in doubt, over-cite rather than under-cite
- Keep a master bibliography for the series

