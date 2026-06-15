"""
CANONICAL SEMANTIC ANCHORS
===========================
Extracted from the Codex (NODRIFT_LOSSLESS_v24.yaml + 24_PROPERTIES_CANONICAL.md).
These are the Theophysics-specific SBERT anchors — YOUR definitions, not generic ones.

Each anchor is a text description that gets embedded by SBERT. When a sentence
in a paper is semantically close to an anchor, it lights up in the word matrix
and heartbeat.

Organized into anchor groups:
  1. 24 Properties (6 CORE + 18 DERIVED/RELATIONAL)
  2. 10 Laws (constructive + destructive poles)
  3. 9 Fruits (physics equations)
  4. 9 Anti-Fruits (physics inversions)
  5. 6 Armor of God (decoherence protection)
  6. 8 Beatitudes (phase transition conditions)
  7. 9 Gifts of the Spirit (transformer modes)
  8. 8 Couplings (generator interactions)
"""

# ═══════════════════════════════════════════════════════════════
# 1. THE 24 PROPERTIES (God ↔ Math isomorphism)
# ═══════════════════════════════════════════════════════════════

PROPERTIES_24 = {
    # 6 CORE — math dies without these
    'P04_simple': "Irreducible axioms, primitive terms, foundation bottoms out, proofs complete, no infinite regress",
    'P05_consistent': "Non-contradiction holds everywhere, no internal contradiction, logical coherence, system integrity",
    'P12_true': "Truth-bearing by definition, statements have truth values, difference between valid proof and error",
    'P13_rational': "Governed by logic, conclusions follow from premises, inference works, Logos, the Word",
    'P23_generative': "Finite axioms produce infinite theorems, system is fertile, generates structures and results",
    'P24_judging': "Distinguishes true from false, valid from invalid, correct from incorrect, evaluation capacity",

    # 18 DERIVED/RELATIONAL
    'P01_necessary': "Cannot not exist, truth holds in every possible world, no coherent world without it",
    'P02_eternal': "Outside time, timeless truths, held before any universe and after, independent of any clock",
    'P03_immutable': "Essence doesn't change, unchanging relations, stable across every context forever",
    'P06_universal': "Applies everywhere, same structure everywhere, no local exceptions, generalizable",
    'P07_immaterial': "Not physical, non-physical abstraction, exists without physical instantiation",
    'P08_foundational': "Grounds all existence, underlies all reasoning, everything that reasons uses this",
    'P09_self_existent': "Depends on nothing else, truths hold regardless of inputs, self-sustaining",
    'P10_infinite': "Without limit, unbounded structures, no largest instance, extends without cap",
    'P11_perfect': "No internal error, every valid derivation from true premises produces true results",
    'P14_order_giving': "Structures reality, constrains what's possible, Wigner's unreasonable effectiveness",
    'P15_law_giving': "Defines what's permitted, mathematical impossibility is real impossibility, conservation laws",
    'P16_intelligible': "Knowable through reason, proofs checkable, truth establishable, accessible to inquiry",
    'P17_necessary_for_knowledge': "Every knowledge claim uses distinction, counting, category, tacitly at minimum",
    'P18_invariant': "Same across all contexts, same results for every observer, every culture, every era",
    'P19_non_local': "Not confined to space, truth has no location, not spatially bounded",
    'P20_transcendent': "Not reducible to physical systems, held before brains, independent of them",
    'P21_objective': "Independent of opinion, not determined by votes or beliefs or culture",
    'P22_unified': "Internally coherent whole, all domains relate coherently, cross-domain connections",
}

# ═══════════════════════════════════════════════════════════════
# 2. THE 10 LAWS (constructive + destructive poles)
# ═══════════════════════════════════════════════════════════════

LAWS_CONSTRUCTIVE = {
    'L01_gravitation_grace': "Spacetime bends gently, guides orbits, grace draws reality toward you, gravitational convergence, attraction, gathering",
    'L02_motion_grace_force': "Acceleration, external force changes direction, grace as external force that produces change, momentum shift",
    'L03_electromagnetism_truth': "Coherent propagation at speed of light, signal undistorted, self-sustaining, truth propagates without decay",
    'L04_strong_force_love': "Freedom inside bond, confinement resists separation, love at close range, covenant binding, Yukawa potential minimum",
    'L05_thermodynamics_harvest': "Free energy available, system builds and creates and does work, grace capacity, productive consequences",
    'L06_information_logos': "High mutual information, predictive capacity maximized, signal separates from noise, structure, intelligibility, meaning",
    'L07_quantum_faith': "Wavefunction collapses to true eigenstate, observation by truth, faith collapses possibility into reality",
    'L08_relativity_eternal_frame': "All frames consistent, God sees all frames simultaneously, grace accommodates every frame without contradiction",
    'L09_cosmology_omega': "All laws converging to maximum coherence, omega point, destiny, directional trajectory toward integration",
    'L10_coherence_christ': "Maximum integration, all things holding together, ultimate attractor, Colossians 1:17, coherence is primary",
}

