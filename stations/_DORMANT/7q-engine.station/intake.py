"""
7Q Forward Mode — Interactive intake Q&A.

Walks the user through Q0→Q7, collects classifications,
builds a ClaimProfile, scores it, and returns the result.

David Lowe | POF 2828 | March 2026
"""

import sys
from typing import List
from scorer import (
    ClaimProfile, EvidenceItem, PredictionItem, DeathTest,
    compute_truth_score, score_summary, machine_block,
)
from id_system import (
    OBJECT_TYPES, DOMAINS,
    Q0_MODE, Q1_ENTITY_TYPE, Q1_AXIOM_CLASS, Q1_STATUS, Q1_SOURCE,
    Q2_SCALE, Q2_ISO_STATUS, Q2_CROSS_DOMAIN_MULTIPLIER,
    Q3_CLAIM_TYPE, Q3_PRECISION, Q3_CERTAINTY, Q3_SCOPE,
    Q4_EVIDENCE_TYPE, Q4_TIER, Q4_STRENGTH, Q4_LINKAGE, Q4_VULNERABILITIES,
    Q5_TERMINUS, Q5_DERIVATION,
    Q6_PREDICTION_TYPE, Q6_COMPETING,
    Q7_DEATH_TYPES, Q7_DEATH_RESULT, Q7_ROBUSTNESS, Q7_CASCADE_SCOPE,
)


# ═══════════════════════════════════════════════
# DISPLAY HELPERS
# ═══════════════════════════════════════════════

def banner(text: str):
    width = 55
    print()
    print("═" * width)
    print(f"  {text}")
    print("═" * width)


def show_options(registry: dict, show_weights: bool = True):
    """Print numbered options from a registry dict."""
    keys = list(registry.keys())
    for i, key in enumerate(keys, 1):
        entry = registry[key]
        label = entry.get("label", entry) if isinstance(entry, dict) else entry
        weight = entry.get("weight", "") if isinstance(entry, dict) else ""
        if show_weights and weight != "":
            print(f"  [{i:2d}] {key:16s} — {label}  (w={weight})")
        else:
            print(f"  [{i:2d}] {key:16s} — {label}")
    return keys


def pick_one(prompt: str, registry: dict, show_weights: bool = True) -> str:
    """Show options, get user's pick, return the key."""
    keys = show_options(registry, show_weights)
    while True:
        raw = input(f"\n  {prompt} [1-{len(keys)}]: ").strip()
        if raw.upper() in keys:
            return raw.upper()
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(keys):
                return keys[idx]
        except ValueError:
            pass
        print("  → Invalid. Try again.")


def pick_many(prompt: str, registry: dict) -> List[str]:
    """Show options, let user pick multiple (comma-separated)."""
    keys = show_options(registry, show_weights=False)
    raw = input(f"\n  {prompt} (comma-sep, e.g. 1,3,5): ").strip()
    if not raw:
        return []
    result = []
    for part in raw.split(","):
        part = part.strip()
        if part.upper() in keys:
            result.append(part.upper())
        else:
            try:
                idx = int(part) - 1
                if 0 <= idx < len(keys):
                    result.append(keys[idx])
            except ValueError:
                pass
    return result


