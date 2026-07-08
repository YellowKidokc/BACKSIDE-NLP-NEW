"""NLP engines for FIS classification cards.

Engine stack (lightest to heaviest):
  1. YAKE         — statistical keyword extraction, no model, ~50MB RAM
  2. spaCy sm     — NER + entities, 12MB model, ~500MB RAM
  3. DeBERTa NLI  — zero-shot classification, 900MB model (optional)
  4. BART         — abstractive summarization, 1.6GB model (optional)

Fallbacks when heavy models disabled:
  - DeBERTa off → rule-based domain/file_type from keywords
  - BART off    → extractive summary (first meaningful sentence)
"""
import json
from pathlib import Path


class YakeEngine:
    """Statistical keyword extraction. No model needed."""

    def __init__(self, top_n: int = 10, language: str = "en"):
        import yake
        self.extractor = yake.KeywordExtractor(
            lan=language, n=3, dedupLim=0.7,
            top=top_n, features=None
        )

    def extract(self, text: str) -> list[dict]:
        results = self.extractor.extract_keywords(text)
        return [{"keyword": kw, "score": round(1 - score, 3), "source": "yake"}
                for kw, score in results]


class SpacyEngine:
    """Named entity recognition via spaCy."""

    def __init__(self, model_name: str = "en_core_web_sm"):
        import spacy
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            import subprocess, sys
            subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
            self.nlp = spacy.load(model_name)

    def extract(self, text: str) -> list[dict]:
        doc = self.nlp(text[:5000])
        seen = set()
        entities = []
        for ent in doc.ents:
            key = (ent.text.lower(), ent.label_)
            if key not in seen:
                seen.add(key)
                entities.append({"entity": ent.text, "label": ent.label_})
        return entities[:20]


class DeBERTaClassifier:
    """Zero-shot classification via DeBERTa NLI."""

    def __init__(self, model_path: str):
        from transformers import pipeline as hf_pipeline
        self.classifier = hf_pipeline(
            "zero-shot-classification",
            model=model_path,
            device=-1  # CPU; set to 0 for GPU
        )

    def classify(self, text: str, candidate_labels: list[str]) -> dict:
        """Returns {label: confidence} for each candidate."""
        result = self.classifier(
            text[:1000],
            candidate_labels=candidate_labels,
            multi_label=False
        )
        return {
            "label": result["labels"][0],
            "confidence": round(result["scores"][0] * 100, 1),
            "all": {l: round(s * 100, 1)
                    for l, s in zip(result["labels"], result["scores"])}
        }


class BARTSummarizer:
    """Abstractive summarization via BART."""

    def __init__(self, model_path: str):
        from transformers import pipeline as hf_pipeline
        self.summarizer = hf_pipeline(
            "summarization",
            model=model_path,
            device=-1
        )

    def summarize(self, text: str, max_words: int = 30) -> str:
        if len(text.split()) < 20:
            return text.strip()
        max_length = max(max_words + 10, 50)
        min_length = min(max_words - 5, 15)
        result = self.summarizer(
            text[:2000],
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        return result[0]["summary_text"].strip()


def extractive_summary(text: str) -> str:
    """Fallback: pick the first meaningful sentence as summary."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text[:3000])
    for s in sentences:
        s = s.strip()
        # Skip very short or header-like sentences
        if len(s.split()) >= 5 and not s.startswith('#'):
            return s[:200]
    return text[:100].strip()


# --- Rule-based fallbacks (when DeBERTa is disabled) ---

DOMAIN_KEYWORDS = {
    "theophysics": ["theophysics", "master equation", "coherence", "entropy", "chi",
                    "grace", "sin", "logos", "axiom", "trinity", "law"],
    "development": ["python", "javascript", "api", "function", "class", "git",
                     "npm", "pip", "docker", "code", "debug", "module"],
    "documents": ["report", "memo", "letter", "proposal", "minutes", "agenda"],
    "brain_system": ["brain", "nlp", "pipeline", "station", "watcher", "classify"],
    "website": ["html", "css", "page", "deploy", "cloudflare", "domain", "url"],
    "trading": ["stock", "option", "theta", "spy", "0dte", "trade", "chart"],
    "lean": ["theorem", "proof", "sorry", "lean", "mathlib", "tactic"],
    "infrastructure": ["proxmox", "nas", "synology", "postgres", "network", "vm"],
    "personal_admin": ["invoice", "receipt", "tax", "insurance", "bill", "payment"],
    "media": ["audio", "video", "image", "photo", "recording", "podcast"],
    "ai_research": ["llm", "transformer", "embedding", "model", "training", "prompt"],
}


FILE_TYPE_KEYWORDS = {
    "research_paper": ["abstract", "hypothesis", "methodology", "conclusion", "findings"],
    "code_file": ["import", "def ", "function", "class ", "return", "const "],
    "transcript": ["speaker", "timestamp", "[", "00:", "said"],
    "config": ["[section]", "key=", "port", "host", "path", "enabled"],
    "notes": ["note", "todo", "idea", "thought", "remember"],
    "session_log": ["session", "worked on", "next session", "blocked", "handoff"],
    "prompt": ["you are", "respond", "generate", "instructions", "system prompt"],
    "article": ["published", "author", "readers", "introduction", "section"],
    "template": ["template", "placeholder", "{{", "%%", "fill in"],
}


def rule_based_classify(text: str, keywords: list[dict],
                        domain_map: dict = None, type_map: dict = None) -> dict:
    """Classify by keyword matching when DeBERTa is unavailable."""
    if domain_map is None:
        domain_map = DOMAIN_KEYWORDS
    if type_map is None:
        type_map = FILE_TYPE_KEYWORDS

    text_lower = text.lower()
    kw_text = " ".join(k["keyword"].lower() for k in keywords)
    combined = text_lower + " " + kw_text

    # Score domains
    domain_scores = {}
    for domain, triggers in domain_map.items():
        score = sum(1 for t in triggers if t in combined)
        if score > 0:
            domain_scores[domain] = score

    # Score file types
    type_scores = {}
    for ftype, triggers in type_map.items():
        score = sum(1 for t in triggers if t in combined)
        if score > 0:
            type_scores[ftype] = score

    # Pick best or default
    if domain_scores:
        best_domain = max(domain_scores, key=domain_scores.get)
        max_possible = len(domain_map.get(best_domain, []))
        domain_conf = min(domain_scores[best_domain] / max(max_possible, 1) * 100, 95)
    else:
        best_domain = "unknown"
        domain_conf = 10.0

    if type_scores:
        best_type = max(type_scores, key=type_scores.get)
        max_possible = len(type_map.get(best_type, []))
        type_conf = min(type_scores[best_type] / max(max_possible, 1) * 100, 95)
    else:
        best_type = "notes"
        type_conf = 20.0

    return {
        "domain": best_domain,
        "domain_confidence": round(domain_conf, 1),
        "file_type_meaning": best_type,
        "file_type_confidence": round(type_conf, 1),
    }
