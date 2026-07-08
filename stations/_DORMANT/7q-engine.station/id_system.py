"""
7Q ID System — All 211 labels, weights, codes, link types.
The complete classification registry as Python data structures.

David Lowe | POF 2828 | March 2026
"""

# ═══════════════════════════════════════════════
# OBJECT TYPE CODES (XX)
# ═══════════════════════════════════════════════

OBJECT_TYPES = {
    "CL": "Claim",
    "AX": "Axiom",
    "TH": "Theorem",
    "LW": "Law",
    "HY": "Hypothesis",
    "EQ": "Equation",
    "MC": "Mechanism",
    "EV": "Evidence",
    "PD": "Prediction",
    "KL": "Kill Condition",
    "DP": "Dependency",
    "IS": "Isomorphism",
    "PP": "Paper",
    "TR": "Theory Mapping",
    "BS": "Blind Spot",
}

# ═══════════════════════════════════════════════
# DOMAIN CODES (DDD)
# ═══════════════════════════════════════════════

DOMAINS = {
    "PHY": "Physics",
    "BIO": "Biology",
    "CHM": "Chemistry",
    "THE": "Theology",
    "PHL": "Philosophy",
    "ECN": "Economics",
    "MTH": "Mathematics",
    "LAW": "Law / Jurisprudence",
    "ETH": "Ethics",
    "PSY": "Psychology",
    "HIS": "History",
    "SOC": "Sociology",
    "LNG": "Linguistics",
    "INF": "Information Theory",
    "CON": "Consciousness",
    "MED": "Medicine",
    "ECL": "Ecology",
    "CSC": "Computer Science",
    "TPH": "Theophysics",
    "UNV": "Universal",
}

# ═══════════════════════════════════════════════
# LINK TYPES
# ═══════════════════════════════════════════════

LINK_TYPES = {
    "DEP": "depends on",
    "SUP": "supported by",
    "PRD": "predicts",
    "KIL": "killed by",
    "ISO": "isomorphic to",
    "CAS": "cascades to",
    "DRV": "derived from",
    "IMP": "implies",
    "CTR": "contradicts",
    "WKN": "weakened by",
    "TST": "tested by",
    "MAP": "maps to (theory)",
    "BLK": "blocked by (blind spot)",
    "GEN": "generates",
    "REP": "replaces / supersedes",
}

# ═══════════════════════════════════════════════
# Q0 — POSTURE
# ═══════════════════════════════════════════════

Q0_MODE = {
    "INVEST":  {"label": "Genuine investigation",    "weight": 1.00},
    "MIXED":   {"label": "Mixed inquiry/advocacy",    "weight": 0.60},
    "ADVOC":   {"label": "Advocacy (biased entry)",   "weight": 0.30},
}

# ═══════════════════════════════════════════════
# Q1 — IDENTITY
# ═══════════════════════════════════════════════

Q1_ENTITY_TYPE = {
    "THEOREM":     {"label": "Formally proven",           "weight": 1.00},
    "LAW":         {"label": "Tested, predictive",        "weight": 0.95},
    "EQUATION":    {"label": "Formalized math",           "weight": 0.85},
    "THEORY":      {"label": "Coherent framework",        "weight": 0.75},
    "MECHANISM":   {"label": "Causal process",            "weight": 0.70},
    "PRINCIPLE":   {"label": "General rule",              "weight": 0.65},
    "OBSERVATION": {"label": "Measured/witnessed",        "weight": 0.60},
    "MODEL":       {"label": "Simplified representation", "weight": 0.55},
    "PATTERN":     {"label": "Recurring regularity",      "weight": 0.50},
    "HYPOTHESIS":  {"label": "Testable guess",            "weight": 0.40},
    "CONJECTURE":  {"label": "Informed guess",            "weight": 0.30},
    "CLAIM":       {"label": "Bare assertion",            "weight": 0.20},
    "POSTULATE":   {"label": "Assumed without proof",     "weight": 0.15},
    "DEFINITION":  {"label": "What a word means",         "weight": None},
}

Q1_AXIOM_CLASS = {
    "PRIMITIVE": {"label": "Cannot be derived",           "weight": 1.00},
    "DERIVED":   {"label": "Follows from other axioms",   "weight": 0.80},
    "BOUNDARY":  {"label": "Defines limits",              "weight": 0.60},
    "DISPUTED":  {"label": "Contested as foundational",   "weight": 0.30},
}

