"""
station_runner.py
Execute queued FAP station requests through Ollama (Mistral).

Reads:   X:\\knowledge-refinery\\13_SOURCE_SYSTEMS\\FAP\\_queue\\pending\\<jobid>\\*.request.md
Writes:  X:\\knowledge-refinery\\13_SOURCE_SYSTEMS\\FAP\\_queue\\completed\\<jobid>\\<station>.result.json
         X:\\knowledge-refinery\\13_SOURCE_SYSTEMS\\FAP\\_queue\\completed\\<jobid>\\<station>.result.md

Each station gets the paper's lossless content + the station's task description,
and Ollama is asked to return a strict JSON shape:

    {
      "status": "PASS" | "REVIEW" | "FAIL",
      "output": "<station-specific content>",
      "evidence": [{"paragraph_id": "p0042", "quote": "..."}],
      "blockers": ["..."],
      "notes": "..."
    }

If Ollama returns something that won't parse, we fall back to a REVIEW status with
the raw response captured.

Usage:
    python station_runner.py <jobid>
    python station_runner.py --all          # all pending jobs
    python station_runner.py --jobid 20260513-110725_gtq-03-first-quantum-state
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: pip install requests", file=sys.stderr)
    sys.exit(2)


# ── CONFIG ────────────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/generate"
# qwen2.5:3b is the only locally installed model fast enough on CPU + small enough
# to fit a useful paper window in its 4096-token context. Override with --model.
OLLAMA_MODEL = "qwen2.5:3b"
OLLAMA_TIMEOUT = 240
OLLAMA_NUM_PREDICT = 800
OLLAMA_TEMP = 0.2
OLLAMA_CONTEXT = 4096  # qwen2.5 default; do not raise without testing

FAP_ROOT = Path(r"X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP")
QUEUE_PENDING = FAP_ROOT / "_queue" / "pending"
QUEUE_COMPLETED = FAP_ROOT / "_queue" / "completed"
LOSSLESS_ROOT = FAP_ROOT / "lossless"

LOG_DIR = Path(r"X:\knowledge-refinery\full_workflow\logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ~6000 chars ≈ 1500 tokens. Leaves room for system preamble (~500),
# station task (~150) and response (~800) inside a 4096 token context.
MAX_PAPER_CHARS = 6000

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / f"station_runner_{datetime.now():%Y%m%d}.log",
            encoding="utf-8",
        ),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("station-runner")


# ── PROMPTS ───────────────────────────────────────────────────
SYSTEM_PREAMBLE = """You are a station processor for the Theophysics paper manufacturing pipeline,
run by David Lowe (POF 2828). Theophysics is a 15+ month framework bridging physics, theology,
consciousness and mathematics with 1,300+ papers.

Your job: execute ONE station task against ONE paper and return a strict JSON object.

CRITICAL RULES:
1. Output ONLY a single JSON object inside a fenced ```json ... ``` block. No prose outside.
2. The JSON object MUST have these five keys: status, output, evidence, blockers, notes.
3. status is exactly one of: PASS, REVIEW, FAIL.
4. The "output" field must contain your ACTUAL findings as markdown — not a placeholder,
   not the word "output", not example text. Replace it with real station content.
5. evidence is a JSON array of objects shaped {"paragraph_id": "p####", "quote": "exact quote"}.
   Use only paragraph ids that appear in the paper. Empty array if you cannot cite.
6. blockers is a JSON array of strings. Empty array if none.
7. notes is a JSON string. Empty string if none.
8. Do not invent equations, citations, sigma values, or paragraph ids you did not see.
9. If the paper lacks the material the station needs, return status=REVIEW and explain.
10. Keep output under 600 words.

Concrete example of a fully-filled return (DO NOT echo this — write your own content):

```json
{
  "status": "PASS",
  "output": "The paper formalizes decoherence as the irreversible step that breaks Eden's coherent state. Three axioms emerge: (A1) measurement is a thermodynamic event; (A2) the wavefunction is ontic, not epistemic; (A3) collapse is asymmetric in time.",
  "evidence": [{"paragraph_id": "p0018", "quote": "A quantum system in superposition occupies multiple eigenstates simultaneously."}],
  "blockers": [],
  "notes": "A1 maps cleanly to Law 9 (moral conservation)."
}
```

