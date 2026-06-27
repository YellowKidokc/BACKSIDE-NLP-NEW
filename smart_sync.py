"""
smart_sync.py -- Whitelist-based station sync for Codex workflow.
POF 2828 | 2026-06-17

Syncs ONLY what Codex needs between X:\04_STATIONS (or NAS) and D: repo.
Whitelist approach: nothing moves unless explicitly listed.

Usage:
  python smart_sync.py                    # dry run X: -> D:
  python smart_sync.py --go               # actually copy X: -> D:
  python smart_sync.py --nas              # use NAS as source instead of X:
  python smart_sync.py --push             # dry run D: -> X:
  python smart_sync.py --push --go        # actually copy D: -> X:
  python smart_sync.py --diff             # show files that differ
  python smart_sync.py --core-only        # only sync Core 8 + _shared
  python smart_sync.py --add my-station.station   # add station to whitelist for this run
"""
import argparse
import hashlib
import os
import shutil
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────
X_STATIONS   = Path(r"X:\04_STATIONS")               # local working drive (default source)
NAS_STATIONS = Path(r"\\192.168.2.50\brain\04_STATIONS")  # NAS share (use --nas)
D_STATIONS   = Path(r"D:\GitHub\BACKSIDE-NLP-NEW\stations")

# ─────────────────────────────────────────────
# WHITELIST — only these folders get synced
# ─────────────────────────────────────────────
# Core 8 NLP stations (Codex's primary workspace)
CORE_8 = [
    "exec-summary.station",
    "plain-language.station",
    "claim-extraction.station",
    "claim-classification.station",
    "load-bearing-claims.station",
    "falsification.station",
    "evidence-map.station",
    "contradiction-scan.station",
]

# Shared infrastructure
SHARED = [
    "_shared",
]

# Other stations Codex may touch
EXTENDED = [
    "axioms.station",
    "paper-intelligence-suite.station",
    "paper-proof-grader.station",
    "html-article.station",
    "series-flow-auditor.station",
    "fruits-spirit-canon.station",
    "master-equation-canon.station",
    "operators-canon.station",
    "trinity-canon.station",
    "graph-linker.station",
    "metadata-extractor.station",
    "section-splitter.station",
    "summarizer.station",
    "mda-publication.station",
    # Added 2026-06-27 — present on X:\ but missing from repo
    "article-taxonomy-classifier.station",
    "chi-evaluator.station",
    "nabla-chi-classifier.station",
    "paper-grade-composer.station",
]

# Combine all
WHITELIST = CORE_8 + SHARED + EXTENDED

# Root-level files in stations/ to always sync (not inside a subfolder)
ROOT_FILES = [
    "STATION_REGISTRY.json",
    "README.md",
    "START.bat",
    "HEALTHCHECK.bat",
    "PROCESS_INBOX.bat",
]

# ─────────────────────────────────────────────
# FILE RULES — what counts as "code"
# ─────────────────────────────────────────────
CODE_EXTENSIONS = {
    ".py", ".md", ".json", ".bat", ".cmd", ".ps1",
    ".txt", ".yaml", ".yml", ".toml", ".ts", ".js",
    ".mjs", ".html", ".ahk", ".cfg",
}

# Skip these subdirectories inside whitelisted stations
SKIP_SUBDIRS = {
    "_outbox", "_processed", "_logs", "_inbox", "_state",
    "_archive", "_exports", "_purge_candidate",
    "_migration_notes", "_ppk_integration_audit",
    "_ppk_runtime", "_private",
    "exports", "export", "output", "_output",
    "input", "archive", "drop_here",
    "__pycache__", ".git", ".venv", ".cache",
    "node_modules", "dist", ".pytest_cache",
    "mirror_nas", "mirror_vault",
    "scored_output", "data", "sample_input",
    "tts_edge",
    # Station output/ready folders — contain processed papers, not code
    "03_final_ready", "02_final_review", "01_inbox_working",
}

# Max file size to sync (500 KB — anything bigger is data, not code)
MAX_FILE_KB = 500

# Files to always skip by name pattern
SKIP_FILES = {
    "desktop.ini", "thumbs.db", ".ds_store",
}


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def file_hash(path: Path) -> str:
    """Quick hash for change detection (first 8KB + size)."""
    h = hashlib.md5()
    try:
        size = path.stat().st_size
        h.update(str(size).encode())
        with open(path, "rb") as f:
            h.update(f.read(8192))
    except OSError:
        return ""
    return h.hexdigest()


def should_copy_file(filepath: Path) -> bool:
    """Check if a file qualifies as code worth syncing."""
    name_lower = filepath.name.lower()
    if name_lower in SKIP_FILES:
        return False
    if filepath.suffix.lower() not in CODE_EXTENSIONS:
        return False
    try:
        if filepath.stat().st_size > MAX_FILE_KB * 1024:
            return False
    except OSError:
        return False
    return True


