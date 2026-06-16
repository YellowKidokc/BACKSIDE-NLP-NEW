"""
pipeline_combined.py - Unified Session Handoff Pipeline
========================================================
Stage 1: Ollama (qwen2.5:7b) reads raw chat -> produces structured Layer 1/2/3 summary
Stage 2: Distribution - mirrors, vectorizes, Postgres upserts, archives

Replaces both:
  - session-handoff-drop/pipeline.py  (regex extraction, no LLM)
  - ollama/ollama_session_handoff.py  (Ollama summarizer, limited distribution)

Usage:
  python pipeline_combined.py                  # process DROP_HERE
  python pipeline_combined.py <file_or_dir>    # process specific file or folder
  python pipeline_combined.py --no-ollama      # skip Ollama, use regex fallback only
"""
from __future__ import annotations

import json
import logging
import math
import os
import re
import shutil
import sys
from datetime import datetime
from html import unescape
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from uuid import NAMESPACE_URL, uuid5

HERE = Path(__file__).resolve().parent
ROOT = Path(r"\\dlowenas\brain")
LOG_DIR = ROOT / "_LOGS"
POSTGRES_TOOL_DIR = Path(r"D:\brain\07_POSTGRES")
if str(POSTGRES_TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(POSTGRES_TOOL_DIR))

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ── PATHS ──────────────────────────────────────────────────────────────
DROP_DIR     = ROOT / "session-handoff-drop" / "DROP_HERE"
OUTPUT_DIR   = ROOT / "session-handoff-drop" / "OUTPUT"
ARCHIVE_DIR  = ROOT / "session-handoff-drop" / "ARCHIVE"

MIRROR_DIRS_CONFIG = [
    ("vault",      Path(r"O:\_Theophysics_v3\00_SYSTEM\04_SESSION_LOGS")),
    ("history",    Path(r"Z:\Vault\AI-Chats History\Theophysics-Codex\Session-Handoffs")),
    ("knowledge",  ROOT / "knowledge" / "Session-Handoffs"),
    ("NAS",        Path(r"\\192.168.1.177\Desktop\Cannon")),
]
FULL_CONVERSATION_DIR = Path(r"Z:\Vault\AI-Chats History\full conversation")

# Ollama config
OLLAMA_URL     = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL   = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT", "180"))

# Embedding config
INFINITY_URL       = "http://192.168.1.177:7997"
QDRANT_URL         = "http://192.168.1.177:6333"
QDRANT_COLLECTION  = "session_handoffs"
EMBED_MODEL        = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_DISTANCE    = "Cosine"

# Postgres DDL
SESSION_HANDOFFS_DDL = """
CREATE TABLE IF NOT EXISTS session_handoffs (
    id SERIAL PRIMARY KEY,
    session_id TEXT UNIQUE,
    session_date DATE,
    ai_partner TEXT,
    source_file TEXT,
    manifest_json JSONB,
    summary_markdown TEXT,
    history_dir TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_session_handoffs_session_date ON session_handoffs(session_date);
CREATE INDEX IF NOT EXISTS idx_session_handoffs_ai_partner ON session_handoffs(ai_partner);
"""

TEXT_EXTENSIONS = {".txt", ".md", ".html", ".htm"}

JUNK_SIGNATURES = [
    "press any key to continue", "nothing to do", "rc=0",
    "done (rc=", "0 candidate files",
]
JUNK_MAX_SIZE = 2048


# ── LOGGING ────────────────────────────────────────────────────────────

def _setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    logfile = LOG_DIR / f"session_handoff_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger("session-handoff-combined")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


# ── OLLAMA (Stage 1) ──────────────────────────────────────────────────

OLLAMA_HANDOFF_PROMPT = r"""You are a session handoff summarizer for the Theophysics project.

You are reading a raw AI chat session transcript. Produce a STRUCTURED handoff summary.

Output EXACTLY this format (markdown). Every section must be present even if empty. Use bullet points (- ) for items:

## Layer 1 - Session Manifest
- path/to/file - description of what was created or changed
- another/path - what happened to it

## Layer 2 - Decisions And Results
- DECIDED: [what] - [why]
- RESULT: [what was verified or confirmed]

## Layer 3 - Open Threads
- TODO: [what] - [context and next action]
- BLOCKED: [what] - [why it is stuck]

## Session Metadata
- AI Partner: [which AI - Opus, Sonnet, Codex, Gemini, GPT, Haiku, etc.]
- Date: [YYYY-MM-DD if visible in transcript]
- Summary: [2-3 sentence overview]

RULES:
- Be specific with file paths, URLs, endpoints, repos.
- Decisions are things LOCKED, not discussed.
- Open threads are things the NEXT session needs to act on.
- Do NOT include raw conversation fragments. Summarize.
- Keep under 1000 words. Dense, not long.

SESSION TRANSCRIPT:
{{INPUT}}"""


