from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def deep_get(obj: Any, *path: str, default: Any = None) -> Any:
    cur = obj
    for key in path:
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur


def first_present(*values: Any, default: Any = None) -> Any:
    for value in values:
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        if isinstance(value, (list, dict)) and not value:
            continue
        return value
    return default


def ensure_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _station_map(raw_station_outputs: dict[str, Any] | None) -> dict[str, Any]:
    if not raw_station_outputs:
        return {}
    normalized: dict[str, Any] = {}
    alias_map = {
        "01": {"01", "1", "raw-metrics", "raw_metrics", "station01", "station_01"},
        "02": {"02", "2", "thesis-claims", "thesis_claims", "claims", "station02", "station_02"},
        "05": {"05", "5", "evidence-overclaim", "evidence_overclaim", "questions", "station05", "station_05"},
        "06": {"06", "6", "domain-classification", "domain_classification", "domains", "station06", "station_06"},
        "07": {"07", "7", "fruits-coherence", "fruits_coherence", "coherence", "station07", "station_07"},
        "08": {"08", "8", "writing-analysis", "writing_analysis", "seo", "station08", "station_08"},
        "09": {"09", "9", "series-continuity", "series_continuity", "series", "station09", "station_09"},
        "12": {"12", "12-highschool-rewrite", "highschool", "highschool_rewrite", "station12", "station_12"},
        "13": {"13", "13-academic-rewrite", "academic", "academic_rewrite", "station13", "station_13"},
        "14": {"14", "14-equation-evidence-map", "equation_map", "formal_surfaces", "station14", "station_14"},
        "15": {"15", "15-media-asset-map", "media_map", "media", "station15", "station_15"},
        "16": {"16", "16-page-integrity", "page_integrity", "integrity", "station16", "station_16"},
    }
    for key, value in raw_station_outputs.items():
        key_lower = str(key).strip().lower()
        placed = False
        for canonical, aliases in alias_map.items():
            if key_lower in aliases:
                normalized[canonical] = value
                placed = True
                break
        if not placed:
            normalized[key] = value
    return normalized


