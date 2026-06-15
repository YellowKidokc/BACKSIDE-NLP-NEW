from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


CHI_VARIABLES: dict[str, dict[str, list[str]]] = {
    "G": {
        "name": "Authority/Ground",
        "triggers": ["ground", "gravity", "grace", "source", "authority", "foundation", "external input", "axiom"],
    },
    "M": {
        "name": "Mechanism/Action",
        "triggers": ["mechanism", "motion", "force", "operator", "action", "process", "transition", "mapping"],
    },
    "E": {
        "name": "Entropy/Disorder",
        "triggers": ["entropy", "disorder", "decay", "corruption", "decoherence", "drift", "noise", "heat death"],
    },
    "S": {
        "name": "Identity/Self",
        "triggers": ["self", "identity", "person", "personhood", "soul", "observer", "subject"],
    },    "T": {
        "name": "Time/Sequence",
        "triggers": ["time", "sequence", "temporal", "irreversible", "history", "timeline", "before", "after"],
    },
    "K": {
        "name": "Knowledge/Information",
        "triggers": ["knowledge", "information", "logos", "truth", "data", "definition", "theorem", "proof"],
    },
    "R": {
        "name": "Relation/Bond",
        "triggers": ["relation", "bond", "covenant", "coupling", "network", "isomorphism", "bridge", "symmetry"],
    },
    "Q": {
        "name": "Experience/Felt",
        "triggers": ["experience", "felt", "perception", "qualia", "suffering", "joy", "peace"],
    },
    "F": {
        "name": "Faith/Trust",
        "triggers": ["faith", "trust", "belief", "reliance", "uncertainty", "commitment", "surrender"],
    },
    "C": {
        "name": "Coherence/Unity",
        "triggers": ["coherence", "unity", "christ", "shalom", "integration", "whole", "completion", "trinity"],
    },
}


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
EQUATION_RE = re.compile(r"(?P<eq>(?:[A-Za-z_χΧ][\w_χΧ]*|[ΦφψΨχΧ∂∇Σσδβλℒ])[^.\n]{0,80}(?:=|≈|≃|∝|->|→|<=|>=)[^.\n]{1,180})")

@dataclass
class CanonSource:
    path: Path
    role: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def iter_markdown_files(paths: Iterable[Path]) -> tuple[list[Path], list[dict]]:
    files: list[Path] = []
    skipped: list[dict] = []
    for path in paths:
        try:
            if path.is_dir():
                for candidate in sorted(p for p in path.rglob("*") if p.suffix.lower() in {".md", ".lean"}):
                    try:
                        if candidate.is_file():
                            files.append(candidate)
                    except OSError as exc:
                        skipped.append({"path": str(candidate), "reason": str(exc)})
            elif path.is_file():
                files.append(path)
            else:
                skipped.append({"path": str(path), "reason": "not found"})
        except OSError as exc:
            skipped.append({"path": str(path), "reason": str(exc)})
    return files, skipped

def split_blocks(text: str) -> list[dict]:
    blocks: list[dict] = []
    headings: list[str] = []
    current: list[str] = []

    def flush() -> None:
        if not current:
            return
        body = "\n".join(current).strip()
        current.clear()
        if body:
            blocks.append({"heading_path": headings[:], "text": body})

    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            flush()
            level = len(match.group(1))
            headings[:] = headings[: level - 1] + [match.group(2).strip()]
            continue
        if line.strip():
            current.append(line)
        else:
            flush()
    flush()
    return blocks


def sentence_evidence(text: str, trigger: str) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    sentences = SENTENCE_RE.split(compact)
    for sentence in sentences:
        if trigger.lower() in sentence.lower():
            return sentence[:500]
    return compact[:500]

def detect_chi_vars(text: str) -> list[dict]:
    low = text.lower()
    rows: list[dict] = []
    for var, spec in CHI_VARIABLES.items():
        hits = [trigger for trigger in spec["triggers"] if trigger in low]
        if hits:
            rows.append(
                {
                    "variable": var,
                    "name": spec["name"],
                    "triggers": sorted(set(hits)),
                    "evidence_sentence": sentence_evidence(text, hits[0]),
                    "status": "AUTO" if len(hits) > 1 else "NEEDS_REVIEW",
                    "confidence": min(0.95, 0.55 + len(set(hits)) * 0.12),
                }
            )
    return rows


