"""
7Q Backward Mode — Destruction / Reverse Proof.

Takes an existing claim or paper and runs Q7→Q1.
Identity is EARNED, not assumed. Whatever survives gets tagged.

David Lowe | POF 2828 | March 2026
"""

import sys
from typing import List, Optional
from scorer import (
    ClaimProfile, EvidenceItem, PredictionItem, DeathTest,
    compute_truth_score, score_summary, machine_block,
)
from id_system import (
    DOMAINS,
    Q0_MODE, Q1_ENTITY_TYPE, Q1_AXIOM_CLASS, Q1_STATUS, Q1_SOURCE,
    Q2_SCALE, Q2_ISO_STATUS, Q2_CROSS_DOMAIN_MULTIPLIER,
    Q3_CLAIM_TYPE, Q3_PRECISION, Q3_CERTAINTY, Q3_SCOPE,
    Q4_EVIDENCE_TYPE, Q4_TIER, Q4_STRENGTH, Q4_LINKAGE, Q4_VULNERABILITIES,
    Q5_TERMINUS, Q5_DERIVATION,
    Q6_PREDICTION_TYPE, Q6_COMPETING,
    Q7_DEATH_TYPES, Q7_DEATH_RESULT, Q7_ROBUSTNESS, Q7_CASCADE_SCOPE,
)
from intake import (
    banner, show_options, pick_one, pick_many,
    ask_float, ask_yn, ask_text,
)


# ═══════════════════════════════════════════════
# DESTRUCTION PHASES
# ═══════════════════════════════════════════════

def phase_ingest(profile: ClaimProfile):
    """Phase 0: Ingest the claim/paper."""
    banner("PHASE 0 — INGEST")
    print("  Feed in the claim or paper to be destroyed.\n")
    profile.claim_text = ask_text("Claim / paper title")
    profile.claim_id = ask_text("Claim ID (e.g. CL-PHY-0001)", f"CL-{profile.domain}-0001")
    profile.domain = pick_one("Domain", DOMAINS, show_weights=False)
    profile.mode = "INVEST"  # Destruction mode is always investigation


def phase_q7_kill(profile: ClaimProfile) -> bool:
    """
    Phase 1: Q7 — Try to KILL it first.

    Run all five death types. If anything kills it, record it.
    Return True if claim survived all tests.
    """
    banner("PHASE 1 — Q7: FALSIFICATION (Kill Attempt)")
    print("  Try every death type. Be adversarial. Be hostile.\n")

    killed = False
    for key, entry in Q7_DEATH_TYPES.items():
        print(f"\n  ═══ DEATH TYPE: {key} ═══")
        print(f"  {entry['label']}")
        print()

        # Guided destruction questions
        prompts = {
            "SELFREF":    "Does the claim, if true, undermine or contradict itself?",
            "REGRESS":    "Does the justification require an infinite chain of prior justifications?",
            "EMPIRICAL":  "Does ANY existing observation or experiment directly contradict this?",
            "INCOHERENT": "Does the claim contain a logical contradiction (A and ¬A)?",
            "EXPLAIN":    "Does a simpler, existing theory explain the same data better?",
        }
        print(f"  → {prompts.get(key, 'Apply this death test.')}\n")

        notes = ask_text("Evidence for/against (describe)")
        result = pick_one("Verdict", Q7_DEATH_RESULT, show_weights=False)

        profile.death_tests.append(DeathTest(death_type=key, result=result, notes=notes))

        if result == "DIES":
            killed = True
            print(f"\n  ☠☠☠ CLAIM KILLED BY {key} ☠☠☠")
            print(f"  Reason: {notes}")
            if not ask_yn("Continue destruction anyway (record all damage)?"):
                break

    if not killed:
        print("\n  ✓ Claim SURVIVED all five death types.")

    print("\n  Overall robustness assessment:")
    profile.robustness = pick_one("Robustness", Q7_ROBUSTNESS)
    profile.cascade_scope = pick_one("If it dies, cascade scope", Q7_CASCADE_SCOPE)

    return not killed


def phase_q6_predictions(profile: ClaimProfile):
    """Phase 2: Q6 — What does it predict? Does it actually predict anything unique?"""
    banner("PHASE 2 — Q6: CONSEQUENCES (What does it predict?)")
    print("  A claim that predicts nothing discriminating is barely alive.\n")

    idx = 1
    while True:
        desc = ask_text(f"Prediction #{idx} (or 'done')")
        if desc.lower() == "done":
            break

        pred = PredictionItem(description=desc)
        pred.pred_type = pick_one("Type", Q6_PREDICTION_TYPE)
        pred.competing = pick_one("How unique? (competing models)", Q6_COMPETING)
        pred.confirmed = ask_yn("Already confirmed?")

        profile.predictions.append(pred)
        idx += 1

    if not profile.predictions:
        print("  ⚠ No predictions. D score will be 0.")
        print("  → This is a major weakness. Claims that predict nothing are hard to support.")


def phase_q5_dependencies(profile: ClaimProfile):
    """Phase 3: Q5 — Trace the dependency chain. Where does it bottom out?"""
    banner("PHASE 3 — Q5: DEPENDENCIES (What does it rest on?)")
    print("  Follow the chain DOWN. Where does justification terminate?\n")

    profile.terminus = pick_one("Terminus type", Q5_TERMINUS)
    profile.derivation = pick_one("Derivation method", Q5_DERIVATION)

    print("\n  List key dependencies (the things this REQUIRES to be true):")
    print("  (one per line, blank to stop)")
    while True:
        dep = ask_text("  Dependency")
        if not dep:
            break
        profile.dependency_chain.append(dep)


