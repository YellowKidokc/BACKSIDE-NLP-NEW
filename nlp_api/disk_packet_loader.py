from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from packet_bridge import build_packet_bundle


DEFAULT_SITE_DATA_DIR = Path(r"D:\GitHub\faiththruphysics-site-data")
DEFAULT_SITE_DIR = Path(r"D:\GitHub\faiththruphysics-site")


def _read_json(path: Path | None) -> dict[str, Any]:
    if not path or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _read_text(path: Path | None) -> str:
    if not path or not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _pick_top_domains(summary: dict[str, Any], domain_scan: dict[str, Any]) -> tuple[str, list[str]]:
    weighted: list[tuple[str, float]] = []
    for row in summary.get("domain_classification", []) if isinstance(summary.get("domain_classification"), list) else []:
        tag = row.get("tag")
        pct = row.get("pct", 0)
        if tag:
            weighted.append((str(tag), float(pct)))
    scan_domains = domain_scan.get("domains", {}) if isinstance(domain_scan.get("domains"), dict) else {}
    for tag, pct in scan_domains.items():
        weighted.append((str(tag), float(pct)))

    totals: dict[str, float] = {}
    for tag, pct in weighted:
        totals[tag] = totals.get(tag, 0.0) + pct

    ordered = [k for k, _ in sorted(totals.items(), key=lambda kv: kv[1], reverse=True)]
    primary = ordered[0] if ordered else "unknown"
    secondary = ordered[1:4]
    return primary, secondary


def _build_source(series_slug: str, article_slug: str, summary: dict[str, Any], source_path: str) -> dict[str, Any]:
    description = summary.get("short_summary") or summary.get("one_sentence_hook") or ""
    return {
        "slug": article_slug,
        "external_slug": summary.get("slug"),
        "series_slug": series_slug,
        "source_path": source_path,
        "content_type": "paper",
        "title": summary.get("title") or article_slug.replace("-", " ").title(),
        "headline": summary.get("title") or article_slug.replace("-", " ").title(),
        "description": description,
        "summary": summary.get("executive_summary") or description,
        "thesis": summary.get("key_claim") or summary.get("one_sentence_hook"),
        "thesis_type": "framework",
        "thesis_strength": 8,
        "canonical_url": f"https://faiththruphysics.com/{source_path}",
        "url": f"https://faiththruphysics.com/{source_path}",
        "author": "David Lowe",
    }


def _build_station_02(summary: dict[str, Any], framework: dict[str, Any]) -> dict[str, Any]:
    key_claim = summary.get("key_claim") or summary.get("one_sentence_hook") or ""
    methodology = summary.get("methodology") or ""
    strength = framework.get("framework_alignment_score", {}).get("total")
    claim_strength = round(float(strength) / 10, 1) if isinstance(strength, (int, float)) else 8.0
    return {
        "payload": {
            "thesis": {
                "one_sentence": key_claim,
                "type": "framework",
                "strength": claim_strength,
                "location": "summary.key_claim",
            },
            "claims": [
                {
                    "id": "C1",
                    "claim": key_claim,
                    "type": "core",
                    "proof": methodology,
                    "proof_type": "summary+framework",
                    "proof_strength": claim_strength,
                    "support_scope": "here",
                    "depends_on": [],
                }
            ],
        }
    }


def _build_station_06(summary: dict[str, Any], domain_scan: dict[str, Any]) -> dict[str, Any]:
    primary, secondary = _pick_top_domains(summary, domain_scan)
    tags = [row.get("tag") for row in summary.get("domain_classification", []) if isinstance(row, dict) and row.get("tag")]
    jurisdictions = []
    jurisdiction_block = domain_scan.get("jurisdiction", {}) if isinstance(domain_scan.get("jurisdiction"), dict) else {}
    for key, value in jurisdiction_block.items():
        if isinstance(value, (int, float)) and value > 0:
            jurisdictions.append(f"{key}:{value}")
    return {
        "payload": {
            "primary_domain": primary,
            "secondary_domains": secondary,
            "topic_tags": tags,
            "method_tags": [summary.get("methodology")] if summary.get("methodology") else [],
            "series_tags": [summary.get("series_context")] if summary.get("series_context") else [],
            "cross_domain_bridges": jurisdictions,
            "domain_confidence": 0.8 if primary != "unknown" else 0.3,
        }
    }


