# CODEX TASK: Wire All NONE Stations
**POF 2828 | 2026-06-17**

## What You Are Doing

36 stations in `D:\GitHub\BACKSIDE-NLP-NEW\stations\` have `"workers": {"default": ["NONE"]}` in their `config.json`. Their `pipeline.py` files exist and are syntactically valid but sections `06_NLP_ROUTE` and `07_PROCESS` contain only the template header comment — no real logic. You are going to wire every one of them.

For each station you must do **two things**:
1. Edit `config.json` → change `"workers": {"default": ["NONE"]}` to the correct model key
2. Edit `pipeline.py` → replace sections `06_NLP_ROUTE` and `07_PROCESS` with real logic

Do NOT touch sections 00–05 or 08–12. Those are standardized and identical across all stations.

---

## Architecture Reference

**NLP API** runs at `http://localhost:8700`. Stations call it via `call_nlp()` from shared helpers.

**Available endpoints:**
| Endpoint | Payload keys | Returns |
|---|---|---|
| `contradiction` | `text_a`, `text_b`, `model` (optional) | `scores: {contradiction, entailment, neutral}` |
| `classify` | `text`, `labels: [...]`, `model` (optional) | `labels: [{label, score}]` |
| `embed` | `texts: [...]`, `model` (optional) | `embeddings: [[...]]` |
| `summarize` | `text`, `model` (optional) | `summary` |
| `ner` | `text`, `model` (optional) | `entities: [{text, label, score}]` |
| `sentiment` | `text` | `label`, `score` |
| `qa` | `question`, `context` | `answer`, `score` |

**Available model keys** (use these in `config.json` `workers.default` and in `call_nlp()` calls):
- `contradiction_primary` — DeBERTa NLI, best accuracy
- `contradiction_fast` — MiniLM NLI, fast
- `contradiction_tiny` — DistilBERT NLI, very fast
- `long_nli` — DeBERTa long context NLI
- `embeddings_fast` — all-MiniLM-L6-v2 sentence embeddings
- `zero_shot` — DeBERTa zero-shot classifier
- `summarizer` — BART-large-cnn
- `ner_general` — BERT NER
- `ner_enhanced` — GLiNER multi
- `qa_extractor` — RoBERTa SQuAD2 extractive QA
- `reranker` — BGE reranker
- `sentiment` — Twitter RoBERTa sentiment
- `M06_llm` — Ollama phi4 (local LLM, call via Ollama API at `http://localhost:11434`)
- `M11_math_verify` — math verification (custom)

**Shared helpers** — import at the top of section 06 exactly like this:
```python
import re, sys
sys.path.insert(0, str(STATIONS))
from _shared.station_helpers import (
    API_BASE, base_result, call_nlp, cosine, data_from_artifact,
    embeddings, flesch_reading_ease, nlp_route, paragraphs,
    read_input, sections, sentences, strip_html, text_from_input,
    top_label, word_count,
)
```

**LLM calls** (for M06_llm stations) use Ollama directly:
```python
import requests as _req
def _llm(prompt: str) -> str:
    r = _req.post("http://localhost:11434/api/generate",
                  json={"model": "phi4", "prompt": prompt, "stream": False}, timeout=120)
    return r.json().get("response", "")
```

**Pattern for `choose_nlp`** (section 06):
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "MODEL_KEY_HERE", "ENDPOINT_HERE")
```

**Pattern for `process_one`** (section 07):
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        text = text_from_input(obj)
        # ... do the work ...
        result["data"] = { ... }
    except Exception as exc:
        result["success"] = False
        result["errors"].append(str(exc))
    return result
```

---

## Reference Example (Already Working)

`contradiction-scan.station` — study this pattern before writing any others:

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "contradiction_primary", "contradiction")
```

**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path); data = obj.get("data", obj)
        claims = data.get("load_bearing") or data.get("classified_claims") or data.get("claims") or []
        contradictions = []; tensions = []; checked = 0
        for i in range(len(claims)):
            for j in range(i+1, len(claims)):
                checked += 1
                res = call_nlp("contradiction", {"text_a": claims[i].get("text",""), "text_b": claims[j].get("text","")})
                scores = res.get("scores", {})
                con = float(scores.get("contradiction", 0))
                item = {"claim_a": claims[i], "claim_b": claims[j], "scores": scores}
                if con > 0.6: contradictions.append({**item, "label": "CONTRADICTION"})
                elif con >= 0.3: tensions.append({**item, "label": "TENSION"})
        result["data"] = {"contradictions": contradictions, "tensions": tensions, "pairs_checked": checked}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

## Station-by-Station Wiring Instructions

Work through each station in the order listed. For each: (a) update `config.json`, (b) write sections 06+07 in `pipeline.py`.

---

### 1. `7q-classifier.station` (ST_001)
**config.json** → `"workers": {"default": ["zero_shot"]}`
**Job:** Classify input text against the 7 Questions framework (Who, What, When, Where, Why, How, So What).

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")
```
**Section 07:**
```python
SEVEN_Q = ["Who is involved", "What is the claim or event", "When did this occur",
           "Where did this happen", "Why does this matter", "How was this determined",
           "So what is the implication"]

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        res = call_nlp("classify", {"text": text[:2000], "labels": SEVEN_Q})
        labels = res.get("labels", [])
        result["data"] = {"seven_q_scores": labels, "top_question": labels[0]["label"] if labels else "", "text_preview": text[:200]}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 2. `7q-engine.station` (ST_002)
**config.json** → `"workers": {"default": ["zero_shot"]}`
**Job:** Run each input through ALL 7 questions, returning a structured answer for each.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")
```
**Section 07:**
```python
SEVEN_Q_PROMPTS = {
    "who":    "Extract who is involved: {text}",
    "what":   "Extract what the main claim or event is: {text}",
    "when":   "Extract when this occurred: {text}",
    "where":  "Extract where this happened: {text}",
    "why":    "Extract why this matters: {text}",
    "how":    "Extract how this was determined: {text}",
    "so_what":"Extract the main implication: {text}",
}

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path); text = text_from_input(obj)
        answers = {}
        for key, prompt in SEVEN_Q_PROMPTS.items():
            res = call_nlp("qa", {"question": prompt.split(":")[0], "context": text[:3000]})
            answers[key] = res.get("answer", "")
        result["data"] = {"seven_q_answers": answers, "source_length": len(text)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 3. `ai-portal-generator.station` (ST_003) — TERMINAL
**config.json** → `"workers": {"default": ["M06_llm"]}`, set `"outputs": {"final_export": true, "artifact_type": "html"}`
**Job:** Generate an HTML research portal page from article metadata and summaries.

**Section 06:**
```python
import requests as _req
def _llm(prompt):
    r = _req.post("http://localhost:11434/api/generate",
                  json={"model":"phi4","prompt":prompt,"stream":False},timeout=120)
    return r.json().get("response","")

