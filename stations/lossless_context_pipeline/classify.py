from __future__ import annotations

import re
import sys
from pathlib import Path

from .schemas import DomainBadge

SHARED = Path(__file__).resolve().parents[1] / "_shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))
from canonical_lexicon import semantic_terms, sheet_terms  # noqa: E402


EQUATION_RE = re.compile(r"(\$\$.*?\$\$|\$[^$\n]+\$|\\\(|\\\[|[A-Za-z_]\w*\s*=\s*[^,\n;]+)", re.DOTALL)
CITATION_RE = re.compile(r"(\[[^\]]+\]\([^)]+\)|\[[0-9,\s]+\]|\bdoi:\S+|\barXiv:\S+)", re.IGNORECASE)
KILL_RE = re.compile(r"\b(falsif|kill condition|would fail|fails if|testable|prediction|counterexample|downgrade|refute)\b", re.IGNORECASE)
DEFINITION_RE = re.compile(r"\b(is defined as|means|definition|where\s+[A-Za-z_]\w*\s*=|:=)\b", re.IGNORECASE)
CLAIM_RE = re.compile(r"\b(claims?|argues?|therefore|because|requires|implies|proves?|shows?|demonstrates?|predicts?)\b", re.IGNORECASE)
DOMAIN_SHIFT_RE = re.compile(r"\b(physics|theology|spiritual|formal|mathematical|empirical|metaphysical|information|scripture|grace|sin|coherence|entropy)\b", re.IGNORECASE)

HIGH_RISK_WORDS = sorted(
    semantic_terms(danger_levels={"high", "critical"})
    | sheet_terms("ABSOLUTE_TERMS")
    | {"proves", "mathematically proven", "undeniable", "impossible", "refuted", "destroyed", "only", "definitive", "settled"}
)
MEDIUM_RISK_WORDS = sorted(
    semantic_terms(danger_levels={"medium"})
    | sheet_terms("HEDGE_TERMS")
    | {"suggests", "demonstrates", "confirms", "clearly", "unique", "necessary", "must"}
)

DOMAIN_KEYWORDS: dict[DomainBadge, list[str]] = {
    "PHYSICS": ["physics", "force", "field", "entropy", "energy", "quantum", "relativity", "thermodynamics"],
    "THEOLOGY": ["theology", "god", "christ", "jesus", "grace", "sin", "scripture", "atonement"],
    "FORMAL": ["proof", "theorem", "axiom", "equation", "formal", "derive", "logic"],
    "EMPIRICAL": sorted(sheet_terms("EVIDENCE_TERMS") | {"data", "test", "measured", "sigma", "experiment", "correlation", "evidence"}),
    "ANALOGY": ["like", "as if", "analogy", "metaphor", "resembles"],
    "METAPHYSICS": ["being", "substrate", "ultimate", "ontological", "metaphysical"],
    "INFORMATION": ["information", "signal", "noise", "channel", "shannon", "meaning"],
    "PUBLIC_COMM": ["reader", "public", "article", "communication", "audience"],
    "LEGAL": ["legal", "liability", "contract", "law"],
    "TECH": ["workflow", "pipeline", "database", "vector", "postgres", "cloudflare", "api"],
}


def classify_block(text: str) -> str:
    if EQUATION_RE.search(text):
        return "EQUATION"
    if KILL_RE.search(text):
        return "KILL_CONDITION"
    if DEFINITION_RE.search(text):
        return "DEFINITION"
    if CITATION_RE.search(text):
        return "EVIDENCE"
    badges = domain_badges(text)
    if len(badges) >= 2:
        return "DOMAIN_SHIFT"
    if CLAIM_RE.search(text):
        return "CLAIM"
    return "OTHER"


def domain_badges(text: str) -> list[DomainBadge]:
    low = text.lower()
    badges: list[DomainBadge] = []
    for badge, words in DOMAIN_KEYWORDS.items():
        if any(word in low for word in words):
            badges.append(badge)
    return badges or ["UNKNOWN"]


def overstatement_words(text: str) -> list[str]:
    low = text.lower()
    return [word for word in HIGH_RISK_WORDS + MEDIUM_RISK_WORDS if word in low]


def citations(text: str) -> list[str]:
    return [match.group(0) for match in CITATION_RE.finditer(text)]


def equations(text: str) -> list[str]:
    return [match.group(0).strip("$ \n") for match in EQUATION_RE.finditer(text)]
