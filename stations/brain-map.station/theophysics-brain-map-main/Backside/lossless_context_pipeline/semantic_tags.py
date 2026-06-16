from __future__ import annotations

import json
from urllib.parse import quote

from .ids import stable_uuid
from .schemas import (
    ClaimArch,
    DomainBoundary,
    EquationSemantics,
    EvidenceChain,
    KillArch,
    MarkdownBlock,
    MechanismEdge,
    SemanticTag,
)


CHI_TERMS: dict[str, set[str]] = {
    "G": {"ground", "gravity", "grace", "authority", "source", "foundation", "external order"},
    "M": {"mechanism", "motion", "force", "action", "workflow", "process", "operation", "causal"},
    "E": {"entropy", "disorder", "fragment", "noise", "corrupt", "contradiction", "ambiguity"},
    "S": {"self", "identity", "personhood", "soul", "inner life", "who"},
    "T": {"time", "sequence", "chronology", "irreversible", "before", "after", "version"},
    "K": {"knowledge", "information", "definition", "claim", "data", "equation", "formal"},
    "R": {"relation", "bond", "dependency", "network", "covenant", "reference", "interlock"},
    "Q": {"experience", "felt", "emotion", "perception", "qualia", "subjective"},
    "F": {"faith", "trust", "belief", "uncertainty", "commitment", "reliance"},
    "C": {"coherence", "unity", "synthesis", "integration", "unification", "reconciliation"},
}


def detect_chi_vars(text: str) -> list[str]:
    low = text.lower()
    hits: list[str] = []
    for var, terms in CHI_TERMS.items():
        if any(term in low for term in terms):
            hits.append(var)
    return hits


def master_equation_uuid(doc_id: str, content_hash: str, address: str) -> str:
    return stable_uuid("master-equation-uuid", doc_id, content_hash, address)


def _quote(text: str, limit: int = 260) -> str:
    compact = " ".join(text.split())
    return compact[:limit]


def _tag(
    *,
    doc_id: str,
    master_uuid: str,
    tag_type: str,
    label: str,
    block_id: str | None,
    source_quote: str | None,
    chi_vars: list[str],
    meta: dict,
) -> SemanticTag:
    tag_id = stable_uuid("semantic-tag", doc_id, tag_type, block_id or "", label, json.dumps(meta, sort_keys=True))
    return SemanticTag(
        tag_id=tag_id,
        tag_type=tag_type,
        label=label,
        block_id=block_id,
        source_quote=source_quote,
        chi_vars=chi_vars,
        master_equation_uuid=master_uuid,
        meta=meta,
    )