def collect_files(base: Path, folders: list[str]) -> dict[str, Path]:
    """Walk whitelisted folders, return {relative_path: absolute_path}."""
    result = {}
    # Root-level files
    for fname in ROOT_FILES:
        fpath = base / fname
        if fpath.exists() and should_copy_file(fpath):
            result[fname] = fpath
    # Whitelisted folders
    for folder_name in folders:
        folder = base / folder_name
        if not folder.exists():
            continue
        for root, dirs, files in os.walk(str(folder)):
            # Filter subdirs in-place
            dirs[:] = [d for d in dirs if d.lower() not in SKIP_SUBDIRS]
            for f in files:
                fpath = Path(root) / f
                if should_copy_file(fpath):
                    rel = fpath.relative_to(base)
                    result[str(rel)] = fpath
    return result


def compare(src_files: dict, dst_base: Path) -> tuple[list, list, list]:
    """Compare src files against dst. Returns (new, changed, same)."""
    new, changed, same = [], [], []
    for rel, src_path in sorted(src_files.items()):
        dst_path = dst_base / rel
        if not dst_path.exists():
            new.append((rel, src_path))
        elif file_hash(src_path) != file_hash(dst_path):
            changed.append((rel, src_path, dst_path))
        else:
            same.append(rel)
    return new, changed, same


def do_sync(src_files: dict, dst_base: Path, dry_run: bool) -> dict:
    """Copy files from src to dst. Returns counts."""
    new, changed, same = compare(src_files, dst_base)
    counts = {"new": 0, "updated": 0, "same": len(same), "errors": 0}

    if new:
        print(f"\n  NEW ({len(new)} files):")
        for rel, src_path in new:
            print(f"    + {rel}")
            if not dry_run:
                dst_path = dst_base / rel
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.copy2(str(src_path), str(dst_path))
                    counts["new"] += 1
                except Exception as e:
                    print(f"      ERR: {e}")
                    counts["errors"] += 1

    if changed:
        print(f"\n  CHANGED ({len(changed)} files):")
        for rel, src_path, dst_path in changed:
            src_t = datetime.fromtimestamp(src_path.stat().st_mtime)
            dst_t = datetime.fromtimestamp(dst_path.stat().st_mtime)
            arrow = "->" if src_t > dst_t else "<-"
            print(f"    ~ {rel}  (src {src_t:%m/%d %H:%M} {arrow} dst {dst_t:%m/%d %H:%M})")
            if not dry_run:
                try:
                    shutil.copy2(str(src_path), str(dst_path))
                    counts["updated"] += 1
                except Exception as e:
                    print(f"      ERR: {e}")
                    counts["errors"] += 1

    if not new and not changed:
        print("\n  Everything in sync.")

    if dry_run and (new or changed):
        print(f"\n  DRY RUN -- nothing copied. Use --go to apply.")

    counts["new"] = len(new) if dry_run else counts["new"]
    counts["updated"] = len(changed) if dry_run else counts["updated"]
    return counts


def main():
    parser = argparse.ArgumentParser(description="Smart station sync (whitelist-based)")
    parser.add_argument("--go",        action="store_true", help="Actually copy (default is dry run)")
    parser.add_argument("--nas",       action="store_true", help="Use NAS as source instead of X:\\")
    parser.add_argument("--push",      action="store_true", help="Sync D: -> X:\\ (or NAS if --nas)")
    parser.add_argument("--diff",      action="store_true", help="Show diffs only, no copy")
    parser.add_argument("--core-only", action="store_true", help="Only sync Core 8 + _shared")
    parser.add_argument("--add",       type=str,            help="Add a station to the whitelist for this run")
    args = parser.parse_args()

    folders = CORE_8 + SHARED
    if not args.core_only:
        folders = WHITELIST
    if args.add:
        folders = folders + [args.add]

    remote_base = NAS_STATIONS if args.nas else X_STATIONS

    if args.push:
        src_base, dst_base = D_STATIONS, remote_base
        direction = f"D: -> {'NAS' if args.nas else 'X:\\'}"
    else:
        src_base, dst_base = remote_base, D_STATIONS
        direction = f"{'NAS' if args.nas else 'X:\\'} -> D:"

    mode = "DRY RUN" if not args.go else "LIVE"
    print(f"{'='*60}")
    print(f"  SMART SYNC -- {direction} [{mode}]")
    print(f"  {datetime.now():%Y-%m-%d %H:%M}")
    print(f"  Folders: {len(folders)} whitelisted")
    print(f"{'='*60}")

    # Check source is reachable
    if not src_base.exists():
        print(f"\n  ERROR: Source not reachable: {src_base}")
        print(f"  Is the NAS mounted?")
        return 1

    # Collect files
    print(f"\n  Scanning {src_base}...")
    src_files = collect_files(src_base, folders)
    print(f"  Found {len(src_files)} code files across {len(folders)} folders")

    if args.diff:
        new, changed, same = compare(src_files, dst_base)
        print(f"\n  New: {len(new)}  |  Changed: {len(changed)}  |  Same: {len(same)}")
        for rel, _ in new:
            print(f"    + {rel}")
        for rel, sp, dp in changed:
            print(f"    ~ {rel}")
        return 0

    # Sync
    counts = do_sync(src_files, dst_base, dry_run=not args.go)

    print(f"\n{'='*60}")
    print(f"  New: {counts['new']}  |  Updated: {counts['updated']}  |  Same: {counts['same']}  |  Errors: {counts['errors']}")
    print(f"{'='*60}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
