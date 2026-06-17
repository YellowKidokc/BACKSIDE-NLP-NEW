"""
smart_sync.py — Whitelist-based station sync for Codex workflow.
POF 2828 | 2026-06-17

Syncs ONLY what Codex needs between NAS (X:\04_STATIONS) and D: repo.
Whitelist approach: nothing moves unless explicitly listed.

Usage:
  python smart_sync.py                    # dry run NAS → D:
  python smart_sync.py --go               # actually copy NAS → D:
  python smart_sync.py --push             # dry run D: → NAS
  python smart_sync.py --push --go        # actually copy D: → NAS
  python smart_sync.py --diff             # show files that differ
  python smart_sync.py --add my-station.station   # add station to whitelist
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
NAS_STATIONS = Path(r"\\192.168.2.50\brain\04_STATIONS")
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
]

# Combine all
WHITELIST = CORE_8 + SHARED + EXTENDED

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
}

# Max file size to sync (500 KB — anything bigger is data, not code)
MAX_FILE_KB = 500

# Files to always skip by name pattern
SKIP_FILES = {
    "desktop.ini", "thumbs.db", ".ds_store",
}

