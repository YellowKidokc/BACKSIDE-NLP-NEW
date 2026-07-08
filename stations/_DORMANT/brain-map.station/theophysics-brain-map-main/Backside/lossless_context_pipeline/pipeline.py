from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .address import build_address, recovery_key, score_vector, semantic_hash, vector_string
from .classify import citations, classify_block, domain_badges, equations, overstatement_words
from .embeddings import Embedder
from .ids import file_doc_id, short_hash, slugify, stable_uuid
from .markdown_parser import load_markdown, split_blocks
from .semantic_tags import build_semantic_tags, detect_chi_vars, master_equation_uuid, render_semantic_tag_markdown
from .schemas import (
    ClaimArch,
    DomainBoundary,
    EvidenceChain,
    FourScoreDashboard,
    GapItem,
    Grade,
    IdSet,
    KillArch,
    LosslessArtifact,
    MarkdownBlock,
    MechanismEdge,
    EquationSemantics,
    ReviewerSeed,
    ScoreLedgerEntry,
)


DOMAIN_TERMS = ["entropy", "coherence", "information", "field", "truth", "proof", "law", "grace", "faith", "meaning"]
RELATION_WORDS = {
    "because": "supports",
    "therefore": "supports",
    "requires": "depends_on",
    "depends": "depends_on",
    "enables": "enables",
    "limits": "limits",
    "contradicts": "contradicts",
    "refines": "refines",
}


def _frontmatter_value(frontmatter: dict[str, Any], key: str, default: str) -> str:
    if key == "access" and "access" not in frontmatter and "audience" in frontmatter:
        value = frontmatter.get("audience", default)
        return str(value).upper()
    value = frontmatter.get(key, default)
    return str(value).upper() if key in {"domain", "access", "use", "risk"} else str(value)


def _entity_candidates(text: str) -> list[str]:
    names = re.findall(r"\b[A-Z][A-Za-z0-9_\-]*(?:\s+[A-Z][A-Za-z0-9_\-]*){0,4}\b", text)
    files = re.findall(r"\b[\w.\-]+\.(?:md|json|html|py|sql|csv|yml|yaml|bat)\b", text, re.IGNORECASE)
    equations_found = equations(text)
    seen: set[str] = set()
    rows: list[str] = []
    for item in names + files + equations_found:
        clean = item.strip()
        if clean and clean.lower() not in seen:
            seen.add(clean.lower())
            rows.append(clean)
    return rows[:80]


def _spine(blocks: list[MarkdownBlock]) -> list[str]:
    rows: list[str] = []
    for block in blocks:
        if block.block_type in {"CLAIM", "KILL_CONDITION", "DOMAIN_SHIFT", "EQUATION"}:
            status = "PROVISIONAL" if block.overstatement_words else "EXTRACTED"
            rationale = block.heading_path[-1] if block.heading_path else "root"
            rows.append(f"{block.block_type} :: {block.text[:260]} :: {rationale} :: {status}")
    return rows[:30]


def _semantics(blocks: list[MarkdownBlock]) -> list[str]:
    rows: list[str] = []
    for block in blocks:
        if block.block_type == "DEFINITION":
            rows.append(f"{block.text[:180]} :: LOCAL-DEFINITION :: extracted from {block.section_id}")
    for term in DOMAIN_TERMS:
        hits = [block for block in blocks if term in block.text.lower()]
        if hits:
            rows.append(f"{term} :: PROJECT-SENSITIVE TERM :: verify domain bridge before reuse")
    return rows[:60]


def _rhetorical_load(text: str, risky: list[str]) -> str:
    if risky:
        return f"overstatement risk via {', '.join(risky)}"
    if len(text) > 300:
        return "high density claim block"
    return "normal"


def _extract_claims(doc_id: str, blocks: list[MarkdownBlock]) -> list[ClaimArch]:
    claims: list[ClaimArch] = []
    for block in blocks:
        if block.block_type not in {"CLAIM", "DOMAIN_SHIFT", "KILL_CONDITION"}:
            continue
        claim_id = stable_uuid("claim", doc_id, block.block_id, block.content_hash)
        claims.append(
            ClaimArch(
                claim_id=claim_id,
                block_id=block.block_id,
                surface_claim=block.text,
                rhetorical_load=_rhetorical_load(block.text, block.overstatement_words),
                domain_shift=len([b for b in block.domain_badges if b != "UNKNOWN"]) > 1,
                domain_badges=block.domain_badges,
            )
        )
    return claims