def _build_station_07(framework: dict[str, Any], graph: dict[str, Any]) -> dict[str, Any]:
    score = framework.get("framework_alignment_score", {}).get("total")
    graph_score = graph.get("graph_summary", {}).get("connectivity_score")
    coherence = None
    if isinstance(score, (int, float)):
        coherence = round(float(score), 1)
    elif isinstance(graph_score, (int, float)):
        coherence = round(float(graph_score) * 10, 1)
    return {
        "payload": {
            "coherence_score": coherence,
            "framework_alignment_score": framework.get("framework_alignment_score", {}),
            "connectivity_score": graph.get("graph_summary", {}).get("connectivity_score"),
            "diagnosis": graph.get("graph_summary", {}).get("one_sentence"),
        }
    }


def _build_station_12_13(reading_layers: dict[str, Any], level: str) -> dict[str, Any]:
    path_key = {
        "12": "highschool_path",
        "13": "academic_path",
    }[level]
    shell_key = {
        "12": "highschool_shell_path",
        "13": "academic_shell_path",
    }[level]
    return {
        "payload": {
            "output_path": reading_layers.get(path_key),
            "path": reading_layers.get(shell_key) or reading_layers.get(path_key),
            "fidelity_score": 0.8,
        }
    }


def _build_station_14(
    article_slug: str,
    framework: dict[str, Any],
    graph: dict[str, Any],
    mtl_items: list[dict[str, Any]],
) -> dict[str, Any]:
    axioms = framework.get("axiom_alignment", {}).get("axioms_touched", [])
    lean_module = framework.get("lean_connection", {}).get("relevant_lean_module")
    equation_refs = [item.get("eq_id") for item in mtl_items if item.get("eq_id")]
    laws = []
    for bucket in ("explicit", "implicit"):
        laws.extend(framework.get("laws_invoked", {}).get(bucket, []))

    claim_alignment = []
    if framework:
        claim_alignment.append(
            {
                "claim_id": "C1",
                "formal_support_type": "framework_alignment",
                "support_ref": article_slug,
                "alignment_strength": framework.get("framework_alignment_score", {}).get("total"),
            }
        )

    surfaces = []
    for item in mtl_items:
        surfaces.append(
            {
                "eq_id": item.get("eq_id"),
                "paper_ref": item.get("paper_ref"),
                "difficulty": item.get("difficulty"),
            }
        )

    return {
        "payload": {
            "coverage_map": {
                "master_equation_presence": "implicit" if equation_refs else "unknown",
                "axiom_ids_present": axioms,
                "lean_refs_present": [lean_module] if lean_module else [],
                "lagrangian_refs_present": ["minimal-chi-field-action"] if equation_refs else [],
                "equation_refs_present": equation_refs,
                "proof_hooks_present": laws,
            },
            "claim_alignment": claim_alignment,
            "surfaces": surfaces,
            "graph_summary": graph.get("graph_summary", {}),
        }
    }


def _build_station_15(
    article_slug: str,
    series_slug: str,
    site_data_dir: Path,
) -> dict[str, Any]:
    audio_assets = []
    outbox = site_data_dir / "assets" / "OUTBOX"
    for suffix in (".canonical.mp3", ".mp3"):
        path = outbox / f"{article_slug}{suffix}"
        if path.exists():
            audio_assets.append(
                {
                    "name": path.name,
                    "contentUrl": str(path),
                    "encodingFormat": path.suffix.lstrip("."),
                    "role": "deep_dive" if "canonical" in path.name else "audio",
                }
            )
    m4a = site_data_dir / "assets" / "audio" / f"{article_slug}.m4a"
    if m4a.exists():
        audio_assets.append(
            {
                "name": m4a.name,
                "contentUrl": str(m4a),
                "encodingFormat": "m4a",
                "role": "archive_audio",
            }
        )

    return {
        "payload": {
            "media_scope": "article",
            "audio_assets": audio_assets,
            "video_assets": [],
            "support_images": [],
            "hero_candidate": None,
            "podcast_roles": ["deep_dive"] if audio_assets else [],
            "media_context_score": 6 if audio_assets else 0,
            "schema_ready": bool(audio_assets),
            "has_minimum_media": bool(audio_assets),
            "main_gap": None if audio_assets else f"missing article media for {series_slug}/{article_slug}",
        }
    }


