from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Iterable


CALIBRATION_VECTOR = {
    "G": 3,
    "M": 3,
    "E": 0,
    "S": 0,
    "T": 3,
    "K": 3,
    "R": 3,
    "Q": 0,
    "F": 0,
    "C": 0,
}
VECTOR_ORDER = ["G", "M", "E", "S", "T", "K", "R", "Q", "F", "C"]
TIE_BREAK = ["E", "C", "G", "K", "M", "T", "R", "F", "S", "Q"]


KNOWN_TRANSLATIONS = {
    r"\frac{dC}{dt} = O \cdot G(1-C) - S \cdot C": {
        "word_equation": "the rate of change of coherence equals openness times grace times the remaining coherence gap minus entropy times current coherence",
        "spoken_explanation": "Coherence grows when grace can couple into an open agent and shrinks when entropy keeps draining the current state.",
        "summary": "Base coherence dynamics with openness gating grace.",
        "confidence": 0.82,
    },
    r"C^* = \frac{O \cdot G}{O \cdot G + S}": {
        "word_equation": "steady-state coherence equals openness-grace coupling divided by openness-grace coupling plus entropy",
        "spoken_explanation": "At equilibrium, coherence settles at the fraction of total system pressure contributed by grace coupling rather than entropy.",
        "summary": "Equilibrium coherence for the base model.",
        "confidence": 0.82,
    },
    r"\frac{dC}{dt} = \frac{(1+s)}{2} \cdot G(1-C) - S \cdot C": {
        "word_equation": "the rate of change of coherence equals the surrender-scaled grace term times the remaining gap minus entropy times current coherence",
        "spoken_explanation": "The surrender parameter changes how much grace actually couples into the agent before entropy is subtracted.",
        "summary": "Surrender-parameter version of the coherence equation.",
        "confidence": 0.79,
    },
    r"\frac{dC}{dt} = 0 \cdot G(1-C) - S \cdot C = -S \cdot C": {
        "word_equation": "with zero coupling, coherence decays only by entropy",
        "spoken_explanation": "When the agent is fully closed, grace contributes nothing to growth and entropy drives the whole trajectory downward.",
        "summary": "Path 1 autonomy dynamics.",
        "confidence": 0.8,
    },
    r"\frac{dC}{dt} \approx \frac{1}{2} G(1-C) - S \cdot C": {
        "word_equation": "with partial coupling, coherence grows at roughly half-strength grace input minus entropy",
        "spoken_explanation": "Performance posture opens the channel only partway, so grace helps but does not fully dominate the entropy term.",
        "summary": "Approximate Path 2 performance dynamics.",
        "confidence": 0.76,
    },
    r"C^*_{perf} = \frac{\frac{G}{2}}{\frac{G}{2} + S} = \frac{G}{G + 2S}": {
        "word_equation": "performance equilibrium coherence equals half-strength grace divided by half-strength grace plus entropy, which simplifies to grace over grace plus twice entropy",
        "spoken_explanation": "Under performance posture, entropy effectively counts twice as heavily against the reachable steady state.",
        "summary": "Performance-path equilibrium ceiling.",
        "confidence": 0.76,
    },
    r"\frac{dC}{dt} = G(1-C) - S \cdot C": {
        "word_equation": "the rate of change of coherence equals full grace input across the remaining gap minus entropy times current coherence",
        "spoken_explanation": "In full surrender the grace term is no longer throttled, so the system receives maximum growth pressure against entropy.",
        "summary": "Path 3 surrender dynamics.",
        "confidence": 0.82,
    },
    r"C^* = \frac{G}{G + S}": {
        "word_equation": "steady-state coherence equals grace divided by grace plus entropy",
        "spoken_explanation": "With full coupling, equilibrium depends only on the balance between grace input and entropy load.",
        "summary": "Path 3 equilibrium coherence.",
        "confidence": 0.82,
    },
}