def phase_q4_evidence(profile: ClaimProfile):
    """Phase 4: Q4 — Evaluate evidence. Be skeptical."""
    banner("PHASE 4 — Q4: EVIDENCE (What actually supports it?)")
    print("  List ONLY genuine evidence. Be harsh. Decorative doesn't count.\n")

    idx = 1
    while True:
        name = ask_text(f"Evidence #{idx} (or 'done')")
        if name.lower() == "done":
            break

        ev = EvidenceItem(name=name)
        ev.evidence_type = pick_one("Type", Q4_EVIDENCE_TYPE)
        ev.tier = pick_one("Tier", Q4_TIER)
        ev.strength = pick_one("Strength", Q4_STRENGTH)
        ev.linkage = pick_one("Linkage to claim", Q4_LINKAGE)
        ev.ps_raw = ask_float("PS (0-1, 0=auto)", 0.0)
        ev.ed = ask_float("ED (Explanatory Depth 0-1)", 0.5)
        ev.ec = ask_float("EC (Epistemic Completeness 0-1)", 0.5)

        print("\n  Check for vulnerabilities (be honest):")
        ev.vulnerabilities = pick_many("Vulnerabilities", Q4_VULNERABILITIES)

        profile.evidence.append(ev)
        idx += 1


def phase_q3_assertion(profile: ClaimProfile):
    """Phase 5: Q3 — Classify the assertion itself."""
    banner("PHASE 5 — Q3: ASSERTION (What is it actually saying?)")
    print("  Now that you've tested it, classify what the claim actually says.\n")

    profile.claim_type = pick_one("Claim type", Q3_CLAIM_TYPE)
    profile.precision = pick_one("Precision", Q3_PRECISION)
    profile.certainty = pick_one("Certainty", Q3_CERTAINTY)
    profile.scope = pick_one("Scope", Q3_SCOPE)


def phase_q2_location(profile: ClaimProfile):
    """Phase 6: Q2 — Where does it live? Cross-domain check."""
    banner("PHASE 6 — Q2: LOCATION (Cross-Domain Check)")
    print("  After destruction, which domains does this claim actually appear in?\n")

    profile.scales = pick_many("Scale(s)", Q2_SCALE)
    profile.domains_present = pick_many("Domains where the claim has structural presence", DOMAINS)

    n = len(profile.domains_present)
    if n >= 2:
        profile.iso_status = pick_one("ISO status between domains", Q2_ISO_STATUS, show_weights=False)
        if profile.iso_status == "CONFIRMED":
            profile.cross_domain_key = "ISO3+" if n >= 3 else "ISO2"
        elif profile.iso_status == "PARALLEL":
            profile.cross_domain_key = "PAR3+" if n >= 3 else "PAR2"
        else:
            profile.cross_domain_key = "ANA"
    else:
        profile.iso_status = "BOUND"
        profile.cross_domain_key = "BOUND"

    xdm = Q2_CROSS_DOMAIN_MULTIPLIER.get(profile.cross_domain_key, {})
    print(f"\n  Cross-domain multiplier: {profile.cross_domain_key} → ×{xdm.get('multiplier', 1.0):.2f}")


def phase_q1_identity(profile: ClaimProfile):
    """
    Phase 7: Q1 — EARN the identity.

    In backward mode, identity is the LAST thing assigned.
    Only after everything else is tested do you get to say what it IS.
    """
    banner("PHASE 7 — Q1: IDENTITY (Earned, Not Assumed)")
    print("  Based on everything above, what has this claim EARNED the right to be?")
    print("  Don't inflate. A hypothesis that survived isn't automatically a law.\n")

    profile.entity_type = pick_one("Entity type (EARNED)", Q1_ENTITY_TYPE)
    profile.axiom_class = pick_one("Axiom class", Q1_AXIOM_CLASS)
    profile.status = pick_one("Status", Q1_STATUS)
    profile.source = pick_one("Source", Q1_SOURCE)


# ═══════════════════════════════════════════════
# MAIN BACKWARD DESTRUCTION
# ═══════════════════════════════════════════════

def run_backward_destruction() -> tuple:
    """
    Run the full backward destruction Q7→Q1.
    Returns (ClaimProfile, ScoreResult).
    """
    banner("7Q REVERSE PROOF — Destruction Mode")
    print("  Feed in a claim. We try to kill it. Whatever survives gets scored.")
    print("  Identity is EARNED at the end, not assumed at the start.")
    print("  Direction: Q7 → Q6 → Q5 → Q4 → Q3 → Q2 → Q1\n")

    profile = ClaimProfile()

    # Phase 0: Ingest
    phase_ingest(profile)

    # Phase 1: Q7 — Kill attempt
    survived = phase_q7_kill(profile)

    if not survived:
        print("\n  The claim was killed. Continuing to document the corpse...\n")

    # Phase 2-7: Q6→Q1
    phase_q6_predictions(profile)
    phase_q5_dependencies(profile)
    phase_q4_evidence(profile)
    phase_q3_assertion(profile)
    phase_q2_location(profile)
    phase_q1_identity(profile)

    # Score
    banner("DESTRUCTION REPORT — FINAL SCORE")
    result = compute_truth_score(profile)

    if not survived:
        print("  ☠ NOTE: This claim was KILLED during Q7. Score reflects the damage.\n")

    print(score_summary(result))
    print()
    print(machine_block(profile, result))

    return profile, result


if __name__ == "__main__":
    profile, result = run_backward_destruction()
