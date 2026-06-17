# WORKFLOW MAP: Article-to-Website Production Pipeline
# POF 2828 | 2026-06-17
# 
# Designed backwards from what faiththruphysics.com NEEDS per article.
# This WILL be wrong in places. That's the point — get the shape right,
# then Codex/David adjust the order and add missing steps.

---

## WHAT THE WEBSITE NEEDS (per article)

Each published article on faiththruphysics.com has these components:

| Component | Source | Currently |
|---|---|---|
| Standard text | Original writing | EXISTS |
| Easy reading tab | Plain-language rewrite | LOCKED (placeholder) |
| Academic tab | Academic version | LOCKED (placeholder) |
| Claims tab | Proof pressure layer | LOCKED (placeholder) |
| Executive summary box | Top of article | EXISTS (manual) |
| Glossary links | Inline term links to /glossary/ | PARTIAL |
| Math translations | Plain-English equation explanations | PARTIAL |
| Proof explorer data | grades_summary.json, claims CSV | EXISTS (needs refresh) |
| Audio | TTS mp3 | PARTIAL |
| Cross-article links | Prev/next navigation | EXISTS |
| Vectorization | Semantic search | NOT YET |
| Contradiction report | Cross-article consistency | NOT YET |

The pipeline's job: take a written article and produce ALL of the above automatically.

---

## THE 5-PHASE WORKFLOW

```
PHASE 1        PHASE 2           PHASE 3          PHASE 4        PHASE 5
INTAKE    -->   CORE NLP    -->   ENRICHMENT  -->  ASSEMBLY  -->  PUBLISH
(parse)        (ST_001-008)      (grade/vec/tts)  (rebuild HTML)  (deploy)
```

---

## PHASE 1: INTAKE

**Goal:** Parse the article into clean text + metadata. Everything downstream works from this.

```
Input: MDA-043-language-decay.html (from faiththruphysics-site repo)
  |
  v
[html-parser] ──> Strip components (nav, footer, sidebar, hero)
  |                Extract PAGE_META (series, part, title, status)
  |                Extract section headings + body text
  |                Extract existing executive summary
  |                Preserve paragraph indices (for claim mapping back to HTML)
  |
  v
Output: {
  "article_id": "MDA-043",
  "title": "Language Decay...",
  "series": "mda",
  "lane": "04-collapse-mechanisms",
  "part": 24,
  "sections": [ { "heading": "...", "paragraphs": [...], "indices": [...] } ],
  "text_clean": "full plain text...",
  "word_count": 4250,
  "html_path": "mda/04-collapse-mechanisms/MDA-043-language-decay.html"
}
```

**Station:** This needs a new station or can be the first step in html-article.station running in reverse (parse mode instead of build mode).

---

## PHASE 2: CORE NLP PIPELINE

**Goal:** Extract everything we need to know about the content.

```
Parsed article
  |
  +---> [ST_001 exec-summary] ──> summary + key entities
  |
  +---> [ST_002 plain-language] ──> easy + standard + academic versions
  |
  +---> [ST_003 claim-extraction] ──> all claims with paragraph positions
  |        |
  |        v
  |     [ST_004 claim-classification] ──> maturity labels + domain tags
  |        |
  |        v
  |     [ST_005 load-bearing-claims] ──> triage into queues
  |        |
  |        v
  |     [ST_006 falsification] ──> kill conditions + evidence bars
  |        |
  |        v
  |     [ST_007 evidence-map] ──> claim-to-evidence coverage
  |
  +---> [ST_008 contradiction-scan] ──> internal + cross-article contradictions
```

Note: ST_001 and ST_002 run independently of ST_003-007. 
ST_008 needs ST_005 output (the claims to compare).
ST_003 through ST_007 are sequential — each feeds the next.

**Key output for the website:**
- ST_002 produces the Easy and Academic tab content
- ST_003-005 produce the Claims tab content
- ST_006-007 produce the proof explorer data
- ST_008 produces the contradiction warnings

---

## PHASE 3: ENRICHMENT

**Goal:** Grade, vectorize, generate audio, build glossary.

```
Core NLP outputs
  |
  +---> [sbert-embedder] ──> article + claim embeddings
  |        |
  |        v
  |     [vector-store] ──> ingest into ChromaDB (all stations can query)
  |
  +---> [7q-classifier] ──> 7Q classification on load-bearing claims
  |
  +---> [paper-proof-grader] ──> grade (rubric, chi, truth, coherence scores)
  |        uses: ST_003 claims + ST_006 falsification + ST_007 evidence
  |
  +---> [math-translation-layer] ──> equation plain-English translations
  |        scans for LaTeX/MathJax blocks, generates explanations
  |
  +---> [reading-level-glossary] ──> extract terms needing glossary entries
  |        uses: ST_001 entities + zero-shot classifier
  |
  +---> [TTS_EDGE] ──> generate audio mp3 for each reading level
```

**Key output for the website:**
- Grading scores → proof-explorer/grades_summary.json
- Glossary terms → glossary/glossary_data.json
- Audio → audio/ folder
- Vectors → ChromaDB (enables cross-article search)

---

## PHASE 4: ASSEMBLY

**Goal:** Rebuild the HTML with all generated content injected.

```
All upstream outputs
  |
  v
[html-article.station] ──> Rebuild article HTML:
  |
  |  1. Update executive summary (from ST_001)
  |  2. Inject Easy tab content (from ST_002)
  |  3. Inject Academic tab content (from ST_002)  
  |  4. Build Claims tab:
  |     - Load-bearing claims list (from ST_005)
  |     - Each claim linked to its paragraph anchor
  |     - Kill condition + evidence bar (from ST_006)
  |     - Evidence match status (from ST_007)
  |     - Contradiction flags (from ST_008)
  |  5. Wire glossary links (from glossary station)
  |  6. Inject math translations (from math-layer)
  |  7. Update scores in footer/metadata
  |  8. Update prev/next navigation (from series manifest)
  |
  v
[series-flow-auditor] ──> Cross-check:
  |  - Are prev/next links correct?
  |  - Do section references match across articles?
  |  - Any contradiction flags that need manual review?
  |
  v
Output: production-ready HTML file
```

