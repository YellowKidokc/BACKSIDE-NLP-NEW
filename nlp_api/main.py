"""
POF 2828 NLP API - FastAPI service exposing all NLP models + vector store.
Run: uvicorn main:app --host 0.0.0.0 --port 8700
Dashboard: http://localhost:8700/docs

Every station calls this instead of loading models locally.
Models load lazily on first request, stay in memory.
"""
from __future__ import annotations
import json, os, time, hashlib
from pathlib import Path
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="POF 2828 NLP API",
    description="Shared NLP model service for Theophysics Brain stations",
    version="1.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# -- Model paths --
MODELS_ROOT = Path(os.environ.get("NLP_MODELS_ROOT", r"\\192.168.2.50\brain\05_MODELS"))

MODEL_PATHS = {
    "contradiction_primary": MODELS_ROOT / "01_CONTRADICTION_PRIMARY",
    "contradiction_fast":    MODELS_ROOT / "02_CONTRADICTION_FAST",
    "embeddings_fast":       MODELS_ROOT / "03_EMBEDDINGS_FAST",
    "scifact_verify":        MODELS_ROOT / "05_SCIENTIFIC_CLAIM_VERIFY",
    "ner_general":           MODELS_ROOT / "06_NER_GENERAL",
    "zero_shot":             MODELS_ROOT / "07_ZERO_SHOT_CLASSIFIER",
    "summarizer":            MODELS_ROOT / "08_SUMMARIZER",
    "reranker":              MODELS_ROOT / "09_RERANKER",
    "sentiment":             MODELS_ROOT / "10_SENTIMENT",
    "contradiction_tiny":    MODELS_ROOT / "14_CONTRADICTION_TINY",
    "long_nli":              MODELS_ROOT / "15_CONTRADICTION_ENSEMBLE_LONG",
    "ner_enhanced":          MODELS_ROOT / "16_NER_ENHANCED",
    "qa_extractor":          MODELS_ROOT / "18_QA_EXTRACTOR",
    "sbert_minilm":          MODELS_ROOT / "sbert_minilm",
}

# -- Lazy model cache --
_models: dict[str, object] = {}
_load_times: dict[str, float] = {}
_startup = datetime.now()

def _load(key: str, loader):
    if key not in _models:
        path = MODEL_PATHS.get(key)
        if not path or not path.exists():
            raise HTTPException(404, f"Model not found: {key}")
        t0 = time.time()
        _models[key] = loader(str(path))
        _load_times[key] = time.time() - t0
    return _models[key]


# ============================================================
# Request / Response schemas
# ============================================================
class TextInput(BaseModel):
    text: str
    model: Optional[str] = None

class TextPairInput(BaseModel):
    premise: str
    hypothesis: str
    model: str = "contradiction_primary"

class ClassifyInput(BaseModel):
    text: str
    labels: list[str]
    model: str = "zero_shot"

class EmbedInput(BaseModel):
    texts: list[str]
    model: str = "embeddings_fast"

class QAInput(BaseModel):
    question: str
    context: str

class RerankInput(BaseModel):
    query: str
    documents: list[str]
    top_k: int = 5

class VectorIngestInput(BaseModel):
    text: str
    metadata: dict = {}
    doc_id: Optional[str] = None

class VectorQueryInput(BaseModel):
    query: str
    n_results: int = 5
    where: Optional[dict] = None



# ============================================================
# Endpoints
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "uptime_seconds": (datetime.now() - _startup).total_seconds(),
        "models_loaded": list(_models.keys()),
        "load_times": _load_times,
        "models_root": str(MODELS_ROOT),
    }


@app.get("/models")
def list_models():
    return {
        k: {"path": str(v), "exists": v.exists(), "loaded": k in _models}
        for k, v in MODEL_PATHS.items()
    }


