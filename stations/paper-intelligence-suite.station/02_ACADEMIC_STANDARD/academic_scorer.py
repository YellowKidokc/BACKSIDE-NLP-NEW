"""
L2: ACADEMIC STANDARD SCORER
=============================
Citation detection, external theory references, academic structure,
and a no-API academic rubric for claims, evidence, equations, and rigor.
"""
import re
from pathlib import Path

try:
    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    HAS_SS = True
except Exception:
    HAS_SS = False
    sch = None

ACADEMIC_SIGNALS = [
    'hypothesis','hypothesize','demonstrate','evidence','empirical',
    'methodology','statistically','significant','correlation','causation',
    'peer-reviewed','journal','publication','citation','literature review',
    'theoretical framework','research question','findings','conclusion',
    'data analysis','quantitative','qualitative','sample size','p-value',
    'confidence interval','reproducible','falsifiable','control group',
]

THEORY_SIGNALS = [
    # Physics
    'general relativity','quantum mechanics','thermodynamics','entropy',
    'information theory','decoherence','superposition','wave function',
    # Philosophy / Logic
    'godel','tarski','church-turing','incompleteness','modal logic',
    'epistemology','ontology','phenomenology',
    # Consciousness
    'integrated information','global workspace','orchestrated reduction',
    'hard problem','qualia','neural correlates',
    # Information
    'shannon entropy','kolmogorov complexity','algorithmic information',
    'landauer principle','maxwells demon',
    # Biology / Systems
    'second law','complexity','emergence','self-organization','attractor',
]

CITATION_PATTERNS = [
    r'\([A-Z][a-zA-Z\s]+,\s*\d{4}\)',   # (Author, 2020)
    r'\[\d+\]',                           # [1]
    r'\[[\w,\s]+\d{4}[\w,\s]*\]',        # [Smith2020]
    r'et al\.',                           # et al.
    r'ibid\.',                            # ibid.
    r'\b(doi|DOI)[:\.]\s*\S+',           # DOI
    r'https?://\S+',                      # URLs as references
]

STRUCTURE_MARKERS = {
    'has_abstract': r'\babstract\b',
    'has_introduction': r'\b(introduction|overview)\b',
    'has_methodology': r'\b(method|methodology|approach)\b',
    'has_results': r'\b(results?|findings?|outcomes?)\b',
    'has_discussion': r'\b(discussion|analysis|implications)\b',
    'has_conclusion': r'\b(conclusion|summary|closing)\b',
    'has_references': r'\b(references?|bibliography|works cited)\b',
}

CLAIM_PATTERNS = [
    r'\b(we claim|we argue|we propose|we contend|we demonstrate|we show|we prove)\b',
    r'\b(this paper (shows|argues|demonstrates|proposes))\b',
    r'\b(it follows that|therefore|thus|hence|necessarily|must be|required)\b',
    r'\b(is defined as|is given by|equals|is equivalent to)\b',
]

EVIDENCE_PATTERNS = [
    r'\b(evidence|empirical|experimental|measured|observed|data|dataset)\b',
    r'\b(statistically|sigma|p-value|confidence interval|correlation)\b',
    r'\b(study|experiment|trial|test|analysis|result|finding)\b',
    r'\([A-Z][a-zA-Z\s]+,\s*\d{4}\)',
    r'\[\d+\]',
    r'\bet al\.',
]

FALSIFIABILITY_PATTERNS = [
    r'\b(falsif|disprove|refute|prediction|testable|measurable)\b',
    r'\b(would be wrong if|fails when|breaks down|boundary condition|limit of)\b',
    r'\b(null hypothesis|counter-example|counterexample)\b',
]

HEDGE_PATTERNS = [
    r'\b(may|might|could|possibly|perhaps|appears|seems|likely|roughly|approximately)\b',
    r'\b(suggests|indicates|points to|is consistent with)\b',
]

ABSOLUTE_PATTERNS = [
    r'\b(always|never|all|none|only|must|cannot|impossible)\b',
    r'\b(proves|demonstrates|establishes|requires|guarantees)\b',
]

COUNTERARGUMENT_PATTERNS = [
    r'\b(however|although|nevertheless|nonetheless|alternatively)\b',
    r'\b(counterargument|objection|critics?|one might argue)\b',
]