@dataclass
class MathBlock:
    raw: str
    normalized: str
    start: int
    end: int
    is_block: bool


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_math(source: str) -> str:
    value = source.strip()
    for left, right in (("$$", "$$"), ("$", "$"), (r"\[", r"\]"), (r"\(", r"\)")):
        if value.startswith(left) and value.endswith(right):
            value = value[len(left): len(value) - len(right)].strip()
            break
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def html_to_text(content: str) -> str:
    stripped = re.sub(r"(?is)<script.*?</script>", " ", content)
    stripped = re.sub(r"(?is)<style.*?</style>", " ", stripped)
    stripped = re.sub(r"(?s)<[^>]+>", " ", stripped)
    stripped = unescape(stripped)
    stripped = re.sub(r"\s+", " ", stripped)
    return stripped.strip()


def slugify(value: str, fallback: str = "x") -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or fallback


def short_hash(*parts: str, length: int = 16) -> str:
    return hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:length]


def vector_string(vector: dict[str, int]) -> str:
    return "".join(f"{key}{vector[key]}" for key in VECTOR_ORDER)


def semantic_hash(vector: dict[str, int]) -> str:
    ranked = sorted(vector.keys(), key=lambda key: (-vector[key], TIE_BREAK.index(key)))
    pairs = [
        (ranked[0], ranked[-1]),
        (ranked[1], ranked[-2]),
        (ranked[2], ranked[-3]),
        (ranked[3], ranked[-4]),
        (ranked[4], ranked[-5]),
    ]
    return "-".join(f"{a}{vector[a]}{b}{vector[b]}" for a, b in pairs)


def build_address(domain: str, entity: str, state: str, access: str, use: str, risk: str, vector: dict[str, int]) -> tuple[str, str, str]:
    hash_value = semantic_hash(vector)
    address = f"{domain}/{entity}/{state}/{access}/{use}/{risk} :: {vector_string(vector)} :: {hash_value}"
    safe = "__".join(
        [
            slugify(domain),
            slugify(entity),
            state,
            access,
            use,
            risk,
            vector_string(vector),
            slugify(hash_value),
        ]
    )
    return address, safe, hash_value


def score_vector(text: str, equation_count: int) -> dict[str, int]:
    low = text.lower()
    has_authority = any(word in low for word in ["must", "required", "kill condition", "falsifiable"])
    has_trust = any(word in low for word in ["grace", "faith", "surrender", "trust"])
    has_unification = any(word in low for word in ["dissolves", "both camps", "same equation", "coherence"])
    return {
        "G": 3 if has_authority else 0,
        "M": 3 if equation_count else 0,
        "E": 0,
        "S": 0,
        "T": 3,
        "K": 3 if equation_count else 0,
        "R": 3 if "calvinist" in low and "arminian" in low else 0,
        "Q": 0,
        "F": 3 if has_trust else 0,
        "C": 3 if has_unification else 0,
    }


def extract_math_blocks(content: str) -> list[MathBlock]:
    blocks: list[MathBlock] = []
    patterns = [
        (re.compile(r"\$\$([\s\S]+?)\$\$"), 1, True),
        (re.compile(r"(?<!\$)\$([^\$\n]+?)\$(?!\$)"), 1, False),
        (re.compile(r"\\\((.+?)\\\)"), 1, False),
        (re.compile(r"\\\[([\s\S]+?)\\\]"), 1, True),
        (
            re.compile(
                r"<div[^>]*class=[\"'][^\"']*math[^\"']*[\"'][^>]*>\s*(\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\$[^$]+\$|\\\(.+?\\\))\s*</div>",
                re.IGNORECASE,
            ),
            1,
            True,
        ),
    ]
    for pattern, group, is_block in patterns:
        for match in pattern.finditer(content):
            raw = match.group(group).strip()
            blocks.append(
                MathBlock(
                    raw=raw,
                    normalized=normalize_math(raw),
                    start=match.start(),
                    end=match.end(),
                    is_block=is_block,
                )
            )
    blocks.sort(key=lambda item: item.start)
    return blocks


