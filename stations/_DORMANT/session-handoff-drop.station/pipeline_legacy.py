from __future__ import annotations

import json
import logging
import re
import shutil
import sys
from datetime import datetime
from html import unescape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
LOG_DIR = ROOT / "_LOGS"


def _setup_logging(name: str) -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    logfile = LOG_DIR / f"workflow_{name}_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger(f"workflow.{name}")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def _read_text(path: Path) -> str:
    if path.suffix.lower() in {".html", ".htm"}:
        raw = path.read_text(encoding="utf-8", errors="replace")
        raw = re.sub(r"(?is)<script.*?>.*?</script>", " ", raw)
        raw = re.sub(r"(?is)<style.*?>.*?</style>", " ", raw)
        raw = re.sub(r"(?s)<[^>]+>", "\n", raw)
        raw = unescape(raw)
        return raw
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="replace")


def _normalize_lines(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in text.split("\n")]
    return [line for line in lines if line]


def _extract_date(text: str, default_date: str) -> str:
    matches = re.findall(r"\b(20\d{2}-\d{2}-\d{2})\b", text)
    return matches[0] if matches else default_date


def _extract_layer(lines: list[str], layer_names: list[str]) -> list[str]:
    start = None
    end = None
    for i, line in enumerate(lines):
        lower = line.lower()
        if any(name in lower for name in layer_names):
            start = i + 1
            break
    if start is None:
        return []
    for j in range(start, len(lines)):
        lower = lines[j].lower()
        if lower.startswith("layer ") or lower.startswith("## layer ") or lower.startswith("### layer "):
            end = j
            break
    return lines[start:end]


def _collect_bullets(lines: list[str]) -> list[str]:
    bullets: list[str] = []
    for line in lines:
        if re.match(r"^[-*]\s+", line):
            bullets.append(re.sub(r"^[-*]\s+", "", line).strip())
        elif re.match(r"^\d+\.\s+", line):
            bullets.append(re.sub(r"^\d+\.\s+", "", line).strip())
        elif "—" in line or " - " in line:
            bullets.append(line.strip())
    return bullets


def _manifest_objects(items: list[str]) -> list[dict]:
    out = []
    for item in items:
        match = re.match(r"^(?P<path>[A-Za-z]:\\[^—]+|\\\\[^—]+|[A-Za-z0-9_.:-]+)\s+[—-]\s+(?P<desc>.+)$", item)
        if match:
            out.append({
                "path": match.group("path").strip(),
                "description": match.group("desc").strip()
            })
        else:
            out.append({
                "description": item
            })
    return out


def _decision_objects(items: list[str]) -> list[dict]:
    out = []
    for item in items:
        if ":" in item:
            topic, rest = item.split(":", 1)
            out.append({"topic": topic.strip(), "detail": rest.strip()})
        else:
            out.append({"detail": item})
    return out


def _open_thread_objects(items: list[str]) -> list[dict]:
    out = []
    for item in items:
        if "—" in item:
            topic, rest = item.split("—", 1)
            out.append({"topic": topic.strip(), "next_action": rest.strip()})
        elif ":" in item:
            topic, rest = item.split(":", 1)
            out.append({"topic": topic.strip(), "next_action": rest.strip()})
        else:
            out.append({"next_action": item})
    return out