LIMITATION_PATTERNS = [
    r'\b(limitations?|constraint|boundary condition|future work)\b',
    r'\b(remains unclear|open question|not yet tested|provisional)\b',
]

NOVELTY_PATTERNS = [
    r'\b(novel|new|original|for the first time)\b',
    r'\b(we introduce|we present|this work presents)\b',
]

DEFINITION_PATTERNS = [
    r'\b(is defined as|we define|definition|is equivalent to)\b',
    r'\b(let [A-Za-z][A-Za-z0-9_]*\b|\bdenote[sd]?\b)',
]

QUANT_PATTERNS = [
    r'\b\d+(\.\d+)?\s*(%|σ|sigma)\b',
    r'\b(p-value|confidence interval|sample size|n\s*=)\b',
    r'\b\d+(\.\d+)?\b',
]

EQUATION_LINE_PATTERN = re.compile(
    r'(?m)^[^\n]{0,160}(=|->|→|∑|∫|χ|Δ|∂|∇|\bexp\()[^\n]{0,160}$'
)
INLINE_MATH_PATTERN = re.compile(r'\$[^$]+\$')
HEADER_PATTERN = re.compile(r'^#{1,6}\s+(.+)$', re.MULTILINE)
AUTHOR_YEAR_CITATION_PATTERN = re.compile(r'\([A-Z][a-zA-Z\s]+,\s*\d{4}\)')
NUMERIC_CITATION_PATTERN = re.compile(r'\[\d+\]')


def _split_sentences(text: str) -> list[str]:
    return [
        s.strip()
        for s in re.split(r'(?<=[.!?])\s+', text)
        if len(s.strip()) >= 40
    ]


def _count_patterns(patterns: list[str], text: str) -> int:
    return sum(len(re.findall(pattern, text, flags=re.IGNORECASE)) for pattern in patterns)


def _extract_reference_section(text: str) -> str:
    match = re.search(
        r'(?ims)^#{1,6}\s*(references|bibliography|works cited)\s*$([\s\S]*)',
        text,
    )
    if not match:
        return ""
    tail = match.group(2).strip()
    next_heading = re.search(r'(?m)^#{1,6}\s+\S', tail)
    if next_heading:
        tail = tail[:next_heading.start()]
    return tail.strip()


def _count_reference_entries(text: str) -> int:
    ref_section = _extract_reference_section(text)
    if not ref_section:
        return 0
    lines = [line.strip() for line in ref_section.splitlines() if line.strip()]
    entries = [
        line for line in lines
        if len(line) > 20 and line not in {"---", "***"}
    ]
    return len(entries)


def _sentence_score(sentence: str, patterns: list[str], bonus_terms: tuple[str, ...] = ()) -> int:
    tl = sentence.lower()
    score = sum(3 for pattern in patterns if re.search(pattern, tl, flags=re.IGNORECASE))
    score += sum(1 for term in bonus_terms if term in tl)
    if any(symbol in sentence for symbol in ("=", "->", "→", "χ", "Δ", "∂")):
        score += 1
    if 8 <= len(sentence.split()) <= 45:
        score += 1
    return score


def _top_sentences(sentences: list[str], patterns: list[str], bonus_terms: tuple[str, ...], top_n: int) -> list[str]:
    ranked: list[tuple[int, str]] = []
    seen: set[str] = set()
    for sentence in sentences:
        score = _sentence_score(sentence, patterns, bonus_terms)
        normalized = re.sub(r'\s+', ' ', sentence).strip()
        if score <= 0 or normalized in seen:
            continue
        seen.add(normalized)
        ranked.append((score, normalized))
    ranked.sort(key=lambda item: (-item[0], len(item[1])))
    return [sentence[:240] for _, sentence in ranked[:top_n]]


def semantic_scholar_lookup(title, max_results=5):
    if not HAS_SS or not title:
        return {}
    try:
        results = sch.search_paper(title, limit=max_results, fields=[
            'title','year','citationCount','referenceCount',
            'venue','authors','abstract','influentialCitationCount'
        ])
        if not results or len(results) == 0:
            return {'ss_found': False}
        top = results[0]
        return {
            'ss_found': True,
            'ss_title': top.title,
            'ss_year': top.year,
            'ss_citation_count': top.citationCount,
            'ss_reference_count': top.referenceCount,
            'ss_venue': top.venue,
            'ss_influential_citations': top.influentialCitationCount,
        }
    except Exception as e:
        return {'ss_found': False, 'ss_error': str(e)}