def _ollama_available() -> bool:
    if not HAS_REQUESTS:
        return False
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        return r.ok
    except Exception:
        return False


def _call_ollama(text: str, logger: logging.Logger) -> str:
    if not HAS_REQUESTS:
        logger.error("requests library not installed")
        return ""
    if len(text) > 24000:
        text = text[:8000] + "\n\n[...middle truncated...]\n\n" + text[-16000:]
    prompt = OLLAMA_HANDOFF_PROMPT.replace("{{INPUT}}", text)
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL, "prompt": prompt, "stream": False,
            "options": {"num_predict": 2048, "temperature": 0.3},
        }, timeout=OLLAMA_TIMEOUT)
        if r.ok:
            resp = r.json().get("response", "")
            logger.info(f"Ollama returned {len(resp)} chars")
            return resp
        else:
            logger.error(f"Ollama HTTP {r.status_code}: {r.text[:200]}")
            return ""
    except requests.exceptions.ConnectionError:
        logger.error("Ollama not running at localhost:11434")
        return ""
    except requests.exceptions.Timeout:
        logger.error(f"Ollama timed out after {OLLAMA_TIMEOUT}s")
        return ""
    except Exception as e:
        logger.error(f"Ollama error: {e}")
        return ""


# ── TEXT READING ───────────────────────────────────────────────────────

def _read_text(path: Path) -> str:
    if path.suffix.lower() in {".html", ".htm"}:
        raw = path.read_text(encoding="utf-8", errors="replace").replace("\x00", "")
        raw = re.sub(r"(?is)<script.*?>.*?</script>", " ", raw)
        raw = re.sub(r"(?is)<style.*?>.*?</style>", " ", raw)
        raw = re.sub(r"(?s)<[^>]+>", "\n", raw)
        return unescape(raw)
    try:
        return path.read_text(encoding="utf-8").replace("\x00", "")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="replace").replace("\x00", "")


