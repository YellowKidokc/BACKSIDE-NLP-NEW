"""
Theophysics Knowledge Refinery Conductor v2
Processes content: intake -> classify -> grade -> compile -> export
Supports: Ollama (default) or Claude Code CLI for LLM checkpoints
Includes: round-trip output + canonical markdown export + idle scheduler
POF 2828 | May 2026
"""
from __future__ import annotations
import json
import re
import sys
import os
import time
import hashlib
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path
from html.parser import HTMLParser
import argparse

# === CONFIGURATION ===
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi4:latest"
REFINERY = Path(r"X:\knowledge-refinery")
FAP_PROMPTS = Path(r"D:\FAP\wiki\prompts")
OBSIDIAN_EXPORT = REFINERY / "07_OBSIDIAN_EXPORT"
HTML_REPORTS = REFINERY / "06_HTML_REPORTS"
LOGS = REFINERY / "12_HEALTH"
CANONICAL_EXPORT = Path(r"X:\knowledge-refinery\canonical")

INTAKE = REFINERY / "00_INTAKE"
CONVERSION = REFINERY / "01_CONVERSION"
NORMALIZATION = REFINERY / "02_NORMALIZATION"
ROUTING = REFINERY / "03_ROUTING"
MODEL_STATIONS = REFINERY / "04_MODEL_STATIONS"
WORKFLOW_RUNS = REFINERY / "05_WORKFLOW_RUNS"
ARCHIVE = REFINERY / "08_ARCHIVE"
MEMORY = REFINERY / "09_MEMORY"

# Round-trip subfolder names
GRADE_LAYER = "_grade-layer"
DATA_LAYER = "_data-layer"

# Ensure dirs exist
for d in [CANONICAL_EXPORT, INTAKE, CONVERSION, NORMALIZATION, ROUTING,
          MODEL_STATIONS, WORKFLOW_RUNS, OBSIDIAN_EXPORT, HTML_REPORTS,
          LOGS, ARCHIVE, MEMORY]:
    d.mkdir(parents=True, exist_ok=True)


# === HTML TEXT EXTRACTOR ===
class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._text = []
        self._skip = False
        self._skip_tags = {"script", "style", "head", "noscript"}

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._skip = True
        if tag in ("br", "p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
                    "li", "tr", "section"):
            self._text.append("\n")

    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self._text.append(data)

    def get_text(self) -> str:
        raw = "".join(self._text)
        lines = [line.strip() for line in raw.splitlines()]
        return "\n".join(line for line in lines if line)


def extract_text_from_html(path: Path) -> str:
    html = path.read_text(encoding="utf-8", errors="replace")
    parser = HTMLTextExtractor()
    parser.feed(html)
    return parser.get_text()


# === LLM ENGINES ===

ENGINE = "ollama"  # set by CLI args

def ollama_generate(prompt: str, max_tokens: int = 4096) -> str:
    body = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": max_tokens, "temperature": 0.3}
    }).encode()
    req = urllib.request.Request(OLLAMA_URL, data=body,
                                headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read())
            return data.get("response", "")
    except Exception as exc:
        return f"OLLAMA_ERROR: {exc}"


def claude_code_generate(prompt: str, max_tokens: int = 4096) -> str:
    """Use Claude Code CLI (claude) as the LLM engine."""
    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True, text=True, timeout=300,
            encoding="utf-8", errors="replace"
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return f"CLAUDE_CODE_ERROR: {result.stderr[:500]}"
    except FileNotFoundError:
        return "CLAUDE_CODE_ERROR: claude CLI not found. Install with: npm install -g @anthropic-ai/claude-code"
    except subprocess.TimeoutExpired:
        return "CLAUDE_CODE_ERROR: timeout after 300s"
    except Exception as exc:
        return f"CLAUDE_CODE_ERROR: {exc}"


def llm_generate(prompt: str, max_tokens: int = 4096) -> str:
    """Route to the active LLM engine."""
    if ENGINE == "claude-code":
        return claude_code_generate(prompt, max_tokens)
    return ollama_generate(prompt, max_tokens)


def extract_json(text: str) -> dict | None:
    try:
        return json.loads(text.strip())
    except Exception:
        pass
    m = re.search(r'\{[\s\S]*\}', text)
    if m:
        try:
            return json.loads(m.group())
        except Exception:
            pass
    return None


# === PIPELINE STATIONS ===

