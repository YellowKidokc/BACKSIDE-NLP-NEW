"""
Fix all broken and phase2_skip stations.
Replaces sections 06+07 (between # 06_NLP_ROUTE and # 08_ARTIFACTS) in each pipeline.py.
"""
import re, sys, json, subprocess
from pathlib import Path

STATIONS_DIR = Path(__file__).parent

# Section boundary markers (exact strings in every pipeline.py)
S06_MARKER = "# 06_NLP_ROUTE  *** STATION-SPECIFIC ***"
S08_MARKER = "# 08_ARTIFACTS"

# ── helpers used in every replacement ────────────────────────────────────────
COMMON_IMPORTS = """\
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

# fmt: off
REPLACEMENTS = {}

# ─────────────────────────────────────────────────────────────────────────────
# HARD FAILURES
# ─────────────────────────────────────────────────────────────────────────────

REPLACEMENTS["fruits-spirit-canon.station"] = COMMON_IMPORTS + """\

_FRUITS = ["love", "joy", "peace", "patience", "kindness", "goodness",
           "faithfulness", "gentleness", "self-control"]

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        para_list = paragraphs(text)[:15]
        fruit_map = {f: [] for f in _FRUITS}
        for para in para_list:
            if len(para.strip()) < 20:
                continue
            res = call_nlp("classify", {"text": para[:500], "labels": _FRUITS})
            for item in res.get("labels", []):
                if item.get("score", 0) > 0.3:
                    fruit_map[item["label"]].append({"text": para[:150], "score": round(item["score"], 4)})
        present = {f: v for f, v in fruit_map.items() if v}
        dominant = max(present, key=lambda f: max(x["score"] for x in present[f])) if present else ""
        result["data"] = {
            "fruits_present": present,
            "fruit_count": len(present),
            "dominant_fruit": dominant,
            "fruits_checked": _FRUITS,
            "paragraphs_analyzed": len([p for p in para_list if len(p.strip()) >= 20]),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["master-equation-canon.station"] = COMMON_IMPORTS + """\

_EQ_QUESTIONS = [
    "What is the master equation described in this text?",
    "What variables does the equation use?",
    "What operators or transformations are defined?",
    "What is the domain of application for this equation?",
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
        equations = []
        for q in _EQ_QUESTIONS:
            res = call_nlp("qa", {"question": q, "context": context})
            answer = res.get("answer", "").strip()
            score = float(res.get("score", 0))
            if answer and score > 0.05:
                equations.append({"question": q, "answer": answer, "confidence": round(score, 4)})
        math_re = _re.compile(r"[A-Za-z]\\s*[=\\+\\-\\*/]\\s*[A-Za-z0-9\\(]")
        raw_eqs = list(dict.fromkeys(math_re.findall(text)))
        result["data"] = {
            "extracted_answers": equations,
            "raw_equation_patterns": raw_eqs[:20],
            "equation_count": len(equations),
            "source_length": len(text),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["operators-canon.station"] = COMMON_IMPORTS + """\

_OPERATOR_LABELS = [
    "logical conjunction", "logical disjunction", "logical negation",
    "implication", "necessity", "possibility", "causal relationship",
    "temporal sequence", "equivalence", "conditional statement",
]

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        sent_list = sentences(text)[:30]
        operator_map = []
        for s in sent_list:
            if len(s) < 15:
                continue
            res = call_nlp("classify", {"text": s, "labels": _OPERATOR_LABELS})
            top = res.get("labels", [{}])[0]
            if top.get("score", 0) > 0.25:
                operator_map.append({"sentence": s, "operator_type": top.get("label", ""), "confidence": round(top.get("score", 0), 4)})
        type_counts = {}
        for o in operator_map:
            type_counts[o["operator_type"]] = type_counts.get(o["operator_type"], 0) + 1
        result["data"] = {
            "operators_found": operator_map,
            "operator_count": len(operator_map),
            "type_distribution": type_counts,
            "dominant_operator": max(type_counts, key=type_counts.get) if type_counts else "",
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["trinity-canon.station"] = COMMON_IMPORTS + """\

_TRINITY_LABELS = [
    "the Father", "the Son / Jesus Christ", "the Holy Spirit",
    "Triune relationship", "divine nature", "incarnation",
    "perichoresis", "economic Trinity", "immanent Trinity",
]

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        sent_list = sentences(text)[:40]
        person_map = {label: [] for label in _TRINITY_LABELS}
        for s in sent_list:
            if len(s) < 15:
                continue
            res = call_nlp("classify", {"text": s, "labels": _TRINITY_LABELS})
            top = res.get("labels", [{}])[0]
            if top.get("score", 0) > 0.25:
                person_map[top["label"]].append({"text": s, "confidence": round(top.get("score", 0), 4)})
        non_empty = {k: v for k, v in person_map.items() if v}
        result["data"] = {
            "person_map": non_empty,
            "statement_count": sum(len(v) for v in non_empty.values()),
            "persons_addressed": list(non_empty.keys()),
            "dominant_person": max(non_empty, key=lambda k: len(non_empty[k])) if non_empty else "",
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["hdbscan-cluster.station"] = COMMON_IMPORTS + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        para_list = [p for p in paragraphs(text) if len(p) > 30][:40]
        chunks = [p[:500] for p in para_list]
        if not chunks:
            chunks = [text[:500]]
        res = call_nlp("embed", {"texts": chunks})
        vecs = res.get("embeddings", [])
        clusters = []
        assigned = set()
        for i in range(len(vecs)):
            if i in assigned:
                continue
            cluster = [i]; assigned.add(i)
            for j in range(i + 1, len(vecs)):
                if j not in assigned and cosine(vecs[i], vecs[j]) > 0.6:
                    cluster.append(j); assigned.add(j)
            clusters.append({"cluster_id": len(clusters), "size": len(cluster),
                              "members": [{"idx": idx, "preview": chunks[idx][:80]} for idx in cluster],
                              "centroid_preview": chunks[cluster[0]][:80]})
        result["data"] = {
            "clusters": clusters, "cluster_count": len(clusters),
            "chunk_count": len(chunks), "vector_dim": len(vecs[0]) if vecs else 0,
            "ready_for_hdbscan": True,
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["apologetic-pipeline.station"] = COMMON_IMPORTS + """\

_APOLOGETIC_LABELS = [
    "theological claim", "philosophical premise", "scriptural reference",
    "logical argument", "counter-argument", "historical evidence", "conclusion",
]

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "contradiction_primary", "contradiction")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        sent_list = sentences(text)[:40]
        classified = []
        for s in sent_list:
            if len(s) < 15:
                continue
            res = call_nlp("classify", {"text": s, "labels": _APOLOGETIC_LABELS})
            top = res.get("labels", [{}])[0]
            classified.append({"sentence": s, "argument_type": top.get("label", ""), "confidence": round(top.get("score", 0), 4)})
        premises = [c for c in classified if c["argument_type"] in ("theological claim", "philosophical premise", "scriptural reference")]
        tensions = []
        for i in range(len(premises)):
            for j in range(i + 1, min(i + 5, len(premises))):
                res = call_nlp("contradiction", {"text_a": premises[i]["sentence"], "text_b": premises[j]["sentence"]})
                con = float(res.get("scores", {}).get("contradiction", 0))
                if con > 0.4:
                    tensions.append({"premise_a": premises[i]["sentence"], "premise_b": premises[j]["sentence"], "contradiction_score": round(con, 4)})
        result["data"] = {
            "classified_sentences": classified, "premises_found": len(premises),
            "tensions": tensions, "argument_types": list(dict.fromkeys(c["argument_type"] for c in classified)),
            "sentence_count": len(classified),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["vault-rater-tsr100.station"] = COMMON_IMPORTS + """\

_TSR_DIMENSIONS = ["factual accuracy", "theological soundness", "logical consistency",
                   "source reliability", "argument strength", "doctrinal alignment"]

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "contradiction_primary", "contradiction")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        dim_scores = {}
        for dim in _TSR_DIMENSIONS:
            res = call_nlp("classify", {"text": text[:2000], "labels": [f"high {dim}", f"medium {dim}", f"low {dim}"]})
            top = res.get("labels", [{}])[0]
            label = top.get("label", "")
            score = 100 if "high" in label else (50 if "medium" in label else 20)
            dim_scores[dim] = {"label": label, "score": score}
        tsr_total = round(sum(d["score"] for d in dim_scores.values()) / len(dim_scores))
        sent_list = sentences(text)[:20]
        contradictions = 0
        for i in range(min(len(sent_list) - 1, 10)):
            res = call_nlp("contradiction", {"text_a": sent_list[i][:300], "text_b": sent_list[i + 1][:300]})
            if float(res.get("scores", {}).get("contradiction", 0)) > 0.5:
                contradictions += 1
        tsr_total = max(0, tsr_total - contradictions * 5)
        result["data"] = {
            "tsr_score": tsr_total,
            "dimensions": dim_scores,
            "contradictions_found": contradictions,
            "rating": "A" if tsr_total >= 80 else ("B" if tsr_total >= 60 else ("C" if tsr_total >= 40 else "F")),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["youtube-fetch.station"] = COMMON_IMPORTS + """\

_YT_ID_RE = _re.compile(r"(?:v=|youtu\\.be/)([A-Za-z0-9_\\-]{11})")

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "summarizer", "summarize")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        video_ids = list(dict.fromkeys(_YT_ID_RE.findall(text)))
        urls = [f"https://www.youtube.com/watch?v={vid}" for vid in video_ids]
        sum_res = call_nlp("summarize", {"text": text[:4000]}) if len(text) > 200 else {"summary": ""}
        result["data"] = {
            "video_ids": video_ids, "video_urls": urls,
            "input_summary": sum_res.get("summary", ""),
            "video_count": len(video_ids),
            "note": "Install youtube-transcript-api for full transcript fetch",
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["postgres-sync.station"] = COMMON_IMPORTS + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        text = text_from_input(obj)
        res = call_nlp("embed", {"texts": [text[:1000]]})
        vec = res.get("embeddings", [None])[0]
        db_record = {
            "source_file": path.name,
            "content_preview": text[:500],
            "embedding": vec,
            "metadata": {k: v for k, v in data.items() if isinstance(v, (str, int, float, bool))},
            "sync_ready": True,
        }
        result["data"] = {"db_record": db_record, "vector_dim": len(vec) if vec else 0, "sync_ready": True}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["7q-classifier.station"] = COMMON_IMPORTS + """\

_SEVEN_Q = ["Who is involved", "What is the claim or event", "When did this occur",
            "Where did this happen", "Why does this matter", "How was this determined",
            "So what is the implication"]

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        res = call_nlp("classify", {"text": text[:2000], "labels": _SEVEN_Q})
        labels = res.get("labels", [])
        result["data"] = {
            "seven_q_scores": labels,
            "top_question": labels[0]["label"] if labels else "",
            "top_score": round(labels[0]["score"], 4) if labels else 0,
            "text_preview": text[:200],
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

# ─────────────────────────────────────────────────────────────────────────────
# PHASE2_SKIP STATIONS — replace only process_one block (keep choose_nlp)
# These share the same section 06, so we replace full 06+07 for consistency.
# ─────────────────────────────────────────────────────────────────────────────

REPLACEMENTS["ai-research-agents.station"] = COMMON_IMPORTS + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        chunks = [text[i:i+500] for i in range(0, min(len(text), 3000), 500)]
        res = call_nlp("embed", {"texts": chunks})
        vecs = res.get("embeddings", [])
        ner_res = call_nlp("ner", {"text": text[:2000]})
        entities = ner_res.get("entities", [])
        mean_vec = [sum(v[i] for v in vecs) / len(vecs) for i in range(len(vecs[0]))] if vecs else []
        result["data"] = {
            "embedding_count": len(vecs),
            "mean_vector_dim": len(mean_vec),
            "entities": entities[:20],
            "entity_count": len(entities),
            "source_length": len(text),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["axioms.station"] = COMMON_IMPORTS + """\

_AXIOM_QUESTIONS = [
    "What is the fundamental premise of this text?",
    "What assumptions does this argument rely on?",
    "What is stated as self-evidently true?",
    "What foundational claim underlies this reasoning?",
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
        axioms = []
        seen = set()
        for q in _AXIOM_QUESTIONS:
            res = call_nlp("qa", {"question": q, "context": context})
            answer = res.get("answer", "").strip()
            score = float(res.get("score", 0))
            if answer and score > 0.1 and answer not in seen:
                seen.add(answer)
                axioms.append({"text": answer, "question": q, "confidence": round(score, 4)})
        result["data"] = {"axioms": axioms, "axiom_count": len(axioms), "source_length": len(text)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["brain-map.station"] = COMMON_IMPORTS + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        sec_list = sections(text) or [{"heading": "Document", "text": text}]
        texts = [s["text"][:500] for s in sec_list if s.get("text")]
        if not texts:
            texts = [text[:500]]
        res = call_nlp("embed", {"texts": texts})
        vecs = res.get("embeddings", [])
        edges = []
        for i in range(len(vecs)):
            for j in range(i + 1, len(vecs)):
                sim = cosine(vecs[i], vecs[j])
                if sim > 0.4:
                    edges.append({"source": sec_list[i].get("heading", str(i)),
                                  "target": sec_list[j].get("heading", str(j)),
                                  "weight": round(sim, 4)})
        result["data"] = {
            "nodes": [{"id": s.get("heading", ""), "preview": s.get("text", "")[:100]} for s in sec_list],
            "edges": edges, "node_count": len(sec_list), "edge_count": len(edges),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["coherence-discoherence.station"] = COMMON_IMPORTS + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "contradiction_primary", "contradiction")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        para_list = paragraphs(text)[:20]
        coherence_pairs = []; incoherent = []
        for i in range(len(para_list) - 1):
            res = call_nlp("contradiction", {"text_a": para_list[i][:500], "text_b": para_list[i+1][:500]})
            scores = res.get("scores", {})
            con = float(scores.get("contradiction", 0))
            ent = float(scores.get("entailment", 0))
            coherence_pairs.append({"para_index": i, "contradiction": round(con, 4), "entailment": round(ent, 4), "coherent": con < 0.3})
            if con > 0.5:
                incoherent.append({"para_a": para_list[i][:200], "para_b": para_list[i+1][:200], "contradiction_score": round(con, 4)})
        avg = sum(1 - p["contradiction"] for p in coherence_pairs) / len(coherence_pairs) if coherence_pairs else 1.0
        result["data"] = {
            "coherence_score": round(avg, 3), "incoherent_transitions": incoherent,
            "paragraphs_checked": len(coherence_pairs), "pairs_analyzed": len(coherence_pairs),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["file-intelligence.station"] = COMMON_IMPORTS + """\

_FILE_TYPE_LABELS = ["research paper", "sermon notes", "book draft", "correspondence",
                     "spreadsheet data", "technical documentation", "theological essay",
                     "meeting notes", "media transcript", "reference material"]

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        cls_res = call_nlp("classify", {"text": text[:2000], "labels": _FILE_TYPE_LABELS})
        sum_res = call_nlp("summarize", {"text": text[:3000]})
        ner_res = call_nlp("ner", {"text": text[:2000]})
        top_type = (cls_res.get("labels", [{}])[0]).get("label", "unknown")
        entities = [e["text"] for e in ner_res.get("entities", [])[:5]]
        slug = _re.sub(r"[^a-z0-9]+", "-", top_type.lower()).strip("-")
        result["data"] = {
            "file_type": top_type,
            "confidence": round((cls_res.get("labels", [{}])[0]).get("score", 0), 4),
            "summary": sum_res.get("summary", ""),
            "key_entities": entities,
            "rename_suggestion": f"{slug}_{path.stem[:30]}{path.suffix}",
            "word_count": word_count(text),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["fis.station"] = COMMON_IMPORTS + """\

_FIS_LABELS = ["theological", "scientific", "philosophical", "administrative",
               "media", "technical", "personal", "reference", "draft", "archive"]

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "zero_shot", "classify")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        cls_res = call_nlp("classify", {"text": text[:2000], "labels": _FIS_LABELS})
        sum_res = call_nlp("summarize", {"text": text[:3000]})
        ner_res = call_nlp("ner", {"text": text[:2000]})
        top = (cls_res.get("labels", [{}])[0])
        tags = [e["text"] for e in ner_res.get("entities", [])[:8]]
        rename = _re.sub(r"[^a-z0-9]+", "-", top.get("label", "file").lower()) + f"_{path.stem[:20]}{path.suffix}"
        result["data"] = {
            "fcard": {
                "filename": path.name, "category": top.get("label", ""),
                "confidence": round(top.get("score", 0), 4),
                "summary": sum_res.get("summary", ""), "tags": tags,
                "word_count": word_count(text), "rename_preview": rename,
            }
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["graph-linker.station"] = COMMON_IMPORTS + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        nodes = data.get("sections") or data.get("claims") or []
        texts = [n.get("text", n.get("heading", "")) for n in nodes if n.get("text") or n.get("heading")]
        if not texts:
            text = text_from_input(obj)
            sec_list = sections(text)
            texts = [s["text"][:400] for s in sec_list]
            nodes = sec_list
        res = call_nlp("embed", {"texts": [t[:500] for t in texts]})
        vecs = res.get("embeddings", [])
        edges = []
        for i in range(len(vecs)):
            for j in range(i + 1, len(vecs)):
                sim = cosine(vecs[i], vecs[j])
                if sim > 0.35:
                    edges.append({"source_idx": i, "target_idx": j,
                                  "source_label": nodes[i].get("heading", str(i)) if isinstance(nodes[i], dict) else str(i),
                                  "target_label": nodes[j].get("heading", str(j)) if isinstance(nodes[j], dict) else str(j),
                                  "weight": round(sim, 4)})
        edges.sort(key=lambda e: e["weight"], reverse=True)
        result["data"] = {"nodes": nodes, "edges": edges[:100], "edge_count": len(edges), "node_count": len(nodes)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["html-article.station"] = COMMON_IMPORTS + """\

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
        summaries = []
        for s in sec_list[:10]:
            if len(s.get("text", "")) > 100:
                res = call_nlp("summarize", {"text": s["text"][:3000]})
                summaries.append({"heading": s.get("heading", ""), "summary": res.get("summary", "")})
        full_res = call_nlp("summarize", {"text": text[:5000]})
        result["data"] = {
            "section_summaries": summaries, "article_summary": full_res.get("summary", ""),
            "section_count": len(sec_list), "word_count": word_count(text),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["link-research.station"] = COMMON_IMPORTS + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        links = data.get("anchors", data.get("urls", data.get("plain_urls", [])))
        texts = []
        for l in links[:50]:
            t = l.get("anchor_text", "") if isinstance(l, dict) else str(l)
            if len(t) > 3:
                texts.append(t)
        if not texts:
            texts = [text_from_input(obj)[:500]]
        res = call_nlp("embed", {"texts": texts})
        vecs = res.get("embeddings", [])
        result["data"] = {
            "link_count": len(links), "embedded_count": len(vecs),
            "link_index": [{"text": texts[i], "vector_idx": i} for i in range(len(texts))],
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["mda-publication.station"] = COMMON_IMPORTS + """\

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
        sum_res = call_nlp("summarize", {"text": body[:5000]})
        abstract = sum_res.get("summary", "")
        pub_md = f"# {title}\\n\\n## Abstract\\n{abstract}\\n\\n## Content\\n{body}"
        export_path = EXPORTS / f"{path.stem}_publication.md"
        export_path.write_text(pub_md, encoding="utf-8")
        result["data"] = {
            "publication_path": str(export_path), "title": title,
            "abstract": abstract, "word_count": word_count(body),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["metadata-extractor.station"] = COMMON_IMPORTS + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "ner_enhanced", "ner")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        ner_res = call_nlp("ner", {"text": text[:4000]})
        entities = ner_res.get("entities", [])
        persons = list(dict.fromkeys(e["text"] for e in entities if e.get("label", "") in ("PER", "PERSON")))
        orgs = list(dict.fromkeys(e["text"] for e in entities if e.get("label", "") in ("ORG", "ORGANIZATION")))
        dates = list(dict.fromkeys(e["text"] for e in entities if e.get("label", "") in ("DATE", "TIME")))
        header = text[:500]
        title_line = next((l.strip() for l in header.splitlines() if len(l.strip()) > 10 and not l.startswith("###")), path.stem)
        result["data"] = {
            "metadata": {
                "title": title_line, "authors": persons[:5],
                "organizations": orgs[:3], "dates": dates[:3], "entities": entities[:20],
            },
            "yaml_candidate": {"title": title_line, "authors": persons[:5], "dates": dates[:3]},
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["obsidian-export.station"] = COMMON_IMPORTS + """\

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
        sum_res = call_nlp("summarize", {"text": body[:4000]})
        summary = sum_res.get("summary", "")
        ner_res = call_nlp("ner", {"text": body[:2000]})
        tags = list(dict.fromkeys(e["text"].replace(" ", "_") for e in ner_res.get("entities", [])[:8]))
        frontmatter = f"---\\ntitle: {title}\\ntags: [{', '.join(tags)}]\\ncreated: {_dt.now():%Y-%m-%d}\\n---\\n\\n"
        note = frontmatter + f"## Summary\\n{summary}\\n\\n## Content\\n{body}"
        export_path = EXPORTS / f"{path.stem}_obsidian.md"
        export_path.write_text(note, encoding="utf-8")
        result["data"] = {"obsidian_path": str(export_path), "title": title, "tags": tags, "summary": summary}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["open-brain-map.station"] = COMMON_IMPORTS + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "embeddings_fast", "embed")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        obj = read_input(path)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        existing_nodes = data.get("nodes", [])
        text = text_from_input(obj)
        new_sections = sections(text)
        all_texts = []
        for n in existing_nodes:
            t = n.get("text_preview", "") or n.get("text", "") if isinstance(n, dict) else ""
            if len(t) > 20: all_texts.append(t)
        for s in new_sections:
            t = s.get("text", "")[:400]
            if len(t) > 20: all_texts.append(t)
        all_texts = all_texts[:30] or [text[:500]]
        res = call_nlp("embed", {"texts": all_texts})
        vecs = res.get("embeddings", [])
        edges = []
        for i in range(len(vecs)):
            for j in range(i + 1, len(vecs)):
                sim = cosine(vecs[i], vecs[j])
                if sim > 0.45:
                    edges.append({"source": i, "target": j, "weight": round(sim, 4)})
        result["data"] = {
            "node_count": len(all_texts), "edge_count": len(edges),
            "edges": edges[:150],
            "nodes": [{"id": i, "preview": all_texts[i][:80]} for i in range(len(all_texts))],
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["section-splitter.station"] = COMMON_IMPORTS + """\

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
        enriched = []
        for s in sec_list[:15]:
            body = s.get("text", "")
            if len(body) > 100:
                res = call_nlp("summarize", {"text": body[:2000]})
                s["summary"] = res.get("summary", "")
            s["word_count"] = word_count(body)
            enriched.append(s)
        result["data"] = {
            "sections": enriched, "section_count": len(enriched),
            "total_words": sum(s.get("word_count", 0) for s in enriched),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["series-flow-auditor.station"] = COMMON_IMPORTS + """\

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
            series = [{"id": str(i), "text": p} for i, p in enumerate(paragraphs(text)[:20])]
        flow_issues = []; transitions = []
        for i in range(len(series) - 1):
            a = series[i].get("text", "")[:500]; b = series[i+1].get("text", "")[:500]
            if not a or not b: continue
            res = call_nlp("contradiction", {"text_a": a, "text_b": b})
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

REPLACEMENTS["session-handoff-combined.station"] = COMMON_IMPORTS + """\

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
        combined_text = "\\n\\n---\\n\\n".join(text_from_input(h) for h in handoffs) if handoffs else text_from_input(obj)
        res = call_nlp("summarize", {"text": combined_text[:5000]})
        summary = res.get("summary", "")
        result["data"] = {
            "combined_summary": summary, "handoff_count": len(handoffs),
            "combined_length": len(combined_text), "ready_for_drop": True,
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["theophysics-engine.station"] = COMMON_IMPORTS + """\

_THEOPHYSICS_LABELS = [
    "axiom", "theorem", "operator definition", "physical law", "theological claim",
    "mathematical relationship", "philosophical premise", "boundary condition",
]

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "contradiction_primary", "contradiction")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        sent_list = sentences(text)[:30]
        classified = []
        for s in sent_list:
            if len(s) < 15: continue
            res = call_nlp("classify", {"text": s, "labels": _THEOPHYSICS_LABELS})
            top = res.get("labels", [{}])[0]
            classified.append({"text": s, "type": top.get("label", ""), "confidence": round(top.get("score", 0), 4)})
        axioms = [c for c in classified if c["type"] == "axiom"]
        tensions = []
        for i in range(len(axioms)):
            for j in range(i + 1, len(axioms)):
                res = call_nlp("contradiction", {"text_a": axioms[i]["text"], "text_b": axioms[j]["text"]})
                con = float(res.get("scores", {}).get("contradiction", 0))
                if con > 0.4:
                    tensions.append({"axiom_a": axioms[i]["text"], "axiom_b": axioms[j]["text"], "contradiction": round(con, 4)})
        result["data"] = {"classified": classified, "axioms": axioms, "tensions": tensions, "axiom_count": len(axioms)}
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["youtube-scrape.station"] = COMMON_IMPORTS + """\

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
        chunks = [transcript[i:i+3000] for i in range(0, min(len(transcript), 12000), 3000)]
        summaries = []
        for i, chunk in enumerate(chunks):
            res = call_nlp("summarize", {"text": chunk})
            summaries.append({"chunk": i + 1, "summary": res.get("summary", "")})
        combined = " ".join(s["summary"] for s in summaries)
        full_res = call_nlp("summarize", {"text": combined[:4000]}) if combined else {"summary": ""}
        result["data"] = {
            "chunk_summaries": summaries, "full_summary": full_res.get("summary", ""),
            "transcript_length": len(transcript), "chunks_processed": len(chunks),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

# fmt: on

REPLACEMENTS["mda-citation-spine.station"] = COMMON_IMPORTS + """\

_CLAIM_LABELS = ["theological assertion", "philosophical claim", "empirical statement",
                 "scriptural citation", "historical claim", "mathematical statement", "conjecture"]

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "qa_extractor", "qa")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        text = text_from_input(read_input(path))
        sent_list = sentences(text)[:40]
        claims = []
        for i, s in enumerate(sent_list):
            if len(s) < 15:
                continue
            res = call_nlp("classify", {"text": s, "labels": _CLAIM_LABELS})
            top = res.get("labels", [{}])[0]
            conf = float(top.get("score", 0))
            if conf > 0.25:
                ner_res = call_nlp("ner", {"text": s})
                entities = [e["text"] for e in ner_res.get("entities", [])[:3]]
                claims.append({
                    "claim_id": f"C{i+1:03d}", "text": s,
                    "claim_type": top.get("label", ""), "confidence": round(conf, 4),
                    "entities": entities,
                })
        result["data"] = {
            "claims": claims, "claim_count": len(claims),
            "claim_types": list(dict.fromkeys(c["claim_type"] for c in claims)),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

# ─────────────────────────────────────────────────────────────────────────────
# Apply replacements
# ─────────────────────────────────────────────────────────────────────────────

def find_section_bounds(lines, start_marker, end_marker):
    """Return (start_line_idx, end_line_idx) inclusive/exclusive."""
    start = end = None
    for i, line in enumerate(lines):
        if start is None and start_marker in line:
            # Find the enclosing ===... line above
            for k in range(i, max(i-3, -1), -1):
                if "# ===" in lines[k]:
                    start = k
                    break
            if start is None:
                start = i
        if start is not None and end is None and end_marker in line:
            for k in range(i, max(i-3, -1), -1):
                if "# ===" in lines[k]:
                    end = k
                    break
            if end is None:
                end = i
            break
    return start, end


errors = []
patched = []

for station_name, new_content in REPLACEMENTS.items():
    pipe_path = STATIONS_DIR / station_name / "pipeline.py"
    if not pipe_path.exists():
        errors.append(f"MISSING: {pipe_path}")
        continue

    src = pipe_path.read_text(encoding="utf-8", errors="replace")
    lines = src.splitlines(keepends=True)

    start, end = find_section_bounds(lines, S06_MARKER, S08_MARKER)
    if start is None or end is None:
        errors.append(f"BOUNDS NOT FOUND: {station_name} (start={start}, end={end})")
        continue

    before = "".join(lines[:start])
    after  = "".join(lines[end:])
    new_src = before + new_content + "\n" + after

    # Syntax check before writing
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tf:
        tf.write(new_src)
        tf_path = tf.name
    check = subprocess.run([sys.executable, "-m", "py_compile", tf_path], capture_output=True, text=True)
    os.unlink(tf_path)

    if check.returncode != 0:
        errors.append(f"SYNTAX ERROR in {station_name}: {check.stderr.strip()[:200]}")
        continue

    pipe_path.write_text(new_src, encoding="utf-8")
    patched.append(station_name)
    print(f"  PATCHED: {station_name}")

print(f"\n{'='*50}")
print(f"Patched: {len(patched)}")
print(f"Errors:  {len(errors)}")
for e in errors:
    print(f"  ! {e}")
