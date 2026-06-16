from __future__ import annotations

from .ids import short_hash, slugify


TIE_BREAK = ["E", "C", "G", "K", "M", "T", "R", "F", "S", "Q"]


def score_vector(block_types: list[str], domain_count: int, entity_count: int, text: str = "") -> dict[str, int]:
    has_claims = "CLAIM" in block_types
    has_equations = "EQUATION" in block_types
    has_evidence = "EVIDENCE" in block_types
    has_kill = "KILL_CONDITION" in block_types
    has_domain = "DOMAIN_SHIFT" in block_types
    low = text.lower()
    has_authority_language = any(word in low for word in ["must", "required", "protocol", "rule", "assign", "return", "do not", "only"])
    has_trust_language = any(word in low for word in ["trust", "confidence", "reconstruct", "reconstruction", "risk", "uncertainty", "audit", "verify"])
    has_unification_language = any(word in low for word in ["coherence", "unity", "synthesis", "integration", "unification", "single artifact", "self-contained"])
    has_artifact_disorder = any(word in low for word in ["corrupted", "fragmented", "redacted", "illegible", "damaged", "contradictory artifact", "structural noise", "ambiguous artifact"])
    has_structured_knowledge = any(word in low for word in ["checklist", "definition", "schema", "table", "verify", "confirm", "inspect", "review", "procedure", "fields"])
    return {
        "G": 3 if has_evidence or has_kill or has_authority_language else 0,
        "M": 3 if has_kill or has_equations else 0,
        "E": 3 if has_artifact_disorder else 0,
        "S": 0,
        "T": 3,
        "K": 3 if has_claims or has_equations or has_evidence or has_structured_knowledge else 0,
        "R": 3 if domain_count > 1 or entity_count > 3 else 0,
        "Q": 0,
        "F": 3 if has_kill or has_trust_language else 0,
        "C": 3 if (has_domain and has_claims) or has_unification_language else 0,
    }


def vector_string(vector: dict[str, int]) -> str:
    return "".join(f"{key}{vector[key]}" for key in ["G", "M", "E", "S", "T", "K", "R", "Q", "F", "C"])


def semantic_hash(vector: dict[str, int]) -> str:
    ranked = sorted(vector.keys(), key=lambda key: (-vector[key], TIE_BREAK.index(key)))
    pairs = [(ranked[0], ranked[-1]), (ranked[1], ranked[-2]), (ranked[2], ranked[-3]), (ranked[3], ranked[-4]), (ranked[4], ranked[-5])]
    return "-".join(f"{a}{vector[a]}{b}{vector[b]}" for a, b in pairs)


def build_address(domain: str, named_entity: str, state: str, access: str, use: str, risk: str, vector: dict[str, int]) -> tuple[str, str, str]:
    hash_value = semantic_hash(vector)
    address = f"{domain}/{named_entity}/{state}/{access}/{use}/{risk} :: {vector_string(vector)} :: {hash_value}"
    safe = "__".join([slugify(domain), slugify(named_entity), state, access, use, risk, vector_string(vector), slugify(hash_value)])
    return address, safe, hash_value


def recovery_key(address: str, content_hash: str) -> str:
    return f"LCC-{short_hash(address, content_hash, length=10).upper()}"
