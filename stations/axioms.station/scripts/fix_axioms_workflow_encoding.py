#!/usr/bin/env python3
"""
Repair UTF-8 / Windows-1252 mojibake in axiom workflow text outputs.

Default use is intentionally narrow: GTQ-17 paper-grade text outputs in
X:/Backside/workflows/axioms.workflow/03_FINAL_READY.

Examples:
  python fix_axioms_workflow_encoding.py --dry-run
  python fix_axioms_workflow_encoding.py
  python fix_axioms_workflow_encoding.py --glob "*.paper-grade.html" --all
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[1] / "03_FINAL_READY"
DEFAULT_GLOBS = [
    "gtq-17-ran-the-numbers.paper-grade.html",
    "gtq-17-ran-the-numbers.paper-grade.md",
    "gtq-17-ran-the-numbers.paper-grade.json",
    "gtq-17-ran-the-numbers.claim-audit.csv",
]

TEXT_EXTENSIONS = {".html", ".md", ".json", ".csv", ".txt"}

SUSPECT_RE = re.compile(
    r"(Ã|Â|â€|â€œ|â€|â€™|â€“|â€”|Ï|Î|Â·|â†|âˆ|â‰|â€ž|â€¢|�)"
)

DIRECT_REPLACEMENTS = {
    # Common already-half-repaired sequences.
    "â€”": "-",
    "â€“": "-",
    "â€œ": '"',
    "â€": '"',
    "â€˜": "'",
    "â€™": "'",
    "â€¦": "...",
    "â€¢": "*",
    "â†’": "->",
    "â†": "<-",
    "â†”": "<->",
    "â‰¤": "<=",
    "â‰¥": ">=",
    "â‰ˆ": "~",
    "â‰ ": "!=",
    "âˆ’": "-",
    "âˆ‚": "d",
    "âˆ‘": "sum",
    "âˆž": "infinity",
    "Ï": "rho",
    "Ï‡": "chi",
    "Ïƒ": "sigma",
    "Î¦": "Phi",
    "Î±": "alpha",
    "Î²": "beta",
    "Î³": "gamma",
    "Ã—": "x",
    "Â·": ".",
    "Â ": " ",
    "Â": "",
    # Double-mojibake forms seen in paper-grade outputs.
    "Ã¢â‚¬â€": "-",
    "Ã¢â‚¬â€œ": "-",
    "Ã¢â‚¬Å“": '"',
    "Ã¢â‚¬Â": '"',
    "Ã¢â‚¬Ëœ": "'",
    "Ã¢â‚¬â„¢": "'",
    "Ã¢â‚¬Â¦": "...",
    "Ã¢â‚¬Â¢": "*",
    "Ã¢â€ â€™": "->",
    "Ã¢â€ Â": "<-",
    "Ã¢â€ â€": "<->",
    "Ã¢â€°Â¤": "<=",
    "Ã¢â€°Â¥": ">=",
    "Ã¢â€°Ë†": "~",
    "Ã¢Ë†â€™": "-",
    "Ã¢Ë†â€š": "d",
    "Ã¢Ë†â€˜": "sum",
    "Ã¢Ë†Å¾": "infinity",
    "ÃÂ": "rho",
    "Ãâ€¡": "chi",
    "ÃÆ’": "sigma",
    "ÃŽÂ¦": "Phi",
    "ÃŽÂ±": "alpha",
    "ÃŽÂ²": "beta",
    "ÃŽÂ³": "gamma",
    "Ãƒâ€”": "x",
    "Ã‚Â·": ".",
    "Ã‚": "",
}


@dataclass
class FileResult:
    path: Path
    changed: bool
    before_score: int
    after_score: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fix mojibake in axiom workflow text outputs.")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--glob", action="append", dest="globs", help="Glob(s) under root to process.")
    parser.add_argument("--all", action="store_true", help="Process matching globs recursively; default is GTQ-17 only.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show-diff", action="store_true")
    parser.add_argument("--no-backup", action="store_true")
    return parser.parse_args()


def suspicious_score(text: str) -> int:
    return len(SUSPECT_RE.findall(text))


def maybe_decode_mojibake(text: str) -> str:
    current = text
    for _ in range(3):
        candidates: list[str] = []
        for encoding in ("cp1252", "latin1"):
            try:
                candidates.append(current.encode(encoding, errors="strict").decode("utf-8", errors="strict"))
            except UnicodeError:
                pass
        if not candidates:
            break
        best = min(candidates, key=suspicious_score)
        if suspicious_score(best) < suspicious_score(current):
            current = best
        else:
            break
    return current


def normalize_text(text: str) -> str:
    current = maybe_decode_mojibake(text)
    for bad, good in DIRECT_REPLACEMENTS.items():
        current = current.replace(bad, good)
    if current.startswith("\ufeff"):
        current = current[1:]
    return current


def candidate_files(root: Path, globs: list[str], recursive: bool) -> list[Path]:
    files: list[Path] = []
    for pattern in globs:
        found = root.rglob(pattern) if recursive else root.glob(pattern)
        files.extend(path for path in found if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS)
    return sorted(set(files))


def repair_file(path: Path, dry_run: bool, show_diff: bool, backup_dir: Path | None) -> FileResult:
    original = path.read_text(encoding="utf-8", errors="replace")
    repaired = normalize_text(original)
    before = suspicious_score(original)
    after = suspicious_score(repaired)

    if repaired == original:
        return FileResult(path, False, before, after)

    if show_diff:
        print(f"\n--- diff: {path}")
        for line in difflib.unified_diff(
            original.splitlines(),
            repaired.splitlines(),
            fromfile=str(path),
            tofile=str(path) + " (fixed)",
            lineterm="",
        ):
            print(line)

    if not dry_run:
        if backup_dir is not None:
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup_dir / path.name)
        path.write_text(repaired, encoding="utf-8", newline="\n")

    return FileResult(path, True, before, after)


def main() -> int:
    args = parse_args()
    root = args.root
    if not root.exists():
        raise SystemExit(f"Root not found: {root}")

    globs = args.globs or DEFAULT_GLOBS
    files = candidate_files(root, globs, args.all)
    if not files:
        raise SystemExit(f"No matching text files found under {root}")

    backup_dir = None
    if not args.dry_run and not args.no_backup:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = root / f"_encoding_backups_{stamp}"

    print(f"Root: {root}")
    print(f"Files: {len(files)}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'WRITE'}")
    if backup_dir:
        print(f"Backup dir: {backup_dir}")

    changed = 0
    for path in files:
        result = repair_file(path, args.dry_run, args.show_diff, backup_dir)
        mark = "CHANGED" if result.changed else "same"
        if result.changed:
            changed += 1
        print(f"- {mark}: {path.name} suspicious {result.before_score}->{result.after_score}")

    print(f"Done. {'Would update' if args.dry_run else 'Updated'} {changed}/{len(files)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