def station_classify(text: str, filename: str) -> dict:
    prompt_template = (FAP_PROMPTS / "classify_document.md").read_text(encoding="utf-8")
    prompt = prompt_template.replace("{{INPUT}}", text[:6000])
    print(f"  [classify] Running on {filename}...")
    raw = llm_generate(prompt)
    result = extract_json(raw)
    if result is None:
        result = {"type": "unknown", "laws": [], "topics": [], "quality": 0.0,
                  "summary": "Classification failed", "raw_response": raw[:500]}
    result["source_file"] = filename
    result["station"] = "classify"
    result["timestamp"] = datetime.now().isoformat()
    return result


def station_grade(text: str, filename: str) -> dict:
    prompt_template = (FAP_PROMPTS / "grade_paper.md").read_text(encoding="utf-8")
    prompt = prompt_template.replace("{{INPUT}}", text[:6000])
    print(f"  [grade] Running on {filename}...")
    raw = llm_generate(prompt)
    result = extract_json(raw)
    if result is None:
        result = {"overall_score": 0.0, "verdict": "review",
                  "raw_response": raw[:500]}
    result["source_file"] = filename
    result["station"] = "grade"
    result["timestamp"] = datetime.now().isoformat()
    return result


def station_exec_summary(text: str, filename: str) -> str:
    prompt = f"""You are summarizing a Theophysics research paper for a busy reader.
Write a 2-3 sentence executive summary. No jargon. What does it claim and why does it matter?

DOCUMENT:
{text[:4000]}

EXECUTIVE SUMMARY:"""
    print(f"  [exec_summary] Running on {filename}...")
    return llm_generate(prompt, max_tokens=300).strip()


def station_plain_english(text: str, filename: str) -> str:
    prompt = f"""Explain this paper in plain English. 200-400 words. No jargon, no citations, no equations.
Write as if explaining to someone over coffee. Use "you" and "I". Be direct.

DOCUMENT:
{text[:4000]}

PLAIN ENGLISH EXPLANATION:"""
    print(f"  [plain_english] Running on {filename}...")
    return llm_generate(prompt, max_tokens=600).strip()


def station_math_extract(text: str, filename: str) -> dict:
    prompt = f"""You are a mathematical reviewer. Extract ALL equations, formulas, and mathematical expressions from this document.
For each one:
1. State the equation
2. Identify the variables
3. Check if the math is internally consistent
4. Flag any errors or unsupported leaps

Return ONLY valid JSON:
{{"equations_found": [{{"equation": "...", "variables": ["..."], "valid": true, "notes": "..."}}],
  "math_score": 0.0, "errors": [], "total_equations": 0}}

DOCUMENT:
{text[:8000]}"""
    print(f"  [math_extract] Running on {filename}...")
    raw = llm_generate(prompt, max_tokens=2000)
    result = extract_json(raw)
    if result is None:
        result = {"equations_found": [], "math_score": 0.0,
                  "errors": ["Extraction failed"], "total_equations": 0,
                  "raw_response": raw[:500]}
    result["station"] = "math_extract"
    return result


def station_contradiction_check(text: str, filename: str) -> dict:
    prompt = f"""You are a logical consistency checker. Read this document and identify:
1. Any claims that contradict each other within the document
2. Any claims that contradict standard physics or established mathematics
3. Any logical gaps where a conclusion does not follow from the premises

Return ONLY valid JSON:
{{"contradictions": [{{"claim_a": "...", "claim_b": "...", "severity": "high", "explanation": "..."}}],
  "logical_gaps": [{{"location": "...", "issue": "...", "severity": "high"}}],
  "contradiction_score": 0.0, "overall_consistency": "consistent"}}

DOCUMENT:
{text[:6000]}"""
    print(f"  [contradiction] Running on {filename}...")
    raw = llm_generate(prompt, max_tokens=2000)
    result = extract_json(raw)
    if result is None:
        result = {"contradictions": [], "logical_gaps": [],
                  "contradiction_score": 0.0, "overall_consistency": "unknown",
                  "raw_response": raw[:500]}
    result["station"] = "contradiction_check"
    return result


# === PAGE COMPILER ===

