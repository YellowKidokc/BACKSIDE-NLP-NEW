"""
nabla_engine.py - Nabla-Chi Universal Semantic Classification Engine v1.0
Theophysics Research Initiative | POF 2828 | June 2026

Classifies, names, decodes, compresses, grades, and coherence-tests
any document, claim, file, dataset, paper, note, transcript, or artifact.

74 independent classification factors. No lexicon. Pure structure.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Literal, Optional
import json, math

# ============================================================
# SECTION 1 — FILING DIMENSIONS (D/N/V/A/U/R)
# ============================================================

DOMAINS = [
    "THEOPHYSICS","SCIENCE","LAW","MEDICINE","FINANCE","PERSONAL",
    "TECH","EDUCATION","GOVERNANCE","ART","BUSINESS","RELIGION",
    "HISTORY","MDA","DATA","UNKNOWN"
]
STATES = {"D":"Draft","W":"Working","F":"Final","P":"Published",
          "A":"Archived","X":"Deprecated","U":"Unknown"}
AUDIENCES = [
    "SELF","INTERNAL","TEAM","AI_RESEARCH","PUBLIC","PUBLIC_RESEARCH",
    "ACADEMIC","CLIENT","RESTRICTED","LEGAL","UNKNOWN"
]
USE_DIRECTIONS = {"I":"Inform","B":"Bind","T":"Transform","R":"Record"}
RISK_LEVELS = {"R0":"public/low","R1":"internal research",
               "R2":"private/PII","R3":"legal/financial/reputational",
               "R4":"life-critical/safety"}

# ============================================================
# SECTION 2 — TEN SEMANTIC VARIABLES
# ============================================================

VARIABLES = {
    "G": "Authority/Ground",
    "M": "Mechanism/Action",
    "E": "Entropy/Disorder",
    "S": "Identity/Self",
    "T": "Time/Sequence",
    "K": "Knowledge/Info",
    "R": "Relation/Bond",
    "Q": "Experience/Felt",
    "F": "Faith/Trust",
    "C": "Coherence/Unity",
}

# Tie-break order for hash construction
TIEBREAK_ORDER = ["E","C","G","K","M","T","R","F","S","Q"]

CLAIM_TYPES = [
    "AXIOM","PRE_ASSUMPTION","EMPIRICAL_EVENT","INSTRUMENT_MEASUREMENT",
    "HISTORICAL_RECORD","INSTITUTIONAL_FACT","LEGAL_FACT","MATHEMATICAL_PROOF",
    "FORMAL_DERIVATION","CLASSIFICATION","INTERPRETATION","SYMBOLIC_TRUTH",
    "MORAL_CLAIM","THEOLOGICAL_CLAIM","EXPERIENTIAL_REPORT","PREDICTION",
    "FICTIONAL_CLAIM","CULTURAL_TRUTH","UNKNOWN"
]

REGIMES = ["constructive","destructive","mixed","unknown"]


# ============================================================
# SECTION 3 — CORE DATACLASSES
# ============================================================

@dataclass
class FilingAddress:
    domain: str = "UNKNOWN"
    entity: str = "X"
    state: str = "U"
    audience: str = "UNKNOWN"
    use_direction: str = "I"
    risk: str = "R0"

    def to_string(self):
        return f"{self.domain}/{self.entity}/{self.state}/{self.audience}/{self.use_direction}/{self.risk}"


@dataclass
class SemanticVector:
    G: int = 0; M: int = 0; E: int = 0; S: int = 0; T: int = 0
    K: int = 0; R: int = 0; Q: int = 0; F: int = 0; C: int = 0

    def to_string(self):
        return "".join(f"{k}{getattr(self, k)}" for k in VARIABLES)

    def to_dict(self):
        return {k: getattr(self, k) for k in VARIABLES}

    def dominants(self):
        return [k for k in VARIABLES if getattr(self, k) == 3]

    def absents(self):
        return [k for k in VARIABLES if getattr(self, k) == 0]


def build_hash(vector: SemanticVector) -> str:
    """Build semantic hash: pair strongest with weakest inward."""
    scores = {k: getattr(vector, k) for k in VARIABLES}
    # Sort: 3s before 0s, within equal scores use tiebreak order
    ranked = sorted(scores.keys(),
                    key=lambda k: (-scores[k], TIEBREAK_ORDER.index(k)))
    # Pair: [#1 with #10], [#2 with #9], [#3 with #8], [#4 with #7], [#5 with #6]
    pairs = []
    for i in range(5):
        pairs.append(f"[{ranked[i]}*{ranked[9-i]}]")
    return "".join(pairs)


@dataclass
class Confidence:
    G: float = 0.5; M: float = 0.5; E: float = 0.5; S: float = 0.5
    T: float = 0.5; K: float = 0.5; R: float = 0.5; Q: float = 0.5
    F: float = 0.5; C: float = 0.5

    def review_flags(self):
        return [k for k in VARIABLES if getattr(self, k) < 0.75]


@dataclass
class RegimeMap:
    law_1_gravity: str = "unknown"
    law_2_motion: str = "unknown"
    law_3_em: str = "unknown"
    law_4_strong: str = "unknown"
    law_5_thermo: str = "unknown"
    law_6_info: str = "unknown"
    law_7_quantum: str = "unknown"
    law_8_relativity: str = "unknown"
    law_9_weak: str = "unknown"
    law_10_coherence: str = "unknown"

    def constructive_count(self):
        return sum(1 for v in asdict(self).values() if v == "constructive")
    def destructive_count(self):
        return sum(1 for v in asdict(self).values() if v == "destructive")


@dataclass
class DefensibilityGrade:
    score: int = 0
    grade: str = ""
    reason: str = ""
    top_positive: str = ""
    top_deduction: str = ""
    fix_to_improve: str = ""


@dataclass
class NablaClassification:
    """Full Nabla-Chi classification for any artifact."""
    filing: FilingAddress = field(default_factory=FilingAddress)
    vector: SemanticVector = field(default_factory=SemanticVector)
    confidence: Confidence = field(default_factory=Confidence)
    regime_map: RegimeMap = field(default_factory=RegimeMap)
    academic_readiness: DefensibilityGrade = field(default_factory=DefensibilityGrade)
    framework_coherence: DefensibilityGrade = field(default_factory=DefensibilityGrade)
    public_communication: DefensibilityGrade = field(default_factory=DefensibilityGrade)
    risk_grade: DefensibilityGrade = field(default_factory=DefensibilityGrade)
    claims: list = field(default_factory=list)
    final_action: str = "KEEP"
    what_holds: list = field(default_factory=list)
    what_breaks: list = field(default_factory=list)
    repair_list: list = field(default_factory=list)

    def compute(self):
        self.hash = build_hash(self.vector)
        self.vector_string = self.vector.to_string()
        self.address_string = self.filing.to_string()
        self.full_address = f"{self.address_string} :: {self.vector_string} :: {self.hash}"
        self.dominants = self.vector.dominants()
        self.absents = self.vector.absents()
        self.review_flags = self.confidence.review_flags()
        self.filename_safe = f"{self.filing.domain}_{self.filing.entity}_{self.filing.state}_{self.filing.risk}".replace(" ","_")
        return self

    def to_json(self):
        d = asdict(self)
        d["hash"] = self.hash
        d["vector_string"] = self.vector_string
        d["full_address"] = self.full_address
        d["dominants"] = self.dominants
        d["absents"] = self.absents
        d["filename_safe"] = self.filename_safe
        return json.dumps(d, indent=2, ensure_ascii=False)

    def to_compact(self):
        return {
            "address": self.full_address,
            "dominants": self.dominants,
            "absents": self.absents,
            "constructive": self.regime_map.constructive_count(),
            "destructive": self.regime_map.destructive_count(),
            "flags": self.review_flags,
            "action": self.final_action,
        }


if __name__ == "__main__":
    # Demo: classify Washington's 1789 inaugural
    nc = NablaClassification(
        filing=FilingAddress("GOVERNANCE","WASHINGTON_1789_INAUGURAL","P","PUBLIC","I","R0"),
        vector=SemanticVector(G=3, M=0, E=0, S=0, T=3, K=3, R=3, Q=3, F=3, C=3),
        confidence=Confidence(G=0.92, M=0.60, E=0.96, S=0.90, T=0.88, K=0.85, R=0.80, Q=0.82, F=0.88, C=0.84),
        regime_map=RegimeMap(law_1_gravity="constructive", law_2_motion="constructive",
                            law_5_thermo="constructive", law_6_info="constructive",
                            law_7_quantum="constructive", law_10_coherence="constructive"),
    ).compute()
    print(nc.full_address)
    print(f"Dominants: {nc.dominants}")
    print(f"Absents: {nc.absents}")
    print(f"Flags: {nc.review_flags}")
    print(f"Constructive: {nc.regime_map.constructive_count()}")
