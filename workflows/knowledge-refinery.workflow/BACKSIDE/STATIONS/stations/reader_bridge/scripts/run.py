from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYSTEM_PROMPT = ROOT / "PROMPT_SYSTEM.md"


def read_required(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Required input missing: {path}")
    return path.read_text(encoding="utf-8")


def packet_dir(input_path: Path) -> Path:
    return input_path if input_path.is_dir() else input_path.parent


def extract_text(response) -> str:
    text = getattr(response, "output_text", None)
    if text:
        return text
    chunks: list[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            value = getattr(content, "text", None)
            if value:
                chunks.append(value)
    return "\n".join(chunks).strip()


def parse_json_output(raw: str) -> dict:
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return json.loads(text)


def call_ollama(model: str, instructions: str, user_input: str) -> str:
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    payload = {
        "model": model,
        "prompt": instructions + "\n\n" + user_input,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2,
            "num_ctx": int(os.getenv("OLLAMA_NUM_CTX", "16384")),
        },
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=int(os.getenv("OLLAMA_TIMEOUT", "180"))) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Ollama call failed at {url}: {exc}") from exc
    return str(data.get("response", "")).strip()


def bridge_markdown(data: dict) -> str:
    lines = ["# Reader Definition Bridge", ""]
    terms = data.get("term_definitions") or []
    if terms:
        lines += ["## Terms", ""]
        for item in terms:
            lines.append(f"### {item.get('term', 'Term')}")
            lines.append("")
            lines.append(str(item.get("plain_definition", "")).strip())
            if item.get("why_flagged"):
                lines.append("")
                lines.append(f"Flag: `{item['why_flagged']}`")
            lines.append("")
    themes = data.get("recurring_themes") or []
    if themes:
        lines += ["## Recurring Themes", ""]
        for item in themes:
            lines.append(f"### {item.get('theme', 'Theme')}")
            lines.append("")
            if item.get("plain_explanation"):
                lines.append(str(item["plain_explanation"]).strip())
                lines.append("")
            if item.get("analogy"):
                lines.append(f"Analogy: {str(item['analogy']).strip()}")
                lines.append("")
            if item.get("analogy_limits"):
                lines.append(f"Limit: {str(item['analogy_limits']).strip()}")
                lines.append("")
    if data.get("terms_not_safely_simplified"):
        lines += ["## Not Safely Simplified", ""]
        for item in data["terms_not_safely_simplified"]:
            lines.append(f"- {item}")
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Reader Definition Bridge station.")
    parser.add_argument("--in", dest="input_path", required=True, help="Packet directory or projection.academic.md path.")
    parser.add_argument("--out", dest="output_path", required=True, help="Output JSON path.")
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "qwen2.5:7b"))
    args = parser.parse_args()

    input_path = Path(args.input_path)
    packet = packet_dir(input_path)
    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    instructions = read_required(SYSTEM_PROMPT)
    academic_md = read_required(packet / "projection.academic.md")
    academic_json = read_required(packet / "projection.academic.json")
    snapshot = read_required(packet / "paper-snapshot.json")
    trace = read_required(packet / "trace-ledger.json")

    user_input = "\n\n".join(
        [
            "Run Reader Definition Bridge on this academic projection.",
            f"PACKET_DIR: {packet}",
            "ACADEMIC_PROJECTION_MD:\n```markdown\n" + academic_md + "\n```",
            "ACADEMIC_PROJECTION_JSON:\n```json\n" + academic_json + "\n```",
            "PAPER_SNAPSHOT_JSON:\n```json\n" + snapshot + "\n```",
            "TRACE_LEDGER_JSON:\n```json\n" + trace + "\n```",
        ]
    )

    raw = call_ollama(args.model, instructions, user_input)

    try:
        data = parse_json_output(raw)
    except json.JSONDecodeError:
        data = {
            "status": "needs_review",
            "projection_type": "reader_definition_bridge",
            "source_snapshot_id": "",
            "raw_model_output": raw,
            "warnings": ["Model output was not valid JSON."],
        }

    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_path.parent / "reader_bridge.md").write_text(bridge_markdown(data), encoding="utf-8")
    print(f"WROTE {output_path}")
    print(f"WROTE {output_path.parent / 'reader_bridge.md'}")
    return 0 if data.get("status") != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
