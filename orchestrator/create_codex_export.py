"""
CREATE_CODEX_EXPORT.py  —  v2
Builds a clean, GitHub-ready export of the Theophysics Brain system.

Scope:
  - 49 named stations (code, configs, prompts, batch files)
  - Workflows (orchestrator workflows)
  - NLP model SHELLS (README, config — NOT weights)
  - Engine SHELLS (README, config — NOT trained state)
  - Orchestrator scripts
  - Architecture docs and standards

Excludes:
  - Model weights (.bin, .safetensors, .pt, .onnx, .gguf)
  - Runtime state (_outbox, _processed, _logs, _state, _exports)
  - Vector indexes, databases, private data
  - Files > 2MB
"""
from __future__ import annotations

import fnmatch, json, shutil
from datetime import datetime
from pathlib import Path
from typing import Any

SOURCE_ROOT = Path(r"X:\\")
DEST_ROOT = Path(r"C:\Users\lowes\Desktop") / "BACKSIDE-NLP-NEW"
GITHUB_REMOTE = "https://github.com/YellowKidokc/BACKSIDE-NLP-NEW.git"

# ── Station export mode: include ALL station folders except apps and legacy NLP ──
# Skip patterns: A_ prefix (apps), NLP_ prefix (legacy), .claude, _front_door, _inbox, etc.
STATION_SKIP_PREFIXES = {"A_", "NLP_", "."}
USE_WHITELIST = False  # False = export all stations except skipped prefixes

# ── Directories to skip inside any station/workflow ──
SKIP_DIRS = {
    "_outbox", "_exports", "_processed", "_logs", "_state",
    "__pycache__", ".venv", ".venv_science_nlp", "venv",
    ".git", ".cache", "#recycle", "node_modules",
    "onnx", "openvino", "d_brain_huggingface_hub",
}

# ── File types to exclude (model weights, binaries, databases) ──
EXCLUDE_EXTENSIONS = {
    ".bin", ".safetensors", ".pt", ".pth", ".gguf", ".onnx",
    ".pkl", ".faiss", ".sqlite", ".db", ".duckdb",
    ".pdf", ".docx", ".xlsx", ".pyc", ".zip",
    ".h5", ".msgpack", ".ot", ".npz", ".npy",
    ".wav", ".mp3", ".mp4", ".webm", ".ogg",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico",
}

# ── File types to include ──
INCLUDE_EXTENSIONS = {
    ".py", ".bat", ".ps1", ".md", ".txt", ".yaml", ".yml",
    ".json", ".toml", ".ini", ".jsonc", ".cfg",
    ".html", ".css", ".js",
}

MAX_FILE_SIZE = 2_000_000  # 2MB cap


def should_skip_dir(path: Path) -> bool:
    return path.name in SKIP_DIRS or (path / ".codex-exclude").exists()


def should_include_file(path: Path) -> bool:
    if path.suffix.lower() in EXCLUDE_EXTENSIONS:
        return False
    if path.suffix.lower() in INCLUDE_EXTENSIONS:
        return True
    return False


def copy_station_files(station_dir: Path, dest_base: Path) -> list[dict]:
    """Copy safe files from a single station folder."""
    copied = []
    for path in sorted(station_dir.rglob("*")):
        if path.is_dir():
            continue
        rel_to_station = path.relative_to(station_dir)
        if any(part in SKIP_DIRS for part in rel_to_station.parts):
            continue
        if not should_include_file(path):
            continue
        try:
            if path.stat().st_size > MAX_FILE_SIZE:
                continue
        except OSError:
            continue
        dest = dest_base / rel_to_station
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        copied.append({"path": str(rel_to_station), "size": path.stat().st_size})
    return copied


