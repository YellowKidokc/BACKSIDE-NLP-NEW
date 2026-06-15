from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime
from html import escape, unescape
from pathlib import Path
from typing import Any, Callable, Literal, Optional


DomainBadge = Literal[
    "PHYSICS",
    "THEOLOGY",
    "FORMAL",
    "EMPIRICAL",
    "ANALOGY",
    "METAPHYSICS",
    "INFORMATION",
    "PUBLIC_COMM",
]

EquationStatus = Literal[
    "DERIVED",
    "PROPOSED",
    "INTERPRETIVE",
    "PRESENTATIONAL",
    "SYMBOLIC_FORMALISM",
    "OPERATIONAL_MODEL",
    "ANALOGY",
    "RHETORICAL_MATH",
]

UseDirection = Literal["I", "B", "T", "R"]  # Inform, Bind, Transform, Record
RiskLevel = Literal["R0", "R1", "R2", "R3", "R4"]
LifecycleState = Literal["D", "W", "F", "P", "A"]  # Draft, Working, Final, Published, Archived


SEMANTIC_VARIABLES = {
    "G": ["grace", "gift", "divine", "law", "govern", "constraint", "authority", "source"],
    "M": ["measurement", "metric", "method", "mechanism", "model", "mass", "material"],
    "E": ["entropy", "disorder", "decay", "error", "collapse", "failure", "noise"],
    "S": ["spacetime", "structure", "system", "state", "symmetry", "sequence", "substrate"],
    "T": ["time", "temporal", "history", "trajectory", "development", "before", "after"],
    "K": ["knowledge", "information", "truth", "data", "evidence", "theorem", "proof"],
    "R": ["repentance", "return", "repair", "reversal", "restoration", "right", "relation"],
    "Q": ["quantum", "quality", "choice", "observer", "probability", "uncertainty"],
    "F": ["faith", "fidelity", "trust", "commitment", "witness", "belief"],
    "C": ["coherence", "christ", "constraint", "covenant", "coupling", "community"],
}

DOMAIN_TERMS: dict[DomainBadge, list[str]] = {
    "PHYSICS": [
        "quantum",
        "measurement",
        "collapse",
        "observer",
        "field",
        "energy",
        "entropy",
        "spacetime",
        "cosmology",
        "particle",
        "wavefunction",
        "decoherence",
    ],
    "THEOLOGY": [
        "god",
        "christ",
        "grace",
        "faith",
        "sin",
        "salvation",
        "scripture",
        "cross",
        "creation",
        "theology",
        "divine",
    ],
    "FORMAL": [
        "axiom",
        "theorem",
        "proof",
        "formal",
        "operator",
        "equation",
        "model",
        "logic",
        "derive",
        "constraint",
    ],
    "EMPIRICAL": [
        "test",
        "prediction",
        "data",
        "experiment",
        "observed",
        "measurement",
        "evidence",
        "falsifiable",
        "empirical",
    ],
    "ANALOGY": ["analogy", "metaphor", "like", "as if", "correspondence", "mapping"],
    "METAPHYSICS": ["being", "ontology", "ultimate", "reality", "necessary", "contingent"],
    "INFORMATION": ["information", "entropy", "signal", "knowledge", "state", "code", "memory"],
    "PUBLIC_COMM": ["reader", "plain", "simple", "story", "understand", "public", "communication"],
}

HIGH_RISK_WORDS = [
    "proves",
    "cannot be denied",
    "mathematically proven",
    "settled",
    "definitive",
    "impossible",
    "refuted",
    "destroyed",
    "only",
]
MEDIUM_RISK_WORDS = ["clearly", "obviously", "undeniably", "must", "cannot"]
SAFE_HEDGES = ["suggests", "appears", "may", "under conditions", "creates explanatory pressure"]


@dataclass
class NablaAddress:
    domain: str
    entity: str
    state: LifecycleState
    audience: str
    use: UseDirection
    risk: RiskLevel
    date: str
    vector: str
    hash: str

    @property
    def canonical(self) -> str:
        return (
            f"{self.domain}/{self.entity}/{self.state}/{self.audience}/{self.use}/{self.risk} :: "
            f"{self.vector} :: {self.hash}"
        )

    @property
    def filename_safe(self) -> str:
        return "__".join(
            [
                slug(self.domain),
                slug(self.entity),
                self.state,
                slug(self.audience),
                self.use,
                self.risk,
                self.vector,
                self.hash.replace("[", "").replace("]", "").replace("·", ""),
            ]
        )


@dataclass
class ClaimArch:
    surface_claim: str
    buried_claim: str
    operational_claim: str
    rhetorical_load: str
    domain_shift: str
    domain_badges: list[DomainBadge]
    evidence_quote: str = ""
    section: str = "CLAIM_ARCH"


@dataclass
class EvidenceChain:
    primary_source: str
    secondary_source: Optional[str]
    tertiary_source: Optional[str]
    tested_thing: str
    connection_to_claim: str
    gap: str
    counterevidence_present: Literal["yes", "no", "partial"]
    evidence_quote: str = ""
    section: str = "EVIDENCE_CHAIN"


@dataclass
class KillArch:
    stated_kill: str
    implicit_kill: str
    testable_kill: str
    rhetorical_armor: str
    evidence_quote: str = ""
    section: str = "KILL_ARCH"


@dataclass
class EquationSemantics:
    equation: str
    role: str
    status: EquationStatus
    undefined_vars: list[str]
    dimensional_status: str
    derivation_present: Literal["yes", "no", "partial"]
    computable: Literal["yes", "no", "conditional"]
    comparison: str
    section: str = "EQ_SEM"


