"""
PAPER INTELLIGENCE — 8-PROMPT o3 SYSTEM
=========================================
Each prompt is focused, cached independently, and run against o3.

CORE (run always):
  1. UPGRADE PATH — specific concrete changes ranked by impact
  2. OVERCLAIM AUDIT — find every overclaim with exact quotes
  3. MISSING EQUATIONS — equations that should appear but don't
  4. ANALOGY vs ISOMORPHISM — the credibility test

PUBLISH (run on demand):
  5. HOSTILE REVIEWER — full reviewer report
  6. PRIOR ART CHECK — similar published work with citations
  7. THE ONE QUESTION — weakest point exposed and defended
  8. AUDIENCE GATEWAY — rewrites for 3 audiences

Cost estimate: ~$0.15-0.25 per prompt × 4-8 prompts = $0.60-2.00 per paper.
All results cached — re-runs are free.
"""

import os
import json
import re
import time
from pathlib import Path
from datetime import datetime
from typing import Optional

try:
    from openai import OpenAI
    _client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    HAS_OPENAI = True
except Exception:
    _client = None
    HAS_OPENAI = False

MODEL = "o3"

# Cost per 1M tokens
COST_RATES = {'input': 10.0, 'output': 40.0}

# ═══════════════════════════════════════════════════════════════
# THE 8 PROMPTS
# ═══════════════════════════════════════════════════════════════

PROMPTS = {
    '1_upgrade_path': {
        'label': 'UPGRADE PATH',
        'tier': 'core',
        'prompt': """Read this paper carefully. Then give me 4-6 specific, concrete changes \
I could make RIGHT NOW that would meaningfully improve this paper's \
persuasive power and intellectual rigor.

Not vague advice like "add more citations." Specific: which paragraph, \
which claim, what to add or cut or rewrite. Each suggestion should include:

(a) What to change (quote the specific sentence or section)
(b) Why it's weak right now (what a skeptic would say)
(c) What to replace it with or add (be specific enough that I could \
    do it in 15 minutes)

Rank them by impact — biggest improvement first.""",
    },

    '2_overclaim_audit': {
        'label': 'OVERCLAIM AUDIT',
        'tier': 'core',
        'prompt': """Go through this paper and find every place where the language claims \
more than the evidence actually supports. I'm looking for:

- "Proves" when we mean "suggests"
- "Identical" when we mean "structurally similar"
- "Must be" when we mean "is consistent with"
- Causal claims without causal evidence
- Quantitative precision stated without quantitative backing
- Any claim that would make a careful physicist wince

For each one:
(a) Quote the exact sentence
(b) What it currently claims
(c) What the evidence actually supports
(d) Suggested rewording that's honest but still strong

I'd rather be precise and credible than bold and dismissable.""",
    },

    '3_missing_equations': {
        'label': 'MISSING EQUATIONS',
        'tier': 'core',
        'prompt': """Based on the physics concepts discussed in this paper, are there \
equations that SHOULD appear but don't? Specifically:

- Equations the text describes in words but never writes formally
- Standard physics equations that the argument depends on but doesn't show
- Equations that would make a vague claim precise and testable
- Substitution maps that are claimed but not demonstrated step-by-step

For each missing equation:
(a) What it is (name and standard form)
(b) Where in the paper it belongs
(c) How it strengthens the argument (what does showing it prove \
    that words alone don't?)

Don't suggest equations for decoration. Only ones that carry load.""",
    },

    '4_analogy_vs_isomorphism': {
        'label': 'ANALOGY vs ISOMORPHISM AUDIT',
        'tier': 'core',
        'prompt': """This paper claims structural isomorphisms between physics and theology — \
not metaphors, not analogies, but shared mathematical architecture.

For EACH physics↔theology mapping in this paper, answer:

(a) Is this a genuine isomorphism (same mathematical structure, \
    mutual constraints, testable predictions in both domains)?
(b) Or is this an analogy (similar-sounding, illustrative, but \
    no mathematical teeth)?
(c) If analogy: can it be UPGRADED to isomorphism? What specific \
    equation or constraint would need to be shown?
(d) If isomorphism: what prediction does it make in the theology \
    domain that would be SURPRISING if true? (That's the test — \
    real isomorphisms predict things analogies can't.)

Be honest. A paper with 3 real isomorphisms and 2 acknowledged \
analogies is stronger than one that claims 5 isomorphisms and \
gets caught on 2.""",
    },

    '5_hostile_reviewer': {
        'label': 'HOSTILE REVIEWER',
        'tier': 'publish',
        'prompt': """You are reviewing this paper for a serious interdisciplinary journal. \
You are competent in both physics and theology. You are not hostile \
to the premise but you have high standards.

Write a 1-page reviewer report that includes:

1. ONE thing the paper does genuinely well (be specific)
2. THREE things that need to be fixed before publication \
   (be specific — cite paragraphs)
3. ONE claim that should be removed entirely (and why)
4. ONE citation that is conspicuously absent (author, year, \
   why it matters)
5. Your recommendation: Accept / Revise / Reject, with one \
   sentence explaining why""",
    },

    '6_prior_art': {
        'label': 'PRIOR ART CHECK',
        'tier': 'publish',
        'prompt': """Has anyone published a paper that makes a similar claim to \
this one? Search specifically for:

- Phase transition models applied to religious conversion
- Thermodynamic models of sin/grace/salvation
- Information-theoretic models of theology
- Coherence/decoherence applied to moral or spiritual states
- Any physics-theology isomorphism paper (not metaphor papers — \
  papers claiming structural identity)

For each paper you find:
(a) Full citation
(b) How it overlaps with mine
(c) How mine differs or extends it
(d) Whether I should cite it (and where in my paper)

If you find nothing: say so, and explain why this gap exists. \
Is it because nobody thought of it, or because serious researchers \
considered it and rejected it? That distinction matters.""",
    },

    '7_one_question': {
        'label': 'THE ONE QUESTION',
        'tier': 'publish',
        'prompt': """If a serious physicist read this paper and could ask me ONE question \
in a Q&A session — the question designed to expose the weakest point \
of my argument — what would that question be?

Then: write the best possible answer to that question. The answer I \
should have ready before I publish.""",
    },

    '8_audience_gateway': {
        'label': 'AUDIENCE GATEWAY',
        'tier': 'publish',
        'prompt': """This paper currently reads at what level? (Be honest about jargon \
density and assumed knowledge.)

Then rewrite JUST the opening 3 paragraphs for each audience:

(a) A physicist who thinks theology is unscientific
(b) A pastor who hasn't taken physics since high school
(c) A smart 19-year-old who's curious but knows neither field

Don't dumb it down. Translate the entry point. The core argument \
stays the same — the doorway changes.""",
    },
}

