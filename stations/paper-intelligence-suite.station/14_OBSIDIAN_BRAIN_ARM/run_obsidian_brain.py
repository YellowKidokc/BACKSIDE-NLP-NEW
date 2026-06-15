from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


HERE = Path(__file__).resolve().parent
SUITE_DIR = HERE.parent

if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from obsidian_pipeline import run_obsidian_sync  # noqa: E402


def _slugify(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "_" for ch in value).strip("_")
    return cleaned[:80] or "vault"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the Obsidian brain-arm intake pipeline inside the paper intelligence suite.",
    )
    parser.add_argument("--vault", required=True, help="Vault root or subfolder to scan.")
    parser.add_argument(
        "--output",
        help="Output root. Defaults to OUTPUT/obsidian_brain/<vault>_<timestamp>/",
    )
    parser.add_argument(
        "--publish-html-dir",
        action="append",
        default=[],
        help="Optional extra HTML publish target. Repeat for multiple targets.",
    )
    args = parser.parse_args()

    vault = Path(args.vault).expanduser()
    if not vault.exists() or not vault.is_dir():
        raise FileNotFoundError(f"Vault path not found or not a directory: {vault}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_output = SUITE_DIR / "OUTPUT" / "obsidian_brain" / f"{_slugify(vault.name)}_{timestamp}"
    output_root = Path(args.output).expanduser() if args.output else default_output
    output_root.mkdir(parents=True, exist_ok=True)

    result = run_obsidian_sync(
        vault_path=str(vault),
        data_root=str(output_root),
        publish_html_dirs=args.publish_html_dir,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
