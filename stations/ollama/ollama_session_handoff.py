"""
ollama_session_handoff.py
Summarize a raw AI chat session using Ollama (Mistral/local LLM)
instead of BART. Produces structured handoff with manifest,
decisions, and open threads.

Usage:
  python ollama_session_handoff.py <session_file>
  python ollama_session_handoff.py  (processes all in DROP_HERE)

Integrates with existing pipeline directories.
"""

import json
import os
import sys
import re
import shutil
import logging
from datetime import datetime
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ── CONFIG ────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"
OLLAMA_TIMEOUT = 120

DROP_DIR = Path(r"X:\session-handoff-drop\DROP_HERE")
EXPORT_ROOT = HERE / "EXPORTS"
OUTPUT_DIR = EXPORT_ROOT / "reports" / "session-handoffs"
ARCHIVE_DIR = HERE / "_ARCHIVE" / "processed_sources"

# Mirror destinations (same as existing pipeline)
MIRRORS = []
FULL_CONV_DIR = EXPORT_ROOT / "source_copies" / "full_conversation"

# Vectorization config (same as existing pipeline)
INFINITY_URL = "http://192.168.1.177:7997"
QDRANT_URL = "http://192.168.1.177:6333"
QDRANT_COLLECTION = "session_handoffs"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_DISTANCE = "Cosine"

# Postgres helper station
POSTGRES_TOOL_DIR = Path(r"X:\Backside\stations\postgres-sync.station")
if str(POSTGRES_TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(POSTGRES_TOOL_DIR))

LOG_DIR = EXPORT_ROOT / "reports" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"ollama_handoff_{datetime.now():%Y%m%d}.log",
                           encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("ollama-handoff")

# ── SUMMARIZATION PROMPT ──────────────────────────────────────

HANDOFF_PROMPT = """You are a session handoff summarizer for the Theophysics project — a research framework bridging physics, theology, consciousness, and mathematics, built by David Lowe (POF 2828).

You are reading a raw AI chat session transcript. Your job is to produce a STRUCTURED handoff summary that the next AI session can use to pick up where this one left off.

Output EXACTLY this format (markdown). Every section must be present even if empty:

# SESSION HANDOFF — {date}
**AI Partner:** {which AI was in this session}
**Duration:** {approximate length}
**Summary:** {2-3 sentence overview of what happened}

## What Was Built
{List every file created, modified, committed, or deployed. Include full paths. Be specific.}

## Decisions Made
{List every decision, lock, or commitment made during the session. Format: "DECIDED: [what] — [why]"}

## Key Insights
{List the 3-5 most important ideas, breakthroughs, or realizations from the session. These are the things the next session needs to KNOW, not just the things that were DONE.}

## Open Threads
{List everything that was started but not finished, or flagged for future work. Format: "TODO: [what] — [context]"}

## Files and Paths Referenced
{List every file path, URL, repo, or resource mentioned in the session. Deduplicate.}

## Next Session Priorities
{Ordered list of what should happen next, based on what was accomplished and what remains.}

---

RULES:
- Be specific. "Built some stuff" is useless. "Created D:\\BIL\\engines\\pipeline\\llm_hub.py — 3-tier AI hierarchy with auto-escalation" is useful.
- Decisions are things that were LOCKED. Not discussed, not proposed — decided.
- Key insights are things that change how the project thinks, not just what it does.
- Open threads are things the NEXT session needs to act on.
- Do NOT include raw conversation fragments. Summarize.
- Do NOT pad with filler. If a section is empty, write "None this session."
- Keep the total summary under 800 words. Dense, not long.

SESSION TRANSCRIPT:
{{INPUT}}"""


# ── CORE FUNCTIONS ────────────────────────────────────────────

def call_ollama(prompt: str, max_chars: int = 24000) -> str:
    """Call Ollama with the summarization prompt."""
    if not HAS_REQUESTS:
        logger.error("requests library not installed")
        return ""

    # Truncate input to fit context window
    if len(prompt) > max_chars:
        # Keep first 8k and last 16k (end of session usually has the summary)
        prompt = prompt[:8000] + "\n\n[...middle of session truncated...]\n\n" + prompt[-16000:]

    try:
        r = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 2048,
                "temperature": 0.3,
            },
        }, timeout=OLLAMA_TIMEOUT)

        if r.ok:
            return r.json().get("response", "")
        else:
            logger.error(f"Ollama returned HTTP {r.status_code}: {r.text[:200]}")
            return ""
    except requests.exceptions.ConnectionError:
        logger.error("Ollama not running at localhost:11434. Start it first.")
        return ""
    except Exception as e:
        logger.error(f"Ollama error: {e}")
        return ""