DEVELOPER_CONTEXT = """You are analyzing a paper from the Theophysics research program.

Theophysics is a formal axiom system that maps theology to physics:
- 193 axioms deriving from 3 primitives: Existence, Distinction, Information
- Master Equation: χ = ∭ (G·M·E·S·T·K·R·Q·F·C) dx dy dt
- 10 Laws mapping physics forces to theological concepts (Gravitation/Grace, EM/Truth, Strong/Love, etc.)
- 24 Properties establishing a God ↔ Math isomorphism
- 9 Fruits of the Spirit mapped to physics equations

The author is a serious independent researcher. He wants REAL adversarial feedback,
not validation. Be specific: name real theories, real authors, real equations.
Quote specific sentences from the paper when critiquing."""


def _call_o3(prompt: str, content: str, title: str) -> tuple[str, dict]:
    """Call o3 with a focused prompt. Returns (text, meta)."""
    full_prompt = f"""PAPER: "{title}"

CONTENT:
{content}

{prompt}"""

    response = _client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "developer", "content": DEVELOPER_CONTEXT},
            {"role": "user", "content": full_prompt}
        ],
        max_completion_tokens=8000,
    )

    text = response.choices[0].message.content
    usage = response.usage

    input_tokens = usage.prompt_tokens if usage else 0
    output_tokens = usage.completion_tokens if usage else 0
    total_tokens = usage.total_tokens if usage else 0
    cost = (input_tokens * COST_RATES['input'] + output_tokens * COST_RATES['output']) / 1_000_000

    meta = {
        'model': MODEL,
        'input_tokens': input_tokens,
        'output_tokens': output_tokens,
        'total_tokens': total_tokens,
        'cost_usd': round(cost, 4),
        'timestamp': datetime.now().isoformat(),
    }

    return text, meta


def run_prompt(prompt_key: str, paper_path: str,
               cache_dir: Optional[str] = None) -> dict:
    """
    Run a single prompt against a paper.
    Returns {'text': str, 'meta': dict} or {'error': str}.
    """
    if not HAS_OPENAI:
        return {'error': 'OpenAI not configured'}

    if prompt_key not in PROMPTS:
        return {'error': f'Unknown prompt: {prompt_key}'}

    paper = Path(paper_path)
    title = paper.stem.replace('_', ' ')
    config = PROMPTS[prompt_key]

    # Check cache
    if cache_dir:
        cache_path = Path(cache_dir) / f"{paper.stem}_{prompt_key}.json"
        if cache_path.exists():
            cached = json.loads(cache_path.read_text(encoding='utf-8'))
            print(f"    [{config['label']}] cached ({cached.get('meta', {}).get('total_tokens', '?')} tokens)")
            return cached

    # Read paper
    text = paper.read_text(encoding='utf-8', errors='replace')
    if len(text) > 12000:
        text = text[:12000] + "\n\n[...truncated...]"

    print(f"    [{config['label']}] calling {MODEL}...", end='', flush=True)

    try:
        result_text, meta = _call_o3(config['prompt'], text, title)
        result = {'text': result_text, 'meta': meta, 'prompt_key': prompt_key}

        print(f" {meta['total_tokens']:,} tokens, ${meta['cost_usd']:.4f}")

        # Cache
        if cache_dir:
            Path(cache_dir).mkdir(parents=True, exist_ok=True)
            cache_path = Path(cache_dir) / f"{paper.stem}_{prompt_key}.json"
            cache_path.write_text(json.dumps(result, indent=2, ensure_ascii=False),
                                  encoding='utf-8')

        return result

    except Exception as e:
        print(f" ERROR: {e}")
        return {'error': str(e), 'prompt_key': prompt_key}


