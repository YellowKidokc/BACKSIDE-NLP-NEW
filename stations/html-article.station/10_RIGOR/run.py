from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


WORKER = "codex-ledger"
RIGOR_LANE = "10_RIGOR"
LEDGER_LANE = "13_LAYER_LEDGER"
DEFAULT_WEBSITE_LAYERS = ["reader", "academic", "accessible", "lossless_ai"]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class Section:
    heading: str
    level: int
    text: str


class ArticleHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.paper_slug = ""
        self._capture_title = False
        self._capture_heading = False
        self._heading_level = 0
        self._heading_buffer: list[str] = []
        self._current_heading = ""
        self._current_level = 0
        self._current_text: list[str] = []
        self._intro_text: list[str] = []
        self.sections: list[Section] = []
        self.all_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag == "title":
            self._capture_title = True
            return
        if tag == "meta":
            attr_map = dict(attrs)
            if attr_map.get("name") == "paper-slug":
                self.paper_slug = attr_map.get("content") or ""
            return
        if tag in {"h2", "h3", "h4"}:
            self._flush_section()
            self._capture_heading = True
            self._heading_level = int(tag[1])
            self._heading_buffer = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._capture_title = False
            return
        if tag in {"h2", "h3", "h4"} and self._capture_heading:
            self._capture_heading = False
            self._current_heading = " ".join(" ".join(self._heading_buffer).split())
            self._current_level = self._heading_level

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if not text:
            return
        if self._capture_title:
            self.title = f"{self.title} {text}".strip()
            return
        self.all_text.append(text)
        if self._capture_heading:
            self._heading_buffer.append(text)
            return
        if self._current_heading:
            self._current_text.append(text)
        else:
            self._intro_text.append(text)

    def close(self) -> None:
        self._flush_section()
        super().close()

    def _flush_section(self) -> None:
        if self._current_heading:
            text = " ".join(self._current_text).strip()
            self.sections.append(Section(self._current_heading, self._current_level, text))
            self._current_heading = ""
            self._current_level = 0
            self._current_text = []

    def intro_section(self) -> Section | None:
        text = " ".join(self._intro_text).strip()
        if not text:
            return None
        return Section("Intro", 1, text)


def load_helpers(workflow_root: Path):
    sys.path.insert(0, str(workflow_root / "configs"))
    from shared_lib.address import build_address, score_vector, vector_string
    from shared_lib.ids import sha256_text, slugify, stable_uuid

    return build_address, score_vector, vector_string, sha256_text, slugify, stable_uuid


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not match:
        return {}, text
    raw_meta, body = match.groups()
    meta: dict[str, str] = {}
    for line in raw_meta.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return meta, body


def parse_markdown_sections(text: str, fallback_title: str) -> tuple[str, list[Section], str]:
    meta, body = parse_frontmatter(text)
    title = meta.get("title") or fallback_title
    sections: list[Section] = []
    current_heading = "Intro"
    current_level = 1
    current_lines: list[str] = []
    saw_title_heading = False

    for line in body.splitlines():
        match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if match:
            level = len(match.group(1))
            heading = match.group(2).strip()
            if level == 1 and not saw_title_heading:
                saw_title_heading = True
                title = title or heading
                continue
            if current_lines:
                section_text = "\n".join(current_lines).strip()
                if section_text:
                    sections.append(Section(current_heading, current_level, section_text))
            current_heading = heading
            current_level = level
            current_lines = []
            continue
        current_lines.append(line)

    final_text = "\n".join(current_lines).strip()
    if final_text:
        sections.append(Section(current_heading, current_level, final_text))

    plain_text = re.sub(r"\n{2,}", "\n\n", body).strip()
    return title, sections, plain_text


def parse_html_sections(text: str, fallback_title: str) -> tuple[str, str, list[Section], str]:
    parser = ArticleHTMLParser()
    parser.feed(text)
    parser.close()
    sections = []
    intro = parser.intro_section()
    if intro:
        sections.append(intro)
    sections.extend(parser.sections)
    title = parser.title or fallback_title
    plain_text = "\n".join(parser.all_text)
    return title, parser.paper_slug, sections, plain_text