# -- NLI / Contradiction --
@app.post("/nlp/contradiction")
def check_contradiction(inp: TextPairInput):
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    import torch

    key = inp.model
    path = MODEL_PATHS.get(key)
    if not path:
        raise HTTPException(404, f"Unknown model: {key}")

    cache_key = f"nli_{key}"
    if cache_key not in _models:
        t0 = time.time()
        tokenizer = AutoTokenizer.from_pretrained(str(path))
        model = AutoModelForSequenceClassification.from_pretrained(str(path))
        model.eval()
        _models[cache_key] = (tokenizer, model)
        _load_times[cache_key] = time.time() - t0

    tokenizer, model = _models[cache_key]
    inputs = tokenizer(inp.premise, inp.hypothesis, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=-1)[0].tolist()
    # DeBERTa NLI order: entailment, neutral, contradiction
    # (some models differ -- check config.json id2label)
    id2label = model.config.id2label if hasattr(model.config, "id2label") else {0: "entailment", 1: "neutral", 2: "contradiction"}
    labels = {id2label[i]: round(p, 4) for i, p in enumerate(probs)}
    predicted = max(labels, key=labels.get)
    return {"label": predicted, "scores": labels, "model": key}


# -- Zero-Shot Classification --
@app.post("/nlp/classify")
def zero_shot_classify(inp: ClassifyInput):
    from transformers import pipeline as hf_pipeline

    key = f"zs_{inp.model}"
    if key not in _models:
        path = MODEL_PATHS.get(inp.model)
        if not path:
            raise HTTPException(404, f"Unknown model: {inp.model}")
        t0 = time.time()
        _models[key] = hf_pipeline("zero-shot-classification", model=str(path))
        _load_times[key] = time.time() - t0

    pipe = _models[key]
    result = pipe(inp.text, inp.labels, multi_label=True)
    return {
        "labels": result["labels"],
        "scores": [round(s, 4) for s in result["scores"]],
        "model": inp.model,
    }


# -- Embeddings --
@app.post("/nlp/embed")
def embed_texts(inp: EmbedInput):
    from sentence_transformers import SentenceTransformer

    key = f"embed_{inp.model}"
    if key not in _models:
        path = MODEL_PATHS.get(inp.model)
        if not path:
            raise HTTPException(404, f"Unknown model: {inp.model}")
        t0 = time.time()
        _models[key] = SentenceTransformer(str(path))
        _load_times[key] = time.time() - t0

    model = _models[key]
    embeddings = model.encode(inp.texts, show_progress_bar=False)
    return {
        "embeddings": embeddings.tolist(),
        "dim": embeddings.shape[1],
        "count": len(inp.texts),
        "model": inp.model,
    }


# -- Summarization --
@app.post("/nlp/summarize")
def summarize(inp: TextInput):
    from transformers import pipeline as hf_pipeline

    key = "summarizer"
    if key not in _models:
        path = MODEL_PATHS.get("summarizer")
        t0 = time.time()
        _models[key] = hf_pipeline("summarization", model=str(path))
        _load_times[key] = time.time() - t0

    pipe = _models[key]
    text = inp.text[:4096]
    result = pipe(text, max_length=200, min_length=40, do_sample=False)
    return {"summary": result[0]["summary_text"], "model": "summarizer"}


# -- NER --
@app.post("/nlp/ner")
def named_entities(inp: TextInput):
    from transformers import pipeline as hf_pipeline

    model_key = inp.model or "ner_general"
    key = f"ner_{model_key}"
    if key not in _models:
        path = MODEL_PATHS.get(model_key)
        if not path:
            raise HTTPException(404, f"Unknown model: {model_key}")
        t0 = time.time()
        _models[key] = hf_pipeline("ner", model=str(path), aggregation_strategy="simple")
        _load_times[key] = time.time() - t0

    pipe = _models[key]
    results = pipe(inp.text[:2048])
    entities = [
        {"entity": r["entity_group"], "word": r["word"], "score": round(r["score"], 4),
         "start": r["start"], "end": r["end"]}
        for r in results
    ]
    return {"entities": entities, "count": len(entities), "model": model_key}


# -- Sentiment --
@app.post("/nlp/sentiment")
def sentiment(inp: TextInput):
    from transformers import pipeline as hf_pipeline

    key = "sentiment"
    if key not in _models:
        path = MODEL_PATHS.get("sentiment")
        t0 = time.time()
        _models[key] = hf_pipeline("sentiment-analysis", model=str(path))
        _load_times[key] = time.time() - t0

    pipe = _models[key]
    result = pipe(inp.text[:512])
    return {"label": result[0]["label"], "score": round(result[0]["score"], 4), "model": "sentiment"}