Q1_STATUS = {
    "CANONICAL":   {"label": "Authoritative",      "weight": 1.00},
    "STABLE":      {"label": "Well-established",    "weight": 0.90},
    "PROVISIONAL": {"label": "Accepted conditionally", "weight": 0.65},
    "CANDIDATE":   {"label": "Under evaluation",    "weight": 0.40},
    "DRAFT":       {"label": "Initial proposal",    "weight": 0.20},
    "DEPRECATED":  {"label": "Superseded",           "weight": 0.10},
    "DEAD":        {"label": "Falsified",            "weight": 0.00},
}

Q1_SOURCE = {
    "PEERREV":     {"label": "Peer-reviewed",        "weight": 1.00},
    "ORIGINAL":    {"label": "First proposal",       "weight": 0.85},
    "COMPUTE":     {"label": "Computational",        "weight": 0.80},
    "HISTORIC":    {"label": "Historical record",    "weight": 0.65},
    "SCRIPTURE":   {"label": "Sacred text",          "weight": 0.50, "domain_adjust": {"THE": 0.85}},
    "AI":          {"label": "AI-generated",         "weight": 0.45},
    "FOLK":        {"label": "Common knowledge",     "weight": 0.30},
    "SPECULATIVE": {"label": "Untested conjecture",  "weight": 0.20},
}

# ═══════════════════════════════════════════════
# Q2 — LOCATION
# ═══════════════════════════════════════════════

Q2_SCALE = {
    "QUANTUM": {"label": "Subatomic / Planck"},
    "MICRO":   {"label": "Cellular / molecular"},
    "MESO":    {"label": "Human-scale"},
    "MACRO":   {"label": "Population / societal"},
    "COSMIC":  {"label": "Universe-scale"},
    "META":    {"label": "Beyond physical measurement"},
    "MULTI":   {"label": "Spans multiple scales"},
}

Q2_ISO_STATUS = {
    "CONFIRMED": {"label": "Same equations hold in both domains"},
    "PARALLEL":  {"label": "Qualitative structural match"},
    "ANALOGY":   {"label": "Surface similarity only"},
    "BOUND":     {"label": "No cross-domain presence"},
}

Q2_CROSS_DOMAIN_MULTIPLIER = {
    "ISO3+":  {"label": "ISO-CONFIRMED in 3+ domains",  "multiplier": 1.50},
    "ISO2":   {"label": "ISO-CONFIRMED in 2 domains",   "multiplier": 1.30},
    "PAR3+":  {"label": "ISO-PARALLEL in 3+ domains",   "multiplier": 1.15},
    "PAR2":   {"label": "ISO-PARALLEL in 2 domains",    "multiplier": 1.05},
    "ANA":    {"label": "ISO-ANALOGY only",              "multiplier": 1.00},
    "BOUND":  {"label": "Domain-bound (isolated)",       "multiplier": 0.90},
}

# ═══════════════════════════════════════════════
# Q3 — ASSERTION
# ═══════════════════════════════════════════════

Q3_CLAIM_TYPE = {
    "MATHEMATICAL":   {"label": "X = f(Y,Z)",                 "weight": 1.00},
    "ISOMORPHIC":     {"label": "X and Y have same structure", "weight": 0.90},
    "CAUSAL":         {"label": "X causes Y",                  "weight": 0.90},
    "MECHANISTIC":    {"label": "X works by doing Y",          "weight": 0.85},
    "PREDICTIVE":     {"label": "If X then Y",                 "weight": 0.85},
    "ONTOLOGICAL":    {"label": "X exists / is real",          "weight": 0.80},
    "CONSERVATION":   {"label": "X is conserved",              "weight": 0.80},
    "SYMMETRY":       {"label": "X is invariant under Y",      "weight": 0.80},
    "CONSTITUTIVE":   {"label": "X is made of Y",              "weight": 0.75},
    "EXISTENTIAL":    {"label": "There exists X such that...", "weight": 0.70},
    "ELIMINATIVE":    {"label": "X doesn't exist",             "weight": 0.70},
    "DESCRIPTIVE":    {"label": "X is like this",              "weight": 0.60},
    "CLASSIFICATORY": {"label": "X belongs to category Y",     "weight": 0.50},
    "CORRELATIONAL":  {"label": "X and Y co-occur",            "weight": 0.50},
    "NORMATIVE":      {"label": "X ought to be",               "weight": 0.40},
    "ANALOGICAL":     {"label": "X is like Y",                 "weight": 0.30},
}

