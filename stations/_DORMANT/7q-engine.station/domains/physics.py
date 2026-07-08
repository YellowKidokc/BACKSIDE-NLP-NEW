"""
Physics Domain Plugin — pre-loaded knowledge for physics claims.

Known isomorphisms, subdomains, standard theories, common dependencies.
Used by intake.py and destroy.py to offer smart defaults.

David Lowe | POF 2828 | March 2026
"""

# ═══════════════════════════════════════════════
# PHYSICS SUBDOMAINS
# ═══════════════════════════════════════════════

SUBDOMAINS = {
    "CM":   "Classical Mechanics",
    "QM":   "Quantum Mechanics",
    "GR":   "General Relativity",
    "SR":   "Special Relativity",
    "SM":   "Standard Model (Particle Physics)",
    "TD":   "Thermodynamics / Statistical Mechanics",
    "EM":   "Electromagnetism",
    "NF":   "Nuclear / Strong Force",
    "WF":   "Weak Force",
    "COS":  "Cosmology",
    "AST":  "Astrophysics",
    "QFT":  "Quantum Field Theory",
    "QG":   "Quantum Gravity",
    "CMT":  "Condensed Matter",
    "OPT":  "Optics",
    "FLD":  "Fluid Dynamics",
    "PLS":  "Plasma Physics",
    "BIO":  "Biophysics",
    "TPH":  "Theophysics",
}

# ═══════════════════════════════════════════════
# STANDARD THEORIES (common dependency anchors)
# ═══════════════════════════════════════════════

STANDARD_THEORIES = {
    "newton_gravity":     {"name": "Newtonian Gravity",              "status": "CANONICAL", "subdomain": "CM"},
    "einstein_gr":        {"name": "General Relativity",             "status": "CANONICAL", "subdomain": "GR"},
    "einstein_sr":        {"name": "Special Relativity",             "status": "CANONICAL", "subdomain": "SR"},
    "maxwell_em":         {"name": "Maxwell's Equations",            "status": "CANONICAL", "subdomain": "EM"},
    "schrodinger":        {"name": "Schrödinger Equation",           "status": "CANONICAL", "subdomain": "QM"},
    "dirac":              {"name": "Dirac Equation",                 "status": "CANONICAL", "subdomain": "QFT"},
    "standard_model":     {"name": "Standard Model of Particles",    "status": "CANONICAL", "subdomain": "SM"},
    "lambda_cdm":         {"name": "ΛCDM Cosmology",                "status": "CANONICAL", "subdomain": "COS"},
    "thermodynamics":     {"name": "Laws of Thermodynamics",         "status": "CANONICAL", "subdomain": "TD"},
    "boltzmann":          {"name": "Boltzmann Statistical Mechanics","status": "CANONICAL", "subdomain": "TD"},
    "kepler":             {"name": "Kepler's Laws",                  "status": "CANONICAL", "subdomain": "CM"},
    "noether":            {"name": "Noether's Theorem",              "status": "CANONICAL", "subdomain": "CM"},
    "chi_field":          {"name": "χ-Field Theory",                 "status": "CANDIDATE", "subdomain": "TPH"},
    "master_equation":    {"name": "Theophysics Master Equation",    "status": "CANDIDATE", "subdomain": "TPH"},
    "grace_source":       {"name": "Grace Source Term (J_grace)",    "status": "CANDIDATE", "subdomain": "TPH"},
    "minimal_chi_action": {"name": "Minimal χ-Field Action (S_χ)",  "status": "CANDIDATE", "subdomain": "TPH"},
}

# ═══════════════════════════════════════════════
# KNOWN ISOMORPHISMS (cross-domain mappings)
# ═══════════════════════════════════════════════