def choose_nlp(path, cfg):
    return {"model": "M06_llm", "endpoint": "llm", "api_base": "http://localhost:11434"}
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path); data = obj.get("data", obj) if isinstance(obj, dict) else {}
        title = data.get("title", path.stem)
        summary = data.get("summary", text_from_input(obj)[:1000])
        prompt = f"Write a clean HTML research portal page for this article.\nTitle: {title}\nSummary: {summary}\nReturn only valid HTML, no markdown fences."
        html = _llm(prompt)
        export_path = EXPORTS / f"{path.stem}_portal.html"
        export_path.write_text(html, encoding="utf-8")
        result["data"] = {"portal_html_path": str(export_path), "title": title, "char_count": len(html)}
        log.info("Portal exported -> %s", export_path)
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 4. `ai-research-agents.station` (ST_004)
**config.json** → `"workers": {"default": ["embeddings_fast"]}`
**Job:** Embed input documents and return a semantic profile for downstream research routing.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        chunks = [text[i:i+500] for i in range(0, min(len(text),3000), 500)]
        res = call_nlp("embed", {"texts": chunks})
        vecs = res.get("embeddings", [])
        ner_res = call_nlp("ner", {"text": text[:2000]})
        entities = ner_res.get("entities", [])
        result["data"] = {"embedding_count": len(vecs), "mean_vector": [sum(v[i] for v in vecs)/len(vecs) for i in range(len(vecs[0]))] if vecs else [], "entities": entities[:20], "source_length": len(text)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 5. `apologetic-pipeline.station` (ST_005)
**config.json** → `"workers": {"default": ["contradiction_primary"]}`
**Job:** Analyze theological apologetics text — detect argument structure, identify premises, check internal consistency.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "contradiction_primary", "contradiction")
```
**Section 07:**
```python
APOLOGETIC_LABELS = ["theological claim", "philosophical premise", "scriptural reference",
                     "logical argument", "counter-argument", "conclusion", "evidence"]

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        sent_list = sentences(text)[:40]
        classified = []
        for s in sent_list:
            res = call_nlp("classify", {"text": s, "labels": APOLOGETIC_LABELS})
            top = res.get("labels", [{}])[0]
            classified.append({"sentence": s, "type": top.get("label",""), "confidence": top.get("score",0)})
        premises = [c for c in classified if c["type"] in ("theological claim","philosophical premise","scriptural reference")]
        tensions = []
        for i in range(len(premises)):
            for j in range(i+1, len(premises)):
                res = call_nlp("contradiction", {"text_a": premises[i]["sentence"], "text_b": premises[j]["sentence"]})
                con = float(res.get("scores",{}).get("contradiction",0))
                if con > 0.4:
                    tensions.append({"a": premises[i]["sentence"], "b": premises[j]["sentence"], "contradiction_score": con})
        result["data"] = {"classified_sentences": classified, "premises_found": len(premises), "tensions": tensions}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 6. `axioms.station` (ST_006)
