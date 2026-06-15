"""
SNAPSHOT MERGE
==============
Glue between the prompt library outputs (`prompts.run_all`) and the master
`ProofExplorerSnapshot` dataclass.

The prompts return JSON dicts whose keys do not always line up 1:1 with the
schema fields:
  - claim_inventory      â†’ wraps the list under "claims"
  - equation_audit       â†’ wraps under "equations"
  - kill_conditions      â†’ wraps under "kill_conditions"
  - evidence_map         â†’ wraps under "evidence_map"
  - physics_comparison   â†’ wraps under "comparisons"
  - assumption_stack     â†’ flat dict matching AssumptionStack + extra ai_confidence
  - novelty_classification â†’ flat dict matching NoveltyClassification + ai_confidence
  - coherence_score      â†’ flat dict + extra justifications + ai_confidence
  - overstatement_detector â†’ flat dict + ai_confidence
  - revision_plan        -> flat dict + ai_confidence
  - spine_analysis       -> flat dict matching the GTQ question-answer spine shape

This module isolates that mapping so adding/renaming a section only touches
one place.
"""
from __future__ import annotations

from dataclasses import fields
from datetime import datetime
from typing import Any

from .snapshot_schema import (
    AssumptionStack,
    CoherenceScore,
    NoveltyClassification,
    OverstatementDetector,
    PaperIdentity,
    ProofExplorerSnapshot,
    RevisionPlan,
)


def _filter_to_dataclass(dc_cls, payload: dict) -> dict:
    """Drop keys not declared on the dataclass â€” protects against extra fields
    like `ai_confidence` or `justifications` that some prompts include."""
    if not isinstance(payload, dict):
        return {}
    allowed = {f.name for f in fields(dc_cls)}
    return {k: v for k, v in payload.items() if k in allowed}


def merge_sections_into_snapshot(
    sections: dict[str, Any],
    snapshot: ProofExplorerSnapshot,
) -> ProofExplorerSnapshot:
    """Merge `prompts.run_all()` output into an existing snapshot in place.

    Errored sections (dicts containing 'error') are skipped silently â€” the
    snapshot's defaults remain so the JSON shape stays predictable.
    """
    sections = sections or {}

    # --- list-of-dataclass sections (stored as plain dicts; asdict tolerates) ---
    ci = sections.get("claim_inventory") or {}
    if isinstance(ci, dict) and "claims" in ci and not ci.get("error"):
        snapshot.claim_inventory = ci.get("claims") or []

    eq = sections.get("equation_audit") or {}
    if isinstance(eq, dict) and "equations" in eq and not eq.get("error"):
        snapshot.equations = eq.get("equations") or []

    kc = sections.get("kill_conditions") or {}
    if isinstance(kc, dict) and "kill_conditions" in kc and not kc.get("error"):
        snapshot.kill_conditions = kc.get("kill_conditions") or []

    em = sections.get("evidence_map") or {}
    if isinstance(em, dict) and "evidence_map" in em and not em.get("error"):
        snapshot.evidence_map = em.get("evidence_map") or []

    pc = sections.get("physics_comparison") or {}
    if isinstance(pc, dict) and "comparisons" in pc and not pc.get("error"):
        snapshot.physics_comparison = pc.get("comparisons") or []

    # --- single-dataclass sections ---
    ass = sections.get("assumption_stack") or {}
    if isinstance(ass, dict) and not ass.get("error"):
        snapshot.assumptions = AssumptionStack(**_filter_to_dataclass(AssumptionStack, ass))

    nov = sections.get("novelty_classification") or {}
    if isinstance(nov, dict) and not nov.get("error"):
        snapshot.novelty = NoveltyClassification(**_filter_to_dataclass(NoveltyClassification, nov))

    coh = sections.get("coherence_score") or {}
    if isinstance(coh, dict) and not coh.get("error"):
        snapshot.coherence = CoherenceScore(**_filter_to_dataclass(CoherenceScore, coh))

    ovs = sections.get("overstatement_detector") or {}
    if isinstance(ovs, dict) and not ovs.get("error"):
        snapshot.overstatement = OverstatementDetector(**_filter_to_dataclass(OverstatementDetector, ovs))

    rev = sections.get("revision_plan") or {}
    if isinstance(rev, dict) and not rev.get("error"):
        snapshot.revision = RevisionPlan(**_filter_to_dataclass(RevisionPlan, rev))

    spine = sections.get("spine_analysis") or {}
    if isinstance(spine, dict) and not spine.get("error"):
        snapshot.spine_analysis = spine

    return snapshot


def build_snapshot(
    paper_id: str,
    paper_path: str,
    pipeline_metrics: dict[str, Any] | None = None,
    sections: dict[str, Any] | None = None,
    identity_overrides: dict[str, Any] | None = None,
) -> ProofExplorerSnapshot:
    """Construct a full snapshot for one paper.

    Args:
        paper_id: stable id (`P-â€¦`) from the orchestrator.
        paper_path: source file path â€” used to fill identity.title from filename.
        pipeline_metrics: flat dict of L1-L10 outputs (everything that lands on
            the Excel row, minus internal keys). Stored on `snapshot.pipeline_metrics`.
        sections: result of `prompts.run_all()`. Optional â€” when missing or all
            errored, the snapshot is still emitted with empty section defaults.
        identity_overrides: optional manual fields (title, author, domain, â€¦)
            from a web intake form. Filled into `snapshot.identity`.
    """
    snap = ProofExplorerSnapshot()
    snap.paper_id = paper_id
    snap.generated_at = datetime.utcnow().isoformat()

    from pathlib import Path
    p = Path(paper_path)

    snap.identity = PaperIdentity(
        paper_id=paper_id,
        title=(identity_overrides or {}).get("title") or p.stem,
        author=(identity_overrides or {}).get("author", ""),
        version=(identity_overrides or {}).get("version", ""),
        date=(identity_overrides or {}).get("date", ""),
        series=(identity_overrides or {}).get("series", ""),
        domain=(identity_overrides or {}).get("domain", ""),
        paper_type=(identity_overrides or {}).get("paper_type", []) or [],
    )

    snap.pipeline_metrics = pipeline_metrics or {}

    if sections:
        merge_sections_into_snapshot(sections, snap)

    return snap