def extract_equations(text: str) -> list[str]:
    equations: list[str] = []
    for match in EQUATION_RE.finditer(text):
        eq = re.sub(r"\s+", " ", match.group("eq")).strip(" -`")
        if len(eq) >= 6:
            equations.append(eq[:500])
    return sorted(set(equations))

def build_index(paths: Iterable[Path], station_id: str) -> dict:
    source_files, skipped_sources = iter_markdown_files(paths)
    blocks_out: list[dict] = []
    sources: list[dict] = []
    var_counts = {var: 0 for var in CHI_VARIABLES}
    equation_rows: list[dict] = []

    for path in source_files:
        try:
            text = read_text(path)
            size = path.stat().st_size
        except OSError as exc:
            skipped_sources.append({"path": str(path), "reason": str(exc)})
            continue
        sources.append({"path": str(path), "bytes": size, "blocks": 0})
        blocks = split_blocks(text)
        sources[-1]["blocks"] = len(blocks)
        for ordinal, block in enumerate(blocks, start=1):
            detections = detect_chi_vars(block["text"])
            equations = extract_equations(block["text"])
            if detections or equations:
                for detection in detections:
                    var_counts[detection["variable"]] += 1
                block_row = {
                    "source_path": str(path),
                    "ordinal": ordinal,
                    "heading_path": block["heading_path"],
                    "chi_vars": [row["variable"] for row in detections],                    "detections": detections,
                    "equations": equations,
                    "text_preview": re.sub(r"\s+", " ", block["text"]).strip()[:700],
                }
                blocks_out.append(block_row)
                for equation in equations:
                    equation_rows.append(
                        {
                            "source_path": str(path),
                            "ordinal": ordinal,
                            "heading_path": block["heading_path"],
                            "equation": equation,
                            "nearby_chi_vars": block_row["chi_vars"],
                        }
                    )

    return {
        "schema": "theophysics.canon_index.v1",
        "station_id": station_id,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "sources": sources,
        "summary": {
            "source_files": len(source_files),
            "tagged_blocks": len(blocks_out),
            "equations": len(equation_rows),
            "var_counts": var_counts,
            "zero_signal_files": [row["path"] for row in sources if row["blocks"] == 0],
            "skipped_sources": skipped_sources,
        },
        "blocks": blocks_out,
        "equations": equation_rows,
    }

def render_markdown(index: dict) -> str:
    lines = [
        f"# Canon Index - {index['station_id']}",
        "",
        f"- Generated: {index['generated_at']}",
        f"- Source files: {index['summary']['source_files']}",
        f"- Tagged blocks: {index['summary']['tagged_blocks']}",
        f"- Equations: {index['summary']['equations']}",
        "",
        "## Chi Variable Counts",
        "",
    ]
    for var, count in index["summary"]["var_counts"].items():
        lines.append(f"- {var}: {count}")
    lines.extend(["", "## Sources", ""])
    for source in index["sources"]:
        lines.append(f"- `{source['path']}` ({source['blocks']} blocks)")
    lines.extend(["", "## Tagged Blocks", ""])
    for row in index["blocks"][:120]:
        heading = " > ".join(row["heading_path"]) or "root"
        lines.extend(
            [
                f"### {Path(row['source_path']).name} :: {row['ordinal']} :: {heading}",
                "",
                f"- chi_vars: `{','.join(row['chi_vars']) or 'NONE'}`",
                f"- equations: {len(row['equations'])}",
                "",
                row["text_preview"],
                "",
            ]
        )    if len(index["blocks"]) > 120:
        lines.append(f"... {len(index['blocks']) - 120} additional blocks omitted from Markdown preview; see JSON.")
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(index: dict, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "canon-index.json"
    md_path = out_dir / "canon-index.md"
    json_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(index), encoding="utf-8")
    return json_path, md_path


def main_for_station(station_id: str, default_sources: list[str]) -> int:
    parser = argparse.ArgumentParser(description=f"Build canon index for {station_id}.")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--source", action="append", type=Path, help="Override/add source path. Can be repeated.")
    args = parser.parse_args()
    sources = args.source if args.source else [Path(source) for source in default_sources]
    index = build_index(sources, station_id)
    json_path, md_path = write_outputs(index, args.out)
    print(f"JSON: {json_path}")
    print(f"Markdown: {md_path}")
    print(f"Tagged blocks: {index['summary']['tagged_blocks']}")
    return 0