**config.json** → `"workers": {"default": ["qa_extractor"]}`
**Job:** Extract axioms (foundational premises) from theological or philosophical text.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "qa_extractor", "qa")
```
**Section 07:**
```python
AXIOM_QUESTIONS = [
    "What is the fundamental premise of this text?",
    "What assumptions does this argument rely on?",
    "What is stated as self-evidently true?",
    "What foundational claim underlies this reasoning?",
]

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        context = text[:4000]
        axioms = []
        for q in AXIOM_QUESTIONS:
            res = call_nlp("qa", {"question": q, "context": context})
            answer = res.get("answer","").strip()
            score = float(res.get("score", 0))
            if answer and score > 0.1 and answer not in [a["text"] for a in axioms]:
                axioms.append({"text": answer, "question": q, "confidence": score})
        result["data"] = {"axioms": axioms, "axiom_count": len(axioms), "source_length": len(text)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 7. `brain-map.station` (ST_007)
**config.json** → `"workers": {"default": ["embeddings_fast"]}`
**Job:** Build a semantic brain map — embed all sections, compute cosine similarity edges for a knowledge graph.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        sec_list = sections(text) or [{"heading":"Document","text":text}]
        texts = [s["text"][:500] for s in sec_list if s.get("text")]
        res = call_nlp("embed", {"texts": texts})
        vecs = res.get("embeddings", [])
        edges = []
        for i in range(len(vecs)):
            for j in range(i+1, len(vecs)):
                sim = cosine(vecs[i], vecs[j])
                if sim > 0.4:
                    edges.append({"source": sec_list[i].get("heading",""), "target": sec_list[j].get("heading",""), "weight": round(sim,4)})
        result["data"] = {"nodes": [{"id": s.get("heading",""), "text_preview": s.get("text","")[:100]} for s in sec_list], "edges": edges, "node_count": len(sec_list), "edge_count": len(edges)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 8. `classify-documents.station` (ST_009)
**config.json** → `"workers": {"default": ["zero_shot"]}`
**Job:** Classify documents into the passport schema categories.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")
```
**Section 07:**
```python
PASSPORT_LABELS = ["theological paper", "philosophical essay", "scientific article",
                   "apologetics", "commentary", "sermon transcript", "devotional",
                   "news article", "academic journal", "book chapter", "other"]

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        res = call_nlp("classify", {"text": text[:2000], "labels": PASSPORT_LABELS})
        labels = res.get("labels", [])
        top = labels[0] if labels else {}
        result["data"] = {"document_type": top.get("label",""), "confidence": top.get("score",0), "all_scores": labels, "passport_ready": top.get("score",0) > 0.5}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 9. `coherence-discoherence.station` (ST_010)
**config.json** → `"workers": {"default": ["contradiction_primary"]}`
**Job:** Measure coherence across paragraphs — flag sections that contradict or drift semantically.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "contradiction_primary", "contradiction")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        para_list = paragraphs(text)[:20]
        coherence_pairs = []; incoherent = []
        for i in range(len(para_list)-1):
            res = call_nlp("contradiction", {"text_a": para_list[i][:500], "text_b": para_list[i+1][:500]})
            scores = res.get("scores", {})
            con = float(scores.get("contradiction", 0))
            ent = float(scores.get("entailment", 0))
            coherence_pairs.append({"para_index": i, "contradiction": con, "entailment": ent, "coherent": con < 0.3})
            if con > 0.5:
                incoherent.append({"para_a": para_list[i][:200], "para_b": para_list[i+1][:200], "contradiction_score": con})
        avg_coherence = sum(1 - p["contradiction"] for p in coherence_pairs) / len(coherence_pairs) if coherence_pairs else 1.0
        result["data"] = {"coherence_score": round(avg_coherence, 3), "incoherent_transitions": incoherent, "paragraphs_checked": len(coherence_pairs)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 10. `file-intelligence.station` (ST_015)
**config.json** → `"workers": {"default": ["zero_shot"]}`
**Job:** Classify, summarize, tag, and suggest rename for a file based on its content.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")
```
**Section 07:**
```python
FILE_TYPE_LABELS = ["research paper", "sermon notes", "book draft", "correspondence",
                    "spreadsheet data", "technical documentation", "theological essay",
                    "meeting notes", "media transcript", "reference material"]

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        cls_res = call_nlp("classify", {"text": text[:2000], "labels": FILE_TYPE_LABELS})
        sum_res = call_nlp("summarize", {"text": text[:3000]})
        ner_res = call_nlp("ner", {"text": text[:2000]})
        top_type = (cls_res.get("labels",[{}])[0]).get("label","unknown")
        summary = sum_res.get("summary","")
        entities = [e["text"] for e in ner_res.get("entities",[])[:5]]
        slug = re.sub(r"[^a-z0-9]+","-", top_type.lower()).strip("-")
        rename_suggestion = f"{slug}_{path.stem[:30]}{path.suffix}"
        result["data"] = {"file_type": top_type, "summary": summary, "key_entities": entities, "rename_suggestion": rename_suggestion, "word_count": word_count(text)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 11. `fis.station` (ST-FIS-001)
**config.json** → `"workers": {"default": ["zero_shot"]}`
**Job:** File Intelligence System — classify, summarize, tag, generate rename preview, produce `.fcard` manifest.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")
```
**Section 07:** (same logic as file-intelligence but outputs `.fcard` manifest YAML)
```python
FIS_LABELS = ["theological", "scientific", "philosophical", "administrative",
              "media", "technical", "personal", "reference", "draft", "archive"]

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        cls_res = call_nlp("classify", {"text": text[:2000], "labels": FIS_LABELS})
        sum_res = call_nlp("summarize", {"text": text[:3000]})
        ner_res = call_nlp("ner", {"text": text[:2000]})
        top = (cls_res.get("labels",[{}])[0])
        fcard = {"filename": path.name, "category": top.get("label",""), "confidence": top.get("score",0),
                 "summary": sum_res.get("summary",""), "tags": [e["text"] for e in ner_res.get("entities",[])[:8]],
                 "word_count": word_count(text), "rename_preview": re.sub(r"[^a-z0-9]+","-", top.get("label","file").lower())+f"_{path.stem[:20]}{path.suffix}"}
        result["data"] = {"fcard": fcard}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 12. `fruits-spirit-canon.station` (fruits-spirit-canon)
**config.json** → `"workers": {"default": ["zero_shot"]}`
**Job:** Analyze text for presence/expression of the Fruits of the Spirit (Galatians 5:22-23).

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")
```
**Section 07:**
```python
FRUITS = ["love", "joy", "peace", "patience", "kindness", "goodness",
          "faithfulness", "gentleness", "self-control"]

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        para_list = paragraphs(text)[:15]
        fruit_map = {f: [] for f in FRUITS}
        for para in para_list:
            if len(para.strip()) < 20: continue
            res = call_nlp("classify", {"text": para[:500], "labels": FRUITS})
            for item in res.get("labels",[]):
                if item.get("score",0) > 0.3:
                    fruit_map[item["label"]].append({"text": para[:150], "score": item["score"]})
        present = {f: v for f,v in fruit_map.items() if v}
        result["data"] = {"fruits_present": present, "fruit_count": len(present), "dominant_fruit": max(present, key=lambda f: max(x["score"] for x in present[f])) if present else ""}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 13. `graph-linker.station` (ST-HTML-GRAPH-001)
**config.json** → `"workers": {"default": ["embeddings_fast"]}`
**Job:** Generate weighted graph edges from section vectors, claims, and tags via cosine similarity.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        nodes = data.get("sections") or data.get("claims") or []
        texts = [n.get("text", n.get("heading","")) for n in nodes if n.get("text") or n.get("heading")]
        if not texts:
            text = text_from_input(obj)
            sec_list = sections(text)
            texts = [s["text"][:400] for s in sec_list]
            nodes = sec_list
        res = call_nlp("embed", {"texts": [t[:500] for t in texts]})
        vecs = res.get("embeddings",[])
        edges = []
        for i in range(len(vecs)):
            for j in range(i+1, len(vecs)):
                sim = cosine(vecs[i], vecs[j])
                if sim > 0.35:
                    edges.append({"source_idx": i, "target_idx": j, "source_label": nodes[i].get("heading", str(i)), "target_label": nodes[j].get("heading", str(j)), "weight": round(sim, 4)})
        edges.sort(key=lambda e: e["weight"], reverse=True)
        result["data"] = {"nodes": nodes, "edges": edges[:100], "edge_count": len(edges)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 14. `harvest-links.station` (ST_019)
**config.json** → `"workers": {"default": ["ner_general"]}`
**Job:** Extract all URLs and named entity references from text, enrich with NER context.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "ner_general", "ner")
```
**Section 07:**
```python
URL_RE = re.compile(r"https?://[^\s\"'<>\]]+")

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        urls = list(dict.fromkeys(URL_RE.findall(text)))
        ner_res = call_nlp("ner", {"text": text[:4000]})
        entities = ner_res.get("entities", [])
        result["data"] = {"urls": urls, "url_count": len(urls), "entities": entities, "entity_count": len(entities)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 15. `hdbscan-cluster.station` (ST_020)
**config.json** → `"workers": {"default": ["embeddings_fast"]}`
**Job:** Embed all input chunks and cluster them semantically (prepare vectors for HDBSCAN downstream).

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        para_list = paragraphs(text)[:50]
        chunks = [p[:500] for p in para_list if len(p) > 30]
        res = call_nlp("embed", {"texts": chunks})
        vecs = res.get("embeddings", [])
        result["data"] = {"chunks": chunks, "embeddings": vecs, "chunk_count": len(chunks), "vector_dim": len(vecs[0]) if vecs else 0, "ready_for_hdbscan": True}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 16. `html-article.station` (ST_021)
**config.json** → `"workers": {"default": ["summarizer"]}`
**Job:** Process an HTML article — strip HTML, split sections, summarize, extract metadata.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        raw = read_input(path)
        if isinstance(raw, str):
            text = strip_html(raw)
        else:
            text = text_from_input(raw)
        sec_list = sections(text)
        summaries = []
        for s in sec_list[:10]:
            if len(s.get("text","")) > 100:
                res = call_nlp("summarize", {"text": s["text"][:3000]})
                summaries.append({"heading": s.get("heading",""), "summary": res.get("summary","")})
        full_res = call_nlp("summarize", {"text": text[:5000]})
        result["data"] = {"section_summaries": summaries, "article_summary": full_res.get("summary",""), "section_count": len(sec_list), "word_count": word_count(text)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 17. `link-pull.station` (ST_024)
**config.json** → `"workers": {"default": ["ner_general"]}`
**Job:** Pull all hyperlinks from HTML/text, classify link type, extract anchor text context.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "ner_general", "ner")
```
**Section 07:**
```python
HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.I)
ANCHOR_RE = re.compile(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>', re.I)

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        raw = read_input(path) if path.suffix.lower() in (".html",".htm") else text_from_input(read_input(path))
        if isinstance(raw, str):
            anchors = [{"url": m[0], "anchor_text": m[1].strip()} for m in ANCHOR_RE.findall(raw)]
            plain_urls = [u for u in HREF_RE.findall(raw) if u not in [a["url"] for a in anchors]]
        else:
            anchors = []; plain_urls = []
        result["data"] = {"anchors": anchors, "plain_urls": plain_urls, "total_links": len(anchors)+len(plain_urls)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 18. `link-research.station` (ST_025)
**config.json** → `"workers": {"default": ["embeddings_fast"]}`
**Job:** Take a list of URLs/links and produce an embedded semantic index for research routing.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        links = data.get("anchors", data.get("urls", data.get("plain_urls", [])))
        texts = [l.get("anchor_text","") or l if isinstance(l,str) else str(l) for l in links[:50]]
        texts = [t for t in texts if len(t) > 3]
        res = call_nlp("embed", {"texts": texts}) if texts else {"embeddings": []}
        vecs = res.get("embeddings", [])
        result["data"] = {"link_count": len(links), "embedded_count": len(vecs), "link_index": [{"text": texts[i], "vector_idx": i} for i in range(len(texts))]}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 19. `master-equation-canon.station` (master-equation-canon)
**config.json** → `"workers": {"default": ["qa_extractor"]}`
**Job:** Extract and structure master equations from theophysics text — identify variables, operators, and their relationships.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "qa_extractor", "qa")
```
**Section 07:**
```python
EQ_QUESTIONS = [
    "What is the master equation described in this text?",
    "What variables does the equation use?",
    "What operators or transformations are defined?",
    "What is the equation's domain of application?",
]

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        context = text[:4000]
        equations = []
        for q in EQ_QUESTIONS:
            res = call_nlp("qa", {"question": q, "context": context})
            answer = res.get("answer","").strip()
            if answer and res.get("score",0) > 0.1:
                equations.append({"question": q, "answer": answer, "score": res.get("score",0)})
        math_re = re.compile(r"[A-Z][a-z]?\s*[=\+\-\*/]\s*[A-Z\d\(]")
        raw_eqs = math_re.findall(text)
        result["data"] = {"extracted_answers": equations, "raw_equation_patterns": raw_eqs[:20], "source_length": len(text)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 20. `mda-citation-spine.station` (ST_031)
**config.json** → `"workers": {"default": ["qa_extractor"]}`
**Job:** Extract citation spine from MDA articles — pull all cited authors, titles, years, claim context.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "qa_extractor", "qa")
```
**Section 07:**
```python
CITE_QUESTIONS = [
    "Who are the authors cited in this text?",
    "What works are referenced in this text?",
    "What publication years are mentioned?",
    "What claims are supported by citations?",
]

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        ner_res = call_nlp("ner", {"text": text[:4000]})
        entities = ner_res.get("entities", [])
        persons = [e["text"] for e in entities if e.get("label","") in ("PER","PERSON")]
        orgs = [e["text"] for e in entities if e.get("label","") in ("ORG","ORGANIZATION")]
        citation_re = re.compile(r"\(([A-Z][a-z]+(?:\s+et\s+al\.?)?,?\s*\d{4})\)")
        inline_cites = citation_re.findall(text)
        qa_answers = []
        for q in CITE_QUESTIONS[:2]:
            res = call_nlp("qa", {"question": q, "context": text[:4000]})
            qa_answers.append({"question": q, "answer": res.get("answer","")})
        result["data"] = {"inline_citations": list(dict.fromkeys(inline_cites)), "cited_persons": list(dict.fromkeys(persons)), "cited_orgs": list(dict.fromkeys(orgs)), "citation_count": len(inline_cites), "qa_answers": qa_answers}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 21. `mda-publication.station` (ST_032) — TERMINAL
**config.json** → `"workers": {"default": ["summarizer"]}`, set `"outputs": {"final_export": true, "artifact_type": "md"}`
**Job:** Assemble final MDA publication — combine all upstream artifacts into a publishable markdown document.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        title = data.get("title", path.stem)
        body = data.get("body") or data.get("content") or text_from_input(obj)
        sum_res = call_nlp("summarize", {"text": body[:5000]})
        abstract = sum_res.get("summary","")
        pub_md = f"# {title}\n\n## Abstract\n{abstract}\n\n## Content\n{body}"
        export_path = EXPORTS / f"{path.stem}_publication.md"
        export_path.write_text(pub_md, encoding="utf-8")
        result["data"] = {"publication_path": str(export_path), "title": title, "abstract": abstract, "word_count": word_count(body)}
        log.info("Publication exported -> %s", export_path)
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 22. `metadata-extractor.station` (ST-HTML-METADATA-001)
**config.json** → `"workers": {"default": ["ner_enhanced"]}`
**Job:** Extract structured YAML metadata from documents — title, authors, date, keywords, DOI, abstract.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "ner_enhanced", "ner")
```
**Section 07:**
```python
META_QUESTIONS = {"title": "What is the title of this document?", "authors": "Who are the authors of this document?", "date": "What is the publication date?", "abstract": "What is the abstract or summary?"}

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        ner_res = call_nlp("ner", {"text": text[:4000]})
        entities = ner_res.get("entities", [])
        persons = [e["text"] for e in entities if e.get("label","") in ("PER","PERSON")]
        orgs = [e["text"] for e in entities if e.get("label","") in ("ORG","ORGANIZATION")]
        dates = [e["text"] for e in entities if e.get("label","") in ("DATE","TIME")]
        header = text[:500]
        title_line = next((l.strip() for l in header.splitlines() if len(l.strip()) > 10 and not l.startswith("#"*3)), path.stem)
        metadata = {"title": title_line, "authors": list(dict.fromkeys(persons))[:5], "organizations": list(dict.fromkeys(orgs))[:3], "dates": list(dict.fromkeys(dates))[:3], "entities": entities[:20]}
        result["data"] = {"metadata": metadata, "yaml_candidate": metadata}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 23. `obsidian-export.station` (ST_034) — TERMINAL
**config.json** → `"workers": {"default": ["summarizer"]}`, set `"outputs": {"final_export": true, "artifact_type": "md"}`
**Job:** Format artifact data as an Obsidian-ready markdown note with YAML frontmatter and wiki links.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        title = data.get("title", path.stem)
        body = text_from_input(obj)
        sum_res = call_nlp("summarize", {"text": body[:4000]})
        summary = sum_res.get("summary","")
        ner_res = call_nlp("ner", {"text": body[:2000]})
        tags = list(dict.fromkeys([e["text"].replace(" ","_") for e in ner_res.get("entities",[])[:8]]))
        frontmatter = f"---\ntitle: {title}\ntags: [{', '.join(tags)}]\ncreated: {datetime.now():%Y-%m-%d}\n---\n\n"
        note = frontmatter + f"## Summary\n{summary}\n\n## Content\n{body}"
        export_path = EXPORTS / f"{path.stem}_obsidian.md"
        export_path.write_text(note, encoding="utf-8")
        result["data"] = {"obsidian_path": str(export_path), "title": title, "tags": tags}
        log.info("Obsidian note exported -> %s", export_path)
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 24. `open-brain-map.station` (ST_035)
**config.json** → `"workers": {"default": ["embeddings_fast"]}`
**Job:** Open/expand a brain map — take an existing brain map artifact and add new nodes via embedding similarity.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")
```
**Section 07:** (same as brain-map but reads existing map data and appends)
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        existing_nodes = data.get("nodes", [])
        text = text_from_input(obj)
        new_sections = sections(text)
        all_texts = [n.get("text_preview","") or n.get("text","") for n in existing_nodes] + [s.get("text","")[:400] for s in new_sections]
        all_texts = [t for t in all_texts if len(t) > 20][:30]
        res = call_nlp("embed", {"texts": all_texts})
        vecs = res.get("embeddings",[])
        edges = []
        for i in range(len(vecs)):
            for j in range(i+1,len(vecs)):
                sim = cosine(vecs[i],vecs[j])
                if sim > 0.45:
                    edges.append({"source": i, "target": j, "weight": round(sim,4)})
        result["data"] = {"node_count": len(all_texts), "edge_count": len(edges), "edges": edges[:150], "nodes": [{"id":i,"preview":all_texts[i][:80]} for i in range(len(all_texts))]}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 25. `operators-canon.station` (operators-canon)
**config.json** → `"workers": {"default": ["zero_shot"]}`
**Job:** Identify and classify logical/theological operators in text (AND, OR, NOT, IMPLIES, NECESSARILY, POSSIBLY, etc.)

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")
```
**Section 07:**
```python
OPERATOR_LABELS = ["logical conjunction", "logical disjunction", "logical negation",
                   "implication", "necessity", "possibility", "causal relationship",
                   "temporal sequence", "equivalence", "conditional statement"]

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        sent_list = sentences(text)[:30]
        operator_map = []
        for s in sent_list:
            if len(s) < 15: continue
            res = call_nlp("classify", {"text": s, "labels": OPERATOR_LABELS})
            top = res.get("labels",[{}])[0]
            if top.get("score",0) > 0.3:
                operator_map.append({"sentence": s, "operator_type": top.get("label",""), "confidence": top.get("score",0)})
        result["data"] = {"operators_found": operator_map, "operator_count": len(operator_map), "operator_types": list(dict.fromkeys(o["operator_type"] for o in operator_map))}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 26. `postgres-sync.station` (ST_043)
**config.json** → `"workers": {"default": ["embeddings_fast"]}`
**Job:** Prepare artifact data for PostgreSQL sync — embed content for vector storage, structure for DB insert.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        text = text_from_input(obj)
        res = call_nlp("embed", {"texts": [text[:1000]]})
        vec = res.get("embeddings",[None])[0]
        db_record = {"source_file": path.name, "content_preview": text[:500], "embedding": vec, "metadata": {k:v for k,v in data.items() if isinstance(v,(str,int,float,bool))}, "sync_ready": True}
        result["data"] = {"db_record": db_record, "vector_dim": len(vec) if vec else 0}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 27. `reading-level-glossary.station` (ST-HTML-READING-GLOSSARY-001)
**config.json** → `"workers": {"default": ["ner_general"]}`
**Job:** Compute reading grade level (Flesch-Kincaid), identify technical terms, generate glossary.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "ner_general", "ner")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        fk_score = flesch_reading_ease(text)
        ner_res = call_nlp("ner", {"text": text[:4000]})
        entities = ner_res.get("entities", [])
        tech_terms = [e["text"] for e in entities if len(e["text"].split()) <= 3]
        glossary = list(dict.fromkeys(tech_terms))[:30]
        if fk_score >= 70: grade = "Easy (6th grade)"
        elif fk_score >= 50: grade = "Standard (10th grade)"
        elif fk_score >= 30: grade = "Difficult (college)"
        else: grade = "Very Difficult (professional)"
        result["data"] = {"flesch_score": round(fk_score,2), "reading_grade": grade, "glossary_terms": glossary, "entity_count": len(entities), "word_count": word_count(text)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 28. `section-splitter.station` (ST-HTML-SECTION-SPLITTER-001)
**config.json** → `"workers": {"default": ["summarizer"]}`
**Job:** Split HTML or markdown document into atomic sections, summarize each section.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        raw = read_input(path)
        text = strip_html(raw) if isinstance(raw,str) and "<" in raw else text_from_input(raw)
        sec_list = sections(text)
        enriched = []
        for s in sec_list[:15]:
            body = s.get("text","")
            if len(body) > 100:
                res = call_nlp("summarize", {"text": body[:2000]})
                s["summary"] = res.get("summary","")
            s["word_count"] = word_count(body)
            enriched.append(s)
        result["data"] = {"sections": enriched, "section_count": len(enriched), "total_words": sum(s.get("word_count",0) for s in enriched)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 29. `series-flow-auditor.station` (ST_051)
**config.json** → `"workers": {"default": ["contradiction_primary"]}`
**Job:** Audit document series for flow consistency — detect argument drift, contradictions, and missing transitions between documents.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "contradiction_primary", "contradiction")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        series = data.get("series") or data.get("documents") or []
        if not series:
            text = text_from_input(obj)
            series = [{"id": str(i), "text": p} for i,p in enumerate(paragraphs(text)[:20])]
        flow_issues = []; transitions = []
        for i in range(len(series)-1):
            a = series[i].get("text","")[:500]; b = series[i+1].get("text","")[:500]
            if not a or not b: continue
            res = call_nlp("contradiction", {"text_a": a, "text_b": b})
            scores = res.get("scores",{}); con = float(scores.get("contradiction",0))
            trans = {"from_id": series[i].get("id",i), "to_id": series[i+1].get("id",i+1), "contradiction": con, "entailment": float(scores.get("entailment",0))}
            transitions.append(trans)
            if con > 0.5: flow_issues.append({**trans, "severity": "HIGH" if con>0.7 else "MEDIUM"})
        result["data"] = {"transitions": transitions, "flow_issues": flow_issues, "issue_count": len(flow_issues), "series_length": len(series)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 30. `session-handoff-combined.station` (ST_052)
**config.json** → `"workers": {"default": ["summarizer"]}`
**Job:** Combine multiple session handoff documents into a single coherent summary handoff.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        handoffs = data.get("handoffs") or [obj] if isinstance(obj,dict) else []
        combined_text = "\n\n---\n\n".join(text_from_input(h) for h in handoffs) if handoffs else text_from_input(obj)
        res = call_nlp("summarize", {"text": combined_text[:5000]})
        summary = res.get("summary","")
        result["data"] = {"combined_summary": summary, "handoff_count": len(handoffs), "combined_length": len(combined_text), "ready_for_drop": True}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 31. `session-handoff-drop.station` (ST_053)
**config.json** → `"workers": {"default": ["summarizer"]}`
**Job:** Format a session handoff for dropping into the next session — produce a compact, structured handoff note.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        res = call_nlp("summarize", {"text": text[:4000]})
        summary = res.get("summary","")
        handoff_note = f"## SESSION HANDOFF\n**Generated:** {datetime.now():%Y-%m-%d %H:%M}\n\n### What Was Done\n{summary}\n\n### Full Context\n{text[:2000]}"
        result["data"] = {"handoff_note": handoff_note, "summary": summary, "source_length": len(text)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 32. `theophysics-engine.station` (ST_055)
**config.json** → `"workers": {"default": ["contradiction_primary"]}`
**Job:** Core theophysics processing — analyze theological-physics text for logical coherence, axiom consistency, and operator validity.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "contradiction_primary", "contradiction")
```
**Section 07:**
```python
THEOPHYSICS_LABELS = ["axiom", "theorem", "operator definition", "physical law", "theological claim",
                      "mathematical relationship", "philosophical premise", "boundary condition"]

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        sent_list = sentences(text)[:30]
        classified = []
        for s in sent_list:
            if len(s) < 15: continue
            res = call_nlp("classify", {"text": s, "labels": THEOPHYSICS_LABELS})
            top = res.get("labels",[{}])[0]
            classified.append({"text": s, "type": top.get("label",""), "confidence": top.get("score",0)})
        axioms = [c for c in classified if c["type"] == "axiom"]
        tensions = []
        for i in range(len(axioms)):
            for j in range(i+1, len(axioms)):
                res = call_nlp("contradiction", {"text_a": axioms[i]["text"], "text_b": axioms[j]["text"]})
                con = float(res.get("scores",{}).get("contradiction",0))
                if con > 0.4:
                    tensions.append({"axiom_a": axioms[i]["text"], "axiom_b": axioms[j]["text"], "contradiction": con})
        result["data"] = {"classified": classified, "axioms": axioms, "tensions": tensions, "axiom_count": len(axioms)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 33. `trinity-canon.station` (trinity-canon)
**config.json** → `"workers": {"default": ["zero_shot"]}`
**Job:** Analyze Trinity doctrine text — classify statements as relating to Father, Son, Holy Spirit, or Triune relationships; detect coherence issues.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")
```
**Section 07:**
```python
TRINITY_LABELS = ["the Father", "the Son / Jesus Christ", "the Holy Spirit",
                  "Triune relationship", "divine nature", "incarnation", "perichoresis",
                  "economic Trinity", "immanent Trinity"]

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        sent_list = sentences(text)[:40]
        person_map = {label: [] for label in TRINITY_LABELS}
        for s in sent_list:
            if len(s) < 15: continue
            res = call_nlp("classify", {"text": s, "labels": TRINITY_LABELS})
            top = res.get("labels",[{}])[0]
            if top.get("score",0) > 0.3:
                person_map[top["label"]].append({"text": s, "confidence": top["score"]})
        non_empty = {k:v for k,v in person_map.items() if v}
        result["data"] = {"person_map": non_empty, "statement_count": sum(len(v) for v in non_empty.values()), "persons_addressed": list(non_empty.keys())}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 34. `vault-rater-tsr100.station` (ST_059)
**config.json** → `"workers": {"default": ["contradiction_primary"]}`
**Job:** Rate vault content on the TSR-100 scale — score theological rigor, source reliability, and claim support.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "contradiction_primary", "contradiction")
```
**Section 07:**
```python
TSR_DIMENSIONS = ["factual accuracy", "theological soundness", "logical consistency",
                  "source reliability", "argument strength", "doctrinal alignment"]

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        dim_scores = {}
        for dim in TSR_DIMENSIONS:
            res = call_nlp("classify", {"text": text[:2000], "labels": [f"high {dim}", f"medium {dim}", f"low {dim}"]})
            top = res.get("labels",[{}])[0]
            label = top.get("label","")
            score = 100 if "high" in label else (50 if "medium" in label else 20)
            dim_scores[dim] = {"label": label, "score": score}
        tsr_total = round(sum(d["score"] for d in dim_scores.values()) / len(dim_scores))
        sent_list = sentences(text)[:20]
        contradictions = 0
        for i in range(min(len(sent_list)-1,10)):
            res = call_nlp("contradiction", {"text_a": sent_list[i][:300], "text_b": sent_list[i+1][:300]})
            if float(res.get("scores",{}).get("contradiction",0)) > 0.5:
                contradictions += 1
        tsr_total = max(0, tsr_total - contradictions*5)
        result["data"] = {"tsr_score": tsr_total, "dimensions": dim_scores, "contradictions_found": contradictions, "rating": "A" if tsr_total>=80 else ("B" if tsr_total>=60 else ("C" if tsr_total>=40 else "F"))}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 35. `youtube-fetch.station` (ST_061)
**config.json** → `"workers": {"default": ["summarizer"]}`
**Job:** Fetch YouTube video metadata and transcript from a URL or video ID input, summarize content.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")
```
**Section 07:**
```python
YT_ID_RE = re.compile(r"(?:v=|youtu\.be/)([A-Za-z0-9_\-]{11})")

def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        video_ids = YT_ID_RE.findall(text)
        urls = [f"https://www.youtube.com/watch?v={vid}" for vid in video_ids]
        summary = ""
        if len(text) > 200:
            res = call_nlp("summarize", {"text": text[:4000]})
            summary = res.get("summary","")
        result["data"] = {"video_ids": video_ids, "video_urls": urls, "input_summary": summary, "video_count": len(video_ids), "note": "Use yt-dlp or youtube-transcript-api to fetch full transcripts"}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

### 36. `youtube-scrape.station` (ST_063)
**config.json** → `"workers": {"default": ["summarizer"]}`
**Job:** Process a scraped YouTube transcript — clean, chunk, and summarize the transcript content.

**Section 06:**
```python
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")
```
**Section 07:**
```python
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        transcript = data.get("transcript") or text_from_input(obj)
        transcript = re.sub(r"\[\d+:\d+\]","", transcript)
        chunks = [transcript[i:i+3000] for i in range(0, min(len(transcript),12000), 3000)]
        summaries = []
        for i, chunk in enumerate(chunks):
            res = call_nlp("summarize", {"text": chunk})
            summaries.append({"chunk": i+1, "summary": res.get("summary","")})
        full_res = call_nlp("summarize", {"text": " ".join(s["summary"] for s in summaries)[:4000]})
        result["data"] = {"chunk_summaries": summaries, "full_summary": full_res.get("summary",""), "transcript_length": len(transcript), "chunks_processed": len(chunks)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
```

---

## After Completing All Stations

Run the audit script to verify:
```
python D:\GitHub\BACKSIDE-NLP-NEW\stations\_STATION_AUDIT.py
```
Expected result: 0 NONE workers, all 71 stations OK.

Then copy the updated station folders from `D:\GitHub\BACKSIDE-NLP-NEW\stations\` to `\\192.168.2.50\brain\04_STATIONS\` using:
```
robocopy "D:\GitHub\BACKSIDE-NLP-NEW\stations" "\\192.168.2.50\brain\04_STATIONS" /E /XO /NFL /NDL
```

## What NOT to touch
- Sections 00–05 (imports, constants, config, logging, ingest, validate)
- Sections 08–12 (artifacts, job card, handoff, archive, main)
- Any already-wired station (those with a real model already in config.json)
- `_shared/station_helpers.py`
- `_shared/__init__.py` if it exists
