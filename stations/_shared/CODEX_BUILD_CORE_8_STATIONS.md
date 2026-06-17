# CODEX BUILD PROMPT: Core 8 NLP Pipeline Stations
# POF 2828 | 2026-06-17
# 
# TASK: Implement sections 06 (NLP_ROUTE) and 07 (PROCESS) in each station's pipeline.py
# Everything else (ingest, validate, artifacts, archive) is already handled by SSS_v1 template.
#
# ARCHITECTURE:
# - Stations call the FastAPI NLP service at http://localhost:8700
# - Models live on NAS, API loads them lazily
# - Each station: one input -> one action -> one JSON artifact in _outbox/
# - Stations chain: ST_001 output feeds ST_002 input, etc.
#
# MODEL REGISTRY: See models/MODEL_REGISTRY.json for folder-to-HuggingFace mapping
# STATION TEMPLATE: See stations/_shared/SSS_TEMPLATE_v1.py for the 13-section structure
# STANDARD: See stations/_shared/SSS_v1_STANDARD.md for architecture rules

---

## PIPELINE FLOW

```
Input Document (.md / .txt / .html)
    |
    v
ST_001 exec-summary -----> executive summary JSON
    |
    v
ST_002 plain-language ----> multi-level rewrites JSON
    |
    v
ST_003 claim-extraction --> all claims extracted JSON
    |
    v
ST_004 claim-classification -> claims classified JSON
    |
    v
ST_005 load-bearing-claims -> structural claims identified JSON
    |
    v
ST_006 falsification ------> kill conditions + evidence bars JSON
    |
    v
ST_007 evidence-map -------> evidence coverage map JSON
    |
    v
ST_008 contradiction-scan -> contradiction report JSON
```

Each station reads from its _inbox/ and writes to its _outbox/.
Workflow orchestrator moves ST_001 _outbox -> ST_002 _inbox, etc.
Every station ALSO accepts the original document alongside upstream artifacts.

---

## SHARED OUTPUT ENVELOPE

Every station artifact wraps its data in this envelope:

```json
{
  "input_file": "MDA-043-Language-Decay.md",
  "station_id": "ST_001",
  "station_name": "exec-summary",
  "nlp_used": "summarizer",
  "api_endpoint": "http://localhost:8700/nlp/summarize",
  "processed_at": "2026-06-17T23:15:00",
  "success": true,
  "errors": [],
  "data": { ... station-specific payload ... }
}
```

---

## ST_001: EXEC-SUMMARY

**Purpose:** Generate a concise executive summary of any document.

**Model:** `summarizer` -> `POST http://localhost:8700/nlp/summarize`
- Primary: facebook/bart-large-cnn (08_SUMMARIZER)
- For long docs (>4K tokens): allenai/led-large-16384-arxiv

**Input:** Any text document (.md, .txt, .html)
- HTML: strip tags first (BeautifulSoup)
- If text > 4096 chars: chunk into sections, summarize each, then summarize summaries

**Processing Logic (Section 07):**
1. Read input text
2. If HTML, strip to plain text
3. Extract document title (first H1 or filename)
4. Call /nlp/summarize with full text (or chunked for long docs)
5. Call /nlp/ner to extract key entities mentioned
6. Count sections, paragraphs, word count for metadata

**Output `data` payload:**
```json
{
  "title": "Language Decay in American Public Discourse",
  "summary": "3-5 sentence executive summary...",
  "key_entities": [
    {"entity": "Flesch-Kincaid", "type": "MISC"},
    {"entity": "GSS", "type": "ORG"}
  ],
  "section_count": 8,
  "word_count": 4250,
  "estimated_reading_time_min": 17,
  "source_format": "markdown"
}
```

---

## ST_002: PLAIN-LANGUAGE

**Purpose:** Rewrite the document at 3 reading levels: Easy (grade 6), Standard (grade 10), Academic (grad school).

**Model:** `M06_llm` -> Ollama (phi4) or OpenAI API
- This is an LLM task, not a HuggingFace model
- Station should support both Ollama (local) and OpenAI (cloud) backends
- Config flag: `llm_backend: "ollama" | "openai"`

**Input:** Original text document + ST_001 summary artifact (for context)

