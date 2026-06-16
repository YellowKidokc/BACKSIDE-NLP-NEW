from __future__ import annotations

import re
import uuid
from dataclasses import dataclass

from app.models import AxiomMapping, Paper, PaperModelItem, PaperScore

CANON_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "theophysics:pof-2828:treaties")


@dataclass(frozen=True)
class ClassificationMetadata:
    uuid: str
    canonical_filename: str
    title: str
    type: str
    series: str
    paper_number: int | None
    status: str
    maturity: str
    claim_type: str
    claim_strength: str
    cds_zone: str
    bucket: str
    pipeline_stage: str
    tags: list[str]

    def as_dict(self) -> dict:
        return {
            "uuid": self.uuid,
            "canonical_filename": self.canonical_filename,
            "title": self.title,
            "type": self.type,
            "series": self.series,
            "paper_number": self.paper_number,
            "status": self.status,
            "maturity": self.maturity,
            "claim_type": self.claim_type,
            "claim_strength": self.claim_strength,
            "cds_zone": self.cds_zone,
            "bucket": self.bucket,
            "pipeline_stage": self.pipeline_stage,
            "tags": self.tags,
        }


def paper_classification(
    paper: Paper,
    items: list[PaperModelItem] | None = None,
    mappings: list[AxiomMapping] | None = None,
    score: PaperScore | None = None,
) -> ClassificationMetadata:
    items = items or []
    mappings = mappings or []
    title = paper.title or "Untitled"
    series = _series_for(title, paper.source_path)
    paper_number = _paper_number(title, paper.id)
    filename = f"{series}-{_slug(title)}-{paper_number:02d}.md"
    stable_uuid = str(uuid.uuid5(CANON_NAMESPACE, filename))
    claim_strength = _claim_strength(items, mappings, score)
    status = _status(items, mappings, score)
    maturity = _maturity(items, mappings, score)
    bucket = _bucket_for(series, status)
    tags = _tags_for(series, items, mappings)

    return ClassificationMetadata(
        uuid=stable_uuid,
        canonical_filename=filename,
        title=title,
        type="paper",
        series=series,
        paper_number=paper_number,
        status=status,
        maturity=maturity,
        claim_type=_claim_type(items),
        claim_strength=claim_strength,
        cds_zone=_cds_zone(status, claim_strength),
        bucket=bucket,
        pipeline_stage=_pipeline_stage(items, mappings, score),
        tags=tags,
    )


def _series_for(title: str, source_path: str | None) -> str:
    text = f"{title} {source_path or ''}".lower()
    if "gtq" in text:
        return "GTQ"
    if "mda" in text or "moral" in text:
        return "MDA"
    if "law" in text:
        return "LAW"
    if "axiom" in text:
        return "AXIOM"
    if "iso" in text or "isomorphism" in text:
        return "ISO"
    if "master equation" in text:
        return "TH"
    return "TH"


def _paper_number(title: str, fallback: int) -> int:
    match = re.search(r"(?:^|[^0-9])([0-9]{1,3})(?:[^0-9]|$)", title)
    if match:
        return int(match.group(1))
    return fallback


def _slug(value: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", value)
    return "-".join(words[:8]) or "Untitled"


def _claim_strength(
    items: list[PaperModelItem], mappings: list[AxiomMapping], score: PaperScore | None
) -> str:
    if not items:
        return "speculative"
    average_confidence = sum(item.confidence or 0 for item in items) / len(items)
    mapping_count = len(mappings)
    overall = score.overall_score if score else 0
    if mapping_count and average_confidence >= 0.8 and overall >= 80:
        return "strong"
    if mapping_count and average_confidence >= 0.6:
        return "moderate"
    if average_confidence >= 0.4:
        return "weak"
    return "speculative"


def _status(
    items: list[PaperModelItem], mappings: list[AxiomMapping], score: PaperScore | None
) -> str:
    if items and mappings and score:
        return "review"
    if items or mappings or score:
        return "active"
    return "draft"


def _maturity(
    items: list[PaperModelItem], mappings: list[AxiomMapping], score: PaperScore | None
) -> str:
    if items and mappings and score:
        return "developing"
    if items:
        return "seed"
    return "seed"


def _claim_type(items: list[PaperModelItem]) -> str:
    categories = {item.category for item in items}
    if "problem" in categories and "evidence" in categories:
        return "hypothesis"
    if "variables" in categories or "mechanism" in categories:
        return "observation"
    return "inference"


def _cds_zone(status: str, claim_strength: str) -> str:
    if status == "review" and claim_strength in {"strong", "moderate"}:
        return "refine"
    if claim_strength in {"weak", "speculative"}:
        return "triage"
    return "refine"


def _bucket_for(series: str, status: str) -> str:
    if status in {"draft", "active", "review"}:
        return "06_DRAFTS"
    if series in {"GTQ", "MDA"}:
        return "03_SERIES"
    if series in {"LAW", "AXIOM", "TH", "ISO"}:
        return "01_CANON"
    return "02_THEORIES"


def _pipeline_stage(
    items: list[PaperModelItem], mappings: list[AxiomMapping], score: PaperScore | None
) -> str:
    if items and mappings and score:
        return "S06 Evaluation"
    if items and mappings:
        return "S04 YAML/Axiom Trace"
    if items:
        return "S02 Concept"
    return "S01 Idea"


def _tags_for(
    series: str, items: list[PaperModelItem], mappings: list[AxiomMapping]
) -> list[str]:
    tags = ["type/paper", f"series/{series.lower()}"]
    categories = sorted({item.category for item in items})
    tags.extend(f"claim-category/{category}" for category in categories)
    tags.extend(f"axiom/{_slug(mapping.axiom.name).lower()}" for mapping in mappings[:8])
    if mappings:
        tags.append("pipeline/axiom-mapped")
    if items:
        tags.append("pipeline/extracted-claims")
    return tags