Now do your station's task and return YOUR JSON object — not the example.
"""


# ── HELPERS ───────────────────────────────────────────────────
def load_lossless(jobid: str) -> dict:
    path = LOSSLESS_ROOT / jobid / "lossless.article.json"
    if not path.exists():
        raise FileNotFoundError(f"lossless missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def paper_context(lossless: dict) -> str:
    title = lossless.get("title", "(no title)")
    blocks = lossless.get("text_blocks") or []
    # build "p0001: <text>" lines for paragraph-id-aware evidence
    lines = [f"TITLE: {title}", "", "PARAGRAPHS:"]
    used = 0
    for b in blocks:
        pid = b.get("id", "")
        text = (b.get("text") or "").strip()
        if not pid or not text:
            continue
        line = f"{pid}: {text}"
        if used + len(line) > MAX_PAPER_CHARS:
            lines.append(f"... (truncated after {pid})")
            break
        lines.append(line)
        used += len(line) + 1
    return "\n".join(lines)


def parse_request(request_path: Path) -> dict:
    """Parse a station request file. Extract station name, slug, task description."""
    text = request_path.read_text(encoding="utf-8")
    station = request_path.stem.replace(".request", "")
    slug_match = re.search(r"Article slug:\s*(.+)", text)
    task_match = re.search(r"Task:\s*\n+(.+?)(?=\n\nReturn:|\Z)", text, re.S)
    return {
        "station": station,
        "slug": slug_match.group(1).strip() if slug_match else "",
        "task": task_match.group(1).strip() if task_match else text,
        "raw": text,
    }


def build_prompt(station: str, task: str, paper_text: str) -> str:
    return f"""{SYSTEM_PREAMBLE}

STATION: {station}

STATION TASK:
{task}

PAPER:
{paper_text}

