"""
7Q Obsidian Writer — Generates scored .md notes for the vault.

Uses custom callout types that match 7q-scored-callouts.css:
  [!q0-arrive]  gray    — the empty soil
  [!q1-define]  gold    — the seed
  [!q2-locate]  brown   — the soil
  [!q3-commit]  green   — the sprout
  [!q4-support] blue    — the rain
  [!q5-ground]  brown   — the roots
  [!q6-propagate] emerald — the canopy
  [!q7-destroy] red     — the axe
  [!verdict]    gold    — executive summary
  [!theory-map] purple  — theory resonance
  [!graph]      blue    — knowledge graph YAML

Format reference: FP-008_SCORED_CLEAN.md

David Lowe | POF 2828 | March 2026
"""

import os
from datetime import datetime
from scorer import ClaimProfile, ScoreResult, machine_block
from id_system import (
    DOMAINS, OBJECT_TYPES,
    Q0_MODE, Q1_ENTITY_TYPE, Q1_STATUS, Q1_SOURCE, Q1_AXIOM_CLASS,
    Q3_CLAIM_TYPE, Q3_PRECISION, Q3_CERTAINTY, Q3_SCOPE,
    Q4_EVIDENCE_TYPE, Q4_TIER, Q4_STRENGTH, Q4_LINKAGE,
    Q5_TERMINUS, Q5_DERIVATION,
    Q6_PREDICTION_TYPE, Q6_COMPETING,
    Q7_DEATH_TYPES, Q7_DEATH_RESULT, Q7_ROBUSTNESS, Q7_CASCADE_SCOPE,
    Q2_CROSS_DOMAIN_MULTIPLIER, Q2_ISO_STATUS,
    get_confidence_class,
)


# ═══════════════════════════════════════════════
# DEFAULT OUTPUT FOLDER
# ═══════════════════════════════════════════════

DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scored_output")


def ensure_output_dir(path: str = None):
    d = path or DEFAULT_OUTPUT_DIR
    os.makedirs(d, exist_ok=True)
    return d


# ═══════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════

def _label(registry: dict, key: str, field: str = "label") -> str:
    """Get a label from a registry dict."""
    entry = registry.get(key, {})
    if isinstance(entry, dict):
        return entry.get(field, key)
    return str(entry)


def _weight(registry: dict, key: str) -> str:
    """Get weight as string from registry."""
    entry = registry.get(key, {})
    w = entry.get("weight", "") if isinstance(entry, dict) else ""
    return str(w) if w is not None else "—"


# ═══════════════════════════════════════════════
# YAML FRONTMATTER (matches FP-008 structure)
# ═══════════════════════════════════════════════

def build_frontmatter(profile: ClaimProfile, result: ScoreResult, mode: str = "forward") -> str:
    """Generate YAML frontmatter matching FP-008 format."""
    domain_label = DOMAINS.get(profile.domain, profile.domain)
    entity_label = _label(Q1_ENTITY_TYPE, profile.entity_type)
    iso_label = _label(Q2_ISO_STATUS, profile.iso_status) if profile.iso_status else "—"

    # Determine strongest/weakest Q
    q_labels = {
        "Q0": "Posture", "Q1": "Identity", "Q2": "Domain",
        "Q3": "Assertion", "Q4": "Evidence", "Q5": "Dependencies",
        "Q6": "Consequences", "Q7": "Falsification",
    }
    qs = result.q_scores
    if qs:
        strongest_q = max(qs, key=qs.get)
        weakest_q = min(qs, key=qs.get)
    else:
        strongest_q = weakest_q = "Q0"

    lines = [
        "---",
        f'title: "{profile.claim_text}"',
        f"scored: true",
        f'scored_date: "{datetime.now().strftime("%Y-%m-%d")}"',
        f'type: "{profile.entity_type}"',
        f'confidence: "{result.confidence_class}"',
        f'iso_status: "{profile.iso_status or "BOUND"}"',
        f"claim_count: 1",
        f"kill_count: {len(profile.death_tests)}",
        f'strongest: "{strongest_q} — {q_labels.get(strongest_q, "")} ({qs.get(strongest_q, 0):.2f})"',
        f'weakest: "{weakest_q} — {q_labels.get(weakest_q, "")} ({qs.get(weakest_q, 0):.2f})"',
        "7q_scores:",
        f"  Q0_POSTURE: {qs.get('Q0', 0):.2f}",
        f"  Q1_IDENTITY: {qs.get('Q1', 0):.2f}",
        f"  Q2_DOMAIN: {qs.get('Q2', 0):.2f}",
        f"  Q3_ASSERTION: {qs.get('Q3', 0):.2f}",
        f"  Q4_EVIDENCE: {qs.get('Q4', 0):.2f}",
        f"  Q5_DEPENDENCIES: {qs.get('Q5', 0):.2f}",
        f"  Q6_CONSEQUENCES: {qs.get('Q6', 0):.2f}",
        f"  Q7_FALSIFICATION: {qs.get('Q7', 0):.2f}",
        "truth_score:",
        f"  S: {result.S:.2f}",
        f"  E: {result.E:.2f}",
        f"  L: {result.L:.2f}",
        f"  D: {result.D:.2f}",
        f"  P: {result.P:.2f}",
        f"  C: {result.C:.2f}",
        f"  T: {result.T_raw:.3f}",
        f"  T_enhanced: {result.T_final:.3f}",
        f"id: {profile.claim_id}",
        f"domain: {profile.domain}",
        f"mode: {mode}",
        "tags:",
        f"  - 7Q/{profile.domain}",
        f"  - 7Q/entity/{profile.entity_type}",
        f"  - 7Q/status/{profile.status}",
        f"  - 7Q/class/{result.confidence_class}",
        f"  - 7Q/mode/{mode}",
    ]
    for v in result.vuln_flags:
        lines.append(f"  - 7Q/vuln/{v}")
    lines.append("---")
    return "\n".join(lines)