def compile_production_page(filename, text, classify_result, grade_result,
                            exec_summary, plain_english, math_result,
                            contradiction_result) -> str:
    title = classify_result.get("suggested_title",
                filename.replace(".html","").replace(".md","").replace("-"," ").title())
    paper_id = hashlib.md5(filename.encode()).hexdigest()[:8].upper()
    laws = classify_result.get("laws", [])
    topics = classify_result.get("topics", [])
    overall_score = grade_result.get("overall_score", 0.0)
    verdict = grade_result.get("verdict", "review").upper()
    math_score = math_result.get("math_score", 0.0)
    contradiction_score = contradiction_result.get("contradiction_score", 0.0)
    consistency = contradiction_result.get("overall_consistency", "unknown")
    dims = grade_result.get("dimensions", {})

    if overall_score >= 0.85 and math_score >= 0.8:
        epistemic = "mathematically_derived"
    elif overall_score >= 0.7:
        epistemic = "partially_supported"
    elif overall_score >= 0.5:
        epistemic = "hypothesis"
    else:
        epistemic = "speculative"

    page = f"""---
title: "{title}"
paper_id: "REF-{paper_id}"
series: ""
status: pipeline_processed
type: paper
epistemic_state: {epistemic}
laws: {json.dumps(laws)}
axioms: []
seven_q: ""
rubric_score: {overall_score}
verdict: {verdict}
fact_check_score: 0.0
math_score: {math_score}
contradiction_score: {contradiction_score}
timeline_score: 0.0
voice_score: {dims.get('voice_authenticity', 0.0)}
cross_domain_score: {dims.get('cross_domain_strength', 0.0)}
word_count: {len(text.split())}
created: "{datetime.now().strftime('%Y-%m-%d')}"
updated: "{datetime.now().strftime('%Y-%m-%d')}"
author: POF 2828
ai_partners: ["opus", "{OLLAMA_MODEL if ENGINE=='ollama' else 'claude-code'}"]
tags: {json.dumps(topics[:10])}
provenance: pipeline_v2
source_file: "{filename}"
pipeline_engine: "{ENGINE}"
---

> [!metadata] Facts
> **Paper ID:** REF-{paper_id}
> **Status:** pipeline_processed
> **Epistemic State:** {epistemic}
> **Verdict:** {verdict}
> **Composite Score:** {overall_score}
> **Math Score:** {math_score}
> **Contradiction Score:** {contradiction_score} ({consistency})
> **Laws:** {', '.join(laws) if laws else '[pending]'}

---

## Layer 1 - Executive Summary

> [!abstract] Executive Summary
> {exec_summary}

---

## Layer 2 - Plain English

{plain_english}

---

## Layer 3 - Article

[Source: `{filename}`]

{text[:10000]}
{"[... truncated - see source file for full text ...]" if len(text) > 10000 else ""}

---

## Layer 4 - Academic Summary

> [!note] Pending manual review

---

## Layer 5 - Cross-References

**Laws:** {', '.join(laws) if laws else '[pending]'}
**Contradictions found:** {len(contradiction_result.get('contradictions', []))}
**Logical gaps found:** {len(contradiction_result.get('logical_gaps', []))}

---

## Layer 6 - Data & Evidence

### Grading
| Dimension | Score |
|-----------|-------|
| Overall | {overall_score} |
| Coherence | {dims.get('coherence', 'n/a')} |
| Voice | {dims.get('voice_authenticity', 'n/a')} |
| Cross-Domain | {dims.get('cross_domain_strength', 'n/a')} |
| Axiom Coverage | {dims.get('axiom_coverage', 'n/a')} |
| Publish Ready | {dims.get('publish_readiness', 'n/a')} |

### Math ({math_result.get('total_equations', 0)} equations, score: {math_score})
{chr(10).join(f"- `{eq.get('equation','')}` {'VALID' if eq.get('valid') else 'CHECK'}" for eq in math_result.get('equations_found', [])[:20])}

### Contradictions
{chr(10).join(f"- [{c.get('severity','?')}] {c.get('explanation','')}" for c in contradiction_result.get('contradictions', [])) or "None found"}

---

## Layer 7A - Framework Impact

[pending]

---

## Layer 7B - Open Obligations

**Issues:** {json.dumps(grade_result.get('issues', []))}
**Action:** {grade_result.get('recommended_action', 'review')}
"""
    return page


# === ROUND-TRIP OUTPUT ===