# -- Extractive QA --
@app.post("/nlp/qa")
def extractive_qa(inp: QAInput):
    from transformers import pipeline as hf_pipeline

    key = "qa"
    if key not in _models:
        path = MODEL_PATHS.get("qa_extractor")
        t0 = time.time()
        _models[key] = hf_pipeline("question-answering", model=str(path))
        _load_times[key] = time.time() - t0

    pipe = _models[key]
    result = pipe(question=inp.question, context=inp.context[:4096])
    return {
        "answer": result["answer"],
        "score": round(result["score"], 4),
        "start": result["start"],
        "end": result["end"],
        "model": "qa_extractor",
    }



# ============================================================
# Vector Store (ChromaDB)
# ============================================================
# Shared corpus-level vector database. All stations can query.
# Stores: text chunks + metadata (series, lane, article, source_path)

VECTOR_DB_PATH = Path(os.environ.get("VECTOR_DB_PATH", r"D:\GitHub\BACKSIDE-NLP-NEW\nlp_api\vector_db"))
_chroma_collection = None

def _get_collection():
    global _chroma_collection
    if _chroma_collection is None:
        import chromadb
        from chromadb.config import Settings
        VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(VECTOR_DB_PATH))
        _chroma_collection = client.get_or_create_collection(
            name="theophysics_corpus",
            metadata={"hnsw:space": "cosine"},
        )
    return _chroma_collection


@app.post("/vector/ingest")
def vector_ingest(inp: VectorIngestInput):
    """Add a document chunk to the vector store."""
    collection = _get_collection()
    doc_id = inp.doc_id or hashlib.md5(inp.text.encode()).hexdigest()
    collection.upsert(
        ids=[doc_id],
        documents=[inp.text],
        metadatas=[inp.metadata],
    )
    return {"ok": True, "doc_id": doc_id, "total": collection.count()}


@app.post("/vector/ingest_batch")
def vector_ingest_batch(items: list[VectorIngestInput]):
    """Add multiple chunks at once."""
    collection = _get_collection()
    ids = []
    docs = []
    metas = []
    for item in items:
        doc_id = item.doc_id or hashlib.md5(item.text.encode()).hexdigest()
        ids.append(doc_id)
        docs.append(item.text)
        metas.append(item.metadata)
    collection.upsert(ids=ids, documents=docs, metadatas=metas)
    return {"ok": True, "count": len(ids), "total": collection.count()}


@app.post("/vector/query")
def vector_query(inp: VectorQueryInput):
    """Semantic search across the corpus."""
    collection = _get_collection()
    kwargs = {
        "query_texts": [inp.query],
        "n_results": inp.n_results,
    }
    if inp.where:
        kwargs["where"] = inp.where
    results = collection.query(**kwargs)
    hits = []
    for i in range(len(results["ids"][0])):
        hits.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i] if results["documents"] else "",
            "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
            "distance": results["distances"][0][i] if results["distances"] else None,
        })
    return {"hits": hits, "total_in_store": collection.count()}


@app.get("/vector/stats")
def vector_stats():
    """Get vector store statistics."""
    collection = _get_collection()
    return {
        "collection": "theophysics_corpus",
        "total_documents": collection.count(),
        "db_path": str(VECTOR_DB_PATH),
    }


@app.delete("/vector/clear")
def vector_clear():
    """Clear the entire vector store. Use with caution."""
    global _chroma_collection
    import chromadb
    client = chromadb.PersistentClient(path=str(VECTOR_DB_PATH))
    client.delete_collection("theophysics_corpus")
    _chroma_collection = None
    return {"ok": True, "message": "Vector store cleared"}


# ============================================================
# Startup
# ============================================================
if __name__ == "__main__":
    import uvicorn
    print(f"\n  POF 2828 NLP API")
    print(f"  Models: {MODELS_ROOT}")
    print(f"  Vector DB: {VECTOR_DB_PATH}")
    print(f"  Docs: http://localhost:8700/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=8700)