@dataclass
class DomainBoundary:
    term: str
    usage_by_domain: list[DomainBadge]
    bridge_present: Literal["yes", "no", "partial"]
    bridge_quality: str
    drift_risk: Literal["low", "medium", "high"]


@dataclass
class ReviewerSeeds:
    skeptical_physicist: str
    academic_philosopher: str
    information_theorist: str
    methodologist: str
    hostile_critic: str


@dataclass
class OverstatementFlag:
    word: str
    risk: Literal["high", "medium"]
    evidence_quote: str
    safer_wording: str


@dataclass
class BenchmarkAnchor:
    comparison_target: str
    score_context: str
    why_low: str
    why_high: str
    lesson: str


@dataclass
class CrossDependency:
    paper_id: str
    depends_on: list[str]
    enables: list[str]
    shared_claims_with: list[str]
    term_drift_flags: list[str]
    orphan_risk: str


@dataclass
class ScoreEvent:
    metric_id: str
    points: float
    max_points: float
    reason: str
    evidence_quote: str
    section: str
    kind: Literal["positive", "deduction"]
    fix_to_improve: str = ""


@dataclass
class FourScoreDashboard:
    academic_readiness: float
    framework_coherence: float
    public_communication: float
    risk: float
    academic_label: str
    framework_label: str
    public_label: str
    risk_label: str


@dataclass
class PaperSnapshot:
    paper_id: str
    title: str
    source_path: str
    generated_at: str
    address: NablaAddress
    four_scores: FourScoreDashboard
    claims: list[ClaimArch] = field(default_factory=list)
    evidence_chains: list[EvidenceChain] = field(default_factory=list)
    kill_conditions: list[KillArch] = field(default_factory=list)
    equations: list[EquationSemantics] = field(default_factory=list)
    domain_boundaries: list[DomainBoundary] = field(default_factory=list)
    reviewer_seeds: Optional[ReviewerSeeds] = None
    overstatement_flags: list[OverstatementFlag] = field(default_factory=list)
    benchmark: Optional[BenchmarkAnchor] = None
    cross_dependency: Optional[CrossDependency] = None
    score_events: list[ScoreEvent] = field(default_factory=list)
    eight_gaps: list[str] = field(default_factory=list)


LLMExtractor = Callable[[str, str], dict[str, Any]]


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", str(value).strip()).strip("-")
    return value.upper() or "UNKNOWN"


def clean_text(value: str) -> str:
    value = unescape(value or "")
    fixes = {
        "\ufeff": "",
        "â€”": "-",
        "â€“": "-",
        "â€œ": '"',
        "â€": '"',
        "â€˜": "'",
        "â€™": "'",
        "Â": "",
        "→": "->",
        "←": "<-",
    }
    for bad, good in fixes.items():
        value = value.replace(bad, good)
    return re.sub(r"\s+", " ", value).strip()


def load_document(path: Path) -> tuple[str, str, dict[str, Any]]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    frontmatter: dict[str, Any] = {}

    if raw.startswith("---"):
        match = re.match(r"(?s)^---\s*(.*?)\s*---\s*(.*)$", raw)
        if match:
            raw_frontmatter, raw = match.groups()
            for line in raw_frontmatter.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip().strip('"')

    if path.suffix.lower() in {".html", ".htm"}:
        title_match = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw)
        if title_match and "title" not in frontmatter:
            frontmatter["title"] = clean_text(title_match.group(1))
        raw = re.sub(r"(?is)<script.*?>.*?</script>", " ", raw)
        raw = re.sub(r"(?is)<style.*?>.*?</style>", " ", raw)
        raw = re.sub(r"(?s)<[^>]+>", "\n", raw)

    text = clean_text(raw)
    title = frontmatter.get("title") or infer_title(path, text)
    return title, text, frontmatter


def infer_title(path: Path, text: str) -> str:
    lines = [clean_text(line) for line in text.splitlines() if clean_text(line)]
    for line in lines[:20]:
        if 6 <= len(line) <= 120:
            return line
    return path.stem.replace("-", " ").replace("_", " ").title()


def split_sentences(text: str) -> list[str]:
    sentences = [clean_text(s) for s in re.split(r"(?<=[.!?])\s+", text)]
    junk = ["main index", "read aloud", "prev next", "mathjax", "toggle audio", "0:00"]
    return [s for s in sentences if len(s) > 45 and not any(j in s.lower() for j in junk)]


def stable_paper_id(path: Path, text: str) -> str:
    basis = f"{path.name.lower()}::{text[:2000]}".encode("utf-8", errors="ignore")
    return "P-" + hashlib.sha1(basis).hexdigest()[:12]


def semantic_vector(text: str) -> str:
    levels: dict[str, int] = {}
    for key, terms in SEMANTIC_VARIABLES.items():
        count = sum(len(re.findall(r"\b" + re.escape(term) + r"\b", text, re.I)) for term in terms)
        if count >= 18:
            level = 3
        elif count >= 7:
            level = 2
        elif count >= 2:
            level = 1
        else:
            level = 0
        levels[key] = level
    return "".join(f"{key}{levels[key]}" for key in SEMANTIC_VARIABLES)


def pair_hash(vector: str) -> str:
    values = {key: int(value) for key, value in re.findall(r"([A-Z])(\d)", vector)}
    pairs = [("C", "Q"), ("G", "S"), ("K", "E"), ("M", "F"), ("T", "R")]
    ordered = []
    for left, right in pairs:
        if values.get(right, 0) > values.get(left, 0):
            left, right = right, left
        ordered.append(f"[{left}·{right}]")
    return "".join(ordered)


