"""
OPENAI PAPER-LEVEL INTELLIGENCE
=================================
One strategic API call per paper — asks what NLP/SBERT cannot reach.

STRATEGIC (o3 reasoning model):
  1. COMPETING THEORIES — established theories making similar/opposing claims
  2. CITATION GAPS — specific papers/authors that SHOULD be cited
  3. SIMILAR PAPERS — closest published work to this approach
  4. ISOMORPHIC BRIDGES (deep) — which physics-theology mappings hold rigorously vs metaphorically
  5. PHYSICS AUDIT — are the physics equations/concepts used correctly?
  6. ARGUMENT STRUCTURE — logical chain analysis, weakest link, missing steps
  7. NOVEL CONTRIBUTION — what does this paper add that doesn't exist?
  8. FALSIFIABLE PREDICTIONS — testable claims the paper makes or should make
  9. KILLER OBJECTION — strongest attack a hostile reviewer would make
  10. PUBLICATION READINESS — what journal, what needs to change
  11. READABILITY — structure, flow, clarity assessment

SENTENCE-LEVEL (gpt-4o-mini, batched):
  Channels O-V for the word matrix.
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

MODEL_STRATEGIC = "o3"            # reasoning model for deep paper-level analysis
MODEL_SENTENCES = "gpt-4o-mini"  # cheaper model for sentence scoring

# ═══════════════════════════════════════════════════════════════
# PAPER-LEVEL STRATEGIC ANALYSIS
# ═══════════════════════════════════════════════════════════════

STRATEGIC_SYSTEM = """You are a world-class interdisciplinary research analyst with deep expertise in:
- Theoretical physics (QFT, thermodynamics, general relativity, quantum mechanics)
- Pure mathematics (group theory, topology, category theory, logic)
- Systematic theology and philosophy of religion
- Philosophy of science and formal epistemology

You are analyzing a paper from the Theophysics framework — a formal axiom system that claims:
- Mathematics and God share 24 structural properties (God ↔ Math isomorphism)
- 193 axioms derive from 3 primitives: Existence, Distinction, Information
- Master Equation: χ = ∭ (G·M·E·S·T·K·R·Q·F·C) dx dy dt
- 10 Laws map physics forces to theological concepts with constructive/destructive poles
- 9 Fruits of the Spirit map to physics equations (V(r) minima, resonance, equilibrium, etc.)
- The framework treats theology as a branch of mathematical physics

The author is a serious independent researcher who wants REAL adversarial feedback.
He does NOT want validation — he wants to know where the argument breaks, where it's strongest,
what he's missing, and what would make a hostile physicist or theologian take notice.

Be ruthlessly specific. Name real theorems, real papers, real objections. No hand-waving."""

STRATEGIC_PROMPT = """Analyze this paper with maximum depth.

PAPER: "{title}"
CONTENT:
{content}

Return a JSON object with EXACTLY these keys:

