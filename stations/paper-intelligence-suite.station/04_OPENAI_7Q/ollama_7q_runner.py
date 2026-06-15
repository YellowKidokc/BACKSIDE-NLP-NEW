"""
LOCAL OLLAMA 7Q RUNNER
======================
Runs the 7Q and peer-review prompts locally through Ollama.

Default model: qwen2.5:3b

Usage:
  python ollama_7q_runner.py --paper path.html
  python ollama_7q_runner.py --paper path.html --sections classic,claim_inventory,evidence_map,kill_conditions
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
SUITE = HERE.parent
sys.path.insert(0, str(SUITE))
sys.path.insert(0, str(HERE))

from extract_text import read_paper

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
DEFAULT_MODEL = "qwen2.5:3b"

SYSTEM_PROMPT = """You are a rigorous scientific claim-audit assistant.
You are not trying to flatter the author. You identify claim type, evidence,
falsifiability, boundaries, and what is not being claimed.

Return valid JSON only. Do not wrap JSON in markdown fences."""

FORWARD_7Q_PROMPT = """Apply the 7-Question Scientific Method in FORWARD mode.
Keep answers concise. Use at most 3 bullets per array and at most 2 sentences per field.

Q0 posture: What is the paper's stance?
Q1 identity/domain: What object and domain is being studied?
Q2 central claim: What is the main claim?
Q3 evidence: What evidence is presented and what is missing?
Q4 assumptions: What assumptions are load-bearing?
Q5 falsification: What could prove it wrong?
Q6 integration: How does it connect to existing fields?
Q7 strengthening actions: What would most improve it?

PAPER CONTENT:
{content}

Return JSON with keys:
q0, q1, q2, q3, q4, q5, q6, q7, summary, top_3_strengthening_actions"""

REVERSE_7Q_PROMPT = """Apply the 7-Question Scientific Method in REVERSE mode.
Be the best fair adversary. Try to break the paper's central claim.
Keep answers concise. Use at most 3 bullets per array and at most 2 sentences per field.

R1 state the central claim precisely.
R2 list its assumptions.
R3 challenge each assumption.
R4 identify the weakest link.
R5 propose the strongest counter-theory.
R6 assess whether the claim survives.
R7 prescribe the work that would settle the issue.

PAPER CONTENT:
{content}

Return JSON with keys:
r1, r2, r3, r4, r5, r6, r7, verdict, confidence_score"""

SNAPSHOT_PROMPT = """Create a one-screen scientific claim audit snapshot.
Do not market the paper. Do not imply physics proves theology unless the paper explicitly claims that.
Keep every field concise.

Required boxes:
1. Paper ID / Identity Strip
2. One-Sentence Claim
3. Claim Maturity Level
4. FACTS Snapshot
5. 7Q Mini Grid
6. Forward / Reverse Test
7. Evidence Bar
8. Kill Conditions
9. Not Claimed

Claim maturity ladder:
1 Metaphor
2 Analogy
3 Structural Correspondence
4 Formal Model
5 Machine-Checked Theorem
6 Empirical Support
7 Public Proof Claim

PAPER CONTENT:
{content}