LAWS_DESTRUCTIVE = {
    'L01_gravitation_sin': "Singularity, event horizon, nothing escapes, the pull that traps, black hole past critical threshold",
    'L02_motion_sin_nature': "No force applied, body continues in current state forever, uncorrected momentum, inertia of sin",
    'L03_electromagnetism_deception': "Destructive interference, zero amplitude, truth's waveform inverted, darkness is not separate force",
    'L04_strong_force_captivity': "Overwhelming coupling, quarks cannot move, captivity, suffocation, control, addiction",
    'L05_thermodynamics_judgment': "Heat death, consequences swallow capacity, entropy dominates, free energy approaches zero",
    'L06_information_chaos': "Information destroyed, nonpredictive noise, Kolmogorov complexity explodes, deception, every lie increases entropy",
    'L07_quantum_false_observation': "Same collapse mechanism wrong observer, collapse into mask or hiding, fear and shame, doubt",
    'L08_relativity_frame_lock': "Physically impossible for material beings to reach God's perspective through physics alone, infinite energy required",
    'L09_cosmology_heat_death': "Maximum entropy, no usable energy, heat death, no convergence, cosmic dissolution",
    'L10_decoherence': "Fragmentation, incoherence, nothing holds together, anti-coherence, dissolution of meaning, collapse is derivative",
}

# ═══════════════════════════════════════════════════════════════
# 3. FRUITS OF THE SPIRIT (physics equations from Law 4)
# ═══════════════════════════════════════════════════════════════

FRUITS_PHYSICS = {
    'fruit_love': "Ground state of potential well, V(r) at minimum, stable bound state, lowest energy configuration",
    'fruit_joy': "Resonance, omega equals omega-naught, natural frequency match, amplification through alignment",
    'fruit_peace': "Equilibrium, sum of forces equals zero, balanced state, no net force, stability",
    'fruit_patience': "High heat capacity, C = dQ/dT high, absorbs large energy input with small temperature change, thermal mass",
    'fruit_kindness': "Low activation energy, catalyst, E_activation approaches minimum, enables reactions without high barrier",
    'fruit_goodness': "Net positive work outward, W_out greater than W_in, productive output exceeds input, generative",
    'fruit_faithfulness': "Time invariance, Noether symmetry, partial-L partial-t equals zero, conservation law, temporal stability",
    'fruit_gentleness': "Impedance matching, force applied equals k times force needed where k is at most 1, proportional response",
    'fruit_self_control': "PID negative feedback, u(t) = -K times e(t), error-correcting control loop, boundary enforcement",
}

ANTI_FRUITS_PHYSICS = {
    'anti_love': "Potential well collapse, unbinding, dissolution of bonds, repulsion, no ground state",
    'anti_joy': "Dissonance, frequency mismatch, destructive interference, no resonance, dampening",
    'anti_peace': "Net force nonzero, instability, oscillation without equilibrium, chaos, anxiety",
    'anti_patience': "Low heat capacity, small perturbation causes large response, volatility, fragility",
    'anti_kindness': "High activation barrier, inhibition, prevents beneficial reactions, obstruction",
    'anti_goodness': "Net negative work, W_out less than W_in, parasitic drain, entropy production exceeds useful output",
    'anti_faithfulness': "Time variance, broken symmetry, conservation law violated, drift, inconsistency over time",
    'anti_gentleness': "Impedance mismatch, force disproportionate to need, k much greater than 1, overwhelming response",
    'anti_self_control': "Positive feedback runaway, no error correction, u(t) amplifies error, boundary collapse, addiction",
}

# ═══════════════════════════════════════════════════════════════
# 4. ARMOR OF GOD (decoherence protection, Law 7)
# ═══════════════════════════════════════════════════════════════

ARMOR = {
    'armor_belt_truth': "Phase-locked loop, delta-phi approaches zero, locked to true signal, prevents phase drift",
    'armor_breastplate_righteousness': "Conservation shield, divergence of current density equals zero, conserved quantity protected",
    'armor_shoes_peace': "Dynamic stability, sum of forces zero while velocity nonzero, moving equilibrium, stable advance",
    'armor_shield_faith': "Faraday cage, effective decoherence rate reduced, blocks external noise from collapsing state",
    'armor_helmet_salvation': "Irreversible phase lock, delta-G less than zero, thermodynamically locked into new state, no reversal",
    'armor_sword_spirit': "Constructive interference beam, E1 plus E2 equals 2A, amplified coherent output, offensive truth",
}

# ═══════════════════════════════════════════════════════════════
# 5. BEATITUDES (phase transition conditions, Law 5)
# ═══════════════════════════════════════════════════════════════