def _extract_evidence(doc_id: str, blocks: list[MarkdownBlock]) -> list[EvidenceChain]:
    rows: list[EvidenceChain] = []
    for block in blocks:
        cite_list = citations(block.text)
        if block.block_type != "EVIDENCE" and not cite_list:
            continue
        evidence_id = stable_uuid("evidence", doc_id, block.block_id, block.content_hash)
        rows.append(
            EvidenceChain(
                evidence_id=evidence_id,
                block_id=block.block_id,
                primary_source=cite_list[0] if cite_list else None,
                secondary_source=cite_list[1] if len(cite_list) > 1 else None,
                gap="citation present but bridge must be verified" if cite_list else "evidence-like block without formal citation",
                counterevidence_present="however" in block.text.lower() or "but" in block.text.lower(),
            )
        )
    return rows


def _extract_kills(doc_id: str, blocks: list[MarkdownBlock]) -> list[KillArch]:
    rows: list[KillArch] = []
    for block in blocks:
        if block.block_type != "KILL_CONDITION" and not block.overstatement_words:
            continue
        rows.append(
            KillArch(
                repair_item_id=stable_uuid("repair", doc_id, block.block_id, block.content_hash),
                block_id=block.block_id,
                stated_kill=block.text if block.block_type == "KILL_CONDITION" else None,
                rhetorical_armor="overclaim wording needs downgrade" if block.overstatement_words else "explicit test/falsification language present",
            )
        )
    return rows


def _extract_equations(doc_id: str, blocks: list[MarkdownBlock]) -> list[EquationSemantics]:
    rows: list[EquationSemantics] = []
    for block in blocks:
        for index, equation in enumerate(equations(block.text), start=1):
            vars_found = sorted(set(re.findall(r"\b[A-Za-z_]\w*\b", equation)))
            rows.append(
                EquationSemantics(
                    equation_id=stable_uuid("equation", doc_id, block.block_id, str(index), equation),
                    block_id=block.block_id,
                    equation=equation,
                    role="formal expression extracted from Markdown block",
                    status="PROPOSED",
                    undefined_vars=vars_found,
                    derivation_present="derive" in block.text.lower() or "therefore" in block.text.lower(),
                    computable=bool(re.search(r"=", equation)),
                )
            )
    return rows


def _domain_boundaries(blocks: list[MarkdownBlock]) -> list[DomainBoundary]:
    rows: list[DomainBoundary] = []
    for term in DOMAIN_TERMS:
        hits = [block for block in blocks if term in block.text.lower()]
        if not hits:
            continue
        badges = sorted({badge for block in hits for badge in block.domain_badges if badge != "UNKNOWN"})
        rows.append(
            DomainBoundary(
                term=term,
                domain_usage_1=badges[0] if badges else "UNKNOWN",
                domain_usage_2=badges[1] if len(badges) > 1 else None,
                domain_usage_3=badges[2] if len(badges) > 2 else None,
                bridge_present=any("because" in block.text.lower() or "therefore" in block.text.lower() for block in hits),
                bridge_quality="rule-detected bridge" if len(badges) > 1 else "single-domain or unknown",
                drift_risk="high" if len(badges) > 1 else "normal",
            )
        )
    return rows


def _mechanism_graph(blocks: list[MarkdownBlock]) -> list[MechanismEdge]:
    edges: list[MechanismEdge] = []
    for block in blocks:
        low = block.text.lower()
        for word, relation in RELATION_WORDS.items():
            if word in low:
                left, _, right = block.text.partition(word)
                source = left.strip()[-120:] or block.section_id
                target = right.strip()[:120] or "EXPAND_REQUIRED"
                edges.append(MechanismEdge(source=source, relation=relation, target=target, evidence_block_id=block.block_id))
    return edges[:80]


