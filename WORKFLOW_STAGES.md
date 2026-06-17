# MDA ARTICLE PRODUCTION WORKFLOW
# POF 2828 | 2026-06-17
# The manufacturing line. Order matters. Every stage feeds the next.

---

## THE LINE (sequential, no skipping)

### STAGE 0: SOURCE VERIFICATION
**Input:** `D:\GitHub\faiththruphysics-site\moral-decline\`
**Gate:** Every article has math translation blocks with `data-eq-id` attributes.
**Check:**
- [ ] All equations wrapped in `.math-translation-block`
- [ ] Each block has reading levels (easy, standard, academic, proof)
- [ ] `mtl-equations.json` covers all equation IDs
- [ ] MathJax renders correctly
**Output:** Verified HTML source files
**Failure mode:** Missing equation translation → markdown gets raw LaTeX → NLP treats notation as text → garbage claims

### STAGE 1: HTML → MARKDOWN CONVERSION
**Input:** Verified HTML from Stage 0
**Gate:** Clean markdown with equations AND their translations preserved.
**Check:**
- [ ] HTML tags stripped cleanly (no orphan tags)
- [ ] Equations preserved (LaTeX notation intact)
- [ ] Plain English translations preserved as content
- [ ] Section headings mapped to markdown `#` levels
- [ ] Tables converted (if any)
- [ ] No encoding artifacts (mojibake, &amp; entities)
- [ ] Reading level tabs extracted correctly
**Output:** `.md` files in staging directory
**Failure mode:** Bad conversion → lost content → every downstream station works on incomplete text

### STAGE 2: VECTORIZATION (ChromaDB)
**Input:** Clean markdown from Stage 1
**Gate:** Every article embedded and queryable in vector store.
**Check:**
- [ ] SBERT embeddings generated for each article
- [ ] Chunked by section (not whole-document — too large for useful retrieval)
- [ ] Metadata stored: article_id, section, series_group, equation_count
- [ ] `/vector/query` returns relevant results for test queries
- [ ] `/vector/stats` shows correct document count
**Output:** Populated ChromaDB collection `theophysics_corpus`
**Failure mode:** Bad chunking → retrieval misses → evidence mapping can't find cross-references

### STAGE 3: CORE NLP PIPELINE (8 stations, sequential)
**Input:** Markdown files from Stage 1, vector store from Stage 2
**Order within stage:**

| Step | Station | What it does | Depends on |
|------|---------|-------------|-----------|
| 3a | ST_001 exec-summary | Summary + NER entities | Stage 1 markdown |
| 3b | ST_002 plain-language | 3 reading level rewrites | Stage 1 markdown |
| 3c | ST_003 claim-extraction | Extract every claim with position | Stage 1 markdown |
| 3d | ST_004 claim-classification | Classify claims by maturity + domain | 3c claims |
| 3e | ST_005 load-bearing-claims | Triage: PAPER_CLAIM / CITATION_FACT / REVIEW / PARK | 3c + 3d |
| 3f | ST_006 falsification | Kill conditions + evidence bars | 3e load-bearing claims |
| 3g | ST_007 evidence-map | Map evidence to claims, find gaps | 3e + Stage 2 vectors |
| 3h | ST_008 contradiction-scan | Cross-claim contradiction detection | 3c + Stage 2 vectors |

**Gate:** Each station produces valid JSON artifact in `_outbox/`.
**Check per station:**
- [ ] Artifact JSON has `success: true`
- [ ] `data` field is populated (not empty)
- [ ] No errors in `errors` array
- [ ] Job card updated (when wired)
**Failure mode:** Station crash → downstream stations get no input → pipeline stalls

### STAGE 4: ENRICHMENT
**Input:** NLP artifacts from Stage 3
**Check:**
- [ ] Paper grader scores generated
- [ ] Proof explorer data assembled (7 framework tabs)
- [ ] Glossary terms extracted (anything above 8th grade reading level)
- [ ] Cross-article knowledge graph links identified
**Output:** Enrichment JSON artifacts

### STAGE 5: ASSEMBLY (rebuild HTML for site)
**Input:** All artifacts from Stages 3-4 + original HTML from Stage 0
**Check:**
- [ ] Reading level tabs populated with Stage 3b rewrites
- [ ] Claims tab populated with Stage 3c-3e data
- [ ] Proof explorer wired with Stage 4 data
- [ ] Glossary terms linked
- [ ] Audio dock wired (TTS from plain-language rewrites)
**Output:** Production-ready HTML files

### STAGE 6: PUBLISH
**Input:** Assembled HTML from Stage 5
**Check:**
- [ ] Deployed to faiththruphysics.com via Cloudflare Pages
- [ ] All internal links resolve
- [ ] MathJax renders
- [ ] Math translation overlay works
- [ ] Reading level tabs switch correctly
**Output:** Live site

---

## DEPENDENCIES (what blocks what)

```
Stage 0 (verify) ──→ Stage 1 (HTML→MD) ──→ Stage 2 (vectorize)
                                      │              │
                                      ▼              │
                                   Stage 3a-3b       │
                                      │              │
                                      ▼              │
                                   Stage 3c          │
                                      │              │
                                      ▼              ▼
                                   3d → 3e → 3f → 3g, 3h
                                              │
                                              ▼
                                         Stage 4 (enrich)
                                              │
                                              ▼
                                         Stage 5 (assemble)
                                              │
                                              ▼
                                         Stage 6 (publish)
```

Note: 3a and 3b can run in PARALLEL with 3c (they don't depend on each other).
3g and 3h can run in PARALLEL (both need 3e + vectors, neither needs the other).
Everything else is strictly sequential.

---

## TRACKING

Each article gets a status line. Format:
`ARTICLE_ID | S0 | S1 | S2 | S3a | S3b | S3c | S3d | S3e | S3f | S3g | S3h | S4 | S5 | S6`

Status codes: `-` not started, `R` running, `P` passed, `F` failed, `S` skipped

Example:
```
MDA-039 | P | P | P | P | P | R | - | - | - | - | - | - | - | -
```

### CURRENT STATUS (all 61 articles)
```
All articles: S0=- | Everything else = -
```
Pipeline has not started. First run: pick ONE article, push it through all stages,
verify output at each gate before batch processing the rest.

---

## TEST ARTICLE

**Recommended first test:** `MDA-039-physics-of-coherence.html`
- Has equations (tests math translation preservation)
- Medium length (not too short, not overwhelming)
- In the method-and-metrics group (representative of technical content)
- Has 3 equation blocks with data-eq-id (verifiable)

---

## RULES

1. **Never skip a stage.** If Stage 0 isn't verified, don't start Stage 1.
2. **Test one before batching.** Run one article end-to-end before processing 61.
3. **Gate checks are mandatory.** A stage isn't done until its checklist passes.
4. **Failures propagate.** If Stage 1 fails for an article, mark all downstream stages as blocked.
5. **The NAS copy (X:\mda\) is NOT the source.** Source is `moral-decline/` on D: drive.
6. **The FastAPI service must be running** before any Stage 3 work (port 8700).

---
*Created: 2026-06-17 | Last updated: 2026-06-17*
