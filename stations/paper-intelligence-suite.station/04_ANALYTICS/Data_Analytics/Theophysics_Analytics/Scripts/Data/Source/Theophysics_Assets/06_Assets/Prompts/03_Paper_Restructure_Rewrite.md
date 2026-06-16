---
uuid: 220fc6da-df86-5bb4-b9e1-92d5266fc266
title: Paper Restructure & Rewrite Prompt
author: David Lowe
type: paper
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\Assets\Prompts\03_Paper_Restructure_Rewrite.md
uuid_generated_at: '2025-11-22T01:23:03.422506'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# Paper Restructure & Rewrite Prompt

## Purpose
Transform jumbled, incomplete, or poorly structured paper drafts into polished, well-organized academic papers following the Logos Papers standard format.

## Context
Some Logos Papers may have:
- Mixed content from multiple versions
- Random text fragments or conversation snippets
- Missing sections
- Poor flow or organization
- Inconsistent tone
- Duplicate content
- JSON-formatted text that needs conversion

This prompt provides a systematic approach to clean up and restructure these papers.

## Instructions

You are an academic editor tasked with restructuring a Logos Paper. Follow this workflow:

## Phase 1: Assessment & Inventory

### Step 1: Identify Issues
Read through the entire paper and catalog problems:

**Content Issues:**
- [ ] Duplicate sections
- [ ] Missing critical sections (Abstract, Introduction, Conclusion)
- [ ] Mixed content from different paper versions
- [ ] Random conversation fragments
- [ ] JSON or malformed text
- [ ] Orphaned paragraphs with unclear context

**Structure Issues:**
- [ ] Unclear section hierarchy
- [ ] Poor logical flow
- [ ] Missing transitions
- [ ] Sections in wrong order
- [ ] Headers inconsistently formatted

**Quality Issues:**
- [ ] Tone inconsistency (academic vs. conversational)
- [ ] Incomplete sentences or thoughts
- [ ] Mathematical notation errors
- [ ] Missing citations or references
- [ ] Unclear arguments

### Step 2: Extract Salvageable Content
Create an outline of what usable content exists:

```markdown
## Content Inventory

### Introduction Material
- [Paragraph about X]
- [Paragraph about Y]

### Main Arguments
1. [Argument 1 with supporting text]
2. [Argument 2 with supporting text]

### Mathematical Formalism
- [Equation 1 with context]
- [Equation 2 with context]

### Evidence/Examples
- [Example 1]
- [Example 2]

### Conclusions
- [Conclusion points]

### Fragments to Clarify
- [Text needing context]
- [Unclear references]
```

### Step 3: Identify Missing Content
Based on paper topic and series position, determine what's missing:

**Essential Sections:**
- Abstract (150-300 words)
- Introduction with motivation
- Background/Prior Work
- Main theoretical content
- Mathematical formalism
- Testable predictions
- Discussion
- Conclusion
- References

## Phase 2: Structure Planning

### Step 4: Design Target Structure

For Logos Papers, use this standard template:

```markdown
---
[YAML Header]
---

# PAPER [#]: [TITLE]

## [Subtitle]

---

**Authors:**  
David Lowe¹  
Claude (Anthropic)²

**Affiliations:**  
¹ Independent Researcher, Oklahoma City, OK  
² Anthropic PBC, San Francisco, CA

**Date:** [Date]

**Paper:** [#] of 12 in the Logos Papers series

---

## ABSTRACT

[150-300 words summarizing: problem, approach, results, implications]

**Keywords:** [5-10 keywords]

---

## 1. INTRODUCTION

### 1.1 [Subsection]
### 1.2 [Subsection]

## 2. [MAIN SECTION 1]

### 2.1 [Subsection]
### 2.2 [Subsection]

## 3. [MAIN SECTION 2]

[Continue with logical flow...]

## [N]. CONCLUSION

## REFERENCES

## NAVIGATION

[Previous: ...] | [Home: ...] | [Next: ...]

---

**License:** CC BY-NC 4.0
```

### Step 5: Create Detailed Outline
Map existing content to target structure:

