# CODEX FOLLOW-UP: Fix Gaps in ST_001-008 Implementation
# POF 2828 | 2026-06-17
#
# CONTEXT: You implemented sections 06+07 for all 8 core stations. 
# The processing logic is correct. These are the gaps that need fixing.
# Reference: CODEX_BUILD_CORE_8_STATIONS.md for the original spec.

---

## PRIORITY 1: BUGS THAT WILL BREAK AT RUNTIME

### Bug 1: ST_008 contradiction-scan parameter mismatch
**File:** `stations/contradiction-scan.station/pipeline.py`
**Problem:** Calls `_api("contradiction", {"text_a":..., "text_b":...})` 
**Fix:** The FastAPI endpoint at `/nlp/contradiction` expects `{"premise":..., "hypothesis":...}`
Change `text_a` → `premise` and `text_b` → `hypothesis` in the API call.

### Bug 2: ST_003 claim-extraction is O(n) API calls per sentence
**File:** `stations/claim-extraction.station/pipeline.py`
**Problem:** Every sentence gets its own `/nlp/classify` API call. A 4000-word article = ~200 calls = very slow.
**Fix:** Batch sentences. Collect all sentences first, then classify in batches of 20-50.
Or: add a simple prefilter — skip sentences under 8 words, skip sentences that start with common non-claim patterns ("In this section", "Next we", "For example").

---

## PRIORITY 2: EXTRACT SHARED HELPERS TO MODULE

### Problem
The helper functions `_api()`, `_read_input()`, `_text_from_input()`, `_strip_html()`, `_sentences()`, `_paragraphs()`, `_sections()`, `_score_map()`, `_top_label()`, `_word_count()`, `_cosine()`, `_embeddings()`, `_base_result()` are copy-pasted identically in all 8 pipeline.py files.

### Fix
Create `stations/_shared/station_helpers.py` with ALL shared functions.
Each pipeline.py imports: `from _shared.station_helpers import *` (or specific names).

The _shared folder already exists. Create the module there.

Also create `stations/_shared/__init__.py` (empty) so Python treats it as a package.

After extraction, each station's pipeline.py should only contain:
- Section 01: Station identity (ID, name, desc) 
- Section 06: choose_nlp() 
- Section 07: process_one()
- Everything else: imported from shared

---

## PRIORITY 3: UPDATE CONFIG FILES

Each station's `config.json` needs these additions:

```json
{
  "station_id": "ST_001",
  "station_name": "exec-summary",
  "station_type": "one_for_one",
  "description": "Generate executive summary of a paper or article",
  "input_extensions": [".md", ".txt", ".json", ".html"],
  "workers": {
    "default": ["summarizer"],
    "optional": ["bart_summarizer"]
  },
  "nlp_id": "summarizer",
  "model_folder": "08_SUMMARIZER",
  "api_base": "http://localhost:8700/nlp",
  "api_timeout": 120,
  "chunk_chars": 4096,
  "outputs": {
    "artifact_type": "json",
    "update_job_card": true,
    "final_export": false
  },
  "upstream": [],
  "downstream": ["ST_002", "ST_003"]
}
```

Do this for all 8 stations. The key additions:
- `nlp_id`: which model key
- `model_folder`: which folder in 05_MODELS
- `api_base`: FastAPI URL
- `api_timeout`: seconds
- `upstream`/`downstream`: which stations feed in/out
- Any station-specific settings (chunk_chars, batch_size, label lists, etc.)

Station wiring:
- ST_001: upstream=[], downstream=[ST_002]
- ST_002: upstream=[ST_001], downstream=[]
- ST_003: upstream=[], downstream=[ST_004]
- ST_004: upstream=[ST_003], downstream=[ST_005]
- ST_005: upstream=[ST_004], downstream=[ST_006]
- ST_006: upstream=[ST_005], downstream=[ST_007]
- ST_007: upstream=[ST_006], downstream=[ST_008]
- ST_008: upstream=[ST_005], downstream=[]

---

## PRIORITY 4: CREATE WIRING_SPEC.JSON

Each station needs `wiring_spec.json` that defines input/output contract:

```json
{
  "station_id": "ST_003",
  "station_name": "claim-extraction",
  "input": {
    "accepts": [".md", ".txt", ".html", ".json"],
    "expects_upstream": null,
    "description": "Raw document text"
  },
  "output": {
    "artifact_type": "json",
    "key_fields": ["claims", "total_claims", "claims_by_type"],
    "description": "Array of extracted claims with positions"
  },
  "api_calls": [
    {"endpoint": "/nlp/classify", "purpose": "Classify each sentence as claim type"}
  ],
  "upstream_stations": [],
  "downstream_stations": ["ST_004"]
}
```

Create this for all 8 stations.

---

## PRIORITY 5: WRITE README.md FOR EACH STATION

Each station's README.md should document:
1. What it does (one paragraph)
2. Which model it uses (with HuggingFace ID)
3. Input format
4. Output format (key fields in the data payload)
5. Pipeline position (what feeds it, what it feeds)
6. How to test standalone

---

## PRIORITY 6: ADD GLOSSARY EXTRACTION TO ST_002

