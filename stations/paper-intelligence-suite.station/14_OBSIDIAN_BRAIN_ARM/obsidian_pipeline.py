from __future__ import annotations

import csv
import hashlib
import html
import json
import os
import re
import shutil
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml


SKIP_DIRS = {
    ".obsidian",
    ".git",
    "node_modules",
    ".trash",
    "__pycache__",
}

TEXT_EXTENSIONS = {".md", ".txt", ".canvas", ".json"}
NOTE_EXTENSIONS = {".md", ".canvas", ".txt"}
ATTACHMENT_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".svg",
    ".mp4",
    ".mp3",
    ".wav",
}

GENERIC_TITLES = {
    "document",
    "index",
    "new document",
    "note",
    "notes",
    "readme",
    "untitled",
}

STATUS_MAP = {
    "active": "working",
    "canonical": "canonical",
    "distilled": "distilled",
    "draft": "raw",
    "final": "canonical",
    "published": "canonical",
    "raw": "raw",
    "working": "working",
}

TYPE_MAP = {
    "analysis": "analysis",
    "article": "paper",
    "attachment": "attachment",
    "axiom": "claim",
    "axiom compendium": "axiom-compendium",
    "axiom compendium complete": "axiom-compendium",
    "bibliography": "reference",
    "breakdown": "analysis",
    "canvas": "canvas",
    "claim": "claim",
    "definition": "claim",
    "framework": "framework",
    "glossary": "reference",
    "guide": "reference",
    "index": "index",
    "journal": "journal",
    "law": "claim",
    "manuscript": "paper",
    "method": "methodology",
    "methodology": "methodology",
    "model": "framework",
    "monograph": "paper",
    "note": "note",
    "paper": "paper",
    "protocol": "methodology",
    "readme": "index",
    "reference": "reference",
    "review": "analysis",
    "scoring system": "methodology",
    "source": "reference",
    "study guide": "reference",
    "system": "framework",
    "theorem": "claim",
    "theory": "framework",
}

TAG_HINTS = {
    "axiom": "axioms",
    "consciousness": "consciousness",
    "defense depth": "defense-depth",
    "ecclesiastes": "ecclesiastes",
    "entropy": "entropy",
    "foundational papers": "foundational-papers",
    "framework": "framework",
    "grace": "grace",
    "knowledge": "knowledge",
    "logos": "logos",
    "master eq": "master-equation",
    "master equation": "master-equation",
    "methodology": "methodology",
    "paper": "paper",
    "scientific method": "scientific-method",
    "structural coherence": "structural-coherence",
    "ten laws": "ten-laws",
    "theophysics": "theophysics",
    "utdgs": "utdgs",
    "wisdom": "wisdom",
}

FOLDER_TAG_HINTS = {
    "ai knowledge": "ai-knowledge",
    "axiom foundations": "axiom-foundations",
    "foundational papers": "foundational-papers",
    "master eq": "master-equation",
    "scientific method": "scientific-method",
}


@dataclass
class PipelinePaths:
    captures_dir: Path
    understood_dir: Path
    digests_dir: Path
    knowledge_dir: Path
    memory_dir: Path


def _now() -> datetime:
    return datetime.now()


def _timestamp_slug() -> str:
    return _now().strftime("%Y%m%d_%H%M%S")


def _safe_slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip())
    return cleaned.strip("-._") or "vault"


def _normalize_text(value: str) -> str:
    cleaned = value.replace("\\", " ").replace("/", " ")
    cleaned = re.sub(r"\[[^\]]+\]", " ", cleaned)
    cleaned = re.sub(r"[_-]+", " ", cleaned)
    cleaned = re.sub(r"[^\w\s]+", " ", cleaned, flags=re.UNICODE)
    return re.sub(r"\s+", " ", cleaned).strip().lower()


def _contains_phrase(text: str, *phrases: str) -> bool:
    haystack = _normalize_text(text)
    if not haystack:
        return False

    for phrase in phrases:
        normalized = _normalize_text(phrase)
        if normalized and re.search(rf"\b{re.escape(normalized)}\b", haystack):
            return True
    return False