def _reviewer_seeds(claims: list[ClaimArch], evidence: list[EvidenceChain], domains: list[DomainBoundary]) -> list[ReviewerSeed]:
    weakest = claims[0].surface_claim[:220] if claims else "No explicit claim extracted."
    evidence_gap = evidence[0].gap if evidence else "No evidence bridge extracted."
    drift = next((item.term for item in domains if item.drift_risk == "high"), "domain bridge")
    return [
        ReviewerSeed(reviewer="skeptical_physicist", attack=f"Show why this is not analogy dressed as mechanism: {weakest}", severity="high", repair="Add operational variables, test boundary, and competing explanation."),
        ReviewerSeed(reviewer="academic_philosopher", attack=f"Clarify category movement around {drift}.", severity="medium", repair="State domain badges and bridge type."),
        ReviewerSeed(reviewer="information_theorist", attack="Define signal/noise/information in measurable terms.", severity="medium", repair="Bind information terms to Shannon or explicitly mark analogy."),
        ReviewerSeed(reviewer="methodologist", attack=evidence_gap, severity="high", repair="Add primary source -> tested thing -> claim bridge."),
        ReviewerSeed(reviewer="hostile_critic", attack="Find the strongest overstatement and demand public retraction.", severity="high", repair="Downgrade proof-language to model/evidence language."),
        ReviewerSeed(reviewer="friendly_editor", attack="The structure is promising but needs reader-visible boundaries.", severity="medium", repair="Add labels: derived, interpretive, analogy, empirical."),
    ]


def _grades(claims: list[ClaimArch], evidence: list[EvidenceChain], equations_out: list[EquationSemantics], domains: list[DomainBoundary], risky_words: list[str]) -> tuple[FourScoreDashboard, list[ScoreLedgerEntry]]:
    academic = min(100, 35 + len(evidence) * 8 + len(equations_out) * 4 - len(risky_words) * 3)
    coherence = min(100, 45 + len(claims) * 2 + len(domains) * 3)
    public = min(100, 70 - len(risky_words) * 4)
    risk = min(100, 20 + len(risky_words) * 8 + sum(1 for d in domains if d.drift_risk == "high") * 8)

    def letter(score: int, risk_mode: bool = False) -> str:
        if risk_mode:
            return "LOW" if score < 30 else "MEDIUM" if score < 65 else "HIGH"
        return "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"

    dashboard = FourScoreDashboard(
        Academic_Readiness=Grade(score=academic, grade=letter(academic), reason="Rule score from evidence/equation coverage minus overstatement.", top_positive=f"{len(evidence)} evidence blocks", top_deduction=f"{len(risky_words)} risky words", fix_to_improve="Add explicit evidence bridges and citations."),
        Framework_Coherence=Grade(score=coherence, grade=letter(coherence), reason="Rule score from claim/domain structure.", top_positive=f"{len(claims)} claim blocks", top_deduction="domain drift requires explicit bridge", fix_to_improve="Add mechanism graph bridge sentences."),
        Public_Communication=Grade(score=public, grade=letter(public), reason="Rule score penalizing overclaim language.", top_positive="Markdown structure is parseable", top_deduction=f"{len(risky_words)} overstatement markers", fix_to_improve="Replace proof-language with bounded model language."),
        Risk=Grade(score=risk, grade=letter(risk, risk_mode=True), reason="Risk increases with overstatement and cross-domain drift.", top_positive="Audit metadata is separated from permanent address", top_deduction="unverified claims may be public-facing", fix_to_improve="Add kill conditions and status labels."),
    )
    ledger = [
        ScoreLedgerEntry(metric="Academic_Readiness", max_points=100, positive_points=academic, deductions=risky_words[:8], evidence_quote=evidence[0].gap if evidence else "No evidence block extracted.", section="global", fix_to_improve="Add source bridges."),
        ScoreLedgerEntry(metric="Framework_Coherence", max_points=100, positive_points=coherence, deductions=["domain drift"] if domains else [], evidence_quote=claims[0].surface_claim[:160] if claims else "No claim extracted.", section="global", fix_to_improve="Add explicit bridge taxonomy."),
        ScoreLedgerEntry(metric="Public_Communication", max_points=100, positive_points=public, deductions=risky_words[:8], evidence_quote=", ".join(risky_words[:8]) or "No risky words found.", section="global", fix_to_improve="Downgrade overclaims."),
        ScoreLedgerEntry(metric="Risk", max_points=100, positive_points=risk, deductions=["higher score means higher risk"], evidence_quote="risk audit metadata, not truth score", section="global", fix_to_improve="Add kill conditions."),
    ]
    return dashboard, ledger


