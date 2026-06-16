# THEOPHYSICS PAPER INTELLIGENCE SUITE
**Version:** 2.0 | **Author:** David Lowe + Claude | **Built:** 2026-03-27

---

## WHAT THIS IS

A 7-layer analytical pipeline that runs every paper through a complete
intelligence stack — from raw word statistics up to semantic truth scoring
and knowledge graph construction.

**Run one paper or an entire series. All outputs go to Excel + vault.**

This suite now also includes a companion **Obsidian Brain Arm** module for
vault/subfolder intake, classification, and digest generation. That gives you
both sides of the mechanism:

- **Paper Intelligence** = deep scoring and rigor metrics per paper
- **Brain Arm** = folder inventory, document typing, HTML digest, CSV/JSON sidecars
- **Alignment Runner** = one command that runs both on the same folder and checks that the outputs reflect one another

---

## THE SEVEN LAYERS

### L1 — TEXT ANALYTICS (Word Games)
Standard NLP metrics every paper gets:
- Word count, sentence count, paragraph count
- Reading grade level (Flesch-Kincaid, Gunning Fog)
- Word density (unique words / total words)
- Average sentence length, paragraph length
- Top 25 keywords by frequency
- N-gram clustering (most common 2- and 3-word phrases)
- Vocabulary richness score

### L2 — ACADEMIC STANDARD (The Game)
Standard academic metrics:
- Citation count and citation density
- External theory references
- Footnote/endnote count
- Structural completeness (intro, body, conclusion markers)
- Reference diversity (how many unique sources)
- Academic signal words (hypothesis, evidence, demonstrate, etc.)

### L3 — THEOPHYSICS METRICS (Ours)
Proprietary framework metrics:
- CHI Coherence Score (0-10)
- Wisdom/Knowledge Ratio (goal: >1.0)
- Fruits of the Spirit Composite (12 dimensions, 0-10)
- Master Equation Variables (G,M,E,S,T,K,R,Q,F,C)
- Cross-Domain Bridge Count
- CKG Score (5-tier: Foundations/Propositions/Constraints/Evidence/Integration)

### L4 — OPENAI 7Q (Vault Product)
OpenAI runs the 7-Question Scientific Method on each paper:
- 7Q FORWARD: Classify the paper's claims
- 7Q REVERSE: Prove/disprove by exhaustive elimination
- Output: Strong questions, more citations, more theories, deeper understanding
- **This output goes directly into the vault as a product per paper**

### L5 — NLP DEEP (Semantic Layer)
Deep NLP analysis using installed packages:
- Named Entity Recognition (spacy) — people, places, concepts detected
- Topic Modeling (gensim LDA) — what topics does this paper contain?
- Semantic Similarity — how similar is this paper to others in the series?
- Key sentence extraction (most semantically central sentences)

### L6 — TRUTH ENGINE (Semantic Scorer)
Two-stage semantic truth measurement:
- Stage 1: Fruits of Spirit (9 anchors in 384-dim vector space)
- Stage 2: Chi Variables (G,M,E,S,T,K,R,Q,F,C anchors)
- Combined score → Tier: NEAR-CANONICAL / STRONG / PROVISIONAL / WEAK
- Dominant variable identification

### L7 — KNOWLEDGE GRAPHS (Big Deal)
Graph construction and analysis:
- Nodes = papers (scored and positioned)
- Edges = shared dominant variable, topic overlap, semantic similarity
- Centrality analysis (which papers are most connected?)
- Cluster detection (which papers belong together?)
- Bridge papers (what connects different clusters?)
- Export to JSON (web viz) + GraphML (Gephi/yEd) + neo4j

---

## OUTPUT FLOW

```
Each paper runs all 7 layers
        ↓
L4 (OpenAI 7Q) → writes directly to paper's vault folder
        ↓
L1-L3, L5-L7 → Excel workbook (one row per paper)
        ↓
David cleans Excel → 1-2 page template
        ↓
Template aggregates → paper-to-paper comparison
        ↓
Knowledge graph → visual map of the entire corpus
```

---

## HOW TO RUN

### Quick Start (single paper):
```
python 00_ORCHESTRATOR\run_pipeline.py --paper "path\to\paper.md"
```

### Full Series:
```
python 00_ORCHESTRATOR\run_pipeline.py --series "path\to\series\folder"
```

### With output directory:
```
python 00_ORCHESTRATOR\run_pipeline.py --series "path\to\series" --output "path\to\output"
```

Or just double-click: **LAUNCH.bat**

### Brain Arm only:
```
python 14_OBSIDIAN_BRAIN_ARM\run_obsidian_brain.py --vault "path\to\vault\folder"
```

### Paper Intelligence + Brain Arm alignment:
```
python 00_ORCHESTRATOR\run_brain_alignment.py --folder "path\to\vault\folder"
```

### Autonomous drop zones:
```
20_DROP_PAPER_ONLY\
21_DROP_BRAIN_ONLY\
22_DROP_BOTH_ALIGNMENT\
```

Each zone supports:

- drop `.md` files into `INBOX\`
- or point `FETCH_SOURCE.txt` at a file/folder
- then double-click the zone's `.bat` launcher

---

## WHAT'S ALREADY BUILT vs NEW

| Layer | Status | Script |
|-------|--------|--------|
| L1 Text Analytics | NEW (built here) | 01_TEXT_ANALYTICS\text_analyzer.py |
| L2 Academic Standard | NEW (built here) | 02_ACADEMIC_STANDARD\academic_scorer.py |
| L3 Theophysics Metrics | EXISTS - linked | 03_THEOPHYSICS_METRICS\theophysics_scorer.py |
| L4 OpenAI 7Q | Canonical adapter over imported 7Q engine | 04_OPENAI_7Q\seven_q_runner.py + 04_OPENAI_7Q\engine_v2\ |
| L5 NLP Deep | NEW (built here) | 05_NLP_DEEP\nlp_analyzer.py |
| L6 Truth Engine | EXISTS - linked | 06_TRUTH_ENGINE\truth_runner.py |
| L7 Knowledge Graphs | PARTIAL - extended | 07_KNOWLEDGE_GRAPHS\graph_builder.py |

**Companion subsystem:** `14_OBSIDIAN_BRAIN_ARM\obsidian_pipeline.py`

**Backend:** O:\999_IGNORE\Obsidian Programs\Python_Backend

---

## EXCEL OUTPUT STRUCTURE

One workbook per run:
- **Sheet 1: SUMMARY** — all papers, all metrics, sortable/filterable
- **Sheet 2: TEXT** — L1 + L2 detail
- **Sheet 3: THEOPHYSICS** — L3 detail (CHI, W/K, Fruits, ME vars)
- **Sheet 4: SEMANTIC** — L5 + L6 detail (NLP, Truth Engine)
- **Sheet 5: GRAPHS** — L7 centrality, cluster assignments
- **Sheet 6: 7Q** — L4 questions per paper (link to vault output)

---