**Processing Logic (Section 07):**
1. Read original document
2. Split into sections (by headings or paragraph blocks)
3. For each section, call LLM with prompt:
   - "Rewrite this at a 6th grade reading level. Keep all facts. Simplify vocabulary."
   - "Rewrite this at a 10th grade reading level. Maintain technical accuracy."
   - Academic version = original text (pass through, maybe light cleanup)
4. Compute Flesch-Kincaid score for each version
5. Assemble all three versions

**Output `data` payload:**
```json
{
  "versions": {
    "easy": {
      "text": "full rewritten text...",
      "reading_level": "grade_6",
      "flesch_kincaid": 65.2,
      "word_count": 3100
    },
    "standard": {
      "text": "full rewritten text...",
      "reading_level": "grade_10",
      "flesch_kincaid": 45.8,
      "word_count": 3800
    },
    "academic": {
      "text": "original or lightly edited...",
      "reading_level": "graduate",
      "flesch_kincaid": 28.1,
      "word_count": 4250
    }
  },
  "section_count": 8
}
```

---

## ST_003: CLAIM-EXTRACTION

**Purpose:** Extract every claim from the document with section context and position.

**Model:** `qa_extractor` -> `POST http://localhost:8700/nlp/qa`
- Primary: deepset/roberta-base-squad2 (18_QA_EXTRACTOR)
- Also uses: zero-shot classifier to tag claim types

**Input:** Original text document

**Processing Logic (Section 07):**
1. Split document into sections (by headings)
2. Split each section into sentences
3. For each sentence, classify: is this a CLAIM or DESCRIPTION?
   - Call /nlp/classify with labels: ["factual claim", "model claim", "opinion", "definition", "narrative", "metadata"]
4. For sentences classified as claims (factual or model), extract:
   - The claim text
   - Section heading it belongs to
   - Position (paragraph index, sentence index)
   - Claim type from classifier
5. Assign claim IDs: {article_id}:claim-{NNN}

**Output `data` payload:**
```json
{
  "claims": [
    {
      "claim_id": "MDA-043:claim-001",
      "text": "Average reading level of public discourse has declined by 3 grade levels since 1960.",
      "section": "The Data",
      "paragraph_index": 4,
      "sentence_index": 2,
      "claim_type": "factual_claim",
      "classifier_score": 0.92
    }
  ],
  "total_claims": 34,
  "claims_by_type": {
    "factual_claim": 18,
    "model_claim": 8,
    "opinion": 5,
    "definition": 3
  }
}
```

---

## ST_004: CLAIM-CLASSIFICATION

**Purpose:** Classify each extracted claim by maturity level and domain.

**Model:** `zero_shot` -> `POST http://localhost:8700/nlp/classify`
- Primary: MoritzLaurer/deberta-v3-large-zeroshot-v2.0 (07_ZERO_SHOT_CLASSIFIER)

**Input:** ST_003 claim-extraction artifact (JSON with claims array)

**Processing Logic (Section 07):**
1. Load claims from upstream artifact
2. For each claim, run zero-shot classification with maturity labels:
   - ["Formal Model", "Structural Correspondence", "Public Proof Claim", "Empirical Support", "Analogy", "Metaphor", "Assertion"]
3. For each claim, also classify domain:
   - ["physics", "theology", "mathematics", "consciousness", "information_theory", "ethics", "empirical_data", "historical"]
4. Assign maturity_label = highest-scoring maturity class
5. Assign domain = highest-scoring domain class

**Output `data` payload:**
```json
{
  "classified_claims": [
    {
      "claim_id": "MDA-043:claim-001",
      "text": "Average reading level...",
      "maturity_label": "Empirical Support",
      "maturity_score": 0.87,
      "domain": "empirical_data",
      "domain_score": 0.94,
      "all_maturity_scores": {"Empirical Support": 0.87, "Assertion": 0.08, ...},
      "all_domain_scores": {"empirical_data": 0.94, "historical": 0.72, ...}
    }
  ],
  "maturity_distribution": {"Formal Model": 3, "Empirical Support": 18, ...},
  "domain_distribution": {"physics": 5, "empirical_data": 18, ...}
}
```

---

## ST_005: LOAD-BEARING-CLAIMS

**Purpose:** Separate structurally load-bearing claims from rhetoric, narrative, and metadata.

**Model:** `zero_shot` + LLM reasoning
- Zero-shot for initial scoring
- LLM (Ollama) for borderline cases that need reasoning

**Input:** ST_004 classified claims artifact