def _clean_inline_markdown(text: str) -> str:
    cleaned = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    cleaned = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", cleaned)
    cleaned = re.sub(
        r"\[\[([^\]]+)\]\]",
        lambda match: Path(match.group(1).split("#", 1)[0]).name.replace("_", " "),
        cleaned,
    )
    cleaned = cleaned.replace("—", " - ").replace("–", " - ")
    cleaned = cleaned.replace("_", " ")
    cleaned = re.sub(r"[`*~]+", "", cleaned)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def _humanize_stem(stem: str) -> str:
    parts = re.sub(r"[_-]+", " ", stem).strip().split()
    rendered: list[str] = []
    for part in parts:
        if re.fullmatch(r"[A-Z]{2,5}", part):
            rendered.append(part)
        elif re.fullmatch(r"v\d+(\.\d+)*", part, flags=re.IGNORECASE):
            rendered.append(part.lower())
        elif part.isupper() and len(part) > 5:
            rendered.append(part.title())
        else:
            rendered.append(part)
    return " ".join(rendered).strip() or stem


def _is_generic_title(value: str) -> bool:
    return _normalize_text(value) in GENERIC_TITLES


def _is_meta_heading(candidate: str) -> bool:
    normalized = _normalize_text(candidate)
    if not normalized:
        return True
    if not re.search(r"[A-Za-z]", candidate):
        return True
    if normalized in {"abstract", "canonical navigation", "quick navigation"}:
        return True
    if "read this first" in normalized or "supersedes all prior versions" in normalized:
        return True
    return False


def _read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="ignore")


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n") and text != "---":
        return {}, text

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    end_index = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() in {"---", "..."}:
            end_index = idx
            break

    if end_index is None:
        return {}, text

    raw_frontmatter = "\n".join(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :])

    try:
        parsed = yaml.safe_load(raw_frontmatter) or {}
        if not isinstance(parsed, dict):
            parsed = {}
    except Exception:
        parsed = {}

    return parsed, body


def _extract_tags(text: str, frontmatter: dict[str, Any]) -> list[str]:
    tags: set[str] = set()

    fm_tags = frontmatter.get("tags", [])
    if isinstance(fm_tags, str):
        fm_tags = [fm_tags]
    if isinstance(fm_tags, list):
        for tag in fm_tags:
            if isinstance(tag, str) and tag.strip():
                tags.add(tag.strip().lstrip("#"))

    for tag in re.findall(r"(?<![\w\[])#([A-Za-z0-9/_-]+)", text):
        tags.add(tag.strip())

    return sorted(tags)


def _infer_tags(source_path: str, title: str, summary: str, body: str, explicit_tags: list[str]) -> list[str]:
    inferred: set[str] = set()
    explicit = {tag.lower() for tag in explicit_tags}
    scope = " ".join([source_path, title, summary]) if summary else " ".join([source_path, title, body[:1200]])
    limited_when_explicit = {"canonical", "logos", "master-equation", "ten-laws", "theophysics"}

    parent_name = Path(source_path).parent.name
    folder_tag = FOLDER_TAG_HINTS.get(_normalize_text(parent_name))
    if folder_tag and folder_tag not in explicit:
        inferred.add(folder_tag)

    for phrase, tag in TAG_HINTS.items():
        if tag in explicit:
            continue
        if explicit and tag not in limited_when_explicit:
            continue
        if _contains_phrase(scope, phrase):
            inferred.add(tag)

    return sorted(inferred)


def _extract_wikilinks(text: str) -> list[str]:
    links = set()
    for match in re.findall(r"\[\[([^\]]+)\]\]", text):
        target = match.split("|", 1)[0].strip()
        if target and target != "..." and not target.startswith("#"):
            links.add(target)
    return sorted(links)