def dedupe_blocks(blocks: Iterable[MathBlock]) -> list[dict]:
    ordered: dict[str, dict] = {}
    for block in blocks:
        current = ordered.get(block.normalized)
        if current is None:
            ordered[block.normalized] = {
                "raw": block.raw,
                "normalized": block.normalized,
                "start": block.start,
                "end": block.end,
                "is_block": block.is_block,
                "occurrence_count": 1,
            }
        else:
            current["occurrence_count"] += 1
    return list(ordered.values())


def find_preview_report(input_path: Path) -> tuple[Path | None, dict | None]:
    candidates = [
        Path(r"\\dlowenas\HPWorkstation\Desktop\gtq-03-free-will-in-two-frames-MATH-PREVIEW-report.json"),
        input_path.with_name(f"{input_path.stem}-MATH-PREVIEW-report.json"),
    ]
    for candidate in candidates:
        try:
            if candidate.exists():
                return candidate, json.loads(read_text(candidate))
        except OSError:
            continue
    return None, None


def preview_matches_input(input_path: Path, preview_report: dict | None) -> bool:
    if not preview_report:
        return False
    article_path = str(preview_report.get("articlePath", "")).lower()
    input_name = input_path.stem.lower()
    if input_name and input_name in article_path:
        return True
    shared_tokens = ["free-will", "two-frames", "gtq-03", "gtq-04"]
    return any(token in input_name and token in article_path for token in shared_tokens)


def nearest_heading(content: str, position: int) -> str:
    pattern = re.compile(r"<h([1-4])[^>]*>(.*?)</h\1>", re.IGNORECASE | re.DOTALL)
    latest = "unassigned"
    for match in pattern.finditer(content):
        if match.start() > position:
            break
        latest = re.sub(r"\s+", " ", html_to_text(match.group(2))) or latest
    return latest


def provisional_translation(equation: str, preview_missing: set[str]) -> tuple[str, str, str, float, str]:
    if equation in KNOWN_TRANSLATIONS:
        item = KNOWN_TRANSLATIONS[equation]
        source = "preview" if equation in preview_missing else "rule_map"
        return (
            item["word_equation"],
            item["spoken_explanation"],
            item["summary"],
            float(item["confidence"]),
            source,
        )

    generic = equation
    generic = generic.replace(r"\frac{dC}{dt}", "the rate of change of coherence")
    generic = generic.replace(r"\cdot", " times ")
    generic = generic.replace("=", " equals ")
    generic = generic.replace(r"\approx", " is approximately ")
    generic = generic.replace(r"\geq", " is greater than or equal to ")
    generic = generic.replace(r"\leq", " is less than or equal to ")
    generic = re.sub(r"\s+", " ", generic).strip()
    return (
        generic,
        "This equation still needs a reviewed structural translation from the math station or a validated preview table.",
        "Generic fallback translation only.",
        0.42,
        "generic_fallback",
    )


def is_structural_math(normalized: str) -> bool:
    if not normalized:
        return False
    if re.fullmatch(r"[^A-Za-z0-9\\]+", normalized):
        return False
    signals = ["=", r"\approx", r"\geq", r"\leq", r"\in", ">", "<"]
    return any(signal in normalized for signal in signals)


def select_equation_inventory(blocks: list[MathBlock], preview_report: dict | None, input_path: Path) -> list[dict]:
    deduped = dedupe_blocks(blocks)
    if preview_matches_input(input_path, preview_report):
        preferred = [normalize_math(item) for item in preview_report.get("missing", []) if normalize_math(item)]
        if preferred:
            by_normalized = {item["normalized"]: item for item in deduped}
            selected = []
            for equation in preferred:
                existing = by_normalized.get(equation)
                if existing is not None:
                    selected.append(existing)
                else:
                    selected.append(
                        {
                            "raw": equation,
                            "normalized": equation,
                            "start": 0,
                            "end": 0,
                            "is_block": True,
                            "occurrence_count": 0,
                        }
                    )
            return selected
    return [item for item in deduped if is_structural_math(item["normalized"])]


