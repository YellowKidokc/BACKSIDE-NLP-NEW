"""
ST-ROUTE-001 — Route Classifier.

Inspect a dropped file, detect type, assign workflow lane, produce routing.yml.

Usage:
    python run.py --in <path_to_any_file> --out <path_to_routing.yml>

The routing.yml is what 13_document_converter reads next.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

STATION_ID = "ST-ROUTE-001"

# extension -> (file_type, lane, next_station)
ROUTING_MAP = {
    ".pdf":        ("pdf",         "text",  "ST-CONV-001"),
    ".html":       ("html",        "text",  "ST-CONV-001"),
    ".htm":        ("html",        "text",  "ST-CONV-001"),
    ".docx":       ("docx",        "text",  "ST-CONV-001"),
    ".doc":        ("doc",         "text",  "ST-CONV-001"),
    ".md":         ("markdown",    "text",  "ST-CLAIM-001"),   # already markdown — skip CONV
    ".markdown":   ("markdown",    "text",  "ST-CLAIM-001"),
    ".txt":        ("text",        "text",  "ST-CONV-001"),
    ".rtf":        ("rtf",         "text",  "ST-CONV-001"),
    ".epub":       ("epub",        "text",  "ST-CONV-001"),

    ".json":       ("json",        "data",  "ST-TBD-000"),
    ".yml":        ("yaml",        "data",  "ST-TBD-000"),
    ".yaml":       ("yaml",        "data",  "ST-TBD-000"),
    ".csv":        ("csv",         "data",  "ST-TBD-000"),

    ".mp3":        ("audio",       "audio", "ST-TBD-000"),
    ".wav":        ("audio",       "audio", "ST-TBD-000"),
    ".m4a":        ("audio",       "audio", "ST-TBD-000"),
    ".flac":       ("audio",       "audio", "ST-TBD-000"),

    ".mp4":        ("video",       "video", "ST-TBD-000"),
    ".webm":       ("video",       "video", "ST-TBD-000"),
    ".mov":        ("video",       "video", "ST-TBD-000"),
    ".mkv":        ("video",       "video", "ST-TBD-000"),
}


def is_transcript(path: Path) -> bool:
    """Heuristic: txt/md with 'transcript' in name."""
    return path.suffix.lower() in {".txt", ".md"} and "transcript" in path.stem.lower()


def classify(path: Path) -> dict:
    suffix = path.suffix.lower()
    if is_transcript(path):
        file_type, lane, nxt = "transcript", "text", "ST-CLAIM-001"
    elif suffix in ROUTING_MAP:
        file_type, lane, nxt = ROUTING_MAP[suffix]
    else:
        file_type, lane, nxt = "unknown", "archive", "ST-TBD-000"

    return {
        "station":          STATION_ID,
        "input_path":       str(path),
        "input_filename":   path.name,
        "input_size_bytes": path.stat().st_size if path.exists() else None,
        "extension":        suffix,
        "file_type":        file_type,
        "lane":             lane,
        "normalized_path":  str(path.resolve()) if path.exists() else str(path),
        "next_station":     nxt,
        "classified_at":    datetime.now().isoformat(timespec="seconds"),
    }


def write_yaml(d: dict, out: Path) -> None:
    """Minimal YAML writer — flat key:value scalars only."""
    lines = []
    for k, v in d.items():
        if v is None:
            lines.append(f"{k}: ~")
        elif isinstance(v, (int, float)):
            lines.append(f"{k}: {v}")
        else:
            s = str(v).replace('"', '\\"')
            lines.append(f'{k}: "{s}"')
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True)
    parser.add_argument("--out", dest="out", required=True)
    args = parser.parse_args()

    path = Path(args.inp)
    result = classify(path)
    write_yaml(result, Path(args.out))

    # Also drop the JSON form alongside for downstream consumption.
    json_out = Path(args.out).with_suffix(".json")
    json_out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps({"status": "ok", "file_type": result["file_type"],
                      "lane": result["lane"], "next": result["next_station"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
