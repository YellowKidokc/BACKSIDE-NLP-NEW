from __future__ import annotations

import json
import py_compile
import urllib.request
from datetime import datetime
from pathlib import Path

BRAIN_ROOT = Path(r"\\dlowenas\brain")
ROOT_CANDIDATES = [
    BRAIN_ROOT / "00_WORKFLOWS",
    BRAIN_ROOT / "WORKFLOWS",
]
ROOT = next((path for path in ROOT_CANDIDATES if path.exists()), ROOT_CANDIDATES[0])
LANES_ROOT = BRAIN_ROOT
LOG_ROOT = Path(r"\\dlowenas\brain\_LOGS")

WORKFLOWS = {
    "ai-portal-generator": {
        "folder": BRAIN_ROOT / "Backside" / "stations" / "ai-portal-generator.station",
        "required": ["config.json", "generator.py", "RUN_BUILD_AI_PORTAL.bat", "TROUBLESHOOT_AI_PORTAL.bat", "README.md"],
        "python": ["generator.py"],
        "json": ["config.json"],
    },
    "link-pull-drop": {
        "folder": BRAIN_ROOT / "Backside" / "stations" / "link-pull.station",
        "required": ["config.json", "pipeline.py", "RUN.bat", "PASTE_AND_RUN.bat", "TROUBLESHOOT.bat", "UPDATE.bat", "INSTALL.bat"],
        "python": ["pipeline.py"],
        "json": ["config.json"],
    },
    "paper-proof-grader": {
        "folder": BRAIN_ROOT / "Backside" / "stations" / "paper-proof-grader.station",
        "required": ["config.json", "pipeline.py", "RUN.bat", "MASTER_VARIABLE_SCHEMA.md", "README.md"],
        "python": ["pipeline.py", "fruits_of_spirit_bridge.py"],
        "json": ["config.json", "fruits_of_spirit_config.json"],
    },
    "session-handoff-drop": {
        "folder": BRAIN_ROOT / "Backside" / "stations" / "session-handoff-drop.station",
        "required": ["config.json", "pipeline.py", "RUN.bat"],
        "python": ["pipeline.py"],
        "json": ["config.json"],
    },
    "theophysics-comms-hub": {
        "folder": BRAIN_ROOT / "Backside" / "control-plane" / "theophysics-comms-hub",
        "required": ["README_COMMS_HUB_QUICK_START.md"],
        "python": [],
        "json": [],
    },
}


def check_url(url: str) -> str:
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return f"OK HTTP {response.status}"
    except Exception as exc:
        return f"WARN {exc.__class__.__name__}: {exc}"


def main() -> int:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []

    for name, spec in WORKFLOWS.items():
        folder = spec.get("folder", LANES_ROOT / name)
        rows.append({"workflow": name, "check": "folder", "status": "OK" if folder.exists() else "FAIL", "detail": str(folder)})
        for rel in spec["required"]:
            path = folder / rel
            rows.append({"workflow": name, "check": f"required:{rel}", "status": "OK" if path.exists() else "FAIL", "detail": str(path)})
        for rel in spec["json"]:
            path = folder / rel
            if not path.exists():
                continue
            try:
                json.loads(path.read_text(encoding="utf-8-sig"))
                rows.append({"workflow": name, "check": f"json:{rel}", "status": "OK", "detail": str(path)})
            except Exception as exc:
                rows.append({"workflow": name, "check": f"json:{rel}", "status": "FAIL", "detail": str(exc)})
        for rel in spec["python"]:
            path = folder / rel
            if not path.exists():
                continue
            try:
                py_compile.compile(str(path), doraise=True)
                rows.append({"workflow": name, "check": f"python:{rel}", "status": "OK", "detail": str(path)})
            except Exception as exc:
                rows.append({"workflow": name, "check": f"python:{rel}", "status": "FAIL", "detail": str(exc)})

    for path in [
        BRAIN_ROOT / "Backside" / "stations" / "paper-proof-grader.station" / "DROP_PAPERS_HERE",
        BRAIN_ROOT / "Backside" / "stations" / "paper-proof-grader.station" / "OUTPUT",
        BRAIN_ROOT / "Backside" / "stations" / "paper-proof-grader.station" / "ARCHIVE",
        BRAIN_ROOT / "Backside" / "stations" / "session-handoff-drop.station" / "DROP_HERE",
        BRAIN_ROOT / "Backside" / "stations" / "session-handoff-drop.station" / "OUTPUT",
        BRAIN_ROOT / "Backside" / "stations" / "session-handoff-drop.station" / "ARCHIVE",
        Path(r"\\dlowenas\brain\captures\links\DROP_HERE"),
        Path(r"\\dlowenas\brain\captures\links\OUTPUT"),
        Path(r"\\dlowenas\brain\captures\links\ARCHIVE"),
    ]:
        path.mkdir(parents=True, exist_ok=True)
        rows.append({"workflow": "shared", "check": "folder-ready", "status": "OK" if path.exists() else "FAIL", "detail": str(path)})

    rows.append({"workflow": "services", "check": "Infinity", "status": check_url("http://192.168.1.177:7997").split()[0], "detail": check_url("http://192.168.1.177:7997")})
    rows.append({"workflow": "services", "check": "Qdrant", "status": check_url("http://192.168.1.177:6333/collections").split()[0], "detail": check_url("http://192.168.1.177:6333/collections")})

    failures = [row for row in rows if row["status"] == "FAIL"]
    warnings = [row for row in rows if row["status"] == "WARN"]
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = ROOT / f"WORKFLOWS_HEALTHCHECK_REPORT_{stamp}.md"
    latest = ROOT / "WORKFLOWS_HEALTHCHECK_REPORT.latest.md"

    lines = [
        "# Workflows Healthcheck",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Root: `{ROOT}`",
        f"- Brain root: `{BRAIN_ROOT}`",
        f"- Workflow folders: `{LANES_ROOT}`",
        f"- Failures: {len(failures)}",
        f"- Warnings: {len(warnings)}",
        "",
        "| Workflow | Check | Status | Detail |",
        "|---|---|---|---|",
    ]
    for row in rows:
        detail = row["detail"].replace("|", "\\|")
        lines.append(f"| {row['workflow']} | {row['check']} | {row['status']} | `{detail}` |")
    text = "\n".join(lines) + "\n"
    report.write_text(text, encoding="utf-8")
    latest.write_text(text, encoding="utf-8")

    print(f"Failures: {len(failures)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Report: {report}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