def station_payload(station: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(station, dict):
        return {}
    payload = station.get("payload")
    if isinstance(payload, dict):
        return payload
    return station


def _extract_thesis(st02: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    payload = station_payload(st02)
    thesis = payload.get("thesis") if isinstance(payload.get("thesis"), dict) else {}
    thesis_text = first_present(
        thesis.get("one_sentence"),
        deep_get(payload, "thesis", "statement"),
        payload.get("one_sentence"),
        source.get("thesis"),
        default="",
    )
    return {
        "one_sentence": thesis_text,
        "type": first_present(
            thesis.get("type"),
            thesis.get("thesis_type"),
            payload.get("thesis_type"),
            source.get("thesis_type"),
            default="unknown",
        ),
        "strength": first_present(
            thesis.get("strength"),
            thesis.get("thesis_strength"),
            payload.get("thesis_strength"),
            source.get("thesis_strength"),
            default=None,
        ),
        "location": first_present(
            thesis.get("location"),
            payload.get("location"),
            source.get("thesis_location"),
            default=None,
        ),
    }


def _extract_formal_surfaces(st14: dict[str, Any]) -> dict[str, Any]:
    payload = station_payload(st14)
    coverage = payload.get("coverage_map") if isinstance(payload.get("coverage_map"), dict) else payload
    per_surface = payload.get("surfaces") if isinstance(payload.get("surfaces"), list) else payload.get("per_surface_map", [])
    return {
        "master_equation": first_present(
            coverage.get("master_equation_presence"),
            coverage.get("master_equation"),
            default="unknown",
        ),
        "axioms": ensure_list(first_present(coverage.get("axiom_ids_present"), coverage.get("axioms"), default=[])),
        "lean_refs": ensure_list(first_present(coverage.get("lean_refs_present"), coverage.get("lean_refs"), default=[])),
        "lagrangian_refs": ensure_list(first_present(coverage.get("lagrangian_refs_present"), coverage.get("lagrangian_refs"), default=[])),
        "equation_refs": ensure_list(first_present(coverage.get("equation_refs_present"), coverage.get("equation_refs"), default=[])),
        "proof_hooks": ensure_list(first_present(coverage.get("proof_hooks_present"), coverage.get("proof_hooks"), default=[])),
        "surfaces": per_surface if isinstance(per_surface, list) else [],
    }


def _claim_formal_lookup(st14: dict[str, Any]) -> dict[str, dict[str, Any]]:
    payload = station_payload(st14)
    alignments = payload.get("claim_alignment") if isinstance(payload.get("claim_alignment"), list) else payload.get("alignments", [])
    result: dict[str, dict[str, Any]] = {}
    for row in alignments:
        if not isinstance(row, dict):
            continue
        claim_id = row.get("claim_id")
        if claim_id:
            result[str(claim_id)] = row
    return result


def _extract_claims(st02: dict[str, Any], st05: dict[str, Any], st14: dict[str, Any]) -> list[dict[str, Any]]:
    payload = station_payload(st02)
    claims = payload.get("claims")
    if not isinstance(claims, list):
        claims = []

    q_payload = station_payload(st05)
    overclaim_block = q_payload.get("overclaim") if isinstance(q_payload.get("overclaim"), dict) else q_payload
    overclaim_flags = set(ensure_list(first_present(overclaim_block.get("overclaim_flags"), default=[])))
    formal_by_claim = _claim_formal_lookup(st14)

    result: list[dict[str, Any]] = []
    for idx, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            continue
        claim_id = str(first_present(claim.get("id"), f"C{idx}"))
        formal = formal_by_claim.get(claim_id, {})
        result.append({
            "id": claim_id,
            "claim": first_present(claim.get("claim"), claim.get("text"), default=""),
            "type": first_present(claim.get("type"), claim.get("claim_type"), default="unknown"),
            "proof": first_present(claim.get("proof"), claim.get("support"), default=None),
            "proof_type": first_present(claim.get("proof_type"), default="none"),
            "proof_strength": first_present(claim.get("proof_strength"), claim.get("strength"), default=None),
            "overclaim_risk": first_present(claim.get("overclaim_risk"), default=None),
            "depends_on": ensure_list(first_present(claim.get("depends_on"), claim.get("dependencies"), default=[])),
            "formal_support_type": first_present(formal.get("formal_support_type"), default="none"),
            "formal_support_ref": first_present(formal.get("support_ref"), default=None),
            "formal_alignment_strength": first_present(formal.get("alignment_strength"), default=None),
            "flagged_by_station_05": claim_id in overclaim_flags,
            "support_scope": first_present(
                claim.get("support_scope"),
                claim.get("deferred_support"),
                claim.get("support_location"),
                default="here",
            ),
        })
    return result


def _extract_classification(st06: dict[str, Any]) -> dict[str, Any]:
    payload = station_payload(st06)
    return {
        "primary_domain": first_present(payload.get("primary_domain"), default="unknown"),
        "secondary_domains": ensure_list(first_present(payload.get("secondary_domains"), default=[])),
        "topic_tags": ensure_list(first_present(payload.get("topic_tags"), payload.get("tags"), default=[])),
        "audience_tags": ensure_list(first_present(payload.get("audience_tags"), default=[])),
        "series_tags": ensure_list(first_present(payload.get("series_tags"), default=[])),
        "method_tags": ensure_list(first_present(payload.get("method_tags"), default=[])),
        "cross_domain_bridges": ensure_list(first_present(payload.get("cross_domain_bridges"), default=[])),
        "domain_confidence": first_present(payload.get("domain_confidence"), default=None),
    }


def _extract_media(st15: dict[str, Any]) -> dict[str, Any]:
    payload = station_payload(st15)
    return {
        "scope": first_present(payload.get("media_scope"), default="unknown"),
        "audio": ensure_list(first_present(payload.get("audio_assets"), default=[])),
        "video": ensure_list(first_present(payload.get("video_assets"), default=[])),
        "images": ensure_list(first_present(payload.get("support_images"), default=[])),
        "hero_image": first_present(payload.get("hero_candidate"), default=None),
        "podcast_roles": ensure_list(first_present(payload.get("podcast_roles"), default=[])),
        "media_context_score": first_present(payload.get("media_context_score"), default=None),
        "schema_ready": first_present(payload.get("schema_ready"), default=None),
        "has_minimum_media": first_present(payload.get("has_minimum_media"), default=None),
        "main_gap": first_present(payload.get("main_gap"), default=None),
    }


def _extract_readiness(st07: dict[str, Any], st08: dict[str, Any], st09: dict[str, Any], st16: dict[str, Any]) -> dict[str, Any]:
    p07 = station_payload(st07)
    p08 = station_payload(st08)
    p09 = station_payload(st09)
    p16 = station_payload(st16)
    scores = p08.get("scores") if isinstance(p08.get("scores"), dict) else {}
    return {
        "seo_score": first_present(scores.get("weighted_total"), p08.get("weighted_total"), default=None),
        "seo_pass": first_present(scores.get("pass"), p08.get("pass"), default=None),
        "coherence_score": first_present(p07.get("coherence_score"), default=None),
        "series_status": first_present(p09.get("status"), p09.get("series_status"), default="unknown"),
        "integrity_status": (
            "red" if first_present(p16.get("background_ok"), default=True) is False
            else first_present(p16.get("white_page_risk"), p16.get("status"), default="unknown")
        ),
        "publish_recommendation": first_present(
            p16.get("publish_recommendation"),
            p09.get("publish_recommendation"),
            p08.get("publish_recommendation"),
            default="review",
        ),
    }


def _extract_reading_layers(st12: dict[str, Any], st13: dict[str, Any]) -> dict[str, Any]:
    p12 = station_payload(st12)
    p13 = station_payload(st13)
    return {
        "highschool": {
            "available": bool(p12),
            "status": "available" if p12 else "missing",
            "path": first_present(p12.get("output_path"), p12.get("path"), default=None),
            "fidelity_score": first_present(p12.get("fidelity_score"), default=None),
        },
        "college": {
            "available": True,
            "status": "self",
            "path": None,
            "fidelity_score": None,
        },
        "academic": {
            "available": bool(p13),
            "status": "available" if p13 else "missing",
            "path": first_present(p13.get("output_path"), p13.get("path"), default=None),
            "fidelity_score": first_present(p13.get("fidelity_score"), default=None),
        },
    }


def _extract_ui(st08: dict[str, Any], st11: dict[str, Any] | None = None) -> dict[str, Any]:
    p08 = station_payload(st08)
    p11 = station_payload(st11 or {})
    variants = p08.get("variants") if isinstance(p08.get("variants"), dict) else {}
    return {
        "domain_pills": ensure_list(first_present(p11.get("pills"), default=[])),
        "summary_card": {
            "headline": first_present(
                p08.get("headline"),
                deep_get(p08, "summary_card", "headline"),
                default="Bridge packet assembled from station outputs",
            ),
            "score": first_present(deep_get(p08, "scores", "weighted_total"), default=None),
            "grade": "green" if first_present(deep_get(p08, "scores", "pass"), default=False) else "yellow",
            "best_signal": first_present(deep_get(p08, "fixes", 0), default=None),
            "main_risk": first_present(deep_get(p08, "fixes", 1), default=None),
            "ship_readiness": "ship" if first_present(deep_get(p08, "scores", "pass"), default=False) else "fix_first",
        },
        "review_strip": {
            "needs_human_review": not bool(first_present(deep_get(p08, "scores", "pass"), default=False)),
            "priority": "medium",
            "blocking_issue": first_present(deep_get(p08, "fixes", 0), default=None),
            "fix_scope": "small",
            "time_estimate_minutes": 15,
            "owner_hint": "site",
        },
        "title_variants": variants.get("title", {}) if isinstance(variants.get("title"), dict) else {},
        "description_variants": variants.get("description", {}) if isinstance(variants.get("description"), dict) else {},
    }


def build_bridge_packet(source: dict[str, Any], station_outputs: dict[str, Any]) -> dict[str, Any]:
    stations = _station_map(station_outputs)
    packet = {
        "packet_version": "1.0",
        "generated_at": utc_now_iso(),
        "slug": source.get("slug", "unknown-slug"),
        "series_slug": source.get("series_slug", "unknown-series"),
        "source_path": source.get("source_path"),
        "content_type": first_present(source.get("content_type"), default="paper"),
        "title": first_present(source.get("title"), source.get("headline"), default="Untitled"),
        "description": first_present(source.get("description"), source.get("summary"), default=""),
        "url": first_present(source.get("url"), source.get("canonical_url"), default=None),
        "author": first_present(source.get("author"), default="David Lowe"),
        "thesis": _extract_thesis(stations.get("02", {}), source),
        "claims": _extract_claims(stations.get("02", {}), stations.get("05", {}), stations.get("14", {})),
        "formal_surfaces": _extract_formal_surfaces(stations.get("14", {})),
        "classification": _extract_classification(stations.get("06", {})),
        "media": _extract_media(stations.get("15", {})),
        "readiness": _extract_readiness(
            stations.get("07", {}),
            stations.get("08", {}),
            stations.get("09", {}),
            stations.get("16", {}),
        ),
        "reading_layers": _extract_reading_layers(stations.get("12", {}), stations.get("13", {})),
        "ui": _extract_ui(stations.get("08", {}), stations.get("11", {})),
        "station_presence": {k: True for k in stations.keys()},
    }
    return packet


def _support_state_for_claim(claim: dict[str, Any]) -> str:
    explicit = first_present(claim.get("support_state"), default=None)
    if explicit:
        return str(explicit)
    scope = str(first_present(claim.get("support_scope"), default="here")).lower()
    strength = claim.get("proof_strength")
    formal_type = str(first_present(claim.get("formal_support_type"), default="none")).lower()

    if scope in {"series", "later_in_series", "supported_elsewhere_in_series"}:
        return "supported_elsewhere_in_series"
    if scope in {"external", "outside_series", "supported_elsewhere_outside_series"}:
        return "supported_elsewhere_outside_series"

    if isinstance(strength, (int, float)) and strength >= 7:
        return "supported_here"
    if formal_type not in {"", "none", "unknown"}:
        return "supported_here"
    if isinstance(strength, (int, float)) and 4 <= strength <= 6:
        return "implied_not_yet_supported"
    if isinstance(strength, (int, float)) and strength <= 3:
        return "unsupported"
    if claim.get("proof") or claim.get("proof_type") not in {None, "", "none"}:
        return "implied_not_yet_supported"
    return "unknown"


def build_integrity_packet(bridge_packet: dict[str, Any], station_outputs: dict[str, Any]) -> dict[str, Any]:
    stations = _station_map(station_outputs)
    p05 = station_payload(stations.get("05", {}))
    questions = ensure_list(first_present(p05.get("questions"), p05.get("items"), default=[]))

    claim_ladder = []
    for claim in bridge_packet.get("claims", []):
        support_state = _support_state_for_claim(claim)
        claim_ladder.append({
            "id": claim.get("id"),
            "claim": claim.get("claim"),
            "support_state": support_state,
            "proof_strength": claim.get("proof_strength"),
            "overclaim_risk": claim.get("overclaim_risk"),
            "depends_on": ensure_list(claim.get("depends_on")),
            "formal_support_type": claim.get("formal_support_type"),
            "formal_support_ref": claim.get("formal_support_ref"),
            "weakness_note": (
                "Flagged by overclaim station"
                if claim.get("flagged_by_station_05")
                else None
            ),
        })

    weak_claims = [c for c in claim_ladder if c["support_state"] in {"unsupported", "implied_not_yet_supported", "unknown"}]
    deferred_claims = [c for c in claim_ladder if c["support_state"] in {"supported_elsewhere_in_series", "supported_elsewhere_outside_series"}]

    strongest = None
    if claim_ladder:
        strongest = max(claim_ladder, key=lambda c: first_present(c.get("proof_strength"), default=-1) or -1)
    weakest = weak_claims[0] if weak_claims else None

    recommendation = bridge_packet.get("readiness", {}).get("publish_recommendation", "review")
    if weak_claims:
        if recommendation in {"ship", "review", "unknown", None}:
            recommendation = "fix_first"

    return {
        "packet_version": "1.0",
        "generated_at": utc_now_iso(),
        "slug": bridge_packet.get("slug"),
        "series_slug": bridge_packet.get("series_slug"),
        "thesis_read": {
            "one_sentence": deep_get(bridge_packet, "thesis", "one_sentence"),
            "type": deep_get(bridge_packet, "thesis", "type"),
            "strength": deep_get(bridge_packet, "thesis", "strength"),
        },
        "claim_ladder": claim_ladder,
        "question_queue": questions[:10],
        "proof_evidence_walk": {
            "claim_count": len(claim_ladder),
            "supported_here_count": sum(1 for c in claim_ladder if c["support_state"] == "supported_here"),
            "deferred_support_count": len(deferred_claims),
            "weak_claim_count": len(weak_claims),
        },
        "structural_verdict": {
            "strongest_part": strongest.get("claim") if strongest else None,
            "weakest_joint": weakest.get("claim") if weakest else None,
            "must_revise_first": weakest.get("id") if weakest else None,
            "publish_recommendation": recommendation,
        },
        "summary_card": {
            "headline": f"{len(claim_ladder)} claims mapped; {len(weak_claims)} need stronger support",
            "score": bridge_packet.get("readiness", {}).get("coherence_score"),
            "grade": "yellow" if weak_claims else "green",
            "best_signal": strongest.get("claim") if strongest else None,
            "main_risk": weakest.get("claim") if weakest else None,
            "ship_readiness": recommendation,
        },
        "review_strip": {
            "needs_human_review": bool(weak_claims or questions),
            "priority": "high" if weak_claims else "medium",
            "blocking_issue": weakest.get("claim") if weakest else None,
            "fix_scope": "medium" if weak_claims else "small",
            "time_estimate_minutes": 20 if weak_claims else 10,
            "owner_hint": "writer",
        },
    }


def build_schema_projection(bridge_packet: dict[str, Any], integrity_packet: dict[str, Any] | None = None) -> dict[str, Any]:
    classification = bridge_packet.get("classification", {})
    media = bridge_packet.get("media", {})
    article_type = "ScholarlyArticle" if bridge_packet.get("content_type") in {"paper", "academic", "scholarly"} else "Article"
    about = [classification.get("primary_domain")] + ensure_list(classification.get("secondary_domains"))
    about = [x for x in about if x]
    keywords = []
    for key in ("topic_tags", "method_tags", "series_tags"):
        keywords.extend([str(x) for x in ensure_list(classification.get(key)) if x])

    has_part = []
    for asset in ensure_list(media.get("audio")):
        if isinstance(asset, dict):
            has_part.append({"@type": "AudioObject", **deepcopy(asset)})
    for asset in ensure_list(media.get("video")):
        if isinstance(asset, dict):
            has_part.append({"@type": "VideoObject", **deepcopy(asset)})
    hero = media.get("hero_image")
    if isinstance(hero, dict):
        has_part.append({"@type": "ImageObject", **deepcopy(hero)})

    payload = {
        "@context": {
            "@vocab": "https://schema.org/",
            "pof": "https://faiththruphysics.com/schema/",
        },
        "@type": article_type,
        "headline": bridge_packet.get("title"),
        "description": bridge_packet.get("description"),
        "author": {"@type": "Person", "name": bridge_packet.get("author", "David Lowe")},
        "url": bridge_packet.get("url"),
        "keywords": sorted(set(keywords)),
        "about": about,
        "hasPart": has_part,
        "pof:packetVersion": bridge_packet.get("packet_version"),
        "pof:thesis": bridge_packet.get("thesis"),
        "pof:formalSurfaces": bridge_packet.get("formal_surfaces"),
        "pof:claims": bridge_packet.get("claims"),
        "pof:classification": bridge_packet.get("classification"),
        "pof:readiness": bridge_packet.get("readiness"),
        "pof:readingLayers": bridge_packet.get("reading_layers"),
    }
    if integrity_packet:
        payload["pof:integrity"] = {
            "structuralVerdict": integrity_packet.get("structural_verdict"),
            "summaryCard": integrity_packet.get("summary_card"),
        }
    return payload


def build_packet_bundle(source: dict[str, Any], station_outputs: dict[str, Any]) -> dict[str, Any]:
    bridge = build_bridge_packet(source, station_outputs)
    integrity = build_integrity_packet(bridge, station_outputs)
    schema = build_schema_projection(bridge, integrity)
    return {
        "bridge_packet": bridge,
        "integrity_packet": integrity,
        "schema_packet": schema,
    }