def _extract_heading_title(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        candidate = ""
        if stripped.startswith("#"):
            candidate = re.sub(r"^#+\s*", "", stripped).strip()
        elif stripped.startswith("**") and stripped.endswith("**") and len(stripped) > 4:
            candidate = stripped.strip("* ").strip()

        cleaned = _clean_inline_markdown(candidate)
        if cleaned and not _is_meta_heading(cleaned):
            return cleaned
    return ""


def _extract_title(file_path: Path, frontmatter: dict[str, Any], body: str) -> str:
    frontmatter_title = _clean_inline_markdown(str(frontmatter.get("title") or "").strip())
    if frontmatter_title and not _is_generic_title(frontmatter_title):
        return frontmatter_title

    heading_title = _extract_heading_title(body)
    if heading_title:
        return heading_title

    return _humanize_stem(file_path.stem)


def _is_summary_paragraph(line_block: str) -> bool:
    lines = [line.strip() for line in line_block.splitlines() if line.strip()]
    if not lines:
        return False
    if all(line.startswith("- ") or line.startswith("* ") for line in lines):
        return False
    if any(line.startswith("> [!") for line in lines[:2]):
        return False
    return True


def _clean_summary_paragraph(line_block: str) -> str:
    lines = [line.strip() for line in line_block.splitlines() if line.strip()]
    cleaned_lines: list[str] = []

    for line in lines:
        normalized = _normalize_text(line)
        if not normalized:
            continue
        if line.startswith("#") or line.startswith("```") or line.startswith("!["):
            continue
        if re.fullmatch(r"[-*]{3,}", line):
            continue
        if line.startswith("> [!"):
            continue
        if line.startswith("|") and line.endswith("|"):
            continue
        if _contains_phrase(
            normalized,
            "canonical navigation",
            "quick navigation",
            "ring 2 canonical grounding",
            "ring 3 framework connections",
        ):
            continue
        candidate = _clean_inline_markdown(line)
        if re.fullmatch(r"(author|created|date|publish|status|updated|uuid)\s+.*", candidate.lower()):
            continue
        if re.search(r"\b(19|20)\d{2}\b", candidate) and len(candidate.split()) <= 8:
            continue
        if candidate.lower().startswith("by ") and len(candidate.split()) <= 8:
            continue
        if candidate:
            cleaned_lines.append(candidate)

    candidate = " ".join(cleaned_lines)
    candidate = re.sub(r"\s+", " ", candidate).strip()
    if len(candidate) < 40:
        return ""
    return candidate


def _summarize_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""

    for index, line in enumerate(lines):
        if _normalize_text(_clean_inline_markdown(line)) == "abstract":
            for paragraph in re.split(r"\n\s*\n", "\n".join(lines[index + 1 :])):
                if not _is_summary_paragraph(paragraph):
                    continue
                candidate = _clean_summary_paragraph(paragraph)
                if candidate:
                    return candidate[:320]

    candidates = []
    for paragraph in re.split(r"\n\s*\n", text):
        if not _is_summary_paragraph(paragraph):
            continue
        candidate = _clean_summary_paragraph(paragraph)
        if candidate:
            candidates.append(candidate)

    if not candidates:
        fallback = _clean_inline_markdown(" ".join(lines[:6]))
        return fallback[:320]

    summary = candidates[0]
    if len(summary) < 90 and len(candidates) > 1:
        summary = f"{summary} {candidates[1]}"
    return summary[:320]


def _map_status(frontmatter: dict[str, Any]) -> str | None:
    raw_status = frontmatter.get("status")
    if raw_status is None:
        return None
    return STATUS_MAP.get(_normalize_text(str(raw_status)))


def _map_frontmatter_type(frontmatter: dict[str, Any]) -> str | None:
    for key in ("knowledge_type", "type", "classification", "document_type", "kind"):
        raw_value = frontmatter.get(key)
        if raw_value is None:
            continue
        mapped = TYPE_MAP.get(_normalize_text(str(raw_value)))
        if mapped:
            return mapped
    return None


def _infer_domain(path_context: str, tags: list[str], title: str, summary: str) -> str:
    haystack = " ".join([path_context, " ".join(tags), title, summary])
    if _contains_phrase(haystack, "theophysics", "axiom", "ten laws", "master equation", "logos", "structural coherence", "trinity"):
        return "theophysics"
    if _contains_phrase(haystack, "bible", "genesis", "hebrew", "greek", "scripture", "ecclesiastes"):
        return "bible"
    if _contains_phrase(haystack, "forge", "tiptap", "axum", "rust", "cloudflare"):
        return "forge"
    if _contains_phrase(haystack, "research", "paper", "study", "dataset"):
        return "research"
    if _contains_phrase(haystack, "ops", "deploy", "server", "infra", "automation"):
        return "operations"
    return "general"


def _infer_status(path_context: str, frontmatter: dict[str, Any]) -> str:
    if _contains_phrase(path_context, "raw", "inbox", "captures", "draft", "scratch"):
        return "raw"
    mapped = _map_status(frontmatter)
    if mapped:
        return mapped
    if _contains_phrase(path_context, "canon", "canonical", "final", "published"):
        return "canonical"
    if _contains_phrase(path_context, "concept", "entity", "reference"):
        return "distilled"
    return "working"


def _infer_knowledge_type(path_context: str, ext: str, frontmatter: dict[str, Any], title: str, summary: str) -> str:
    if ext == ".canvas":
        return "canvas"
    if ext in ATTACHMENT_EXTENSIONS:
        return "attachment"
    explicit_type = _map_frontmatter_type(frontmatter)
    if explicit_type:
        return explicit_type

    haystack = " ".join([path_context, title, summary])
    if _contains_phrase(haystack, "index", "readme", "table of contents"):
        return "index"
    if _contains_phrase(haystack, "axioms theophysics complete", "axiomatic framework", "188 axioms", "complete read through"):
        return "axiom-compendium"
    if _contains_phrase(haystack, "methodology", "defense depth", "grading system", "scoring system", "framework for theory evaluation", "scientific method"):
        return "methodology"
    if _contains_phrase(haystack, "analysis", "comparison", "breakdown", "critique", "recommendations for consolidation"):
        return "analysis"
    if _contains_phrase(haystack, "foundational papers", "paper", "monograph", "manuscript"):
        return "paper"
    if _contains_phrase(haystack, "master equation", "ten laws", "full explanation", "canonical rewrite", "framework"):
        return "framework"
    if _contains_phrase(haystack, "journal", "daily log", "daily note"):
        return "journal"
    if _contains_phrase(haystack, "reference", "source", "glossary", "study guide"):
        return "reference"
    if _contains_phrase(haystack, "entity", "person", "place", "organization"):
        return "entity"
    if _contains_phrase(haystack, "concept", "idea", "theory", "model"):
        return "concept"
    if _contains_phrase(haystack, "claim", "axiom", "law"):
        return "claim"
    if _contains_phrase(haystack, "evidence"):
        return "evidence"
    if _contains_phrase(haystack, "task", "todo"):
        return "task"
    return "note"


def _confidence(source_type: str, summary: str) -> dict[str, float]:
    if source_type in {"canvas", "attachment"}:
        return {"extracted": 0.55, "inferred": 0.35, "ambiguous": 0.10}
    if not summary:
        return {"extracted": 0.40, "inferred": 0.45, "ambiguous": 0.15}
    return {"extracted": 0.75, "inferred": 0.20, "ambiguous": 0.05}


def _parse_canvas(path: Path) -> tuple[str, dict[str, Any]]:
    try:
        payload = json.loads(_read_text(path))
    except Exception:
        return "", {"node_count": 0, "edge_count": 0, "file_refs": []}

    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    edges = payload.get("edges", []) if isinstance(payload, dict) else []
    file_refs = []
    text_nodes = []

    for node in nodes:
        if not isinstance(node, dict):
            continue
        if isinstance(node.get("file"), str):
            file_refs.append(node["file"])
        if isinstance(node.get("text"), str) and node["text"].strip():
            text_nodes.append(node["text"].strip())

    text = "\n".join(text_nodes)
    meta = {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "file_refs": file_refs,
    }
    return text, meta


def _json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_ready(item) for item in value]
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    return value