Now return the single JSON object. Remember: only paragraph_ids you can see above are valid evidence.
"""


JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.S)
JSON_BARE_RE = re.compile(r"(\{(?:[^{}]|\{[^{}]*\})*\})", re.S)


def extract_json(text: str) -> dict | None:
    if not text:
        return None
    m = JSON_FENCE_RE.search(text)
    candidate = m.group(1) if m else None
    if candidate is None:
        # try the largest bare {...} block
        candidates = JSON_BARE_RE.findall(text)
        if candidates:
            candidate = max(candidates, key=len)
    if not candidate:
        return None
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        # last-resort cleanup
        cleaned = candidate.replace("\r", "")
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return None


def call_ollama(prompt: str) -> tuple[str, dict]:
    """Returns (response_text, raw_meta_dict). Empty string on failure."""
    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": OLLAMA_NUM_PREDICT,
                    "temperature": OLLAMA_TEMP,
                    "num_ctx": OLLAMA_CONTEXT,
                },
            },
            timeout=OLLAMA_TIMEOUT,
        )
        if not r.ok:
            log.error("Ollama HTTP %s: %s", r.status_code, r.text[:200])
            return "", {"http_status": r.status_code}
        body = r.json()
        return body.get("response", ""), {
            "eval_count": body.get("eval_count"),
            "total_duration_ns": body.get("total_duration"),
        }
    except requests.exceptions.ConnectionError:
        log.error("Ollama not reachable at %s", OLLAMA_URL)
        return "", {"error": "connection-refused"}
    except Exception as e:
        log.error("Ollama call failed: %s", e)
        return "", {"error": str(e)}


def health_check() -> bool:
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        return r.ok
    except Exception:
        return False


def normalize_result(parsed: dict | None, raw_response: str) -> dict:
    """Force the result into the canonical shape, regardless of what Ollama returned."""
    if not isinstance(parsed, dict):
        return {
            "status": "REVIEW",
            "output": raw_response.strip() or "(empty response from Ollama)",
            "evidence": [],
            "blockers": ["Ollama returned unparseable response — needs human review"],
            "notes": "auto-fallback: JSON parse failed",
        }
    status = str(parsed.get("status", "REVIEW")).upper().strip()
    if status not in {"PASS", "REVIEW", "FAIL"}:
        status = "REVIEW"
    evidence_raw = parsed.get("evidence") or []
    evidence = []
    if isinstance(evidence_raw, list):
        for e in evidence_raw:
            if isinstance(e, dict):
                pid = str(e.get("paragraph_id", "")).strip()
                quote = str(e.get("quote", "")).strip()
                if pid:
                    evidence.append({"paragraph_id": pid, "quote": quote})
    blockers_raw = parsed.get("blockers") or []
    blockers = (
        [str(b) for b in blockers_raw if str(b).strip()]
        if isinstance(blockers_raw, list)
        else [str(blockers_raw)]
    )
    return {
        "status": status,
        "output": str(parsed.get("output", "")).strip(),
        "evidence": evidence,
        "blockers": blockers,
        "notes": str(parsed.get("notes", "")).strip(),
    }


def write_result(jobid: str, station: str, result: dict, meta: dict) -> Path:
    out_dir = QUEUE_COMPLETED / jobid
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema_version": "fap.station_result.v1",
        "jobid": jobid,
        "station": station,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "model": OLLAMA_MODEL,
        "result": result,
        "ollama_meta": meta,
    }
    json_path = out_dir / f"{station}.result.json"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    md = [
        f"# Station Result - {station}",
        "",
        f"- Status: **{result['status']}**",
        f"- Job: {jobid}",
        f"- Model: {OLLAMA_MODEL}",
        f"- Generated: {payload['generated_at']}",
        "",
        "## Output",
        "",
        result["output"] or "(empty)",
        "",
        "## Evidence",
        "",
    ]
    if result["evidence"]:
        for e in result["evidence"]:
            md.append(f"- `{e['paragraph_id']}` — {e['quote']}")
    else:
        md.append("(none)")
    md += ["", "## Blockers", ""]
    if result["blockers"]:
        for b in result["blockers"]:
            md.append(f"- {b}")
    else:
        md.append("(none)")
    if result["notes"]:
        md += ["", "## Notes", "", result["notes"]]
    md_path = out_dir / f"{station}.result.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    return json_path


def move_request_to_completed(request_path: Path, jobid: str):
    dest_dir = QUEUE_COMPLETED / jobid
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / request_path.name
    try:
        shutil.move(str(request_path), str(dest))
    except Exception as e:
        log.warning("Couldn't move request %s -> %s: %s", request_path.name, dest, e)


def process_job(jobid: str) -> dict:
    log.info("=" * 60)
    log.info("Processing job: %s", jobid)
    log.info("=" * 60)

    pending_dir = QUEUE_PENDING / jobid
    if not pending_dir.exists():
        log.warning("No pending dir for %s — already processed?", jobid)
        return {"jobid": jobid, "stations": [], "skipped": True}

    requests_list = sorted(pending_dir.glob("*.request.md"))
    if not requests_list:
        log.info("No pending requests for %s", jobid)
        return {"jobid": jobid, "stations": [], "skipped": True}

    try:
        lossless = load_lossless(jobid)
    except FileNotFoundError as e:
        log.error("Lossless missing: %s", e)
        return {"jobid": jobid, "stations": [], "error": str(e)}

    paper_text = paper_context(lossless)

    summary = {"jobid": jobid, "stations": []}
    for req_path in requests_list:
        req = parse_request(req_path)
        station = req["station"]
        log.info("→ Station: %s", station)
        prompt = build_prompt(station, req["task"], paper_text)

        t0 = time.time()
        response, meta = call_ollama(prompt)
        elapsed = time.time() - t0
        log.info("  Ollama %.1fs (%d chars)", elapsed, len(response))
        meta["elapsed_sec"] = round(elapsed, 1)

        parsed = extract_json(response)
        result = normalize_result(parsed, response)
        out_path = write_result(jobid, station, result, meta)
        log.info("  -> %s  status=%s", out_path.name, result["status"])

        move_request_to_completed(req_path, jobid)
        summary["stations"].append({
            "station": station,
            "status": result["status"],
            "evidence_count": len(result["evidence"]),
            "blocker_count": len(result["blockers"]),
            "elapsed_sec": meta["elapsed_sec"],
        })

    # cleanup: remove the now-empty pending dir
    try:
        pending_dir.rmdir()
    except OSError:
        pass

    log.info(
        "Done %s: %d stations, PASS=%d REVIEW=%d FAIL=%d",
        jobid,
        len(summary["stations"]),
        sum(1 for s in summary["stations"] if s["status"] == "PASS"),
        sum(1 for s in summary["stations"] if s["status"] == "REVIEW"),
        sum(1 for s in summary["stations"] if s["status"] == "FAIL"),
    )
    return summary


def list_pending_jobids() -> list[str]:
    if not QUEUE_PENDING.exists():
        return []
    return sorted(d.name for d in QUEUE_PENDING.iterdir() if d.is_dir())


# ── MAIN ──────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--all", action="store_true", help="Process all pending jobs")
    g.add_argument("--jobid", help="Single jobid (folder name)")
    ap.add_argument("jobid_pos", nargs="?", help="Positional jobid")
    args = ap.parse_args()

    if not health_check():
        log.error("Ollama not reachable. Start it via RUN_OLLAMA.bat then retry.")
        return 1

    if args.all:
        targets = list_pending_jobids()
    else:
        jid = args.jobid or args.jobid_pos
        if not jid:
            targets = list_pending_jobids()
            if not targets:
                log.info("No pending jobs.")
                return 0
        else:
            targets = [jid]

    if not targets:
        log.info("Nothing to do.")
        return 0

    log.info("Targets: %s", ", ".join(targets))
    summaries = [process_job(j) for j in targets]

    total = sum(len(s.get("stations", [])) for s in summaries)
    log.info("All done. %d job(s), %d station call(s).", len(summaries), total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
