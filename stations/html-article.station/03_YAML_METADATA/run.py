#!/usr/bin/env python3
"""03_YAML_METADATA — deterministic page + section metadata builder.

Stdlib only. Reads the raw source and the 02 section-map; emits routing-ready
metadata aligned to SEMANTIC_ADDRESS_AND_ROUTING.md and ARTICLE_OUTPUT_REGISTRY.md.

Usage:
    python run.py --in <source_path> [--section-map <path>] --out <out_dir>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

KNOWN_STORY_SERIES = {"GTQ", "MDA", "CROSS_DOMAIN", "CD"}
CANONICAL_BUCKETS = {
    "01_CANON", "02_THEORIES", "03_SERIES", "04_FRAMEWORKS",
    "05_EVIDENCE", "06_DRAFTS", "07_PUBLISH", "08_ARCHIVE", "09_MEDIA",
}
CANONICAL_TYPES = {"paper", "note", "axiom", "claim", "evidence", "dashboard", "story"}
DEFAULT_LAYERS = ["reader", "academic", "accessible", "lossless_ai"]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def screaming_snake(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "_", value or "").strip("_")
    return value.upper()


def parse_yaml_frontmatter(text: str) -> tuple[dict, str]:
    """Extract a single-document YAML frontmatter block. Stdlib only.

    Only handles the flat `key: value` and `key: "value"` forms used in the
    Theophysics calibration files. Lists and nested dicts are not parsed.
    """
    fm: dict = {}
    if not text.lstrip().startswith("---"):
        return fm, text
    m = re.match(r"^\s*---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
    if not m:
        return fm, text
    block = m.group(1)
    rest = text[m.end():]
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        fm[key] = value
    return fm, rest


class HtmlMetaScanner(HTMLParser):
    """Pulls <title>, <h1>, <meta>, and the first <p> from an HTML source."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.h1_parts: list[str] = []
        self.first_p_parts: list[str] = []
        self.metas: dict[str, str] = {}
        self._in_title = False
        self._in_h1 = False
        self._in_first_p = False
        self._h1_done = False
        self._first_p_done = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs_d = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "h1" and not self._h1_done:
            self._in_h1 = True
        elif tag == "p" and self._h1_done and not self._first_p_done:
            self._in_first_p = True
        elif tag == "meta":
            name = attrs_d.get("name") or attrs_d.get("property")
            content = attrs_d.get("content")
            if name and content:
                self.metas[name.lower()] = content

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            if self._in_h1:
                self._h1_done = True
            self._in_h1 = False
        elif tag == "p":
            if self._in_first_p:
                self._first_p_done = True
            self._in_first_p = False

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)
        elif self._in_h1:
            self.h1_parts.append(data)
        elif self._in_first_p:
            self.first_p_parts.append(data)


def detect_filename_series(filename: str) -> tuple[str | None, str | None]:
    """Filename like 'gtq-03-free-will-two-frames.html' → ('GTQ', '03')."""
    m = re.match(r"(?i)^([a-z]+)-([0-9]+)\b", filename)
    if not m:
        return None, None
    return m.group(1).upper(), m.group(2)