```markdown
## Target Structure with Content Mapping

1. INTRODUCTION
   - 1.1 The Problem → Use paragraphs 3, 7, 12 from current draft
   - 1.2 Our Approach → Create new, synthesizing ideas from fragments
   
2. BACKGROUND
   - 2.1 Prior Attempts → Use paragraphs 15-18
   - 2.2 Why They Failed → Extract from paragraph 22
   
3. THE [MAIN FRAMEWORK]
   - 3.1 Core Postulate → Clean up section currently at line 45
   - 3.2 Mathematical Formalism → Equations from lines 67-89, needs reorganization
   
[etc.]
```

## Phase 3: Content Transformation

### Step 6: Clean and Rewrite Each Section

For each section in the outline:

**A. Remove garbage:**
- Delete conversation fragments ("I'll get my shoes", etc.)
- Remove meta-commentary ("This needs work", etc.)
- Delete duplicate text
- Remove broken JSON formatting

**B. Improve clarity:**
- Rewrite unclear sentences
- Add topic sentences
- Improve transitions
- Ensure logical flow

**C. Maintain academic tone:**
- Convert casual language to formal
- Remove first-person unless appropriate
- Use precise technical terminology
- Maintain professional voice

**D. Preserve mathematical content:**
- Keep all equations intact
- Add context where missing
- Ensure proper LaTeX formatting
- Number important equations

**Example Transformation:**

**Before:**
```
So basically what I want what I have to have is like the universe runs on code 
you know not like metaphorically but literally executing algorithms and stuff 
and this isn't simulation theory btw
```

**After:**
```
This paper argues that reality itself is fundamentally computational—not 
metaphorically, but in a precise, mathematical sense. The universe executes 
an algorithm at its foundation because information is the fundamental substrate 
of existence. This is distinct from simulation theory; we are not claiming 
reality runs on someone else's computer, but rather that computation is 
intrinsic to physical law.
```

### Step 7: Fill Missing Sections

For any missing essential content:

**Option A - Generate from context:**
If the paper has enough content to infer what should be in missing sections, write them based on:
- Overall paper thesis
- Related papers in the series
- Standard academic conventions

**Option B - Flag for author input:**
If critical content is missing and cannot be reliably inferred, add placeholder:

```markdown
## [SECTION TITLE]

**[AUTHOR NOTE: This section needs to be written. Based on the paper's focus on 
[topic], it should cover:
- [Point 1]
- [Point 2]
- [Point 3]
]**
```

### Step 8: Improve Mathematical Presentation

For all equations:

1. **Context before equation**: Never drop an equation without setup
2. **Explain notation**: Define all symbols
3. **Physical interpretation**: Explain what it means
4. **Derivation or citation**: Show where it comes from
5. **Limiting cases**: Discuss special cases or limits

**Example:**

**Before:**
```
$$F = ma$$
```

**After:**
```
Newton's second law provides the fundamental relationship between force, mass, 
and acceleration:

$$F = ma$$

where F is the net force (in Newtons), m is mass (kg), and a is acceleration 
(m/s²). This equation shows that force is the rate of change of momentum, and 
in the limit where mass is constant, it simplifies to the familiar form above.
```

## Phase 4: Quality Enhancement

### Step 9: Check Cross-References

Ensure all internal references work:
- Figure numbers correct and sequential
- Equation references point to right equations
- Section cross-references accurate
- Citations to other papers in series correct

### Step 10: Verify Consistency with Series

Check that:
- Notation matches other papers (χ for coherence, etc.)
- Parameter values consistent (g ~ 10⁻¹⁵, etc.)
- Frameworks referenced correctly
- No contradictions with other papers
- Build on rather than repeat prior papers

### Step 11: Add Missing Elements

**Figures:**
If text references figures that don't exist:
```markdown
![Figure Title](../Assets/images/P[##]_figure_name.png)

**Figure [#]. [Title]**

[Caption describing the visualization and its significance]

*Visualization: Claude (Anthropic), [Date]*
```

**Callouts/Boxes:**
For important points, use:
```markdown
> [!important] **Key Insight**
> [Important point that should stand out]
```

**Navigation:**
Every paper needs:
```markdown
## NAVIGATION

[Previous: Paper [##] - [Title]](./Paper%20[##]%20-%20[Title]%20-%20FULL.md) | 
[Home](../00-Series-Index.md) | 
[Next: Paper [##] - [Title]](./Paper%20[##]%20-%20[Title]%20-%20FULL.md)
```

## Phase 5: Final Polish

### Step 12: Style Consistency

**Headings:**
- Use ## for main sections (numbered)
- Use ### for subsections (numbered)
- Use #### sparingly for sub-subsections

