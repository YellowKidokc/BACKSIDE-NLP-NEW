# Shared library for Theophysics Paper Intelligence Suite.
# Currently exports: snapshot_schema (master ProofExplorerSnapshot dataclass)
from .snapshot_schema import (
    ProofExplorerSnapshot,
    PaperIdentity,
    Thesis,
    Claim,
    EquationEntry,
    AssumptionStack,
    KillCondition,
    EvidenceEntry,
    PhysicsComparison,
    NoveltyClassification,
    CoherenceScore,
    OverstatementDetector,
    RevisionPlan,
    CitationNode,
    TheophysicsOverlay,
)

__all__ = [
    "ProofExplorerSnapshot",
    "PaperIdentity",
    "Thesis",
    "Claim",
    "EquationEntry",
    "AssumptionStack",
    "KillCondition",
    "EvidenceEntry",
    "PhysicsComparison",
    "NoveltyClassification",
    "CoherenceScore",
    "OverstatementDetector",
    "RevisionPlan",
    "CitationNode",
    "TheophysicsOverlay",
]
