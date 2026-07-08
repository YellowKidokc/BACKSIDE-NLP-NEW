"""
7Q Scorer — All scoring math in one place.

Three-channel evidence scoring, category-weighted truth score,
cross-domain multiplier, vulnerability penalties, confidence class.

David Lowe | POF 2828 | March 2026
"""

from dataclasses import dataclass, field
from typing import List, Optional
from id_system import (
    Q0_MODE, Q1_ENTITY_TYPE, Q1_AXIOM_CLASS, Q1_STATUS, Q1_SOURCE,
    Q2_CROSS_DOMAIN_MULTIPLIER,
    Q3_CLAIM_TYPE, Q3_PRECISION, Q3_CERTAINTY, Q3_SCOPE,
    Q4_EVIDENCE_TYPE, Q4_TIER, Q4_STRENGTH, Q4_LINKAGE, Q4_VULNERABILITIES,
    Q5_TERMINUS, Q7_ROBUSTNESS, Q7_CASCADE_SCOPE,
    Q6_PREDICTION_TYPE, Q6_COMPETING,
    get_weight, get_confidence_class,
)


# ═══════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════

@dataclass
class EvidenceItem:
    """A single piece of evidence with its classifications."""
    name: str = ""
    evidence_type: str = ""       # key into Q4_EVIDENCE_TYPE
    tier: str = ""                # key into Q4_TIER
    strength: str = ""            # key into Q4_STRENGTH
    linkage: str = ""             # key into Q4_LINKAGE
    vulnerabilities: List[str] = field(default_factory=list)  # keys into Q4_VULNERABILITIES
    ps_raw: float = 0.0          # Phenomenon Strength (0–1), user-assessed or derived
    ed: float = 0.0              # Explanatory Depth (0–1)
    ec: float = 0.0              # Epistemic Completeness (0–1)


@dataclass
class PredictionItem:
    """A prediction / consequence of the claim."""
    description: str = ""
    pred_type: str = ""           # key into Q6_PREDICTION_TYPE
    competing: str = ""           # key into Q6_COMPETING
    confirmed: bool = False


@dataclass
class DeathTest:
    """One Q7 kill attempt."""
    death_type: str = ""          # key into Q7_DEATH_TYPES
    result: str = "UNTESTED"      # SURVIVES | DIES | WEAKENED | UNTESTED
    notes: str = ""


@dataclass
class ClaimProfile:
    """Everything the scorer needs — filled in by intake or destroy mode."""
    # Metadata
    claim_id: str = ""
    claim_text: str = ""
    domain: str = "PHY"

    # Q0
    mode: str = "INVEST"

    # Q1
    entity_type: str = ""
    axiom_class: str = ""
    status: str = ""
    source: str = ""

    # Q2
    scales: List[str] = field(default_factory=list)
    iso_status: str = ""
    cross_domain_key: str = ""     # key into Q2_CROSS_DOMAIN_MULTIPLIER
    domains_present: List[str] = field(default_factory=list)

    # Q3
    claim_type: str = ""
    precision: str = ""
    certainty: str = ""
    scope: str = ""

    # Q4
    evidence: List[EvidenceItem] = field(default_factory=list)

    # Q5
    terminus: str = ""
    derivation: str = ""
    dependency_chain: List[str] = field(default_factory=list)

    # Q6
    predictions: List[PredictionItem] = field(default_factory=list)

    # Q7
    death_tests: List[DeathTest] = field(default_factory=list)
    robustness: str = ""
    cascade_scope: str = ""