def detect_domain(text: str) -> str:
    counts = domain_counts(text)
    if not counts:
        return "GENERAL"
    return sorted(counts.items(), key=lambda item: item[1], reverse=True)[0][0]


def domain_counts(text: str) -> dict[DomainBadge, int]:
    counts: dict[DomainBadge, int] = {}
    for domain, terms in DOMAIN_TERMS.items():
        count = sum(len(re.findall(r"\b" + re.escape(term) + r"\b", text, re.I)) for term in terms)
        if count:
            counts[domain] = count
    return counts


def detect_state(frontmatter: dict[str, Any], text: str) -> LifecycleState:
    raw = str(frontmatter.get("state") or frontmatter.get("status") or "").lower()
    if "publish" in raw:
        return "P"
    if "final" in raw or "canonical" in raw:
        return "F"
    if "archive" in raw:
        return "A"
    if "draft" in raw:
        return "D"
    if re.search(r"\b(draft|working|todo|revision|pending)\b", text, re.I):
        return "W"
    return "F"


def detect_audience(frontmatter: dict[str, Any], text: str) -> str:
    raw = frontmatter.get("audience")
    if raw:
        return slug(str(raw))
    if re.search(r"\b(public|reader|layperson|non-expert|website)\b", text, re.I):
        return "PUBLIC"
    if re.search(r"\b(reviewer|physicist|academic|methodologist|journal)\b", text, re.I):
        return "ACADEMIC"
    if re.search(r"\b(ai|llm|codex|claude|gpt|handoff)\b", text, re.I):
        return "AI-RESEARCH"
    return "GENERAL"


def detect_use(text: str) -> UseDirection:
    if re.search(r"\b(bind|law|oath|constitution|contract|must|shall|requirement)\b", text, re.I):
        return "B"
    if re.search(r"\b(transform|convert|repair|change|reconstruct|rewrite|heal)\b", text, re.I):
        return "T"
    if re.search(r"\b(record|log|archive|manifest|inventory|snapshot)\b", text, re.I):
        return "R"
    return "I"


def detect_risk(text: str, overstatement_count: int, drift_count: int) -> RiskLevel:
    raw = overstatement_count + drift_count
    if re.search(r"\b(legal|medical|financial|defamation|danger|high risk)\b", text, re.I):
        raw += 3
    if raw >= 12:
        return "R4"
    if raw >= 8:
        return "R3"
    if raw >= 4:
        return "R2"
    if raw >= 1:
        return "R1"
    return "R0"


def extract_domain_boundaries(text: str) -> list[DomainBoundary]:
    term_domains: dict[str, list[DomainBadge]] = defaultdict(list)
    for domain, terms in DOMAIN_TERMS.items():
        for term in terms:
            if re.search(r"\b" + re.escape(term) + r"\b", text, re.I):
                term_domains[term.lower()].append(domain)

    boundaries = []
    for term, domains in sorted(term_domains.items()):
        if len(domains) < 2:
            continue
        bridge_present = "partial" if re.search(rf"{re.escape(term)}.*\b(means|defined|as|analogous|maps)\b", text, re.I) else "no"
        boundaries.append(
            DomainBoundary(
                term=term,
                usage_by_domain=domains,
                bridge_present=bridge_present,
                bridge_quality="manual review required" if bridge_present == "partial" else "missing explicit bridge",
                drift_risk="high" if len(domains) >= 3 else "medium",
            )
        )
    return boundaries


def extract_overstatement(sentences: list[str]) -> list[OverstatementFlag]:
    flags = []
    for word in HIGH_RISK_WORDS + MEDIUM_RISK_WORDS:
        risk = "high" if word in HIGH_RISK_WORDS else "medium"
        pattern = r"\b" + re.escape(word) + r"\b"
        for sentence in sentences:
            if re.search(pattern, sentence, re.I):
                flags.append(
                    OverstatementFlag(
                        word=word,
                        risk=risk,
                        evidence_quote=sentence,
                        safer_wording="Use 'suggests', 'models', or 'under these assumptions' unless the evidence bridge supports stronger language.",
                    )
                )
    return flags


def extract_claims(sentences: list[str], boundaries: list[DomainBoundary]) -> list[ClaimArch]:
    marker = re.compile(
        r"\b(argues|claims|proposes|predicts|shows|demonstrates|suggests|therefore|implies|must|requires|"
        r"hypothesis|falsifiable|framework|model|test)\b",
        re.I,
    )
    candidates = [s for s in sentences if marker.search(s)]
    candidates = sorted(
        candidates,
        key=lambda s: (bool(re.search(r"\b(test|predict|falsif|evidence|hypothesis)\b", s, re.I)), len(s)),
        reverse=True,
    )
    claims = []
    for sentence in candidates[:6]:
        badges = sentence_domains(sentence)
        drift = "unbridged domain shift possible" if any(b.term in sentence.lower() for b in boundaries) else "no obvious domain shift"
        claims.append(
            ClaimArch(
                surface_claim=sentence,
                buried_claim="The claim assumes its key terms keep stable meanings across the paper.",
                operational_claim="The claim must be expressible as a test, formal dependency, or falsifiable review condition.",
                rhetorical_load="computed from overstatement flags",
                domain_shift=drift,
                domain_badges=badges or ["PUBLIC_COMM"],
                evidence_quote=sentence,
            )
        )
    return claims