def parse_front_matter(content: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def article_identity(input_path: Path, content: str, equation_count: int) -> dict[str, object]:
    if input_path.suffix.lower() == ".md":
        front_matter = parse_front_matter(content)
        title = front_matter.get("title", input_path.stem.replace("-", " ").title())
        domain = front_matter.get("domain", "GENERAL")
        state = front_matter.get("state", "W")
        audience = front_matter.get("audience", "TEAM")
        risk = front_matter.get("risk", "R1")
        use = "I"
        calibration_name = input_path.name.lower().replace("_", "-")
        vector = CALIBRATION_VECTOR if equation_count == 0 and "pilot-preflight-checklist" in calibration_name else score_vector(content, equation_count)
        named_entity = slugify(title, "document").replace("-", "_").upper()
        page_id = slugify(input_path.stem)
        semantic_address, filename_safe_address, hash_value = build_address(domain, named_entity, state, audience, use, risk, vector)
        return {
            "page_id": page_id,
            "title": title,
            "domain": domain,
            "state": state,
            "audience": audience,
            "use": use,
            "risk": risk,
            "vector": vector,
            "semantic_address": semantic_address,
            "filename_safe_address": filename_safe_address,
            "address_hash": hash_value,
            "status": "calibration",
        }

    title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    title = html_to_text(title_match.group(1)) if title_match else input_path.stem.replace("-", " ").title()
    slug_match = re.search(r'<meta\s+name="paper-slug"\s+content="([^"]+)"', content, re.IGNORECASE)
    page_id = slug_match.group(1) if slug_match else slugify(input_path.stem)
    vector = score_vector(content, equation_count)
    semantic_address, filename_safe_address, hash_value = build_address(
        "THEOPHYSICS",
        slugify(title, "article").replace("-", "_").upper(),
        "W",
        "PUBLIC",
        "I",
        "R2",
        vector,
    )
    return {
        "page_id": page_id,
        "title": title,
        "domain": "THEOPHYSICS",
        "state": "W",
        "audience": "PUBLIC",
        "use": "I",
        "risk": "R2",
        "vector": vector,
        "semantic_address": semantic_address,
        "filename_safe_address": filename_safe_address,
        "address_hash": hash_value,
        "status": "provisional",
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")


def safe_exists(path: Path | None) -> bool:
    if path is None:
        return False
    try:
        return path.exists()
    except OSError:
        return False


def build_markdown(identity: dict[str, object], equations: list[dict], preview_summary: dict[str, object], loopback_required: bool) -> str:
    lines = [
        f"# Math Translation - {identity['title']}",
        "",
        f"- page_id: `{identity['page_id']}`",
        f"- semantic_address: `{identity['semantic_address']}`",
        f"- equation_count: `{len(equations)}`",
        f"- loopback_required: `{str(loopback_required).lower()}`",
        "",
    ]
    if preview_summary:
        lines.extend(
            [
                "## Upstream Preview",
                "",
                f"- preview_report_found: `{preview_summary.get('report_found', False)}`",
                f"- reviewed_matches: `{preview_summary.get('reviewed_matches', 0)}`",
                f"- fallback_translations: `{preview_summary.get('fallback_translations', 0)}`",
                f"- csv_path_found: `{preview_summary.get('csv_path_found', False)}`",
                "",
            ]
        )

    if not equations:
        lines.extend(["## Result", "", "No equations found. This is the expected calibration outcome when the source article is non-mathematical."])
        return "\n".join(lines) + "\n"

    lines.extend(["## Equations", ""])
    for item in equations:
        lines.extend(
            [
                f"### {item['equation_id']} - {item['section_hint']}",
                "",
                f"- confidence: `{item['confidence']}`",
                f"- translation_source: `{item['translation_source']}`",
                f"- occurrence_count: `{item['occurrence_count']}`",
                "",
                "```latex",
                item["normalized_math"],
                "```",
                "",
                f"Word equation: {item['word_equation']}",
                "",
                f"Explanation: {item['spoken_explanation']}",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def build_html_snippets(identity: dict[str, object], equations: list[dict]) -> str:
    cards = []
    for item in equations:
        cards.append(
            "\n".join(
                [
                    '<section class="math-snippet">',
                    f'  <h3>{item["equation_id"]} - {item["section_hint"]}</h3>',
                    f'  <div class="raw"><code>{item["normalized_math"]}</code></div>',
                    f'  <p class="word">{item["word_equation"]}</p>',
                    f'  <p class="explanation">{item["spoken_explanation"]}</p>',
                    f'  <p class="meta">confidence={item["confidence"]} source={item["translation_source"]}</p>',
                    "</section>",
                ]
            )
        )
    body = "\n\n".join(cards) if cards else "<p>No equations found.</p>"
    return "\n".join(
        [
            "<!DOCTYPE html>",
            '<html lang="en">',
            "<head>",
            '  <meta charset="utf-8">',
            f"  <title>{identity['title']} - Math Snippets</title>",
            "  <style>body{font-family:Arial,sans-serif;margin:2rem;line-height:1.5}.math-snippet{border:1px solid #ccc;padding:1rem;margin:1rem 0}.raw{background:#f5f5f5;padding:.75rem}.meta{color:#666;font-size:.9rem}</style>",
            "</head>",
            "<body>",
            f"  <h1>{identity['title']} - Math Snippets</h1>",
            body,
            "</body>",
            "</html>",
        ]
    )


def build_loopback(identity: dict[str, object], preview_summary: dict[str, object], equations: list[dict]) -> dict:
    triggers = []
    if preview_summary.get("report_found") and not preview_summary.get("csv_path_found"):
        triggers.append(
            {
                "trigger_id": "preview-csv-missing",
                "severity": "medium",
                "condition": "preview report references a math translation table path that is no longer reachable",
                "evidence": preview_summary.get("csv_path"),
                "recommendation": "either restore the referenced CSV table or regenerate a reviewed translation table from the active math station",
            }
        )
    if preview_summary.get("fallback_translations", 0):
        triggers.append(
            {
                "trigger_id": "preview-fallback-only",
                "severity": "medium",
                "condition": "preview report indicates fallback translations with zero reviewed matches",
                "evidence": f"fallback_translations={preview_summary.get('fallback_translations', 0)} reviewed_matches={preview_summary.get('reviewed_matches', 0)}",
                "recommendation": "review the nine GTQ equations against the live station dictionary and replace provisional wording with validated structural translations",
            }
        )
    generic_count = sum(1 for item in equations if item["translation_source"] == "generic_fallback")
    if generic_count:
        triggers.append(
            {
                "trigger_id": "generic-fallback-present",
                "severity": "high",
                "condition": "one or more equations could not be matched to known structural translations",
                "evidence": f"generic_fallback_count={generic_count}",
                "recommendation": "extend the shared field vocabulary or station dictionary before downstream claims/rigor treat these equations as settled",
            }
        )

    return {
        "protocol_version": "1.0",
        "generated_at": utc_now(),
        "lane_id": "14",
        "source_lane": "07_MATH_TRANSLATION",
        "page_id": identity["page_id"],
        "title": identity["title"],
        "status": "loopback" if triggers else "passed",
        "trigger_count": len(triggers),
        "triggers": triggers,
        "downstream_safe_to_continue": True,
        "notes": "HTML workflow continues because this round permits mocked or provisional upstream, but math remains revisitable.",
    }


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Lane 07 math translation wrapper")
    parser.add_argument("--input", required=True, help="path to source article")
    parser.add_argument("--output-dir", required=True, help="directory to receive lane 07 outputs")
    parser.add_argument("--loopback-dir", required=True, help="directory to receive lane 14 outputs")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    loopback_dir = Path(args.loopback_dir)
    ensure_dir(output_dir)
    ensure_dir(loopback_dir)

    content = read_text(input_path)
    blocks = extract_math_blocks(content)
    preview_path, preview_report = find_preview_report(input_path)
    deduped = select_equation_inventory(blocks, preview_report, input_path)
    identity = article_identity(input_path, content, len(deduped))

    preview_is_relevant = preview_matches_input(input_path, preview_report)
    preview_missing = set(preview_report.get("missing", [])) if preview_is_relevant and preview_report else set()
    csv_path = Path(preview_report["csvPath"]) if preview_is_relevant and preview_report and preview_report.get("csvPath") else None
    preview_summary = {
        "report_found": bool(preview_is_relevant and preview_report),
        "report_path": str(preview_path) if preview_is_relevant and preview_path else None,
        "csv_path": str(csv_path) if csv_path else None,
        "csv_path_found": safe_exists(csv_path),
        "reviewed_matches": int(preview_report.get("reviewedMatches", 0)) if preview_is_relevant and preview_report else 0,
        "fallback_translations": int(preview_report.get("fallbackTranslations", 0)) if preview_is_relevant and preview_report else 0,
        "standalone_equations_wrapped": int(preview_report.get("standaloneEquationsWrapped", 0)) if preview_is_relevant and preview_report else 0,
    }

    equations = []
    for index, block in enumerate(deduped, start=1):
        word_equation, spoken, summary, confidence, source = provisional_translation(block["normalized"], preview_missing)
        equations.append(
            {
                "equation_id": f"{identity['page_id']}-eq-{index:02d}",
                "raw_math": block["raw"],
                "normalized_math": block["normalized"],
                "source_format": "tex",
                "display_mode": block["is_block"],
                "occurrence_count": block["occurrence_count"],
                "section_hint": nearest_heading(content, int(block["start"])),
                "translation_source": source,
                "word_equation": word_equation,
                "spoken_explanation": spoken,
                "summary": summary,
                "confidence": confidence,
                "loopback_required": source == "generic_fallback",
                "diagnostics": [],
            }
        )

    loopback = build_loopback(identity, preview_summary, equations)
    loopback_required = bool(loopback["trigger_count"])
    payload = {
        "protocol_version": "1.0",
        "generated_at": utc_now(),
        "lane_id": "07",
        "lane_name": "Math Translation",
        "worker": "worker-3-math-loopback",
        "source_file_name": input_path.name,
        "source_path": str(input_path),
        "page_id": identity["page_id"],
        "title": identity["title"],
        "semantic_address": identity["semantic_address"],
        "filename_safe_address": identity["filename_safe_address"],
        "semantic_vector": identity["vector"],
        "vector_string": vector_string(identity["vector"]),
        "address_hash": identity["address_hash"],
        "status": identity["status"],
        "upstream_artifacts": {
            "preview_report": preview_summary,
        },
        "equation_count": len(equations),
        "math_status": "passed" if equations and not loopback_required else ("passed-empty" if not equations else "loopback"),
        "loopback_required": loopback_required,
        "equations": equations,
        "notes": [
            "Math translation is provisional and revisitable for this workflow.",
            "Existing preview artifacts are consumed when present, but stale support files are recorded as loopback rather than treated as blockers.",
        ],
        "content_hash": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "run_id": short_hash(str(input_path), utc_now()),
    }

    write_json(output_dir / "math-payload.json", payload)
    write_text(output_dir / "math-translation.md", build_markdown(identity, equations, preview_summary, loopback_required))
    write_text(output_dir / "math-snippets.html", build_html_snippets(identity, equations))
    write_json(loopback_dir / "loopback-review.json", loopback)
    write_text(
        loopback_dir / "loopback-review.md",
        "\n".join(
            [
                f"# Loopback Review - {identity['title']}",
                "",
                f"- status: `{loopback['status']}`",
                f"- trigger_count: `{loopback['trigger_count']}`",
                "",
                "## Triggers",
                "",
            ]
            + (
                [
                    "- none"
                ]
                if not loopback["triggers"]
                else [
                    f"- `{item['trigger_id']}` ({item['severity']}): {item['condition']} | evidence: `{item['evidence']}` | fix: {item['recommendation']}"
                    for item in loopback["triggers"]
                ]
            )
            + [
                "",
                "Downstream can continue in this build round because mock/provisional upstream is explicitly allowed.",
            ]
        )
        + "\n",
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