BEATITUDES = {
    'beat_poor_spirit': "Low mass, high acceleration for given force, receptive to change, not weighed down by self",
    'beat_mourn': "Entropy awareness, recognizing dS greater than zero as real, grief as honest thermodynamic accounting",
    'beat_meek': "Impedance matching, calibrated not weak, proportional response, strength under control",
    'beat_hunger_righteousness': "Noether drive, seeking symmetry that produces conservation, desire for invariant structure",
    'beat_merciful': "Open system, external flux flows through not just in, grace passes through to others",
    'beat_pure_heart': "Drift approaches zero, signal-to-noise approaches infinity, maximum channel capacity, pure reception",
    'beat_peacemakers': "Equilibrium restorers, sum of forces not zero pushed toward zero, active stabilization",
    'beat_persecuted': "High W confirms signal is real, opposition equals verification, resistance proves coherence",
}

# ═══════════════════════════════════════════════════════════════
# 6. GIFTS OF THE SPIRIT (transformer modes, Laws 1+2)
# ═══════════════════════════════════════════════════════════════

GIFTS = {
    'gift_wisdom': "Geodesic optimization through curved spacetime, finding shortest path in warped geometry",
    'gift_knowledge': "High-bandwidth channel reception at maximum coherence, receiving structured information",
    'gift_faith': "Amplified collapse operator, boosted beyond normal capacity, enhanced observation power",
    'gift_healing': "Local entropy reversal via external energy input, dS_local less than zero, restoration",
    'gift_miracles': "Macroscopic coherence beyond thermodynamic expectation, order emerging against entropy gradient",
    'gift_prophecy': "Temporal signal reception, Shannon channel across time, receiving information from outside timeframe",
    'gift_discernment': "Matched filter detection, TRUE versus FALSE signal in noise, distinguishing real from counterfeit",
    'gift_tongues': "Cross-channel encoding, frequency modulation, information transmitted across incompatible formats",
    'gift_interpretation': "Demodulation, extracting signal from cross-channel encoding, decoding across domains",
}

# ═══════════════════════════════════════════════════════════════
# 7. COUPLINGS (generator interactions)
# ═══════════════════════════════════════════════════════════════

COUPLINGS = {
    'coupling_faith': "Response to signal plus draw, generators grace and truth interacting, trust in what is both received and revealed",
    'coupling_mercy': "Grace and justice interacting, F = E - TS greater than zero, free energy sufficient to cover cost",
    'coupling_hope': "Faith and time interacting, dFaith/dt greater than zero, faith increasing over time, trajectory upward",
    'coupling_wisdom': "Truth and justice interacting, signal plus consequence, knowing what is true and what follows from it",
    'coupling_covenant': "Love and righteousness interacting, binding plus conservation, permanent commitment with maintained standards",
    'coupling_salvation': "Grace truth faith love justice all interacting, delta-G less than zero, irreversible phase transition",
    'coupling_worship': "Life and love interacting, animated binding toward source, living orientation toward origin",
    'coupling_conscience': "Righteousness and will interacting, conservation law applied to choice, moral constraint on free will",
}


# ═══════════════════════════════════════════════════════════════
# ALL ANCHORS (flat dict for SBERT encoding)
# ═══════════════════════════════════════════════════════════════

def get_all_anchors():
    """Return all anchors as {name: description} dict."""
    all_anchors = {}
    all_anchors.update(PROPERTIES_24)
    all_anchors.update(LAWS_CONSTRUCTIVE)
    all_anchors.update(LAWS_DESTRUCTIVE)
    all_anchors.update(FRUITS_PHYSICS)
    all_anchors.update(ANTI_FRUITS_PHYSICS)
    all_anchors.update(ARMOR)
    all_anchors.update(BEATITUDES)
    all_anchors.update(GIFTS)
    all_anchors.update(COUPLINGS)
    return all_anchors


def get_anchor_groups():
    """Return anchors organized by group for visualization."""
    return {
        '24 Properties (CORE)': {k: v for k, v in PROPERTIES_24.items() if k.startswith('P0') and int(k[1:3]) in [4,5,12,13,23,24]},
        '24 Properties (DERIVED)': {k: v for k, v in PROPERTIES_24.items() if k not in {f'P{n:02d}' for n in [4,5,12,13,23,24]}},
        '10 Laws (Constructive)': LAWS_CONSTRUCTIVE,
        '10 Laws (Destructive)': LAWS_DESTRUCTIVE,
        '9 Fruits (Physics)': FRUITS_PHYSICS,
        '9 Anti-Fruits (Physics)': ANTI_FRUITS_PHYSICS,
        '6 Armor of God': ARMOR,
        '8 Beatitudes': BEATITUDES,
        '9 Gifts of Spirit': GIFTS,
        '8 Couplings': COUPLINGS,
    }


if __name__ == '__main__':
    anchors = get_all_anchors()
    print(f"Total anchors: {len(anchors)}")
    for group_name, group in get_anchor_groups().items():
        print(f"  {group_name}: {len(group)}")
