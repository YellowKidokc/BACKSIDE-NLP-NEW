"""
L4: OPENAI 7Q RUNNER
====================
Runs the 7-Question Scientific Method on each paper — FORWARD and REVERSE.
NOT for self-validation. For strengthening: more citations, more theories,
better questions, deeper understanding.

Output goes DIRECTLY into each paper's vault folder as a product.
"""
import os, json, re, sys
from pathlib import Path
from datetime import datetime

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from extract_text import read_paper

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
except Exception:
    client = None

MODEL = "gpt-4o-mini"
SUPPORTED_SUFFIXES = {".md", ".markdown", ".txt", ".html", ".htm"}

SYSTEM_PROMPT = """You are a rigorous academic analyst specializing in cross-domain research.
You apply the 7-Question Scientific Method with maximum intellectual honesty.
Your goal is NOT to validate claims — it is to STRENGTHEN the paper by identifying:
- Missing citations and supporting literature
- Alternative theories that should be addressed
- Stronger theoretical frameworks
- Deep conceptual questions the paper raises but doesn't answer
Be direct. Be specific. Name real theories, real authors, real journals where possible."""


FORWARD_7Q_PROMPT = """Apply the 7-Question Scientific Method (FORWARD — Classification Mode) to this paper.

The 7 Questions:
Q0: POSTURE — What is the paper's fundamental stance toward reality? (humility/surrender vs assertion)
Q1: DOMAIN — What field(s) does this paper operate in?
Q2: CLAIM — What is the central claim?
Q3: EVIDENCE — What evidence is presented? What's missing?
Q4: ASSUMPTIONS — What hidden assumptions are load-bearing?
Q5: FALSIFICATION — How could this claim be proven wrong?
Q6: INTEGRATION — How does this connect to existing literature?
Q7: STRENGTH GAPS — What citations, theories, or frameworks would most strengthen this paper?

For EACH question, be specific and actionable.
For Q7 especially: name real papers, authors, journals, and theories David should engage with.

PAPER CONTENT:
{content}

Respond in structured JSON with keys: q0, q1, q2, q3, q4, q5, q6, q7, summary, top_3_strengthening_actions"""

REVERSE_7Q_PROMPT = """Apply the 7-Question Scientific Method (REVERSE — Proof by Exhaustive Elimination) to this paper.

The goal: Attempt to DISPROVE the central claim by working backwards.
If the claim survives, it is strengthened. If it fails, we know exactly where.

Reverse 7Q Process:
R1: STATE the central claim precisely
R2: LIST all assumptions the claim depends on
R3: CHALLENGE each assumption — what would have to be true for it to fail?
R4: IDENTIFY the single weakest link in the logical chain
R5: PROPOSE the strongest possible counter-theory
R6: ASSESS — does the claim survive this attack? What remains unresolved?
R7: PRESCRIBE — what specific work would settle the remaining question?

Be the best possible adversary. Then report honestly.

PAPER CONTENT:
{content}

Respond in structured JSON with keys: r1, r2, r3, r4, r5, r6, r7, verdict, confidence_score"""


def call_openai(prompt, max_tokens=2000):
    if not client:
        return {"error": "OpenAI not configured. Set OPENAI_API_KEY env variable."}
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        text = response.choices[0].message.content
        return json.loads(text)
    except Exception as e:
        return {"error": str(e)}