def _eight_gaps(evidence: list[EvidenceChain], domains: list[DomainBoundary], equations_out: list[EquationSemantics], risky_words: list[str]) -> dict[str, GapItem]:
    return {
        "1. Score separation gap": GapItem(status="addressed", why_it_matters="Grade must not become identity.", repair_action="Address and grade are separate fields."),
        "2. Hostile reviewer gap": GapItem(status="partial", why_it_matters="Claims need adversarial pressure.", repair_action="Run LLM reviewer pass over reviewer_seeds."),
        "3. Evidence bridge gap": GapItem(status="partial" if evidence else "open", why_it_matters="Citation is not support unless bridge is explicit.", repair_action="Fill evidence_chain.connection_to_claim."),
        "4. Domain badge gap": GapItem(status="partial" if domains else "open", why_it_matters="Cross-domain claims drift without labels.", repair_action="Verify all domain badges."),
        "5. Score ledger gap": GapItem(status="addressed", why_it_matters="Scores need traceability.", repair_action="Review ledger_schema entries."),
        "6. Equation semantics gap": GapItem(status="partial" if equations_out else "open", why_it_matters="Equations can be formal or rhetorical.", repair_action="Fill derivation and known-theory comparison."),
        "7. Overstatement gap": GapItem(status="open" if risky_words else "addressed", why_it_matters="Public proof-language raises risk.", repair_action="Rewrite high-risk words."),
        "8. Benchmark/risk-context gap": GapItem(status="open", why_it_matters="Scores need calibration against known corpora.", repair_action="Add benchmark set."),
    }


