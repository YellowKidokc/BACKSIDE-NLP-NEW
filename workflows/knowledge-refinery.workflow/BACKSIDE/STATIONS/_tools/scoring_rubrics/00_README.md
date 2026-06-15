---
publish: false
---
# EVALUATION BUNDLE
## Complete AI Evaluation Workflow for Research Projects

---

## WHAT THIS IS

A complete 4-prompt workflow for having multiple AIs evaluate a research folder/paper:

1. **Step 1:** Claim Indexer (extract and classify claims)
2. **Step 2:** Sectional Coherence (evaluate each section by its role)
3. **Step 3:** Meta-Synthesis (combine outputs from multiple AIs)
4. **Step 4:** LSDP Protocol (format for publication)

---

## HOW TO USE

### **NEW USERS START HERE:**
1. Read **`FOR_NORMAL_PEOPLE.md`** for a plain-English explanation
2. Read **`QUICK_START_ONE_PAGE.md`** for a one-page reference
3. Use **`05_INTEGRATED_FRUITS_EVALUATOR.md`** for quick validation

### Traditional 4-Step Workflow:
1. Pick a folder or paper to evaluate
2. Run **01_CLAIM_INDEXER.md** on it with 3 different AIs (Claude, GPT, Gemini)
3. Run **02_SECTIONAL_COHERENCE.md** on each section
4. Feed all outputs into **03_META_SYNTHESIS.md** to get consensus
5. Use **04_LSDP_PROTOCOL.md** to format for publication

### Quick Workflow (Single AI):
1. Run **05_INTEGRATED_FRUITS_EVALUATOR.md** with one AI
2. Get technical + coherence scores
3. Fix low-scoring sections
4. Re-run to confirm

---

## FILES IN THIS BUNDLE

### Core Workflow
| File | Purpose | Input | Output |
|------|---------|-------|--------|
| `FOR_NORMAL_PEOPLE.md` | Non-technical guide | None | Easy explanation |
| `QUICK_START_ONE_PAGE.md` | One-page reference | None | Quick guide |
| `01_CLAIM_INDEXER.md` | Extract claims | Raw text | JSON + Mermaid diagram |
| `02_SECTIONAL_COHERENCE.md` | Evaluate sections | Section text | Scorecard |
| `03_META_SYNTHESIS.md` | Combine AI outputs | 3x JSON/Scorecards | Consensus report |
| `04_LSDP_PROTOCOL.md` | Publication format | Final analysis | Series manifest |
| `05_INTEGRATED_FRUITS_EVALUATOR.md` | All-in-one prompt | Raw text | Technical + Coherence scores |

### Advanced Evaluation
| File | Purpose |
|------|---------|
| `FOUR_PILLARS.md` | Grounded truth framework (History/Science/Philosophy/Theology) |
| `EPISTEMIC_GRADING_SYSTEM.md` | **3-phase evaluation** for multi-folder projects |
| `LLM_JUDGMENT_LAYER.md` | Contract for LLM semantic triage over evidence bundles |

---

## KEY PRINCIPLES

### Zero Evaluation in Step 1
The Claim Indexer does NOT judge quality. It extracts WHAT is claimed and maps dependencies.

### Role-Based Evaluation in Step 2
Each section is judged ONLY by the job it's supposed to do. An Introduction isn't punished for lacking statistics.

### Multi-Model Consensus in Step 3
Run the same prompts on 3 different AIs. Disagreement = underspecified text, not model error.

### Traceable Evidence in Step 4
Every claim maps to a specific location in the source material using the curly bracket system: `{P#, §X.X, Element}`

---

## ORIGIN

Developed for the Theophysics project to evaluate research folders with rigor, transparency, and multi-AI consensus.

Based on:
- IPCC report structure
- Academic peer review processes
- Supreme Court majority/dissent format

---

*Read each file in order for the full methodology.*
