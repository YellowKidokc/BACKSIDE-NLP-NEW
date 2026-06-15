"""
PROMPT LIBRARY SMOKE TEST
==========================
Verifies the prompt library is wired correctly. Runs all 10 prompts
against a short paper and prints the section names + first key of each result.

Usage:
    python prompts_smoketest.py "path/to/paper.md"

Requires: OPENAI_API_KEY in env. Run SET_OPENAI_KEY.ps1 first if needed.
"""
import os
import sys
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

try:
    from openai import OpenAI
except ImportError:
    print("[ERROR] openai package not installed. pip install openai")
    sys.exit(1)

from prompts import run_all  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print("Usage: python prompts_smoketest.py <path-to-paper.md>")
        sys.exit(1)

    paper_path = Path(sys.argv[1])
    if not paper_path.exists():
        print(f"[ERROR] Paper not found: {paper_path}")
        sys.exit(1)

    if not os.environ.get("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY not set in environment.")
        print("        Run SET_OPENAI_KEY.ps1 in this shell first.")
        sys.exit(1)

    content = paper_path.read_text(encoding="utf-8", errors="ignore")
    print(f"[INFO] Loaded paper: {paper_path.name} ({len(content)} chars)")

    client = OpenAI()
    print("[INFO] Running all 10 peer-review prompts...")
    print()

    results = run_all(content, client)

    for section, result in results.items():
        if "error" in result:
            print(f"  [ERROR] {section}: {result['error'][:100]}")
        else:
            keys = list(result.keys())[:5]
            print(f"  [OK]    {section}: keys={keys}")

    print()
    out_path = paper_path.parent / f"{paper_path.stem}_snapshot_sections.json"
    out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[INFO] Wrote results to: {out_path}")
    print()
    print("Smoke test complete. If all 10 sections show [OK], the prompt library is healthy.")


if __name__ == "__main__":
    main()