def summarize_session(file_path: Path) -> dict:
    """Read a session file and produce a structured handoff."""
    logger.info(f"Processing: {file_path.name}")

    text = file_path.read_text(encoding="utf-8", errors="replace")
    if len(text.strip()) < 100:
        logger.warning(f"File too short, skipping: {file_path.name}")
        return {}

    # Build the prompt
    prompt = HANDOFF_PROMPT.replace("{{INPUT}}", text)

    # Call Ollama
    logger.info(f"Calling Ollama ({OLLAMA_MODEL})...")
    summary = call_ollama(prompt)

    if not summary:
        logger.error("Ollama returned empty response")
        return {}

    logger.info(f"Got {len(summary)} chars back from Ollama")

    # Extract date from filename or content
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", file_path.stem)
    if not date_match:
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", text[:500])
    session_date = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")

    return {
        "session_id": file_path.stem,
        "session_date": session_date,
        "source_file": str(file_path),
        "summary_markdown": summary,
        "model_used": OLLAMA_MODEL,
        "timestamp": datetime.now().isoformat(),
    }


def save_and_mirror(result: dict, source_path: Path):
    """Save summary and mirror to all destinations."""
    if not result:
        return

    session_id = result["session_id"]
    summary_md = result["summary_markdown"]

    # Save to ollama output dir
    md_path = OUTPUT_DIR / f"{session_id}_ollama_summary.md"
    json_path = OUTPUT_DIR / f"{session_id}_ollama_manifest.json"

    md_path.write_text(summary_md, encoding="utf-8")
    json_path.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    logger.info(f"Saved: {md_path}")
    logger.info(f"Saved: {json_path}")

    # Mirror to all destinations
    for mirror_dir in MIRRORS:
        try:
            mirror_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(md_path), str(mirror_dir / md_path.name))
            shutil.copy2(str(json_path), str(mirror_dir / json_path.name))
            logger.info(f"Mirrored -> {mirror_dir}")
        except Exception as e:
            logger.warning(f"Mirror failed for {mirror_dir}: {e}")

    # Copy full conversation
    try:
        FULL_CONV_DIR.mkdir(parents=True, exist_ok=True)
        if not (FULL_CONV_DIR / source_path.name).exists():
            shutil.copy2(str(source_path), str(FULL_CONV_DIR / source_path.name))
            logger.info(f"Full conversation -> {FULL_CONV_DIR}")
    except Exception as e:
        logger.warning(f"Full conversation copy failed: {e}")


# ── VECTORIZATION (Infinity → Qdrant) ────────────────────────

def _request_json(method: str, url: str, body: dict = None, timeout: float = 60.0) -> dict:
    """HTTP helper using urllib (no extra deps beyond requests for Ollama)."""
    from urllib.request import Request, urlopen
    import json as _json
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = _json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = Request(url, data=data, headers=headers, method=method)
    with urlopen(req, timeout=timeout) as resp:
        return _json.loads(resp.read().decode("utf-8"))


def vectorize_handoff(result: dict):
    """Embed the summary into Qdrant via Infinity."""
    from uuid import NAMESPACE_URL, uuid5

    text = result.get("summary_markdown", "").strip()
    if not text:
        logger.warning("Vectorization skipped: empty summary")
        return

    try:
        # Get embedding from Infinity
        embed_resp = _request_json(
            "POST",
            f"{INFINITY_URL}/embeddings",
            {"input": [text[:8000]], "model": EMBED_MODEL},
            timeout=120.0,
        )
        vector = embed_resp["data"][0]["embedding"]
        # Normalize
        import math
        norm = math.sqrt(sum(x * x for x in vector))
        if norm > 0:
            vector = [x / norm for x in vector]

        # Ensure collection exists
        try:
            _request_json("GET", f"{QDRANT_URL}/collections/{QDRANT_COLLECTION}", timeout=10.0)
        except Exception:
            _request_json("PUT", f"{QDRANT_URL}/collections/{QDRANT_COLLECTION}",
                         {"vectors": {"size": len(vector), "distance": VECTOR_DISTANCE}},
                         timeout=30.0)

        # Upsert point
        point_id = str(uuid5(NAMESPACE_URL, f"ollama_handoff:{result['session_id']}"))
        point_payload = {
            "kind": "session_handoff_ollama",
            "session_id": result["session_id"],
            "session_date": result["session_date"],
            "source_file": result["source_file"],
            "model_used": result.get("model_used", OLLAMA_MODEL),
            "summary_preview": text[:1000],
            "embedded_at": datetime.now().isoformat(),
        }
        _request_json(
            "PUT",
            f"{QDRANT_URL}/collections/{QDRANT_COLLECTION}/points?wait=true",
            {"points": [{"id": point_id, "vector": vector, "payload": point_payload}]},
            timeout=120.0,
        )
        logger.info(f"Vectorized -> Qdrant {QDRANT_COLLECTION} point {point_id}")

    except Exception as e:
        logger.warning(f"Vectorization failed (non-fatal): {e}")


