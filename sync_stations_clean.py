"""
sync_stations_clean.py
Sync station CODE ONLY from NAS to D: — skip all data/exports/logs/cache.
Copies: pipeline.py, config.json, RUN.bat, README.md, prompts, scripts, wiring specs
Skips: _outbox, _processed, _logs, _inbox contents, EXPORTS, __pycache__, .git, .venv, node_modules, INPUT, OUTPUT, ARCHIVE, models

Usage: python sync_stations_clean.py
"""
import os, shutil
from pathlib import Path
from datetime import datetime

SRC = Path(r"\\192.168.2.50\brain\04_STATIONS")
DST = Path(r"D:\GitHub\BACKSIDE-NLP-NEW\stations")

# === SKIP RULES ===

# Skip these directory names entirely (case-insensitive match)
SKIP_DIRS = {
    "_outbox", "_processed", "_logs", "_inbox", "_state",
    "_archive", "_purge_candidate", "_migration_notes",
    "_ppk_integration_audit", "_ppk_runtime", "_private",
    "_source_imports_from_20251109_drive",
    "exports", "export", "_exports",
    "input", "output", "_output",
    "archive", "mirror_nas", "mirror_vault",
    "__pycache__", ".git", ".venv", ".cache",
    "node_modules", "dist", ".pytest_cache",
    "docker_package_20260507_191530",
    "online_codex_package", "reference",
    "scored_output", "input_canary",
    "input_claims-realpaper-mda043-20260601",
    "tts_edge", "drop_here",
    # Large app directories that aren't station code
    "gpt-researcher", "local-deep-researcher",
    "open-brain-map-main", "stratum-ai-claude-main",
    "organize-main", "behavioral-intelligence-layer-obs-plugin-final-claude",
    # Data folders
    "data", "sample_input", "samples", "tests",
    "calibration", "docs",
}

# Skip these prefixed directories
SKIP_DIR_PREFIXES = {
    "a_",  # A_BIL, A_GUI, A_openrecall, etc — apps not stations
    "nlp_",  # NLP data folders
    "input_",
}

# Skip files with these extensions
SKIP_EXT = {
    ".pyc", ".pyo", ".log", ".tmp", ".bak",
    ".safetensors", ".bin", ".pt", ".pth", ".h5", ".onnx",
    ".zip", ".tar", ".gz", ".7z",
    ".xlsx", ".xls", ".csv",  # data files
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico",
    ".mp3", ".wav", ".mp4",
    ".pdf",
    ".npz", ".npy",
    ".db", ".sqlite",
}

# Skip files over this size (500 KB)
MAX_FILE_SIZE = 500 * 1024

# KEEP these files regardless of extension (important station files)
ALWAYS_KEEP = {
    "pipeline.py", "pipeline_legacy.py",
    "config.json", "station.json", "wiring_spec.json",
    "run.bat", "start.bat", "install.bat", "healthcheck.bat",
    "front_door.bat", "troubleshoot.bat",
    "readme.md", "front_door_readme.md", "troubleshoot.md",
    "prompt.md", "requirements.txt",
    ".gitignore", ".gitkeep",
    "station_registry.json",
    "sss_template_v1.py", "sss_v1_standard.md",
    "core_8_nlp_cheat_sheet.md", "nlp_model_registry_detailed.md",
    "codex_build_core_8_stations.md",
}

def should_skip_dir(dirname):
    dl = dirname.lower()
    if dl in SKIP_DIRS:
        return True
    for prefix in SKIP_DIR_PREFIXES:
        if dl.startswith(prefix):
            return True
    return False

def should_copy_file(filepath):
    name = filepath.name.lower()
    # Always keep essential station files
    if name in ALWAYS_KEEP:
        return True
    # Skip by extension
    if filepath.suffix.lower() in SKIP_EXT:
        return False
    # Skip large files
    try:
        if filepath.stat().st_size > MAX_FILE_SIZE:
            return False
    except OSError:
        return False
    # Keep .py, .md, .json, .bat, .txt, .ps1, .ts, .js, .html (small ones)
    keep_ext = {".py", ".md", ".json", ".bat", ".txt", ".ps1",
                ".ts", ".js", ".mjs", ".html", ".yaml", ".yml",
                ".toml", ".cfg", ".ini", ".env", ".ahk", ".cmd"}
    if filepath.suffix.lower() in keep_ext:
        return True
    # Skip everything else
    return False


def main():
    print(f"Smart Station Sync")
    print(f"  From: {SRC}")
    print(f"  To:   {DST}")
    print(f"  Time: {datetime.now()}")
    print()

    copied = 0
    skipped_files = 0
    skipped_dirs = 0
    dirs_created = 0

    for root, dirs, files in os.walk(str(SRC)):
        # Filter dirs in-place to prevent descent
        original_dir_count = len(dirs)
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]
        skipped_dirs += original_dir_count - len(dirs)

        rel = Path(root).relative_to(SRC)
        dst_dir = DST / rel

        for f in files:
            src_file = Path(root) / f
            if should_copy_file(src_file):
                if not dst_dir.exists():
                    dst_dir.mkdir(parents=True, exist_ok=True)
                    dirs_created += 1
                dst_file = dst_dir / f
                try:
                    shutil.copy2(str(src_file), str(dst_file))
                    copied += 1
                except Exception as e:
                    print(f"  ERR: {rel / f}: {e}")
            else:
                skipped_files += 1

    # Create empty marker dirs for station structure
    for station_dir in DST.iterdir():
        if station_dir.is_dir() and station_dir.name.endswith(".station"):
            for sub in ["_inbox", "_outbox", "_processed", "_logs", "_state"]:
                marker = station_dir / sub
                marker.mkdir(exist_ok=True)
                gitkeep = marker / ".gitkeep"
                if not gitkeep.exists():
                    gitkeep.write_text("")

    print(f"\nDone!")
    print(f"  Files copied:      {copied}")
    print(f"  Files skipped:     {skipped_files}")
    print(f"  Dirs skipped:      {skipped_dirs}")
    print(f"  Dirs created:      {dirs_created}")


if __name__ == "__main__":
    main()
