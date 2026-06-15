"""
ST-TIME-002 — Timeline / temporal extraction.

STUB. David will show me which model/library to wire here.
The HF snapshot `timeline_temporal_information` is downloaded
(per MODELS/MODEL_INVENTORY.md) but the exact model id and
inference recipe are not yet defined.

Usage (once wired):
    python run.py --in <input.md> --out <output.json>

Expected output (placeholder):
    {
      "station": "ST-TIME-002",
      "events": [{"text": "...", "date": "YYYY-MM-DD", "type": "..."}, ...]
    }
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

STATION_ID = "ST-TIME-002"
MODEL_ID = "M-TIME-001"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True)
    parser.add_argument("--out", dest="out", required=True)
    args = parser.parse_args()

    result = {
        "station":     STATION_ID,
        "model":       MODEL_ID,
        "status":      "stub",
        "note":        "Awaiting David's guidance on which library/recipe to use for the timeline_temporal_information snapshot.",
        "input_path":  args.inp,
        "computed_at": datetime.now().isoformat(timespec="seconds"),
    }
    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": "stub", "station": STATION_ID}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