@dataclass
class ScoreResult:
    """Full scored output."""
    # Category scores (S, E, L, D, P, C — the six pillars)
    S: float = 0.0   # Structural (Q1 identity + Q3 assertion)
    E: float = 0.0   # Evidence (Q4)
    L: float = 0.0   # Logical (Q5 dependency)
    D: float = 0.0   # Discriminatory (Q6 predictions)
    P: float = 0.0   # Posture (Q0)
    C: float = 0.0   # Combat (Q7 falsification)

    # Evidence sub-scores
    ps_avg: float = 0.0
    cf_avg: float = 0.0
    e_raw: float = 0.0

    # Vulnerability
    vuln_penalty: float = 0.0
    vuln_flags: List[str] = field(default_factory=list)

    # Truth score
    T_raw: float = 0.0
    xdm: float = 1.0             # cross-domain multiplier
    T_final: float = 0.0

    # Caps applied
    caps_applied: List[str] = field(default_factory=list)

    # Result
    confidence_class: str = ""
    confidence_label: str = ""

    # Per-question scores for output
    q_scores: dict = field(default_factory=dict)


# ═══════════════════════════════════════════════
# EVIDENCE SCORING (Three-Channel)
# ═══════════════════════════════════════════════

def score_evidence_item(ev: EvidenceItem, domain: str = None) -> dict:
    """
    Score a single evidence item.

    PS = Phenomenon Strength (user-assessed or derived from type/tier/strength)
    CF = Completeness Factor = (0.5 + 0.5*ED) × (0.5 + 0.5*EC)
    E_item = PS × CF

    WHY-PENALTY: if ED < 0.3, E is capped at 0.50
    """
    # Derive PS if not set directly
    ps = ev.ps_raw
    if ps <= 0:
        # Auto-derive from type × tier × strength × linkage
        w_type = get_weight(Q4_EVIDENCE_TYPE, ev.evidence_type, domain)
        w_tier = get_weight(Q4_TIER, ev.tier)
        w_str  = get_weight(Q4_STRENGTH, ev.strength)
        w_link = get_weight(Q4_LINKAGE, ev.linkage)
        # PS = geometric-ish blend: mostly type/strength, modulated by tier/linkage
        ps = w_type * 0.35 + w_str * 0.35 + w_tier * 0.15 + w_link * 0.15

    # CF = (0.5 + 0.5*ED) × (0.5 + 0.5*EC)
    cf = (0.5 + 0.5 * ev.ed) * (0.5 + 0.5 * ev.ec)

    e_item = ps * cf

    # WHY-PENALTY: no mechanism → cap at 50%
    why_capped = False
    if ev.ed < 0.3:
        e_item = min(e_item, 0.50)
        why_capped = True

    return {
        "ps": round(ps, 4),
        "ed": ev.ed,
        "ec": ev.ec,
        "cf": round(cf, 4),
        "e_item": round(e_item, 4),
        "why_capped": why_capped,
    }


def score_all_evidence(evidence: List[EvidenceItem], domain: str = None) -> dict:
    """
    Score all evidence items and return aggregate.

    E = average of all evidence items (after per-item caps).
    Then apply vulnerability penalties.
    """
    if not evidence:
        return {"ps_avg": 0, "cf_avg": 0, "e_raw": 0, "items": [], "vuln_penalty": 0, "vuln_flags": []}

    items = [score_evidence_item(ev, domain) for ev in evidence]
    ps_avg = sum(i["ps"] for i in items) / len(items)
    cf_avg = sum(i["cf"] for i in items) / len(items)
    e_raw  = sum(i["e_item"] for i in items) / len(items)

    # Vulnerability penalties (aggregate across all evidence items)
    all_vulns = set()
    for ev in evidence:
        all_vulns.update(ev.vulnerabilities)

    vuln_penalty = 0.0
    vuln_flags = []
    cap_T = None
    for v in all_vulns:
        entry = Q4_VULNERABILITIES.get(v, {})
        p = entry.get("penalty", 0)
        vuln_penalty += p
        if p != 0 or entry.get("flag"):
            vuln_flags.append(v)
        if "cap" in entry:
            e_raw = min(e_raw, entry["cap"])
        if "cap_T" in entry:
            cap_T = min(cap_T, entry["cap_T"]) if cap_T is not None else entry["cap_T"]

    e_final = max(0.0, e_raw + vuln_penalty)

    return {
        "ps_avg": round(ps_avg, 4),
        "cf_avg": round(cf_avg, 4),
        "e_raw": round(e_raw, 4),
        "e_final": round(e_final, 4),
        "vuln_penalty": round(vuln_penalty, 4),
        "vuln_flags": vuln_flags,
        "cap_T": cap_T,
        "items": items,
    }