Q3_PRECISION = {
    "PRECISE":  {"label": "Exact values, error bars, units", "weight": 1.00},
    "MATH":     {"label": "Formal equations, computable",     "weight": 0.85},
    "DETAILED": {"label": "Testable with specified method",   "weight": 0.65},
    "BASIC":    {"label": "Testable in principle",            "weight": 0.40},
    "VAGUE":    {"label": "Can't be tested",                  "weight": 0.00, "kill": True},
}

Q3_CERTAINTY = {
    "PROVEN":      {"label": "Formally demonstrated",  "weight": 1.00},
    "DERIVED":     {"label": "Follows from proven",    "weight": 0.85},
    "WELLSUP":     {"label": "Strong evidence",        "weight": 0.70},
    "TENTATIVE":   {"label": "Promising but gaps",     "weight": 0.45},
    "SPECULATIVE": {"label": "Interesting but weak",   "weight": 0.20},
    "UNKNOWN":     {"label": "Not enough info",        "weight": 0.10},
}

Q3_SCOPE = {
    "UNIVERSAL":    {"label": "Applies everywhere",    "weight": 1.00},
    "DOMAIN":       {"label": "Within one field",      "weight": 0.70},
    "CONDITIONAL":  {"label": "Under stated conditions","weight": 0.50},
    "LOCAL":        {"label": "Specific case",         "weight": 0.40},
    "HISTORICAL":   {"label": "Applied in the past",   "weight": 0.30},
}

# ═══════════════════════════════════════════════
# Q4 — EVIDENCE
# ═══════════════════════════════════════════════

Q4_EVIDENCE_TYPE = {
    "EXPERIMENTAL":    {"label": "Controlled experiment",    "weight": 1.00},
    "MATHEMATICAL":    {"label": "Formal proof/derivation",  "weight": 1.00},
    "COMPUTATIONAL":   {"label": "Simulation/numerical",     "weight": 0.85},
    "OBSERVATIONAL":   {"label": "Measured but not controlled","weight": 0.80},
    "META_ANALYTIC":   {"label": "Synthesis of studies",     "weight": 0.80},
    "CLINICAL":        {"label": "Medical/therapeutic trial", "weight": 0.75},
    "STATISTICAL":     {"label": "Probabilistic analysis",   "weight": 0.70},
    "SYSTEMATIC":      {"label": "Structured review",        "weight": 0.65},
    "HISTORICAL":      {"label": "Documented past event",    "weight": 0.55},
    "ARCHAEOLOGICAL":  {"label": "Physical artifacts",       "weight": 0.55},
    "CASE_STUDY":      {"label": "Single detailed analysis", "weight": 0.40},
    "SURVEY":          {"label": "Questionnaire/poll",       "weight": 0.40},
    "EXPERT":          {"label": "Specialist opinion",       "weight": 0.35},
    "TESTIMONIAL":     {"label": "Witness account",          "weight": 0.30},
    "PHENOMENOLOGICAL":{"label": "First-person experience",  "weight": 0.25},
    "SCRIPTURAL":      {"label": "Sacred text",              "weight": 0.20, "domain_adjust": {"THE": 0.80}},
    "ANALOGICAL":      {"label": "Pattern from other domain","weight": 0.15},
    "ANECDOTAL":       {"label": "Informal, uncontrolled",   "weight": 0.10},
}

Q4_TIER = {
    "T1": {"label": "Gold standard — replicated, σ > 3",  "weight": 1.00},
    "T2": {"label": "Contested but published",             "weight": 0.60},
    "T3": {"label": "Speculative / unreplicated",          "weight": 0.30},
}

Q4_STRENGTH = {
    "CONCLUSIVE":    {"label": "Would convince hostile expert", "weight": 1.00},
    "STRONG":        {"label": "Would convince neutral expert", "weight": 0.85},
    "MODERATE":      {"label": "Would shift credence",          "weight": 0.65},
    "SUGGESTIVE":    {"label": "Worth investigating",           "weight": 0.40},
    "WEAK":          {"label": "Anecdotal / poorly controlled", "weight": 0.20},
    "CONTESTED":     {"label": "Significant disputes",          "weight": 0.15},
    "INDETERMINATE": {"label": "Can't assess",                  "weight": 0.05},
}

