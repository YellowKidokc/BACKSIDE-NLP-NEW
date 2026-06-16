"""
nlp_layer.py â€” POF 2828 Shared NLP Brain
==========================================
Single module. Every tool calls analyze() and gets back:
  - classification (what domain/type is this)
  - sentiment (positive/negative)
  - similarity score (vs a reference)
  - summary + suggested title (when text is long)

Models load on demand, stay cached in memory.
All stored on \\dlowenas\\brain\\models\

Usage:
    from nlp_layer import NLPLayer
    nlp = NLPLayer()
    result = nlp.analyze("your text", labels=["code","document","theophysics"])
"""

import os
import time
import logging
from pathlib import Path
from typing import Optional

log = logging.getLogger("nlp_layer")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [NLP] %(message)s")

# â”€â”€ Model paths â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BRAIN = Path(r"\\dlowenas\brain\models")
NLI_BRAIN = Path(r"\\dlowenas\brain\NLI_Models")

MODEL_PATHS = {
    "deberta":  NLI_BRAIN / "nli-deberta-v3-base",
    "sbert":    BRAIN / "huggingface" / "hub" / "models--sentence-transformers--all-MiniLM-L6-v2" / "snapshots" / "c9745ed1d9f207416be6d2e6f8de32d1f16199bf",
    "bart":     BRAIN / "bart_summarizer",
    "whisper":  BRAIN / "whisper_large_v3",
    "mistral":  BRAIN / "mistral_7b",
}

# â”€â”€ Lazy-loaded model cache â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
_cache = {}

def _load_deberta():
    if "deberta" not in _cache:
        log.info("Loading DeBERTa NLI...")
        from transformers import pipeline
        _cache["deberta"] = pipeline(
            "zero-shot-classification",
            model=str(MODEL_PATHS["deberta"]),
            device=-1  # CPU â€” change to 0 for GPU
        )
    return _cache["deberta"]

def _load_sbert():
    if "sbert" not in _cache:
        log.info("Loading SBERT MiniLM...")
        from sentence_transformers import SentenceTransformer
        _cache["sbert"] = SentenceTransformer(str(MODEL_PATHS["sbert"]))
    return _cache["sbert"]

def _load_bart():
    if "bart" not in _cache:
        log.info("Loading BART summarizer...")
        from transformers import pipeline
        _cache["bart"] = pipeline(
            "summarization",
            model=str(MODEL_PATHS["bart"]),
            device=-1
        )
    return _cache["bart"]

def _load_sentiment():
    """Lightweight sentiment â€” uses distilbert from HF hub (tiny, cached)."""
    if "sentiment" not in _cache:
        log.info("Loading sentiment model...")
        from transformers import pipeline
        _cache["sentiment"] = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1
        )
    return _cache["sentiment"]

# â”€â”€ Core functions â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def classify(text: str, labels: list[str],
             multi_label: bool = False) -> dict:
    """
    Zero-shot classification using DeBERTa.
    Returns ranked label scores.

    Example:
        classify("This is a Python script", ["code","document","media"])
        â†’ {"code": 0.91, "document": 0.07, "media": 0.02}
    """
    if not labels:
        return {}
    pipe = _load_deberta()
    truncated = text[:2000]  # DeBERTa has context limit
    result = pipe(truncated, candidate_labels=labels, multi_label=multi_label)
    return dict(zip(result["labels"], result["scores"]))


def sentiment(text: str) -> dict:
    """
    Positive/negative sentiment + confidence.
    Returns: {"label": "POSITIVE", "score": 0.97}
    """
    pipe = _load_sentiment()
    result = pipe(text[:512])[0]
    return {"label": result["label"], "score": round(result["score"], 3)}


def embed(texts: list[str]) -> list:
    """
    Embed text(s) to vectors using SBERT.
    Use for similarity, dedup, semantic search.
    """
    model = _load_sbert()
    return model.encode(texts, convert_to_numpy=True).tolist()


def similarity(text_a: str, text_b: str) -> float:
    """
    Cosine similarity between two texts. 0.0-1.0
    """
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    model = _load_sbert()
    vecs = model.encode([text_a, text_b])
    score = cosine_similarity([vecs[0]], [vecs[1]])[0][0]
    return round(float(score), 4)


