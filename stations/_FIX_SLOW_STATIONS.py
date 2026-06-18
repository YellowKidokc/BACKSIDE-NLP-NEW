"""
Fix v2 — replace TIMEOUT / 422 stations with fast 1-call implementations.

Strategy:
  - Embed-classify: embed(text + labels) in ONE call, cosine-rank labels locally
  - Single summarize: one call on truncated full text
  - Contradiction: use correct premise/hypothesis fields, max 1-3 calls
  - QA: limit to 1 question
"""
import re as _re, sys, subprocess, tempfile, os
from pathlib import Path

STATIONS_DIR = Path(__file__).parent
S06_MARKER = "# 06_NLP_ROUTE  *** STATION-SPECIFIC ***"
S08_MARKER = "# 08_ARTIFACTS"

EMBED_CLASSIFY_HELPER = """
def _embed_classify(text, labels, top_n=5):
    import math
    all_texts = [text[:1000]] + [l[:100] for l in labels]
    res = call_nlp("embed", {"texts": all_texts})
    vecs = res.get("embeddings", [])
    if len(vecs) < 2:
        return [{"label": l, "score": 0.0} for l in labels]
    text_vec = vecs[0]
    scored = []
    for i, label in enumerate(labels):
        if i + 1 >= len(vecs):
            break
        scored.append({"label": label, "score": round(cosine(text_vec, vecs[i + 1]), 4)})
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:top_n]
"""

COMMON = """\
# ============================================================
# 06_NLP_ROUTE  *** STATION-SPECIFIC ***
# ============================================================
import re as _re, sys as _sys
_sys.path.insert(0, str(STATIONS))
from _shared.station_helpers import (
    API_BASE, base_result, call_nlp, cosine, flesch_reading_ease,
    nlp_route, paragraphs, read_input, sections, sentences,
    strip_html, text_from_input, word_count,
)
"""

REPLACEMENTS = {}

# ─────────────────────────────────────────────────────────────────────────────
# TIMEOUT STATIONS — rewritten with 1-call maximum
# ─────────────────────────────────────────────────────────────────────────────