# ═══════════════════════════════════════════════
# CATEGORY SCORES (S, E, L, D, P, C)
# ═══════════════════════════════════════════════

def compute_S(profile: ClaimProfile) -> float:
    """
    S = Structural score from Q1 (identity) and Q3 (assertion).

    S = 0.25*entity_type + 0.15*axiom_class + 0.10*status + 0.10*source
      + 0.15*claim_type + 0.10*precision + 0.10*certainty + 0.05*scope
    """
    d = profile.domain
    scores = {
        "entity": get_weight(Q1_ENTITY_TYPE, profile.entity_type, d) * 0.25,
        "axiom":  get_weight(Q1_AXIOM_CLASS, profile.axiom_class, d) * 0.15,
        "status": get_weight(Q1_STATUS, profile.status, d) * 0.10,
        "source": get_weight(Q1_SOURCE, profile.source, d) * 0.10,
        "claim":  get_weight(Q3_CLAIM_TYPE, profile.claim_type, d) * 0.15,
        "prec":   get_weight(Q3_PRECISION, profile.precision, d) * 0.10,
        "cert":   get_weight(Q3_CERTAINTY, profile.certainty, d) * 0.10,
        "scope":  get_weight(Q3_SCOPE, profile.scope, d) * 0.05,
    }
    return round(sum(scores.values()), 4)


def compute_L(profile: ClaimProfile) -> float:
    """
    L = Logical foundation score from Q5 (dependency).

    L = terminus_weight (that's the whole pillar — where do you bottom out?)
    Kill conditions: CIRCULAR or INFINITE → L = 0.0
    """
    d = profile.domain
    t = Q5_TERMINUS.get(profile.terminus, {})
    w = get_weight(Q5_TERMINUS, profile.terminus, d)
    if t.get("kill"):
        return 0.0
    return round(w, 4)


def compute_D(profile: ClaimProfile) -> float:
    """
    D = Discriminatory power from Q6 (predictions/consequences).

    D = average of (prediction_type_weight × competing_weight) for all predictions.
    Bonus: if any prediction is CONFIRMED, +0.10 (capped at 1.0).
    """
    if not profile.predictions:
        return 0.0

    scores = []
    has_confirmed = False
    for pred in profile.predictions:
        pt = get_weight(Q6_PREDICTION_TYPE, pred.pred_type)
        cp = get_weight(Q6_COMPETING, pred.competing)
        scores.append(pt * cp)
        if pred.confirmed:
            has_confirmed = True

    d = sum(scores) / len(scores)
    if has_confirmed:
        d = min(1.0, d + 0.10)
    return round(d, 4)


def compute_P(profile: ClaimProfile) -> float:
    """P = Posture score from Q0. Straightforward weight lookup."""
    return round(get_weight(Q0_MODE, profile.mode), 4)


def compute_C(profile: ClaimProfile) -> float:
    """
    C = Combat score from Q7 (falsification).

    Base = robustness weight.
    For each death test:
      SURVIVES → +0.15
      WEAKENED → -0.05
      DIES     → C = 0.0 (kill)
    """
    base = get_weight(Q7_ROBUSTNESS, profile.robustness)

    for dt in profile.death_tests:
        if dt.result == "DIES":
            return 0.0
        elif dt.result == "SURVIVES":
            base = min(1.0, base + 0.15)
        elif dt.result == "WEAKENED":
            base = max(0.0, base - 0.05)
        # UNTESTED → no change

    return round(base, 4)


