from __future__ import annotations

import json
import py_compile
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(r"\\dlowenas\brain\knowledge-refinery")
BRAIN = Path(r"\\dlowenas\brain")
MODELS = BRAIN / "models"
REPORT_DIR = ROOT / "12_HEALTH"

REQUIRED_DIRS = [
    "00_INTAKE",
    "01_CONVERSION",
    "02_NORMALIZATION",
    "03_ROUTING",
    "04_MODEL_STATIONS",
    "05_WORKFLOW_RUNS",
    "06_HTML_REPORTS",
    "07_OBSIDIAN_EXPORT",
    "08_ARCHIVE",
    "09_MEMORY",
    "10_PROMPTS",
    "11_CONFIG",
    "12_HEALTH",
    "scripts",
]

REQUIRED_FILES = [
    "README.md",
    "MODEL_STATION_MAP.md",
    "PAGE_ARCHITECTURE_PRODUCTION_STANDARD.md",
    "07_OBSIDIAN_EXPORT/THEOPHYSICS_PRODUCTION_PAGE_TEMPLATE.md",
    "10_PROMPTS/generate_page_layers.md",
    "11_CONFIG/station_registry.json",
    "11_CONFIG/page_layer_station_map.json",
]

ROOT_WORKFLOWS = [
    "session-handoff-drop",
    "paper-proof-grader",
    "link-pull-drop",
    "ai-portal-generator",
    "axioms",
    "ollama",
    "models",
]

MODEL_FOLDERS = [
    "math_verify",
    "claim_extract",
    "fact_verify",
    "contradiction_detect",
    "timeline_verify",
    "paper_review",
]


def check_url(url: str) -> str:
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return f"OK HTTP {response.status}"
    except Exception as exc:
        return f"WARN {exc.__class__.__name__}: {exc}"


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []

    for rel in REQUIRED_DIRS:
        path = ROOT / rel
        rows.append({"area": "refinery", "check": rel, "status": "OK" if path.exists() else "FAIL", "detail": str(path)})

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        rows.append({"area": "required_file", "check": rel, "status": "OK" if path.exists() else "FAIL", "detail": str(path)})

    for config_name in ["station_registry.json", "page_layer_station_map.json"]:
        registry = ROOT / "11_CONFIG" / config_name
        try:
            json.loads(registry.read_text(encoding="utf-8-sig"))
            rows.append({"area": "config", "check": config_name, "status": "OK", "detail": str(registry)})
        except Exception as exc:
            rows.append({"area": "config", "check": config_name, "status": "FAIL", "detail": str(exc)})

    for name in ROOT_WORKFLOWS:
        path = BRAIN / name
        rows.append({"area": "root_workflow", "check": name, "status": "OK" if path.exists() else "FAIL", "detail": str(path)})

    for name in MODEL_FOLDERS:
        path = MODELS / name
        item_count = len(list(path.iterdir())) if path.exists() else 0
        status = "OK" if path.exists() else "FAIL"
        detail = f"{path} items={item_count}"
        rows.append({"area": "model_station", "check": name, "status": status, "detail": detail})

    for script in [ROOT / "scripts" / "refinery_healthcheck.py"]:
        try:
            py_compile.compile(str(script), doraise=True)
            rows.append({"area": "python", "check": script.name, "status": "OK", "detail": str(script)})
        except Exception as exc:
            rows.append({"area": "python", "check": script.name, "status": "FAIL", "detail": str(exc)})

    rows.append({"area": "service", "check": "Ollama", "status": check_url("http://localhost:11434/api/tags").split()[0], "detail": check_url("http://localhost:11434/api/tags")})
    rows.append({"area": "service", "check": "Qdrant", "status": check_url("http://192.168.1.177:6333/collections").split()[0], "detail": check_url("http://192.168.1.177:6333/collections")})
    rows.append({"area": "service", "check": "Infinity", "status": check_url("http://192.168.1.177:7997").split()[0], "detail": check_url("http://192.168.1.177:7997")})

    failures = [row for row in rows if row["status"] == "FAIL"]
    warnings = [row for row in rows if row["status"] == "WARN"]
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = REPORT_DIR / f"REFINERY_HEALTHCHECK_{stamp}.md"
    latest = REPORT_DIR / "REFINERY_HEALTHCHECK.latest.md"

    lines = [
        "# Knowledge Refinery Healthcheck",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Root: `{ROOT}`",
        f"- Failures: {len(failures)}",
        f"- Warnings: {len(warnings)}",
        "",
        "| Area | Check | Status | Detail |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['area']} | {row['check']} | {row['status']} | `{row['detail'].replace('|', '\\|')}` |")

    text = "\n".join(lines) + "\n"
    report.write_text(text, encoding="utf-8")
    latest.write_text(text, encoding="utf-8")

    print(f"Failures: {len(failures)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Report: {latest}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