REPLACEMENTS["7q-classifier.station"] = COMMON + """
_SEVEN_Q = [
    "Who is involved",
    "What is the claim or event",
    "When did this occur",
    "Where did this happen",
    "Why does this matter",
    "How was this determined",
    "What is the implication",
]
""" + EMBED_CLASSIFY_HELPER + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        scored = _embed_classify(text, _SEVEN_Q)
        result["data"] = {
            "seven_q_scores": scored,
            "top_question": scored[0]["label"] if scored else "",
            "top_score": scored[0]["score"] if scored else 0,
            "text_preview": text[:200],
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["fruits-spirit-canon.station"] = COMMON + """
_FRUITS = [
    "love", "joy", "peace", "patience", "kindness",
    "goodness", "faithfulness", "gentleness", "self-control",
]
""" + EMBED_CLASSIFY_HELPER + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        scored = _embed_classify(text, _FRUITS)
        # Check each fruit presence via keyword too
        text_lower = text.lower()
        present = {}
        for item in scored:
            fruit = item["label"]
            kw_hit = fruit in text_lower
            if item["score"] > 0.2 or kw_hit:
                present[fruit] = {"score": item["score"], "keyword_hit": kw_hit}
        dominant = scored[0]["label"] if scored else ""
        result["data"] = {
            "fruits_present": present,
            "fruit_count": len(present),
            "dominant_fruit": dominant,
            "full_ranking": scored,
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["operators-canon.station"] = COMMON + """
_OPERATORS = [
    "logical conjunction AND",
    "logical disjunction OR",
    "logical negation NOT",
    "implication IF-THEN",
    "necessity must always",
    "possibility might could",
    "causal relationship causes",
    "temporal sequence before after",
    "equivalence equals identical",
    "conditional statement if given",
]
""" + EMBED_CLASSIFY_HELPER + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        scored = _embed_classify(text, _OPERATORS)
        type_dist = {s["label"].split()[0].lower(): s["score"] for s in scored}
        result["data"] = {
            "operator_ranking": scored,
            "operator_count": len([s for s in scored if s["score"] > 0.1]),
            "type_distribution": type_dist,
            "dominant_operator": scored[0]["label"] if scored else "",
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["trinity-canon.station"] = COMMON + """
_TRINITY = [
    "Father God Creator",
    "Son Jesus Christ incarnation",
    "Holy Spirit comforter advocate",
    "Triune relationship perichoresis",
    "divine nature essence",
    "economic Trinity mission",
    "immanent Trinity eternal",
    "unity of three persons",
]
""" + EMBED_CLASSIFY_HELPER + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        scored = _embed_classify(text, _TRINITY)
        non_empty = {s["label"]: s["score"] for s in scored if s["score"] > 0.1}
        result["data"] = {
            "person_map": non_empty,
            "statement_count": len([s for s in scored if s["score"] > 0.15]),
            "persons_addressed": list(non_empty.keys()),
            "dominant_person": scored[0]["label"] if scored else "",
            "full_ranking": scored,
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["file-intelligence.station"] = COMMON + """
_FILE_TYPES = [
    "research paper academic",
    "sermon homily church",
    "book draft manuscript",
    "personal correspondence letter",
    "spreadsheet numerical data",
    "technical documentation code",
    "theological essay doctrine",
    "meeting notes minutes",
    "media transcript interview",
    "reference bibliography",
]
""" + EMBED_CLASSIFY_HELPER + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        scored = _embed_classify(text, _FILE_TYPES)
        top_type = scored[0]["label"].split()[0] if scored else "unknown"
        # Quick entity extraction from first 500 chars
        header = text[:500]
        entities = [w for w in _re.findall(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*", header)
                    if len(w) > 5 and not w.startswith("The ")][:5]
        slug = _re.sub(r"[^a-z0-9]+", "-", top_type.lower()).strip("-")
        result["data"] = {
            "file_type": top_type,
            "confidence": scored[0]["score"] if scored else 0,
            "file_type_ranking": scored,
            "key_entities": entities,
            "rename_suggestion": f"{slug}_{path.stem[:30]}{path.suffix}",
            "word_count": word_count(text),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["fis.station"] = COMMON + """
_FIS_LABELS = [
    "theological doctrine",
    "scientific research",
    "philosophical argument",
    "administrative record",
    "media content",
    "technical specification",
    "personal communication",
    "reference material",
    "draft content",
    "archived historical",
]
""" + EMBED_CLASSIFY_HELPER + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        scored = _embed_classify(text, _FIS_LABELS)
        top = scored[0] if scored else {"label": "unknown", "score": 0}
        # Keyword tags from text
        tags = list(dict.fromkeys(
            w.lower() for w in _re.findall(r"\b[A-Z][a-z]{3,}\b", text[:1000])
            if len(w) > 4
        ))[:8]
        rename = _re.sub(r"[^a-z0-9]+", "-", top["label"].split()[0].lower()) + f"_{path.stem[:20]}{path.suffix}"
        result["data"] = {
            "fcard": {
                "filename": path.name,
                "category": top["label"],
                "confidence": top["score"],
                "tags": tags,
                "word_count": word_count(text),
                "rename_preview": rename,
                "ranking": scored,
            }
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["apologetic-pipeline.station"] = COMMON + """
_APOL_LABELS = [
    "theological assertion claim",
    "philosophical premise assumption",
    "scriptural reference citation",
    "logical argument inference",
    "counter-argument objection",
    "historical evidence example",
    "conclusion implication",
]
""" + EMBED_CLASSIFY_HELPER + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        scored = _embed_classify(text, _APOL_LABELS)
        # ONE contradiction call between first and last paragraph
        paras = paragraphs(text)
        tensions = []
        if len(paras) >= 2:
            res = call_nlp("contradiction", {
                "premise": paras[0][:400],
                "hypothesis": paras[-1][:400],
            })
            con = float(res.get("scores", {}).get("contradiction", 0))
            if con > 0.25:
                tensions.append({
                    "premise_a": paras[0][:200],
                    "premise_b": paras[-1][:200],
                    "contradiction_score": round(con, 4),
                })
        result["data"] = {
            "argument_type_ranking": scored,
            "dominant_type": scored[0]["label"] if scored else "",
            "tensions": tensions,
            "sentence_count": len(sentences(text)),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["vault-rater-tsr100.station"] = COMMON + """
_TSR_DIMS = [
    "factual accuracy verified",
    "theological soundness orthodox",
    "logical consistency coherent",
    "source reliability credible",
    "argument strength compelling",
    "doctrinal alignment correct",
]
""" + EMBED_CLASSIFY_HELPER + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        scored = _embed_classify(text, _TSR_DIMS)
        # Normalize scores to 0-100 per dimension
        dim_scores = {}
        for s in scored:
            dim = s["label"].split()[0]
            # cosine similarity 0.0-1.0 → scale to 0-100
            dim_scores[dim] = round(min(100, s["score"] * 120))
        tsr_total = round(sum(dim_scores.values()) / max(len(dim_scores), 1)) if dim_scores else 50
        # ONE contradiction call for internal consistency check
        paras = paragraphs(text)
        contradictions = 0
        if len(paras) >= 2:
            res = call_nlp("contradiction", {
                "premise": paras[0][:400],
                "hypothesis": paras[-1][:400],
            })
            if float(res.get("scores", {}).get("contradiction", 0)) > 0.5:
                contradictions = 1
        tsr_total = max(0, tsr_total - contradictions * 10)
        result["data"] = {
            "tsr_score": tsr_total,
            "dimensions": dim_scores,
            "dimension_ranking": scored,
            "contradictions_found": contradictions,
            "rating": "A" if tsr_total >= 80 else ("B" if tsr_total >= 60 else ("C" if tsr_total >= 40 else "F")),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["theophysics-engine.station"] = COMMON + """
_THEOPHYSICS_LABELS = [
    "axiom foundational premise",
    "theorem derived proposition",
    "physical law empirical",
    "theological claim divine",
    "mathematical relationship equation",
    "philosophical premise assumption",
    "boundary condition constraint",
    "operator definition transformation",
]
""" + EMBED_CLASSIFY_HELPER + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        scored = _embed_classify(text, _THEOPHYSICS_LABELS)
        # ONE contradiction call between theological and scientific claims
        paras = paragraphs(text)
        tensions = []
        if len(paras) >= 2:
            res = call_nlp("contradiction", {
                "premise": paras[0][:400],
                "hypothesis": paras[min(2, len(paras)-1)][:400],
            })
            con = float(res.get("scores", {}).get("contradiction", 0))
            tensions.append({
                "section_a": paras[0][:150],
                "section_b": paras[min(2, len(paras)-1)][:150],
                "contradiction": round(con, 4),
            })
        result["data"] = {
            "statement_type_ranking": scored,
            "dominant_type": scored[0]["label"] if scored else "",
            "tensions": tensions,
            "axiom_count": len([s for s in scored if "axiom" in s["label"] and s["score"] > 0.1]),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["html-article.station"] = COMMON + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        raw = read_input(path)
        text = strip_html(raw) if isinstance(raw, str) and "<" in str(raw) else text_from_input(raw)
        sec_list = sections(text)
        # ONE summarize call on full text (not per-section)
        res = call_nlp("summarize", {"text": text[:4000]})
        summary = res.get("summary", "")
        result["data"] = {
            "article_summary": summary,
            "section_count": len(sec_list),
            "section_headings": [s.get("heading", "") for s in sec_list[:10]],
            "word_count": word_count(text),
            "reading_ease": round(flesch_reading_ease(text[:2000]), 1),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["section-splitter.station"] = COMMON + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        raw = read_input(path)
        text = strip_html(raw) if isinstance(raw, str) and "<" in str(raw) else text_from_input(raw)
        sec_list = sections(text)
        # ONE summarize call on full text
        res = call_nlp("summarize", {"text": text[:4000]})
        global_summary = res.get("summary", "")
        enriched = []
        for s in sec_list[:20]:
            body = s.get("text", "")
            enriched.append({
                "heading": s.get("heading", ""),
                "word_count": word_count(body),
                "preview": body[:200],
            })
        result["data"] = {
            "global_summary": global_summary,
            "sections": enriched,
            "section_count": len(enriched),
            "total_words": sum(s.get("word_count", 0) for s in enriched),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["mda-publication.station"] = COMMON + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        title = data.get("title", path.stem)
        body = data.get("body") or data.get("content") or text_from_input(obj)
        # ONE summarize call
        res = call_nlp("summarize", {"text": body[:4000]})
        abstract = res.get("summary", "")
        pub_md = f"# {title}\\n\\n## Abstract\\n{abstract}\\n\\n## Content\\n{body[:3000]}"
        export_path = EXPORTS / f"{path.stem}_publication.md"
        export_path.write_text(pub_md, encoding="utf-8")
        result["data"] = {
            "publication_path": str(export_path),
            "title": title,
            "abstract": abstract,
            "word_count": word_count(body),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["obsidian-export.station"] = COMMON + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        from datetime import datetime as _dt
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        title = data.get("title", path.stem)
        body = text_from_input(obj)
        # ONE summarize call
        res = call_nlp("summarize", {"text": body[:4000]})
        summary = res.get("summary", "")
        # keyword tags from text (no NER call needed)
        tags = list(dict.fromkeys(
            w.lower() for w in _re.findall(r"\\b[A-Z][a-z]{4,}\\b", body[:2000])
        ))[:8]
        frontmatter = f"---\\ntitle: {title}\\ntags: [{', '.join(tags)}]\\ncreated: {_dt.now():%Y-%m-%d}\\n---\\n\\n"
        note = frontmatter + f"## Summary\\n{summary}\\n\\n## Content\\n{body[:3000]}"
        export_path = EXPORTS / f"{path.stem}_obsidian.md"
        export_path.write_text(note, encoding="utf-8")
        result["data"] = {"obsidian_path": str(export_path), "title": title, "tags": tags, "summary": summary}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["session-handoff-combined.station"] = COMMON + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        handoffs = data.get("handoffs") or ([obj] if isinstance(obj, dict) else [])
        combined = "\\n\\n---\\n\\n".join(text_from_input(h) for h in handoffs) if handoffs else text_from_input(obj)
        # ONE summarize call
        res = call_nlp("summarize", {"text": combined[:4000]})
        summary = res.get("summary", "")
        result["data"] = {
            "combined_summary": summary,
            "handoff_count": len(handoffs),
            "combined_length": len(combined),
            "ready_for_drop": True,
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["youtube-scrape.station"] = COMMON + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        transcript = data.get("transcript") or text_from_input(obj)
        transcript = _re.sub(r"\\[\\d+:\\d+\\]", "", transcript)
        # ONE summarize call on first 4000 chars
        res = call_nlp("summarize", {"text": transcript[:4000]})
        result["data"] = {
            "full_summary": res.get("summary", ""),
            "transcript_length": len(transcript),
            "transcript_preview": transcript[:300],
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["mda-citation-spine.station"] = COMMON + """
_CLAIM_QUESTIONS = [
    "What is the main claim or thesis being argued?",
    "What evidence or citations support this claim?",
]

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "qa_extractor", "qa")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        context = text[:4000]
        claims = []
        for i, q in enumerate(_CLAIM_QUESTIONS):
            res = call_nlp("qa", {"question": q, "context": context})
            answer = res.get("answer", "").strip()
            score = float(res.get("score", 0))
            if answer and score > 0.05:
                claims.append({
                    "claim_id": f"C{i+1:03d}",
                    "text": answer,
                    "question": q,
                    "confidence": round(score, 4),
                })
        result["data"] = {
            "claims": claims,
            "claim_count": len(claims),
            "source_length": len(text),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

# ── FIX CONTRADICTION FIELD NAMES ─────────────────────────────────────────────
REPLACEMENTS["coherence-discoherence.station"] = COMMON + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "contradiction_primary", "contradiction")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        paras = paragraphs(text)[:10]
        pairs = []
        incoherent = []
        for i in range(min(len(paras) - 1, 4)):  # max 4 contradiction calls
            a = paras[i][:400]; b = paras[i+1][:400]
            res = call_nlp("contradiction", {"premise": a, "hypothesis": b})
            scores = res.get("scores", {})
            con = float(scores.get("contradiction", 0))
            ent = float(scores.get("entailment", 0))
            pairs.append({"para_index": i, "contradiction": round(con, 4), "entailment": round(ent, 4), "coherent": con < 0.3})
            if con > 0.5:
                incoherent.append({"para_a": a[:150], "para_b": b[:150], "contradiction_score": round(con, 4)})
        avg = sum(1 - p["contradiction"] for p in pairs) / len(pairs) if pairs else 1.0
        result["data"] = {
            "coherence_score": round(avg, 3),
            "incoherent_transitions": incoherent,
            "paragraphs_checked": len(pairs),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["series-flow-auditor.station"] = COMMON + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "contradiction_primary", "contradiction")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        series = data.get("series") or data.get("documents") or []
        if not series:
            text = text_from_input(obj)
            series = [{"id": str(i), "text": p} for i, p in enumerate(paragraphs(text)[:10])]
        flow_issues = []; transitions = []
        for i in range(min(len(series) - 1, 4)):  # max 4 contradiction calls
            a = series[i].get("text", "")[:400]; b = series[i+1].get("text", "")[:400]
            if not a or not b: continue
            res = call_nlp("contradiction", {"premise": a, "hypothesis": b})
            scores = res.get("scores", {}); con = float(scores.get("contradiction", 0))
            trans = {"from_id": series[i].get("id", i), "to_id": series[i+1].get("id", i+1),
                     "contradiction": round(con, 4), "entailment": round(float(scores.get("entailment", 0)), 4)}
            transitions.append(trans)
            if con > 0.5:
                flow_issues.append({**trans, "severity": "HIGH" if con > 0.7 else "MEDIUM"})
        result["data"] = {
            "transitions": transitions, "flow_issues": flow_issues,
            "issue_count": len(flow_issues), "series_length": len(series),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["apologetic-pipeline.station"] = COMMON + """
_APOL_LABELS = [
    "theological assertion claim",
    "philosophical premise assumption",
    "scriptural reference citation",
    "logical argument inference",
    "counter-argument objection",
    "historical evidence example",
    "conclusion implication",
]
""" + EMBED_CLASSIFY_HELPER + """
def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        scored = _embed_classify(text, _APOL_LABELS)
        paras = paragraphs(text)
        tensions = []
        if len(paras) >= 2:
            res = call_nlp("contradiction", {
                "premise": paras[0][:400],
                "hypothesis": paras[-1][:400],
            })
            con = float(res.get("scores", {}).get("contradiction", 0))
            if con > 0.25:
                tensions.append({
                    "premise_a": paras[0][:200],
                    "premise_b": paras[-1][:200],
                    "contradiction_score": round(con, 4),
                })
        result["data"] = {
            "argument_type_ranking": scored,
            "dominant_type": scored[0]["label"] if scored else "",
            "tensions": tensions,
            "sentence_count": len(sentences(text)),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

# ─────────────────────────────────────────────────────────────────────────────
# Apply
# ─────────────────────────────────────────────────────────────────────────────

def find_section_bounds(lines, start_marker, end_marker):
    start = end = None
    for i, line in enumerate(lines):
        if start is None and start_marker in line:
            for k in range(i, max(i-3, -1), -1):
                if "# ===" in lines[k]:
                    start = k; break
            if start is None: start = i
        if start is not None and end is None and end_marker in line:
            for k in range(i, max(i-3, -1), -1):
                if "# ===" in lines[k]:
                    end = k; break
            if end is None: end = i
            break
    return start, end


errors = []; patched = []

for station_name, new_content in REPLACEMENTS.items():
    pipe_path = STATIONS_DIR / station_name / "pipeline.py"
    if not pipe_path.exists():
        errors.append(f"MISSING: {pipe_path}"); continue

    src = pipe_path.read_text(encoding="utf-8", errors="replace")
    lines = src.splitlines(keepends=True)
    start, end = find_section_bounds(lines, S06_MARKER, S08_MARKER)

    if start is None or end is None:
        errors.append(f"BOUNDS NOT FOUND: {station_name}"); continue

    before = "".join(lines[:start])
    after  = "".join(lines[end:])
    new_src = before + new_content + "\n" + after

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tf:
        tf.write(new_src); tf_path = tf.name
    check = subprocess.run([sys.executable, "-m", "py_compile", tf_path], capture_output=True, text=True)
    os.unlink(tf_path)

    if check.returncode != 0:
        errors.append(f"SYNTAX {station_name}: {check.stderr.strip()[:200]}"); continue

    pipe_path.write_text(new_src, encoding="utf-8")
    patched.append(station_name)
    print(f"  PATCHED: {station_name}")

print(f"\n{'='*50}")
print(f"Patched: {len(patched)}  Errors: {len(errors)}")
for e in errors: print(f"  ! {e}")
