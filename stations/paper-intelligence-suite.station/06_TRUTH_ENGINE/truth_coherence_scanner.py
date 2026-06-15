#!/usr/bin/env python3
"""
Scan local documents and web pages into truth/coherence records.

Outputs:
- truth_coherence_records.json
- truth_coherence_records.csv
- truth_coherence_summary.md

Design goal:
- extraction and scoring first
- explainable features
- stable enough to compare corpora later

================================================================================
KNOWN ISSUES — READ BEFORE TRUSTING THIS SCANNER ON A NEW CORPUS TYPE
================================================================================
See ./KNOWN_ISSUES.md for the full list, reproduction steps, and regression
test results.

ISSUE-001 (RESOLVED 2026-04-07): meta-rhetoric beat facts on spoken English.
Fix: two-channel evidence anchoring — lexical + spaCy NER, combined as
max(lexical, ner_anchor). The Charlie Kirk timeline-contradiction sentence
in the test corpus moved from #8 → #1; the meta-rhetoric sentence dropped
from #1 → #3. Backwards-compatible with academic papers (max() means lexical
text loses nothing). spaCy is loaded lazily and falls back to legacy lexical-
only behavior if the package or model is unavailable.

ISSUE-002 (OPEN): anti-fruits lexicons are 4 terms each — too narrow to fire
on most real text. fruit_integrity_score effectively collapses to fruits-only.

ISSUE-003 (OPEN): EVIDENCE_TERMS lexicon misses journalism/legal/financial
vocabulary ("records show", "according to", "court documents", "the filing",
etc.). Lower priority since the NER channel from ISSUE-001's fix now picks
up most of the named-entity load on transcripts.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.error import URLError
from urllib.request import Request, urlopen


# ─── NER (lazy spaCy loader for the second evidence channel) ────────────────
# See KNOWN_ISSUES.md ISSUE-001. spaCy en_core_web_sm is loaded once and cached.
# If spaCy or the model is unavailable, the scanner falls back to lexical-only
# evidence anchoring (legacy behavior) and ner_anchor stays at 0.0.
_NLP_CACHE = {"loaded": False, "nlp": None}
NER_KEEP_LABELS = {
    "PERSON", "ORG", "DATE", "MONEY", "GPE", "CARDINAL",
    "LOC", "EVENT", "FAC", "NORP", "TIME", "PERCENT", "QUANTITY",
}

def _get_nlp():
    if _NLP_CACHE["loaded"]:
        return _NLP_CACHE["nlp"]
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm", disable=["lemmatizer", "tagger", "attribute_ruler"])
        _NLP_CACHE["nlp"] = nlp
    except Exception:
        _NLP_CACHE["nlp"] = None
    _NLP_CACHE["loaded"] = True
    return _NLP_CACHE["nlp"]


def _doc_entity_strings(text: str) -> list[str]:
    """Parse `text` once with spaCy and return all kept entity strings."""
    nlp = _get_nlp()
    if nlp is None or not text.strip():
        return []
    try:
        doc = nlp(text)
        return [e.text for e in doc.ents if e.label_ in NER_KEEP_LABELS]
    except Exception:
        return []


def _ner_anchor_for_sentence(sentence: str, doc_entities: list[str]) -> float:
    """How many doc-level NER entities appear in this sentence (0..1)."""
    if not doc_entities:
        return 0.0
    s_lower = sentence.lower()
    hits = 0
    for ent in doc_entities:
        et = ent.lower().strip()
        if len(et) >= 2 and et in s_lower:
            hits += 1
    # 3+ entity hits = full anchor. Tunable.
    return min(1.0, hits / 3.0)


SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_\-']+")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
DATASET_RE = re.compile(r"\b(PEAR|GCP|DESI|PROP-COSMOS|JAX|Oxford|CTNS|sigma|p_value|effect size)\b", re.IGNORECASE)
NUMBER_RE = re.compile(r"\b\d+(?:\.\d+)?(?:σ|%|x)?\b")
EQUATION_RE = re.compile(r"[=∭χλμσΔ]|\\[A-Za-z]+")
URL_RE = re.compile(r"^https?://", re.IGNORECASE)
EXCLUDED_DIR_NAMES = {
    "_ANALYTICS",
    "_OUTPUTS",
    "_SYSTEM",
    "_STAGING",
    "Data_Analytics",
    "__pycache__",
}
EXCLUDED_FILE_NAMES = {
    "WEB_TEMPLATE_TYPE.md",
    "PIPELINE_POINTER.md",
    "summary.md",
    "README.md",
}
EXCLUDED_FILE_PATTERNS = [
    re.compile(r"redirect\.html$", re.IGNORECASE),
    re.compile(r"_audit", re.IGNORECASE),
    re.compile(r"audit", re.IGNORECASE),
    re.compile(r"report", re.IGNORECASE),
    re.compile(r"diagnostic", re.IGNORECASE),
    re.compile(r"media_block", re.IGNORECASE),
]

CLAIM_TERMS = {
    "must", "is", "are", "requires", "demands", "forces", "proves", "shows",
    "indicates", "explains", "grounds", "predicts", "means",
}
EVIDENCE_TERMS = {
    "data", "dataset", "study", "source", "evidence", "measured", "observed",
    "experiment", "trial", "equation", "proof", "replicated", "confirmed",
}
FALSIFY_TERMS = {
    "falsify", "falsification", "kill", "disconfirm", "if false", "would fail",
    "breaks if", "collapse if", "death condition", "invalidates",
}
DEPENDENCY_TERMS = {
    "depends on", "requires", "assumes", "given", "if", "because", "under",
    "boundary condition", "premise",
}
HEDGE_TERMS = {
    "maybe", "perhaps", "possibly", "appears", "seems", "might", "could",
    "likely", "probably", "roughly", "sort of", "kind of",
}
ABSOLUTE_TERMS = {
    "always", "never", "undeniable", "proves", "certainly", "obviously", "impossible",
}
BRIDGE_TERMS = {
    "therefore", "thus", "because", "so", "then", "however", "but", "next",
    "this means", "as a result", "consequently",
}
NEGATION_TERMS = {"not", "never", "no", "cannot", "can't", "fails", "false"}

FRUITS_LEXICON = {
    "love": {"love", "charity", "care", "caring", "compassion", "agape", "sacrifice", "sacrificial", "communion", "covenantal"},
    "joy": {"joy", "delight", "glad", "gladness", "rejoice", "rejoicing", "gratitude", "abundance", "flourishing", "celebration"},
    "peace": {"peace", "calm", "rest", "reconcile", "reconciliation", "shalom", "harmony", "wholeness", "stability", "nonviolence"},
    "patience": {"patience", "patient", "longsuffering", "long-suffering", "endure", "endurance", "wait", "waiting", "perseverance", "delayed gratification"},
    "kindness": {"kindness", "kind", "mercy", "gentle", "generosity", "hospitality", "benevolent", "benevolence", "tender", "tenderness"},
    "goodness": {"goodness", "good", "upright", "virtue", "righteous", "righteousness", "integrity", "honest", "honorable", "moral excellence"},
    "faithfulness": {"faithfulness", "faithful", "loyal", "loyalty", "steadfast", "fidelity", "reliable", "consistent", "committed", "covenant"},
    "gentleness": {"gentleness", "gentle", "softly", "meek", "meekness", "humble", "humility", "lowly", "soft answer", "restraint"},
    "self_control": {"self-control", "self control", "self_control", "discipline", "disciplined", "restrain", "restraint", "measured", "temperance", "moderation", "sober"},
}

# Canonical anti-fruit families: hatred, despair, anxiety, impatience, cruelty,
# corruption, betrayal, harshness, addiction.
ANTI_FRUITS_LEXICON = {
    "love": {"hatred", "hate", "contempt", "cruelty", "malice", "resentment", "dehumanize", "dehumanization", "exploit", "exploitation", "domination", "violence", "hostility", "bitterness", "vengeance", "rivalry"},
    "joy": {"despair", "misery", "nihilism", "hopeless", "hopelessness", "cynicism", "dread", "grief", "depression", "emptiness", "meaninglessness", "apathy", "bleak", "despondent", "anguish"},
    "peace": {"chaos", "panic", "anxiety", "anxious", "violence", "hostility", "conflict", "unrest", "agitation", "fear", "dread", "turbulence", "disorder", "fragmentation", "war"},
    "patience": {"impatience", "rash", "reactionary", "restless", "hurry", "rushed", "impulsive", "immediate", "instant", "frantic", "short-term", "volatility", "escalation", "snap", "reactive"},
    "kindness": {"harsh", "brutal", "unkind", "vindictive", "cruel", "contemptuous", "scorn", "mockery", "callous", "punitive", "merciless", "humiliation", "derision", "sneer", "hostility"},
    "goodness": {"corrupt", "corruption", "depraved", "wicked", "dishonest", "exploitation", "vice", "injustice", "perverse", "immoral", "fraud", "predatory", "abuse", "evil", "compromised"},
    "faithfulness": {"fickle", "treacherous", "faithless", "betray", "betrayal", "disloyal", "abandonment", "unfaithful", "unreliable", "break faith", "broken promise", "infidelity", "apostasy", "defection"},
    "gentleness": {"abrasive", "dominating", "coercive", "coercive pressure", "bullying", "harshness", "aggression", "forceful", "authoritarian", "intimidation", "threatening", "domineering", "controlling", "humiliation"},
    "self_control": {"impulsive", "undisciplined", "unrestrained", "reckless", "addiction", "addictive", "indulgence", "compulsive", "appetite", "craving", "excess", "binge", "ungoverned", "out of control", "license"},
}

CHARACTER_ATTRIBUTE_PATTERNS = {
    "spiritual_coherence": {
        "kind": "protective",
        "positive": {
            "consistent worldview", "coherent theology", "transparent faith", "sacrificial love",
            "servant heart", "genuine worship", "walks the talk", "glorifies god",
        },
        "negative": {
            "contradictory statements", "selective scripture", "self-serving theology",
            "manipulates faith", "twists scripture",
        },
    },
    "humility_index": {
        "kind": "protective",
        "positive": {
            "acknowledges mistakes", "seeks guidance", "gives credit to others",
            "admits uncertainty", "teachable spirit", "puts others first", "servant leadership",
        },
        "negative": {
            "claims infallibility", "never admits error", "takes all credit",
            "refuses counsel", "shows arrogance", "demands worship", "places self above all",
        },
    },
    "spiritual_discernment": {
        "kind": "protective",
        "positive": {
            "tests the spirits", "discerns motives", "sees through deception",
            "spiritual maturity", "recognizes false teaching", "identifies wolves",
        },
        "negative": {
            "easily deceived", "follows blindly", "lacks discernment", "naive trust",
        },
    },
    "moral_courage": {
        "kind": "protective",
        "positive": {
            "stands for truth", "resists pressure", "defends the innocent", "speaks against injustice",
            "sacrifices for others", "maintains integrity", "refuses compromise",
        },
        "negative": {
            "compromises principles", "follows crowd", "stays silent about evil",
            "abandons principles for gain",
        },
    },
    "deception_mastery": {
        "kind": "threat",
        "positive": {
            "controls narrative", "shapes perception", "manages information",
            "selective truth telling", "creates false consensus", "gaslighting",
            "manipulates media", "curates reality", "spin doctor", "narrative architect",
        },
        "negative": {
            "transparent communication", "admits when wrong", "open information",
            "welcomes scrutiny", "provides full context",
        },
    },
    "charismatic_manipulation": {
        "kind": "threat",
        "positive": {
            "inspires cult-like devotion", "creates parasocial bonds", "uses emotional manipulation",
            "exploits trust", "false intimacy", "creates dependency", "demands loyalty",
            "uses charm to deceive", "magnetic personality", "mesmerizing presence",
        },
        "negative": {
            "encourages independence", "transparent motives", "empowers others",
            "builds genuine community", "honest leadership",
        },
    },
    "authority_usurpation": {
        "kind": "threat",
        "positive": {
            "undermines institutions", "replaces established authority", "creates parallel power structures",
            "demands supreme loyalty", "consolidates control", "eliminates opposition",
            "bypasses democratic processes", "executive overreach", "concentrates authority",
        },
        "negative": {
            "respects institutions", "shares power", "accountable to others",
            "respects checks and balances", "distributes authority",
        },
    },
    "global_solution_complex": {
        "kind": "threat",
        "positive": {
            "one solution for humanity", "final answer to", "era of universal peace",
            "global integration", "ushering in a new age", "global governance",
            "world government", "single global framework", "comprehensive solutions",
        },
        "negative": {
            "respects local autonomy", "acknowledges complexity", "distributed solutions",
            "respects national sovereignty", "bottom-up approach",
        },
    },
}


class HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self.skip_depth += 1
        if tag in {"p", "div", "section", "article", "br", "li", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self.skip_depth:
            self.skip_depth -= 1
        if tag in {"p", "div", "section", "article", "li"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def get_text(self) -> str:
        return re.sub(r"\n{3,}", "\n\n", unescape("".join(self.parts))).strip()


@dataclass
class SentenceScore:
    index: int
    text: str
    claim_strength: float
    evidence_anchor: float
    falsifiability_signal: float
    dependency_signal: float
    precision_signal: float
    hedge_pressure: float
    absolute_pressure: float
    contradiction_pressure: float
    truth_score: float
    truth_status: str


@dataclass
class ClaimRecord:
    source: str
    claim_index: int
    sentence_index: int
    paragraph_index: int
    claim_text: str
    claim_kind: str
    support_status: str
    evidence_present: bool
    falsifiability_present: bool
    dependency_present: bool
    hedge_present: bool
    absolute_overreach: bool
    local_contradiction: bool
    precision_present: bool
    claim_status: str
    claim_score: float


@dataclass
class DocumentRecord:
    source: str
    source_type: str
    title: str
    sentence_count: int
    paragraph_count: int
    section_count: int
    truth_score: float
    coherence_score: float
    combined_score: float
    evidence_density: float
    falsifiability_density: float
    hedge_density: float
    contradiction_flags: int
    absolute_pressure: float
    rhetorical_force: float
    warmth_score: float
    discipline_score: float
    fruit_integrity_score: float
    anti_fruit_pressure: float
    claim_count: int
    anchored_claims: int
    under_supported_claims: int
    overstated_claims: int
    speculative_claims: int
    contradictory_claims: int
    falsifiable_claims: int
    integrity_profiles: list[str] = field(default_factory=list)
    fruits_vector: dict[str, float] = field(default_factory=dict)
    anti_fruits_vector: dict[str, float] = field(default_factory=dict)
    character_attributes: dict[str, dict[str, float | str]] = field(default_factory=dict)
    character_profile: dict[str, object] = field(default_factory=dict)
    character_posture: list[str] = field(default_factory=list)
    top_supported_sentences: list[str] = field(default_factory=list)
    top_risky_sentences: list[str] = field(default_factory=list)


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def normalize_whitespace(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text.replace("\r", "")).strip()


def read_text_from_path(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() in {".html", ".htm"}:
        return html_to_text(text)
    return text


def fetch_url_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "TheophysicsTruthScanner/1.0"})
    with urlopen(request, timeout=20) as response:
        body = response.read().decode("utf-8", errors="ignore")
    return html_to_text(body)


def html_to_text(html: str) -> str:
    parser = HTMLTextExtractor()
    parser.feed(html)
    return normalize_whitespace(parser.get_text())


def split_sections(text: str) -> list[tuple[str, str]]:
    headings = list(HEADING_RE.finditer(text))
    if not headings:
        return [("Document", text)]
    sections: list[tuple[str, str]] = []
    for i, match in enumerate(headings):
        start = match.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        title = match.group(2).strip()
        content = text[start:end].strip()
        if content:
            sections.append((title, content))
    return sections or [("Document", text)]


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def split_sentences(text: str) -> list[str]:
    rough = SENTENCE_RE.split(text)
    return [normalize_whitespace(s) for s in rough if len(normalize_whitespace(s)) >= 20]


def tokenize(text: str) -> list[str]:
    return [m.group(0).lower() for m in WORD_RE.finditer(text)]


def contains_phrase(text: str, phrases: Iterable[str]) -> bool:
    lower = text.lower()
    return any(phrase in lower for phrase in phrases)


def count_terms(tokens: list[str], terms: set[str]) -> int:
    return sum(1 for token in tokens if token in terms)


def count_lexicon_hits(text: str, tokens: list[str], terms: set[str]) -> int:
    lower = text.lower()
    token_hits = 0
    phrase_hits = 0
    for term in terms:
        t = term.lower().strip()
        if not t:
            continue
        if re.search(r"[\s\-_]", t):
            pattern = re.escape(t)
            pattern = pattern.replace(r"\ ", r"[\s\-_]+").replace(r"\-", r"[\s\-_]+").replace("_", r"[\s\-_]+")
            phrase_hits += len(re.findall(rf"(?<![a-z0-9]){pattern}(?![a-z0-9])", lower))
        else:
            token_hits += sum(1 for token in tokens if token == t)
    return token_hits + phrase_hits


def sentence_truth(sentence: str, ner_anchor: float = 0.0) -> SentenceScore:
    tokens = tokenize(sentence)
    token_count = max(len(tokens), 1)

    claim_strength = clamp((count_terms(tokens, CLAIM_TERMS) + (1 if len(tokens) > 10 else 0)) / 5.0)
    lexical_anchor = clamp(
        (
            count_terms(tokens, EVIDENCE_TERMS)
            + (1 if DATASET_RE.search(sentence) else 0)
            + (1 if NUMBER_RE.search(sentence) else 0)
            + (1 if "http" in sentence.lower() else 0)
        )
        / 5.0
    )
    # Two-channel evidence: lexical (current) + NER (new). Take the max so
    # transcripts with named entities (PERSON, ORG, DATE, MONEY, GPE) anchor
    # as strongly as papers with lexical evidence terms ("data", "study").
    # See KNOWN_ISSUES.md ISSUE-001 for the test that motivated this.
    evidence_anchor = clamp(max(lexical_anchor, ner_anchor))
    falsifiability_signal = clamp(
        (
            (1 if contains_phrase(sentence, FALSIFY_TERMS) else 0)
            + (1 if "if" in tokens and any(x in tokens for x in {"false", "fails", "breaks"}) else 0)
        )
        / 2.0
    )
    dependency_signal = clamp(
        (
            (1 if contains_phrase(sentence, DEPENDENCY_TERMS) else 0)
            + (1 if "because" in tokens else 0)
            + (1 if "requires" in tokens else 0)
        )
        / 3.0
    )
    precision_signal = clamp(
        (
            (1 if EQUATION_RE.search(sentence) else 0)
            + (1 if NUMBER_RE.search(sentence) else 0)
            + (1 if DATASET_RE.search(sentence) else 0)
        )
        / 3.0
    )
    hedge_pressure = clamp(count_terms(tokens, HEDGE_TERMS) / max(2.0, token_count / 8.0))
    absolute_pressure = clamp(count_terms(tokens, ABSOLUTE_TERMS) / max(2.0, token_count / 8.0))

    contradiction_pressure = 0.0
    lower = sentence.lower()
    if any(term in lower for term in ABSOLUTE_TERMS) and any(term in lower for term in HEDGE_TERMS):
        contradiction_pressure += 0.5
    if "proven" in lower and any(term in lower for term in {"unknown", "uncertain", "maybe", "tentative"}):
        contradiction_pressure += 0.5
    contradiction_pressure = clamp(contradiction_pressure)

    positive = 0.28 * claim_strength + 0.26 * evidence_anchor + 0.18 * falsifiability_signal + 0.14 * dependency_signal + 0.14 * precision_signal
    negative = 0.45 * hedge_pressure + 0.30 * absolute_pressure + 0.25 * contradiction_pressure
    truth_score = clamp(positive - negative + 0.35)

    if truth_score >= 0.7:
        status = "supported"
    elif truth_score >= 0.5:
        status = "mixed"
    elif hedge_pressure > 0.25 and evidence_anchor < 0.25:
        status = "speculative"
    else:
        status = "unsupported"

    return SentenceScore(
        index=0,
        text=sentence,
        claim_strength=round(claim_strength, 4),
        evidence_anchor=round(evidence_anchor, 4),
        falsifiability_signal=round(falsifiability_signal, 4),
        dependency_signal=round(dependency_signal, 4),
        precision_signal=round(precision_signal, 4),
        hedge_pressure=round(hedge_pressure, 4),
        absolute_pressure=round(absolute_pressure, 4),
        contradiction_pressure=round(contradiction_pressure, 4),
        truth_score=round(truth_score, 4),
        truth_status=status,
    )


def classify_claim_kind(sentence: str) -> str:
    lower = sentence.lower()
    if EQUATION_RE.search(sentence):
        return "mathematical"
    if any(term in lower for term in ["predict", "will", "expected", "forecast"]):
        return "predictive"
    if any(term in lower for term in ["because", "causes", "grounds", "explains"]):
        return "causal"
    if any(term in lower for term in ["must", "necessary", "required", "demands", "forces"]):
        return "ontological"
    return "descriptive"


def is_claim_sentence(sentence: str, score: SentenceScore) -> bool:
    lower = sentence.lower()
    if len(tokenize(sentence)) < 6:
        return False
    if score.claim_strength >= 0.2:
        return True
    return any(token in lower for token in [" is ", " are ", " must ", " requires ", " proves ", " shows ", " means "])


def claim_status_from_score(score: SentenceScore) -> tuple[str, str]:
    evidence_present = score.evidence_anchor >= 0.4
    falsifiable = score.falsifiability_signal >= 0.4
    dependency_present = score.dependency_signal >= 0.34
    hedge_present = score.hedge_pressure >= 0.25
    overreach = score.absolute_pressure >= 0.25
    contradiction = score.contradiction_pressure >= 0.5

    if contradiction:
        return "contradictory", "contradictory"
    if evidence_present and (falsifiable or dependency_present):
        return "anchored", "anchored"
    if hedge_present and not evidence_present:
        return "speculative", "speculative"
    if overreach and not evidence_present:
        return "overstated", "overstated"
    if score.claim_strength >= 0.2 and not evidence_present:
        return "under-supported", "under-supported"
    if falsifiable or dependency_present:
        return "bounded", "bounded"
    return "needs-review", "needs-review"


def extract_claim_records(source: str, sentence_scores: list[SentenceScore],
                          sentence_to_para: dict[int, int] | None = None) -> list[ClaimRecord]:
    claims: list[ClaimRecord] = []
    claim_index = 0
    _s2p = sentence_to_para or {}
    for sentence_score in sentence_scores:
        if not is_claim_sentence(sentence_score.text, sentence_score):
            continue
        support_status, claim_status = claim_status_from_score(sentence_score)
        claims.append(
            ClaimRecord(
                source=source,
                claim_index=claim_index,
                sentence_index=sentence_score.index,
                paragraph_index=_s2p.get(sentence_score.index, -1),
                claim_text=sentence_score.text,
                claim_kind=classify_claim_kind(sentence_score.text),
                support_status=support_status,
                evidence_present=sentence_score.evidence_anchor >= 0.4,
                falsifiability_present=sentence_score.falsifiability_signal >= 0.4,
                dependency_present=sentence_score.dependency_signal >= 0.34,
                hedge_present=sentence_score.hedge_pressure >= 0.25,
                absolute_overreach=sentence_score.absolute_pressure >= 0.25,
                local_contradiction=sentence_score.contradiction_pressure >= 0.5,
                precision_present=sentence_score.precision_signal >= 0.34,
                claim_status=claim_status,
                claim_score=sentence_score.truth_score,
            )
        )
        claim_index += 1
    return claims


def term_overlap(a: str, b: str) -> float:
    ta = set(tokenize(a))
    tb = set(tokenize(b))
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def heading_alignment_score(heading: str, paragraphs: list[str]) -> float:
    if not paragraphs or heading == "Document":
        return 0.5
    joined = " ".join(paragraphs[:2])
    heading_terms = set(tokenize(heading))
    body_terms = set(tokenize(joined))
    if not heading_terms:
        return 0.5
    return clamp(len(heading_terms & body_terms) / max(1, len(heading_terms)))


def fruits_vector(text: str) -> dict[str, float]:
    tokens = tokenize(text)
    token_count = max(len(tokens), 1)
    vector: dict[str, float] = {}
    for key, lexicon in FRUITS_LEXICON.items():
        hits = count_lexicon_hits(text, tokens, lexicon)
        vector[key] = round(clamp(hits / max(2.0, token_count / 120.0)), 4)
    return vector


def anti_fruits_vector(text: str) -> dict[str, float]:
    tokens = tokenize(text)
    token_count = max(len(tokens), 1)
    vector: dict[str, float] = {}
    for key, lexicon in ANTI_FRUITS_LEXICON.items():
        hits = count_lexicon_hits(text, tokens, lexicon)
        vector[key] = round(clamp(hits / max(2.0, token_count / 120.0)), 4)
    return vector


def analyze_character_attributes(text: str) -> tuple[dict[str, dict[str, float | str]], dict[str, object]]:
    lower = text.lower()
    attributes: dict[str, dict[str, float | str]] = {}
    threat_total = 0.0
    protection_total = 0.0

    for name, config in CHARACTER_ATTRIBUTE_PATTERNS.items():
        pos_hits = sum(1 for phrase in config["positive"] if phrase in lower)
        neg_hits = sum(1 for phrase in config["negative"] if phrase in lower)
        raw_strength = clamp((pos_hits - 0.5 * neg_hits) / max(1.0, len(config["positive"]) * 0.35))
        counter_pressure = clamp(neg_hits / max(1.0, len(config["negative"]) * 0.5))
        net_score = clamp(raw_strength - 0.35 * counter_pressure)
        attributes[name] = {
            "kind": config["kind"],
            "positive_hits": float(pos_hits),
            "negative_hits": float(neg_hits),
            "strength": round(raw_strength, 4),
            "counter_pressure": round(counter_pressure, 4),
            "net_score": round(net_score, 4),
        }
        if config["kind"] == "threat":
            threat_total += net_score
        else:
            protection_total += net_score

    primary_threats = [name for name, data in attributes.items() if data["kind"] == "threat" and float(data["net_score"]) >= 0.15]
    primary_protections = [name for name, data in attributes.items() if data["kind"] == "protective" and float(data["net_score"]) >= 0.15]

    profile = {
        "threat_score": round(threat_total, 4),
        "protection_score": round(protection_total, 4),
        "balance_score": round(protection_total - threat_total, 4),
        "primary_threats": primary_threats,
        "primary_protections": primary_protections,
    }
    return attributes, profile


def derive_character_posture(
    fruit_vector: dict[str, float],
    anti_vector: dict[str, float],
    truth_score: float,
    coherence_score: float,
) -> tuple[list[str], float, float]:
    profiles: list[str] = []
    fruit_integrity_score = clamp(average(list(fruit_vector.values())) - 0.65 * average(list(anti_vector.values())) + 0.25)
    anti_fruit_pressure = clamp(average(list(anti_vector.values())))

    if fruit_integrity_score >= 0.34 and anti_fruit_pressure < 0.08:
        profiles.append("spiritually ordered")
    if anti_fruit_pressure >= 0.12 and fruit_integrity_score < 0.24:
        profiles.append("anti-fruit dominant")
    if anti_vector["kindness"] >= 0.12 or anti_vector["gentleness"] >= 0.12:
        profiles.append("abrasive or coercive")
    if anti_vector["peace"] >= 0.12 or anti_vector["patience"] >= 0.12:
        profiles.append("agitated or reactionary")
    if anti_vector["goodness"] >= 0.10 or anti_vector["faithfulness"] >= 0.10:
        profiles.append("morally unstable")
    if fruit_vector["self_control"] >= 0.12 and anti_vector["self_control"] < 0.08:
        profiles.append("disciplined")
    if fruit_vector["love"] >= 0.10 and fruit_vector["kindness"] >= 0.10 and anti_vector["kindness"] < 0.08:
        profiles.append("charitable")
    if truth_score >= 0.42 and coherence_score >= 0.28 and anti_fruit_pressure >= 0.12:
        profiles.append("technically strong, spiritually corrosive")
    if truth_score >= 0.42 and coherence_score >= 0.28 and fruit_integrity_score >= 0.30:
        profiles.append("technically strong, spiritually ordered")
    if truth_score < 0.38 and fruit_integrity_score >= 0.28:
        profiles.append("humble but under-defended")
    if not profiles:
        profiles.append("mixed spiritual posture")
    return sorted(set(profiles)), round(fruit_integrity_score, 4), round(anti_fruit_pressure, 4)


def average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def derive_integrity_profiles(
    truth_score: float,
    coherence_score: float,
    evidence_density: float,
    falsifiability_density: float,
    hedge_density: float,
    contradiction_rate: float,
    absolute_pressure: float,
    rhetorical_force: float,
    warmth_score: float,
    discipline_score: float,
) -> list[str]:
    profiles: list[str] = []

    if truth_score >= 0.42 and coherence_score < 0.30 and evidence_density >= 0.12 and absolute_pressure < 0.18:
        profiles.append("truth-seeking but rough")
    if coherence_score >= 0.34 and evidence_density < 0.10 and falsifiability_density < 0.04 and absolute_pressure >= 0.10:
        profiles.append("polished but manipulative")
    if coherence_score >= 0.32 and warmth_score < 0.10 and truth_score >= 0.36:
        profiles.append("coherent but cold")
    if evidence_density < 0.10 and hedge_density >= 0.08 and absolute_pressure < 0.10 and warmth_score >= 0.08:
        profiles.append("evidence-light but humble")
    if truth_score >= 0.48 and coherence_score >= 0.28 and contradiction_rate < 0.08 and hedge_density < 0.10 and absolute_pressure < 0.15:
        profiles.append("forceful and disciplined")
    if rhetorical_force >= 0.16 and warmth_score < 0.08 and discipline_score < 0.08 and truth_score < 0.46:
        profiles.append("confident but spiritually rotten")
    if rhetorical_force >= 0.14 and evidence_density < 0.10:
        profiles.append("high-claim, low-support")
    if evidence_density >= 0.18 and coherence_score < 0.28:
        profiles.append("high-support, low-clarity")
    if falsifiability_density >= 0.05 and evidence_density >= 0.10 and coherence_score >= 0.28:
        profiles.append("falsifiable and mature")
    if truth_score < 0.40 and evidence_density < 0.10 and absolute_pressure >= 0.10:
        profiles.append("assertive without warrant")
    if warmth_score >= 0.10 and truth_score < 0.40 and falsifiability_density < 0.03:
        profiles.append("gentle but evasive")
    if rhetorical_force >= 0.12 and warmth_score < 0.08 and truth_score >= 0.40:
        profiles.append("precise but lifeless")
    if coherence_score >= 0.32 and evidence_density < 0.09:
        profiles.append("internally stable, externally ungrounded")
    if truth_score >= 0.42 and coherence_score < 0.26:
        profiles.append("deep but poorly sequenced")
    if coherence_score >= 0.30 and evidence_density < 0.08 and falsifiability_density < 0.03 and truth_score < 0.42:
        profiles.append("structured but semantically hollow")
    if hedge_density >= 0.08 and falsifiability_density >= 0.04 and evidence_density >= 0.10 and contradiction_rate < 0.08:
        profiles.append("honest uncertainty, strong method")
    if absolute_pressure >= 0.12 and evidence_density < 0.09 and falsifiability_density < 0.03:
        profiles.append("inflated certainty, weak method")
    if evidence_density >= 0.18 and coherence_score < 0.26:
        profiles.append("rich evidence, weak synthesis")
    if coherence_score >= 0.34 and evidence_density < 0.10:
        profiles.append("strong synthesis, weak sourcing")
    if warmth_score >= 0.12 and rhetorical_force < 0.12 and evidence_density < 0.10:
        profiles.append("morally serious, technically thin")
    if truth_score >= 0.46 and coherence_score >= 0.30 and warmth_score < 0.08:
        profiles.append("technically strong, morally vacant")
    if coherence_score >= 0.34 and contradiction_rate < 0.06 and hedge_density < 0.10 and falsifiability_density >= 0.04:
        profiles.append("coherent under pressure")
    if coherence_score < 0.24 and contradiction_rate >= 0.08 and falsifiability_density < 0.03:
        profiles.append("fragile under scrutiny")
    if rhetorical_force >= 0.14 and evidence_density < 0.08 and coherence_score < 0.26:
        profiles.append("broad but shallow")
    if truth_score >= 0.46 and coherence_score >= 0.30 and evidence_density >= 0.10 and rhetorical_force < 0.16:
        profiles.append("narrow but rigorous")
    if falsifiability_density >= 0.04 and truth_score >= 0.42 and contradiction_rate < 0.08:
        profiles.append("dependency-aware and accountable")
    if rhetorical_force >= 0.14 and falsifiability_density < 0.03 and truth_score < 0.44:
        profiles.append("dependency-blind and overextended")
    if truth_score >= 0.40 and evidence_density < 0.09 and falsifiability_density < 0.03:
        profiles.append("conceptually fertile but under-tested")
    if rhetorical_force >= 0.14 and contradiction_rate >= 0.08 and coherence_score < 0.28:
        profiles.append("rhetorically persuasive but structurally unstable")
    if truth_score >= 0.42 and coherence_score >= 0.28 and falsifiability_density < 0.03:
        profiles.append("publication-ready but adversarially incomplete")

    if not profiles:
        if truth_score >= coherence_score + 0.10:
            profiles.append("truth-seeking but rough")
        elif coherence_score >= truth_score + 0.10:
            profiles.append("strong synthesis, weak sourcing")
        else:
            profiles.append("mixed integrity profile")

    return profiles[:5]


def analyze_document(source: str, text: str, source_type: str) -> tuple[DocumentRecord, list[SentenceScore], list[ClaimRecord]]:
    clean = normalize_whitespace(text)
    sections = split_sections(text)
    all_sentence_scores: list[SentenceScore] = []
    section_coherence_scores: list[float] = []

    # Doc-level NER pass (single spaCy parse). See ISSUE-001 in KNOWN_ISSUES.md.
    doc_entities = _doc_entity_strings(clean)

    contradiction_flags = 0
    evidence_sentences = 0
    falsify_sentences = 0
    hedge_sentences = 0
    absolute_pressure_scores: list[float] = []
    claim_strength_scores: list[float] = []
    section_count = 0
    paragraph_total = 0
    sentence_to_para: dict[int, int] = {}  # global sentence idx → global paragraph idx
    _global_para_idx = 0

    for heading, section_text in sections:
        paragraphs = split_paragraphs(section_text)
        paragraph_total += len(paragraphs)
        section_count += 1

        local_sentences = split_sentences(section_text)
        local_scores: list[SentenceScore] = []
        for idx, sentence in enumerate(local_sentences):
            ner_a = _ner_anchor_for_sentence(sentence, doc_entities)
            score = sentence_truth(sentence, ner_anchor=ner_a)
            score.index = len(all_sentence_scores) + idx
            local_scores.append(score)
            if score.evidence_anchor >= 0.4:
                evidence_sentences += 1
            if score.falsifiability_signal >= 0.4:
                falsify_sentences += 1
            if score.hedge_pressure >= 0.25:
                hedge_sentences += 1
            if score.contradiction_pressure >= 0.5:
                contradiction_flags += 1
            absolute_pressure_scores.append(score.absolute_pressure)
            claim_strength_scores.append(score.claim_strength)

        # Map each sentence to its containing paragraph (global indices)
        for sc in local_scores:
            best_para = _global_para_idx  # default: first paragraph of this section
            for pi, para in enumerate(paragraphs):
                if sc.text[:40] in para:
                    best_para = _global_para_idx + pi
                    break
            sentence_to_para[sc.index] = best_para
        _global_para_idx += len(paragraphs)

        all_sentence_scores.extend(local_scores)

        if paragraphs:
            lexical_links = []
            for i in range(len(paragraphs) - 1):
                lexical_links.append(term_overlap(paragraphs[i], paragraphs[i + 1]))
            lexical_cohesion = sum(lexical_links) / len(lexical_links) if lexical_links else 0.5
            bridge_signal = 1.0 if any(contains_phrase(p, BRIDGE_TERMS) for p in paragraphs) else 0.0
            heading_alignment = heading_alignment_score(heading, paragraphs)
            jump_pressure = 1.0 - lexical_cohesion if lexical_cohesion < 0.15 else 0.0
            section_coherence = clamp(0.45 * lexical_cohesion + 0.30 * heading_alignment + 0.15 * bridge_signal + 0.10 * (1.0 - jump_pressure))
            section_coherence_scores.append(section_coherence)

    sentence_count = len(all_sentence_scores)
    truth_score = sum(s.truth_score for s in all_sentence_scores) / sentence_count if sentence_count else 0.0
    coherence_score = sum(section_coherence_scores) / len(section_coherence_scores) if section_coherence_scores else 0.0
    combined_score = clamp(0.58 * truth_score + 0.42 * coherence_score)

    evidence_density = evidence_sentences / sentence_count if sentence_count else 0.0
    falsifiability_density = falsify_sentences / sentence_count if sentence_count else 0.0
    hedge_density = hedge_sentences / sentence_count if sentence_count else 0.0
    contradiction_rate = contradiction_flags / sentence_count if sentence_count else 0.0
    absolute_pressure = average(absolute_pressure_scores)
    rhetorical_force = average(claim_strength_scores)
    fruit_vector = fruits_vector(clean)
    anti_vector = anti_fruits_vector(clean)
    warmth_score = average([fruit_vector["love"], fruit_vector["peace"], fruit_vector["kindness"], fruit_vector["gentleness"]])
    discipline_score = average([fruit_vector["faithfulness"], fruit_vector["self_control"], fruit_vector["patience"]])
    character_posture, fruit_integrity_score, anti_fruit_pressure = derive_character_posture(
        fruit_vector=fruit_vector,
        anti_vector=anti_vector,
        truth_score=truth_score,
        coherence_score=coherence_score,
    )
    character_attributes, character_profile = analyze_character_attributes(clean)
    if character_profile["threat_score"] > character_profile["protection_score"] + 0.2:
        character_posture = sorted(set(character_posture + ["underlying threat structure"]))
    if character_profile["protection_score"] > character_profile["threat_score"] + 0.2:
        character_posture = sorted(set(character_posture + ["protective character structure"]))
    integrity_profiles = derive_integrity_profiles(
        truth_score=truth_score,
        coherence_score=coherence_score,
        evidence_density=evidence_density,
        falsifiability_density=falsifiability_density,
        hedge_density=hedge_density,
        contradiction_rate=contradiction_rate,
        absolute_pressure=absolute_pressure,
        rhetorical_force=rhetorical_force,
        warmth_score=warmth_score,
        discipline_score=discipline_score,
    )

    ranked = sorted(all_sentence_scores, key=lambda s: s.truth_score, reverse=True)
    top_supported = [s.text for s in ranked[:5]]
    top_risky = [s.text for s in sorted(all_sentence_scores, key=lambda s: (s.truth_score, -s.contradiction_pressure))[:5]]
    claim_records = extract_claim_records(source, all_sentence_scores, sentence_to_para)
    claim_status_counts: dict[str, int] = {}
    for claim in claim_records:
        claim_status_counts[claim.claim_status] = claim_status_counts.get(claim.claim_status, 0) + 1

    title = source
    if source_type == "file":
        title = Path(source).stem
    elif source_type == "url":
        title = source

    record = DocumentRecord(
        source=source,
        source_type=source_type,
        title=title,
        sentence_count=sentence_count,
        paragraph_count=paragraph_total,
        section_count=section_count,
        truth_score=round(truth_score, 4),
        coherence_score=round(coherence_score, 4),
        combined_score=round(combined_score, 4),
        evidence_density=round(evidence_density, 4),
        falsifiability_density=round(falsifiability_density, 4),
        hedge_density=round(hedge_density, 4),
        contradiction_flags=contradiction_flags,
        absolute_pressure=round(absolute_pressure, 4),
        rhetorical_force=round(rhetorical_force, 4),
        warmth_score=round(warmth_score, 4),
        discipline_score=round(discipline_score, 4),
        fruit_integrity_score=fruit_integrity_score,
        anti_fruit_pressure=anti_fruit_pressure,
        claim_count=len(claim_records),
        anchored_claims=claim_status_counts.get("anchored", 0),
        under_supported_claims=claim_status_counts.get("under-supported", 0),
        overstated_claims=claim_status_counts.get("overstated", 0),
        speculative_claims=claim_status_counts.get("speculative", 0),
        contradictory_claims=claim_status_counts.get("contradictory", 0),
        falsifiable_claims=sum(1 for claim in claim_records if claim.falsifiability_present),
        integrity_profiles=integrity_profiles,
        fruits_vector=fruit_vector,
        anti_fruits_vector=anti_vector,
        character_attributes=character_attributes,
        character_profile=character_profile,
        character_posture=character_posture,
        top_supported_sentences=top_supported,
        top_risky_sentences=top_risky,
    )
    return record, all_sentence_scores, claim_records


def collect_local_targets(target: str) -> list[Path]:
    path = Path(target)
    if path.is_file():
        return [path]
    if path.is_dir():
        files: list[Path] = []
        for p in path.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".md", ".txt", ".html", ".htm"}:
                continue
            if p.name in EXCLUDED_FILE_NAMES:
                continue
            if any(pattern.search(p.name) for pattern in EXCLUDED_FILE_PATTERNS):
                continue
            if any(part in EXCLUDED_DIR_NAMES for part in p.parts):
                continue
            files.append(p)
        return sorted(files)
    return []


def write_outputs(
    records: list[DocumentRecord],
    output_dir: Path,
    sentence_map: dict[str, list[SentenceScore]],
    claim_map: dict[str, list[ClaimRecord]],
    label: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    records_json = output_dir / "truth_coherence_records.json"
    records_csv = output_dir / "truth_coherence_records.csv"
    summary_md = output_dir / "truth_coherence_summary.md"
    sentence_json = output_dir / "truth_sentence_flags.json"
    claims_json = output_dir / "truth_claim_records.json"
    claims_csv = output_dir / "truth_claim_records.csv"

    records_json.write_text(json.dumps([asdict(r) for r in records], indent=2), encoding="utf-8")
    sentence_payload = {key: [asdict(item) for item in value] for key, value in sentence_map.items()}
    sentence_json.write_text(json.dumps(sentence_payload, indent=2), encoding="utf-8")
    claims_payload = {key: [asdict(item) for item in value] for key, value in claim_map.items()}
    claims_json.write_text(json.dumps(claims_payload, indent=2), encoding="utf-8")

    with records_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(records[0]).keys()) if records else [])
        if records:
            writer.writeheader()
        for record in records:
            row = asdict(record)
            row["fruits_vector"] = json.dumps(row["fruits_vector"], ensure_ascii=True)
            row["anti_fruits_vector"] = json.dumps(row["anti_fruits_vector"], ensure_ascii=True)
            row["character_attributes"] = json.dumps(row["character_attributes"], ensure_ascii=True)
            row["character_profile"] = json.dumps(row["character_profile"], ensure_ascii=True)
            row["integrity_profiles"] = " | ".join(row["integrity_profiles"])
            row["character_posture"] = " | ".join(row["character_posture"])
            row["top_supported_sentences"] = " | ".join(row["top_supported_sentences"])
            row["top_risky_sentences"] = " | ".join(row["top_risky_sentences"])
            writer.writerow(row)

    flat_claims = [claim for claims in claim_map.values() for claim in claims]
    with claims_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(flat_claims[0]).keys()) if flat_claims else [])
        if flat_claims:
            writer.writeheader()
            for claim in flat_claims:
                writer.writerow(asdict(claim))

    avg_truth = sum(r.truth_score for r in records) / len(records) if records else 0.0
    avg_coherence = sum(r.coherence_score for r in records) / len(records) if records else 0.0
    avg_combined = sum(r.combined_score for r in records) / len(records) if records else 0.0
    total_claims = sum(r.claim_count for r in records)
    total_anchored = sum(r.anchored_claims for r in records)
    total_under_supported = sum(r.under_supported_claims for r in records)
    total_overstated = sum(r.overstated_claims for r in records)
    total_speculative = sum(r.speculative_claims for r in records)
    total_contradictory = sum(r.contradictory_claims for r in records)
    total_falsifiable = sum(r.falsifiable_claims for r in records)
    avg_fruit_integrity = sum(r.fruit_integrity_score for r in records) / len(records) if records else 0.0
    avg_anti_fruit = sum(r.anti_fruit_pressure for r in records) / len(records) if records else 0.0
    avg_threat_structure = sum(float(r.character_profile.get("threat_score", 0.0)) for r in records) / len(records) if records else 0.0
    avg_protection_structure = sum(float(r.character_profile.get("protection_score", 0.0)) for r in records) / len(records) if records else 0.0
    worst = sorted(records, key=lambda r: r.combined_score)[:10]
    best = sorted(records, key=lambda r: r.combined_score, reverse=True)[:10]

    lines = [
        "# Truth / Coherence Summary",
        "",
        f"- Target: `{label}`",
        f"- Generated: `{datetime.now().isoformat(timespec='seconds')}`",
        f"- Documents scanned: `{len(records)}`",
        f"- Claims isolated: `{total_claims}`",
        f"- Anchored claims: `{total_anchored}`",
        f"- Under-supported claims: `{total_under_supported}`",
        f"- Overstated claims: `{total_overstated}`",
        f"- Speculative claims: `{total_speculative}`",
        f"- Contradictory claims: `{total_contradictory}`",
        f"- Falsifiable claims: `{total_falsifiable}`",
        f"- Average truth score: `{avg_truth:.4f}`",
        f"- Average coherence score: `{avg_coherence:.4f}`",
        f"- Average combined score: `{avg_combined:.4f}`",
        f"- Average fruit integrity score: `{avg_fruit_integrity:.4f}`",
        f"- Average anti-fruit pressure: `{avg_anti_fruit:.4f}`",
        f"- Average character threat score: `{avg_threat_structure:.4f}`",
        f"- Average character protection score: `{avg_protection_structure:.4f}`",
        "",
        "## Claim Status Totals",
        f"- `anchored`: {total_anchored}",
        f"- `under-supported`: {total_under_supported}",
        f"- `overstated`: {total_overstated}",
        f"- `speculative`: {total_speculative}",
        f"- `contradictory`: {total_contradictory}",
        f"- `falsifiable`: {total_falsifiable}",
        "",
        "## Most Common Integrity Profiles",
    ]
    profile_counts: dict[str, int] = {}
    for record in records:
        for profile in record.integrity_profiles:
            profile_counts[profile] = profile_counts.get(profile, 0) + 1
    for profile, count in sorted(profile_counts.items(), key=lambda item: (-item[1], item[0]))[:12]:
        lines.append(f"- `{profile}`: {count}")
    lines.extend([
        "",
        "## Most Common Character Postures",
    ])
    posture_counts: dict[str, int] = {}
    for record in records:
        for posture in record.character_posture:
            posture_counts[posture] = posture_counts.get(posture, 0) + 1
    for posture, count in sorted(posture_counts.items(), key=lambda item: (-item[1], item[0]))[:12]:
        lines.append(f"- `{posture}`: {count}")
    lines.extend([
        "",
        "## Highest Anchored Claim Density",
    ])
    anchored_rank = sorted(records, key=lambda r: (r.anchored_claims / r.claim_count) if r.claim_count else 0.0, reverse=True)[:10]
    for record in anchored_rank:
        density = (record.anchored_claims / record.claim_count) if record.claim_count else 0.0
        lines.append(f"- `{density:.4f}` `{record.source}`")
    lines.extend([
        "",
        "## Highest Under-Supported Claim Density",
    ])
    under_supported_rank = sorted(records, key=lambda r: (r.under_supported_claims / r.claim_count) if r.claim_count else 0.0, reverse=True)[:10]
    for record in under_supported_rank:
        density = (record.under_supported_claims / record.claim_count) if record.claim_count else 0.0
        lines.append(f"- `{density:.4f}` `{record.source}`")
    lines.extend([
        "",
        "## Highest Combined Scores",
    ])
    for record in best:
        lines.append(f"- `{record.combined_score:.4f}` `{record.source}`")
    lines.extend(["", "## Lowest Combined Scores"])
    for record in worst:
        lines.append(f"- `{record.combined_score:.4f}` `{record.source}`")
    lines.extend([
        "",
        "## Output Files",
        "- `truth_coherence_records.json`",
        "- `truth_coherence_records.csv`",
        "- `truth_coherence_summary.md`",
        "- `truth_sentence_flags.json`",
        "- `truth_claim_records.json`",
        "- `truth_claim_records.csv`",
    ])
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan documents and web pages for truth/coherence features")
    parser.add_argument("target", nargs="?", default="", help="Local file or folder target")
    parser.add_argument("--url", action="append", default=[], help="Web page URL to scan; can be repeated")
    parser.add_argument("--output-dir", default="", help="Output directory")
    args = parser.parse_args()

    local_files = collect_local_targets(args.target) if args.target else []
    if not local_files and not args.url:
        raise SystemExit("Provide a file/folder target and/or one or more --url values.")

    records: list[DocumentRecord] = []
    sentence_map: dict[str, list[SentenceScore]] = {}
    claim_map: dict[str, list[ClaimRecord]] = {}

    for path in local_files:
        text = read_text_from_path(path)
        record, scores, claims = analyze_document(str(path), text, "file")
        records.append(record)
        sentence_map[str(path)] = scores
        claim_map[str(path)] = claims

    for url in args.url:
        try:
            text = fetch_url_text(url)
        except URLError as exc:
            print(f"Failed to fetch {url}: {exc}")
            continue
        record, scores, claims = analyze_document(url, text, "url")
        records.append(record)
        sentence_map[url] = scores
        claim_map[url] = claims

    if not records:
        raise SystemExit("No documents could be analyzed.")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    label = args.target or ",".join(args.url[:3])
    output_dir = Path(args.output_dir) if args.output_dir else Path.cwd() / f"truth_coherence_scan_{stamp}"
    write_outputs(records, output_dir, sentence_map, claim_map, label)

    print(f"Documents analyzed: {len(records)}")
    print(f"Output directory: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
