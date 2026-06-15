"""
Theophysics Knowledge Refinery Conductor
Processes content through the pipeline: intake -> classify -> grade -> compile -> export
Uses Ollama for all LLM checkpoints.
POF 2828 | May 2026
"""
from __future__ import annotations
import json
import re
import sys
import time
import hashlib
import urllib.request
from datetime import datetime
from pathlib import Path
from html.parser import HTMLParser

# === CONFIGURATION ===
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi4:latest"
REFINERY = Path(r"X:\knowledge-refinery")
FAP_PROMPTS = Path(r"D:\FAP\wiki\prompts")
OBSIDIAN_EXPORT = REFINERY / "07_OBSIDIAN_EXPORT"
HTML_REPORTS = REFINERY / "06_HTML_REPORTS"
LOGS = REFINERY / "12_HEALTH"

INTAKE = REFINERY / "00_INTAKE"
CONVERSION = REFINERY / "01_CONVERSION"
NORMALIZATION = REFINERY / "02_NORMALIZATION"
ROUTING = REFINERY / "03_ROUTING"
MODEL_STATIONS = REFINERY / "04_MODEL_STATIONS"
WORKFLOW_RUNS = REFINERY / "05_WORKFLOW_RUNS"
ARCHIVE = REFINERY / "08_ARCHIVE"
MEMORY = REFINERY / "09_MEMORY"


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
        if tag in ("br", "p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "section"):
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


# === OLLAMA INTERFACE ===
def ollama_generate(prompt: str, max_tokens: int = 4096) -> str:
    """Call Ollama and return the full response text."""
    body = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": max_tokens, "temperature": 0.3}
    }).encode()
    req = urllib.request.Request(OLLAMA_URL, data=body,
                                headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
            return data.get("response", "")
    except Exception as exc:
        return f"OLLAMA_ERROR: {exc}"


def extract_json(text: str) -> dict | None:
    """Try to pull JSON from LLM output."""
    # Try direct parse
    try:
        return json.loads(text.strip())
    except Exception:
        pass
    # Try finding JSON block
    m = re.search(r'\{[\s\S]*\}', text)
    if m:
        try:
            return json.loads(m.group())
        except Exception:
            pass
    return None


# === PIPELINE STATIONS ===

def station_classify(text: str, filename: str) -> dict:
    """Station 1: Classify the document."""
    prompt_template = (FAP_PROMPTS / "classify_document.md").read_text(encoding="utf-8")
    # Truncate to ~6000 chars for LLM context
    doc_text = text[:6000]
    prompt = prompt_template.replace("{{INPUT}}", doc_text)
    print(f"  [classify] Running on {filename}...")
    raw = ollama_generate(prompt)
    result = extract_json(raw)
    if result is None:
        result = {"type": "unknown", "laws": [], "topics": [], "quality": 0.0,
                  "summary": "Classification failed", "raw_response": raw[:500]}
    result["source_file"] = filename
    result["station"] = "classify"
    result["timestamp"] = datetime.now().isoformat()
    return result


def station_grade(text: str, filename: str) -> dict:
    """Station 2: Grade the paper."""
    prompt_template = (FAP_PROMPTS / "grade_paper.md").read_text(encoding="utf-8")
    doc_text = text[:6000]
    prompt = prompt_template.replace("{{INPUT}}", doc_text)
    print(f"  [grade] Running on {filename}...")
    raw = ollama_generate(prompt)
    result = extract_json(raw)
    if result is None:
        result = {"overall_score": 0.0, "verdict": "review",
                  "raw_response": raw[:500]}
    result["source_file"] = filename
    result["station"] = "grade"
    result["timestamp"] = datetime.now().isoformat()
    return result


def station_exec_summary(text: str, filename: str) -> str:
    """Station 3: Generate executive summary (Layer 1)."""
    doc_text = text[:4000]
    prompt = f"""You are summarizing a Theophysics research paper for a busy reader.
Write a 2-3 sentence executive summary. No jargon. What does it claim and why does it matter?

DOCUMENT:
{doc_text}

EXECUTIVE SUMMARY:"""
    print(f"  [exec_summary] Running on {filename}...")
    return ollama_generate(prompt, max_tokens=300).strip()


def station_plain_english(text: str, filename: str) -> str:
    """Station 4: Generate plain English explanation (Layer 2)."""
    doc_text = text[:4000]
    prompt = f"""Explain this paper in plain English. 200-400 words. No jargon, no citations, no equations.
Write as if explaining to someone over coffee. Use "you" and "I". Be direct.

DOCUMENT:
{doc_text}

PLAIN ENGLISH EXPLANATION:"""
    print(f"  [plain_english] Running on {filename}...")
    return ollama_generate(prompt, max_tokens=600).strip()


def station_math_extract(text: str, filename: str) -> dict:
    """Station 5: Extract and verify all math/equations."""
    doc_text = text[:8000]
    prompt = f"""You are a mathematical reviewer. Extract ALL equations, formulas, and mathematical expressions from this document.
For each one:
1. State the equation
2. Identify the variables
3. Check if the math is internally consistent
4. Flag any errors or unsupported leaps

Return ONLY valid JSON:
{{
  "equations_found": [
    {{"equation": "...", "variables": ["..."], "valid": true/false, "notes": "..."}}
  ],
  "math_score": 0.0-1.0,
  "errors": ["list of math errors if any"],
  "total_equations": 0
}}

DOCUMENT:
{doc_text}"""
    print(f"  [math_extract] Running on {filename}...")
    raw = ollama_generate(prompt, max_tokens=2000)
    result = extract_json(raw)
    if result is None:
        result = {"equations_found": [], "math_score": 0.0, "errors": ["Extraction failed"],
                  "total_equations": 0, "raw_response": raw[:500]}
    result["station"] = "math_extract"
    return result


def station_contradiction_check(text: str, filename: str) -> dict:
    """Station 6: Check for internal contradictions."""
    doc_text = text[:6000]
    prompt = f"""You are a logical consistency checker. Read this document and identify:
1. Any claims that contradict each other within the document
2. Any claims that contradict standard physics or established mathematics
3. Any logical gaps where a conclusion doesn't follow from the premises

Return ONLY valid JSON:
{{
  "contradictions": [
    {{"claim_a": "...", "claim_b": "...", "severity": "high/medium/low", "explanation": "..."}}
  ],
  "logical_gaps": [
    {{"location": "...", "issue": "...", "severity": "high/medium/low"}}
  ],
  "contradiction_score": 0.0-1.0,
  "overall_consistency": "consistent/minor_issues/significant_issues"
}}

DOCUMENT:
{doc_text}"""
    print(f"  [contradiction] Running on {filename}...")
    raw = ollama_generate(prompt, max_tokens=2000)
    result = extract_json(raw)
    if result is None:
        result = {"contradictions": [], "logical_gaps": [], "contradiction_score": 0.0,
                  "overall_consistency": "unknown", "raw_response": raw[:500]}
    result["station"] = "contradiction_check"
    return result


# === PAGE COMPILER ===

def compile_production_page(filename: str, text: str,
                            classify_result: dict,
                            grade_result: dict,
                            exec_summary: str,
                            plain_english: str,
                            math_result: dict,
                            contradiction_result: dict) -> str:
    """Compile all station outputs into a 7-layer production vault page."""

    title = classify_result.get("suggested_title", filename.replace(".html", "").replace("-", " ").title())
    paper_id = hashlib.md5(filename.encode()).hexdigest()[:8].upper()
    laws = classify_result.get("laws", [])
    topics = classify_result.get("topics", [])
    quality = classify_result.get("quality", 0.0)
    overall_score = grade_result.get("overall_score", 0.0)
    verdict = grade_result.get("verdict", "review").upper()
    math_score = math_result.get("math_score", 0.0)
    contradiction_score = contradiction_result.get("contradiction_score", 0.0)
    consistency = contradiction_result.get("overall_consistency", "unknown")
    dims = grade_result.get("dimensions", {})

    # Determine epistemic state from scores
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
reading_level: 0.0
created: "{datetime.now().strftime('%Y-%m-%d')}"
updated: "{datetime.now().strftime('%Y-%m-%d')}"
author: POF 2828
ai_partners: ["opus", "phi4"]
tags: {json.dumps(topics[:10])}
provenance: pipeline
depends_on: []
supports: []
relates_to: []
contradicts: []
supersedes: []
related: []
source_file: "{filename}"
pipeline_version: "conductor_v1"
---

> [!metadata] Facts
> **Paper ID:** REF-{paper_id}
> **Status:** pipeline_processed
> **Epistemic State:** {epistemic}
> **Verdict:** {verdict}
> **Composite Score:** {overall_score}
> **Math Score:** {math_score}
> **Contradiction Score:** {contradiction_score} ({consistency})
> **Provenance:** pipeline
> **Laws:** {', '.join(laws) if laws else '[pending]'}

---

## Layer 1 — Executive Summary

> [!abstract] Executive Summary
> {exec_summary}

---

## Layer 2 — Plain English

{plain_english}

---

## Layer 3 — Article

[Source: `{filename}`]

{text[:10000]}

{"[... truncated for vault page — see source file for full text ...]" if len(text) > 10000 else ""}

---

## Layer 4 — Academic Summary

> [!note] Academic Summary
> **Key Claims:** [pending — requires manual review]
> **Methodology:** Cross-domain structural analysis (physics ↔ theology)
> **Limitations:** [pending]
> **Falsification Criteria:** [pending]

---

## Layer 5 — Cross-References

**Laws touched:** {', '.join(laws) if laws else '[pending]'}
**Axioms:** [pending — axiom mapper not yet run]
**Related papers:** [pending]
**Contradictions:** {len(contradiction_result.get('contradictions', []))} found
**Logical gaps:** {len(contradiction_result.get('logical_gaps', []))} found

---

## Layer 6 — Data & Evidence

### Grading Results
| Dimension | Score |
|-----------|-------|
| Overall | {overall_score} |
| Coherence | {dims.get('coherence', 'n/a')} |
| Voice Authenticity | {dims.get('voice_authenticity', 'n/a')} |
| Cross-Domain | {dims.get('cross_domain_strength', 'n/a')} |
| Axiom Coverage | {dims.get('axiom_coverage', 'n/a')} |
| Publish Readiness | {dims.get('publish_readiness', 'n/a')} |

### Math Inventory
**Equations found:** {math_result.get('total_equations', 0)}
**Math score:** {math_score}
**Errors:** {json.dumps(math_result.get('errors', []))}

### Contradiction Check
**Internal contradictions:** {len(contradiction_result.get('contradictions', []))}
**Logical gaps:** {len(contradiction_result.get('logical_gaps', []))}
**Consistency:** {consistency}

---

## Layer 7A — Framework Impact

[pending — requires manual assessment]

---

## Layer 7B — Open Obligations

**Grade issues:** {json.dumps(grade_result.get('issues', []), indent=2)}
**Recommended action:** {grade_result.get('recommended_action', 'review')}
**Revision notes:** {grade_result.get('revision_notes', '[none]')}
"""
    return page


# === MANIFEST WRITER ===

def write_manifest(stage_dir: Path, filename: str, station: str,
                   status: str, result: dict):
    """Write a station manifest JSON."""
    manifest = {
        "input": filename,
        "stage": station,
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "outputs": [],
        "next_routes": []
    }
    manifest.update({k: v for k, v in result.items()
                     if k not in ("raw_response",)})
    out_path = stage_dir / f"{Path(filename).stem}_{station}.json"
    out_path.write_text(json.dumps(manifest, indent=2, default=str),
                        encoding="utf-8")
    return out_path


# === MAIN CONDUCTOR ===

def process_file(source_path: Path) -> dict:
    """Run a single file through the full pipeline."""
    filename = source_path.name
    print(f"\n{'='*60}")
    print(f"PROCESSING: {filename}")
    print(f"{'='*60}")

    # Stage 1: Convert
    print("[1/7] Converting HTML to text...")
    if source_path.suffix.lower() in (".html", ".htm"):
        text = extract_text_from_html(source_path)
    else:
        text = source_path.read_text(encoding="utf-8", errors="replace")

    conv_path = CONVERSION / f"{source_path.stem}.txt"
    conv_path.write_text(text, encoding="utf-8")
    print(f"  Converted: {len(text)} chars, {len(text.split())} words")

    # Stage 2: Classify
    print("[2/7] Classifying...")
    classify_result = station_classify(text, filename)
    write_manifest(ROUTING, filename, "classify",
                   "pass" if classify_result.get("quality", 0) > 0.2 else "review",
                   classify_result)
    print(f"  Type: {classify_result.get('type')}, Quality: {classify_result.get('quality')}")
    print(f"  Laws: {classify_result.get('laws')}")

    # Stage 3: Grade
    print("[3/7] Grading...")
    grade_result = station_grade(text, filename)
    write_manifest(MODEL_STATIONS, filename, "grade",
                   grade_result.get("verdict", "review"),
                   grade_result)
    print(f"  Score: {grade_result.get('overall_score')}, Verdict: {grade_result.get('verdict')}")

    # Stage 4: Executive Summary
    print("[4/7] Generating executive summary...")
    exec_summary = station_exec_summary(text, filename)

    # Stage 5: Plain English
    print("[5/7] Generating plain English explanation...")
    plain_english = station_plain_english(text, filename)

    # Stage 6: Math extraction
    print("[6/7] Extracting and checking math...")
    math_result = station_math_extract(text, filename)
    write_manifest(MODEL_STATIONS, filename, "math_verify",
                   "pass" if math_result.get("math_score", 0) > 0.5 else "review",
                   math_result)
    print(f"  Equations: {math_result.get('total_equations')}, Score: {math_result.get('math_score')}")

    # Stage 7: Contradiction check
    print("[7/7] Checking for contradictions...")
    contradiction_result = station_contradiction_check(text, filename)
    write_manifest(MODEL_STATIONS, filename, "contradiction",
                   "pass" if contradiction_result.get("overall_consistency") == "consistent" else "review",
                   contradiction_result)
    print(f"  Consistency: {contradiction_result.get('overall_consistency')}")

    # Compile production page
    print("\n[COMPILE] Building 7-layer production page...")
    page = compile_production_page(
        filename, text, classify_result, grade_result,
        exec_summary, plain_english, math_result, contradiction_result
    )
    out_name = f"{source_path.stem}.md"
    out_path = OBSIDIAN_EXPORT / out_name
    out_path.write_text(page, encoding="utf-8")
    print(f"  Output: {out_path}")

    # Write full pipeline result JSON
    full_result = {
        "source": str(source_path),
        "output": str(out_path),
        "classify": classify_result,
        "grade": grade_result,
        "exec_summary": exec_summary,
        "plain_english": plain_english[:200],
        "math": math_result,
        "contradiction": contradiction_result,
        "timestamp": datetime.now().isoformat()
    }
    result_path = WORKFLOW_RUNS / f"{source_path.stem}_pipeline_result.json"
    result_path.write_text(json.dumps(full_result, indent=2, default=str),
                           encoding="utf-8")

    return full_result


def main():
    """Process files from intake or from command-line args."""
    # Accept paths as args, or scan intake folder
    if len(sys.argv) > 1:
        sources = [Path(p) for p in sys.argv[1:] if Path(p).exists()]
    else:
        sources = sorted(INTAKE.glob("*"))
        sources = [s for s in sources if s.is_file()]

    if not sources:
        print("No files to process.")
        print(f"  Drop files in {INTAKE}")
        print(f"  Or pass paths as arguments: python conductor.py file1.html file2.md")
        return

    print(f"Theophysics Knowledge Refinery Conductor")
    print(f"Model: {OLLAMA_MODEL}")
    print(f"Files to process: {len(sources)}")
    print(f"Output: {OBSIDIAN_EXPORT}")
    print()

    results = []
    start = time.time()

    for source in sources:
        try:
            result = process_file(source)
            results.append(result)
        except Exception as exc:
            print(f"\nERROR processing {source.name}: {exc}")
            results.append({"source": str(source), "error": str(exc)})

    elapsed = time.time() - start
    successes = sum(1 for r in results if "error" not in r)
    failures = sum(1 for r in results if "error" in r)

    print(f"\n{'='*60}")
    print(f"PIPELINE COMPLETE")
    print(f"  Processed: {len(results)} files")
    print(f"  Success: {successes}")
    print(f"  Failed: {failures}")
    print(f"  Time: {elapsed:.1f}s ({elapsed/max(len(results),1):.1f}s per file)")
    print(f"  Output: {OBSIDIAN_EXPORT}")
    print(f"{'='*60}")

    # Write run summary
    summary = {
        "run_timestamp": datetime.now().isoformat(),
        "model": OLLAMA_MODEL,
        "files_processed": len(results),
        "successes": successes,
        "failures": failures,
        "elapsed_seconds": round(elapsed, 1),
        "files": [{"source": r.get("source", "?"),
                   "output": r.get("output", "?"),
                   "score": r.get("grade", {}).get("overall_score", "?"),
                   "verdict": r.get("grade", {}).get("verdict", "?")}
                  for r in results]
    }
    summary_path = LOGS / f"pipeline_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"  Run log: {summary_path}")


if __name__ == "__main__":
    main()