def _scan_file(vault_root: Path, file_path: Path) -> dict[str, Any]:
    ext = file_path.suffix.lower()
    relative_path = str(file_path.relative_to(vault_root)).replace("\\", "/")
    source_path = str(file_path)
    path_context = f"{source_path} {relative_path}"
    stat = file_path.stat()

    frontmatter: dict[str, Any] = {}
    body = ""
    canvas_meta: dict[str, Any] = {}

    if ext == ".canvas":
        body, canvas_meta = _parse_canvas(file_path)
    elif ext in TEXT_EXTENSIONS:
        raw = _read_text(file_path)
        frontmatter, body = _parse_frontmatter(raw)

    title = _extract_title(file_path, frontmatter, body)
    explicit_tags = _extract_tags(body, frontmatter) if body else _extract_tags("", frontmatter)
    wikilinks = _extract_wikilinks(body) if body else []
    summary = _summarize_text(body)
    inferred_tags = _infer_tags(source_path, title, summary, body, explicit_tags)
    tags = sorted(set(explicit_tags) | set(inferred_tags))

    source_type = (
        "note" if ext == ".md" else
        "canvas" if ext == ".canvas" else
        "text" if ext == ".txt" else
        "attachment"
    )

    content_hash = hashlib.sha1(
        f"{relative_path}|{stat.st_mtime_ns}|{stat.st_size}".encode("utf-8")
    ).hexdigest()

    record = {
        "doc_id": content_hash[:16],
        "source_path": source_path,
        "relative_path": relative_path,
        "source_type": source_type,
        "knowledge_type": _infer_knowledge_type(path_context, ext, frontmatter, title, summary),
        "domain": _infer_domain(path_context, tags, title, summary),
        "status": _infer_status(path_context, frontmatter),
        "title": title,
        "summary": summary,
        "tags": tags,
        "explicit_tags": explicit_tags,
        "inferred_tags": inferred_tags,
        "wikilinks": wikilinks,
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "word_count": len(re.findall(r"\b\w+\b", body)),
        "heading_count": len(re.findall(r"^\s*#+\s+", body, flags=re.MULTILINE)),
        "frontmatter": _json_ready(frontmatter),
        "confidence": _confidence(source_type, summary),
    }

    if canvas_meta:
        record.update(canvas_meta)

    return record