**Emphasis:**
- **Bold** for key terms on first use
- *Italics* for emphasis or technical terms
- `Code` for variables in text
- _Underscored italics_ for book titles

**Lists:**
- Use numbered lists for sequential items
- Use bullet lists for non-sequential items
- Maintain parallel structure

**Equations:**
- Display: $$...$$ for important equations on own line
- Inline: $...$ for symbols or brief expressions in text
- Number key equations: Add (1), (2), etc. if referenced

### Step 13: Readability Check

Read through as if you're the target audience:
- Does introduction hook and motivate?
- Can you follow the argument?
- Are technical terms defined?
- Do examples clarify or confuse?
- Is the conclusion satisfying?

### Step 14: Academic Rigor Check

Verify:
- Claims are supported with reasoning or evidence
- Arguments are logical and complete
- Assumptions are stated
- Limitations are acknowledged
- Appropriate caveats given

## Special Cases

### Case 1: Mixed Paper Versions

If paper contains two competing versions (e.g., Paper 4 had both "Hard Problem" and "Chronos-Logos"):

1. **Determine primary focus** from title and paper number
2. **Extract best content** from each version
3. **Create single unified** paper
4. **Archive alternate version** with note about future paper

### Case 2: JSON or Structured Data

If paper contains JSON-like formatting:

```json
{
  "title": "Paper 4",
  "content": "The hard problem..."
}
```

Convert to proper markdown:
```markdown
# Paper 4: The Hard Problem of Consciousness

The hard problem of consciousness...
```

### Case 3: Conversation Fragments

Remove fragments like:
- "I'll be back in a minute"
- "Oh wait I forgot to mention"
- "Hold on let me find..."
- Timestamps
- User prompts mixed in text

### Case 4: Missing Abstract

Generate abstract using this template:
1. **Problem statement** (2 sentences)
2. **Approach** (2-3 sentences)
3. **Key results** (2-3 sentences)
4. **Implications** (1-2 sentences)

Total: 150-300 words

## Output Checklist

Before considering restructure complete:

- [ ] YAML header present and valid
- [ ] Title and metadata complete
- [ ] Abstract 150-300 words, informative
- [ ] Introduction motivates and previews
- [ ] Logical section flow
- [ ] All equations have context
- [ ] All figures referenced and described
- [ ] Mathematical notation consistent
- [ ] Cross-references valid
- [ ] Conclusion summarizes contributions
- [ ] References complete
- [ ] Navigation links present
- [ ] No conversation fragments
- [ ] No duplicate content
- [ ] No missing sections (or flagged)
- [ ] Academic tone throughout
- [ ] Readability appropriate for target audience
- [ ] Consistent with rest of series

## Quality Standards

**Excellent restructure should:**
- Read like a cohesive, professionally written paper
- Have clear, logical argument flow
- Be accessible to educated non-expert
- Have rigorous technical content for experts
- Build on previous papers without excessive repetition
- Make unique contribution to series
- Inspire confidence in readers

**Red flags (needs more work):**
- Still contains fragments or garbage text
- Unclear argument or purpose
- Missing critical sections
- Inconsistent notation or terminology
- Equations without context
- Poor transitions
- Tone shifts (casual to academic and back)

## Example: Paper 4 Restructure

**Before:** Jumbled with two competing frameworks, conversation fragments, abrupt mid-sentence cutoffs

**After:** Clean paper focused on Hard Problem of Consciousness, using Logos Field framework to dissolve the problem through ontological inversion

**Changes made:**
1. Removed duplicate titles
2. Deleted conversation fragments ("I'll find my shoes...")
3. Chose Hard Problem as primary focus (Chronos-Logos mentioned as potential future paper)
4. Reorganized into logical flow:
   - The Hard Problem explained
   - Failed materialist solutions
   - Ontological inversion as solution
   - Evidence from anomalous phenomena
   - Testable predictions
5. Added missing sections (Conclusion, References, Navigation)
6. Unified tone throughout
7. Added proper YAML header

**Result:** Professional academic paper ready for review

## Notes

- Restructuring is creative work—use judgment
- Preserve author's voice and key ideas
- When in doubt, flag for author review
- Consistent terminology across papers is critical
- Don't invent facts or claims—work with given content
- It's okay to write "To be developed" for missing content
- Quality over speed—better to do it right than fast