**Processing Logic (Section 07):**
1. Load classified claims
2. Apply triage rules (from claim_inventory.py logic):
   - PAPER_CLAIM_QUEUE: maturity in [Formal Model, Structural Correspondence, Public Proof Claim, Empirical Support] AND contains model terms
   - CITATION_FACT_QUEUE: contains data terms (percent, survey, census, study) or named sources (GSS, Gallup, Pew)
   - REVIEW_QUEUE: borderline — has some evidence markers but unclear
   - PARK: narrative, metadata, author voice, metaphor
3. For REVIEW_QUEUE items, optionally call LLM: "Is this claim structurally load-bearing for the argument, or is it rhetorical decoration?"
4. Score each claim: composite of maturity_score + section_relevance + evidence_presence + kill_condition_presence

**Output `data` payload:**
```json
{
  "load_bearing": [
    {
      "claim_id": "MDA-043:claim-001",
      "text": "Average reading level...",
      "triage_status": "PAPER_CLAIM_QUEUE",
      "triage_score": 7,
      "triage_reason": "maturity=Empirical Support; load-bearing section=The Data; model term present",
      "maturity_label": "Empirical Support",
      "domain": "empirical_data"
    }
  ],
  "citation_facts": [...],
  "review_queue": [...],
  "parked": [...],
  "counts": {
    "PAPER_CLAIM_QUEUE": 12,
    "CITATION_FACT_QUEUE": 8,
    "REVIEW_QUEUE": 5,
    "PARK": 9
  }
}
```

---

## ST_006: FALSIFICATION

**Purpose:** For each load-bearing claim, generate explicit kill conditions and evidence bars.

**Model:** LLM (Ollama/OpenAI) for reasoning + `scifact_verify` for evidence checking
- LLM generates the kill condition
- SciFact pipeline checks if evidence supports/refutes

**Input:** ST_005 load-bearing claims artifact

**Processing Logic (Section 07):**
1. Load load-bearing claims (PAPER_CLAIM_QUEUE only)
2. For each claim, call LLM with prompt:
   "Given this claim: '{claim}'
    1. State one specific observation that would FALSIFY this claim.
    2. State the minimum evidence bar required to SUPPORT this claim.
    3. Rate falsifiability: HIGH (clearly testable), MEDIUM (testable with effort), LOW (unfalsifiable)."
3. Parse LLM response into structured fields
4. Optionally: call /nlp/contradiction with claim vs known evidence passages

**Output `data` payload:**
```json
{
  "falsification_results": [
    {
      "claim_id": "MDA-043:claim-001",
      "text": "Average reading level...",
      "kill_condition": "Finding a Flesch-Kincaid analysis of comparable text samples from 1960-2024 showing stable or increasing reading levels.",
      "evidence_bar": "Longitudinal corpus study of public discourse texts (newspapers, speeches, legislation) with consistent methodology across decades.",
      "falsifiability": "HIGH",
      "has_evidence_in_text": true,
      "evidence_excerpt": "Flesch-Kincaid scores from the GSS corpus show..."
    }
  ],
  "falsifiability_distribution": {"HIGH": 8, "MEDIUM": 3, "LOW": 1}
}
```

---

## ST_007: EVIDENCE-MAP

**Purpose:** Map every claim to its supporting evidence. Identify unsupported claims and evidence gaps.

**Model:** `embeddings_fast` -> `POST http://localhost:8700/nlp/embed`
- Embed claims and evidence passages, compute cosine similarity
- Also: `reranker` -> `POST http://localhost:8700/nlp/rerank` (optional, for precision)

**Input:** ST_006 falsification artifact + original document text

**Processing Logic (Section 07):**
1. Load claims from upstream
2. Split original document into evidence passages (paragraphs that contain data, citations, or results)
3. Embed all claims via /nlp/embed
4. Embed all evidence passages via /nlp/embed
5. For each claim, find top-3 most similar evidence passages (cosine similarity)
6. Threshold: similarity > 0.5 = "supported", 0.3-0.5 = "partial", < 0.3 = "unsupported"
7. Flag claims with NO matching evidence as "EVIDENCE_GAP"