---

## PHASE 5: PUBLISH

**Goal:** Deploy to production.

```
Production HTML
  |
  +---> [mda-publication] ──> Copy to faiththruphysics-site repo
  |        git add, git commit, Cloudflare Pages auto-deploys
  |
  +---> [proof-explorer-update] ──> Regenerate:
  |        - grades_summary.json
  |        - mda-proof-layer-data.json
  |        - promoted claims CSV
  |        - per-article scorecards
  |
  +---> [obsidian-export] ──> Export to vault (O:\_Theophysics_v5)
  |
  +---> [postgres-sync] ──> Write claims, grades, evidence to database
  |
  +---> [vector-store ingest] ──> Update ChromaDB with final content
```

---

## FULL STATION CHAIN (linear view, approximate)

```
 1. html-parser (new)          -- parse article HTML to clean text + metadata
 2. ST_001 exec-summary        -- generate executive summary
 3. ST_002 plain-language       -- generate easy + academic versions  
 4. ST_003 claim-extraction     -- extract all claims with positions
 5. ST_004 claim-classification -- classify claims by maturity + domain
 6. ST_005 load-bearing-claims  -- triage into queues
 7. ST_006 falsification        -- generate kill conditions
 8. ST_007 evidence-map         -- map evidence to claims
 9. sbert-embedder              -- vectorize article + claims
10. vector-store                -- ingest into ChromaDB
11. ST_008 contradiction-scan   -- find contradictions (uses vector store)
12. 7q-classifier               -- 7Q classify load-bearing claims
13. paper-proof-grader          -- grade the article
14. math-translation-layer      -- translate equations
15. reading-level-glossary      -- extract glossary terms
16. TTS_EDGE                    -- generate audio
17. html-article                -- rebuild HTML with everything injected
18. series-flow-auditor         -- cross-article consistency check
19. mda-publication             -- route to production
20. proof-explorer-update       -- regenerate proof explorer data
21. obsidian-export             -- export to vault
22. postgres-sync               -- write to database
```

---

## WHAT'S MISSING (stations that don't exist yet)

| Need | Station | Notes |
|---|---|---|
| Parse HTML to text + metadata | html-parser.station (NEW) | Or reverse mode of html-article |
| ChromaDB vector store | vector-store.station (NEW) | FastAPI /vector/ endpoints exist, need station wrapper |
| Proof explorer data regen | proof-explorer-update.station (NEW) | Rebuilds grades_summary.json etc |
| Glossary data update | glossary-update.station (NEW) | Merges new terms into glossary_data.json |

---

## WORKFLOW JSON (for orchestrator)

This goes in workflows/ as `article-production.json`:

```json
{
  "name": "article-production",
  "description": "Full article-to-website production pipeline",
  "version": "1.0-DRAFT",
  "phases": [
    {
      "name": "intake",
      "stations": ["html-parser"],
      "parallel": false
    },
    {
      "name": "core-nlp",
      "stations": [
        {"name": "exec-summary", "depends": ["html-parser"]},
        {"name": "plain-language", "depends": ["html-parser"]},
        {"name": "claim-extraction", "depends": ["html-parser"]},
        {"name": "claim-classification", "depends": ["claim-extraction"]},
        {"name": "load-bearing-claims", "depends": ["claim-classification"]},
        {"name": "falsification", "depends": ["load-bearing-claims"]},
        {"name": "evidence-map", "depends": ["falsification"]}
      ]
    },
    {
      "name": "enrichment",
      "stations": [
        {"name": "sbert-embedder", "depends": ["html-parser"]},
        {"name": "vector-store", "depends": ["sbert-embedder"]},
        {"name": "contradiction-scan", "depends": ["load-bearing-claims", "vector-store"]},
        {"name": "7q-classifier", "depends": ["load-bearing-claims"]},
        {"name": "paper-proof-grader", "depends": ["claim-extraction", "falsification", "evidence-map"]},
        {"name": "math-translation-layer", "depends": ["html-parser"]},
        {"name": "reading-level-glossary", "depends": ["exec-summary"]},
        {"name": "tts-edge", "depends": ["plain-language"]}
      ]
    },
    {
      "name": "assembly",
      "stations": [
        {"name": "html-article", "depends": ["ALL PHASE 2+3"]},
        {"name": "series-flow-auditor", "depends": ["html-article"]}
      ]
    },
    {
      "name": "publish",
      "stations": [
        {"name": "mda-publication", "depends": ["series-flow-auditor"]},
        {"name": "proof-explorer-update", "depends": ["paper-proof-grader"]},
        {"name": "obsidian-export", "depends": ["html-article"]},
        {"name": "postgres-sync", "depends": ["paper-proof-grader"]}
      ]
    }
  ]
}
```

---

## NOTES FOR CODEX

1. This workflow is DRAFT. Station order will change as we test.
2. Some stations can run in parallel (ST_001, ST_002, ST_003 all only need the parsed text).
3. The claim chain (ST_003 -> 004 -> 005 -> 006 -> 007) is strictly sequential.
4. ST_008 (contradiction) should run AFTER vectorization so it can check cross-article.
5. The html-article assembly step is the most complex — it needs outputs from ~8 upstream stations.
6. For MDA: 61 articles across 8 lanes. Run the whole series, not one at a time.
7. The vector store accumulates — each article adds to it, making contradiction checking better.