KNOWN_ISOMORPHISMS = [
    {
        "id": "ISO-001",
        "name": "Beer-Lambert ↔ Sin attenuation",
        "domains": ["PHY", "THE"],
        "status": "CONFIRMED",
        "confidence": 0.85,
        "note": "Exponential decay in optical absorption maps to spiritual attenuation",
    },
    {
        "id": "ISO-037",
        "name": "Beer-Lambert isomorphism (full)",
        "domains": ["PHY", "THE", "INF"],
        "status": "CONFIRMED",
        "confidence": 0.90,
        "note": "High confidence cross-domain mapping — strongest piece",
    },
    {
        "id": "ISO-002",
        "name": "Shannon entropy ↔ Logos capacity",
        "domains": ["INF", "THE"],
        "status": "CONFIRMED",
        "confidence": 0.80,
        "note": "Information channel capacity maps to truth transmission",
    },
    {
        "id": "ISO-003",
        "name": "Gravity ↔ Grace",
        "domains": ["PHY", "THE"],
        "status": "PARALLEL",
        "confidence": 0.70,
        "note": "Attractive universal force → universal unmerited sustaining",
    },
    {
        "id": "ISO-004",
        "name": "Strong Force ↔ Love",
        "domains": ["PHY", "THE"],
        "status": "PARALLEL",
        "confidence": 0.65,
        "note": "Short-range binding → sacrificial covenant binding",
    },
    {
        "id": "ISO-005",
        "name": "Entropy ↔ Judgment",
        "domains": ["PHY", "THE"],
        "status": "PARALLEL",
        "confidence": 0.70,
        "note": "Irreversible disorder increase → irreversible moral accounting",
    },
    {
        "id": "ISO-006",
        "name": "Weak Force ↔ Sin",
        "domains": ["PHY", "THE"],
        "status": "PARALLEL",
        "confidence": 0.55,
        "note": "Flavor-changing decay → identity-corrupting moral decay",
    },
    {
        "id": "ISO-007",
        "name": "Electromagnetism ↔ Truth",
        "domains": ["PHY", "THE"],
        "status": "PARALLEL",
        "confidence": 0.60,
        "note": "Light/signal propagation → truth/revelation transmission",
    },
    {
        "id": "ISO-008",
        "name": "Quantum Mechanics ↔ Faith",
        "domains": ["PHY", "THE"],
        "status": "PARALLEL",
        "confidence": 0.50,
        "note": "Superposition/collapse → possibility/commitment",
    },
]

# ═══════════════════════════════════════════════
# SYMMETRY PAIRS (canonical)
# ═══════════════════════════════════════════════

SYMMETRY_PAIRS = [
    {"pair": "G↔T", "laws": ("L01", "L05"), "names": ("Gravity/Grace", "Entropy/Judgment"),
     "type": "coherence vs decay"},
    {"pair": "S↔F", "laws": ("L04", "L09"), "names": ("Strong/Love", "Weak/Sin"),
     "type": "binding vs breaking"},
    {"pair": "E↔K", "laws": ("L03", "L06"), "names": ("EM/Truth", "Info/Logos"),
     "type": "content vs capacity"},
    {"pair": "M↔Q", "laws": ("L02", "L08"), "names": ("Mass/Meaning", "Quantum/Faith"),
     "type": "actual vs possible"},
    {"pair": "R↔C", "laws": ("L07", "L10"), "names": ("Relativity/Relationship", "Coherence/Christ"),
     "type": "frame vs unity"},
]

# ═══════════════════════════════════════════════
# COMMON KILL TESTS (physics-specific)
# ═══════════════════════════════════════════════