def run_core(paper_path: str, cache_dir: Optional[str] = None) -> dict:
    """Run core prompts 1-4. Returns {prompt_key: result}."""
    results = {}
    for key, config in PROMPTS.items():
        if config['tier'] == 'core':
            results[key] = run_prompt(key, paper_path, cache_dir)
            time.sleep(0.5)  # rate limit courtesy
    return results


def run_publish(paper_path: str, cache_dir: Optional[str] = None) -> dict:
    """Run publish prompts 5-8. Returns {prompt_key: result}."""
    results = {}
    for key, config in PROMPTS.items():
        if config['tier'] == 'publish':
            results[key] = run_prompt(key, paper_path, cache_dir)
            time.sleep(0.5)
    return results


def run_all(paper_path: str, cache_dir: Optional[str] = None) -> dict:
    """Run all 8 prompts. Returns {prompt_key: result}."""
    results = {}
    for key in PROMPTS:
        results[key] = run_prompt(key, paper_path, cache_dir)
        time.sleep(0.5)
    return results


def write_intel_report(results: dict, paper_name: str, output_path: str):
    """Write combined intelligence report as markdown."""
    lines = []
    lines.append(f"# Paper Intelligence Report: {paper_name}")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Model: {MODEL}*\n")

    # Cost summary
    total_cost = 0
    total_tokens = 0
    for key, result in results.items():
        if 'meta' in result:
            total_cost += result['meta'].get('cost_usd', 0)
            total_tokens += result['meta'].get('total_tokens', 0)

    lines.append(f"**Total: {total_tokens:,} tokens | ${total_cost:.4f}**\n")
    lines.append("---\n")

    # Each prompt result as a section
    for key in sorted(results.keys()):
        config = PROMPTS.get(key, {})
        result = results[key]
        label = config.get('label', key)
        tier = config.get('tier', '?')
        tier_badge = '[CORE]' if tier == 'core' else '[PUBLISH]'

        lines.append(f"## {label} {tier_badge}")

        if 'error' in result:
            lines.append(f"*Error: {result['error']}*\n")
        elif 'text' in result:
            meta = result.get('meta', {})
            lines.append(f"*{meta.get('total_tokens', '?')} tokens | ${meta.get('cost_usd', '?')}*\n")
            lines.append(result['text'])
            lines.append("")

        lines.append("---\n")

    Path(output_path).write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Report: {output_path}")


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Paper Intelligence — 8-Prompt o3 System")
    parser.add_argument('paper', help='Path to paper .md file')
    parser.add_argument('--output', '-o', help='Output directory')
    parser.add_argument('--publish', action='store_true',
                        help='Run publish prompts 5-8 (in addition to core 1-4)')
    parser.add_argument('--all', action='store_true',
                        help='Run all 8 prompts')
    parser.add_argument('--only', help='Run only this prompt (e.g., 4_analogy_vs_isomorphism)')
    args = parser.parse_args()

    paper = Path(args.paper)
    output_dir = args.output or str(paper.parent / '_intel')
    cache_dir = str(Path(output_dir) / '_cache')

    print(f"Paper Intelligence: {paper.name}")
    print("=" * 60)

    if args.only:
        results = {args.only: run_prompt(args.only, str(paper), cache_dir)}
    elif args.all:
        print("  Running ALL 8 prompts...")
        results = run_all(str(paper), cache_dir)
    elif args.publish:
        print("  Running CORE (1-4) + PUBLISH (5-8)...")
        results = run_all(str(paper), cache_dir)
    else:
        print("  Running CORE prompts (1-4)...")
        results = run_core(str(paper), cache_dir)

    # Write report
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    report_path = str(Path(output_dir) / f"{paper.stem}_INTEL_REPORT.md")
    write_intel_report(results, paper.stem.replace('_', ' '), report_path)

    # Summary
    total_cost = sum(r.get('meta', {}).get('cost_usd', 0) for r in results.values())
    total_tokens = sum(r.get('meta', {}).get('total_tokens', 0) for r in results.values())
    print(f"\n{'='*60}")
    print(f"  {len(results)} prompts | {total_tokens:,} tokens | ${total_cost:.4f}")
    print(f"  Report: {report_path}")