# ── POSTGRES UPSERT ──────────────────────────────────────────

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
"""

def upsert_to_postgres(result: dict):
    """Upsert the handoff into the session_handoffs table."""
    try:
        from db_utils import Database
        with Database(application_name="ollama_session_handoff") as db:
            db.execute(SESSION_HANDOFFS_DDL)
            db.execute(
                """
                INSERT INTO session_handoffs
                    (session_id, session_date, ai_partner, source_file,
                     manifest_json, summary_markdown, history_dir, updated_at)
                VALUES
                    (%s, %s, %s, %s, %s::jsonb, %s, %s, NOW())
                ON CONFLICT (session_id) DO UPDATE SET
                    session_date = EXCLUDED.session_date,
                    ai_partner = EXCLUDED.ai_partner,
                    source_file = EXCLUDED.source_file,
                    manifest_json = EXCLUDED.manifest_json,
                    summary_markdown = EXCLUDED.summary_markdown,
                    history_dir = EXCLUDED.history_dir,
                    updated_at = NOW()
                """,
                (
                    result["session_id"],
                    result["session_date"],
                    result.get("ai_partner", "Unknown"),
                    result["source_file"],
                    json.dumps(result, ensure_ascii=False, default=str),
                    result["summary_markdown"],
                    str(OUTPUT_DIR),
                ),
            )
        logger.info(f"Postgres upserted: {result['session_id']}")
    except ImportError:
        logger.warning("db_utils not found at X:\\Backside\\stations\\postgres-sync.station - Postgres skipped")
    except Exception as e:
        logger.warning(f"Postgres upsert failed (non-fatal): {e}")


def process_file(file_path: Path):
    """Process a single session file end-to-end."""
    result = summarize_session(file_path)
    if result:
        save_and_mirror(result, file_path)
        vectorize_handoff(result)
        upsert_to_postgres(result)
        # Archive the source
        try:
            ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
            archive_path = ARCHIVE_DIR / file_path.name
            if not archive_path.exists():
                shutil.move(str(file_path), str(archive_path))
                logger.info(f"Archived: {file_path.name}")
        except Exception as e:
            logger.warning(f"Archive failed: {e}")
    return result


def process_drop_folder():
    """Process all files in DROP_HERE."""
    if not DROP_DIR.exists():
        logger.error(f"DROP_HERE not found: {DROP_DIR}")
        return

    files = [f for f in DROP_DIR.iterdir()
             if f.is_file() and f.suffix.lower() in {".txt", ".md", ".html"}
             and not f.name.startswith((".", "_"))]

    if not files:
        logger.info("No files in DROP_HERE")
        return

    logger.info(f"Found {len(files)} file(s) to process")
    for f in sorted(files):
        process_file(f)


# ── MAIN ──────────────────────────────────────────────────────

def main():
    logger.info("=" * 60)
    logger.info("Ollama Session Handoff Summarizer")
    logger.info(f"Model: {OLLAMA_MODEL} @ {OLLAMA_URL}")
    logger.info("=" * 60)

    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        if target.is_dir():
            # Batch mode: process entire folder
            files = [f for f in target.iterdir()
                     if f.is_file() and f.suffix.lower() in {".txt", ".md", ".html"}
                     and not f.name.startswith((".", "_"))
                     and f.stat().st_size > 500]  # skip tiny junk files
            logger.info(f"Batch mode: {len(files)} files in {target}")
            for i, f in enumerate(sorted(files), 1):
                logger.info(f"[{i}/{len(files)}] {f.name}")
                result = summarize_session(f)
                if result:
                    save_and_mirror(result, f)
                    vectorize_handoff(result)
                    upsert_to_postgres(result)
                    # DON'T archive when reprocessing — leave originals in place
        elif target.is_file():
            process_file(target)
        else:
            logger.error(f"Not found: {target}")
    else:
        # Process DROP_HERE folder
        process_drop_folder()

    logger.info("Done.")


if __name__ == "__main__":
    main()