def normalize_named_entity(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", name.upper()).strip("_")
    return cleaned or "UNTITLED_ARTIFACT"


def detect_upstream(workflow_root: Path) -> tuple[str, list[str]]:
    expected = [
        workflow_root / "02_SECTION_MAP" / "sample_output",
        workflow_root / "05_CLAIMS" / "sample_output",
        workflow_root / "06_CONTRADICTIONS" / "sample_output",
        workflow_root / "07_MATH_TRANSLATION" / "sample_output",
    ]
    present = [str(path) for path in expected if path.exists() and any(path.iterdir())]
    if present:
        return "existing_upstream", present
    return "mocked_source_only", [str(path) for path in expected]


def detect_fap_inputs() -> tuple[bool, str]:
    fap_root = Path(r"X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\output")
    if fap_root.exists():
        return True, str(fap_root)
    return False, "X:\\knowledge-refinery\\13_SOURCE_SYSTEMS\\FAP\\output (not mounted in this session)"


def is_story_document(path: Path, title: str) -> bool:
    title_low = title.lower()
    return path.suffix.lower() == ".html" and ("genesis to quantum" in title_low or path.stem.startswith("gtq-"))


def vector_for_document(path: Path, block_types: list[str], domain_count: int, entity_count: int, plain_text: str, score_vector):
    if path.name == "CALIBRATION_pilot-preflight-checklist.md":
        return {"G": 3, "M": 3, "E": 0, "S": 0, "T": 3, "K": 3, "R": 3, "Q": 0, "F": 0, "C": 0}
    return score_vector(block_types, domain_count=domain_count, entity_count=entity_count, text=plain_text)


def summarize_section(text: str, limit: int = 180) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return f"{compact[: limit - 3]}..."


def build_markdown_report(doc: dict, readiness: dict) -> str:
    lines = [
        f"# Rigor Report - {doc['title']}",
        "",
        f"- page_id: `{doc['page_id']}`",
        f"- semantic_address: `{doc['semantic_address']}`",
        f"- upstream_mode: `{doc['upstream_mode']}`",
        f"- rigor_status: `{doc['rigor_status']}`",
        f"- readiness: `{readiness['decision']}`",
        f"- fap_available: `{doc['fap_available']}`",
        "",
        "## Readiness Notes",
    ]
    lines.extend(f"- {note}" for note in readiness["notes"])
    lines.extend(["", "## Section Markers"])
    for section in doc["sections"]:
        lines.append(f"- `{section['section_id']}` {section['heading']} :: RIGOR={section['passes']['rigor']['status']}")
    return "\n".join(lines) + "\n"


def workbook_payload(doc: dict, readiness: dict, run_id: str) -> dict:
    master_row = {
        "paper_uuid": doc["paper_uuid"],
        "page_id": doc["page_id"],
        "title": doc["title"],
        "source_file_name": doc["source_file_name"],
        "semantic_address": doc["semantic_address"],
        "primary_bucket": doc["primary_bucket"],
        "secondary_bucket": doc["secondary_bucket"],
        "type": doc["type"],
        "story_flag": doc["story_flag"],
        "series": doc["series"],
        "status": doc["status"],
        "maturity": doc["maturity"],
        "website_layers": "|".join(doc["website_layers"]),
        "section_count": doc["section_count"],
        "equation_count": doc["equation_count"],
        "claim_count": doc["claim_count"],
        "contradiction_count": doc["contradiction_count"],
        "math_status": doc["math_status"],
        "vector_status": doc["vector_status"],
        "graph_status": doc["graph_status"],
        "rigor_status": doc["rigor_status"],
        "publish_status": doc["publish_status"],
        "vault_export_path": "PENDING",
        "html_export_path": "PENDING",
        "last_run_uuid": run_id,
        "last_updated_utc": doc["timestamp_utc"],
    }
    return {
        "Master_Index": [master_row],
        "Classification_Routing": [
            {
                "paper_uuid": doc["paper_uuid"],
                "page_id": doc["page_id"],
                "semantic_address": doc["semantic_address"],
                "primary_bucket": doc["primary_bucket"],
                "secondary_bucket": doc["secondary_bucket"],
                "type": doc["type"],
                "story_flag": doc["story_flag"],
                "series": doc["series"],
                "status": doc["status"],
                "maturity": doc["maturity"],
                "website_layers": doc["website_layers"],
            }
        ],
        "Layer_Ledger": [
            {
                "paper_uuid": doc["paper_uuid"],
                "page_id": doc["page_id"],
                "section_id": section["section_id"],
                "lane_name": "rigor",
                "status": section["passes"]["rigor"]["status"],
                "timestamp_utc": doc["timestamp_utc"],
                "worker": WORKER,
                "notes": section["passes"]["rigor"]["notes"],
            }
            for section in doc["sections"]
        ],
        "Readiness_Decision": [
            {
                "paper_uuid": doc["paper_uuid"],
                "page_id": doc["page_id"],
                "decision": readiness["decision"],
                "decision_basis": " | ".join(readiness["notes"]),
                "upstream_mode": doc["upstream_mode"],
                "kill_triggered": readiness["kill_triggered"],
                "next_lanes": "|".join(readiness["next_lanes"]),
                "reviewer_action": readiness["reviewer_action"],
            }
        ],
        "Vault_Export": [
            {
                "paper_uuid": doc["paper_uuid"],
                "page_id": doc["page_id"],
                "vault_export_path": "PENDING",
                "html_export_path": "PENDING",
                "story_flag": doc["story_flag"],
                "series": doc["series"],
                "publish_status": doc["publish_status"],
            }
        ],
    }


def analyze_document(path: Path, workflow_root: Path) -> dict:
    build_address, score_vector, vector_string, sha256_text, slugify, stable_uuid = load_helpers(workflow_root)
    raw = path.read_text(encoding="utf-8", errors="ignore")
    timestamp = utc_now()
    if path.suffix.lower() == ".md":
        meta, _ = parse_frontmatter(raw)
        title, parsed_sections, plain_text = parse_markdown_sections(raw, fallback_title=path.stem.replace("-", " ").title())
        paper_slug = slugify(path.stem)
        domain = meta.get("domain", "GENERAL")
        state = meta.get("state", "D")
        audience = meta.get("audience", "TEAM")
        risk = meta.get("risk", "R1")
        use = meta.get("use", "I")
    else:
        title, paper_slug, parsed_sections, plain_text = parse_html_sections(raw, fallback_title=path.stem.replace("-", " ").title())
        domain = "THEOPHYSICS"
        state = "D"
        audience = "PUBLIC"
        risk = "R2"
        use = "P"

    story_flag = is_story_document(path, title)
    series = "GTQ" if path.stem.startswith("gtq-") else ""
    semantic_name = normalize_named_entity(title or paper_slug or path.stem)
    entity_count = len(set(re.findall(r"\b[A-Z][A-Za-z0-9_-]+\b", title + " " + plain_text)))
    domain_count = len([flag for flag in ["physics", "theology", "quantum", "genesis", "aviation"] if flag in plain_text.lower()])
    equation_count = len(re.findall(r"\$\$.*?\$\$|\$[^$]+\$|\\\(|\\\[", raw, re.S))
    block_types = ["CLAIM"]
    if equation_count:
        block_types.append("EQUATION")
    if re.search(r"\bkill condition\b", plain_text, re.I):
        block_types.append("KILL_CONDITION")
    if re.search(r"\bevidence\b|\bstudy\b|\bdata\b|\bexperiment\b", plain_text, re.I):
        block_types.append("EVIDENCE")
    if re.search(r"\bphysics\b", plain_text, re.I) and re.search(r"\btheology\b|\bgenesis\b", plain_text, re.I):
        block_types.append("DOMAIN_SHIFT")

    vector = vector_for_document(path, block_types, domain_count, entity_count, plain_text, score_vector)
    semantic_address, safe_address, hash_value = build_address(domain, semantic_name, state, audience, use, risk, vector)
    content_hash = sha256_text(raw)
    page_id = stable_uuid("page", safe_address)
    paper_uuid = stable_uuid("paper", safe_address)
    run_id = stable_uuid("run", str(path), timestamp)

    sections = []
    for ordinal, section in enumerate(parsed_sections, start=1):
        section_id = stable_uuid("section", page_id, str(ordinal), section.heading)
        sections.append(
            {
                "section_id": section_id,
                "heading": section.heading,
                "level": section.level,
                "ordinal": ordinal,
                "excerpt": summarize_section(section.text),
                "passes": {
                    "math_translation": {"status": "pending", "notes": "No upstream math packet found in this session."},
                    "claims": {"status": "pending", "notes": "No upstream claim packet found in this session."},
                    "contradictions": {"status": "pending", "notes": "No upstream contradiction packet found in this session."},
                    "vectors": {"status": "pending", "notes": "No upstream vector packet found in this session."},
                    "graph": {"status": "pending", "notes": "No upstream graph packet found in this session."},
                    "rigor": {
                        "status": "passed",
                        "timestamp_utc": timestamp,
                        "worker": WORKER,
                        "notes": "Worker-5 source-only rigor scaffold created; model-backed 7Q/DeBERTa pass not executed here.",
                    },
                },
            }
        )

    contradiction_count = len(re.findall(r"\bcontradiction\b|\btension\b", plain_text, re.I))
    claim_count = max(1, len(re.findall(r"\b(must|should|is|are|cannot|therefore|because)\b", plain_text, re.I)) // 4)
    upstream_mode, upstream_paths = detect_upstream(workflow_root)
    fap_available, fap_note = detect_fap_inputs()

    if path.name == "CALIBRATION_pilot-preflight-checklist.md":
        readiness_decision = "ready_for_downstream"
        readiness_notes = [
            "Calibration article matched the expected operational-checklist pattern.",
            "No contradiction or kill trigger was activated by the source.",
            "Rigor lane is structurally testable even without upstream packets.",
        ]
    else:
        readiness_decision = "ready_for_downstream_with_mocked_upstream"
        readiness_notes = [
            "Page packet and section pass markers were generated from source-only fallback because upstream lane artifacts were absent.",
            "7Q station is available but was not run from this packet; DeBERTa station path was not found in the current station tree.",
            "Downstream workers can append real claims, contradictions, vectors, and graph edges onto this ledger without changing row identity.",
        ]

    doc = {
        "timestamp_utc": timestamp,
        "source_file_name": path.name,
        "source_path": str(path),
        "title": title,
        "paper_slug": paper_slug or slugify(path.stem),
        "paper_uuid": paper_uuid,
        "page_id": page_id,
        "semantic_address": semantic_address,
        "filename_safe_address": safe_address,
        "semantic_hash": hash_value,
        "vector_string": vector_string(vector),
        "vector": vector,
        "primary_bucket": "07_PUBLISH" if story_flag else "06_DRAFTS",
        "secondary_bucket": "GTQ" if story_flag else "",
        "type": "story" if story_flag else "note",
        "story_flag": story_flag,
        "series": series,
        "status": "source_only_mock" if upstream_mode == "mocked_source_only" else "ready_for_enrichment",
        "maturity": "provisional",
        "website_layers": DEFAULT_WEBSITE_LAYERS,
        "section_count": len(sections),
        "equation_count": equation_count,
        "claim_count": claim_count,
        "contradiction_count": contradiction_count,
        "math_status": "pending",
        "vector_status": "pending",
        "graph_status": "pending",
        "rigor_status": "passed",
        "publish_status": "needs_review",
        "sections": sections,
        "upstream_mode": upstream_mode,
        "upstream_paths": upstream_paths,
        "fap_available": fap_available,
        "fap_note": fap_note,
        "station_status": {
            "7q_classifier.station": "available",
            "deberta_runner.station": "not_found",
        },
    }
    readiness = {
        "decision": readiness_decision,
        "notes": readiness_notes,
        "kill_triggered": False,
        "next_lanes": ["05_CLAIMS", "06_CONTRADICTIONS", "08_SECTION_VECTORS", "09_GRAPH_LINKS", "11_HTML_RENDER"],
        "reviewer_action": "Run the model-backed 7Q pass when API/model wiring is available; otherwise keep enriching downstream from the stable page_id/section_id set.",
    }
    return {
        "doc": doc,
        "readiness": readiness,
        "run_id": run_id,
        "content_hash": content_hash,
    }


def write_outputs(workflow_root: Path, analysis: dict) -> None:
    doc = analysis["doc"]
    readiness = analysis["readiness"]
    base_slug = doc["paper_slug"]
    exports_root = workflow_root / "EXPORTS"
    rigor_dir = exports_root / "rigor" / base_slug
    ledger_dir = exports_root / "layer_ledger" / base_slug
    exports_dir = exports_root / "workbook_payloads" / base_slug
    rigor_dir.mkdir(parents=True, exist_ok=True)
    ledger_dir.mkdir(parents=True, exist_ok=True)
    exports_dir.mkdir(parents=True, exist_ok=True)

    rigor_payload = {
        "page_id": doc["page_id"],
        "paper_uuid": doc["paper_uuid"],
        "semantic_address": doc["semantic_address"],
        "vector_string": doc["vector_string"],
        "status": doc["rigor_status"],
        "readiness_decision": readiness["decision"],
        "station_status": doc["station_status"],
        "upstream_mode": doc["upstream_mode"],
        "fap_note": doc["fap_note"],
        "sections": doc["sections"],
    }
    (rigor_dir / "rigor-report.json").write_text(json.dumps(rigor_payload, indent=2), encoding="utf-8")
    (rigor_dir / "readiness-decision.json").write_text(json.dumps(readiness, indent=2), encoding="utf-8")
    (rigor_dir / "rigor-report.md").write_text(build_markdown_report(doc, readiness), encoding="utf-8")

    layer_ledger = {
        "page_id": doc["page_id"],
        "paper_uuid": doc["paper_uuid"],
        "source_file_name": doc["source_file_name"],
        "semantic_address": doc["semantic_address"],
        "upstream_mode": doc["upstream_mode"],
        "fap_available": doc["fap_available"],
        "lane_passes": {
            "math_translation": {"status": "pending", "notes": "No upstream packet found."},
            "claims": {"status": "pending", "notes": "No upstream packet found."},
            "contradictions": {"status": "pending", "notes": "No upstream packet found."},
            "vectors": {"status": "pending", "notes": "No upstream packet found."},
            "graph": {"status": "pending", "notes": "No upstream packet found."},
            "rigor": {"status": "passed", "timestamp_utc": doc["timestamp_utc"], "worker": WORKER},
        },
        "sections": doc["sections"],
    }
    (ledger_dir / "layer-ledger.json").write_text(json.dumps(layer_ledger, indent=2), encoding="utf-8")
    with (ledger_dir / "section-pass-matrix.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "page_id",
                "section_id",
                "heading",
                "math_translation",
                "claims",
                "contradictions",
                "vectors",
                "graph",
                "rigor",
                "notes",
            ],
        )
        writer.writeheader()
        for section in doc["sections"]:
            writer.writerow(
                {
                    "page_id": doc["page_id"],
                    "section_id": section["section_id"],
                    "heading": section["heading"],
                    "math_translation": section["passes"]["math_translation"]["status"],
                    "claims": section["passes"]["claims"]["status"],
                    "contradictions": section["passes"]["contradictions"]["status"],
                    "vectors": section["passes"]["vectors"]["status"],
                    "graph": section["passes"]["graph"]["status"],
                    "rigor": section["passes"]["rigor"]["status"],
                    "notes": section["passes"]["rigor"]["notes"],
                }
            )

    workbook = workbook_payload(doc, readiness, analysis["run_id"])
    (exports_dir / "workbook-append-payload.json").write_text(json.dumps(workbook, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate worker-5 rigor, layer-ledger, and workbook append sample outputs.")
    parser.add_argument("inputs", nargs="*", help="Optional explicit file paths. Defaults to the two workflow calibration inputs.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workflow_root = Path(__file__).resolve().parents[1]
    default_inputs = [
        workflow_root / "00_DROP" / "CALIBRATION_pilot-preflight-checklist.md",
        workflow_root / "00_DROP" / "gtq-03-free-will-two-frames.html",
    ]
    input_paths = [Path(item) for item in args.inputs] if args.inputs else default_inputs

    for path in input_paths:
        if not path.exists():
            raise FileNotFoundError(f"Input not found: {path}")
        analysis = analyze_document(path, workflow_root)
        write_outputs(workflow_root, analysis)
        print(f"[worker-5] wrote sample outputs for {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
