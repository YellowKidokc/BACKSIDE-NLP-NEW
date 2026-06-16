from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


BlockType = Literal["CLAIM", "EVIDENCE", "EQUATION", "DEFINITION", "KILL_CONDITION", "DOMAIN_SHIFT", "OTHER"]
DomainBadge = Literal[
    "PHYSICS",
    "THEOLOGY",
    "FORMAL",
    "EMPIRICAL",
    "ANALOGY",
    "METAPHYSICS",
    "INFORMATION",
    "PUBLIC_COMM",
    "LEGAL",
    "TECH",
    "UNKNOWN",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class IdSet(BaseModel):
    vault_id: str
    doc_id: str
    note_version: str
    content_hash: str
    run_id: str
    audit_snapshot_id: str


class MarkdownBlock(BaseModel):
    block_id: str
    section_id: str
    heading_path: list[str]
    ordinal: int
    text: str
    block_type: BlockType
    content_hash: str
    domain_badges: list[DomainBadge] = Field(default_factory=list)
    overstatement_words: list[str] = Field(default_factory=list)
    chi_vars: list[str] = Field(default_factory=list)
    embedding: list[float] | None = None


class EquationSemantics(BaseModel):
    equation_id: str
    block_id: str
    equation: str
    role: str
    status: str
    undefined_vars: list[str] = Field(default_factory=list)
    dimensional_status: str = "UNKNOWN"
    derivation_present: bool = False
    computable: bool = False
    known_theory_comparison: str = "EXPAND_REQUIRED"


class ClaimArch(BaseModel):
    claim_id: str
    block_id: str
    surface_claim: str
    buried_claim: str = "EXPAND_REQUIRED"
    operational_claim: str = "EXPAND_REQUIRED"
    rhetorical_load: str
    domain_shift: bool
    domain_badges: list[DomainBadge]


class EvidenceChain(BaseModel):
    evidence_id: str
    block_id: str
    primary_source: str | None = None
    secondary_source: str | None = None
    tertiary_source: str | None = None
    tested_thing: str = "EXPAND_REQUIRED"
    connection_to_claim: str = "EXPAND_REQUIRED"
    gap: str
    counterevidence_present: bool = False


class KillArch(BaseModel):
    repair_item_id: str
    block_id: str
    stated_kill: str | None = None
    implicit_kill: str = "EXPAND_REQUIRED"
    testable_kill: str = "EXPAND_REQUIRED"
    rhetorical_armor: str


class DomainBoundary(BaseModel):
    term: str
    domain_usage_1: str
    domain_usage_2: str | None = None
    domain_usage_3: str | None = None
    bridge_present: bool
    bridge_quality: str
    drift_risk: str


class MechanismEdge(BaseModel):
    source: str
    relation: str
    target: str
    evidence_block_id: str | None = None


class ReviewerSeed(BaseModel):
    reviewer: str
    attack: str
    severity: str
    repair: str


class ScoreLedgerEntry(BaseModel):
    metric: str
    max_points: int
    positive_points: int
    deductions: list[str]
    evidence_quote: str
    section: str
    fix_to_improve: str


class Grade(BaseModel):
    score: int
    grade: str
    reason: str
    top_positive: str
    top_deduction: str
    fix_to_improve: str


class FourScoreDashboard(BaseModel):
    Academic_Readiness: Grade
    Framework_Coherence: Grade
    Public_Communication: Grade
    Risk: Grade


class GapItem(BaseModel):
    status: str
    why_it_matters: str
    repair_action: str


class SemanticTag(BaseModel):
    tag_id: str
    tag_type: str
    label: str
    block_id: str | None = None
    source_quote: str | None = None
    chi_vars: list[str] = Field(default_factory=list)
    master_equation_uuid: str
    meta: dict = Field(default_factory=dict)


class LosslessArtifact(BaseModel):
    protocol_version: str = "1.0"
    generated_at: str = Field(default_factory=utc_now)
    ids: IdSet
    master_equation_uuid: str
    compression_declaration: dict
    address: str
    filename_safe_address: str
    semantic_vector: dict[str, int]
    vector_string: str
    hash: str
    spine: list[str]
    entities: list[str]
    semantics: list[str]
    blocks: list[MarkdownBlock]
    claim_arch: list[ClaimArch]
    evidence_chain: list[EvidenceChain]
    kill_arch: list[KillArch]
    eq_sem: list[EquationSemantics]
    domain_boundary: list[DomainBoundary]
    mechanism_graph: list[MechanismEdge]
    reviewer_seeds: list[ReviewerSeed]
    overstate_pattern: dict
    ledger_schema: list[ScoreLedgerEntry]
    four_score_dashboard: FourScoreDashboard
    cross_dep: dict
    eight_gaps: dict[str, GapItem]
    semantic_tags: list[SemanticTag] = Field(default_factory=list)
    semantic_tag_markdown: str = ""
    seed_bank: dict[str, list[str]]
    open_threads: list[str]
    decompress: list[str]
    check: dict
    recovery_key: str