Q4_LINKAGE = {
    "DIRECT":      {"label": "Designed to test this claim", "weight": 1.00},
    "SUFFICIENT":  {"label": "Alone establishes claim",     "weight": 0.95},
    "NECESSARY":   {"label": "Logically required",          "weight": 0.90},
    "INDIRECT":    {"label": "Tests a consequence",         "weight": 0.70},
    "STRUCTURAL":  {"label": "Same formal structure",       "weight": 0.60},
    "CORROBORATE": {"label": "Consistent but not decisive", "weight": 0.50},
    "ANALOGY":     {"label": "Similar pattern",             "weight": 0.25},
    "DECORATIVE":  {"label": "Illustrative only",           "weight": 0.05},
}

Q4_VULNERABILITIES = {
    "WHY_PENALTY":   {"label": "No mechanism (ED < 0.3)",      "penalty": -0.50, "cap": 0.50, "note": "E capped at 50%"},
    "NO_LIVED":      {"label": "No experiential coherence",    "penalty": 0.00,  "flag": True},
    "UNFALSIFIABLE":  {"label": "No kill conditions",           "penalty": 0.00,  "cap_T": 0.60},
    "UNGROUNDED":    {"label": "Assumptions not declared",     "penalty": -0.10},
    "UNDEFINED":     {"label": "Claim type not classified",    "penalty": -0.05},
    "SELECT_BIAS":   {"label": "Evidence cherry-picked",       "penalty": -0.15},
    "SURVIVE_BIAS":  {"label": "Failures not counted",         "penalty": -0.10},
    "CONFIRM_BIAS":  {"label": "Only supporting evidence",     "penalty": -0.15},
    "P_HACK":        {"label": "Statistical significance gamed","penalty": -0.20},
    "SMALL_N":       {"label": "Sample too small",             "penalty": -0.10},
    "SINGLE_SRC":    {"label": "One lab/dataset/author",       "penalty": -0.15},
    "UNREPLICATED":  {"label": "No independent replication",   "penalty": -0.10},
    "CIRCULAR":      {"label": "Evidence assumes conclusion",  "penalty": -0.25},
    "COMPETING":     {"label": "Equally supported by rival",   "penalty": -0.10},
    "AUTHORITY":     {"label": "Expert replaces evidence",     "penalty": -0.15},
    "OBSERVER":      {"label": "Experimenter influenced",      "penalty": -0.15},
    "RECALL":        {"label": "Memory-based distortion",      "penalty": -0.10},
    "PUB_BIAS":      {"label": "Negative results hidden",     "penalty": -0.10},
    "EQUIVOCATION":  {"label": "Key term shifts meaning",     "penalty": -0.15},
    "NON_SEQUITUR":  {"label": "Conclusion doesn't follow",   "penalty": -0.20},
    "HASTY_GEN":     {"label": "Universal from local",        "penalty": -0.15},
    "ANACHRONISM":   {"label": "Modern standards on old data", "penalty": -0.10},
    "TRANSLATION":   {"label": "Disputed translation",        "penalty": -0.10},
    "CULTURAL":      {"label": "One culture's framework",     "penalty": -0.10},
}

# ═══════════════════════════════════════════════
# Q5 — DEPENDENCY
# ═══════════════════════════════════════════════

Q5_TERMINUS = {
    "AXIOM":      {"label": "Genuine foundation",     "weight": 1.00},
    "EMPIRICAL":  {"label": "Grounded in observation", "weight": 0.85},
    "BRUTE":      {"label": "Irreducible fact",        "weight": 0.70},
    "CONSENSUS":  {"label": "Community agreement",     "weight": 0.40},
    "AUTHORITY":  {"label": "'X said so'",             "weight": 0.20},
    "REVELATION": {"label": "Claimed divine source",   "weight": 0.15, "domain_adjust": {"THE": 0.80}},
    "CIRCULAR":   {"label": "Chain loops",             "weight": 0.00, "kill": True},
    "INFINITE":   {"label": "Chain never terminates",  "weight": 0.00, "kill": True},
}

Q5_DERIVATION = {
    "DEDUCTIVE":      {"label": "Follows necessarily"},
    "INDUCTIVE":      {"label": "Generalized from cases"},
    "ABDUCTIVE":      {"label": "Best explanation"},
    "CONSTRUCTIVE":   {"label": "Built from components"},
    "CONTRADICTION":  {"label": "Proof by contradiction"},
    "ANALOGICAL":     {"label": "Imported from parallel"},
    "EMPIRICAL":      {"label": "Grounded in data"},
}