def _select_mtl_items(site_dir: Path, article_slug: str) -> list[dict[str, Any]]:
    path = site_dir / "shared" / "data" / "mtl-equations-canonical.json"
    payload = _read_json(path)
    items = payload.get("items", []) if isinstance(payload.get("items"), list) else []
    matches = [item for item in items if isinstance(item, dict) and item.get("source_file") == article_slug]
    # Prefer the canonical article-specific rows and collapse historical duplicates.
    matches.sort(
        key=lambda item: (
            0 if item.get("source") == "Consciousness_Equations" else 1,
            0 if item.get("difficulty") == "advanced" else 1,
            str(item.get("eq_id", "")),
        )
    )
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in matches:
        key = (str(item.get("eq_id", "")), str(item.get("latex_hash", "")))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def load_article_fixture(
    series_slug: str,
    article_slug: str,
    site_data_dir: Path = DEFAULT_SITE_DATA_DIR,
    site_dir: Path = DEFAULT_SITE_DIR,
) -> dict[str, Any]:
    source_path = f"{series_slug}/{article_slug}.html"
    summary_path = site_data_dir / "_summaries" / "by-source" / series_slug / "root" / f"{article_slug}.summary.json"
    reading_layers_path = site_data_dir / series_slug / "reading_layers" / f"{article_slug}.json"
    framework_path = site_data_dir / "framework-alignment" / series_slug / f"{article_slug}.json"
    graph_path = site_data_dir / "knowledge-graph" / series_slug / f"{article_slug}.json"
    domain_scan_path = site_data_dir / "domain-scan" / series_slug / f"{article_slug}.json"

    summary = _read_json(summary_path)
    reading_layers = _read_json(reading_layers_path)
    framework = _read_json(framework_path)
    graph = _read_json(graph_path)
    domain_scan = _read_json(domain_scan_path)
    mtl_items = _select_mtl_items(site_dir, article_slug)

    source = _build_source(series_slug, article_slug, summary, source_path)

    station_outputs: dict[str, Any] = {}
    # Canonical station files when available
    direct_station_paths = {
        "01": site_data_dir / "APIs" / "outputs" / "01-raw-metrics" / f"{article_slug}.canonical.json",
        "08": site_data_dir / "APIs" / "outputs" / "08-writing-analysis" / f"{series_slug}--{article_slug}.seo.json",
        "09": site_data_dir / "APIs" / "outputs" / "09-series-continuity" / f"{series_slug}--{article_slug}.series.json",
        "10": site_data_dir / "APIs" / "outputs" / "10-final-report" / f"{series_slug}--{article_slug}.report.json",
    }
    for station_id, path in direct_station_paths.items():
        loaded = _read_json(path)
        if loaded:
            station_outputs[station_id] = loaded

    # Normalized/synthesized stations from the actual surrounding ecosystem.
    station_outputs["02"] = _build_station_02(summary, framework)
    station_outputs["06"] = _build_station_06(summary, domain_scan)
    station_outputs["07"] = _build_station_07(framework, graph)
    station_outputs["12"] = _build_station_12_13(reading_layers, "12")
    station_outputs["13"] = _build_station_12_13(reading_layers, "13")
    station_outputs["14"] = _build_station_14(article_slug, framework, graph, mtl_items)
    station_outputs["15"] = _build_station_15(article_slug, series_slug, site_data_dir)

    evidence_files = {
        "summary": str(summary_path) if summary_path.exists() else None,
        "reading_layers": str(reading_layers_path) if reading_layers_path.exists() else None,
        "framework_alignment": str(framework_path) if framework_path.exists() else None,
        "knowledge_graph": str(graph_path) if graph_path.exists() else None,
        "domain_scan": str(domain_scan_path) if domain_scan_path.exists() else None,
        "station_01": str(direct_station_paths["01"]) if direct_station_paths["01"].exists() else None,
        "station_08": str(direct_station_paths["08"]) if direct_station_paths["08"].exists() else None,
        "station_09": str(direct_station_paths["09"]) if direct_station_paths["09"].exists() else None,
        "station_10": str(direct_station_paths["10"]) if direct_station_paths["10"].exists() else None,
        "mtl_equations": f"{site_dir}\\shared\\data\\mtl-equations-canonical.json" if mtl_items else None,
    }

    return {
        "source": source,
        "station_outputs": station_outputs,
        "evidence_files": evidence_files,
        "bundle": build_packet_bundle(source, station_outputs),
    }