**File:** `stations/plain-language.station/pipeline.py`

ST_002 should also output a `glossary_candidates` array:
1. After generating the Easy version, scan the original text for terms above 8th grade reading level
2. Use syllable counting + word frequency heuristic (3+ syllables or not in top-5000 common English words = above grade 8)
3. For each flagged term, include:
   - `term`: the word/phrase
   - `grade_level`: estimated
   - `easy_replacement`: what the Easy version used instead
   - `first_occurrence`: paragraph + sentence index
   - `frequency_in_article`: how many times it appears

Add this to the `result["data"]` dict alongside `versions`.

---

## PRIORITY 7: CREATE WORKFLOW JOB CARD SYSTEM

Create `stations/_shared/job_card.py` with:

```python
class JobCard:
    """Tracks a document through the pipeline."""
    
    def __init__(self, doc_id, doc_path, workflow_name="article-production"):
        self.doc_id = doc_id
        self.doc_path = doc_path  
        self.workflow = workflow_name
        self.created_at = datetime.now().isoformat()
        self.stations_completed = []
        self.stations_failed = []
        self.current_station = None
        self.status = "IN_PROGRESS"
    
    def check_in(self, station_id, station_name):
        """Called when a station starts processing this doc."""
        self.current_station = {"id": station_id, "name": station_name, 
                                "started": datetime.now().isoformat()}
    
    def check_out(self, station_id, success, artifact_path=None, error=None):
        """Called when a station finishes processing this doc."""
        entry = {
            "id": station_id,
            "completed": datetime.now().isoformat(),
            "success": success,
            "artifact": str(artifact_path) if artifact_path else None,
            "error": error
        }
        if success:
            self.stations_completed.append(entry)
        else:
            self.stations_failed.append(entry)
        self.current_station = None
    
    def save(self, job_cards_dir):
        """Write job card to disk."""
        path = Path(job_cards_dir) / f"JOB_{self.doc_id}.json"
        path.write_text(json.dumps(self.__dict__, indent=2, default=str))
        return path
    
    @classmethod
    def load(cls, path):
        """Load existing job card."""
        data = json.loads(Path(path).read_text())
        card = cls(data["doc_id"], data["doc_path"], data["workflow"])
        card.__dict__.update(data)
        return card
```

Then update Section 09 (WORKFLOW) in the shared template to use this:
```python
def update_workflow(result, artifact_path, cfg, log):
    job_cards_dir = HERE.parent / "_shared" / "job_cards"
    job_cards_dir.mkdir(exist_ok=True)
    doc_id = Path(result["input_file"]).stem
    card_path = job_cards_dir / f"JOB_{doc_id}.json"
    if card_path.exists():
        card = JobCard.load(card_path)
    else:
        card = JobCard(doc_id, result["input_file"])
    card.check_out(STATION_ID, result["success"], artifact_path,
                   result["errors"][0] if result["errors"] else None)
    card.save(job_cards_dir)
    log.info("Job card updated: %s", card_path)
```

---

## PRIORITY 8: PROMPT FILES FOR LLM STATIONS

Create `prompt.md` in these stations:

**stations/plain-language.station/prompt.md:**
```
You are rewriting a Theophysics research article for a general audience.

TASK: Rewrite the following section at a {grade_level} reading level.
- Keep ALL facts, numbers, and claims
- Replace technical terms with simpler words or brief explanations
- Use short sentences (under 20 words when possible)
- Use analogies from everyday life
- Do NOT add new claims or opinions
- Do NOT remove any data points or statistics

SECTION:
{section_text}
```

**stations/falsification.station/prompt.md:**
```
You are a rigorous scientific reviewer.

TASK: For the following claim, provide:
1. KILL CONDITION: One specific observation that would FALSIFY this claim.
2. EVIDENCE BAR: The minimum evidence required to SUPPORT this claim.
3. FALSIFIABILITY RATING: HIGH (clearly testable), MEDIUM (testable with effort), LOW (unfalsifiable).

Format your response as:
KILL: [one sentence]
EVIDENCE: [one sentence]
RATING: [HIGH/MEDIUM/LOW]

CLAIM:
{claim_text}
```

**stations/load-bearing-claims.station/prompt.md:**
```
You are analyzing a research paper's claims.

TASK: Is this claim structurally load-bearing for the paper's argument, 
or is it rhetorical decoration (narrative, metaphor, aside)?

Answer LOAD_BEARING or RHETORIC with a one-sentence reason.

CLAIM: {claim_text}
SECTION: {section_heading}
```

---

## SUMMARY

| Priority | Task | Files Changed |
|----------|------|---------------|
| P1 | Fix ST_008 param names | 1 file |
| P1 | Fix ST_003 batching | 1 file |
| P2 | Extract shared helpers | Create 1 new file, update 8 |
| P3 | Update config.json | 8 files |
| P4 | Create wiring_spec.json | 8 new files |
| P5 | Update README.md | 8 files |
| P6 | Add glossary to ST_002 | 1 file |
| P7 | Create job card system | 1 new file, update 8 |
| P8 | Create prompt.md | 3 new files |

Total: ~40 file operations. All mechanical, all following the patterns already established.