def build_artifact(path: Path, *, vault_id: str, note_version: str = "1", embeddings: str = "none") -> LosslessArtifact:
    frontmatter, markdown = load_markdown(path)
    content_hash = short_hash(markdown, length=64)
    doc_id = file_doc_id(path, content_hash)
    run_id = stable_uuid("run", doc_id, content_hash, note_version)
    audit_snapshot_id = stable_uuid("audit_snapshot", run_id, content_hash)
    embedder = Embedder(embeddings)

    raw_blocks = split_blocks(markdown)
    blocks: list[MarkdownBlock] = []
    all_text = markdown
    for raw in raw_blocks:
        block_type = classify_block(raw["text"])
        block_id = stable_uuid("block", doc_id, str(raw["ordinal"]), raw["content_hash"])
        blocks.append(
            MarkdownBlock(
                block_id=block_id,
                section_id=raw["section_id"],
                heading_path=raw["heading_path"],
                ordinal=raw["ordinal"],
                text=raw["text"],
                block_type=block_type,
                content_hash=raw["content_hash"],
                domain_badges=domain_badges(raw["text"]),
                overstatement_words=overstatement_words(raw["text"]),
                chi_vars=detect_chi_vars(raw["text"]),
                embedding=embedder.embed(raw["text"]),
            )
        )

    entities = [f"{item} :: ENTITY :: extracted-name-or-expression" for item in _entity_candidates(all_text)]
    claim_arch = _extract_claims(doc_id, blocks)
    evidence_chain = _extract_evidence(doc_id, blocks)
    kill_arch = _extract_kills(doc_id, blocks)
    eq_sem = _extract_equations(doc_id, blocks)
    domain_boundary = _domain_boundaries(blocks)
    mechanism_graph = _mechanism_graph(blocks)
    risky = sorted({word for block in blocks for word in block.overstatement_words})
    dashboard, ledger = _grades(claim_arch, evidence_chain, eq_sem, domain_boundary, risky)
    vector = score_vector([block.block_type for block in blocks], len(domain_boundary), len(entities), all_text)

    domain = _frontmatter_value(frontmatter, "domain", "THEOPHYSICS")
    named_entity = slugify(str(frontmatter.get("title") or path.stem)).upper()
    state = str(frontmatter.get("state", "W")).upper()
    access = _frontmatter_value(frontmatter, "access", "AI_RESEARCH")
    use = _frontmatter_value(frontmatter, "use", "R")
    risk = _frontmatter_value(frontmatter, "risk", "R1")
    address, safe_address, hash_value = build_address(domain, named_entity, state, access, use, risk, vector)
    hash_value = hash_value or semantic_hash(vector)
    master_uuid = master_equation_uuid(doc_id, content_hash, address)
    semantic_tags = build_semantic_tags(
        doc_id=doc_id,
        master_uuid=master_uuid,
        address=address,
        vector_string=vector_string(vector),
        semantic_hash=hash_value,
        blocks=blocks,
        claims=claim_arch,
        evidence=evidence_chain,
        kills=kill_arch,
        equations=eq_sem,
        domains=domain_boundary,
        mechanisms=mechanism_graph,
    )

    return LosslessArtifact(
        ids=IdSet(vault_id=vault_id, doc_id=doc_id, note_version=note_version, content_hash=content_hash, run_id=run_id, audit_snapshot_id=audit_snapshot_id),
        master_equation_uuid=master_uuid,
        compression_declaration={
            "scope": str(path),
            "goal": "maximum density with maximum reconstructability",
            "known_limits": "LLM-only fields marked EXPAND_REQUIRED; deterministic extraction is conservative.",
            "reconstruction_confidence": "medium-high for structure; medium for buried claims until LLM pass.",
        },
        address=address,
        filename_safe_address=safe_address,
        semantic_vector=vector,
        vector_string=vector_string(vector),
        hash=hash_value,
        spine=_spine(blocks),
        entities=entities,
        semantics=_semantics(blocks),
        blocks=blocks,
        claim_arch=claim_arch,
        evidence_chain=evidence_chain,
        kill_arch=kill_arch,
        eq_sem=eq_sem,
        domain_boundary=domain_boundary,
        mechanism_graph=mechanism_graph,
        reviewer_seeds=_reviewer_seeds(claim_arch, evidence_chain, domain_boundary),
        overstate_pattern={
            "high_risk_words": [word for word in risky if word in {"proves", "mathematically proven", "undeniable", "impossible", "refuted", "destroyed", "only", "definitive", "settled"}],
            "medium_risk_words": [word for word in risky if word not in {"proves", "mathematically proven", "undeniable", "impossible", "refuted", "destroyed", "only", "definitive", "settled"}],
            "safe_rewrite": "Replace proof-language with bounded model/evidence language.",
            "detection_rule": "case-insensitive keyword scan over blocks",
        },
        ledger_schema=ledger,
        four_score_dashboard=dashboard,
        cross_dep={"paper_id": frontmatter.get("paper_id", "UNKNOWN"), "depends_on": [], "enables": [], "shared_claims_with": [], "term_drift_flags": [item.term for item in domain_boundary if item.drift_risk == "high"], "orphan_risk": "UNKNOWN"},
        eight_gaps=_eight_gaps(evidence_chain, domain_boundary, eq_sem, risky),
        semantic_tags=semantic_tags,
        semantic_tag_markdown=render_semantic_tag_markdown(semantic_tags),
        seed_bank={"writing": [], "code": ["LLM fill pass for EXPAND_REQUIRED fields"], "research": [], "tests": ["reconstruction test"], "diagrams": ["mechanism graph"], "prompts": ["hostile reviewer fill pass"], "filenames": [safe_address + ".json"], "public_language": ["This is an audit snapshot, not a truth verdict."]},
        open_threads=[f"{item} :: LAST_STATE unresolved :: NEXT_ACTION fill by LLM or reviewer" for item in ["buried_claim", "evidence_bridge", "implicit_kill", "known_theory_comparison"]],
        decompress=[
            "Decode ADDRESS.",
            "Expand VECTOR and HASH.",
            "Read SPINE first.",
            "Rebuild ENTITIES.",
            "Apply SEMANTICS.",
            "Reconstruct CLAIM_ARCH and MECHANISM_GRAPH.",
            "Check EVIDENCE_CHAIN and KILL_ARCH.",
            "Preserve OPEN_THREADS.",
            "Use SEED_BANK to continue work.",
            "Do not replace the user's framework with generic interpretation.",
            "Separate formal proof, structural support, empirical evidence, and interpretation.",
            "Mark missing material as EXPAND_REQUIRED.",
        ],
        check={
            "included_threads": len(blocks),
            "missing_threads": ["LLM-only fields"] if any("EXPAND_REQUIRED" in item.model_dump_json() for item in claim_arch + evidence_chain + kill_arch + eq_sem) else [],
            "ambiguity_flags": [item.term for item in domain_boundary if item.drift_risk == "high"],
            "compression_loss_risk": "medium",
            "reconstruction_confidence": "medium-high",
            "decision_count": len([block for block in blocks if block.block_type == "KILL_CONDITION"]),
            "entity_count": len(entities),
            "claim_count": len(claim_arch),
            "equation_count": len(eq_sem),
            "open_thread_count": 4,
        },
        recovery_key=recovery_key(address, content_hash),
    )


def artifact_to_json(artifact: LosslessArtifact) -> str:
    return json.dumps(artifact.model_dump(mode="json"), ensure_ascii=False, indent=2)