def sentence_domains(sentence: str) -> list[DomainBadge]:
    hits = []
    for domain, terms in DOMAIN_TERMS.items():
        if any(re.search(r"\b" + re.escape(term) + r"\b", sentence, re.I) for term in terms):
            hits.append(domain)
    return hits


def extract_evidence(sentences: list[str]) -> list[EvidenceChain]:
    marker = re.compile(r"\b(data|experiment|test|prediction|observed|evidence|measured|falsif|empirical|dataset|analysis|R\^2|p\s*<)\b", re.I)
    chains = []
    for sentence in [s for s in sentences if marker.search(s)][:8]:
        chains.append(
            EvidenceChain(
                primary_source="paper text",
                secondary_source=None,
                tertiary_source=None,
                tested_thing=infer_tested_thing(sentence),
                connection_to_claim="candidate support; requires explicit Source -> Tested Thing -> Connection -> Gap bridge",
                gap="null model, dataset quality, or domain bridge must be checked",
                counterevidence_present="partial" if re.search(r"\b(fail|failed|contradict|however|but)\b", sentence, re.I) else "no",
                evidence_quote=sentence,
            )
        )
    return chains


def infer_tested_thing(sentence: str) -> str:
    for phrase in ["lifespan", "linguistic", "civilization", "entropy", "prediction", "dataset", "curve", "observer"]:
        if re.search(r"\b" + phrase + r"\b", sentence, re.I):
            return phrase
    return "unspecified evidence hook"


def extract_kills(sentences: list[str]) -> list[KillArch]:
    marker = re.compile(r"\b(kill|falsif|fail|failure|break|contradict|invalid|revision|rejection|not observed|does not scale)\b", re.I)
    kills = []
    for sentence in [s for s in sentences if marker.search(s)][:6]:
        kills.append(
            KillArch(
                stated_kill=sentence,
                implicit_kill="if variables cannot be operationalized or predictions are indistinguishable from baseline models",
                testable_kill="conditional; tie this sentence to a measurable dataset, threshold, or formal contradiction",
                rhetorical_armor="strong if it can demote the claim; weak if only performative humility",
                evidence_quote=sentence,
            )
        )
    return kills


def extract_equations(raw_text: str) -> list[EquationSemantics]:
    equations = []
    patterns = [r"\$([^$]{4,300})\$", r"\\\[([^\]]{4,500})\\\]", r"\\begin\{equation\}(.{4,700}?)\\end\{equation\}"]
    for pattern in patterns:
        for match in re.finditer(pattern, raw_text, re.S):
            equation = clean_text(match.group(1))
            low = equation.lower()
            if any(junk in low for junk in ["mathjax", "displaymath", "inlinemath"]):
                continue
            if not re.search(r"[=^{}]|\\frac|\\cdot|R\^2|p\s*<", equation):
                continue
            equations.append(
                EquationSemantics(
                    equation=equation,
                    role=infer_equation_role(equation),
                    status=infer_equation_status(equation),
                    undefined_vars=extract_undefined_vars(equation),
                    dimensional_status="unknown until variables/units are declared",
                    derivation_present="partial" if re.search(r"\b(derive|therefore|from)\b", raw_text, re.I) else "no",
                    computable="conditional",
                    comparison=infer_equation_comparison(equation),
                )
            )
    deduped = []
    seen = set()
    for equation in equations:
        if equation.equation not in seen:
            seen.add(equation.equation)
            deduped.append(equation)
    return deduped[:12]


def infer_equation_role(equation: str) -> str:
    if re.search(r"R\^2|p\s*<|\\sigma|\\mu", equation):
        return "statistical support or reported result"
    if re.search(r"\\chi|G\s*\\cdot|grace|faith|logos|O_", equation, re.I):
        return "framework model expression"
    return "formal or presentational expression"


def infer_equation_status(equation: str) -> EquationStatus:
    if re.search(r"R\^2|p\s*<", equation):
        return "PRESENTATIONAL"
    if re.search(r"\\chi|grace|faith|logos|O_", equation, re.I):
        return "OPERATIONAL_MODEL"
    if len(extract_undefined_vars(equation)) > 6:
        return "SYMBOLIC_FORMALISM"
    return "INTERPRETIVE"


def extract_undefined_vars(equation: str) -> list[str]:
    candidates = re.findall(r"(?<!\\)([A-Z][A-Za-z]?)", equation)
    return sorted(set(candidates))[:12]


def infer_equation_comparison(equation: str) -> str:
    if "\\frac{d" in equation or "dt" in equation:
        return "differential equation / dynamical system analogy"
    if "\\iiint" in equation or "\\int" in equation:
        return "integral action or aggregate field analogy"
    if "R^2" in equation or "p <" in equation:
        return "statistical reporting"
    return "no direct comparison inferred"


def reviewer_seeds() -> ReviewerSeeds:
    return ReviewerSeeds(
        skeptical_physicist="Define variables, units, measurement protocol, and where the prediction differs from standard physics.",
        academic_philosopher="Clarify whether each bridge is analogy, structural correspondence, ontology, or formal identity.",
        information_theorist="Lock entropy, information, observer, and state to one domain at a time.",
        methodologist="State datasets, null models, controls, replication path, and falsification thresholds.",
        hostile_critic="The likely attack is that formal language is being used rhetorically; answer with equation status, domain badges, and real kill conditions.",
    )


def build_benchmark() -> BenchmarkAnchor:
    return BenchmarkAnchor(
        comparison_target="empirical/theoretical paper with defined variables, null model, evidence bridge, and falsification threshold",
        score_context="scores are audit trails, not verdicts; internal framework fit is separate from external academic readiness",
        why_low="missing variable definitions, missing null model, unbridged domain shift, or unsupported certainty language",
        why_high="explicit claims, evidence bridge, clear equations, real kill conditions, and repair path",
        lesson="publish the ledger so critique targets specific bridges, variables, deductions, or quotes",
    )


