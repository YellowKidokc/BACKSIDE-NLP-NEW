"""Classification card builder and .fcard manifest writer."""
import yaml
import json
from pathlib import Path
from datetime import datetime


def build_card(
    file_path: Path,
    baseline: str,
    domain: str,
    domain_confidence: float,
    file_type_meaning: str,
    file_type_confidence: float,
    summary: str,
    tags: list[str],
    keywords: list[str],
    slug: str,
    rename_preview: dict,
    confidence_threshold: float = 50.0,
) -> dict:
    """Build a classification card from NLP outputs."""
    overall_conf = round((domain_confidence + file_type_confidence) / 2, 1)
    needs_review = overall_conf < confidence_threshold

    # Determine suggested action
    if needs_review:
        primary_action = "review"
        secondary_action = "classify"
    elif overall_conf >= 85:
        primary_action = "rename"
        secondary_action = "move"
    else:
        primary_action = "classify"
        secondary_action = "rename"

    card = {
        "file_id": f"FILE_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_path.name[:20]}",
        "source_path": str(file_path),
        "original_name": file_path.name,
        "baseline": baseline,
        "domain": {
            "value": domain,
            "confidence": domain_confidence,
            "approved": False,
        },
        "file_type_meaning": {
            "value": file_type_meaning,
            "confidence": file_type_confidence,
        },
        "summary": summary,
        "tags": tags[:5],
        "keywords": keywords[:6],
        "slug": slug,
        "rename_preview": rename_preview,
        "suggested_action": {
            "primary": primary_action,
            "secondary": secondary_action,
        },
        "confidence": {
            "overall": overall_conf,
            "domain": domain_confidence,
            "file_type_meaning": file_type_confidence,
        },
        "review": {
            "needs_review": needs_review,
            "reason": "Low confidence" if needs_review else None,
        },
        "classified_at": datetime.now().isoformat(),
    }
    return card


def write_manifest(cards: list[dict], folder_path: Path,
                   filename: str = "_manifest.fcard") -> Path:
    """Write all classification cards to a single .fcard manifest."""
    manifest = {
        "fis_version": "1.0.0",
        "folder": str(folder_path),
        "classified_at": datetime.now().isoformat(),
        "file_count": len(cards),
        "cards": cards,
    }
    out_path = folder_path / filename
    with open(out_path, 'w', encoding='utf-8') as f:
        yaml.dump(manifest, f, default_flow_style=False,
                  allow_unicode=True, sort_keys=False, width=120)
    return out_path
