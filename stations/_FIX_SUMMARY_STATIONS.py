"""
Fix v3 — Replace summarize calls (too slow >90s) with QA-based extraction.
One QA call: "What is the main thesis, argument, or key points of this text?"
QA is ~5-15s per call vs 90s+ for summarize.
"""
import sys, subprocess, tempfile, os
from pathlib import Path

STATIONS_DIR = Path(__file__).parent
S06_MARKER = "# 06_NLP_ROUTE  *** STATION-SPECIFIC ***"
S08_MARKER = "# 08_ARTIFACTS"

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

REPLACEMENTS["html-article.station"] = COMMON + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "qa_extractor", "qa")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        raw = read_input(path)
        text = strip_html(raw) if isinstance(raw, str) and "<" in str(raw) else text_from_input(raw)
        sec_list = sections(text)
        res = call_nlp("qa", {"question": "What is the main argument or thesis of this article?", "context": text[:3000]})
        summary = res.get("answer", "")
        result["data"] = {
            "article_summary": summary,
            "summary_confidence": round(float(res.get("score", 0)), 4),
            "section_count": len(sec_list),
            "section_headings": [s.get("heading", "") for s in sec_list[:10]],
            "word_count": word_count(text),
            "reading_ease": round(flesch_reading_ease(text[:2000]), 1),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["section-splitter.station"] = COMMON + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "qa_extractor", "qa")

# ============================================================
# 07_PROCESS  *** STATION-SPECIFIC ***
# ============================================================
def process_one(path, nlp_info, cfg, log):
    result = base_result(path, STATION_ID, STATION_NAME, nlp_info)
    try:
        raw = read_input(path)
        text = strip_html(raw) if isinstance(raw, str) and "<" in str(raw) else text_from_input(raw)
        sec_list = sections(text)
        res = call_nlp("qa", {"question": "What is the main topic covered in this document?", "context": text[:3000]})
        global_topic = res.get("answer", "")
        enriched = []
        for s in sec_list[:20]:
            body = s.get("text", "")
            enriched.append({
                "heading": s.get("heading", ""),
                "word_count": word_count(body),
                "preview": body[:200],
            })
        result["data"] = {
            "document_topic": global_topic,
            "topic_confidence": round(float(res.get("score", 0)), 4),
            "sections": enriched,
            "section_count": len(enriched),
            "total_words": sum(s.get("word_count", 0) for s in enriched),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["mda-publication.station"] = COMMON + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "qa_extractor", "qa")

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
        res = call_nlp("qa", {"question": "What is the central claim or contribution of this publication?", "context": body[:3000]})
        abstract = res.get("answer", "")
        pub_md = f"# {title}\\n\\n## Abstract\\n{abstract}\\n\\n## Content\\n{body[:3000]}"
        export_path = EXPORTS / f"{path.stem}_publication.md"
        export_path.write_text(pub_md, encoding="utf-8")
        result["data"] = {
            "publication_path": str(export_path),
            "title": title,
            "abstract": abstract,
            "abstract_confidence": round(float(res.get("score", 0)), 4),
            "word_count": word_count(body),
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["obsidian-export.station"] = COMMON + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "qa_extractor", "qa")

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
        res = call_nlp("qa", {"question": "What is the main idea or conclusion of this document?", "context": body[:3000]})
        summary = res.get("answer", "")
        # Keyword tags from proper nouns
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

REPLACEMENTS["session-handoff-combined.station"] = COMMON + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "qa_extractor", "qa")

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
        res = call_nlp("qa", {"question": "What decisions were made and what remains open or unresolved?", "context": combined[:3000]})
        summary = res.get("answer", "")
        result["data"] = {
            "combined_summary": summary,
            "summary_confidence": round(float(res.get("score", 0)), 4),
            "handoff_count": len(handoffs),
            "combined_length": len(combined),
            "ready_for_drop": True,
        }
    except Exception as exc:
        result["success"] = False; result["errors"].append(str(exc))
    return result
"""

REPLACEMENTS["youtube-scrape.station"] = COMMON + """\

def choose_nlp(path, cfg):
    return nlp_route(API_BASE, MODELS, cfg, "qa_extractor", "qa")

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
        res = call_nlp("qa", {"question": "What is the main topic and key points discussed in this content?", "context": transcript[:3000]})
        result["data"] = {
            "full_summary": res.get("answer", ""),
            "summary_confidence": round(float(res.get("score", 0)), 4),
            "transcript_length": len(transcript),
            "transcript_preview": transcript[:300],
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