{{
  "competing_theories": [
    {{
      "theory": "formal name",
      "author": "name(s)",
      "relationship": "supports/contradicts/parallel/subsumes",
      "key_paper": "Author (Year). Title. Journal.",
      "relevance": "specific connection to THIS paper's claims",
      "threat_level": "low/medium/high — how much does this undermine or preempt the paper?"
    }}
  ],

  "citation_gaps": [
    {{
      "author": "name",
      "work": "specific paper/book title",
      "year": "year",
      "field": "physics/math/theology/philosophy",
      "why_critical": "what specific argument in this paper needs this citation to hold up"
    }}
  ],

  "similar_papers": [
    {{
      "title": "exact paper title if known",
      "author": "name",
      "field": "field",
      "similarity": "what specific claim/method overlaps",
      "key_difference": "what this paper does that the other doesn't",
      "should_cite": true/false
    }}
  ],

  "isomorphic_bridges": {{
    "rigorous_bridges": [
      {{
        "physics_concept": "name",
        "physics_equation": "the actual equation if applicable",
        "theology_concept": "name",
        "mapping_type": "formal isomorphism/structural analogy/metaphor",
        "strength": 0.0-1.0,
        "justification": "WHY this mapping holds or doesn't — be specific about the math"
      }}
    ],
    "broken_bridges": [
      {{
        "physics_concept": "name",
        "theology_concept": "name",
        "failure_mode": "exactly where the mapping breaks down",
        "could_be_fixed": "what would need to be true for it to work"
      }}
    ],
    "novel_mappings": "any bridge in this paper that is genuinely new in the literature — not found in Polkinghorne, Tipler, Barbour, etc."
  }},

  "physics_audit": {{
    "equations_used_correctly": ["list equations/concepts used correctly"],
    "equations_used_incorrectly": [
      {{
        "concept": "what's misused",
        "error": "what's wrong specifically",
        "correction": "what the physics actually says"
      }}
    ],
    "physics_grade": 0.0-1.0,
    "physics_note": "overall assessment of physics accuracy"
  }},

  "argument_structure": {{
    "logical_chain": ["step 1", "step 2", "...each step in the argument"],
    "strongest_link": "which step is most rigorous and WHY",
    "weakest_link": "which step is the biggest logical leap and WHY",
    "missing_steps": ["intermediate claims that need to be explicitly stated"],
    "hidden_assumptions": ["assumptions the paper relies on but doesn't state"],
    "formal_validity": 0.0-1.0
  }},

  "novel_contribution": {{
    "what_is_new": "the specific claim/framework/insight that doesn't exist elsewhere",
    "prior_art": "closest existing work and how this extends it",
    "significance": "why this matters IF it holds up",
    "novelty_score": 0.0-1.0
  }},

  "falsifiable_predictions": [
    {{
      "prediction": "specific testable claim derived from this paper",
      "domain": "physics/math/psychology/sociology",
      "test_method": "exactly how you would test it",
      "expected_result": "what result would confirm vs. disconfirm",
      "current_status": "untested/partially tested/tested/unfalsifiable"
    }}
  ],

  "killer_objection": {{
    "objection": "the single strongest attack a hostile reviewer would make",
    "objector_profile": "what kind of expert would raise this (physicist/theologian/philosopher)",
    "why_dangerous": "why this objection has real teeth — be specific",
    "paper_survives": true/false,
    "best_defense": "the strongest possible response",
    "preemptive_addition": "what to add to the paper NOW to defuse it before review"
  }},

  "publication_readiness": {{
    "target_journals": ["journal name — be realistic about acceptance probability"],
    "current_readiness": 0.0-1.0,
    "blocking_issues": ["what MUST change before submission"],
    "quick_wins": ["easy changes that would significantly improve it"]
  }},

  "readability": {{
    "structure_score": 0.0-1.0,
    "flow_issues": ["where the reader gets lost or confused"],
    "jargon_barriers": ["terms that need definition for the target audience"],
    "suggested_restructure": "how to reorder sections for maximum impact"
  }},

  "overall_grade": {{
    "rigor": 0.0-1.0,
    "originality": 0.0-1.0,
    "physics_accuracy": 0.0-1.0,
    "theological_depth": 0.0-1.0,
    "clarity": 0.0-1.0,
    "citation_completeness": 0.0-1.0,
    "publication_readiness": 0.0-1.0,
    "one_line_verdict": "one-sentence brutally honest assessment"
  }}
}}

RULES:
- Name REAL theories, authors, papers, journals. No placeholders.
- If you don't know a specific citation, say so — don't fabricate.
- Score honestly. A 0.5 means mediocre. Don't grade inflate.
- The isomorphic_bridges section is the MOST IMPORTANT — spend the most reasoning here.
- For physics_audit: actually check whether the physics is used correctly."""


# ═══════════════════════════════════════════════════════════════
# SENTENCE-LEVEL SCORING (for word matrix channels O-V)
# ═══════════════════════════════════════════════════════════════

SENTENCE_SYSTEM = """You are analyzing individual sentences from a Theophysics research paper.

Theophysics maps theology to physics via 193 axioms, 10 Laws, 24 Properties, and a Master Equation.
For each sentence, classify and score it rigorously.

Return a JSON object with key "results" containing an array of objects, one per sentence."""

SENTENCE_PROMPT = """Score these {n} sentences from "{title}":

{sentences}