Return JSON with keys:
identity_strip, one_sentence_claim, claim_maturity, facts_snapshot, seven_q_mini_grid,
forward_reverse_test, evidence_bar, kill_conditions, not_claimed"""

PROMPT_MODULES = {
    "claim_inventory": "prompts.claim_inventory",
    "equation_audit": "prompts.equation_audit",
    "assumption_stack": "prompts.assumption_stack",
    "kill_conditions": "prompts.kill_conditions",
    "evidence_map": "prompts.evidence_map",
    "physics_comparison": "prompts.physics_comparison",
    "novelty_classification": "prompts.novelty_classification",
    "coherence_score": "prompts.coherence_score",
    "overstatement_detector": "prompts.overstatement_detector",
    "revision_plan": "prompts.revision_plan",
}

def trim_content(content: str, head: int = 3000, tail: int = 700) -> str:
    if len(content) <= head + tail:
        return content
    return f"{content[:head]}\n\n[...middle truncated for local analysis...]\n\n{content[-tail:]}"


def call_ollama_json(prompt: str, model: str, timeout: int = 360, max_tokens: int = 1100) -> dict:
    body = {
        "model": model,
        "stream": False,
        "system": SYSTEM_PROMPT,
        "prompt": prompt,
        "format": "json",
        "options": {
            "temperature": 0.1,
            "num_ctx": 4096,
            "num_predict": max_tokens,
        },
    }
    req = Request(
        OLLAMA_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": f"ollama request failed: {e}"}
    return parse_jsonish(payload.get("response", ""))


def parse_jsonish(text: str) -> dict:
    text = (text or "").strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
    return {"error": "could not parse JSON", "raw_response": text[:4000]}


def import_prompt_module(name: str):
    module_path = PROMPT_MODULES[name]
    components = module_path.split(".")
    mod = __import__(module_path, fromlist=[components[-1]])
    return mod


def run_prompt_section(name: str, content: str, model: str, timeout: int, max_tokens: int) -> dict:
    mod = import_prompt_module(name)
    user = mod.USER_PROMPT_TEMPLATE.format(content=content)
    system = getattr(mod, "SYSTEM_PROMPT", SYSTEM_PROMPT)
    prompt = f"{system}\n\n{user}\n\nReturn valid JSON only."
    return call_ollama_json(prompt, model=model, timeout=timeout, max_tokens=max_tokens)


def run_paper(
    path: Path,
    out_dir: Path,
    model: str,
    sections: list[str],
    head: int,
    tail: int,
    timeout: int,
    classic_tokens: int,
    section_tokens: int,
) -> dict:
    content = trim_content(read_paper(path), head=head, tail=tail)
    out_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "paper": path.name,
        "source_path": str(path),
        "analyzed_at": datetime.now().isoformat(timespec="seconds"),
        "runner": "ollama_7q_runner",
        "model": model,
        "sections_requested": sections,
        "classic_7q": {},
        "snapshot": {},
        "peer_review": {},
    }

    if "classic" in sections:
        print("  local 7Q forward")
        result["classic_7q"]["forward_7q"] = call_ollama_json(
            FORWARD_7Q_PROMPT.format(content=content),
            model=model,
            timeout=timeout,
            max_tokens=classic_tokens,
        )
        print("  local 7Q reverse")
        result["classic_7q"]["reverse_7q"] = call_ollama_json(
            REVERSE_7Q_PROMPT.format(content=content),
            model=model,
            timeout=timeout,
            max_tokens=classic_tokens,
        )

    if "snapshot" in sections:
        print("  local scientific snapshot")
        result["snapshot"] = call_ollama_json(
            SNAPSHOT_PROMPT.format(content=content),
            model=model,
            timeout=timeout,
            max_tokens=section_tokens,
        )

    for name in sections:
        if name in {"classic", "snapshot"}:
            continue
        if name not in PROMPT_MODULES:
            result["peer_review"][name] = {"error": f"unknown section: {name}"}
            continue
        print(f"  local peer review: {name}")
        result["peer_review"][name] = run_prompt_section(
            name,
            content,
            model,
            timeout=timeout,
            max_tokens=section_tokens,
        )

    stem = re.sub(r"[^\w\-]+", "_", path.stem)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = out_dir / f"{stem}_OLLAMA_7Q_{stamp}.json"
    md_path = out_dir / f"{stem}_OLLAMA_7Q_{stamp}.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(md_path, result)
    result["json_path"] = str(json_path)
    result["markdown_path"] = str(md_path)
    return result


def write_markdown(path: Path, result: dict) -> None:
    lines = [
        f"# Local Ollama 7Q: {result['paper']}",
        "",
        f"- Model: `{result['model']}`",
        f"- Generated: `{result['analyzed_at']}`",
        "",
        "## Classic 7Q",
    ]
    classic = result.get("classic_7q") or {}
    for key, value in classic.items():
        lines.extend(["", f"### {key}", "```json", json.dumps(value, ensure_ascii=False, indent=2), "```"])
    if result.get("snapshot"):
        lines.extend(["", "## Paper Snapshot", "```json", json.dumps(result["snapshot"], ensure_ascii=False, indent=2), "```"])
    lines.extend(["", "## Peer Review Sections"])
    for key, value in (result.get("peer_review") or {}).items():
        lines.extend(["", f"### {key}", "```json", json.dumps(value, ensure_ascii=False, indent=2), "```"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper", required=True)
    parser.add_argument("--output", default=None)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--head", type=int, default=3000, help="Leading characters of paper sent to local model")
    parser.add_argument("--tail", type=int, default=700, help="Trailing characters of paper sent to local model")
    parser.add_argument("--timeout", type=int, default=360, help="Seconds to wait for each local model section")
    parser.add_argument("--classic-tokens", type=int, default=1000, help="Max tokens for forward/reverse 7Q")
    parser.add_argument("--section-tokens", type=int, default=1000, help="Max tokens for peer review sections")
    parser.add_argument(
        "--sections",
        default="classic,snapshot",
        help="Comma-separated: classic plus any prompt module names, or all",
    )
    args = parser.parse_args()

    sections = [s.strip() for s in args.sections.split(",") if s.strip()]
    if "all" in sections:
        sections = ["classic", *PROMPT_MODULES.keys()]
    paper = Path(args.paper).resolve()
    out_dir = Path(args.output) if args.output else paper.parent / "_OLLAMA_7Q_ANALYSIS"
    result = run_paper(
        paper,
        out_dir,
        args.model,
        sections,
        head=args.head,
        tail=args.tail,
        timeout=args.timeout,
        classic_tokens=args.classic_tokens,
        section_tokens=args.section_tokens,
    )
    print(json.dumps({
        "status": "ok",
        "json": result["json_path"],
        "markdown": result["markdown_path"],
        "model": result["model"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