def resolve_routing(
    *,
    frontmatter: dict,
    metas: dict,
    source_name: str,
    title: str,
    h1: str,
    section_map: dict,
) -> dict:
    extracted: list[str] = []
    derived: list[str] = []
    inferred: list[str] = []

    fields: dict = {}

    # series / article / paper_slug
    paper_slug = (metas.get("paper-slug") or frontmatter.get("paper-slug") or frontmatter.get("slug") or "").strip()
    series_from_slug, article_from_slug = (None, None)
    if paper_slug:
        series_from_slug, article_from_slug = detect_filename_series(paper_slug + ".x")
        extracted.append("paper_slug")
    if not paper_slug:
        fn_series, fn_article = detect_filename_series(source_name)
        if fn_series:
            paper_slug = f"{fn_series.lower()}-{fn_article}"
            series_from_slug, article_from_slug = fn_series, fn_article
            derived.append("paper_slug")

    series = frontmatter.get("series") or metas.get("series") or series_from_slug
    article_no = frontmatter.get("article_no") or frontmatter.get("series_article_number") or article_from_slug
    if frontmatter.get("series") or metas.get("series"):
        extracted.append("series")
    elif series:
        derived.append("series")
    if article_no:
        (extracted if "series" in extracted else derived).append("series_article_number")

    fields["paper_slug"] = paper_slug or None
    fields["series"] = series or None
    fields["series_article_number"] = article_no or None

    # primary / secondary bucket
    primary = frontmatter.get("primary_bucket") or metas.get("primary_bucket")
    secondary = frontmatter.get("secondary_bucket") or metas.get("secondary_bucket")
    if primary:
        extracted.append("primary_bucket")
    elif series in KNOWN_STORY_SERIES:
        primary = "03_SERIES"
        derived.append("primary_bucket")
    elif "checklist" in source_name.lower() or "calibration" in source_name.lower():
        primary = "06_DRAFTS"
        inferred.append("primary_bucket")
    else:
        primary = "06_DRAFTS"
        inferred.append("primary_bucket")
    if secondary:
        extracted.append("secondary_bucket")
    elif primary == "03_SERIES" and series:
        secondary = series
        derived.append("secondary_bucket")
    fields["primary_bucket"] = primary
    fields["secondary_bucket"] = secondary

    # type + story_flag
    type_v = frontmatter.get("type") or metas.get("type")
    if type_v:
        extracted.append("type")
    elif series in KNOWN_STORY_SERIES:
        type_v = "story"
        derived.append("type")
    elif "checklist" in source_name.lower() or "calibration" in source_name.lower():
        type_v = "note"
        derived.append("type")
    else:
        type_v = "paper"
        inferred.append("type")
    if type_v not in CANONICAL_TYPES:
        type_v = "paper"
    fields["type"] = type_v

    story_flag_explicit = frontmatter.get("story_flag") or metas.get("story_flag")
    if story_flag_explicit is not None:
        fields["story_flag"] = str(story_flag_explicit).strip().lower() in ("true", "1", "yes")
        extracted.append("story_flag")
    else:
        fields["story_flag"] = type_v == "story"
        (derived if type_v == "story" else inferred).append("story_flag")

    # status + maturity
    status = frontmatter.get("status") or frontmatter.get("state") or metas.get("status")
    if status:
        extracted.append("status")
    else:
        status = "D" if "draft" in source_name.lower() else "F"
        inferred.append("status")
    fields["status"] = status

    maturity = frontmatter.get("maturity") or metas.get("maturity")
    if maturity:
        extracted.append("maturity")
    else:
        maturity = "published" if status == "F" else "draft"
        derived.append("maturity")
    fields["maturity"] = maturity

    # website layers
    layers_raw = frontmatter.get("website_layers") or metas.get("website_layers")
    if layers_raw:
        layers = [l.strip() for l in str(layers_raw).split(",") if l.strip()]
        extracted.append("website_layers")
    else:
        layers = list(DEFAULT_LAYERS)
        inferred.append("website_layers")
    fields["website_layers"] = layers

    # Address candidate components — only mark as extracted when the value
    # came directly from frontmatter or <meta>, not from the status fallback.
    domain = frontmatter.get("domain") or metas.get("domain")
    if domain:
        extracted.append("domain")
    state = frontmatter.get("state") or metas.get("state")
    if state:
        extracted.append("state")
    else:
        state = status
        if "status" in extracted:
            derived.append("state")
        else:
            inferred.append("state")
    audience = frontmatter.get("audience") or metas.get("audience")
    if audience:
        extracted.append("audience")
    use = frontmatter.get("use") or metas.get("use")
    if use:
        extracted.append("use")
    risk = frontmatter.get("risk") or metas.get("risk")
    if risk:
        extracted.append("risk")

    if not domain:
        if series in KNOWN_STORY_SERIES:
            domain = "THEOPHYSICS"
            derived.append("domain")
        elif "aviation" in (title + " " + source_name).lower() or "pilot" in (title + " " + source_name).lower():
            domain = "AVIATION"
            derived.append("domain")
        else:
            domain = "GENERAL"
            inferred.append("domain")
    if not audience:
        if "checklist" in source_name.lower() or "calibration" in source_name.lower():
            audience = "TEAM"
            derived.append("audience")
        else:
            audience = "GENERAL"
            inferred.append("audience")
    if not use:
        use = "I"
        inferred.append("use")
    if not risk:
        risk = "R1"
        inferred.append("risk")

    if frontmatter.get("named_entity"):
        named_entity = frontmatter["named_entity"]
        extracted.append("named_entity")
    else:
        named_entity_source = h1 or title or source_name
        named_entity = screaming_snake(named_entity_source)[:64] or "UNTITLED"
        derived.append("named_entity")

    address_string = f"{domain}/{named_entity}/{state}/{audience}/{use}/{risk}"

    candidate_confidence = "high"
    if len(set(inferred) & {"domain", "audience", "use", "risk"}) >= 2:
        candidate_confidence = "low"
    elif inferred:
        candidate_confidence = "medium"

    fields.update({
        "domain": domain,
        "named_entity": named_entity,
        "state": state,
        "audience": audience,
        "use": use,
        "risk": risk,
        "address_string": address_string,
        "vector_string": None,
        "hash": None,
        "vector_owner_lane": "04_TAGS",
        "hash_owner_lane": "04_TAGS",
        "candidate_confidence": candidate_confidence,
    })

    fields["_provenance"] = {
        "extracted_fields": sorted(set(extracted)),
        "derived_fields": sorted(set(derived)),
        "inferred_fields": sorted(set(inferred)),
    }
    return fields