For EACH sentence, return:
{{
  "type": "claim|evidence|definition|derivation|question|narrative|transition|equation",
  "axiom_deps": [numbers 1-193 this depends on, or []],
  "theories": ["Named Theory 1", "Named Theory 2"],
  "bridge_score": 0.0-1.0 (physics-theology mapping strength),
  "logic_score": 0.0-1.0 (does conclusion follow from premises?),
  "falsifiable": 0.0-1.0 (empirically/formally testable?),
  "missing_citations": ["Author - Work"],
  "strongest_objection": "best counter-argument (max 40 words, '' if not a claim)"
}}

Return {{"results": [...]}} with one object per sentence, in order."""


BATCH_SIZE = 10


def analyze_paper_strategic(paper_path: str, cache_dir: Optional[str] = None) -> dict:
    """
    Run paper-level strategic intelligence analysis.
    Returns the full strategic analysis dict.
    """
    if not HAS_OPENAI:
        return {"error": "OpenAI not configured"}

    paper = Path(paper_path)
    text = paper.read_text(encoding='utf-8', errors='replace')
    title = paper.stem.replace('_', ' ')

    # Check cache
    if cache_dir:
        cache_path = Path(cache_dir) / f"{paper.stem}_strategic.json"
        if cache_path.exists():
            print(f"  Using cached strategic analysis: {cache_path.name}")
            return json.loads(cache_path.read_text(encoding='utf-8'))

    # Send full paper to o3 — it can handle more context and reasons better with more
    content = text
    if len(content) > 12000:
        content = content[:12000] + "\n\n[...content continues, truncated for analysis...]"

    print(f"  Strategic analysis: {title} (model: {MODEL_STRATEGIC})")

    try:
        # o3 reasoning model — different call pattern
        is_reasoning = MODEL_STRATEGIC.startswith('o')

        if is_reasoning:
            response = _client.chat.completions.create(
                model=MODEL_STRATEGIC,
                messages=[
                    {"role": "developer", "content": STRATEGIC_SYSTEM},
                    {"role": "user", "content": STRATEGIC_PROMPT.format(
                        title=title, content=content) +
                        "\n\nIMPORTANT: Return ONLY valid JSON. No markdown fences, no explanation outside the JSON object."}
                ],
                max_completion_tokens=16000,
            )
        else:
            response = _client.chat.completions.create(
                model=MODEL_STRATEGIC,
                messages=[
                    {"role": "system", "content": STRATEGIC_SYSTEM},
                    {"role": "user", "content": STRATEGIC_PROMPT.format(
                        title=title, content=content)}
                ],
                max_tokens=8000,
                temperature=0.3,
                response_format={"type": "json_object"}
            )

        text_out = response.choices[0].message.content
        usage = response.usage

        # o3 may wrap JSON in markdown fences — strip them
        text_out = text_out.strip()
        if text_out.startswith('```'):
            text_out = re.sub(r'^```(?:json)?\s*', '', text_out)
            text_out = re.sub(r'\s*```$', '', text_out)

        result = json.loads(text_out)

        # Calculate cost estimate
        input_tokens = usage.prompt_tokens if usage else 0
        output_tokens = usage.completion_tokens if usage else 0
        total_tokens = usage.total_tokens if usage else 0

        # Cost per 1M tokens (approximate)
        COST_TABLE = {
            'o3': {'input': 10.0, 'output': 40.0},
            'gpt-4o': {'input': 2.50, 'output': 10.0},
            'gpt-4o-mini': {'input': 0.15, 'output': 0.60},
        }
        rates = COST_TABLE.get(MODEL_STRATEGIC, COST_TABLE['gpt-4o'])
        est_cost = (input_tokens * rates['input'] + output_tokens * rates['output']) / 1_000_000

        result['_meta'] = {
            'model': MODEL_STRATEGIC,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': total_tokens,
            'estimated_cost_usd': round(est_cost, 4),
            'analyzed_at': datetime.now().isoformat(),
            'paper': paper.name,
        }

        print(f"  Strategic complete: {total_tokens:,} tokens (input={input_tokens:,}, output={output_tokens:,})")
        print(f"  Estimated cost: ${est_cost:.4f}")

        # Cache
        if cache_dir:
            Path(cache_dir).mkdir(parents=True, exist_ok=True)
            cache_path = Path(cache_dir) / f"{paper.stem}_strategic.json"
            cache_path.write_text(json.dumps(result, indent=2, ensure_ascii=False),
                                  encoding='utf-8')

        return result

    except Exception as e:
        print(f"  Strategic analysis ERROR: {e}")
        return {"error": str(e)}


def score_sentences_openai(sentences: list[str], paper_name: str = "",
                           cache_dir: Optional[str] = None) -> list[dict]:
    """
    Score sentences for word matrix channels O-V.
    Batches ~10 sentences per call using gpt-4o-mini.
    """
    if not HAS_OPENAI:
        print("  ERROR: OpenAI not configured")
        return [_empty_result()] * len(sentences)

    # Check cache
    if cache_dir and paper_name:
        cache_path = Path(cache_dir) / f"{paper_name}_sentence_scores.json"
        if cache_path.exists():
            cached = json.loads(cache_path.read_text(encoding='utf-8'))
            if len(cached) == len(sentences):
                print(f"  Using cached sentence scores ({len(cached)} sentences)")
                return cached

    all_results = [None] * len(sentences)
    n_batches = (len(sentences) + BATCH_SIZE - 1) // BATCH_SIZE
    total_tokens = 0

    print(f"  Sentence scoring: {len(sentences)} sentences in {n_batches} batches (model: {MODEL_SENTENCES})")

    for batch_idx in range(n_batches):
        start = batch_idx * BATCH_SIZE
        end = min(start + BATCH_SIZE, len(sentences))
        batch = sentences[start:end]

        sent_block = "\n".join(f"[{i}] \"{s}\"" for i, s in enumerate(batch))

        try:
            response = _client.chat.completions.create(
                model=MODEL_SENTENCES,
                messages=[
                    {"role": "system", "content": SENTENCE_SYSTEM},
                    {"role": "user", "content": SENTENCE_PROMPT.format(
                        n=len(batch), title=paper_name.replace('_', ' '),
                        sentences=sent_block)}
                ],
                max_tokens=3000,
                temperature=0.2,
                response_format={"type": "json_object"}
            )

            text = response.choices[0].message.content
            usage = response.usage
            total_tokens += usage.total_tokens if usage else 0

            parsed = json.loads(text)
            if isinstance(parsed, dict):
                for key in ('results', 'sentences', 'analysis', 'data'):
                    if key in parsed:
                        parsed = parsed[key]
                        break

            if isinstance(parsed, list):
                for i, result in enumerate(parsed):
                    if start + i < len(sentences):
                        all_results[start + i] = _normalize_result(result)

            print(f"    Batch {batch_idx + 1}/{n_batches} — {usage.total_tokens if usage else '?'} tokens")

        except Exception as e:
            print(f"    Batch {batch_idx + 1} ERROR: {e}")
            for i in range(start, end):
                all_results[i] = _empty_result()

        if batch_idx < n_batches - 1:
            time.sleep(0.3)

    # Fill gaps
    for i in range(len(all_results)):
        if all_results[i] is None:
            all_results[i] = _empty_result()

    print(f"  Sentence scoring complete: {total_tokens:,} tokens")

    # Cache
    if cache_dir and paper_name:
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        cache_path = Path(cache_dir) / f"{paper_name}_sentence_scores.json"
        cache_path.write_text(json.dumps(all_results, indent=2, ensure_ascii=False),
                              encoding='utf-8')

    return all_results


def _normalize_result(raw: dict) -> dict:
    TYPE_MAP = {
        'claim': 'claim', 'evidence': 'evidence', 'definition': 'definition',
        'derivation': 'derivation', 'question': 'question', 'narrative': 'narrative',
        'transition': 'transition', 'equation': 'equation',
    }
    return {
        'type': TYPE_MAP.get(str(raw.get('type', 'narrative')).lower().strip(), 'narrative'),
        'axiom_deps': _safe_list_int(raw.get('axiom_deps', [])),
        'theories': _safe_list(raw.get('theories', [])),
        'bridge_score': _safe_float(raw.get('bridge_score', 0)),
        'logic_score': _safe_float(raw.get('logic_score', 0)),
        'falsifiable': _safe_float(raw.get('falsifiable', 0)),
        'missing_citations': _safe_list(raw.get('missing_citations', [])),
        'strongest_objection': str(raw.get('strongest_objection', ''))[:300],
    }


def _empty_result() -> dict:
    return {
        'type': 'narrative', 'axiom_deps': [], 'theories': [],
        'bridge_score': 0.0, 'logic_score': 0.0, 'falsifiable': 0.0,
        'missing_citations': [], 'strongest_objection': '',
    }


def _safe_float(v) -> float:
    try:
        return max(0.0, min(1.0, float(v)))
    except (ValueError, TypeError):
        return 0.0


def _safe_list(v) -> list:
    if isinstance(v, list):
        return [str(x) for x in v]
    if isinstance(v, str):
        return [x.strip() for x in v.split(',') if x.strip()]
    return []


def _safe_list_int(v) -> list:
    if isinstance(v, list):
        result = []
        for x in v:
            try:
                result.append(int(x))
            except (ValueError, TypeError):
                pass
        return result
    return []


SENTENCE_TYPE_ENCODING = {
    'claim': 1.0, 'derivation': 0.9, 'equation': 0.85,
    'evidence': 0.8, 'definition': 0.7, 'question': 0.5,
    'narrative': 0.3, 'transition': 0.1,
}


# ═══════════════════════════════════════════════════════════════
# STRATEGIC REPORT → MARKDOWN
# ═══════════════════════════════════════════════════════════════

def write_strategic_markdown(analysis: dict, output_path: str):
    """Write the strategic analysis as a readable markdown report."""
    lines = []
    meta = analysis.get('_meta', {})
    title = meta.get('paper', 'Unknown')
    model = meta.get('model', '?')
    total_tokens = meta.get('total_tokens', meta.get('tokens', '?'))
    cost = meta.get('estimated_cost_usd', '?')

    lines.append(f"# Strategic Intelligence: {title}")
    lines.append(f"*Model: {model} | Tokens: {total_tokens} | Cost: ${cost} | {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")

    # Overall grade
    grade = analysis.get('overall_grade', {})
    if grade:
        lines.append("## Overall Grade")
        for k in ('rigor', 'originality', 'physics_accuracy', 'theological_depth',
                   'clarity', 'citation_completeness', 'publication_readiness'):
            v = grade.get(k, 0)
            try:
                fv = float(v)
                bar = '█' * int(fv * 10) + '░' * (10 - int(fv * 10))
                lines.append(f"  {k:<25} {bar} {v}")
            except (ValueError, TypeError):
                lines.append(f"  {k:<25} {v}")
        lines.append(f"\n  **{grade.get('one_line_verdict', '')}**\n")

    # Competing theories
    theories = analysis.get('competing_theories', [])
    if theories:
        lines.append("## Competing Theories")
        for t in theories:
            threat = t.get('threat_level', '')
            marker = '🔴' if threat == 'high' else '🟡' if threat == 'medium' else '🟢'
            lines.append(f"- {marker} **{t.get('theory', '?')}** ({t.get('author', '?')}) [{t.get('relationship', '?')}]")
            lines.append(f"  - Paper: {t.get('key_paper', '?')}")
            lines.append(f"  - Relevance: {t.get('relevance', '?')}")
            lines.append(f"  - Threat: {threat}\n")

    # Citation gaps
    gaps = analysis.get('citation_gaps', [])
    if gaps:
        lines.append("## Citation Gaps")
        for g in gaps:
            lines.append(f"- **{g.get('author', '?')}** — *{g.get('work', '?')}* ({g.get('year', '?')}) [{g.get('field', '')}]")
            lines.append(f"  - Why critical: {g.get('why_critical', g.get('why_needed', '?'))}\n")

    # Similar papers
    similar = analysis.get('similar_papers', [])
    if similar:
        lines.append("## Similar Published Work")
        for s in similar:
            cite = '📌' if s.get('should_cite', False) else ''
            lines.append(f"- {cite} **{s.get('title', '?')}** by {s.get('author', '?')} ({s.get('field', '?')})")
            lines.append(f"  - Similar: {s.get('similarity', '?')}")
            lines.append(f"  - Different: {s.get('key_difference', '?')}\n")

    # ISOMORPHIC BRIDGES (the big one)
    bridges = analysis.get('isomorphic_bridges', {})
    if bridges:
        lines.append("## Isomorphic Bridge Analysis")
        lines.append("")
        rig = bridges.get('rigorous_bridges', [])
        if rig:
            lines.append("### Rigorous Bridges")
            for b in rig:
                lines.append(f"- **{b.get('physics_concept', '?')}** ↔ **{b.get('theology_concept', '?')}** (strength: {b.get('strength', '?')})")
                if b.get('physics_equation'):
                    lines.append(f"  - Equation: `{b.get('physics_equation')}`")
                lines.append(f"  - Type: {b.get('mapping_type', '?')}")
                lines.append(f"  - Justification: {b.get('justification', '?')}\n")

        broken = bridges.get('broken_bridges', [])
        if broken:
            lines.append("### Broken Bridges")
            for b in broken:
                lines.append(f"- **{b.get('physics_concept', '?')}** ↔ **{b.get('theology_concept', '?')}**")
                lines.append(f"  - Failure: {b.get('failure_mode', '?')}")
                lines.append(f"  - Could fix: {b.get('could_be_fixed', '?')}\n")

        novel = bridges.get('novel_mappings', '')
        if novel:
            lines.append(f"### Novel Mappings\n{novel}\n")

    # Physics audit
    phys = analysis.get('physics_audit', {})
    if phys:
        lines.append("## Physics Audit")
        lines.append(f"**Grade: {phys.get('physics_grade', '?')}** — {phys.get('physics_note', '')}\n")
        correct = phys.get('equations_used_correctly', [])
        if correct:
            lines.append("Correct usage:")
            for c in correct:
                lines.append(f"  - ✓ {c}")
        incorrect = phys.get('equations_used_incorrectly', [])
        if incorrect:
            lines.append("\nIncorrect usage:")
            for ic in incorrect:
                lines.append(f"  - ✗ **{ic.get('concept', '?')}**: {ic.get('error', '?')}")
                lines.append(f"    Correction: {ic.get('correction', '?')}")
        lines.append("")

    # Argument structure
    arg = analysis.get('argument_structure', {})
    if arg:
        lines.append("## Argument Structure")
        chain = arg.get('logical_chain', [])
        if chain:
            lines.append("Logical chain:")
            for i, step in enumerate(chain, 1):
                lines.append(f"  {i}. {step}")
            lines.append("")
        lines.append(f"- **Strongest link:** {arg.get('strongest_link', '?')}")
        lines.append(f"- **Weakest link:** {arg.get('weakest_link', '?')}")
        missing = arg.get('missing_steps', [])
        if missing:
            lines.append("- Missing steps:")
            for m in missing:
                lines.append(f"  - {m}")
        hidden = arg.get('hidden_assumptions', [])
        if hidden:
            lines.append("- Hidden assumptions:")
            for h in hidden:
                lines.append(f"  - {h}")
        lines.append(f"- Formal validity: {arg.get('formal_validity', '?')}\n")

    # Novel contribution
    novel = analysis.get('novel_contribution', {})
    if novel:
        lines.append("## Novel Contribution")
        lines.append(f"- **What's new:** {novel.get('what_is_new', '?')}")
        lines.append(f"- Prior art: {novel.get('prior_art', '?')}")
        lines.append(f"- Significance: {novel.get('significance', '?')}")
        lines.append(f"- Novelty score: {novel.get('novelty_score', '?')}\n")

    # Falsifiable predictions
    preds = analysis.get('falsifiable_predictions', [])
    if preds:
        lines.append("## Falsifiable Predictions")
        for p in preds:
            status = p.get('current_status', '?')
            marker = '✓' if status == 'tested' else '◐' if 'partial' in str(status) else '○'
            lines.append(f"- {marker} **{p.get('prediction', '?')}** [{p.get('domain', '')}]")
            lines.append(f"  - Test: {p.get('test_method', '?')}")
            lines.append(f"  - Expected: {p.get('expected_result', '?')}")
            lines.append(f"  - Status: {status}\n")

    # Killer objection
    killer = analysis.get('killer_objection', {})
    if killer:
        lines.append("## Killer Objection")
        survives = killer.get('paper_survives', None)
        icon = '✓ SURVIVES' if survives else '✗ FATAL' if survives is False else '? UNKNOWN'
        lines.append(f"**Verdict: {icon}**\n")
        lines.append(f"- Objection: **{killer.get('objection', '?')}**")
        lines.append(f"- From: {killer.get('objector_profile', '?')}")
        lines.append(f"- Why dangerous: {killer.get('why_dangerous', '?')}")
        lines.append(f"- Best defense: {killer.get('best_defense', '?')}")
        lines.append(f"- **ADD TO PAPER:** {killer.get('preemptive_addition', '?')}\n")

    # Publication readiness
    pub = analysis.get('publication_readiness', {})
    if pub:
        lines.append("## Publication Readiness")
        lines.append(f"Score: {pub.get('current_readiness', '?')}\n")
        targets = pub.get('target_journals', [])
        if targets:
            lines.append("Target journals:")
            for j in targets:
                lines.append(f"  - {j}")
        blockers = pub.get('blocking_issues', [])
        if blockers:
            lines.append("\nBlocking issues:")
            for b in blockers:
                lines.append(f"  - ⛔ {b}")
        wins = pub.get('quick_wins', [])
        if wins:
            lines.append("\nQuick wins:")
            for w in wins:
                lines.append(f"  - ✓ {w}")
        lines.append("")

    # Readability
    read = analysis.get('readability', {})
    if read:
        lines.append("## Readability")
        lines.append(f"Structure score: {read.get('structure_score', '?')}\n")
        flow = read.get('flow_issues', [])
        if flow:
            for f in flow:
                lines.append(f"- Flow: {f}")
        jargon = read.get('jargon_barriers', [])
        if jargon:
            for j in jargon:
                lines.append(f"- Jargon: {j}")
        restruct = read.get('suggested_restructure', '')
        if restruct:
            lines.append(f"\n**Restructure suggestion:** {restruct}")

    Path(output_path).write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Strategic report: {output_path}")


# ═══════════════════════════════════════════════════════════════
# CLI — run both analyses on a paper
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python openai_paper_intel.py <paper.md> [output_dir]")
        sys.exit(1)

    paper_path = sys.argv[1]
    paper = Path(paper_path)
    output_dir = sys.argv[2] if len(sys.argv) > 2 else str(paper.parent / '_intel')
    cache_dir = str(Path(output_dir) / '_cache')

    print(f"Paper Intelligence: {paper.name}")
    print("=" * 60)

    # 1. Strategic analysis (gpt-4o, ~1 call)
    print("\n[1/2] STRATEGIC ANALYSIS...")
    strategic = analyze_paper_strategic(paper_path, cache_dir=cache_dir)
    if 'error' not in strategic:
        md_path = str(Path(output_dir) / f"{paper.stem}_STRATEGIC_INTEL.md")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        write_strategic_markdown(strategic, md_path)

    # 2. Sentence-level scoring (gpt-4o-mini, batched)
    print("\n[2/2] SENTENCE-LEVEL SCORING...")
    text = paper.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'^---.*?---', '', text, flags=re.DOTALL)
    text = re.sub(r'#+\s+', '', text)
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 20]

    sent_scores = score_sentences_openai(sents, paper.stem, cache_dir=cache_dir)

    # Show summary
    types = {}
    for r in sent_scores:
        t = r.get('type', 'unknown')
        types[t] = types.get(t, 0) + 1

    print(f"\n{'='*60}")
    print(f"SUMMARY: {paper.name}")
    print(f"{'='*60}")
    print(f"  Sentence types: {json.dumps(types, indent=4)}")

    all_theories = set()
    for r in sent_scores:
        all_theories.update(r.get('theories', []))
    print(f"  Theories referenced: {len(all_theories)}")
    for t in sorted(all_theories)[:15]:
        print(f"    - {t}")

    bridge_scores = [r['bridge_score'] for r in sent_scores if r['bridge_score'] > 0]
    logic_scores = [r['logic_score'] for r in sent_scores if r['logic_score'] > 0]
    if bridge_scores:
        print(f"  Bridge score: mean={sum(bridge_scores)/len(bridge_scores):.3f}, max={max(bridge_scores):.3f}")
    if logic_scores:
        print(f"  Logic score:  mean={sum(logic_scores)/len(logic_scores):.3f}, max={max(logic_scores):.3f}")

    print(f"\nDone. Results in: {output_dir}")