# ═══════════════════════════════════════════════
# TRUTH SCORE
# ═══════════════════════════════════════════════

def compute_truth_score(profile: ClaimProfile) -> ScoreResult:
    """
    Full truth score computation.

    T_raw = (S + E + L + D + P + C) / 6
    T_final = T_raw × XDM

    Caps:
      - VAGUE precision → T capped at 0.00 (kill)
      - UNFALSIFIABLE → T capped at 0.60
      - CIRCULAR/INFINITE terminus → L = 0.0 (already handled)
      - Any DIES in Q7 → C = 0.0 (already handled)
    """
    result = ScoreResult()

    # Category scores
    result.S = compute_S(profile)
    result.P = compute_P(profile)
    result.L = compute_L(profile)
    result.D = compute_D(profile)
    result.C = compute_C(profile)

    # Evidence (most complex)
    ev_result = score_all_evidence(profile.evidence, profile.domain)
    result.E = ev_result["e_final"]
    result.ps_avg = ev_result["ps_avg"]
    result.cf_avg = ev_result["cf_avg"]
    result.e_raw = ev_result["e_raw"]
    result.vuln_penalty = ev_result["vuln_penalty"]
    result.vuln_flags = ev_result["vuln_flags"]

    # Per-question scores for output
    result.q_scores = {
        "Q0": result.P,
        "Q1": round(get_weight(Q1_ENTITY_TYPE, profile.entity_type, profile.domain), 4),
        "Q2": round(len(profile.domains_present) / 18.0, 4) if profile.domains_present else 0.0,
        "Q3": round(
            get_weight(Q3_CLAIM_TYPE, profile.claim_type, profile.domain) * 0.4
            + get_weight(Q3_PRECISION, profile.precision) * 0.3
            + get_weight(Q3_CERTAINTY, profile.certainty) * 0.3, 4),
        "Q4": result.E,
        "Q5": result.L,
        "Q6": result.D,
        "Q7": result.C,
    }

    # Cross-domain multiplier
    xdm_entry = Q2_CROSS_DOMAIN_MULTIPLIER.get(profile.cross_domain_key, {})
    result.xdm = xdm_entry.get("multiplier", 1.0)

    # T_raw = (S + E + L + D + P + C) / 6
    result.T_raw = round((result.S + result.E + result.L + result.D + result.P + result.C) / 6.0, 4)

    # Apply caps
    # VAGUE precision kills the claim
    prec_entry = Q3_PRECISION.get(profile.precision, {})
    if prec_entry.get("kill"):
        result.T_raw = 0.0
        result.caps_applied.append("VAGUE_PRECISION_KILL")

    # UNFALSIFIABLE cap
    if "UNFALSIFIABLE" in result.vuln_flags:
        result.T_raw = min(result.T_raw, 0.60)
        if result.T_raw == 0.60:
            result.caps_applied.append("UNFALSIFIABLE_CAP_0.60")

    # Evidence cap_T (from vulnerability entries)
    if ev_result.get("cap_T") is not None:
        result.T_raw = min(result.T_raw, ev_result["cap_T"])
        result.caps_applied.append(f"VULN_CAP_{ev_result['cap_T']}")

    # T_final
    result.T_final = round(min(1.0, result.T_raw * result.xdm), 4)

    # Confidence class
    cc = get_confidence_class(result.T_final)
    result.confidence_class = cc["id"]
    result.confidence_label = cc["label"]

    return result


# ═══════════════════════════════════════════════
# DISPLAY HELPERS
# ═══════════════════════════════════════════════