def ask_float(prompt: str, default: float = 0.0) -> float:
    raw = input(f"  {prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return max(0.0, min(1.0, float(raw)))
    except ValueError:
        return default


def ask_yn(prompt: str, default: bool = False) -> bool:
    d = "Y/n" if default else "y/N"
    raw = input(f"  {prompt} [{d}]: ").strip().lower()
    if not raw:
        return default
    return raw.startswith("y")


def ask_text(prompt: str, default: str = "") -> str:
    raw = input(f"  {prompt}: ").strip()
    return raw if raw else default


# ═══════════════════════════════════════════════
# INTAKE STEPS
# ═══════════════════════════════════════════════

def step_baseline(profile: ClaimProfile):
    """Step 0: Domain and claim text."""
    banner("STEP 0 — BASELINE")
    print("  What domain is this claim in?")
    profile.domain = pick_one("Domain", DOMAINS, show_weights=False)
    profile.claim_text = ask_text("State the claim in one sentence")
    profile.claim_id = ask_text("Claim ID (e.g. CL-PHY-0001)", f"CL-{profile.domain}-0001")


def step_q0(profile: ClaimProfile):
    """Q0: Posture — why are you here?"""
    banner("Q0 — POSTURE")
    print("  Are you genuinely investigating, or advocating?")
    profile.mode = pick_one("Mode", Q0_MODE)


def step_q1(profile: ClaimProfile):
    """Q1: Identity — what IS this thing?"""
    banner("Q1 — IDENTITY")
    print("  What kind of entity is this claim?")
    profile.entity_type = pick_one("Entity type", Q1_ENTITY_TYPE)

    print("\n  What axiom class?")
    profile.axiom_class = pick_one("Axiom class", Q1_AXIOM_CLASS)

    print("\n  Current status?")
    profile.status = pick_one("Status", Q1_STATUS)

    print("\n  Source of the claim?")
    profile.source = pick_one("Source", Q1_SOURCE)


def step_q2(profile: ClaimProfile):
    """Q2: Location — where does it live? Cross-domain analysis."""
    banner("Q2 — LOCATION (Cross-Domain Analysis)")
    print("  What scale(s) does this claim operate at?")
    profile.scales = pick_many("Scale(s)", Q2_SCALE)

    print("\n  Which domains does this claim appear in?")
    profile.domains_present = pick_many("Domains present", DOMAINS)

    n_domains = len(profile.domains_present)
    if n_domains >= 3:
        print(f"\n  → {n_domains} domains! Checking isomorphism status...")
        print("  Is the structural mapping confirmed (same equations) or just parallel?")
        profile.iso_status = pick_one("ISO status", Q2_ISO_STATUS, show_weights=False)
        # Auto-suggest cross-domain multiplier
        if profile.iso_status == "CONFIRMED":
            profile.cross_domain_key = "ISO3+" if n_domains >= 3 else "ISO2"
        elif profile.iso_status == "PARALLEL":
            profile.cross_domain_key = "PAR3+" if n_domains >= 3 else "PAR2"
        else:
            profile.cross_domain_key = "ANA"
    elif n_domains == 2:
        profile.iso_status = pick_one("ISO status", Q2_ISO_STATUS, show_weights=False)
        if profile.iso_status == "CONFIRMED":
            profile.cross_domain_key = "ISO2"
        elif profile.iso_status == "PARALLEL":
            profile.cross_domain_key = "PAR2"
        else:
            profile.cross_domain_key = "ANA"
    else:
        profile.iso_status = "BOUND"
        profile.cross_domain_key = "BOUND"
        print("  → Single domain. Cross-domain multiplier: ×0.90 (penalty)")

    xdm = Q2_CROSS_DOMAIN_MULTIPLIER.get(profile.cross_domain_key, {})
    print(f"\n  Cross-domain multiplier: {profile.cross_domain_key} → ×{xdm.get('multiplier', 1.0):.2f}")


def step_q3(profile: ClaimProfile):
    """Q3: Assertion — what exactly is being claimed?"""
    banner("Q3 — ASSERTION")
    print("  What type of claim is this?")
    profile.claim_type = pick_one("Claim type", Q3_CLAIM_TYPE)

    print("\n  How precise is the claim?")
    profile.precision = pick_one("Precision", Q3_PRECISION)

    print("\n  How certain are we?")
    profile.certainty = pick_one("Certainty", Q3_CERTAINTY)

    print("\n  What's the scope?")
    profile.scope = pick_one("Scope", Q3_SCOPE)


def step_q4(profile: ClaimProfile):
    """Q4: Evidence — what supports it?"""
    banner("Q4 — EVIDENCE")
    print("  Add evidence items. Type 'done' when finished.\n")

    idx = 1
    while True:
        print(f"  ─── Evidence #{idx} ───")
        name = ask_text(f"  Evidence name (or 'done')")
        if name.lower() == "done":
            break

        ev = EvidenceItem(name=name)
        ev.evidence_type = pick_one("Type", Q4_EVIDENCE_TYPE)
        ev.tier = pick_one("Tier", Q4_TIER)
        ev.strength = pick_one("Strength", Q4_STRENGTH)
        ev.linkage = pick_one("Linkage", Q4_LINKAGE)

        print("\n  Three-channel scoring:")
        ev.ps_raw = ask_float("PS (Phenomenon Strength 0-1, 0=auto-derive)", 0.0)
        ev.ed = ask_float("ED (Explanatory Depth 0-1)", 0.5)
        ev.ec = ask_float("EC (Epistemic Completeness 0-1)", 0.5)

        print("\n  Any vulnerabilities?")
        ev.vulnerabilities = pick_many("Vulnerabilities", Q4_VULNERABILITIES)

        profile.evidence.append(ev)
        idx += 1

    if not profile.evidence:
        print("  ⚠ No evidence entered. E score will be 0.")


def step_q5(profile: ClaimProfile):
    """Q5: Dependency — what does it rest on?"""
    banner("Q5 — DEPENDENCY")
    print("  Where does the justification chain terminate?")
    profile.terminus = pick_one("Terminus type", Q5_TERMINUS)

    print("\n  How is it derived?")
    profile.derivation = pick_one("Derivation method", Q5_DERIVATION)

    print("\n  List key dependencies (one per line, blank to stop):")
    while True:
        dep = ask_text("  Dependency")
        if not dep:
            break
        profile.dependency_chain.append(dep)


def step_q6(profile: ClaimProfile):
    """Q6: Consequence — what does it predict?"""
    banner("Q6 — CONSEQUENCE")
    print("  Add predictions / consequences. Type 'done' when finished.\n")

    idx = 1
    while True:
        desc = ask_text(f"  Prediction #{idx} (or 'done')")
        if desc.lower() == "done":
            break

        pred = PredictionItem(description=desc)
        pred.pred_type = pick_one("Prediction type", Q6_PREDICTION_TYPE)
        pred.competing = pick_one("Competing models?", Q6_COMPETING)
        pred.confirmed = ask_yn("Already confirmed?")

        profile.predictions.append(pred)
        idx += 1


def step_q7(profile: ClaimProfile):
    """Q7: Falsification — try to kill it."""
    banner("Q7 — FALSIFICATION (Destruction)")
    print("  Run each death type against the claim.\n")

    for key, entry in Q7_DEATH_TYPES.items():
        print(f"\n  ─── {key}: {entry['label']} ───")
        result = pick_one("Result", Q7_DEATH_RESULT, show_weights=False)
        notes = ask_text("Notes (optional)", "")
        profile.death_tests.append(DeathTest(death_type=key, result=result, notes=notes))

        if result == "DIES":
            print(f"\n  ☠ CLAIM KILLED by {key}.")
            if not ask_yn("Continue testing remaining death types anyway?"):
                break

    print("\n  Overall robustness level?")
    profile.robustness = pick_one("Robustness", Q7_ROBUSTNESS)

    print("\n  If this claim dies, what falls with it?")
    profile.cascade_scope = pick_one("Cascade scope", Q7_CASCADE_SCOPE)


# ═══════════════════════════════════════════════
# MAIN FORWARD INTAKE
# ═══════════════════════════════════════════════

def run_forward_intake() -> tuple:
    """
    Run the full forward intake Q0→Q7.
    Returns (ClaimProfile, ScoreResult).
    """
    banner("7Q FORWARD CLASSIFIER — Interactive Intake")
    print("  Walk through Q0→Q7. Every question gets classified.")
    print("  At the end, you get a truth score and Obsidian note.\n")

    profile = ClaimProfile()

    steps = [
        step_baseline,
        step_q0,
        step_q1,
        step_q2,
        step_q3,
        step_q4,
        step_q5,
        step_q6,
        step_q7,
    ]

    for step_fn in steps:
        step_fn(profile)

    # Score it
    banner("SCORING")
    result = compute_truth_score(profile)
    print(score_summary(result))
    print()
    print(machine_block(profile, result))

    return profile, result


if __name__ == "__main__":
    profile, result = run_forward_intake()