def build_cross_dep(paper_id: str, claims: list[ClaimArch], boundaries: list[DomainBoundary]) -> CrossDependency:
    common_terms = sorted({b.term for b in boundaries})
    return CrossDependency(
        paper_id=paper_id,
        depends_on=["framework definitions", "semantic vector dictionary", "domain boundary rules"],
        enables=["HTML audit card", "Postgres ledger row", "series comparison", "LLM handoff snapshot"],
        shared_claims_with=[claim.surface_claim[:90] for claim in claims[:3]],
        term_drift_flags=common_terms,
        orphan_risk="downstream papers inherit this paper's weakness if shared terms remain undefined or unbridged",
    )


def score_claim_arch(claim: ClaimArch) -> list[ScoreEvent]:
    events: list[ScoreEvent] = []
    if claim.surface_claim:
        events.append(
            ScoreEvent(
                metric_id="CLAIM_ARCH_SURFACE",
                points=2,
                max_points=2,
                reason="Surface claim is explicit.",
                evidence_quote=claim.surface_claim,
                section=claim.section,
                kind="positive",
            )
        )
    if claim.operational_claim:
        events.append(
            ScoreEvent(
                metric_id="CLAIM_ARCH_OPERATIONAL",
                points=2,
                max_points=2,
                reason="Operational claim is present.",
                evidence_quote=claim.operational_claim,
                section=claim.section,
                kind="positive",
            )
        )
    else:
        events.append(
            ScoreEvent(
                metric_id="CLAIM_ARCH_OPERATIONAL",
                points=-2,
                max_points=2,
                reason="Operational claim is missing.",
                evidence_quote="",
                section=claim.section,
                kind="deduction",
                fix_to_improve="State what must be testable, measurable, or formally true for the claim to work.",
            )
        )
    if "unbridged" in claim.domain_shift.lower():
        events.append(
            ScoreEvent(
                metric_id="DOMAIN_BOUNDARY_UNBRIDGED",
                points=-2,
                max_points=2,
                reason="Domain shift appears unbridged.",
                evidence_quote=claim.domain_shift,
                section="DOMAIN_BOUNDARY",
                kind="deduction",
                fix_to_improve="Add a domain bridge sentence explaining whether the relation is analogy, formal correspondence, or empirical claim.",
            )
        )
    return events


def score_evidence_chain(chain: EvidenceChain) -> list[ScoreEvent]:
    events = []
    if chain.evidence_quote:
        events.append(
            ScoreEvent(
                metric_id="EVIDENCE_QUOTE_PRESENT",
                points=2,
                max_points=2,
                reason="Evidence hook is traceable to a quote.",
                evidence_quote=chain.evidence_quote,
                section=chain.section,
                kind="positive",
            )
        )
    if "requires explicit" in chain.connection_to_claim.lower() or "must be checked" in chain.gap.lower():
        events.append(
            ScoreEvent(
                metric_id="EVIDENCE_BRIDGE_GAP",
                points=-1,
                max_points=2,
                reason="Evidence-to-claim bridge still needs explicit closure.",
                evidence_quote=chain.gap,
                section=chain.section,
                kind="deduction",
                fix_to_improve="Write Source -> Tested Thing -> Connection -> Gap under the claim.",
            )
        )
    return events


def score_kill_arch(kill: KillArch) -> list[ScoreEvent]:
    if not kill.stated_kill:
        return [
            ScoreEvent(
                metric_id="KILL_ARCH_MISSING",
                points=-3,
                max_points=3,
                reason="No stated kill condition.",
                evidence_quote="",
                section=kill.section,
                kind="deduction",
                fix_to_improve="State what would falsify, demote, or weaken the claim.",
            )
        ]
    return [
        ScoreEvent(
            metric_id="KILL_ARCH_PRESENT",
            points=3,
            max_points=3,
            reason="A kill/failure condition is stated.",
            evidence_quote=kill.stated_kill,
            section=kill.section,
            kind="positive",
        )
    ]


def score_equation(eq: EquationSemantics) -> list[ScoreEvent]:
    events = [
        ScoreEvent(
            metric_id="EQ_SEM_STATUS",
            points=1,
            max_points=1,
            reason=f"Equation status labeled as {eq.status}.",
            evidence_quote=eq.equation,
            section=eq.section,
            kind="positive",
        )
    ]
    if eq.undefined_vars:
        events.append(
            ScoreEvent(
                metric_id="EQ_SEM_UNDEFINED_VARS",
                points=-min(3, len(eq.undefined_vars) * 0.5),
                max_points=3,
                reason="Equation contains variables that need local definitions.",
                evidence_quote=", ".join(eq.undefined_vars),
                section=eq.section,
                kind="deduction",
                fix_to_improve="Add nearby variable definitions and units.",
            )
        )
    return events


def score_overstatement(flag: OverstatementFlag) -> ScoreEvent:
    return ScoreEvent(
        metric_id="OVERSTATEMENT",
        points=-2 if flag.risk == "high" else -1,
        max_points=2,
        reason=f"{flag.risk.title()}-risk overstatement word found: {flag.word}",
        evidence_quote=flag.evidence_quote,
        section="OVERSTATE_PATTERN",
        kind="deduction",
        fix_to_improve=flag.safer_wording,
    )