def classify_section(s: dict) -> str:
    h = (s.get("heading_text") or "").lower()
    if "kill" in h:
        return "kill_condition"
    if "risk" in h:
        return "risk"
    if "summary" in h or "executive" in h:
        return "summary"
    if "tangent" in h or (s.get("source_anchor") or "").startswith("tangent"):
        return "tangent"
    if "media" in h or (s.get("source_anchor") or "") == "media":
        return "media"
    if "nav" in h:
        return "nav"
    if (s.get("equation_count") or 0) > 5:
        return "equation"
    return "body"


def emit_section_metadata(sm: dict, paper_uuid: str) -> list[dict]:
    out: list[dict] = []
    for s in sm.get("sections", []):
        out.append({
            "paper_uuid": paper_uuid,
            "section_id": s["section_id"],
            "stable_uuid": s["stable_uuid"],
            "ordinal": s["ordinal"],
            "heading_level": s["heading_level"],
            "heading_text": s["heading_text"],
            "heading_path": s["heading_path"],
            "parent_section_id": s.get("parent_section_id"),
            "source_anchor": s.get("source_anchor"),
            "inferred": s["inferred"],
            "equation_count": s["equation_count"],
            "citation_count": s["citation_count"],
            "word_count": s["word_count"],
            "type_hint": classify_section(s),
            "yaml_anchor": s["section_id"],
            "passes_pointer": f"02_SECTION_MAP/{sm['article_slug']}/section-map.json#/sections/{s['ordinal']-1}/passes",
        })
    return out