def score_summary(result: ScoreResult) -> str:
    """Human-readable one-block summary."""
    lines = [
        "═══════════════════════════════════════",
        "           7Q TRUTH SCORE",
        "═══════════════════════════════════════",
        f"  S (Structural)   : {result.S:.3f}",
        f"  E (Evidence)     : {result.E:.3f}  (PS={result.ps_avg:.2f} CF={result.cf_avg:.2f})",
        f"  L (Logical)      : {result.L:.3f}",
        f"  D (Discriminatory): {result.D:.3f}",
        f"  P (Posture)      : {result.P:.3f}",
        f"  C (Combat)       : {result.C:.3f}",
        "───────────────────────────────────────",
        f"  T_raw            : {result.T_raw:.4f}",
        f"  XDM              : ×{result.xdm:.2f}",
        f"  T_final          : {result.T_final:.4f}",
        "───────────────────────────────────────",
        f"  CLASS: {result.confidence_class} — {result.confidence_label}",
    ]
    if result.vuln_flags:
        lines.append(f"  VULNS: {', '.join(result.vuln_flags)}")
    if result.caps_applied:
        lines.append(f"  CAPS:  {', '.join(result.caps_applied)}")
    lines.append("═══════════════════════════════════════")
    return "\n".join(lines)


def machine_block(profile: ClaimProfile, result: ScoreResult) -> str:
    """Machine-parseable scoring block (matches LLM Maximum Rigor output format)."""
    lines = [
        "```scoring",
        f"CLAIM_ID: {profile.claim_id}",
        f"DOMAIN: {profile.domain}",
    ]
    for q, val in result.q_scores.items():
        lines.append(f"{q}: {val:.4f}")
    lines += [
        f"T_RAW: {result.T_raw:.4f}",
        f"XDM: {result.xdm:.2f}",
        f"T_FINAL: {result.T_final:.4f}",
        f"CLASS: {result.confidence_class}",
        f"VULNS: [{', '.join(result.vuln_flags)}]",
        f"CAPS: [{', '.join(result.caps_applied)}]",
        f"MODE: {profile.mode}",
        "```",
    ]
    return "\n".join(lines)


# ═══════════════════════════════════════════════
# QUICK TEST
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    # Example: planet positions claim from the walkthrough
    profile = ClaimProfile(
        claim_id="CL-PHY-0001",
        claim_text="Planet size and position follow predictable patterns based on orbital mechanics",
        domain="PHY",
        mode="INVEST",
        entity_type="LAW",
        axiom_class="DERIVED",
        status="CANONICAL",
        source="PEERREV",
        scales=["COSMIC"],
        iso_status="CONFIRMED",
        cross_domain_key="ISO2",
        domains_present=["PHY", "MTH"],
        claim_type="MATHEMATICAL",
        precision="PRECISE",
        certainty="PROVEN",
        scope="UNIVERSAL",
        evidence=[
            EvidenceItem(
                name="Kepler's laws + observations",
                evidence_type="EXPERIMENTAL",
                tier="T1",
                strength="CONCLUSIVE",
                linkage="DIRECT",
                ps_raw=0.95,
                ed=0.90,
                ec=0.85,
            ),
            EvidenceItem(
                name="Exoplanet surveys (Kepler/TESS)",
                evidence_type="OBSERVATIONAL",
                tier="T1",
                strength="STRONG",
                linkage="DIRECT",
                ps_raw=0.85,
                ed=0.80,
                ec=0.75,
            ),
        ],
        terminus="EMPIRICAL",
        derivation="DEDUCTIVE",
        predictions=[
            PredictionItem(
                description="Next planet position from orbital elements",
                pred_type="CONFIRMED",
                competing="EXCLUSIVE",
                confirmed=True,
            ),
        ],
        death_tests=[
            DeathTest(death_type="EMPIRICAL", result="SURVIVES", notes="Centuries of observation"),
            DeathTest(death_type="EXPLAIN", result="SURVIVES", notes="No competing model works better"),
        ],
        robustness="SURVIVED_ADV",
        cascade_scope="FRAMEWORK",
    )

    result = compute_truth_score(profile)
    print(score_summary(result))
    print()
    print(machine_block(profile, result))