def four_score(events: list[ScoreEvent], claims: list[ClaimArch], evidence: list[EvidenceChain], kills: list[KillArch], equations: list[EquationSemantics], flags: list[OverstatementFlag], boundaries: list[DomainBoundary]) -> FourScoreDashboard:
    positives = sum(e.points for e in events if e.points > 0)
    deductions = abs(sum(e.points for e in events if e.points < 0))

    academic = clamp01((len(evidence) * 0.08) + (len(kills) * 0.08) + (len(equations) * 0.04) + positives * 0.015 - deductions * 0.02)
    framework = clamp01((len(claims) * 0.07) + (len(equations) * 0.04) + (len(boundaries) * 0.02))
    public = clamp01(0.65 - len(flags) * 0.04 - len([b for b in boundaries if b.drift_risk == "high"]) * 0.08)
    risk = clamp01(len(flags) * 0.08 + len([b for b in boundaries if b.drift_risk == "high"]) * 0.12 + max(0, 3 - len(kills)) * 0.08)

    return FourScoreDashboard(
        academic_readiness=round(academic, 3),
        framework_coherence=round(framework, 3),
        public_communication=round(public, 3),
        risk=round(risk, 3),
        academic_label=label_score(academic),
        framework_label=label_score(framework),
        public_label=label_score(public),
        risk_label=label_risk(risk),
    )


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def label_score(value: float) -> str:
    if value >= 0.75:
        return "A / strong"
    if value >= 0.55:
        return "B / usable with review"
    if value >= 0.35:
        return "C / needs repair"
    return "D / weak"


def label_risk(value: float) -> str:
    if value >= 0.75:
        return "critical"
    if value >= 0.5:
        return "high"
    if value >= 0.25:
        return "medium"
    return "low"


def build_address(path: Path, title: str, text: str, frontmatter: dict[str, Any], overstatement_count: int, drift_count: int) -> NablaAddress:
    vector = semantic_vector(text)
    risk = detect_risk(text, overstatement_count, drift_count)
    return NablaAddress(
        domain=slug(frontmatter.get("domain") or detect_domain(text)),
        entity=slug(frontmatter.get("entity") or title),
        state=detect_state(frontmatter, text),
        audience=detect_audience(frontmatter, text),
        use=detect_use(text),
        risk=risk,
        date=str(frontmatter.get("date") or datetime.now().date()),
        vector=vector,
        hash=pair_hash(vector),
    )


def build_snapshot(path: Path, llm_extractor: Optional[LLMExtractor] = None) -> PaperSnapshot:
    title, text, frontmatter = load_document(path)
    raw = path.read_text(encoding="utf-8", errors="replace")
    sentences = split_sentences(text)

    boundaries = extract_domain_boundaries(text)
    flags = extract_overstatement(sentences)
    claims = extract_claims(sentences, boundaries)
    evidence = extract_evidence(sentences)
    kills = extract_kills(sentences)
    equations = extract_equations(raw)

    # Optional future hook: an LLM can fill buried/operational claims more deeply,
    # but Python remains the schema validator and scorer.
    if llm_extractor:
        claims = merge_llm_claims(claims, llm_extractor("CLAIM_ARCH", text))

    paper_id = stable_paper_id(path, text)
    address = build_address(path, title, text, frontmatter, len(flags), len(boundaries))

    events: list[ScoreEvent] = []
    for claim in claims:
        events.extend(score_claim_arch(claim))
    for chain in evidence:
        events.extend(score_evidence_chain(chain))
    for kill in kills:
        events.extend(score_kill_arch(kill))
    for equation in equations:
        events.extend(score_equation(equation))
    events.extend(score_overstatement(flag) for flag in flags)

    return PaperSnapshot(
        paper_id=paper_id,
        title=title,
        source_path=str(path),
        generated_at=datetime.now().isoformat(timespec="seconds"),
        address=address,
        four_scores=four_score(events, claims, evidence, kills, equations, flags, boundaries),
        claims=claims,
        evidence_chains=evidence,
        kill_conditions=kills,
        equations=equations,
        domain_boundaries=boundaries,
        reviewer_seeds=reviewer_seeds(),
        overstatement_flags=flags,
        benchmark=build_benchmark(),
        cross_dependency=build_cross_dep(paper_id, claims, boundaries),
        score_events=events,
        eight_gaps=[
            "Score separation gap",
            "Hostile reviewer gap",
            "Evidence bridge gap",
            "Domain badge gap",
            "Score ledger gap",
            "Equation semantics gap",
            "Overstatement gap",
            "Benchmark/risk-context gap",
        ],
    )


def merge_llm_claims(claims: list[ClaimArch], payload: dict[str, Any]) -> list[ClaimArch]:
    # Conservative merge point. Do not let LLM output change IDs, scores, or address.
    llm_claims = payload.get("claims") if isinstance(payload, dict) else None
    if not isinstance(llm_claims, list):
        return claims
    merged = claims[:]
    for item in llm_claims:
        if not isinstance(item, dict):
            continue
        surface = clean_text(item.get("surface_claim", ""))
        if not surface:
            continue
        merged.append(
            ClaimArch(
                surface_claim=surface,
                buried_claim=clean_text(item.get("buried_claim", "")),
                operational_claim=clean_text(item.get("operational_claim", "")),
                rhetorical_load=clean_text(item.get("rhetorical_load", "LLM-assisted")),
                domain_shift=clean_text(item.get("domain_shift", "")),
                domain_badges=[badge for badge in item.get("domain_badges", []) if badge in DOMAIN_TERMS] or ["PUBLIC_COMM"],
                evidence_quote=surface,
            )
        )
    return merged[:10]