def copy_shell_only(source_dir: Path, dest_dir: Path, label: str) -> list[dict]:
    """Copy only README, config, and top-level script files (no deep content)."""
    copied = []
    dest_dir.mkdir(parents=True, exist_ok=True)
    for item in sorted(source_dir.iterdir()):
        if item.is_dir():
            sub_dest = dest_dir / item.name
            sub_dest.mkdir(parents=True, exist_ok=True)
            # Only copy shell files from each subdirectory
            for f in sorted(item.iterdir()):
                if f.is_file() and should_include_file(f):
                    try:
                        if f.stat().st_size > MAX_FILE_SIZE:
                            continue
                    except OSError:
                        continue
                    shutil.copy2(f, sub_dest / f.name)
                    copied.append({"path": f"{label}/{item.name}/{f.name}", "size": f.stat().st_size})
        elif item.is_file() and should_include_file(item):
            try:
                if item.stat().st_size > MAX_FILE_SIZE:
                    continue
            except OSError:
                continue
            shutil.copy2(item, dest_dir / item.name)
            copied.append({"path": f"{label}/{item.name}", "size": item.stat().st_size})
    return copied


def write_full_tree(output_file: Path) -> None:
    """Write X: drive folder tree showing architecture (excluded dirs marked)."""
    lines = ["# X: Drive Architecture Map", f"# Generated: {datetime.now():%Y-%m-%d %H:%M}", ""]
    for item in sorted(SOURCE_ROOT.iterdir()):
        if not item.is_dir() or item.name.startswith(".") or item.name == "#recycle":
            continue
        lines.append(f"{item.name}/")
        try:
            for sub in sorted(item.iterdir()):
                prefix = "  "
                if sub.is_dir():
                    tag = "  [EXCLUDED]" if sub.name in SKIP_DIRS else ""
                    lines.append(f"{prefix}{sub.name}/{tag}")
                else:
                    lines.append(f"{prefix}{sub.name}")
        except PermissionError:
            lines.append("  [ACCESS DENIED]")
    output_file.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    DEST_ROOT.mkdir(parents=True, exist_ok=True)
    all_copied: list[dict] = []
    stations_dir = SOURCE_ROOT / "04_STATIONS"
    workflows_dir = SOURCE_ROOT / "07_ORCHESTRATOR" / "workflows_legacy" / "workflows"
    mda_workflow_dir = SOURCE_ROOT / "07_ORCHESTRATOR" / "workflows_legacy" / "MDA-PUBLICATION"
    models_dir = SOURCE_ROOT / "05_MODELS"
    engines_dir = SOURCE_ROOT / "06_ENGINES"
    orchestrator_dir = SOURCE_ROOT / "07_ORCHESTRATOR"

    # 1. Export stations (all except A_ apps and NLP_ legacy)
    print("Scanning stations...")
    station_count = 0
    skip_also = {"_front_door", "_inbox", "_outbox", "_processed", "_state", "_logs", "_shared"}
    for station_path in sorted(stations_dir.iterdir()):
        if not station_path.is_dir():
            continue
        name = station_path.name
        if any(name.startswith(p) for p in STATION_SKIP_PREFIXES):
            continue
        if name in skip_also:
            continue
        dest = DEST_ROOT / "stations" / name
        copied = copy_station_files(station_path, dest)
        all_copied.extend(copied)
        station_count += 1
        print(f"  {name}: {len(copied)} files")
    print(f"Exported {station_count} stations.")

    # 2. Export workflows
    print("Exporting workflows...")
    if workflows_dir.exists():
        for wf in sorted(workflows_dir.iterdir()):
            if wf.is_dir():
                dest = DEST_ROOT / "workflows" / wf.name
                copied = copy_station_files(wf, dest)
                all_copied.extend(copied)
                print(f"  {wf.name}: {len(copied)} files")

    if mda_workflow_dir.exists():
        dest = DEST_ROOT / "workflows" / "MDA-PUBLICATION"
        copied = copy_station_files(mda_workflow_dir, dest)
        all_copied.extend(copied)
        print(f"  MDA-PUBLICATION: {len(copied)} files")

    # 3. Export NLP model shells (README/config only, no weights)
    print("Exporting NLP model shells...")
    copied = copy_shell_only(models_dir, DEST_ROOT / "models", "models")
    all_copied.extend(copied)
    print(f"  Models: {len(copied)} shell files")

    # 4. Export engine shells
    print("Exporting engine shells...")
    copied = copy_shell_only(engines_dir, DEST_ROOT / "engines", "engines")
    all_copied.extend(copied)
    print(f"  Engines: {len(copied)} shell files")

    # 5. Export orchestrator scripts (top-level only)
    print("Exporting orchestrator scripts...")
    orch_dest = DEST_ROOT / "orchestrator"
    orch_dest.mkdir(parents=True, exist_ok=True)
    for f in sorted(orchestrator_dir.iterdir()):
        if f.is_file() and should_include_file(f):
            try:
                if f.stat().st_size <= MAX_FILE_SIZE:
                    shutil.copy2(f, orch_dest / f.name)
                    all_copied.append({"path": f"orchestrator/{f.name}", "size": f.stat().st_size})
            except OSError:
                pass

    # 6. Copy station-level shared files and standards
    for fname in ["STATION_REGISTRY.json", "README.md", "TYPED_STATION_FOLDERS_20260613.md",
                   "STATION_CLEANUP_HANDOFF_LEDGER_20260602.md", "START.bat",
                   "HEALTHCHECK.bat", "PROCESS_INBOX.bat"]:
        src = stations_dir / fname
        if src.exists():
            shutil.copy2(src, DEST_ROOT / "stations" / fname)

    # 7. Write architecture tree
    print("Writing folder structure map...")
    write_full_tree(DEST_ROOT / "00_ARCHITECTURE_MAP.txt")

    # 8. Write manifest
    manifest = {
        "created": datetime.now().isoformat(timespec="seconds"),
        "source": str(SOURCE_ROOT),
        "stations_exported": station_count,
        "total_files_copied": len(all_copied),
        "files": all_copied,
    }
    (DEST_ROOT / "00_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    # 9. Write README
    readme = f"""# Theophysics Brain — Codex Export
**Generated: {datetime.now():%Y-%m-%d %H:%M}**
**POF 2828**

## What This Is
Clean export of the Theophysics Brain processing system for Codex.
Contains station code, workflow definitions, model/engine shells, and orchestrator scripts.

## What's Included
- **stations/** — {station_count} processing stations (Python, configs, batch files, prompts)
- **workflows/** — Multi-station workflow definitions
- **models/** — NLP model folder shells (README/config only, NO weights)
- **engines/** — Preference engine shells (README/config only, NO trained state)
- **orchestrator/** — Top-level orchestration scripts

## What's Excluded
Model weights, vector indexes, runtime state, logs, exports, private data, databases.

## Station Script Standard (SSS_v1)
Every station should follow this flow:
`ingest -> validate -> route/call NLP -> process -> write artifact -> update job card -> export/handoff -> archive/log`

Standard sections in every pipeline.py:
00_IMPORTS, 01_CONSTANTS_AND_PATHS, 02_CONFIG_LOADING, 03_LOGGING, 04_INGEST,
05_VALIDATE, 06_ROUTE_OR_CALL_WORKER, 07_PROCESS, 08_WRITE_ARTIFACTS,
09_UPDATE_JOB_CARD, 10_EXPORT_OR_HANDOFF, 11_ARCHIVE_INPUTS, 12_MAIN

## Architecture Layers
- Layer 0: Intake (drop folder, auto-route)
- Layer 1: Conversion (format normalization)
- Layer 2: NLPs/Models (processing horsepower)
- Layer 3: Stations (atomic 1:1 operations, 30-50 of them)
- Layer 4: Workflows (stations chained in sequence)
- Layer 5: Apps (self-contained independent systems)

## Key Rule
Station = one action. Workflow = many stations in order. App = whole independent system.
If a station does five things, split it.
"""
    (DEST_ROOT / "00_README_FOR_CODEX.md").write_text(readme, encoding="utf-8")

    # 10. Copy .gitignore
    gitignore_src = Path(r"X:\07_ORCHESTRATOR\gitignore_template.txt")
    if gitignore_src.exists():
        shutil.copy2(gitignore_src, DEST_ROOT / ".gitignore")
        print("Created .gitignore")

    print(f"\nDone. {len(all_copied)} files exported to:\n  {DEST_ROOT}")
    print(f"\nNext steps:")
    print(f"  cd {DEST_ROOT}")
    print(f"  git init")
    print(f"  git add .")
    print(f'  git commit -m "Initial export: {station_count} stations, workflows, model/engine shells"')
    print(f"  git remote add origin {GITHUB_REMOTE}")
    print(f"  git branch -M main")
    print(f"  git push -u origin main")


if __name__ == "__main__":
    main()
