"""
PROOF EXPLORER SNAPSHOT — Master Schema
========================================
Single canonical shape for everything that lands in the per-paper snapshot.

This is the contract:
  - Excel writer → flattens this into columns
  - HTML report → renders this into the dark/gold scorecard
  - Front-end intake page → consumes the JSON form of this
  - OpenAI prompts in 04_OPENAI_7Q/prompts/ fill named sub-sections

If a layer adds new output, add it here first, then update the layer.
If you break this schema, you break Excel + HTML + Web at once.

Author: David Lowe + Claude
Created: 2026-04-29
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, Literal
from datetime import datetime


# ─── 1. IDENTITY ────────────────────────────────────────────────────────────

@dataclass
class PaperIdentity:
    paper_id: str = ""
    title: str = ""
    author: str = ""
    version: str = ""
    date: str = ""
    series: str = ""
    domain: str = ""  # cosmology | quantum | thermodynamics | info-theory | consciousness | theology-physics-bridge | other
    paper_type: list[str] = field(default_factory=list)  # hypothesis | model | framework | derivation | empirical | philosophical | formal


# ─── 2. THESIS ──────────────────────────────────────────────────────────────

@dataclass
class Thesis:
    one_sentence: str = ""
    ai_confidence: Literal["low", "medium", "high"] = "medium"


# ─── 3. CLAIM INVENTORY ─────────────────────────────────────────────────────

@dataclass
class Claim:
    claim: str = ""
    claim_type: Literal[
        "mathematical", "physical", "information_theoretic",
        "metaphysical", "historical", "empirical", "analogy",
    ] = "physical"
    importance: Literal["core", "support", "rhetorical"] = "support"
    evidence_present: bool = False
    testability: Literal["yes", "partial", "no"] = "no"
    risk_level: Literal["low", "medium", "high"] = "medium"
    needs_citation: bool = False
    notes: str = ""


# ─── 4. EQUATION AUDIT ──────────────────────────────────────────────────────

@dataclass
class EquationEntry:
    equation: str = ""
    purpose: str = ""
    variables_defined: bool = False
    variable_definitions: dict[str, str] = field(default_factory=dict)
    dimensional_status: Literal["defined", "undefined", "symbolic", "not_applicable"] = "symbolic"
    operational_status: Literal["computable", "symbolic", "metaphorical"] = "symbolic"
    role: Literal["doing_work", "decorative", "structural", "predictive"] = "structural"
    issues: list[str] = field(default_factory=list)


# ─── 5. ASSUMPTION STACK ────────────────────────────────────────────────────

@dataclass
class AssumptionStack:
    explicit: list[str] = field(default_factory=list)
    implicit: list[str] = field(default_factory=list)
    imported: list[str] = field(default_factory=list)  # from existing physics
    theological: list[str] = field(default_factory=list)
    scientific: list[str] = field(default_factory=list)
    philosophical: list[str] = field(default_factory=list)
    measurement: list[str] = field(default_factory=list)
    causal: list[str] = field(default_factory=list)


# ─── 6. KILL CONDITIONS / FALSIFIABILITY ────────────────────────────────────

@dataclass
class KillCondition:
    claim: str = ""
    kill_condition: str = ""
    test_method: str = ""
    severity: Literal["fatal", "wounding", "minor"] = "wounding"
    current_status: Literal["open", "weak", "strong", "unresolved", "satisfied"] = "open"


# ─── 7. EVIDENCE MAP ────────────────────────────────────────────────────────

@dataclass
class EvidenceEntry:
    claim: str = ""
    supporting_evidence: str = ""
    evidence_type: Literal["primary", "secondary", "interpretive", "speculative"] = "interpretive"
    evidence_quality: Literal["weak", "moderate", "strong"] = "moderate"
    counterevidence_needed: str = ""
    gap: str = ""


# ─── 8. PHYSICS COMPARISON ──────────────────────────────────────────────────

@dataclass
class PhysicsComparison:
    nearest_theory: str = ""
    similarity: str = ""
    difference: str = ""
    does_paper_outperform: Literal["yes", "no", "unclear"] = "unclear"
    category_confusion_risk: str = ""


# ─── 9. NOVELTY CLASSIFICATION ──────────────────────────────────────────────

@dataclass
class NoveltyClassification:
    novelty_levels: list[Literal[
        "new_framing", "new_model", "new_prediction",
        "new_derivation", "new_empirical_result",
    ]] = field(default_factory=list)
    primary_novelty: str = ""
    overstated_novelty_flags: list[str] = field(default_factory=list)
    honest_label: str = ""  # what the paper SHOULD be labeled if author isn't overselling


# ─── 10. COHERENCE / REVIEW-READINESS SCORE ─────────────────────────────────

@dataclass
class CoherenceScore:
    """8-metric review-readiness rubric. NOT an objective truth score."""
    definition_clarity: int = 0      # 0-10
    equation_coherence: int = 0
    claim_discipline: int = 0
    scope_control: int = 0
    falsifiability: int = 0
    citation_adequacy: int = 0
    domain_separation: int = 0       # physics/theology/metaphor/math kept distinct
    reader_burden: int = 0
    review_readiness: int = 0        # weighted aggregate, 0-100
    ai_confidence: Literal["low", "medium", "high"] = "medium"


# ─── 11. OVERSTATEMENT DETECTOR ─────────────────────────────────────────────

@dataclass
class OverstatementDetector:
    overstated_passages: list[str] = field(default_factory=list)
    rhetorical_strength_index: float = 0.0  # 0-1, prose intensity
    evidence_strength_index: float = 0.0    # 0-1, supporting backing
    delta: float = 0.0                       # rhetorical - evidence; positive = oversold
    severity: Literal["none", "mild", "moderate", "severe"] = "none"


# ─── 12. REVISION PLAN ──────────────────────────────────────────────────────

@dataclass
class RevisionPlan:
    strongest_part: str = ""
    weakest_part: str = ""
    must_fix_before_publication: list[str] = field(default_factory=list)
    best_next_test: str = ""
    needs_expert_review: list[str] = field(default_factory=list)  # e.g. ["philology", "statistics"]


# ─── 13. CITATIONS / CROSS-PAPER LINKS ──────────────────────────────────────

@dataclass
class CitationNode:
    cited: str = ""           # title or identifier
    relation: Literal[
        "supports", "extends", "replaces", "contradicts", "depends_on", "uses_method",
    ] = "supports"
    confidence: Literal["low", "medium", "high"] = "medium"


# ─── 14. THEOPHYSICS-OPTIONAL OVERLAY ───────────────────────────────────────
# Only filled when domain == "theophysics" or paper opts in.
# This is where the existing 7Q / Decision Tree / Swap Test / Fruits stuff lives.

@dataclass
class TheophysicsOverlay:
    seven_q_grid: dict = field(default_factory=dict)        # Q0-Q7 narrative cells
    decision_tree_status: dict = field(default_factory=dict)  # Q0-Q12 worldview filter
    swap_test: dict = field(default_factory=dict)
    ckg_score: dict = field(default_factory=dict)
    fruits_score: dict = field(default_factory=dict)
    spine_mappings: dict = field(default_factory=dict)      # Physics/Theology/Consciousness/Cat-Theory
    declared_axioms: list[str] = field(default_factory=list)  # manual entry, not auto-extracted
    lean_file_path: Optional[str] = None                     # if user uploaded their own .lean


# ─── MASTER SNAPSHOT ────────────────────────────────────────────────────────

@dataclass
class ProofExplorerSnapshot:
    schema_version: str = "1.0.0"
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    paper_id: str = ""

    identity: PaperIdentity = field(default_factory=PaperIdentity)
    thesis: Thesis = field(default_factory=Thesis)
    claim_inventory: list[Claim] = field(default_factory=list)
    equations: list[EquationEntry] = field(default_factory=list)
    assumptions: AssumptionStack = field(default_factory=AssumptionStack)
    kill_conditions: list[KillCondition] = field(default_factory=list)
    evidence_map: list[EvidenceEntry] = field(default_factory=list)
    physics_comparison: list[PhysicsComparison] = field(default_factory=list)
    novelty: NoveltyClassification = field(default_factory=NoveltyClassification)
    coherence: CoherenceScore = field(default_factory=CoherenceScore)
    overstatement: OverstatementDetector = field(default_factory=OverstatementDetector)
    revision: RevisionPlan = field(default_factory=RevisionPlan)
    spine_analysis: dict = field(default_factory=dict)
    citations: list[CitationNode] = field(default_factory=list)

    # Existing pipeline outputs (L1-L10) merge in here as a flat dict
    pipeline_metrics: dict = field(default_factory=dict)

    # Optional theophysics-specific data (only filled when relevant)
    theophysics: Optional[TheophysicsOverlay] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ProofExplorerSnapshot":
        # Minimal, defensive reconstruction. Used when reading saved JSON.
        snap = cls()
        for k, v in d.items():
            if hasattr(snap, k):
                setattr(snap, k, v)
        return snap