def run_paper(paper_path, vault_output_dir=None):
    paper = Path(paper_path)
    content = read_paper(paper)

    # Truncate if very long (keep first 6000 chars for API efficiency)
    if len(content) > 6000:
        content_trimmed = content[:6000] + "\n\n[...truncated for analysis...]"
    else:
        content_trimmed = content

    print(f"  Running 7Q FORWARD on: {paper.name}")
    forward = call_openai(FORWARD_7Q_PROMPT.format(content=content_trimmed), max_tokens=2500)

    print(f"  Running 7Q REVERSE on: {paper.name}")
    reverse = call_openai(REVERSE_7Q_PROMPT.format(content=content_trimmed), max_tokens=2000)

    result = {
        "paper": paper.name,
        "analyzed_at": datetime.now().isoformat(),
        "model": MODEL,
        "forward_7q": forward,
        "reverse_7q": reverse,
    }

    # Write to vault output dir if specified, else alongside paper
    if vault_output_dir:
        out_dir = Path(vault_output_dir)
    else:
        out_dir = paper.parent / "_7Q_ANALYSIS"
    out_dir.mkdir(parents=True, exist_ok=True)

    stem = re.sub(r'[^\w\-]', '_', paper.stem)
    out_path = out_dir / f"{stem}_7Q_{datetime.now().strftime('%Y%m%d')}.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')

    # Also write a readable markdown version
    md_path = out_dir / f"{stem}_7Q_{datetime.now().strftime('%Y%m%d')}.md"
    _write_markdown(md_path, paper.name, forward, reverse)

    print(f"  Saved: {out_path.name}")
    return result


def _write_markdown(path, paper_name, forward, reverse):
    lines = [
        f"# 7Q Analysis: {paper_name}",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Model: {MODEL}*",
        "",
        "---",
        "",
        "## FORWARD 7Q — Classification Mode",
        "",
    ]
    fwd_labels = {
        'q0':'Q0: Posture', 'q1':'Q1: Domain', 'q2':'Q2: Claim',
        'q3':'Q3: Evidence', 'q4':'Q4: Assumptions', 'q5':'Q5: Falsification',
        'q6':'Q6: Integration', 'q7':'Q7: Strength Gaps',
        'summary':'Summary', 'top_3_strengthening_actions':'Top 3 Actions',
    }
    for key, label in fwd_labels.items():
        val = forward.get(key, '')
        if isinstance(val, list):
            val = '\n'.join(f"- {v}" for v in val)
        elif isinstance(val, dict):
            val = json.dumps(val, indent=2)
        lines.append(f"### {label}")
        lines.append(str(val))
        lines.append("")

    lines += ["---", "", "## REVERSE 7Q — Proof by Exhaustive Elimination", ""]
    rev_labels = {
        'r1':'R1: Claim', 'r2':'R2: Assumptions', 'r3':'R3: Challenge',
        'r4':'R4: Weakest Link', 'r5':'R5: Counter-Theory',
        'r6':'R6: Assessment', 'r7':'R7: Prescription',
        'verdict':'Verdict', 'confidence_score':'Confidence Score',
    }
    for key, label in rev_labels.items():
        val = reverse.get(key, '')
        if isinstance(val, list):
            val = '\n'.join(f"- {v}" for v in val)
        lines.append(f"### {label}")
        lines.append(str(val))
        lines.append("")

    path.write_text('\n'.join(lines), encoding='utf-8')


def run_folder(folder_path, vault_base=None):
    folder = Path(folder_path)
    papers = sorted(
        f for f in folder.iterdir()
        if f.is_file()
        and f.suffix.lower() in SUPPORTED_SUFFIXES
        and re.match(r'^\d{2}', f.name)
        and not f.name.startswith('00')
    )
    print(f"\nRunning 7Q on {len(papers)} papers in: {folder.name}")
    results = []
    for p in papers:
        vault_out = None
        if vault_base:
            vault_out = Path(vault_base) / "_7Q_ANALYSIS"
        r = run_paper(p, vault_out)
        results.append({'paper': r['paper'],
                        'verdict': r['reverse_7q'].get('verdict',''),
                        'confidence': r['reverse_7q'].get('confidence_score',''),
                        'top_actions': r['forward_7q'].get('top_3_strengthening_actions','')})
    print(f"\nComplete. {len(results)} papers processed.")
    return results


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--paper', help='Single paper path (.md, .txt, .html, .htm)')
    parser.add_argument('--folder', help='Series folder path')
    parser.add_argument('--vault-output', help='Vault output directory for 7Q results')
    args = parser.parse_args()
    if args.paper:
        run_paper(args.paper, args.vault_output)
    elif args.folder:
        run_folder(args.folder, args.vault_output)
    else:
        print("Usage: python seven_q_runner.py --paper path.(md|txt|html)  OR  --folder path/")