def summarize(text: str, max_length: int = 130,
              min_length: int = 30) -> str:
    """
    Summarize long text using BART.
    Falls back to first 200 chars if BART not loaded.
    """
    if len(text) < 200:
        return text
    try:
        pipe = _load_bart()
        result = pipe(text[:1024], max_length=max_length,
                      min_length=min_length, do_sample=False)
        return result[0]["summary_text"]
    except Exception as e:
        log.warning(f"BART summarize failed: {e}")
        return text[:200] + "..."


def suggest_title(text: str) -> str:
    """
    Generate a short title from text content.
    Uses BART summary â†’ takes first sentence.
    """
    summary = summarize(text, max_length=40, min_length=5)
    # First sentence only
    title = summary.split(".")[0].strip()
    return title[:80] if title else text[:50]


def find_duplicates(texts: list[str],
                    threshold: float = 0.92) -> list[tuple[int, int, float]]:
    """
    Find near-duplicate texts by cosine similarity.
    Returns list of (idx_a, idx_b, score) pairs above threshold.
    """
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    model = _load_sbert()
    vecs = model.encode(texts)
    sim_matrix = cosine_similarity(vecs)
    dupes = []
    n = len(texts)
    for i in range(n):
        for j in range(i+1, n):
            score = float(sim_matrix[i][j])
            if score >= threshold:
                dupes.append((i, j, round(score, 4)))
    return sorted(dupes, key=lambda x: -x[2])


# â”€â”€ Master analyze function â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

DEFAULT_LABELS = [
    "code", "document", "spreadsheet", "image", "audio", "video",
    "theophysics", "trading", "research", "task", "note", "bookmark",
]

def analyze(text: str,
            labels: Optional[list[str]] = None,
            run_sentiment: bool = True,
            run_summary: bool = False) -> dict:
    """
    Master function. Runs classification + optional sentiment + optional summary.
    This is what the file organizer, Truth Engine, and overlay all call.

    Args:
        text:           The text to analyze
        labels:         Custom label list (uses DEFAULT_LABELS if not provided)
        run_sentiment:  Include sentiment analysis (fast)
        run_summary:    Include BART summary (slow, only for long text)

    Returns:
        {
            "classification": {"code": 0.91, "document": 0.07, ...},
            "top_label": "code",
            "top_score": 0.91,
            "sentiment": {"label": "POSITIVE", "score": 0.97},
            "summary": "...",    # only if run_summary=True
            "title": "...",      # only if run_summary=True
            "word_count": 42,
            "elapsed_ms": 312,
        }
    """
    t0 = time.time()
    result = {"word_count": len(text.split())}

    # Classification
    use_labels = labels or DEFAULT_LABELS
    scores = classify(text, use_labels)
    result["classification"] = scores
    if scores:
        top = max(scores, key=scores.get)
        result["top_label"] = top
        result["top_score"] = round(scores[top], 3)

    # Sentiment
    if run_sentiment:
        result["sentiment"] = sentiment(text)

    # Summary + title
    if run_summary and len(text) > 200:
        result["summary"] = summarize(text)
        result["title"]   = suggest_title(text)

    result["elapsed_ms"] = round((time.time() - t0) * 1000)
    return result


# â”€â”€ CLI test â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
if __name__ == "__main__":
    tests = [
        ("import os\nfrom pathlib import Path\ndef load():\n    pass",
         ["code", "document", "theophysics"]),
        ("The Master Equation chi integrates G M E S T K R Q F C across all domains",
         ["theophysics", "code", "trading", "research"]),
        ("SPY 0DTE entry at 9:35, theta positive, delta neutral",
         ["trading", "theophysics", "code", "task"]),
        ("TODO: fix the bridge_watch.py path on the NAS",
         ["task", "code", "document", "note"]),
    ]

    print("\n=== NLP Layer â€” POF 2828 ===\n")
    for text, labels in tests:
        print(f"TEXT: {text[:60]}...")
        result = analyze(text, labels=labels)
        print(f"  â†’ {result['top_label']} ({result['top_score']:.0%})"
              f"  | sentiment: {result['sentiment']['label']}"
              f"  | {result['elapsed_ms']}ms")
        print()




def update_workflow_traveler(paper_id: str, station: str, success: bool,
                             artifact: str = "", summary: str = "") -> dict:
    """Stamp the workflow traveler after a station completes."""
    import sys
    orchestrator_dir = Path(__file__).resolve().parent
    if str(orchestrator_dir) not in sys.path:
        sys.path.insert(0, str(orchestrator_dir))
    from tracker import stamp_station
    return stamp_station(
        paper_id=paper_id,
        station=station,
        success=success,
        artifact=artifact,
        summary=summary,
    )