def emit_yaml(fields: dict, title: str, paper_uuid: str, page_id: str) -> str:
    layers = fields.get("website_layers") or []
    layers_yaml = "\n".join(f"  - {l}" for l in layers) or "  []"
    lines = [
        "---",
        f"paper_uuid: {paper_uuid}",
        f"page_id: {page_id}",
        f"title: \"{(title or '').replace(chr(34), chr(39))}\"",
        f"paper_slug: {fields.get('paper_slug') or 'null'}",
        f"series: {fields.get('series') or 'null'}",
        f"series_article_number: {fields.get('series_article_number') or 'null'}",
        f"primary_bucket: {fields.get('primary_bucket')}",
        f"secondary_bucket: {fields.get('secondary_bucket') or 'null'}",
        f"type: {fields.get('type')}",
        f"story_flag: {str(fields.get('story_flag', False)).lower()}",
        f"status: {fields.get('status')}",
        f"maturity: {fields.get('maturity')}",
        f"domain: {fields.get('domain')}",
        f"named_entity: {fields.get('named_entity')}",
        f"state: {fields.get('state')}",
        f"audience: {fields.get('audience')}",
        f"use: {fields.get('use')}",
        f"risk: {fields.get('risk')}",
        f"address_string: {fields.get('address_string')}",
        f"candidate_confidence: {fields.get('candidate_confidence')}",
        "website_layers:",
        layers_yaml,
        "---",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="out", required=True)
    ap.add_argument("--section-map", dest="section_map", default=None)
    ap.add_argument("--worker", dest="worker", default="worker-1")
    args = ap.parse_args(argv)

    src = Path(args.src)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    sm_path = Path(args.section_map) if args.section_map else None
    if sm_path is None:
        guess = out_dir.parent.parent / "02_SECTION_MAP" / out_dir.name / "section-map.json"
        sm_path = guess
    if not sm_path.exists():
        print(f"ERROR: section-map.json not found at {sm_path}", file=sys.stderr)
        return 2
    section_map = json.loads(sm_path.read_text(encoding="utf-8"))

    raw = src.read_text(encoding="utf-8", errors="replace")

    title = ""
    h1 = ""
    metas: dict[str, str] = {}
    frontmatter: dict[str, str] = {}

    if src.suffix.lower() in {".html", ".htm"}:
        scanner = HtmlMetaScanner()
        scanner.feed(raw)
        scanner.close()
        title = ("".join(scanner.title_parts) or "").strip()
        h1 = ("".join(scanner.h1_parts) or "").strip()
        if not title:
            title = h1
        metas = scanner.metas
    else:
        frontmatter, _ = parse_yaml_frontmatter(raw)
        title = frontmatter.get("title") or ""
        m = re.search(r"^#\s+(.+?)\s*$", raw, flags=re.M)
        if m:
            h1 = m.group(1).strip()
        if not title:
            title = h1

    fields = resolve_routing(
        frontmatter=frontmatter,
        metas=metas,
        source_name=src.name,
        title=title,
        h1=h1,
        section_map=section_map,
    )

    paper_uuid = section_map["paper_uuid"]
    page_id = f"page::{paper_uuid}"

    rollups = {
        "section_count": section_map.get("section_count", 0),
        "equation_count": section_map.get("equation_count_total", 0),
        "citation_count": section_map.get("citation_count_total", 0),
        "inferred_section_count": section_map.get("inferred_section_count", 0),
    }

    provenance = fields.pop("_provenance")
    page_metadata = {
        "lane_id": "03",
        "lane_name": "YAML + Filing",
        "article_slug": out_dir.name,
        "paper_uuid": paper_uuid,
        "page_id": page_id,
        "title": title,
        "source_file_name": src.name,
        "lane_owner": args.worker,
        "last_updated_utc": utc_now(),
        **{k: v for k, v in fields.items()},
        **rollups,
        "extracted_fields": provenance["extracted_fields"],
        "derived_fields": provenance["derived_fields"],
        "inferred_fields": provenance["inferred_fields"],
    }

    (out_dir / "metadata.json").write_text(json.dumps(page_metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "frontmatter.yaml").write_text(emit_yaml(fields, title, paper_uuid, page_id), encoding="utf-8")

    md = [
        f"# Page Metadata — {out_dir.name}",
        "",
        f"- title: {title}",
        f"- paper_uuid: `{paper_uuid}`",
        f"- source: `{src.name}`",
        "",
        "## Routing",
        f"- primary_bucket: **{fields.get('primary_bucket')}**",
        f"- secondary_bucket: {fields.get('secondary_bucket')}",
        f"- type: {fields.get('type')}    story_flag: {fields.get('story_flag')}",
        f"- series: {fields.get('series')} / article {fields.get('series_article_number')}",
        f"- status: {fields.get('status')}    maturity: {fields.get('maturity')}",
        f"- website_layers: {', '.join(fields.get('website_layers') or [])}",
        "",
        "## Address candidate",
        f"- `{fields.get('address_string')}`",
        f"- confidence: **{fields.get('candidate_confidence')}**",
        f"- vector + hash owned by `{fields.get('vector_owner_lane')}` (left null here)",
        "",
        "## Rollups (from 02)",
        f"- sections: {rollups['section_count']}",
        f"- equations: {rollups['equation_count']}",
        f"- citations: {rollups['citation_count']}",
        f"- inferred sections: {rollups['inferred_section_count']}",
        "",
        "## Provenance",
        f"- extracted: {', '.join(provenance['extracted_fields']) or '—'}",
        f"- derived: {', '.join(provenance['derived_fields']) or '—'}",
        f"- inferred: {', '.join(provenance['inferred_fields']) or '—'}",
    ]
    (out_dir / "metadata.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    section_meta = emit_section_metadata(section_map, paper_uuid)
    (out_dir / "section_metadata.json").write_text(json.dumps(section_meta, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"OK lane=03 article={out_dir.name} address={fields.get('address_string')} confidence={fields.get('candidate_confidence')} sections={rollups['section_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
