"""
ST-EMBED-001 — Science paper embeddings (SPECTER2).

SPECTER2 produces a single document-level embedding for a scientific paper,
expecting title + [SEP] + abstract format. Output dim 768 by default.

Usage (via scripts\\03_run_prompt.bat):
    python run.py --in <input.md> --out <output.json>

Input markdown convention:
    # <title>

    <abstract / body>

The first line starting with `# ` is treated as title; the rest is body.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

STATION_ID = "ST-EMBED-001"
MODEL_ID = "M-EMB-SCI-001"

MODEL_CACHE = Path(
    r"X:\knowledge-refinery\BACKSIDE\MODELS\_MODELS\HF_SNAPSHOTS\science_embeddings_specter2"
)


def load_model():
    try:
        from transformers import AutoTokenizer, AutoModel
        import torch  # noqa: F401
    except ImportError:
        print('{"status":"error","reason":"transformers/torch not installed."}', file=sys.stderr)
        sys.exit(4)

    if MODEL_CACHE.exists():
        path = str(MODEL_CACHE)
    else:
        path = "allenai/specter2_base"  # fallback to hub
    tok = AutoTokenizer.from_pretrained(path)
    mdl = AutoModel.from_pretrained(path)
    mdl.eval()
    return tok, mdl


def parse_title_body(text: str) -> tuple[str, str]:
    lines = text.splitlines()
    title = ""
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            body_start = i + 1
            break
    body = "\n".join(lines[body_start:]).strip()
    if not title:
        # No markdown heading — take first line as title, rest as body.
        if lines:
            title = lines[0].strip()
            body = "\n".join(lines[1:]).strip()
    return title, body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True)
    parser.add_argument("--out", dest="out", required=True)
    args = parser.parse_args()

    text = Path(args.inp).read_text(encoding="utf-8")
    title, body = parse_title_body(text)

    import torch
    tok, mdl = load_model()
    sep = tok.sep_token or "[SEP]"
    combined = f"{title}{sep}{body}"
    inputs = tok(combined, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        out = mdl(**inputs)
    # CLS token embedding
    cls = out.last_hidden_state[:, 0, :].squeeze(0).tolist()

    result = {
        "station":     STATION_ID,
        "model":       MODEL_ID,
        "title":       title,
        "body_chars":  len(body),
        "dim":         len(cls),
        "embedding":   cls,
        "computed_at": datetime.now().isoformat(timespec="seconds"),
    }
    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")

    md = (
        f"# {STATION_ID} result\n\n"
        f"Title: **{title}**\n\nDim: **{len(cls)}** | Model: `{MODEL_ID}` (SPECTER2)\n\n"
        f"Embedding stored in `{Path(args.out).name}`.\n"
    )
    Path(args.out).with_suffix(".md").write_text(md, encoding="utf-8")

    print(json.dumps({"status": "ok", "dim": len(cls)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