def _iter_vault_files(vault_root: Path) -> list[Path]:
    files: list[Path] = []
    for current_root, dir_names, file_names in os.walk(vault_root):
        dir_names[:] = [d for d in dir_names if d.lower() not in SKIP_DIRS]
        current = Path(current_root)
        for file_name in file_names:
            path = current / file_name
            ext = path.suffix.lower()
            if ext in NOTE_EXTENSIONS or ext in ATTACHMENT_EXTENSIONS or ext == ".json":
                files.append(path)
    return sorted(files)


def _ensure_paths(data_root: Path) -> PipelinePaths:
    captures_dir = data_root / "captures" / "obsidian"
    understood_dir = data_root / "understood" / "obsidian"
    digests_dir = data_root / "digests" / "obsidian"
    knowledge_dir = data_root / "knowledge" / "obsidian"
    memory_dir = data_root / "memory" / "obsidian"

    for path in [captures_dir, understood_dir, digests_dir, knowledge_dir, memory_dir]:
        path.mkdir(parents=True, exist_ok=True)

    return PipelinePaths(
        captures_dir=captures_dir,
        understood_dir=understood_dir,
        digests_dir=digests_dir,
        knowledge_dir=knowledge_dir,
        memory_dir=memory_dir,
    )


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(_json_ready(payload), indent=2, ensure_ascii=False), encoding="utf-8")


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(_json_ready(record), ensure_ascii=False) + "\n")