def build_semantic_tags(
    *,
    doc_id: str,
    master_uuid: str,
    address: str,
    vector_string: str,
    semantic_hash: str,
    blocks: list[MarkdownBlock],
    claims: list[ClaimArch],
    evidence: list[EvidenceChain],
    kills: list[KillArch],
    equations: list[EquationSemantics],
    domains: list[DomainBoundary],
    mechanisms: list[MechanismEdge],
) -> list[SemanticTag]:
    block_map = {block.block_id: block for block in blocks}
    tags: list[SemanticTag] = [
        _tag(
            doc_id=doc_id,
            master_uuid=master_uuid,
            tag_type="DocumentAddress",
            label=address,
            block_id=None,
            source_quote=None,
            chi_vars=detect_chi_vars(address),
            meta={"address": address, "vector": vector_string, "hash": semantic_hash},
        )
    ]

    for claim in claims:
        block = block_map.get(claim.block_id)
        tags.append(
            _tag(
                doc_id=doc_id,
                master_uuid=master_uuid,
                tag_type="Claim",
                label=_quote(claim.surface_claim, 120),
                block_id=claim.block_id,
                source_quote=_quote(block.text if block else claim.surface_claim),
                chi_vars=block.chi_vars if block else detect_chi_vars(claim.surface_claim),
                meta={
                    "claim_id": claim.claim_id,
                    "domain_badges": claim.domain_badges,
                    "chain": " -> ".join(block.heading_path) if block else "",
                    "weakestLink": "EXPAND_REQUIRED",
                    "ifBreaks": "EXPAND_REQUIRED",
                    "vulnerability": claim.rhetorical_load,
                    "unlocks": claim.operational_claim,
                },
            )
        )

    for item in evidence:
        block = block_map.get(item.block_id)
        tags.append(
            _tag(
                doc_id=doc_id,
                master_uuid=master_uuid,
                tag_type="EvidenceBundle",
                label=_quote(item.primary_source or item.gap, 120),
                block_id=item.block_id,
                source_quote=_quote(block.text if block else item.gap),
                chi_vars=block.chi_vars if block else detect_chi_vars(item.gap),
                meta={
                    "evidence_id": item.evidence_id,
                    "claimBeingGrounded": "EXPAND_REQUIRED",
                    "dataCited": item.primary_source,
                    "supportsFullOrWeakerVersion": "EXPAND_REQUIRED",
                    "whatKillsEmpirically": "EXPAND_REQUIRED",
                    "confidence": "EXPAND_REQUIRED",
                    "vulnerability": item.gap,
                    "unlocks": item.connection_to_claim,
                },
            )
        )

    for item in kills:
        block = block_map.get(item.block_id)
        tags.append(
            _tag(
                doc_id=doc_id,
                master_uuid=master_uuid,
                tag_type="KillCondition",
                label=_quote(item.stated_kill or item.implicit_kill, 120),
                block_id=item.block_id,
                source_quote=_quote(block.text if block else item.testable_kill),
                chi_vars=block.chi_vars if block else detect_chi_vars(item.testable_kill),
                meta={
                    "repair_item_id": item.repair_item_id,
                    "statedKill": item.stated_kill,
                    "implicitKill": item.implicit_kill,
                    "testableKill": item.testable_kill,
                    "rhetoricalArmor": item.rhetorical_armor,
                },
            )
        )

    for item in equations:
        block = block_map.get(item.block_id)
        tags.append(
            _tag(
                doc_id=doc_id,
                master_uuid=master_uuid,
                tag_type="Equation",
                label=_quote(item.equation, 120),
                block_id=item.block_id,
                source_quote=_quote(block.text if block else item.equation),
                chi_vars=block.chi_vars if block else detect_chi_vars(item.equation),
                meta={
                    "equation_id": item.equation_id,
                    "role": item.role,
                    "status": item.status,
                    "undefinedVars": item.undefined_vars,
                    "computable": item.computable,
                },
            )
        )

    for item in domains:
        tags.append(
            _tag(
                doc_id=doc_id,
                master_uuid=master_uuid,
                tag_type="DomainBoundary",
                label=item.term,
                block_id=None,
                source_quote=None,
                chi_vars=detect_chi_vars(item.term),
                meta=item.model_dump(mode="json"),
            )
        )

    for index, item in enumerate(mechanisms[:60], start=1):
        tags.append(
            _tag(
                doc_id=doc_id,
                master_uuid=master_uuid,
                tag_type="Relationship",
                label=f"{item.source} {item.relation} {item.target}"[:120],
                block_id=item.evidence_block_id,
                source_quote=None,
                chi_vars=detect_chi_vars(f"{item.source} {item.target}"),
                meta={
                    "relationship_index": index,
                    "domainA": item.source,
                    "domainB": item.target,
                    "isomorphism": item.relation,
                    "constrainsPredictions": "EXPAND_REQUIRED",
                    "whatWouldMakeThisJustAMetaphor": "EXPAND_REQUIRED",
                    "vulnerability": "EXPAND_REQUIRED",
                    "unlocks": "EXPAND_REQUIRED",
                },
            )
        )

    return tags


def render_semantic_tag_markdown(tags: list[SemanticTag]) -> str:
    rows = ["--- SEMANTIC TAGS ---%%"]
    for tag in tags:
        meta = quote(json.dumps(tag.meta, ensure_ascii=False, sort_keys=True), safe="")
        label = tag.label.replace('"', '\\"')
        block = tag.block_id or "null"
        rows.append(f'%%tag::{tag.tag_type}::{tag.tag_id}::"{label}"::{block}::meta={meta}%%')
    rows.append("%%--- END SEMANTIC TAGS ---%%")
    return "\n".join(rows)