# ═══════════════════════════════════════════════
# Q6 — CONSEQUENCE
# ═══════════════════════════════════════════════

Q6_PREDICTION_TYPE = {
    "DECISIVE":     {"label": "One test settles it",     "weight": 1.00},
    "CONFIRMED":    {"label": "Already came true",        "weight": 0.95},
    "PREDICTIVE":   {"label": "Says what happens next",   "weight": 0.90},
    "CROSSDOMAIN":  {"label": "Consequence in OTHER domain","weight": 0.85},
    "STRUCTURAL":   {"label": "Says what structure must be","weight": 0.75},
    "EXPLANATORY":  {"label": "Says why it works",        "weight": 0.65},
    "RETRODICTIVE": {"label": "Explains past observation", "weight": 0.60},
    "UNTESTED":     {"label": "Can be tested, hasn't been","weight": 0.50},
    "FAILED":       {"label": "Was wrong",                 "weight": 0.00},
}

Q6_COMPETING = {
    "EXCLUSIVE":   {"label": "No other model predicts this",  "weight": 1.00},
    "DISCRIMIN":   {"label": "This model predicts better",    "weight": 0.80},
    "AMBIGUOUS":   {"label": "Multiple models predict equally","weight": 0.40},
    "GENERIC":     {"label": "Almost any model could",         "weight": 0.10},
}

# ═══════════════════════════════════════════════
# Q7 — FALSIFICATION
# ═══════════════════════════════════════════════

Q7_DEATH_TYPES = {
    "SELFREF":    {"label": "Self-refutation — claim destroys itself"},
    "REGRESS":    {"label": "Infinite regress — justification never ends"},
    "EMPIRICAL":  {"label": "Empirical contradiction — reality says no"},
    "INCOHERENT": {"label": "Logical incoherence — A and ¬A"},
    "EXPLAIN":    {"label": "Explanatory failure — competitor is better"},
}

Q7_DEATH_RESULT = {
    "SURVIVES": {"label": "Passed this death test"},
    "DIES":     {"label": "Failed — claim is dead"},
    "WEAKENED": {"label": "Partially damaged"},
    "UNTESTED": {"label": "Not yet applied"},
}

Q7_ROBUSTNESS = {
    "SURVIVED_ADV": {"label": "Attacked and still standing", "weight": 1.00},
    "TESTED":       {"label": "Experiments run",              "weight": 0.85},
    "DERIVED":      {"label": "Follows from tested premises", "weight": 0.70},
    "ARGUED":       {"label": "Defended but not tested",      "weight": 0.45},
    "OPEN":         {"label": "Not yet challenged",           "weight": 0.20},
}

Q7_CASCADE_SCOPE = {
    "LOCAL":     {"label": "Only this claim falls",     "weight": 0.20},
    "DOMAIN":    {"label": "Other claims in domain fall","weight": 0.50},
    "FRAMEWORK": {"label": "Framework-level collapse",   "weight": 1.00},
}

# ═══════════════════════════════════════════════
# CONFIDENCE CLASSES
# ═══════════════════════════════════════════════

CONFIDENCE_CLASSES = [
    {"id": "ESTABLISHED",  "label": "Rock solid",      "min_T": 0.85},
    {"id": "WELLSUP",      "label": "Strong",          "min_T": 0.65},
    {"id": "TENTATIVE",    "label": "Promising",       "min_T": 0.40},
    {"id": "SPECULATIVE",  "label": "Shaky",           "min_T": 0.15},
    {"id": "UNSUPPORTED",  "label": "In trouble",      "min_T": 0.00},
]


def get_confidence_class(t_final: float) -> dict:
    """Return the confidence class for a given T_final score."""
    for cls in CONFIDENCE_CLASSES:
        if t_final >= cls["min_T"]:
            return cls
    return CONFIDENCE_CLASSES[-1]


def get_weight(registry: dict, key: str, domain: str = None) -> float:
    """Get the weight for a label, with optional domain adjustment."""
    entry = registry.get(key, {})
    weight = entry.get("weight", 0.0)
    if domain and "domain_adjust" in entry:
        weight = entry["domain_adjust"].get(domain, weight)
    return weight if weight is not None else 0.0
