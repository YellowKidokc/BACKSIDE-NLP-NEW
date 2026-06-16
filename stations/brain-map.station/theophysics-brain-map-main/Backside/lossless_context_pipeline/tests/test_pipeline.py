from pathlib import Path

from Backside.lossless_context_pipeline.pipeline import build_artifact
from Backside.lossless_context_pipeline.address import score_vector, vector_string
from Backside.lossless_context_pipeline.vector_space import artifact_text


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "samples" / "sample_article.md"


def test_build_artifact_has_required_ids_and_address():
    artifact = build_artifact(SAMPLE, vault_id="test-vault", embeddings="none")

    assert artifact.ids.vault_id == "test-vault"
    assert artifact.ids.doc_id
    assert artifact.ids.run_id
    assert artifact.ids.audit_snapshot_id
    assert " :: " in artifact.address
    assert artifact.vector_string.startswith("G")
    assert artifact.recovery_key.startswith("LCC-")


def test_extracts_core_protocol_objects():
    artifact = build_artifact(SAMPLE, vault_id="test-vault", embeddings="none")

    assert artifact.blocks
    assert artifact.claim_arch
    assert artifact.evidence_chain
    assert artifact.kill_arch
    assert artifact.eq_sem
    assert artifact.domain_boundary
    assert artifact.mechanism_graph
    assert artifact.four_score_dashboard.Academic_Readiness.score >= 0
    assert "7. Overstatement gap" in artifact.eight_gaps


def test_stable_ids_for_same_content():
    first = build_artifact(SAMPLE, vault_id="test-vault", embeddings="none")
    second = build_artifact(SAMPLE, vault_id="test-vault", embeddings="none")

    assert first.ids.doc_id == second.ids.doc_id
    assert first.ids.content_hash == second.ids.content_hash
    assert [b.block_id for b in first.blocks] == [b.block_id for b in second.blocks]


def test_protocol_like_artifact_scores_authority_trust_and_coherence():
    text = "Protocol rule: reconstruct a self-contained artifact. Required fields must preserve audit confidence and risk."
    vector = score_vector(["CLAIM", "EQUATION", "DOMAIN_SHIFT"], domain_count=2, entity_count=4, text=text)

    assert vector_string(vector) == "G3M3E0S0T3K3R3Q0F3C3"


def test_entropy_topic_does_not_force_artifact_entropy():
    text = "This orderly article discusses entropy, collapse, risk, coherence, and kill conditions with clear sections."
    vector = score_vector(["CLAIM", "KILL_CONDITION", "DOMAIN_SHIFT"], domain_count=3, entity_count=4, text=text)

    assert vector["E"] == 0


def test_checklist_scores_structured_knowledge_without_equations():
    text = "Final checklist: confirm aircraft identity, verify fuel level, inspect engine status, review emergency procedures."
    vector = score_vector(["KILL_CONDITION", "OTHER"], domain_count=1, entity_count=2, text=text)

    assert vector["K"] == 3


def test_audience_frontmatter_aliases_to_access(tmp_path):
    md = tmp_path / "pilot.md"
    md.write_text(
        """---
title: Pilot
domain: AVIATION
state: F
audience: TEAM
risk: R4
---

# Pilot

The checklist must be completed in order.
""",
        encoding="utf-8",
    )
    artifact = build_artifact(md, vault_id="test-vault", embeddings="none")

    assert "/TEAM/" in artifact.address


def test_artifact_text_contains_claims_for_projection():
    artifact = build_artifact(SAMPLE, vault_id="test-vault", embeddings="none")
    text = artifact_text(artifact.model_dump(mode="json"))

    assert artifact.address in text
    assert "grace" in text.lower()