def write_round_trip(source_path: Path, classify_result: dict,
                     grade_result: dict, math_result: dict,
                     contradiction_result: dict, production_page: str):
    """Write outputs BACK to the source folder."""
    source_dir = source_path.parent

    # Grade layer
    grade_dir = source_dir / GRADE_LAYER
    grade_dir.mkdir(exist_ok=True)
    stem = source_path.stem

    (grade_dir / f"{stem}_classify.json").write_text(
        json.dumps(classify_result, indent=2, default=str), encoding="utf-8")
    (grade_dir / f"{stem}_grade.json").write_text(
        json.dumps(grade_result, indent=2, default=str), encoding="utf-8")

    # Data layer
    data_dir = source_dir / DATA_LAYER
    data_dir.mkdir(exist_ok=True)
    (data_dir / f"{stem}_math.json").write_text(
        json.dumps(math_result, indent=2, default=str), encoding="utf-8")
    (data_dir / f"{stem}_contradiction.json").write_text(
        json.dumps(contradiction_result, indent=2, default=str), encoding="utf-8")
    (data_dir / f"{stem}_production_page.md").write_text(
        production_page, encoding="utf-8")

    print(f"  [round-trip] Written to {grade_dir} and {data_dir}")


# === CANONICAL EXPORT ===

def write_canonical_markdown(source_path: Path, text: str,
                              production_page: str):
    """Export clean canonical markdown to the canonical folder."""
    out_path = CANONICAL_EXPORT / f"{source_path.stem}.md"
    out_path.write_text(production_page, encoding="utf-8")
    print(f"  [canonical] Exported to {out_path}")


# === MANIFEST ===

def write_manifest(stage_dir: Path, filename: str, station: str,
                   status: str, result: dict):
    manifest = {
        "input": filename, "stage": station, "status": status,
        "timestamp": datetime.now().isoformat(),
    }
    manifest.update({k: v for k, v in result.items() if k != "raw_response"})
    out_path = stage_dir / f"{Path(filename).stem}_{station}.json"
    out_path.write_text(json.dumps(manifest, indent=2, default=str),
                        encoding="utf-8")


# === PROCESSED TRACKER ===

PROCESSED_LOG = REFINERY / "09_MEMORY" / "processed_files.json"

def load_processed() -> set:
    if PROCESSED_LOG.exists():
        data = json.loads(PROCESSED_LOG.read_text(encoding="utf-8"))
        return set(data)
    return set()

def save_processed(processed: set):
    PROCESSED_LOG.write_text(json.dumps(sorted(processed)), encoding="utf-8")


# === MAIN PIPELINE ===

def process_file(source_path: Path) -> dict:
    filename = source_path.name
    print(f"\n{'='*60}")
    print(f"PROCESSING: {filename}")
    print(f"Engine: {ENGINE}")
    print(f"{'='*60}")

    # Convert
    print("[1/7] Converting...")
    if source_path.suffix.lower() in (".html", ".htm"):
        text = extract_text_from_html(source_path)
    else:
        text = source_path.read_text(encoding="utf-8", errors="replace")
    conv_path = CONVERSION / f"{source_path.stem}.txt"
    conv_path.write_text(text, encoding="utf-8")
    print(f"  {len(text)} chars, {len(text.split())} words")

    # Classify
    print("[2/7] Classifying...")
    classify_result = station_classify(text, filename)
    write_manifest(ROUTING, filename, "classify",
                   "pass" if classify_result.get("quality", 0) > 0.2 else "review",
                   classify_result)

    # Grade
    print("[3/7] Grading...")
    grade_result = station_grade(text, filename)
    write_manifest(MODEL_STATIONS, filename, "grade",
                   grade_result.get("verdict", "review"), grade_result)

    # Exec summary
    print("[4/7] Executive summary...")
    exec_summary = station_exec_summary(text, filename)

    # Plain English
    print("[5/7] Plain English...")
    plain_english = station_plain_english(text, filename)

    # Math
    print("[6/7] Math extraction...")
    math_result = station_math_extract(text, filename)
    write_manifest(MODEL_STATIONS, filename, "math_verify",
                   "pass" if math_result.get("math_score", 0) > 0.5 else "review",
                   math_result)

    # Contradiction
    print("[7/7] Contradiction check...")
    contradiction_result = station_contradiction_check(text, filename)
    write_manifest(MODEL_STATIONS, filename, "contradiction",
                   "pass" if contradiction_result.get("overall_consistency") == "consistent" else "review",
                   contradiction_result)

    # Compile page
    print("\n[COMPILE] Building 7-layer production page...")
    page = compile_production_page(filename, text, classify_result,
                                   grade_result, exec_summary, plain_english,
                                   math_result, contradiction_result)

    # Write to obsidian export
    out_path = OBSIDIAN_EXPORT / f"{source_path.stem}.md"
    out_path.write_text(page, encoding="utf-8")
    print(f"  Output: {out_path}")

    # Round-trip: write back to source folder
    print("[ROUND-TRIP] Writing outputs back to source folder...")
    write_round_trip(source_path, classify_result, grade_result,
                     math_result, contradiction_result, page)

    # Canonical export
    print("[CANONICAL] Exporting markdown...")
    write_canonical_markdown(source_path, text, page)

    # Full result JSON
    full_result = {
        "source": str(source_path), "output": str(out_path),
        "classify": classify_result, "grade": grade_result,
        "exec_summary": exec_summary, "plain_english": plain_english[:200],
        "math": math_result, "contradiction": contradiction_result,
        "engine": ENGINE, "timestamp": datetime.now().isoformat()
    }
    result_path = WORKFLOW_RUNS / f"{source_path.stem}_pipeline_result.json"
    result_path.write_text(json.dumps(full_result, indent=2, default=str),
                           encoding="utf-8")
    return full_result