**Output `data` payload:**
```json
{
  "evidence_map": [
    {
      "claim_id": "MDA-043:claim-001",
      "text": "Average reading level...",
      "evidence_matches": [
        {
          "passage": "GSS corpus analysis shows Flesch-Kincaid scores dropping from 62.1 to 43.7...",
          "similarity": 0.87,
          "paragraph_index": 12,
          "status": "SUPPORTED"
        }
      ],
      "coverage_status": "SUPPORTED",
      "best_similarity": 0.87
    }
  ],
  "coverage_summary": {
    "SUPPORTED": 10,
    "PARTIAL": 2,
    "UNSUPPORTED": 0,
    "EVIDENCE_GAP": 0
  },
  "orphan_evidence": [
    {
      "passage": "Barna Group 2019 survey found...",
      "paragraph_index": 15,
      "nearest_claim": "MDA-043:claim-008",
      "similarity": 0.31
    }
  ]
}
```

---

## ST_008: CONTRADICTION-SCAN

**Purpose:** Scan for internal contradictions between claims within and across articles.

**Model:** `contradiction_primary` -> `POST http://localhost:8700/nlp/contradiction`
- Primary: MoritzLaurer/DeBERTa-v3-large (deep)
- Fast prefilter: cross-encoder/nli-MiniLM2 (quick screen)
- Long pairs: tasksource/deberta-base-long-nli

**Input:** All claims from ST_005 (load-bearing) + optionally claims from other articles in the series

**Processing Logic (Section 07):**
1. Load all claims
2. Generate all unique pairs (N*(N-1)/2)
3. FAST PASS: Run each pair through contradiction_fast
   - If contradiction score > 0.3, flag for deep pass
   - If entailment score > 0.8, skip (consistent)
4. DEEP PASS: Run flagged pairs through contradiction_primary
   - Record: contradiction / entailment / neutral scores
5. For pairs with contradiction > 0.6: mark as CONTRADICTION
6. For pairs with contradiction 0.3-0.6: mark as TENSION
7. Cross-article mode: if vector store has other articles, query for similar claims and check those pairs too

**Output `data` payload:**
```json
{
  "contradictions": [
    {
      "claim_a": {"id": "MDA-043:claim-005", "text": "Church attendance..."},
      "claim_b": {"id": "MDA-043:claim-019", "text": "Religious participation..."},
      "label": "CONTRADICTION",
      "scores": {"contradiction": 0.82, "entailment": 0.05, "neutral": 0.13},
      "model": "contradiction_primary",
      "severity": "HIGH"
    }
  ],
  "tensions": [...],
  "pairs_checked": 561,
  "pairs_flagged_fast": 23,
  "contradictions_found": 2,
  "tensions_found": 5,
  "cross_article_checked": false
}
```

---

## ADDITIONAL STATIONS TO CONSIDER (Future)

These capabilities have models downloaded but no station yet:

| Capability | Model Ready | Station Needed |
|---|---|---|
| Sentiment analysis | 10_SENTIMENT | sentiment-analyzer.station |
| General NER | 06_NER_GENERAL | entity-extractor.station |
| Enhanced NER (open-type) | 16_NER_ENHANCED | entity-extractor-enhanced.station |
| Reranking | 09_RERANKER | Built into ST_007 evidence-map |
| Image captioning | 13_IMAGE_CAPTION | image-describer.station |
| Deduplication | 17_DEDUP concept | dedup.station |
| Text chunking | N/A | Already: section-splitter.station |

---

## HOW TO IMPLEMENT

For each station, Codex needs to:

1. Open `stations/{name}.station/pipeline.py`
2. Find Section 06 (NLP_ROUTE) and Section 07 (PROCESS)
3. Replace the placeholder code with the logic described above
4. The station calls `http://localhost:8700/nlp/{endpoint}` via `requests.post()`
5. Parse the JSON response
6. Build the `result["data"]` dict as specified above
7. Return the result dict — Section 08 handles writing it to _outbox/

Example API call pattern:
```python
import requests

def call_nlp(endpoint, payload):
    """Call the shared NLP API."""
    resp = requests.post(f"http://localhost:8700/nlp/{endpoint}", json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()

# In Section 07:
summary = call_nlp("summarize", {"text": document_text})
entities = call_nlp("ner", {"text": document_text})
```

## TESTING

After implementation, each station can be tested standalone:
1. Drop a test document in `stations/{name}.station/_inbox/`
2. Run `python pipeline.py`
3. Check `_outbox/` for the JSON artifact
4. Verify the `data` payload matches the schema above