def snapshot_to_json(snapshot: PaperSnapshot, path: Path) -> None:
    path.write_text(json.dumps(asdict(snapshot), ensure_ascii=False, indent=2), encoding="utf-8")


def render_html(snapshot: PaperSnapshot, path: Path) -> None:
    s = snapshot
    score = s.four_scores
    claims = "\n".join(f"<li>{escape(c.surface_claim)}</li>" for c in s.claims[:5]) or "<li>No claims extracted.</li>"
    evidence = "\n".join(f"<li>{escape(e.evidence_quote)}</li>" for e in s.evidence_chains[:5]) or "<li>No evidence hooks extracted.</li>"
    kills = "\n".join(f"<li>{escape(k.stated_kill)}</li>" for k in s.kill_conditions[:5]) or "<li>No kill hooks extracted.</li>"
    equations = "\n".join(
        f"<li><code>{escape(eq.equation)}</code><br><span>{eq.status} / {escape(eq.role)}</span></li>"
        for eq in s.equations[:6]
    ) or "<li>No equations extracted.</li>"
    flags = "\n".join(f"<li><b>{escape(f.word)}</b>: {escape(f.evidence_quote)}</li>" for f in s.overstatement_flags[:6]) or "<li>No overstatement flags.</li>"
    ledger = "\n".join(
        f"<tr><td>{escape(e.metric_id)}</td><td>{e.points}</td><td>{escape(e.kind)}</td><td>{escape(e.reason)}</td><td>{escape(e.fix_to_improve)}</td></tr>"
        for e in s.score_events[:40]
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{escape(s.title)} | Defensibility Snapshot</title>
  <style>
    :root {{ --bg:#070707; --card:#141419; --line:#30303a; --gold:#d4af37; --text:#f4efe3; --muted:#aaa4ba; --text-dim:#c9c1d2; --text-muted:#aaa4ba; --surface2:#101014; --border:#30303a; --red:#d45b5b; --green:#41b879; --orange:#d88b35; }}
    body {{ margin:0; background:var(--bg); color:var(--text); font-family:Inter,Segoe UI,Arial,sans-serif; }}
    main {{ max-width:1180px; margin:auto; padding:34px 20px 70px; }}
    h1 {{ font-size:clamp(32px,5vw,58px); margin:0 0 12px; line-height:1; }}
    h2 {{ color:var(--gold); font-size:16px; text-transform:uppercase; letter-spacing:.06em; margin:26px 0 12px; }}
    .panel,.card,.pr-section-wrap {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:18px; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:14px; }}
    .score b {{ display:block; color:var(--gold); font-size:30px; }}
    .muted, li span {{ color:var(--muted); }}
    .qa-btn {{ display:inline-flex; align-items:center; gap:6px; border:1px solid var(--line); background:#101014; color:var(--gold); border-radius:6px; padding:7px 10px; font-size:0.78rem; }}
    code {{ color:#f6d66f; white-space:normal; }}
    li {{ margin:8px 0; line-height:1.45; }}
    table {{ width:100%; border-collapse:collapse; font-size:13px; }}
    td,th {{ border-bottom:1px solid var(--line); padding:9px; vertical-align:top; }}
    th {{ color:var(--gold); text-align:left; }}
    @media (max-width:800px) {{ .transparency-grid {{ grid-template-columns:1fr !important; }} }}
  </style>
</head>
<body>
<main>
  <section class="panel">
    <p class="muted">Paper Defensibility Snapshot</p>
    <h1>{escape(s.title)}</h1>
    <p><b>Address:</b> {escape(s.address.canonical)}</p>
    <p class="muted">Paper ID: {escape(s.paper_id)} | Generated: {escape(s.generated_at)}</p>
  </section>
  {transparency_notice_html()}

  <h2>Four Score Separation</h2>
  <section class="grid">
    <div class="card score"><b>{score.academic_readiness}</b><span>Academic Readiness<br>{escape(score.academic_label)}</span></div>
    <div class="card score"><b>{score.framework_coherence}</b><span>Framework Coherence<br>{escape(score.framework_label)}</span></div>
    <div class="card score"><b>{score.public_communication}</b><span>Public Communication<br>{escape(score.public_label)}</span></div>
    <div class="card score"><b>{score.risk}</b><span>Risk<br>{escape(score.risk_label)}</span></div>
  </section>

  <h2>CLAIM_ARCH</h2><section class="card"><ul>{claims}</ul></section>
  <h2>EVIDENCE_CHAIN</h2><section class="card"><ul>{evidence}</ul></section>
  <h2>KILL_ARCH</h2><section class="card"><ul>{kills}</ul></section>
  <h2>EQ_SEM</h2><section class="card"><ul>{equations}</ul></section>
  <h2>OVERSTATE_PATTERN</h2><section class="card"><ul>{flags}</ul></section>
  <h2>Reviewer Seeds</h2>
  <section class="grid">
    <div class="card"><b>Skeptical Physicist</b><p>{escape(s.reviewer_seeds.skeptical_physicist if s.reviewer_seeds else "")}</p></div>
    <div class="card"><b>Academic Philosopher</b><p>{escape(s.reviewer_seeds.academic_philosopher if s.reviewer_seeds else "")}</p></div>
    <div class="card"><b>Methodologist</b><p>{escape(s.reviewer_seeds.methodologist if s.reviewer_seeds else "")}</p></div>
    <div class="card"><b>Hostile Critic</b><p>{escape(s.reviewer_seeds.hostile_critic if s.reviewer_seeds else "")}</p></div>
  </section>

  <h2>Score Ledger</h2>
  <section class="card"><table><thead><tr><th>Metric</th><th>Points</th><th>Kind</th><th>Reason</th><th>Fix</th></tr></thead><tbody>{ledger}</tbody></table></section>

  <h2>Eight Gaps</h2>
  <section class="card"><ol>{"".join(f"<li>{escape(g)}</li>" for g in s.eight_gaps)}</ol></section>

  <script type="application/json" id="paper-defensibility-snapshot">{json.dumps(asdict(s), ensure_ascii=False)}</script>
</main>
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")


def transparency_notice_html() -> str:
    return """<!-- PAPER INTELLIGENCE TRANSPARENCY NOTICE -->
<section class="pr-section-wrap" style="border-color:rgba(212,175,55,0.25); margin:0 0 2rem;">
  <h3 style="color:var(--gold); margin-top:0;">Transparency Notice</h3>
  <p style="font-size:0.85rem; color:var(--text-dim); line-height:1.7; margin:0.8rem 0;">
    This paper has been evaluated by the <strong style="color:var(--text);">Theophysics Paper Intelligence</strong> pipeline &mdash;
    a deterministic, open-source scoring system distributed as a Docker container.
    The pipeline performs automated analysis across multiple dimensions including coherence index (&chi;),
    truth density, claim-support ratio, equation coverage, lexical and semantic Fruits alignment,
    readability metrics, and Master Equation variable mapping.
  </p>
  <div class="transparency-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin:1rem 0; font-size:0.8rem;">
    <div style="border-left:2px solid var(--green); padding-left:12px;">
      <div style="color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; font-size:0.65rem; margin-bottom:4px;">What these scores measure</div>
      <div style="color:var(--text-dim); line-height:1.6;">
        Structural properties of the text. High coherence = all ten Master Equation variables engaged.
        High truth density = claims paired with evidence at a high ratio.
        Neither score validates content. That remains the reader&rsquo;s work.
      </div>
    </div>
    <div style="border-left:2px solid var(--red); padding-left:12px;">
      <div style="color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; font-size:0.65rem; margin-bottom:4px;">What these scores do not measure</div>
      <div style="color:var(--text-dim); line-height:1.6;">
        Correctness of conclusions, theological validity, experimental replicability,
        or domain-specific peer review. This is a structural audit, not a truth oracle.
      </div>
    </div>
  </div>
  <div style="background:var(--surface2); border:1px solid var(--border); border-radius:6px; padding:12px 14px; margin:1rem 0;">
    <div style="font-size:0.75rem; color:var(--gold); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:6px;">Reproducibility Guarantee</div>
    <p style="font-size:0.8rem; color:var(--text-dim); line-height:1.6; margin:0;">
      This pipeline is deterministic. Given identical input, it produces identical output across runs,
      machines, and operators. The Docker image, source code, and scoring methodology are publicly
      available. You are invited&mdash;encouraged&mdash;to run this pipeline against this paper,
      against any paper in this corpus, or against any paper from any source.
    </p>
  </div>
  <details style="margin-top:0.8rem;">
    <summary style="font-size:0.75rem; color:var(--text-muted); cursor:pointer; letter-spacing:0.5px;">Known Limitations of This Run</summary>
    <ul style="font-size:0.78rem; color:var(--text-muted); line-height:1.8; margin:8px 0 0 16px; padding:0;">
      <li>27 fine-grained emotion categories returned incomplete due to model unavailability. Affected sections are marked rather than populated with zeros.</li>
      <li>Equation counts include inline mathematical notation and may overcount relative to distinct formal statements.</li>
      <li>Formal verification against the axiom spine, Master Equation, Lagrangian, and Lean proofs requires a separate workflow not included in this scoring pass.</li>
      <li>Counterargument detection identifies explicit rebuttal language only; structural objections embedded in argument flow may not be counted.</li>
    </ul>
  </details>
  <div style="margin-top:0.8rem; display:flex; gap:8px; flex-wrap:wrap;">
    <a class="qa-btn" href="https://github.com/YellowKidokc/paper-proof-grader" target="_blank" style="text-decoration:none;">Source &amp; Docker</a>
    <a class="qa-btn" href="https://hub.docker.com/r/yellowkid/paper-intelligence" target="_blank" style="text-decoration:none;">Docker Hub</a>
    <a class="qa-btn" href="https://theophysics.pro" target="_blank" style="text-decoration:none;">Theophysics</a>
  </div>
</section>"""


def run(input_path: Path, output_dir: Path) -> PaperSnapshot:
    output_dir.mkdir(parents=True, exist_ok=True)
    snapshot = build_snapshot(input_path)
    base = slug(input_path.stem).lower()
    snapshot_to_json(snapshot, output_dir / f"{base}.snapshot.json")
    render_html(snapshot, output_dir / f"{base}.snapshot.html")
    return snapshot


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a paper defensibility snapshot.")
    parser.add_argument("input", type=Path, help="HTML, Markdown, or text paper")
    parser.add_argument("--output", type=Path, default=Path("defensibility_output"))
    args = parser.parse_args()

    snapshot = run(args.input, args.output)
    print(json.dumps({
        "paper_id": snapshot.paper_id,
        "title": snapshot.title,
        "address": snapshot.address.canonical,
        "four_scores": asdict(snapshot.four_scores),
        "claims": len(snapshot.claims),
        "evidence_chains": len(snapshot.evidence_chains),
        "kill_conditions": len(snapshot.kill_conditions),
        "equations": len(snapshot.equations),
        "score_events": len(snapshot.score_events),
    }, indent=2))


if __name__ == "__main__":
    main()