def collect_sources(args) -> list[Path]:
    """Collect files to process based on CLI args."""
    sources = []
    if args.files:
        sources = [Path(p) for p in args.files if Path(p).exists()]
    elif args.folder:
        folder = Path(args.folder)
        for ext in ("*.html", "*.htm", "*.md", "*.txt"):
            sources.extend(sorted(folder.rglob(ext)))
    else:
        sources = sorted(INTAKE.glob("*"))
        sources = [s for s in sources if s.is_file()]

    # Filter already-processed if --skip-processed
    if args.skip_processed:
        processed = load_processed()
        before = len(sources)
        sources = [s for s in sources if str(s) not in processed]
        skipped = before - len(sources)
        if skipped:
            print(f"Skipping {skipped} already-processed files")

    return sources


def main():
    global ENGINE

    parser = argparse.ArgumentParser(description="Theophysics Knowledge Refinery Conductor v2")
    parser.add_argument("files", nargs="*", help="Files to process")
    parser.add_argument("--engine", choices=["ollama", "claude-code"],
                        default="ollama", help="LLM engine (default: ollama)")
    parser.add_argument("--folder", help="Process all files in a folder recursively")
    parser.add_argument("--skip-processed", action="store_true",
                        help="Skip files already in the processed log")
    parser.add_argument("--limit", type=int, default=0,
                        help="Max files to process (0 = unlimited)")
    args = parser.parse_args()

    ENGINE = args.engine
    sources = collect_sources(args)

    if args.limit > 0:
        sources = sources[:args.limit]

    if not sources:
        print("No files to process.")
        print(f"  Drop files in {INTAKE}")
        print(f"  Or: python conductor.py file1.html file2.md")
        print(f"  Or: python conductor.py --folder \"Z:\\HTML DUMP\"")
        return

    print(f"Theophysics Knowledge Refinery Conductor v2")
    print(f"Engine: {ENGINE}")
    print(f"Files: {len(sources)}")
    print(f"Output: {OBSIDIAN_EXPORT}")
    print()

    results = []
    processed = load_processed()
    start = time.time()

    for source in sources:
        try:
            result = process_file(source)
            results.append(result)
            processed.add(str(source))
            save_processed(processed)
        except Exception as exc:
            print(f"\nERROR processing {source.name}: {exc}")
            results.append({"source": str(source), "error": str(exc)})

    elapsed = time.time() - start
    successes = sum(1 for r in results if "error" not in r)

    print(f"\n{'='*60}")
    print(f"PIPELINE COMPLETE")
    print(f"  Processed: {len(results)} | Success: {successes}")
    print(f"  Time: {elapsed:.1f}s ({elapsed/max(len(results),1):.1f}s/file)")
    print(f"  Output: {OBSIDIAN_EXPORT}")
    print(f"  Canonical: {CANONICAL_EXPORT}")
    print(f"{'='*60}")

    summary = {
        "run_timestamp": datetime.now().isoformat(),
        "engine": ENGINE, "files_processed": len(results),
        "successes": successes, "elapsed_seconds": round(elapsed, 1),
        "files": [{"source": r.get("source"), "score": r.get("grade",{}).get("overall_score"),
                   "verdict": r.get("grade",{}).get("verdict")} for r in results]
    }
    summary_path = LOGS / f"pipeline_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
