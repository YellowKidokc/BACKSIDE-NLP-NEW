"""Build a sample snapshot JSON for HTML report sanity testing.

Run: python 11_HTML_REPORT/_test_fixture.py
Then: python 11_HTML_REPORT/generate_report.py --json 11_HTML_REPORT/_fixture_snapshot.json
"""
import json
from pathlib import Path
import sys

# Make lib importable when run from repo root or this folder
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from lib.snapshot_schema import (
    ProofExplorerSnapshot, PaperIdentity, Thesis, Claim, EquationEntry,
    AssumptionStack, KillCondition, EvidenceEntry, PhysicsComparison,
    NoveltyClassification, CoherenceScore, OverstatementDetector, RevisionPlan,
)

snap = ProofExplorerSnapshot(
    paper_id="FP-005",
    identity=PaperIdentity(
        paper_id="FP-005",
        title="The Turtles and the Floor",
        author="David Lowe",
        version="1.0",
        date="2026-04-26",
        series="Foundational Papers",
        domain="theology-physics-bridge",
        paper_type=["framework", "philosophical"],
    ),
    thesis=Thesis(
        one_sentence="A composition of four known physical operations produces a transition sequence with candidate structural correspondence to the Incarnation-Crucifixion-Resurrection-Pentecost sequence.",
        ai_confidence="medium",
    ),
    claim_inventory=[
        Claim(claim="Closed systems cannot ground themselves",
              claim_type="mathematical", importance="core",
              evidence_present=True, testability="partial", risk_level="low",
              needs_citation=False,
              notes="Anchored in Gödel + Turing + Shannon convergence."),
        Claim(claim="The Cross satisfies all four CPT-symmetry constraints uniquely",
              claim_type="metaphysical", importance="core",
              evidence_present=False, testability="no", risk_level="high",
              needs_citation=True,
              notes="Strongest interpretive claim; lacks formal derivation."),
        Claim(claim="τ_lock = 33 years derivable from coupling constants",
              claim_type="physical", importance="core",
              evidence_present=False, testability="yes", risk_level="high",
              needs_citation=False,
              notes="Open Problem 2 — decisive."),
        Claim(claim="Eden cherubim corresponds to no-cloning theorem",
              claim_type="analogy", importance="rhetorical",
              evidence_present=False, testability="no", risk_level="medium",
              needs_citation=True,
              notes="Structural analogy; framework explicitly does not claim isomorphism."),
    ],
    equations=[
        EquationEntry(
            equation="g_L(s,X) = κ · I_A(s; M_X) · Φ_X",
            purpose="Resonant coupling between input structure and target system",
            variables_defined=True,
            variable_definitions={"κ": "Universal coupling constant", "I_A": "Algorithmic mutual info", "Φ_X": "System susceptibility"},
            dimensional_status="defined", operational_status="computable", role="doing_work",
            issues=[],
        ),
        EquationEntry(
            equation="ΔO ≈ g_L(s,X) · S_X",
            purpose="General observable prediction",
            variables_defined=True, variable_definitions={"S_X": "system response"},
            dimensional_status="defined", operational_status="computable", role="predictive",
            issues=[],
        ),
        EquationEntry(
            equation="□(QM ⊨ ⊤ → ∃O_∞ : Φ(O_∞) = ∞)",
            purpose="Necessity of Terminal Observer in modal logic",
            variables_defined=False, variable_definitions={},
            dimensional_status="not_applicable", operational_status="symbolic", role="structural",
            issues=["Missing operational definition of Φ at infinity"],
        ),
    ],
    assumptions=AssumptionStack(
        explicit=["Quantum mechanics is true", "Well-foundedness of grounding relation"],
        implicit=["Personal terminal observer is identical to classical theism's God"],
        imported=["von Neumann measurement formalism", "Tononi IIT (Φ as integration)"],
        theological=["Trinity is a non-derived primitive", "Cross is a unique CPT counter-move"],
        scientific=["Standard Model holds", "Decoherence is real but insufficient"],
        philosophical=["Self-refutation is a valid termination criterion"],
        measurement=["Φ is in-principle measurable for finite systems"],
        causal=[],
    ),
    kill_conditions=[
        KillCondition(claim="SSB-irreversibility composition holds",
                      kill_condition="SSB reversible in infinite-volume limit",
                      test_method="QFT calculation", severity="fatal", current_status="open"),
        KillCondition(claim="Energy conservation across full arc",
                      kill_condition="Energy non-conserved across full arc",
                      test_method="Thermodynamic audit", severity="fatal", current_status="strong"),
        KillCondition(claim="τ_lock derivability",
                      kill_condition="τ_lock derivation ≠ 33 years",
                      test_method="Coupling constant calc", severity="fatal", current_status="unresolved"),
        KillCondition(claim="EM invisibility",
                      kill_condition="Coupling produces EM signature",
                      test_method="Direct detection", severity="fatal", current_status="weak"),
        KillCondition(claim="Historical fit",
                      kill_condition="Historical record contradicts P1",
                      test_method="Sociological analysis", severity="wounding", current_status="strong"),
    ],
    evidence_map=[
        EvidenceEntry(claim="Closed systems cannot ground themselves",
                      supporting_evidence="Gödel (1931), Turing (1936), Chaitin (1975), Landauer (1961)",
                      evidence_type="primary", evidence_quality="strong",
                      counterevidence_needed="Constructive grounding without external input",
                      gap=""),
        EvidenceEntry(claim="Human intent measurably affects physical systems",
                      supporting_evidence="PEAR-LAB 2.5M trials at 6.35σ; GCP 325+ replications at 6σ",
                      evidence_type="secondary", evidence_quality="moderate",
                      counterevidence_needed="Pre-registered replication outside PEAR/GCP communities",
                      gap="Replication crisis context not addressed"),
        EvidenceEntry(claim="τ_lock = 33 years",
                      supporting_evidence="Historical anchor only",
                      evidence_type="interpretive", evidence_quality="weak",
                      counterevidence_needed="First-principles derivation",
                      gap="No mechanism proposed for the specific value"),
    ],
    physics_comparison=[
        PhysicsComparison(
            nearest_theory="Penrose Orchestrated Objective Reduction",
            similarity="Both posit consciousness as fundamental to measurement.",
            difference="Penrose locates collapse in microtubules; this paper locates it in the terminal observer.",
            does_paper_outperform="unclear",
            category_confusion_risk="Penrose is physicalist; this is dualist — comparison risks category drift.",
        ),
        PhysicsComparison(
            nearest_theory="Wheeler Participatory Universe",
            similarity="It-from-bit, observation as creation",
            difference="Wheeler doesn't terminate the regress; BC1 does.",
            does_paper_outperform="yes",
            category_confusion_risk="",
        ),
    ],
    novelty=NoveltyClassification(
        novelty_levels=["new_framing", "new_derivation"],
        primary_novelty="Identification of the von Neumann fixed point with classical theism's God",
        overstated_novelty_flags=["'six theorems prove grace' — the convergence is suggestive, not a single theorem"],
        honest_label="Framework paper with one new structural argument and several plausible analogies",
    ),
    coherence=CoherenceScore(
        definition_clarity=7, equation_coherence=6, claim_discipline=5,
        scope_control=6, falsifiability=8, citation_adequacy=4,
        domain_separation=7, reader_burden=6,
        review_readiness=58, ai_confidence="medium",
    ),
    overstatement=OverstatementDetector(
        overstated_passages=[
            "\"The data is in. The math is done.\" — overstates the maturity of the formal work; RCH calibration ladder is not yet executed.",
            "\"Six theorems that accidentally proved Grace\" — six convergent theorems do not prove grace; they motivate it.",
        ],
        rhetorical_strength_index=0.78,
        evidence_strength_index=0.42,
        delta=0.36,
        severity="moderate",
    ),
    revision=RevisionPlan(
        strongest_part="Falsifiability discipline in RCH section; explicit STOP conditions in the four-rung ladder.",
        weakest_part="The compressed identification of the von Neumann fixed point with the personal God of classical theism — the math gives you a self-grounding observer, not personhood.",
        must_fix_before_publication=[
            "Separate the fixed-point existence claim from the personhood claim and treat them as distinct propositions.",
            "Provide a first-principles derivation candidate for τ_lock, even if speculative.",
            "Tone down 'proven' / 'mathematically necessary' to 'structurally required under stated assumptions'.",
        ],
        best_next_test="Run Rung A of the RCH calibration ladder on synthetic baselines; report whether the monotonic trend holds.",
        needs_expert_review=["philosophy of religion", "QFT", "philology"],
    ),
    pipeline_metrics={
        "file": "FP-005.md",
        "analyzed_at": "2026-04-29T15:00:00",
        "schema_version": "1.0.0",
        "L1_word_count": 4200,
        "L1_text_standard": "11th-12th grade",
        "L1_keybert_keywords": "logos | terminal observer | resonant coupling | grace | participatory",
        "L2_academic_grade": "B+",
        "L3_chi_score": 7.2, "L3_chi_status": "Coherent",
        "L3_ckg_tier": "Tier 2 — Sourced",
        "L3_me_G_gravity_belonging": 0.6, "L3_me_M_mass_meaning": 0.7,
        "L3_me_E_entropy_engagement": 0.5, "L3_me_S_spacetime_structure": 0.4,
        "L3_me_T_time_eternity": 0.55, "L3_me_K_knowledge_logos": 0.8,
        "L3_me_R_relationship": 0.65, "L3_me_Q_quantum_observer": 0.85,
        "L3_me_F_faith_coupling": 0.7, "L3_me_C_christ_coherence": 0.75,
        "L5_entity_people": "Wheeler, von Neumann, Gödel, Tononi",
        "L5_entity_orgs": "PEAR, GCP",
        "L5_entity_count": 12, "L5_entity_types_found": "PERSON, ORG, WORK_OF_ART",
        "L6_truth_score": 7.0, "L6_coherence_score": 0.71, "L6_combined_score": 6.85,
        "L6_claim_count": 14, "L6_contradiction_flags": 1, "L6_evidence_density": 0.42,
        "L6_anchored_claims": 6, "L6_under_supported_claims": 4,
        "L6_overstated_claims": 2, "L6_falsifiable_claims": 5, "L6_speculative_claims": 3,
        "L6_character_posture": "Investigative — doctrinally bold but methodologically cautious",
        "L6_integrity_profiles": "Self-flags speculative claims with bridge conditions; uses 'candidate' rather than 'proven'.",
        "L6_fruit_love": 0.18, "L6_fruit_joy": 0.12, "L6_fruit_peace": 0.10,
        "L6_fruit_patience": 0.08, "L6_fruit_kindness": 0.09, "L6_fruit_goodness": 0.14,
        "L6_fruit_faithfulness": 0.21, "L6_fruit_gentleness": 0.07, "L6_fruit_self_control": 0.16,
        "L7_centrality_within_series": "0.82 (hub)", "L7_cluster": "Foundational",
        "L8_fruit_emo_net": 0.45, "L8_emo_dominant": "curiosity",
        "L8_emo_top_5": "curiosity, awe, conviction, gratitude, resolve",
        "L8_fruit_emo_love": 0.55, "L8_fruit_emo_joy": 0.38,
        "L8_fruit_emo_peace": 0.42, "L8_fruit_emo_patience": 0.30,
        "L8_fruit_emo_kindness": 0.35, "L8_fruit_emo_goodness": 0.48,
        "L8_fruit_emo_faithfulness": 0.62, "L8_fruit_emo_gentleness": 0.28,
        "L8_fruit_emo_self_control": 0.41,
        "L8_anti_emo_hatred": 0.02, "L8_anti_emo_despair": 0.03,
        "L8_emo_admiration": 0.35, "L8_emo_curiosity": 0.62, "L8_emo_gratitude": 0.28,
        "L8_emo_realization": 0.41, "L8_emo_optimism": 0.33,
        "L8_nrc_joy": 0.45, "L8_nrc_trust": 0.62, "L8_nrc_anticipation": 0.55,
        "L8_nrc_top_emotions": "trust, anticipation, joy, surprise",
        "L9_lr_mtld": 92,
        "L10_idea_density_mean": 0.51, "L10_idea_density_level": "Above average",
        "_layer_status": {"L1": "ok", "L2": "ok", "L3": "ok", "L4": "skipped",
                          "L5": "ok", "L6": "ok", "L7": "ok", "L8": "ok",
                          "L9": "ok", "L10": "ok", "L13_peer_review": "ok"},
    },
)

# Also build an empty-snapshot fixture to test graceful fallback
empty = ProofExplorerSnapshot(
    paper_id="EMPTY-DEMO",
    identity=PaperIdentity(paper_id="EMPTY-DEMO", title="Empty Snapshot Demo"),
    pipeline_metrics={"file": "EMPTY-DEMO.md",
                      "analyzed_at": "2026-04-29T15:00:00",
                      "schema_version": "1.0.0",
                      "L1_word_count": 0,
                      "_layer_status": {"L13_peer_review": "skipped"}},
)

out = _HERE / "_fixture_snapshot.json"
out.write_text(json.dumps([snap.to_dict(), empty.to_dict()], indent=2), encoding='utf-8')
print(f"Wrote {out}")
print(f"  - 1 fully-populated snapshot (FP-005)")
print(f"  - 1 empty snapshot (EMPTY-DEMO) for fallback testing")