# ═══════════════════════════════════════════════
# OVERVIEW STRIP (tabbed callout at top)
# ═══════════════════════════════════════════════

def build_overview_strip(profile: ClaimProfile, result: ScoreResult) -> str:
    """Build the tabbed overview strip matching FP-008 format."""
    domain_label = DOMAINS.get(profile.domain, profile.domain)
    entity_label = _label(Q1_ENTITY_TYPE, profile.entity_type)
    xdm_entry = Q2_CROSS_DOMAIN_MULTIPLIER.get(profile.cross_domain_key, {})

    q_labels = {
        "Q0": "Posture", "Q1": "Identity", "Q2": "Domain",
        "Q3": "Assertion", "Q4": "Evidence", "Q5": "Dependencies",
        "Q6": "Consequences", "Q7": "Falsification",
    }
    qs = result.q_scores
    strongest_q = max(qs, key=qs.get) if qs else "Q0"
    weakest_q = min(qs, key=qs.get) if qs else "Q0"

    # Caps string
    caps_str = ", ".join(result.caps_applied) if result.caps_applied else "None active"

    lines = [
        '> [!tabbed]',
        '> <label>Overview<input type="radio" name="7q-tabs" checked /></label>',
        f'> > **Type:** {entity_label} | **Confidence:** {result.confidence_class} | **ISO:** {profile.iso_status or "BOUND"}',
        f'> > **T-Score:** {result.T_raw:.3f} | **T-Enhanced:** {result.T_final:.3f} | **XDM:** x{result.xdm:.2f}',
        f'> > **Strongest:** {strongest_q} {q_labels.get(strongest_q, "")} ({qs.get(strongest_q, 0):.2f})',
        f'> > **Weakest:** {weakest_q} {q_labels.get(weakest_q, "")} ({qs.get(weakest_q, 0):.2f})',
        f'> > **Caps:** {caps_str}',
        '> <label>Score<input type="radio" name="7q-tabs" /></label>',
        '> > | Q | Dimension | Score |',
        '> > |---|-----------|-------|',
    ]
    for q_key in ["Q0", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"]:
        lines.append(f'> > | {q_key} | {q_labels.get(q_key, "")} | {qs.get(q_key, 0):.2f} |')
    lines.append(f'> > | **T** | **Composite** | **{result.T_raw:.3f}** |')
    lines.append(f'> > | **T+** | **Enhanced (XDM)** | **{result.T_final:.3f}** |')

    # Kill tab
    lines.append('> <label>Kill<input type="radio" name="7q-tabs" /></label>')
    for i, dt in enumerate(profile.death_tests, 1):
        dtype_label = Q7_DEATH_TYPES.get(dt.death_type, {}).get("label", dt.death_type)
        result_str = dt.result
        notes_str = f" — {dt.notes}" if dt.notes else ""
        lines.append(f'> > **Kill {i}:** {dtype_label} -> {result_str}{notes_str}')

    return "\n".join(lines)


# ═══════════════════════════════════════════════
# Q0–Q7 CALLOUTS (matching custom CSS types)
# ═══════════════════════════════════════════════

def callout_q0(profile: ClaimProfile, result: ScoreResult) -> str:
    mode_info = Q0_MODE.get(profile.mode, {})
    lines = [
        f'> [!q0-arrive]- Q0 — ARRIVE ({result.P:.2f})',
        f'> **Posture Assessment:** Mode is {profile.mode} — {mode_info.get("label", "")} (weight: {mode_info.get("weight", "")})',
    ]
    if profile.mode == "ADVOC":
        lines.append('> **Caveat:** Advocacy posture detected. Claim enters with reduced weight.')
    elif profile.mode == "MIXED":
        lines.append('> **Caveat:** Mixed posture. Some advocacy bias may be present.')
    return "\n".join(lines)


def callout_q1(profile: ClaimProfile, result: ScoreResult) -> str:
    etype = _label(Q1_ENTITY_TYPE, profile.entity_type)
    aclass = _label(Q1_AXIOM_CLASS, profile.axiom_class)
    status = _label(Q1_STATUS, profile.status)
    source = _label(Q1_SOURCE, profile.source)
    lines = [
        f'> [!q1-define]- Q1 — DEFINE ({result.q_scores.get("Q1", 0):.2f})',
        f'> **Type:** {profile.entity_type} — {etype}',
        f'> **Axiom Class:** {profile.axiom_class} — {aclass}',
        f'> **Status:** {profile.status} — {status}',
        f'> **Source:** {profile.source} — {source}',
    ]
    return "\n".join(lines)


def callout_q2(profile: ClaimProfile, result: ScoreResult) -> str:
    xdm_entry = Q2_CROSS_DOMAIN_MULTIPLIER.get(profile.cross_domain_key, {})
    domains_str = ", ".join(profile.domains_present) if profile.domains_present else "—"
    scales_str = ", ".join(profile.scales) if profile.scales else "—"
    iso_label = _label(Q2_ISO_STATUS, profile.iso_status) if profile.iso_status else "—"
    lines = [
        f'> [!q2-locate]- Q2 — LOCATE ({result.q_scores.get("Q2", 0):.2f})',
        f'> **Primary Domain:** {DOMAINS.get(profile.domain, profile.domain)}',
        f'> **Cross-Domain:** {domains_str} ({len(profile.domains_present)} domains)',
        f'> **Scale:** {scales_str}',
        f'> **Isomorphism Status:** {profile.iso_status} — {iso_label}',
        f'> **Cross-Domain Multiplier:** {profile.cross_domain_key} -> x{xdm_entry.get("multiplier", 1.0):.2f}',
    ]
    return "\n".join(lines)


def callout_q3(profile: ClaimProfile, result: ScoreResult) -> str:
    q3 = result.q_scores.get("Q3", 0)
    ctype = _label(Q3_CLAIM_TYPE, profile.claim_type)
    prec = _label(Q3_PRECISION, profile.precision)
    cert = _label(Q3_CERTAINTY, profile.certainty)
    scope = _label(Q3_SCOPE, profile.scope)
    lines = [
        f'> [!q3-commit]- Q3 — COMMIT ({q3:.2f})',
        f'> **Statement:** "{profile.claim_text}"',
        f'> **Claim Type:** {profile.claim_type} — {ctype}',
        f'> **Precision:** {profile.precision} — {prec}',
        f'> **Certainty:** {profile.certainty} — {cert}',
        f'> **Scope:** {profile.scope} — {scope}',
    ]
    return "\n".join(lines)


def callout_q4(profile: ClaimProfile, result: ScoreResult) -> str:
    lines = [
        f'> [!q4-support]- Q4 — SUPPORT ({result.E:.2f})',
        f'> **PS (Phenomenon Strength):** {result.ps_avg:.2f}',
        f'> **CF (Completeness Factor):** {result.cf_avg:.2f}',
        f'> **E_final:** {result.E:.2f}',
    ]
    if result.e_raw != result.E:
        lines.append(f'> **E_raw (before penalties):** {result.e_raw:.2f}')
    why_active = any(ev.ed < 0.3 for ev in profile.evidence)
    lines.append(f'> **Why-Penalty:** {"ACTIVE (ED < 0.3)" if why_active else "NOT active (ED >= 0.3)"}')

    if result.vuln_flags:
        lines.append(f'> **Vulnerability Flags:** {", ".join(result.vuln_flags)}')
        lines.append(f'> **Vulnerability Penalty:** {result.vuln_penalty:+.2f}')

    # Per-evidence detail
    for i, ev in enumerate(profile.evidence, 1):
        ev_type_label = _label(Q4_EVIDENCE_TYPE, ev.evidence_type)
        tier_label = _label(Q4_TIER, ev.tier)
        str_label = _label(Q4_STRENGTH, ev.strength)
        link_label = _label(Q4_LINKAGE, ev.linkage)
        lines.append(f'>')
        lines.append(f'> **Evidence {i}: {ev.name}**')
        lines.append(f'> - Type: {ev.evidence_type} ({ev_type_label}) | Tier: {ev.tier} ({tier_label})')
        lines.append(f'> - Strength: {ev.strength} ({str_label}) | Linkage: {ev.linkage} ({link_label})')
        lines.append(f'> - PS: {ev.ps_raw:.2f} | ED: {ev.ed:.2f} | EC: {ev.ec:.2f}')
        if ev.vulnerabilities:
            lines.append(f'> - Vulns: {", ".join(ev.vulnerabilities)}')

    return "\n".join(lines)


def callout_q5(profile: ClaimProfile, result: ScoreResult) -> str:
    term_label = _label(Q5_TERMINUS, profile.terminus)
    deriv_label = _label(Q5_DERIVATION, profile.derivation)
    lines = [
        f'> [!q5-ground]- Q5 — GROUND ({result.L:.2f})',
        f'> **Chain Terminus:** {profile.terminus} — {term_label}',
        f'> **Derivation:** {profile.derivation} — {deriv_label}',
        f'> **Dependencies:**',
    ]
    if profile.dependency_chain:
        for dep in profile.dependency_chain:
            lines.append(f'> - {dep}')
    else:
        lines.append(f'> - None listed')

    # Flag kill conditions
    if profile.terminus in ("CIRCULAR", "INFINITE"):
        lines.append(f'>')
        lines.append(f'> **KILL CONDITION:** {profile.terminus} — chain {term_label.lower()}. L = 0.00')

    return "\n".join(lines)


def callout_q6(profile: ClaimProfile, result: ScoreResult) -> str:
    lines = [
        f'> [!q6-propagate]- Q6 — PROPAGATE ({result.D:.2f})',
    ]
    confirmed = [p for p in profile.predictions if p.confirmed]
    untested = [p for p in profile.predictions if not p.confirmed]

    if confirmed:
        lines.append(f'> **Predictions Confirmed:**')
        for p in confirmed:
            competing_label = _label(Q6_COMPETING, p.competing)
            lines.append(f'> - {p.description} ({p.pred_type}, {competing_label})')

    if untested:
        lines.append(f'> **Predictions Untested:**')
        for p in untested:
            competing_label = _label(Q6_COMPETING, p.competing)
            lines.append(f'> - {p.description} ({p.pred_type}, {competing_label})')

    if not profile.predictions:
        lines.append(f'> No predictions listed. D score = 0.')

    return "\n".join(lines)


def callout_q7(profile: ClaimProfile, result: ScoreResult) -> str:
    rob_label = _label(Q7_ROBUSTNESS, profile.robustness)
    cas_label = _label(Q7_CASCADE_SCOPE, profile.cascade_scope) if profile.cascade_scope else "—"
    lines = [
        f'> [!q7-destroy]- Q7 — DESTROY ({result.C:.2f})',
    ]

    # Kill conditions
    lines.append(f'> **Explicit Kill Conditions:**')
    for i, dt in enumerate(profile.death_tests, 1):
        dtype_label = Q7_DEATH_TYPES.get(dt.death_type, {}).get("label", dt.death_type)
        icon = {"SURVIVES": "NOT MET", "DIES": "**KILLED**", "WEAKENED": "PARTIALLY MET", "UNTESTED": "NOT TESTED"}.get(dt.result, dt.result)
        lines.append(f'> **Kill {i}:** {dtype_label} -> {icon}')
        if dt.notes:
            lines.append(f'> - {dt.notes}')

    # What survives / what dies
    survived = [dt for dt in profile.death_tests if dt.result == "SURVIVES"]
    died = [dt for dt in profile.death_tests if dt.result == "DIES"]
    weakened = [dt for dt in profile.death_tests if dt.result == "WEAKENED"]

    if survived:
        labels = [Q7_DEATH_TYPES.get(dt.death_type, {}).get("label", dt.death_type) for dt in survived]
        lines.append(f'> **What Survives:** Passed {len(survived)}/{len(profile.death_tests)} death tests')
    if died:
        labels = [Q7_DEATH_TYPES.get(dt.death_type, {}).get("label", dt.death_type) for dt in died]
        lines.append(f'> **What Dies:** {"; ".join(labels)}')
    if weakened:
        labels = [Q7_DEATH_TYPES.get(dt.death_type, {}).get("label", dt.death_type) for dt in weakened]
        lines.append(f'> **Weakened By:** {"; ".join(labels)}')

    lines.append(f'>')
    lines.append(f'> **Robustness:** {profile.robustness} — {rob_label}')
    lines.append(f'> **Cascade Scope:** {profile.cascade_scope} — {cas_label}')

    return "\n".join(lines)


# ═══════════════════════════════════════════════
# VERDICT + THEORY MAP + GRAPH
# ═══════════════════════════════════════════════

def callout_verdict(profile: ClaimProfile, result: ScoreResult) -> str:
    """Executive summary in gold verdict callout."""
    domain_label = DOMAINS.get(profile.domain, profile.domain)
    entity_label = _label(Q1_ENTITY_TYPE, profile.entity_type)

    qs = result.q_scores
    strongest_q = max(qs, key=qs.get) if qs else "Q0"
    weakest_q = min(qs, key=qs.get) if qs else "Q0"
    q_labels = {
        "Q0": "Posture", "Q1": "Identity", "Q2": "Domain",
        "Q3": "Assertion", "Q4": "Evidence", "Q5": "Dependencies",
        "Q6": "Consequences", "Q7": "Falsification",
    }

    died = any(dt.result == "DIES" for dt in profile.death_tests)
    if died:
        verdict_line = f"This claim was **KILLED** during Q7 falsification. The score reflects the damage."
    else:
        verdict_line = (
            f"This {entity_label.lower()} in {domain_label.lower()} scores "
            f"T={result.T_raw:.3f} (enhanced T={result.T_final:.3f} with XDM x{result.xdm:.2f}), "
            f"classified as **{result.confidence_class}** — {result.confidence_label}."
        )

    lines = [
        f'> [!verdict] Executive Summary',
        f'> {verdict_line}',
        f'> Strongest dimension: {strongest_q} {q_labels.get(strongest_q, "")} ({qs.get(strongest_q, 0):.2f}). '
        f'Weakest: {weakest_q} {q_labels.get(weakest_q, "")} ({qs.get(weakest_q, 0):.2f}).',
    ]
    if result.vuln_flags:
        lines.append(f'> Vulnerability flags: {", ".join(result.vuln_flags)}.')
    if result.caps_applied:
        lines.append(f'> Score caps active: {", ".join(result.caps_applied)}.')
    return "\n".join(lines)


def callout_graph(profile: ClaimProfile, result: ScoreResult) -> str:
    """Knowledge graph YAML in blue graph callout."""
    lines = [
        f'> [!graph]- Knowledge Graph YAML',
        f'> ```yaml',
        f'> nodes:',
        f'>   - {{id: {profile.claim_id}, type: {profile.entity_type}, domain: {profile.domain}, score: {result.T_final:.3f}}}',
    ]
    # Add evidence as nodes
    for i, ev in enumerate(profile.evidence, 1):
        lines.append(f'>   - {{id: ev_{i:03d}, type: Evidence, label: "{ev.name}"}}')
    # Add predictions as nodes
    for i, pred in enumerate(profile.predictions, 1):
        lines.append(f'>   - {{id: pred_{i:03d}, type: Prediction, label: "{pred.description}"}}')

    lines.append(f'> edges:')
    for i, ev in enumerate(profile.evidence, 1):
        lines.append(f'>   - {{source: {profile.claim_id}, target: ev_{i:03d}, relation: supported_by}}')
    for i, pred in enumerate(profile.predictions, 1):
        lines.append(f'>   - {{source: {profile.claim_id}, target: pred_{i:03d}, relation: predicts}}')
    for dep in profile.dependency_chain:
        safe_dep = dep.replace('"', "'")
        lines.append(f'>   - {{source: {profile.claim_id}, target: dep, relation: depends_on, label: "{safe_dep}"}}')

    lines.append(f'> ```')
    return "\n".join(lines)


# ═══════════════════════════════════════════════
# MACHINE BLOCK (inside comment fence)
# ═══════════════════════════════════════════════

def section_machine_block(profile: ClaimProfile, result: ScoreResult) -> str:
    return f"""%%
{machine_block(profile, result)}
%%"""


# ═══════════════════════════════════════════════
# FULL NOTE ASSEMBLY
# ═══════════════════════════════════════════════

def build_full_note(profile: ClaimProfile, result: ScoreResult, mode: str = "forward") -> str:
    """Assemble the complete Obsidian note matching FP-008 clean format."""
    sections = [
        build_frontmatter(profile, result, mode),
        build_overview_strip(profile, result),
        "",
        "---",
        "",
        "",
        f"# {profile.claim_text}",
        "",
        "*[Claim content / paper body goes here]*",
        "",
        "---",
        "",
        "%%",
        "===============================================",
        "  7Q DETAILED ANALYSIS — ENGINE OUTPUT BELOW",
        "===============================================",
        "%%",
        "",
        "## 7Q Detailed Analysis",
        "",
        callout_q0(profile, result),
        "",
        callout_q1(profile, result),
        "",
        callout_q2(profile, result),
        "",
        callout_q3(profile, result),
        "",
        callout_q4(profile, result),
        "",
        callout_q5(profile, result),
        "",
        callout_q6(profile, result),
        "",
        callout_q7(profile, result),
        "",
        "",
        callout_verdict(profile, result),
        "",
        callout_graph(profile, result),
        "",
        section_machine_block(profile, result),
        "",
        "---",
        f"*Scored by 7Q Engine v2 | {mode} mode | {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        f"*CSS: 7q-scored-callouts.css (enable in Settings -> Appearance -> CSS Snippets)*",
    ]
    return "\n".join(sections)


def write_note(profile: ClaimProfile, result: ScoreResult,
               mode: str = "forward", output_dir: str = None) -> str:
    """
    Write the scored note to an .md file in the vault.
    Returns the full path of the written file.
    """
    d = ensure_output_dir(output_dir)

    # Filename: CLAIM_ID + sanitized claim text
    safe_text = "".join(c if c.isalnum() or c in " -_" else "" for c in profile.claim_text)
    safe_text = safe_text[:60].strip().replace(" ", "_")
    filename = f"{profile.claim_id}_{safe_text}.md"
    filepath = os.path.join(d, filename)

    content = build_full_note(profile, result, mode)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n  >> Note written: {filepath}")
    return filepath


# ═══════════════════════════════════════════════
# QUICK TEST
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    from scorer import ClaimProfile, EvidenceItem, PredictionItem, DeathTest, compute_truth_score

    profile = ClaimProfile(
        claim_id="CL-PHY-TEST",
        claim_text="Test claim for Obsidian output",
        domain="PHY",
        mode="INVEST",
        entity_type="HYPOTHESIS",
        axiom_class="DERIVED",
        status="CANDIDATE",
        source="ORIGINAL",
        scales=["MESO"],
        iso_status="BOUND",
        cross_domain_key="BOUND",
        domains_present=["PHY"],
        claim_type="CAUSAL",
        precision="DETAILED",
        certainty="TENTATIVE",
        scope="LOCAL",
        evidence=[
            EvidenceItem(name="Test observation", evidence_type="OBSERVATIONAL",
                        tier="T2", strength="MODERATE", linkage="INDIRECT",
                        ps_raw=0.6, ed=0.5, ec=0.4),
        ],
        terminus="EMPIRICAL",
        derivation="INDUCTIVE",
        predictions=[
            PredictionItem(description="Test prediction", pred_type="UNTESTED",
                          competing="AMBIGUOUS", confirmed=False),
        ],
        death_tests=[
            DeathTest(death_type="SELFREF", result="SURVIVES"),
            DeathTest(death_type="EMPIRICAL", result="SURVIVES"),
        ],
        robustness="TESTED",
        cascade_scope="LOCAL",
    )
    result = compute_truth_score(profile)
    filepath = write_note(profile, result, mode="forward")
    print(f"  Written to: {filepath}")