def _write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    fieldnames = [
        "doc_id",
        "relative_path",
        "source_type",
        "knowledge_type",
        "domain",
        "status",
        "title",
        "summary",
        "modified_at",
        "size_bytes",
        "word_count",
        "heading_count",
        "tags",
        "wikilinks",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["tags"] = ", ".join(record.get("tags", []))
            row["wikilinks"] = ", ".join(record.get("wikilinks", []))
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def _html_table_rows(records: list[dict[str, Any]], limit: int = 120) -> str:
    rows = []
    for record in records[:limit]:
        rows.append(
            "<tr>"
            f"<td>{html.escape(record['relative_path'])}</td>"
            f"<td>{html.escape(record['knowledge_type'])}</td>"
            f"<td>{html.escape(record['domain'])}</td>"
            f"<td>{html.escape(record['status'])}</td>"
            f"<td>{html.escape(record['title'])}</td>"
            f"<td>{html.escape(record['summary'])}</td>"
            f"<td>{html.escape(', '.join(record.get('tags', [])))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def _render_html(summary: dict[str, Any], records: list[dict[str, Any]]) -> str:
    scanned_at = html.escape(summary["scanned_at"])
    vault_path = html.escape(summary["vault_path"])
    total_docs = summary["total_docs"]

    domain_items = "".join(
        f"<li><strong>{html.escape(name)}</strong>: {count}</li>"
        for name, count in summary["by_domain"].items()
    )
    type_items = "".join(
        f"<li><strong>{html.escape(name)}</strong>: {count}</li>"
        for name, count in summary["by_knowledge_type"].items()
    )
    status_items = "".join(
        f"<li><strong>{html.escape(name)}</strong>: {count}</li>"
        for name, count in summary["by_status"].items()
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Obsidian Brain Digest</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #0f1418;
      --panel: #182028;
      --line: #2b3947;
      --text: #e9f0f5;
      --muted: #9fb0be;
      --accent: #e3a93a;
    }}
    body {{
      margin: 0;
      font-family: Georgia, "Segoe UI", serif;
      background:
        radial-gradient(circle at top right, rgba(227, 169, 58, 0.16), transparent 28%),
        linear-gradient(180deg, #0f1418 0%, #101820 100%);
      color: var(--text);
    }}
    .wrap {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 32px 24px 64px;
    }}
    .hero {{
      border: 1px solid var(--line);
      background: rgba(24, 32, 40, 0.92);
      padding: 28px;
      border-radius: 20px;
      margin-bottom: 24px;
      box-shadow: 0 12px 42px rgba(0, 0, 0, 0.24);
    }}
    h1, h2 {{
      margin: 0 0 8px;
      letter-spacing: 0.02em;
    }}
    p, li {{
      color: var(--muted);
      line-height: 1.55;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin: 24px 0;
    }}
    .card {{
      border: 1px solid var(--line);
      background: rgba(15, 20, 24, 0.65);
      border-radius: 16px;
      padding: 18px;
    }}
    .stat {{
      font-size: 2rem;
      font-weight: 700;
      color: var(--accent);
      margin-top: 10px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
      background: rgba(24, 32, 40, 0.88);
      border: 1px solid var(--line);
      border-radius: 16px;
      overflow: hidden;
    }}
    th, td {{
      padding: 12px 14px;
      text-align: left;
      vertical-align: top;
      border-bottom: 1px solid rgba(43, 57, 71, 0.75);
      font-size: 0.92rem;
    }}
    th {{
      position: sticky;
      top: 0;
      background: #17212b;
      color: var(--text);
    }}
    .eyebrow {{
      text-transform: uppercase;
      letter-spacing: 0.2em;
      font-size: 0.76rem;
      color: var(--accent);
      margin-bottom: 10px;
    }}
    code {{
      background: rgba(255,255,255,0.06);
      padding: 2px 6px;
      border-radius: 6px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <div class="eyebrow">Brain Intake Digest</div>
      <h1>Obsidian Aggregation Report</h1>
      <p>Scanned <code>{vault_path}</code> on {scanned_at}. This is the canonical browser view for the current intake pass. Spreadsheet export exists alongside it for sorting and manual review.</p>
      <div class="grid">
        <div class="card"><div>Total Documents</div><div class="stat">{total_docs}</div></div>
        <div class="card"><div>Markdown Notes</div><div class="stat">{summary["by_source_type"].get("note", 0)}</div></div>
        <div class="card"><div>Canvases</div><div class="stat">{summary["by_source_type"].get("canvas", 0)}</div></div>
        <div class="card"><div>Attachments</div><div class="stat">{summary["by_source_type"].get("attachment", 0)}</div></div>
      </div>
    </section>

    <section class="grid">
      <div class="card">
        <h2>By Domain</h2>
        <ul>{domain_items}</ul>
      </div>
      <div class="card">
        <h2>By Knowledge Type</h2>
        <ul>{type_items}</ul>
      </div>
      <div class="card">
        <h2>By Status</h2>
        <ul>{status_items}</ul>
      </div>
    </section>

    <section class="card">
      <h2>Document Index</h2>
      <p>Showing the first 120 records. Full machine-readable output lives in JSON and JSONL under <code>understood/obsidian</code>, and the spreadsheet-friendly export lives next to this report.</p>
      <table>
        <thead>
          <tr>
            <th>Path</th>
            <th>Type</th>
            <th>Domain</th>
            <th>Status</th>
            <th>Title</th>
            <th>Summary</th>
            <th>Tags</th>
          </tr>
        </thead>
        <tbody>
          {_html_table_rows(records)}
        </tbody>
      </table>
    </section>
  </div>
</body>
</html>
"""


def _published_filename(directory: str) -> str:
    lowered = directory.lower()
    if "proof-explorer" in lowered:
        return "obsidian-brain-explorer.html"
    if "proof-architecture" in lowered:
        return "obsidian-brain-architecture.html"
    return "obsidian-brain-digest.html"


def _publish_html_outputs(html_report: str, csv_source_path: Path, publish_html_dirs: list[str]) -> list[str]:
    published: list[str] = []
    for raw_dir in publish_html_dirs:
        if not raw_dir:
            continue
        target_dir = Path(raw_dir)
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            html_target = target_dir / _published_filename(str(target_dir))
            html_target.write_text(html_report, encoding="utf-8")
            csv_target = target_dir / "obsidian-brain-digest.csv"
            shutil.copyfile(csv_source_path, csv_target)
            published.append(str(html_target))
        except Exception:
            continue
    return published


def run_obsidian_sync(vault_path: str, data_root: str, publish_html_dirs: list[str] | None = None) -> dict[str, Any]:
    if not vault_path:
        raise ValueError("vault_path is required")

    vault_root = Path(vault_path).expanduser()
    if not vault_root.exists() or not vault_root.is_dir():
        raise FileNotFoundError(f"Vault path not found or not a directory: {vault_root}")

    paths = _ensure_paths(Path(data_root))
    timestamp = _timestamp_slug()
    vault_slug = _safe_slug(vault_root.name)

    files = _iter_vault_files(vault_root)
    records = [_scan_file(vault_root, path) for path in files]

    by_source_type = Counter(record["source_type"] for record in records)
    by_domain = Counter(record["domain"] for record in records)
    by_knowledge_type = Counter(record["knowledge_type"] for record in records)
    by_status = Counter(record["status"] for record in records)
    tag_counter = Counter(tag for record in records for tag in record.get("tags", []))

    summary = {
        "vault_path": str(vault_root),
        "vault_name": vault_root.name,
        "vault_slug": vault_slug,
        "scanned_at": _now().isoformat(),
        "total_docs": len(records),
        "by_source_type": dict(sorted(by_source_type.items())),
        "by_domain": dict(sorted(by_domain.items())),
        "by_knowledge_type": dict(sorted(by_knowledge_type.items())),
        "by_status": dict(sorted(by_status.items())),
        "top_tags": tag_counter.most_common(25),
    }

    manifest = {
        "summary": summary,
        "files": [
            {
                "doc_id": record["doc_id"],
                "relative_path": record["relative_path"],
                "source_path": record["source_path"],
                "size_bytes": record["size_bytes"],
                "modified_at": record["modified_at"],
                "source_type": record["source_type"],
            }
            for record in records
        ],
    }

    manifest_path = paths.captures_dir / f"manifest_{vault_slug}_{timestamp}.json"
    latest_manifest_path = paths.captures_dir / "latest_manifest.json"
    classified_json_path = paths.understood_dir / f"classified_{vault_slug}_{timestamp}.json"
    latest_classified_path = paths.understood_dir / "latest_classified.json"
    classified_jsonl_path = paths.understood_dir / f"classified_{vault_slug}_{timestamp}.jsonl"
    latest_classified_jsonl_path = paths.understood_dir / "latest_classified.jsonl"
    csv_path = paths.digests_dir / f"digest_{vault_slug}_{timestamp}.csv"
    latest_csv_path = paths.digests_dir / "latest.csv"
    html_path = paths.digests_dir / f"digest_{vault_slug}_{timestamp}.html"
    latest_html_path = paths.digests_dir / "latest.html"
    summary_path = paths.digests_dir / "latest_summary.json"

    _write_json(manifest_path, manifest)
    _write_json(latest_manifest_path, manifest)
    _write_json(classified_json_path, records)
    _write_json(latest_classified_path, records)
    _write_jsonl(classified_jsonl_path, records)
    _write_jsonl(latest_classified_jsonl_path, records)
    _write_csv(csv_path, records)
    _write_csv(latest_csv_path, records)
    html_report = _render_html(summary, records)
    latest_html_path.write_text(html_report, encoding="utf-8")
    html_path.write_text(html_report, encoding="utf-8")
    _write_json(summary_path, summary)
    published_html = _publish_html_outputs(html_report, latest_csv_path, publish_html_dirs or [])

    return {
        "status": "ok",
        "vault_path": str(vault_root),
        "total_docs": len(records),
        "outputs": {
            "manifest": str(latest_manifest_path),
            "classified_json": str(latest_classified_path),
            "classified_jsonl": str(latest_classified_jsonl_path),
            "digest_html": str(latest_html_path),
            "digest_csv": str(latest_csv_path),
            "summary_json": str(summary_path),
            "published_html": published_html,
        },
        "summary": summary,
    }


def load_latest_obsidian_summary(data_root: str) -> dict[str, Any] | None:
    path = Path(data_root) / "digests" / "obsidian" / "latest_summary.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_latest_obsidian_html(data_root: str) -> str | None:
    path = Path(data_root) / "digests" / "obsidian" / "latest.html"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")
