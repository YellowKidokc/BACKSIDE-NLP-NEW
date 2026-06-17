"""
L2: ACADEMIC STANDARD SCORER v2
================================
No-API academic quality scanner for Markdown/text papers.

Major v2 upgrades over the original:
- Heading-aware IMRaD/academic structure detection.
- Cleaner citation parsing with de-duplication and bibliography separation.
- Claim/evidence/falsifiability/limitation/counterargument scoring.
- Overclaim risk flags: strong claims without nearby evidence or hedging.
- Reference quality signals: DOI/URL/year diversity/reference entries.
- Actionable recommendations, not just counts.
- Backward-compatible analyze(path_or_text, is_path=True, run_ss_lookup=False).

This is intentionally heuristic. It does not decide whether a paper is true.
It estimates whether the writing looks academically defensible enough to review.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    from semanticscholar import SemanticScholar  # type: ignore

    _SS_CLIENT = SemanticScholar()
    HAS_SS = True
except Exception:  # pragma: no cover - optional dependency
    _SS_CLIENT = None
    HAS_SS = False


# -----------------------------------------------------------------------------
# Pattern libraries
# -----------------------------------------------------------------------------

ACADEMIC_SIGNALS = [
    "hypothesis", "hypothesize", "demonstrate", "evidence", "empirical",
    "methodology", "statistically", "significant", "correlation", "causation",
    "peer-reviewed", "journal", "publication", "citation", "literature review",
    "theoretical framework", "research question", "findings", "conclusion",
    "data analysis", "quantitative", "qualitative", "sample size", "p-value",
    "confidence interval", "reproducible", "falsifiable", "control group",
    "replication", "operationalize", "validity", "reliability", "construct",
    "confound", "effect size", "dataset", "preprint", "meta-analysis",
]

THEORY_SIGNALS = [
    # Physics / information
    "general relativity", "special relativity", "quantum mechanics", "thermodynamics",
    "entropy", "information theory", "decoherence", "superposition", "wave function",
    "wavefunction", "second law", "shannon entropy", "kolmogorov complexity",
    "algorithmic information", "landauer principle", "maxwell's demon", "maxwells demon",
    # Philosophy / logic
    "godel", "gödel", "tarski", "church-turing", "incompleteness", "modal logic",
    "epistemology", "ontology", "phenomenology", "abduction", "deduction", "induction",
    # Consciousness
    "integrated information", "global workspace", "orchestrated reduction", "orch-or",
    "hard problem", "qualia", "neural correlates",
    # Systems / biology
    "complexity", "emergence", "self-organization", "attractor", "cybernetics",
    "systems theory", "network theory",
]

SECTION_ALIASES = {
    "abstract": ("abstract", "summary"),
    "introduction": ("introduction", "overview", "background"),
    "literature_review": ("literature review", "related work", "prior work", "state of the literature"),
    "research_question": ("research question", "problem statement", "thesis", "aims", "objectives"),
    "methodology": ("method", "methods", "methodology", "approach", "materials and methods"),
    "results": ("result", "results", "findings", "outcomes"),
    "discussion": ("discussion", "analysis", "interpretation", "implications"),
    "limitations": ("limitations", "limits", "boundary conditions", "scope", "future work"),
    "conclusion": ("conclusion", "conclusions", "closing"),
    "references": ("references", "bibliography", "works cited"),
}

CLAIM_PATTERNS = [
    r"\b(we claim|we argue|we propose|we contend|we demonstrate|we show|we prove)\b",
    r"\b(this paper (shows|argues|demonstrates|proposes|presents|introduces))\b",
    r"\b(it follows that|therefore|thus|hence|necessarily|required|entails|implies)\b",
    r"\b(is defined as|is given by|equals|is equivalent to|we define)\b",
]

STRONG_CLAIM_PATTERNS = [
    r"\b(always|never|all|none|only|must|cannot|impossible|necessarily)\b",
    r"\b(proves|proven|demonstrates|establishes|requires|guarantees|definitive|undeniable)\b",
    r"\b(universal|fundamental|complete|final|exhaustive|irrefutable)\b",
]

EVIDENCE_PATTERNS = [
    r"\b(evidence|empirical|experimental|measured|observed|data|dataset|corpus)\b",
    r"\b(statistically|sigma|p-value|p\s*[<=>]|confidence interval|effect size|correlation)\b",
    r"\b(study|experiment|trial|test|analysis|result|finding|replication)\b",
    r"\b(sample size|n\s*=|n\s+of\s+\d+|participants|subjects)\b",
]

FALSIFIABILITY_PATTERNS = [
    r"\b(falsif\w*|disprove|refute|prediction|testable|measurable|operationali[sz]e)\b",
    r"\b(would be wrong if|fails when|breaks down|boundary condition|limit of|failure condition)\b",
    r"\b(null hypothesis|counter-example|counterexample|negative case)\b",
]

HEDGE_PATTERNS = [
    r"\b(may|might|could|possibly|perhaps|appears|seems|likely|roughly|approximately)\b",
    r"\b(suggests|indicates|points to|is consistent with|preliminary|provisional)\b",
]

COUNTERARGUMENT_PATTERNS = [
    r"\b(however|although|nevertheless|nonetheless|alternatively|by contrast)\b",
    r"\b(counterargument|counter-argument|objection|critics?|one might argue|rival account)\b",
]

LIMITATION_PATTERNS = [
    r"\b(limitations?|constraint|boundary condition|future work|scope)\b",
    r"\b(remains unclear|open question|not yet tested|provisional|unknown|unresolved)\b",
]

NOVELTY_PATTERNS = [
    r"\b(novel|new|original|for the first time)\b",
    r"\b(we introduce|we present|this work presents|this paper introduces)\b",
]

DEFINITION_PATTERNS = [
    r"\b(is defined as|we define|definition|is equivalent to|denote[sd]?)\b",
    r"\blet\s+[A-Za-z][A-Za-z0-9_]*\b",
]

QUANT_PATTERNS = [
    r"\b\d+(\.\d+)?\s*(%|σ|sigma)\b",
    r"\b(p-value|p\s*[<=>]|confidence interval|effect size|sample size|n\s*=)\b",
    r"\b\d+(\.\d+)?\b",
]

# Citation / reference patterns
AUTHOR_YEAR_RE = re.compile(r"\(([A-Z][A-Za-z'\-]+(?:\s+et\s+al\.)?(?:\s*&\s*[A-Z][A-Za-z'\-]+)?(?:\s*,\s*[A-Z][A-Za-z'\-]+)*)\s*,\s*(19\d{2}|20\d{2}|2100)\)")
NUMERIC_CITATION_RE = re.compile(r"\[(\d{1,3}(?:\s*[-,]\s*\d{1,3})*)\]")
BRACKET_YEAR_RE = re.compile(r"\[[A-Za-z][\w\s,;.&-]{1,80}(19\d{2}|20\d{2}|2100)[\w\s,;.&-]*\]")
DOI_RE = re.compile(r"\b(?:doi\s*[:.]?\s*)?(10\.\d{4,9}/[-._;()/:A-Z0-9]+)", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s)>\]]+")
FOOTNOTE_RE = re.compile(r"\[\^[\w\d-]+\]")
YEAR_RE = re.compile(r"\b(19\d{2}|20\d{2}|2100)\b")

HEADER_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
EQUATION_LINE_RE = re.compile(r"(?m)^[^\n]{0,180}(=|->|→|∑|∫|χ|Δ|∂|∇|≈|≤|≥|\bexp\(|\blog\()[^\n]{0,180}$")
INLINE_MATH_RE = re.compile(r"(?<!\\)\$[^$\n]{1,240}(?<!\\)\$")


# -----------------------------------------------------------------------------
# Dataclasses
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class Section:
    name: str
    title: str
    level: int
    start: int
    end: int


@dataclass(frozen=True)
class SentenceHit:
    sentence: str
    score: int
    reasons: tuple[str, ...]


# -----------------------------------------------------------------------------
# Text helpers
# -----------------------------------------------------------------------------

def _read_text(path_or_text: str | Path, is_path: bool) -> tuple[str, str, str]:
    if is_path:
        path = Path(path_or_text)
        text = path.read_text(encoding="utf-8", errors="ignore")
        filename = path.name
        title_match = re.search(r"^#\s+(.+)", text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else path.stem
        return text, filename, title
    return str(path_or_text), "inline", ""


def _strip_code_blocks(text: str) -> str:
    return re.sub(r"```[\s\S]*?```", " ", text)


def _norm_heading(title: str) -> str:
    cleaned = re.sub(r"[*_`#>\[\]()]+", " ", title).strip().lower()
    cleaned = re.sub(r"^\d+(\.\d+)*\s*[:.)-]?\s*", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def _split_sentences(text: str) -> list[str]:
    clean = _strip_code_blocks(text)
    clean = re.sub(r"\s+", " ", clean)
    pieces = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'`(])", clean)
    return [p.strip() for p in pieces if 35 <= len(p.strip()) <= 700]


def _pattern_count(patterns: Iterable[str], text: str) -> int:
    return sum(len(re.findall(p, text, flags=re.IGNORECASE)) for p in patterns)


def _bounded(value: float, max_value: float = 5.0) -> float:
    return round(max(0.0, min(max_value, value)), 2)


def _density(count: int | float, words: int) -> float:
    return round((float(count) / max(words, 1)) * 1000, 2)


# -----------------------------------------------------------------------------
# Section and reference parsing
# -----------------------------------------------------------------------------

def _detect_sections(text: str) -> dict[str, bool]:
    """Heading-aware section detection, with a fallback for plain text labels."""
    found = {key: False for key in SECTION_ALIASES}

    for match in HEADER_RE.finditer(text):
        heading = _norm_heading(match.group(2))
        for key, aliases in SECTION_ALIASES.items():
            if any(heading == a or heading.startswith(a + ":") for a in aliases):
                found[key] = True

    # Fallback: label-style lines like "Abstract:" without markdown heading.
    for key, aliases in SECTION_ALIASES.items():
        if found[key]:
            continue
        alias_re = "|".join(re.escape(a) for a in aliases)
        if re.search(rf"(?im)^\s*(?:{alias_re})\s*[:\-]\s*$", text):
            found[key] = True

    return found


def _section_spans(text: str) -> list[Section]:
    headers = list(HEADER_RE.finditer(text))
    sections: list[Section] = []
    for i, h in enumerate(headers):
        level = len(h.group(1))
        title = h.group(2).strip()
        start = h.end()
        end = len(text)
        for later in headers[i + 1 :]:
            if len(later.group(1)) <= level:
                end = later.start()
                break
        name = "other"
        normalized = _norm_heading(title)
        for key, aliases in SECTION_ALIASES.items():
            if any(normalized == a or normalized.startswith(a + ":") for a in aliases):
                name = key
                break
        sections.append(Section(name=name, title=title, level=level, start=start, end=end))
    return sections


def _reference_section(text: str) -> str:
    sections = _section_spans(text)
    for sec in sections:
        if sec.name == "references":
            return text[sec.start : sec.end].strip()

    # Plain-text fallback.
    match = re.search(r"(?ims)^\s*(references|bibliography|works cited)\s*[:\-]?\s*$([\s\S]*)", text)
    if not match:
        return ""
    tail = match.group(2).strip()
    next_heading = re.search(r"(?m)^\s*#{1,6}\s+\S", tail)
    return tail[: next_heading.start()].strip() if next_heading else tail


def _count_reference_entries(text: str) -> int:
    refs = _reference_section(text)
    if not refs:
        return 0

    lines = [ln.strip() for ln in refs.splitlines() if ln.strip() and ln.strip() not in {"---", "***"}]
    entries = []
    current = ""
    for line in lines:
        starts_entry = bool(re.match(r"^(\[\d+\]|\d+\.|[-*]\s+|[A-Z][A-Za-z'\-]+,\s+[A-Z])", line))
        if starts_entry and current:
            entries.append(current.strip())
            current = line
        else:
            current = f"{current} {line}".strip()
    if current:
        entries.append(current.strip())

    # Keep only plausible bibliographic entries.
    plausible = [e for e in entries if len(e) >= 25 and (YEAR_RE.search(e) or DOI_RE.search(e) or URL_RE.search(e))]
    return len(plausible)


def _citation_metrics(text: str) -> dict[str, Any]:
    ref_text = _reference_section(text)
    body_text = text.replace(ref_text, " ") if ref_text else text

    author_year = AUTHOR_YEAR_RE.findall(body_text)
    numeric = NUMERIC_CITATION_RE.findall(body_text)
    bracket_year = BRACKET_YEAR_RE.findall(body_text)
    dois = DOI_RE.findall(text)
    urls = URL_RE.findall(text)
    footnotes = FOOTNOTE_RE.findall(text)

    author_year_count = len(author_year)
    numeric_count = len(numeric)
    bracket_year_count = len(bracket_year)
    doi_count = len(set(d.lower() for d in dois))
    url_count = len(set(urls))
    footnote_count = len(set(footnotes))

    # Do not double-count bibliography URLs/DOIs as body citations. They are reference quality.
    body_url_count = len(set(URL_RE.findall(body_text)))
    body_doi_count = len(set(d.lower() for d in DOI_RE.findall(body_text)))

    total_body_citations = author_year_count + numeric_count + bracket_year_count + body_url_count + body_doi_count + footnote_count
    reference_entry_count = _count_reference_entries(text)
    citation_styles = sum(1 for n in [author_year_count, numeric_count, bracket_year_count, footnote_count] if n > 0)

    years = [int(y) for y in YEAR_RE.findall(ref_text or text)]
    recent_refs = sum(1 for y in years if y >= 2015)
    old_refs = sum(1 for y in years if y < 1990)

    return {
        "citation_count": total_body_citations,
        "author_year_citation_count": author_year_count,
        "numeric_citation_count": numeric_count,
        "bracket_year_citation_count": bracket_year_count,
        "footnote_count": footnote_count,
        "url_references": url_count,
        "doi_references": doi_count,
        "body_url_citation_count": body_url_count,
        "body_doi_citation_count": body_doi_count,
        "reference_entry_count": reference_entry_count,
        "citation_style_count": citation_styles,
        "reference_year_count": len(years),
        "recent_reference_count": recent_refs,
        "older_reference_count": old_refs,
    }


# -----------------------------------------------------------------------------
# Sentence extraction and risk analysis
# -----------------------------------------------------------------------------

def _sentence_hit(sentence: str, pattern_groups: dict[str, list[str]], bonus_terms: Iterable[str] = ()) -> SentenceHit | None:
    reasons: list[str] = []
    score = 0
    for name, patterns in pattern_groups.items():
        if any(re.search(p, sentence, flags=re.IGNORECASE) for p in patterns):
            reasons.append(name)
            score += 3
    lower = sentence.lower()
    for term in bonus_terms:
        if term in lower:
            score += 1
    if any(sym in sentence for sym in ("=", "->", "→", "χ", "Δ", "∂", "≈", "≤", "≥")):
        score += 1
    words = sentence.split()
    if 8 <= len(words) <= 55:
        score += 1
    return SentenceHit(sentence=re.sub(r"\s+", " ", sentence).strip(), score=score, reasons=tuple(reasons)) if score else None


def _top_sentence_hits(sentences: list[str], pattern_groups: dict[str, list[str]], top_n: int, bonus_terms: Iterable[str] = ()) -> list[str]:
    hits: list[SentenceHit] = []
    seen: set[str] = set()
    for sentence in sentences:
        hit = _sentence_hit(sentence, pattern_groups, bonus_terms)
        if not hit:
            continue
        key = hit.sentence.lower()
        if key in seen:
            continue
        seen.add(key)
        hits.append(hit)
    hits.sort(key=lambda h: (-h.score, len(h.sentence)))
    return [h.sentence[:280] for h in hits[:top_n]]


def _unsupported_strong_claims(sentences: list[str]) -> list[str]:
    """Find risky strong claims without citation/evidence/hedging in the same sentence."""
    risky: list[str] = []
    citation_any = re.compile(
        r"(" + AUTHOR_YEAR_RE.pattern + r"|" + NUMERIC_CITATION_RE.pattern + r"|" + BRACKET_YEAR_RE.pattern + r"|" + DOI_RE.pattern + r")",
        re.IGNORECASE,
    )
    for sent in sentences:
        has_strong = any(re.search(p, sent, re.IGNORECASE) for p in STRONG_CLAIM_PATTERNS)
        if not has_strong:
            continue
        has_evidence = any(re.search(p, sent, re.IGNORECASE) for p in EVIDENCE_PATTERNS)
        has_hedge = any(re.search(p, sent, re.IGNORECASE) for p in HEDGE_PATTERNS)
        has_citation = bool(citation_any.search(sent))
        if not (has_evidence or has_hedge or has_citation):
            risky.append(re.sub(r"\s+", " ", sent).strip()[:280])
        if len(risky) >= 5:
            break
    return risky


# -----------------------------------------------------------------------------
# Scoring
# -----------------------------------------------------------------------------

def _score_structure(sections: dict[str, bool], words: int) -> float:
    # More academic than the old 7-section count. Literature/research question/limitations matter.
    weights = {
        "abstract": 0.8,
        "introduction": 0.8,
        "literature_review": 0.8,
        "research_question": 0.7,
        "methodology": 1.0,
        "results": 0.8,
        "discussion": 0.8,
        "limitations": 0.6,
        "conclusion": 0.4,
        "references": 0.8,
    }
    raw = sum(w for k, w in weights.items() if sections.get(k))
    max_raw = sum(weights.values())
    length_factor = 0.75 if words < 800 else 0.9 if words < 1500 else 1.0
    return _bounded((raw / max_raw) * 5 * length_factor)


def _score_grounding(cites: dict[str, Any], words: int) -> float:
    body_cites = cites["citation_count"]
    refs = cites["reference_entry_count"]
    doi = cites["doi_references"]
    styles = cites["citation_style_count"]
    density = body_cites / max(words / 1000, 1)

    score = 0.0
    score += min(1.6, density / 4.0)              # body citation density
    score += min(1.4, refs / 10.0)                # bibliography depth
    score += min(0.8, doi / 4.0)                  # DOI quality
    score += 0.4 if styles == 1 else 0.15 if styles > 1 else 0.0  # consistent style preferred
    score += min(0.8, cites["recent_reference_count"] / 8.0)
    return _bounded(score)


def _score_claim_evidence(claims: int, evidence: int, unsupported: int) -> float:
    if claims == 0:
        return 1.0 if evidence > 0 else 0.0
    ratio = evidence / max(claims, 1)
    score = min(2.0, claims / 8.0) + min(2.5, ratio * 1.25)
    score -= min(1.5, unsupported * 0.3)
    return _bounded(score)


def _score_quantitative(equations: int, quant: int, definitions: int) -> float:
    score = min(2.0, equations * 0.65) + min(1.6, quant / 8.0) + min(1.4, definitions / 8.0)
    return _bounded(score)


def _score_falsifiability(falsifiability: int, counters: int, limitations: int, hedges: int, absolutes: int) -> float:
    score = min(2.0, falsifiability * 0.55) + min(1.2, counters * 0.25) + min(1.1, limitations * 0.35)
    # Academic papers need some caution, but too many absolutes relative to hedges hurts.
    if absolutes:
        score += min(0.7, hedges / absolutes * 0.18)
        if absolutes > hedges * 2 and absolutes >= 8:
            score -= 0.8
    else:
        score += min(0.7, hedges * 0.05)
    return _bounded(score)


def _grade(total: float) -> str:
    if total >= 22.5:
        return "A (Review-ready)"
    if total >= 19.0:
        return "B (Strong draft)"
    if total >= 15.0:
        return "C (Developing academic draft)"
    if total >= 10.0:
        return "D (Argument sketch)"
    return "F (Not yet academic)"


def _recommendations(result: dict[str, Any]) -> list[str]:
    recs: list[str] = []
    if result["rubric_structure_points"] < 3.5:
        missing = [label for label in [
            "abstract", "literature_review", "research_question", "methodology", "results", "limitations", "references"
        ] if not result.get(f"has_{label}", False)]
        recs.append("Add explicit academic sections: " + ", ".join(missing[:5]) + ".")
    if result["rubric_grounding_points"] < 3.5:
        recs.append("Strengthen grounding: add peer-reviewed references, DOI entries, and citations near the strongest claims.")
    if result["unsupported_strong_claim_count"]:
        recs.append("Reduce overclaim risk: qualify or cite the flagged absolute/universal claims.")
    if result["falsifiability_marker_count"] < 2:
        recs.append("State what would falsify, weaken, or bound the theory; academic readers need failure conditions.")
    if result["counterargument_count"] < 2:
        recs.append("Add a serious objection/rival-framework section and answer it directly.")
    if result["definition_marker_count"] < 3:
        recs.append("Define key terms and symbols before using them as load-bearing claims.")
    if not recs:
        recs.append("Main structure is present; next gain is external validation and tighter claim-by-claim evidence mapping.")
    return recs[:6]


# -----------------------------------------------------------------------------
# Optional Semantic Scholar lookup
# -----------------------------------------------------------------------------

def semantic_scholar_lookup(title: str, max_results: int = 5) -> dict[str, Any]:
    if not HAS_SS or not title or _SS_CLIENT is None:
        return {}
    try:  # pragma: no cover - network/API dependent
        results = _SS_CLIENT.search_paper(
            title,
            limit=max_results,
            fields=[
                "title", "year", "citationCount", "referenceCount",
                "venue", "authors", "abstract", "influentialCitationCount",
            ],
        )
        if not results or len(results) == 0:
            return {"ss_found": False}
        top = results[0]
        return {
            "ss_found": True,
            "ss_title": top.title,
            "ss_year": top.year,
            "ss_citation_count": top.citationCount,
            "ss_reference_count": top.referenceCount,
            "ss_venue": top.venue,
            "ss_influential_citations": top.influentialCitationCount,
        }
    except Exception as exc:
        return {"ss_found": False, "ss_error": str(exc)}


# -----------------------------------------------------------------------------
# Public API
# -----------------------------------------------------------------------------

def analyze(path_or_text: str | Path, is_path: bool = True, run_ss_lookup: bool = False) -> dict[str, Any]:
    text, fname, title = _read_text(path_or_text, is_path)
    analysis_text = _strip_code_blocks(text)
    tl = analysis_text.lower()
    words = len(re.findall(r"\b\w+\b", analysis_text))
    sentences = _split_sentences(analysis_text)

    sections = _detect_sections(text)
    cites = _citation_metrics(text)

    heading_count = len(HEADER_RE.findall(text))
    theory_hits = sorted({term for term in THEORY_SIGNALS if term in tl})
    theory_count = len(theory_hits)
    academic_signal_count = sum(1 for term in ACADEMIC_SIGNALS if term in tl)

    claim_marker_count = _pattern_count(CLAIM_PATTERNS, analysis_text)
    strong_claim_count = _pattern_count(STRONG_CLAIM_PATTERNS, analysis_text)
    evidence_marker_count = _pattern_count(EVIDENCE_PATTERNS, analysis_text)
    falsifiability_marker_count = _pattern_count(FALSIFIABILITY_PATTERNS, analysis_text)
    hedge_count = _pattern_count(HEDGE_PATTERNS, analysis_text)
    counterargument_count = _pattern_count(COUNTERARGUMENT_PATTERNS, analysis_text)
    limitation_count = _pattern_count(LIMITATION_PATTERNS, analysis_text)
    novelty_marker_count = _pattern_count(NOVELTY_PATTERNS, analysis_text)
    definition_marker_count = _pattern_count(DEFINITION_PATTERNS, analysis_text)
    quantitative_marker_count = _pattern_count(QUANT_PATTERNS, analysis_text)
    equation_count = len(EQUATION_LINE_RE.findall(analysis_text)) + len(INLINE_MATH_RE.findall(analysis_text))

    unsupported = _unsupported_strong_claims(sentences)

    evidence_to_claim_ratio = round(evidence_marker_count / max(claim_marker_count, 1), 2)
    hedge_to_strong_ratio = round(hedge_count / max(strong_claim_count, 1), 2)

    structure_points = _score_structure(sections, words)
    grounding_points = _score_grounding(cites, words)
    claim_points = _score_claim_evidence(claim_marker_count, evidence_marker_count, len(unsupported))
    quantitative_points = _score_quantitative(equation_count, quantitative_marker_count, definition_marker_count)
    falsifiability_points = _score_falsifiability(
        falsifiability_marker_count,
        counterargument_count,
        limitation_count,
        hedge_count,
        strong_claim_count,
    )
    rubric_total = round(
        structure_points + grounding_points + claim_points + quantitative_points + falsifiability_points,
        2,
    )

    claim_candidates = _top_sentence_hits(
        sentences,
        {"claim": CLAIM_PATTERNS, "strong_claim": STRONG_CLAIM_PATTERNS},
        top_n=3,
        bonus_terms=("therefore", "thus", "hence", "requires", "implies"),
    )
    evidence_candidates = _top_sentence_hits(
        sentences,
        {"evidence": EVIDENCE_PATTERNS},
        top_n=3,
        bonus_terms=("data", "evidence", "observed", "measured", "result"),
    )
    falsifiability_candidates = _top_sentence_hits(
        sentences,
        {"falsifiability": FALSIFIABILITY_PATTERNS, "limitation": LIMITATION_PATTERNS},
        top_n=3,
        bonus_terms=("wrong", "fails", "boundary", "testable"),
    )

    result: dict[str, Any] = {
        "file": fname,
        "title_detected": title[:120],
        "word_count": words,
        "sentence_count": len(sentences),
        "heading_count": heading_count,
        "academic_signal_count": academic_signal_count,
        "academic_signal_density": _density(academic_signal_count, words),
        "external_theory_count": theory_count,
        "external_theories": ", ".join(theory_hits[:12]),
        "structure_score": f"{sum(sections.values())}/{len(sections)}",
        # Backward-compatible fields from v1.
        "has_abstract": sections["abstract"],
        "has_introduction": sections["introduction"],
        "has_methodology": sections["methodology"],
        "has_results": sections["results"],
        "has_discussion": sections["discussion"],
        "has_conclusion": sections["conclusion"],
        "has_references_section": sections["references"],
        # New section fields.
        "has_literature_review": sections["literature_review"],
        "has_research_question": sections["research_question"],
        "has_limitations": sections["limitations"],
        **cites,
        "citation_density_per1k": _density(cites["citation_count"], words),
        "claim_marker_count": claim_marker_count,
        "claim_density_per1k": _density(claim_marker_count, words),
        "strong_claim_count": strong_claim_count,
        "strong_claim_density_per1k": _density(strong_claim_count, words),
        "evidence_marker_count": evidence_marker_count,
        "evidence_density_per1k": _density(evidence_marker_count, words),
        "evidence_to_claim_ratio": evidence_to_claim_ratio,
        "falsifiability_marker_count": falsifiability_marker_count,
        "falsifiability_density_per1k": _density(falsifiability_marker_count, words),
        "hedge_count": hedge_count,
        "hedge_density_per1k": _density(hedge_count, words),
        "absolute_claim_count": strong_claim_count,
        "absolute_density_per1k": _density(strong_claim_count, words),
        "hedge_to_absolute_ratio": hedge_to_strong_ratio,
        "counterargument_count": counterargument_count,
        "limitation_count": limitation_count,
        "novelty_marker_count": novelty_marker_count,
        "definition_marker_count": definition_marker_count,
        "quantitative_marker_count": quantitative_marker_count,
        "equation_count": equation_count,
        "equation_density_per1k": _density(equation_count, words),
        "unsupported_strong_claim_count": len(unsupported),
        "unsupported_strong_claim_1": unsupported[0] if len(unsupported) > 0 else "",
        "unsupported_strong_claim_2": unsupported[1] if len(unsupported) > 1 else "",
        "unsupported_strong_claim_3": unsupported[2] if len(unsupported) > 2 else "",
        "claim_candidate_1": claim_candidates[0] if len(claim_candidates) > 0 else "",
        "claim_candidate_2": claim_candidates[1] if len(claim_candidates) > 1 else "",
        "claim_candidate_3": claim_candidates[2] if len(claim_candidates) > 2 else "",
        "evidence_candidate_1": evidence_candidates[0] if len(evidence_candidates) > 0 else "",
        "evidence_candidate_2": evidence_candidates[1] if len(evidence_candidates) > 1 else "",
        "evidence_candidate_3": evidence_candidates[2] if len(evidence_candidates) > 2 else "",
        "falsifiability_candidate_1": falsifiability_candidates[0] if len(falsifiability_candidates) > 0 else "",
        "falsifiability_candidate_2": falsifiability_candidates[1] if len(falsifiability_candidates) > 1 else "",
        "falsifiability_candidate_3": falsifiability_candidates[2] if len(falsifiability_candidates) > 2 else "",
        "rubric_structure_points": structure_points,
        "rubric_grounding_points": grounding_points,
        "rubric_claim_points": claim_points,
        "rubric_quantitative_points": quantitative_points,
        "rubric_falsifiability_points": falsifiability_points,
        "academic_rubric_total": rubric_total,
        "academic_rubric_grade": _grade(rubric_total),
    }

    # Preserve old simple grade field, but make it use the better rubric.
    result["academic_grade"] = result["academic_rubric_grade"]
    result["recommendations"] = _recommendations(result)
    result["recommendation_1"] = result["recommendations"][0] if result["recommendations"] else ""
    result["recommendation_2"] = result["recommendations"][1] if len(result["recommendations"]) > 1 else ""
    result["recommendation_3"] = result["recommendations"][2] if len(result["recommendations"]) > 2 else ""

    if run_ss_lookup and title:
        result.update(semantic_scholar_lookup(title))

    return result


def analyze_many(paths: Iterable[str | Path], run_ss_lookup: bool = False) -> list[dict[str, Any]]:
    return [analyze(Path(p), is_path=True, run_ss_lookup=run_ss_lookup) for p in paths]


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def _paths_from_target(target: Path, pattern: str) -> list[Path]:
    if target.is_file():
        return [target]
    if target.is_dir():
        return sorted(p for p in target.rglob(pattern) if p.is_file())
    raise FileNotFoundError(f"Path not found: {target}")


def _write_csv(rows: list[dict[str, Any]], output: Path) -> None:
    if not rows:
        output.write_text("", encoding="utf-8")
        return
    keys: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in keys and key != "recommendations":
                keys.append(key)
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Academic standard scorer for Markdown/text papers.")
    parser.add_argument("target", help="File or folder to analyze")
    parser.add_argument("--pattern", default="*.md", help="Glob pattern when target is a folder. Default: *.md")
    parser.add_argument("--ss", action="store_true", help="Optional Semantic Scholar lookup when installed/configured")
    parser.add_argument("--format", choices=("json", "csv"), default="json")
    parser.add_argument("--out", help="Optional output path. Prints to stdout if omitted.")
    args = parser.parse_args(argv)

    paths = _paths_from_target(Path(args.target), args.pattern)
    rows = analyze_many(paths, run_ss_lookup=args.ss)

    if args.format == "csv":
        if args.out:
            _write_csv(rows, Path(args.out))
        else:
            import sys
            writer = csv.DictWriter(sys.stdout, fieldnames=[k for k in rows[0].keys() if k != "recommendations"] if rows else [])
            writer.writeheader()
            writer.writerows(rows)
    else:
        payload: Any = rows[0] if len(rows) == 1 else rows
        text = json.dumps(payload, indent=2, ensure_ascii=False)
        if args.out:
            Path(args.out).write_text(text, encoding="utf-8")
        else:
            print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