def analyze(path_or_text, is_path=True, run_ss_lookup=False):
    if is_path:
        text = Path(path_or_text).read_text(encoding='utf-8', errors='ignore')
        fname = Path(path_or_text).name
        # Extract title from first H1
        title_match = re.search(r'^#\s+(.+)', text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else fname.replace('.md','')
    else:
        text = path_or_text
        fname = 'inline'
        title = ''

    tl = text.lower()
    words = text.split()
    per1k = 1000 / max(len(words), 1)
    sentences = _split_sentences(text)

    # Citation patterns
    total_citations = 0
    for p in CITATION_PATTERNS:
        hits = re.findall(p, text)
        total_citations += len(hits)

    # Academic signal words
    academic_score = sum(1 for term in ACADEMIC_SIGNALS if term in tl)
    academic_density = round(academic_score / max(len(text.split()), 1) * 1000, 2)

    # External theory references
    theory_hits = [t for t in THEORY_SIGNALS if t in tl]
    theory_count = len(theory_hits)

    # Structure check
    structure = {k: bool(re.search(v, tl)) for k, v in STRUCTURE_MARKERS.items()}
    structure_score = sum(structure.values())

    # Footnote / endnote markers
    footnotes = len(re.findall(r'\[\^[\w\d]+\]', text))

    # URL references
    urls = len(re.findall(r'https?://\S+', text))

    # DOI references
    dois = len(re.findall(r'\b(doi|DOI)[:\.]\s*\S+', text))

    # Structure/meta
    heading_count = len(HEADER_PATTERN.findall(text))
    reference_entry_count = _count_reference_entries(text)

    # Claim / rigor / equation metrics
    claim_marker_count = _count_patterns(CLAIM_PATTERNS, tl)
    evidence_marker_count = _count_patterns(EVIDENCE_PATTERNS, text)
    falsifiability_marker_count = _count_patterns(FALSIFIABILITY_PATTERNS, tl)
    hedge_count = _count_patterns(HEDGE_PATTERNS, tl)
    absolute_claim_count = _count_patterns(ABSOLUTE_PATTERNS, tl)
    counterargument_count = _count_patterns(COUNTERARGUMENT_PATTERNS, tl)
    limitation_count = _count_patterns(LIMITATION_PATTERNS, tl)
    novelty_marker_count = _count_patterns(NOVELTY_PATTERNS, tl)
    definition_marker_count = _count_patterns(DEFINITION_PATTERNS, tl)
    quantitative_marker_count = _count_patterns(QUANT_PATTERNS, text)
    equation_count = len(list(EQUATION_LINE_PATTERN.finditer(text))) + len(list(INLINE_MATH_PATTERN.finditer(text)))
    author_year_citations = len(AUTHOR_YEAR_CITATION_PATTERN.findall(text))
    numeric_citations = len(NUMERIC_CITATION_PATTERN.findall(text))
    evidence_to_claim_ratio = round(evidence_marker_count / max(claim_marker_count, 1), 2)
    hedge_to_absolute_ratio = round(hedge_count / max(absolute_claim_count, 1), 2)

    claim_candidates = _top_sentences(
        sentences,
        CLAIM_PATTERNS,
        ("therefore", "thus", "hence", "must", "requires", "implies"),
        top_n=3,
    )
    evidence_candidates = _top_sentences(
        sentences,
        EVIDENCE_PATTERNS,
        ("data", "evidence", "observed", "measured", "result"),
        top_n=2,
    )

    # No-API academic rubric (0-25)
    structure_points = round((structure_score / max(len(STRUCTURE_MARKERS), 1)) * 5, 2)
    grounding_points = round(min(5.0, (total_citations / 4.0) + (reference_entry_count / 8.0) + min(dois, 2) * 0.5), 2)
    claim_points = round(min(5.0, (claim_marker_count / 6.0) + min(evidence_to_claim_ratio, 2.0)), 2)
    quantitative_points = round(min(5.0, equation_count + (quantitative_marker_count / 6.0)), 2)
    falsifiability_points = round(
        min(5.0, falsifiability_marker_count + (counterargument_count * 0.5) + (limitation_count * 0.5)),
        2,
    )
    rubric_total = round(
        structure_points + grounding_points + claim_points + quantitative_points + falsifiability_points,
        2,
    )
    if rubric_total >= 21:
        rubric_grade = 'A (Rigorous)'
    elif rubric_total >= 16:
        rubric_grade = 'B (Strong)'
    elif rubric_total >= 11:
        rubric_grade = 'C (Developing)'
    elif rubric_total >= 6:
        rubric_grade = 'D (Light)'
    else:
        rubric_grade = 'F (Thin)'

    result = {
        'file': fname,
        'title_detected': title[:80],
        'citation_count': total_citations,
        'author_year_citation_count': author_year_citations,
        'numeric_citation_count': numeric_citations,
        'citation_density_per1k': round(total_citations / max(len(text.split()), 1) * 1000, 2),
        'external_theory_count': theory_count,
        'external_theories': ', '.join(theory_hits[:8]),
        'academic_signal_count': academic_score,
        'academic_signal_density': academic_density,
        'structure_score': f"{structure_score}/{len(STRUCTURE_MARKERS)}",
        'heading_count': heading_count,
        'reference_entry_count': reference_entry_count,
        'has_abstract': structure['has_abstract'],
        'has_introduction': structure['has_introduction'],
        'has_methodology': structure['has_methodology'],
        'has_results': structure['has_results'],
        'has_discussion': structure['has_discussion'],
        'has_conclusion': structure['has_conclusion'],
        'has_references_section': structure['has_references'],
        'footnote_count': footnotes,
        'url_references': urls,
        'doi_references': dois,
        'claim_marker_count': claim_marker_count,
        'claim_density_per1k': round(claim_marker_count * per1k, 2),
        'evidence_marker_count': evidence_marker_count,
        'evidence_density_per1k': round(evidence_marker_count * per1k, 2),
        'evidence_to_claim_ratio': evidence_to_claim_ratio,
        'falsifiability_marker_count': falsifiability_marker_count,
        'falsifiability_density_per1k': round(falsifiability_marker_count * per1k, 2),
        'hedge_count': hedge_count,
        'hedge_density_per1k': round(hedge_count * per1k, 2),
        'absolute_claim_count': absolute_claim_count,
        'absolute_density_per1k': round(absolute_claim_count * per1k, 2),
        'hedge_to_absolute_ratio': hedge_to_absolute_ratio,
        'counterargument_count': counterargument_count,
        'limitation_count': limitation_count,
        'novelty_marker_count': novelty_marker_count,
        'definition_marker_count': definition_marker_count,
        'quantitative_marker_count': quantitative_marker_count,
        'equation_count': equation_count,
        'equation_density_per1k': round(equation_count * per1k, 2),
        'claim_candidate_1': claim_candidates[0] if len(claim_candidates) > 0 else '',
        'claim_candidate_2': claim_candidates[1] if len(claim_candidates) > 1 else '',
        'claim_candidate_3': claim_candidates[2] if len(claim_candidates) > 2 else '',
        'evidence_candidate_1': evidence_candidates[0] if len(evidence_candidates) > 0 else '',
        'evidence_candidate_2': evidence_candidates[1] if len(evidence_candidates) > 1 else '',
        'rubric_structure_points': structure_points,
        'rubric_grounding_points': grounding_points,
        'rubric_claim_points': claim_points,
        'rubric_quantitative_points': quantitative_points,
        'rubric_falsifiability_points': falsifiability_points,
        'academic_rubric_total': rubric_total,
        'academic_rubric_grade': rubric_grade,
    }

    # Optional: Semantic Scholar lookup
    if run_ss_lookup and title:
        result.update(semantic_scholar_lookup(title))

    # Academic grade
    total = total_citations + theory_count + academic_score
    if total >= 40: result['academic_grade'] = 'A (Publication Grade)'
    elif total >= 25: result['academic_grade'] = 'B (Strong)'
    elif total >= 15: result['academic_grade'] = 'C (Moderate)'
    elif total >= 5:  result['academic_grade'] = 'D (Light)'
    else:             result['academic_grade'] = 'F (Needs Citations)'

    return result


if __name__ == '__main__':
    import sys, json
    run_ss = '--ss' in sys.argv
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        r = analyze(sys.argv[1], run_ss_lookup=run_ss)
        print(json.dumps(r, indent=2))