def _normalize_lines(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return [line.strip() for line in text.split("\n") if line.strip()]


def _is_junk_input(path: Path) -> str | None:
    if path.stat().st_size < JUNK_MAX_SIZE:
        try:
            text = path.read_text(encoding="utf-8", errors="replace").lower()
        except Exception:
            return "unreadable file under 2KB"
        hits = [sig for sig in JUNK_SIGNATURES if sig in text]
        if hits:
            return f"junk signatures: {', '.join(hits)}"
    return None


# ── EXTRACTION ─────────────────────────────────────────────────────────

def _extract_layer(lines: list[str], layer_names: list[str]) -> list[str]:
    start = None
    for i, line in enumerate(lines):
        lower = line.lower().lstrip("#").strip()
        if any(name in lower for name in layer_names):
            start = i + 1
            break
    if start is None:
        return []
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## ") and j > start:
            end = j
            break
    return lines[start:end]


def _extract_metadata(lines: list[str]) -> dict:
    meta_lines = _extract_layer(lines, ["session metadata"])
    result = {}
    for line in meta_lines:
        lower = line.lower().lstrip("- ").strip()
        if lower.startswith("ai partner:"):
            result["ai_partner"] = line.split(":", 1)[1].strip().strip("*")
        elif lower.startswith("date:"):
            m = re.search(r"(\d{4}-\d{2}-\d{2})", line)
            if m:
                result["session_date"] = m.group(1)
        elif lower.startswith("summary:"):
            result["summary"] = line.split(":", 1)[1].strip()
    return result


def _collect_bullets(lines: list[str]) -> list[str]:
    bullets = []
    for line in lines:
        if re.match(r"^[-*]\s+", line):
            bullets.append(re.sub(r"^[-*]\s+", "", line).strip())
        elif re.match(r"^\d+\.\s+", line):
            bullets.append(re.sub(r"^\d+\.\s+", "", line).strip())
        elif "\u2014" in line or " - " in line:
            bullets.append(line.strip())
    return bullets


def _detect_ai_partner(text: str, default: str = "Unknown") -> str:
    lower = text[:2000].lower()
    for name, pat in [("Opus","opus"),("Sonnet","sonnet"),("Codex","codex"),
                      ("Codex","claude code"),("Gemini","gemini"),("Gemini","jim"),
                      ("Haiku","haiku"),("GPT","gpt"),("GPT","chatgpt")]:
        if pat in lower:
            return name
    return default


def _extract_date(text: str) -> str:
    matches = re.findall(r"\b(20\d{2}-\d{2}-\d{2})\b", text)
    return matches[0] if matches else datetime.now().strftime("%Y-%m-%d")


# ── FREEFORM FALLBACK ─────────────────────────────────────────────────

_RE_FILE_PATH = re.compile(r"[A-Za-z]:\\[^\s,;\"'<>|]+", re.MULTILINE)
_MANIFEST_VERBS = re.compile(
    r"\b(?:created?|built|wrote|generated|installed|downloaded|deployed|"
    r"copied|moved|saved|pushed|cloned|configured|fixed|patched|"
    r"refactored|migrated|uploaded|exported)\b", re.IGNORECASE)
_DECISION_PATTERNS = re.compile(
    r"\b(?:decided|locked|chose|confirmed|going with|settled on|"
    r"we'll use|switching to|final call|verdict|consensus)\b", re.IGNORECASE)
_THREAD_PATTERNS = re.compile(
    r"\b(?:TODO|still need|next session|pending|open item|remaining|"
    r"missing|not yet|needs? to be|should be|follow[- ]?up|pick up|"
    r"unfinished|blocked on|waiting for|next step|future work)\b", re.IGNORECASE)


def _freeform_manifest(lines: list[str]) -> list[str]:
    items, seen = [], set()
    full = "\n".join(lines)
    for m in _RE_FILE_PATH.finditer(full):
        p = m.group(0).rstrip(".,;:)")
        if p not in seen: seen.add(p); items.append(p)
    for line in lines:
        if _MANIFEST_VERBS.search(line) and len(line) > 15:
            k = line[:60].lower()
            if k not in seen: seen.add(k); items.append(line)
    return items[:50]


def _freeform_decisions(lines: list[str]) -> list[str]:
    items, seen = [], set()
    for line in lines:
        if _DECISION_PATTERNS.search(line) and len(line) > 15:
            k = line[:60].lower()
            if k not in seen: seen.add(k); items.append(line)
    return items[:30]


def _freeform_threads(lines: list[str]) -> list[str]:
    items, seen = [], set()
    for line in lines:
        if _THREAD_PATTERNS.search(line) and len(line) > 15:
            k = line[:60].lower()
            if k not in seen: seen.add(k); items.append(line)
    for line in lines[-40:][-15:]:
        if len(line) > 20:
            k = line[:60].lower()
            if k not in seen: seen.add(k); items.append(line)
    return items[:30]


# ── STRUCTURED OUTPUT BUILDERS ─────────────────────────────────────────

def _manifest_objects(items: list[str]) -> list[dict]:
    out = []
    for item in items:
        m = re.match(r"^(?P<path>[A-Za-z]:\\[^\u2014-]+|\\\\[^\u2014-]+)\s*[\u2014-]\s*(?P<desc>.+)$", item)
        if m:
            out.append({"path": m.group("path").strip(), "description": m.group("desc").strip()})
        else:
            out.append({"description": item})
    return out


def _decision_objects(items: list[str]) -> list[dict]:
    out = []
    for item in items:
        if ":" in item:
            t, r = item.split(":", 1)
            out.append({"topic": t.strip(), "detail": r.strip()})
        else:
            out.append({"detail": item})
    return out


def _open_thread_objects(items: list[str]) -> list[dict]:
    out = []
    for item in items:
        if "\u2014" in item:
            t, r = item.split("\u2014", 1)
            out.append({"topic": t.strip(), "next_action": r.strip()})
        elif ":" in item:
            t, r = item.split(":", 1)
            out.append({"topic": t.strip(), "next_action": r.strip()})
        else:
            out.append({"next_action": item})
    return out


# ── MARKDOWN RENDERER ──────────────────────────────────────────────────

def _render_markdown(session_date, ai_partner, manifest, decisions, threads,
                     source_name, ollama_used, freeform_fallback=False, summary_text=""):
    lines = [
        f"# SESSION LOG - {ai_partner} | {session_date}", "",
        "**Purpose:** Preserve full conversation as source truth, distill into foundational handoff.", "",
    ]
    if summary_text:
        lines.extend([f"**Summary:** {summary_text}", ""])
    if ollama_used:
        lines.extend([f"> Summarized by Ollama ({OLLAMA_MODEL})", ""])
    if freeform_fallback:
        lines.extend(["> **Note:** Freeform extraction fallback. Review recommended.", ""])
    lines.extend([f"**Source:** `{source_name}`", "", "## Layer 1 - Session Manifest"])
    for item in manifest:
        if "path" in item:
            lines.append(f"- `{item['path']}` - {item['description']}")
        else:
            lines.append(f"- {item['description']}")
    if not manifest:
        lines.append("- *(no manifest items extracted)*")
    lines.extend(["", "## Layer 2 - Decisions And Results"])
    for item in decisions:
        if item.get("topic"):
            lines.append(f"- **{item['topic']}** - {item['detail']}")
        else:
            lines.append(f"- {item['detail']}")
    if not decisions:
        lines.append("- *(no decisions extracted)*")
    lines.extend(["", "## Layer 3 - Open Threads"])
    for idx, item in enumerate(threads, 1):
        if item.get("topic"):
            lines.append(f"{idx}. **{item['topic']}** - {item['next_action']}")
        else:
            lines.append(f"{idx}. {item['next_action']}")
    if not threads:
        lines.append("1. *(no open threads extracted)*")
    lines.extend(["", "---",
        f"*Generated {datetime.now():%Y-%m-%d %H:%M} | Pipeline: combined | Ollama: {'yes' if ollama_used else 'no'}*"])
    return "\n".join(lines) + "\n"


# ── DISTRIBUTION ───────────────────────────────────────────────────────

def _prepare_dir(path, logger, label):
    try:
        path.mkdir(parents=True, exist_ok=True)
        return path
    except (FileNotFoundError, OSError):
        logger.warning(f"{label} mirror unavailable: {path}")
        return None


def _request_json(method, url, body=None, timeout=60.0):
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = Request(url, data=data, headers=headers, method=method)
    with urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    return json.loads(raw.decode("utf-8")) if raw else {}


def _vectorize(payload, markdown, logger):
    text = markdown.strip()
    if not text:
        logger.warning("vectorization skipped: empty summary")
        return
    try:
        embed_resp = _request_json("POST", f"{INFINITY_URL}/embeddings",
            {"input": [text[:8000]], "model": EMBED_MODEL}, timeout=120.0)
        vector = embed_resp["data"][0]["embedding"]
        norm = math.sqrt(sum(x*x for x in vector))
        if norm > 0:
            vector = [x/norm for x in vector]
        try:
            _request_json("GET", f"{QDRANT_URL}/collections/{QDRANT_COLLECTION}", timeout=10.0)
        except Exception:
            _request_json("PUT", f"{QDRANT_URL}/collections/{QDRANT_COLLECTION}",
                {"vectors": {"size": len(vector), "distance": VECTOR_DISTANCE}}, timeout=30.0)
        point_id = str(uuid5(NAMESPACE_URL, f"session_handoff:{payload['session_id']}"))
        _request_json("PUT", f"{QDRANT_URL}/collections/{QDRANT_COLLECTION}/points?wait=true",
            {"points": [{"id": point_id, "vector": vector, "payload": {
                "kind": "session_handoff", "session_id": payload["session_id"],
                "session_date": payload["session_date"], "ai_partner": payload["ai_partner"],
                "source_file": payload["source_file"], "summary_preview": text[:1000],
                "embedded_at": datetime.now().isoformat(),
            }}]}, timeout=120.0)
        logger.info(f"vectorized -> Qdrant point {point_id}")
    except Exception as e:
        logger.warning(f"vectorization failed (non-fatal): {e}")


def _upsert_postgres(payload, markdown, logger):
    try:
        from db_utils import Database
        with Database(application_name="session_handoff_combined") as db:
            db.execute(SESSION_HANDOFFS_DDL)
            db.execute("""
                INSERT INTO session_handoffs
                    (session_id, session_date, ai_partner, source_file,
                     manifest_json, summary_markdown, history_dir, updated_at)
                VALUES (%s, %s, %s, %s, %s::jsonb, %s, %s, NOW())
                ON CONFLICT (session_id) DO UPDATE SET
                    session_date=EXCLUDED.session_date, ai_partner=EXCLUDED.ai_partner,
                    source_file=EXCLUDED.source_file, manifest_json=EXCLUDED.manifest_json,
                    summary_markdown=EXCLUDED.summary_markdown, history_dir=EXCLUDED.history_dir,
                    updated_at=NOW()
            """, (payload["session_id"], payload["session_date"], payload["ai_partner"],
                  payload["source_file"], json.dumps(payload, ensure_ascii=False, default=str),
                  markdown, str(ROOT / "knowledge" / "Session-Handoffs")))
        logger.info(f"Postgres upserted: {payload['session_id']}")
        return True
    except ImportError:
        logger.warning("db_utils not found - Postgres skipped")
    except Exception as e:
        logger.warning(f"Postgres failed (non-fatal): {e}")
    return False


def _update_history_index(history_dir):
    source_files = sorted(history_dir.glob("*_source.*"))
    lines = ["# Session Handoffs Index", "", "## Sessions"]
    if not source_files:
        lines.extend(["", "No sessions indexed yet."])
    else:
        for sf in reversed(source_files):
            stem = sf.name.split("_source")[0]
            lines.append(f"- `{stem}` - Source: `{sf.name}`")
    (history_dir / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── MAIN PIPELINE ─────────────────────────────────────────────────────

def process_file(file_path, logger, use_ollama=True):
    logger.info("=" * 60)
    logger.info(f"Processing: {file_path.name}")

    junk = _is_junk_input(file_path)
    if junk:
        logger.warning(f"SKIPPING junk: {file_path.name} - {junk}")
        _prepare_dir(ARCHIVE_DIR, logger, "archive")
        dest = ARCHIVE_DIR / file_path.name
        if dest.exists(): dest.unlink()
        shutil.move(str(file_path), str(dest))
        return None

    raw_text = _read_text(file_path)
    if len(raw_text.strip()) < 100:
        logger.warning(f"File too short, skipping: {file_path.name}")
        return None

    # ── STAGE 1: Ollama summarization ──────────────────────────────
    ollama_used = False
    ollama_output = ""
    ollama_summary_text = ""
    manifest_raw = decision_raw = thread_raw = []

    if use_ollama and _ollama_available():
        logger.info(f"Stage 1: Ollama ({OLLAMA_MODEL})...")
        ollama_output = _call_ollama(raw_text, logger)
        if ollama_output:
            ollama_used = True
            ol = _normalize_lines(ollama_output)
            manifest_raw = _collect_bullets(_extract_layer(ol, ["layer 1", "session manifest"]))
            decision_raw = _collect_bullets(_extract_layer(ol, ["layer 2", "decisions"]))
            thread_raw   = _collect_bullets(_extract_layer(ol, ["layer 3", "open threads"]))
            meta = _extract_metadata(ol)
            ollama_summary_text = meta.get("summary", "")
        else:
            logger.warning("Ollama returned empty - falling to regex")
    elif use_ollama:
        logger.warning("Ollama unavailable - falling to regex")

    # ── STAGE 1 FALLBACK: Regex ────────────────────────────────────
    freeform_fallback = False
    if not ollama_used:
        lines = _normalize_lines(raw_text)
        manifest_raw = _collect_bullets(_extract_layer(lines, ["layer 1", "session manifest"]))
        decision_raw = _collect_bullets(_extract_layer(lines, ["layer 2", "decisions and results", "decisions"]))
        thread_raw   = _collect_bullets(_extract_layer(lines, ["layer 3", "open threads"]))
        if not manifest_raw and not decision_raw and not thread_raw:
            logger.warning("No structured headers - freeform fallback")
            freeform_fallback = True
            manifest_raw = _freeform_manifest(lines)
            decision_raw = _freeform_decisions(lines)
            thread_raw   = _freeform_threads(lines)

    manifest  = _manifest_objects(manifest_raw)
    decisions = _decision_objects(decision_raw)
    threads   = _open_thread_objects(thread_raw)

    total = len(manifest) + len(decisions) + len(threads)
    skip_embedding = total == 0
    if skip_embedding:
        logger.warning("All layers empty - embedding will be skipped")

    # Metadata
    if ollama_used:
        meta = _extract_metadata(_normalize_lines(ollama_output))
        ai_partner = meta.get("ai_partner", _detect_ai_partner(raw_text))
        session_date = meta.get("session_date", _extract_date(raw_text))
    else:
        ai_partner = _detect_ai_partner(raw_text)
        session_date = _extract_date(raw_text)

    stem = file_path.stem
    payload = {
        "session_id": stem, "session_date": session_date,
        "ai_partner": ai_partner, "source_file": str(file_path),
        "ollama_used": ollama_used, "ollama_model": OLLAMA_MODEL if ollama_used else None,
        "freeform_fallback": freeform_fallback,
        "layer_1_session_manifest": manifest,
        "layer_2_decisions_and_results": decisions,
        "layer_3_open_threads": threads,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
    markdown = _render_markdown(
        session_date, ai_partner, manifest, decisions, threads,
        str(file_path), ollama_used, freeform_fallback, ollama_summary_text)

    # ── STAGE 2: Distribution ──────────────────────────────────────
    logger.info("Stage 2: Distribution...")
    _prepare_dir(OUTPUT_DIR, logger, "output")
    _prepare_dir(ARCHIVE_DIR, logger, "archive")

    json_name = f"{stem}_manifest.json"
    md_name   = f"{stem}_summary.md"
    json_path = OUTPUT_DIR / json_name
    md_path   = OUTPUT_DIR / md_name
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    logger.info(f"Written: {json_path}")
    logger.info(f"Written: {md_path}")

    if ollama_used and ollama_output:
        (OUTPUT_DIR / f"{stem}_ollama_raw.md").write_text(
            f"# Ollama Raw Summary - {stem}\n\n{ollama_output}\n", encoding="utf-8")

    # Mirror
    for label, path in MIRROR_DIRS_CONFIG:
        ready = _prepare_dir(path, logger, label)
        if ready:
            shutil.copy2(json_path, ready / json_name)
            shutil.copy2(md_path, ready / md_name)
            logger.info(f"Mirrored -> {ready}")

    # Archive source
    archived = ARCHIVE_DIR / file_path.name
    if archived.exists(): archived.unlink()
    shutil.move(str(file_path), str(archived))
    logger.info(f"Archived: {archived}")

    # Copy source to history dirs
    source_copy_name = f"{stem}_source{archived.suffix.lower() or '.md'}"
    for label, path in MIRROR_DIRS_CONFIG:
        if label in ("history", "knowledge"):
            ready = _prepare_dir(path, logger, label)
            if ready:
                shutil.copy2(archived, ready / source_copy_name)

    # Full conversation
    fc = _prepare_dir(FULL_CONVERSATION_DIR, logger, "full conversation")
    if fc:
        try:
            shutil.copy2(archived, fc / archived.name)
            logger.info(f"Full conversation -> {fc}")
        except Exception as e:
            logger.warning(f"Full conversation copy failed: {e}")

    # Update index
    for label, path in MIRROR_DIRS_CONFIG:
        if label in ("history", "knowledge") and path.exists():
            _update_history_index(path)

    _upsert_postgres(payload, markdown, logger)
    if not skip_embedding:
        _vectorize(payload, markdown, logger)
    else:
        logger.warning("Embedding SKIPPED (empty layers)")

    logger.info(f"DONE: {stem}")
    return payload


def main() -> int:
    logger = _setup_logging()
    logger.info("=" * 60)
    logger.info("Session Handoff Pipeline (Combined)")
    logger.info(f"Ollama: {OLLAMA_MODEL} @ {OLLAMA_URL}")
    logger.info("=" * 60)

    use_ollama = "--no-ollama" not in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if args:
        target = Path(args[0])
        if target.is_dir():
            files = sorted([f for f in target.iterdir()
                if f.is_file() and f.suffix.lower() in TEXT_EXTENSIONS
                and not f.name.startswith((".", "_")) and f.stat().st_size > 500])
            logger.info(f"Batch mode: {len(files)} files in {target}")
            for i, f in enumerate(files, 1):
                logger.info(f"[{i}/{len(files)}] {f.name}")
                process_file(f, logger, use_ollama=use_ollama)
        elif target.is_file():
            process_file(target, logger, use_ollama=use_ollama)
        else:
            logger.error(f"Not found: {target}")
            return 1
    else:
        DROP_DIR.mkdir(parents=True, exist_ok=True)
        files = sorted([f for f in DROP_DIR.iterdir()
            if f.is_file() and f.suffix.lower() in TEXT_EXTENSIONS
            and not f.name.startswith((".", "_"))])
        if not files:
            logger.info("No files in DROP_HERE")
            return 0
        logger.info(f"Found {len(files)} file(s) in DROP_HERE")
        for f in files:
            process_file(f, logger, use_ollama=use_ollama)

    logger.info("Pipeline complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