PHYSICS_KILL_TESTS = [
    {
        "name": "Conservation violation",
        "death_type": "EMPIRICAL",
        "question": "Does this violate energy, momentum, charge, or baryon number conservation?",
    },
    {
        "name": "Lorentz violation",
        "death_type": "EMPIRICAL",
        "question": "Does this require a preferred frame or violate Lorentz invariance?",
    },
    {
        "name": "Dimensional inconsistency",
        "death_type": "INCOHERENT",
        "question": "Do the units/dimensions work out on both sides of the equation?",
    },
    {
        "name": "Ghost/tachyon instability",
        "death_type": "INCOHERENT",
        "question": "Does the theory produce negative-norm states or superluminal propagation?",
    },
    {
        "name": "Thermodynamic violation",
        "death_type": "EMPIRICAL",
        "question": "Does this violate the second law of thermodynamics in a closed system?",
    },
    {
        "name": "Observational contradiction",
        "death_type": "EMPIRICAL",
        "question": "Does existing data directly contradict a specific prediction?",
    },
    {
        "name": "Explanatory supersession",
        "death_type": "EXPLAIN",
        "question": "Does an existing theory explain the same data more simply?",
    },
    {
        "name": "Self-refutation check",
        "death_type": "SELFREF",
        "question": "Does the claim, if true, undermine its own premises?",
    },
    {
        "name": "Infinite regress check",
        "death_type": "REGRESS",
        "question": "Does the explanation require an infinite chain of prior explanations?",
    },
    {
        "name": "Fine-tuning / naturalness",
        "death_type": "EXPLAIN",
        "question": "Does this require extreme fine-tuning of parameters without explanation?",
    },
]

# ═══════════════════════════════════════════════
# EXPERIMENTAL ANCHORS (known key experiments)
# ═══════════════════════════════════════════════

EXPERIMENTAL_ANCHORS = {
    "desi_dr2": {
        "name": "DESI DR2",
        "sigma": 4.2,
        "claim": "Evolving dark energy (w₀ ≠ -1)",
        "status": "published",
        "relevance": "Consistent with χ-field predictions",
    },
    "euclid_oct2026": {
        "name": "Euclid (October 2026)",
        "sigma": None,
        "claim": "fσ₈ growth rate measurement",
        "status": "upcoming",
        "relevance": "Decisive test for χ-field",
    },
    "pear_lab": {
        "name": "PEAR Lab",
        "sigma": 6.0,
        "claim": "Consciousness-QM coupling",
        "status": "published",
        "relevance": "Supports Q8/consciousness channel",
    },
    "gcp": {
        "name": "Global Consciousness Project",
        "sigma": 6.0,
        "claim": "Collective consciousness effects",
        "status": "published",
        "relevance": "Supports collective χ-field",
    },
    "cassini": {
        "name": "Cassini mission",
        "sigma": None,
        "claim": "|ξ| ≲ 10⁵ constraint on scalar-tensor coupling",
        "status": "published",
        "relevance": "Bounds χ-field coupling constant",
    },
    "planck_cmb": {
        "name": "Planck CMB",
        "sigma": None,
        "claim": "Precision cosmological parameters",
        "status": "published",
        "relevance": "Background constraints on any dark energy model",
    },
}


def get_relevant_isomorphisms(domains: list) -> list:
    """Return isomorphisms that involve any of the given domains."""
    domain_set = set(domains)
    return [iso for iso in KNOWN_ISOMORPHISMS
            if domain_set.intersection(iso["domains"])]


def get_kill_tests() -> list:
    """Return all physics-specific kill tests."""
    return PHYSICS_KILL_TESTS


def suggest_dependencies(subdomain: str) -> list:
    """Suggest standard theories that are likely dependencies for a given subdomain."""
    mapping = {
        "CM":  ["newton_gravity", "noether"],
        "QM":  ["schrodinger"],
        "GR":  ["einstein_gr", "einstein_sr"],
        "SR":  ["einstein_sr"],
        "SM":  ["standard_model", "dirac"],
        "TD":  ["thermodynamics", "boltzmann"],
        "EM":  ["maxwell_em"],
        "COS": ["lambda_cdm", "einstein_gr"],
        "QFT": ["dirac", "standard_model"],
        "TPH": ["chi_field", "master_equation", "grace_source"],
    }
    keys = mapping.get(subdomain, [])
    return [STANDARD_THEORIES[k] for k in keys if k in STANDARD_THEORIES]