def _render_markdown(session_date: str, ai_partner: str, manifest: list[dict], decisions: list[dict], threads: list[dict], source_name: str, canonical_inputs: list[str]) -> str:
    lines = [
        f"# SESSION LOG - {ai_partner} | {session_date}",
        "",
        "**Purpose**",
        "Convert a dropped full-page session recap into a startup-ready handoff with a strict machine layer and a readable human layer.",
        "",
        "**Canonical Inputs Used**",
    ]
    for item in canonical_inputs:
        lines.append(f"- `{item}`")
    lines.extend([
        f"- Source page: `{source_name}`",
        "",
        "## Layer 1 - Session Manifest",
    ])
    for item in manifest:
        if "path" in item:
            lines.append(f"- `{item['path']}` - {item['description']}")
        else:
            lines.append(f"- {item['description']}")
    lines.extend([
        "",
        "## Layer 2 - Decisions And Results",
    ])
    for item in decisions:
        if item.get("topic"):
            lines.append(f"- **{item['topic']}** - {item['detail']}")
        else:
            lines.append(f"- {item['detail']}")
    lines.extend([
        "",
        "## Layer 3 - Open Threads",
    ])
    for idx, item in enumerate(threads, 1):
        if item.get("topic"):
            lines.append(f"{idx}. **{item['topic']}** - {item['next_action']}")
        else:
            lines.append(f"{idx}. {item['next_action']}")
    lines.extend([
        "",
        "## Audit Footer",
        "",
        "### Where We Are Right",
        "The dropped page is now split into a machine-ingest manifest and a startup summary that another AI can use immediately.",
        "",
        "### Where We Might Be Wrong",
        "This parser trusts the three-layer structure. If the dropped page is freeform or missing the layer headers, the outputs will be thinner and should be reviewed once.",
        "",
        "### What We Think",
        "This is the right local workflow for handoff pages: drop, run, mirror, and start the next session from the generated summary instead of from raw chat history."
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    log = _setup_logging(cfg.get("name", "session-handoff-drop"))

    input_dir = Path(cfg["input_dir"])
    output_dir = Path(cfg["output_dir"])
    archive_dir = Path(cfg["archive_dir"])
    vault_output_dir = Path(cfg["vault_output_dir"])
    nas_output_dir = Path(cfg["nas_output_dir"])

    for path in (input_dir, output_dir, archive_dir, vault_output_dir, nas_output_dir):
        path.mkdir(parents=True, exist_ok=True)

    exts = {e.lower() for e in cfg.get("text_extensions", [".txt", ".md"])}
    files = sorted([p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in exts])
    log.info("found %d candidate files", len(files))
    if not files:
        log.info("nothing to do")
        return 0

    latest = max(files, key=lambda p: p.stat().st_mtime)
    log.info("processing %s", latest)
    text = _read_text(latest)
    lines = _normalize_lines(text)

    manifest_lines = _extract_layer(lines, ["layer 1", "session manifest"])
    decision_lines = _extract_layer(lines, ["layer 2", "decisions and results"])
    thread_lines = _extract_layer(lines, ["layer 3", "open threads"])

    manifest_items = _manifest_objects(_collect_bullets(manifest_lines))
    decision_items = _decision_objects(_collect_bullets(decision_lines))
    thread_items = _open_thread_objects(_collect_bullets(thread_lines))

    session_date = _extract_date(text, cfg.get("default_date", datetime.now().strftime("%Y-%m-%d")))
    ai_partner = cfg.get("default_ai_partner", "Codex")
    stem = latest.stem
    archived_input = archive_dir / latest.name

    json_name = f"{stem}_manifest.json"
    md_name = f"{stem}_summary.md"

    payload = {
        "session_date": session_date,
        "session_id": stem,
        "ai_partner": ai_partner,
        "source_file": str(archived_input),
        "source_original_path": str(latest),
        "source_archive_path": str(archived_input),
        "canonical_inputs_used": cfg.get("canonical_inputs", []),
        "layer_1_session_manifest": manifest_items,
        "layer_2_decisions_and_results": decision_items,
        "layer_3_open_threads": thread_items,
        "generated_at": datetime.now().isoformat(timespec="seconds")
    }
    markdown = _render_markdown(
        session_date=session_date,
        ai_partner=ai_partner,
        manifest=manifest_items,
        decisions=decision_items,
        threads=thread_items,
        source_name=str(archived_input),
        canonical_inputs=cfg.get("canonical_inputs", [])
    )

    json_path = output_dir / json_name
    md_path = output_dir / md_name
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")

    for target_dir in (nas_output_dir, vault_output_dir):
        shutil.copy2(json_path, target_dir / json_name)
        shutil.copy2(md_path, target_dir / md_name)

    if archived_input.exists():
        archived_input.unlink()
    shutil.move(str(latest), str(archived_input))

    log.info("json -> %s", json_path)
    log.info("markdown -> %s", md_path)
    log.info("mirrored to NAS -> %s", nas_output_dir / json_name)
    log.info("mirrored to vault -> %s", vault_output_dir / md_name)
    log.info("archived input -> %s", archived_input)
    return 0


if __name__ == "__main__":
    sys.exit(main())
