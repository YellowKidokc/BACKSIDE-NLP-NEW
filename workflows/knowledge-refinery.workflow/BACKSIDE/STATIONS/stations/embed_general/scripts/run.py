"""
ST-EMBED-006 — General sentence embeddings (MiniLM all-MiniLM-L6-v2).

Reads text input (markdown or plain), splits on blank lines into sentences,
returns a 384-dim normalized embedding per sentence.

Usage (via scripts\\03_run_prompt.bat):
    python run.py --in <input.md> --out <output.json>

Input:  text/markdown (blank-line-separated paragraphs treated as sentences).
Output: JSON with per-sentence embeddings + the sentences themselves.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

STATION_ID = "ST-EMBED-006"
MODEL_ID = "M-EMB-GEN-001"

# Local HF cache location for sentence-transformers/all-MiniLM-L6-v2.
# Per MODELS/MODEL_INVENTORY.md.
MODEL_CACHE = Path(
    r"X:\knowledge-refinery\BACKSIDE\MODELS\_MODELS\OTHER_MODELS"
    r"\from_userprofile_hf_cache\hub\models--sentence-transformers--all-MiniLM-L6-v2"
)


def load_model():
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print('{"status":"error","reason":"sentence-transformers not installed. pip install sentence-transformers"}',
              file=sys.stderr)
        sys.exit(4)

    # HF cache layout: models--<repo>/snapshots/<commit>/
    snapshot_root = MODEL_CACHE / "snapshots"
    if snapshot_root.is_dir():
        snapshots = [d for d in snapshot_root.iterdir() if d.is_dir()]
        if snapshots:
            return SentenceTransformer(str(snapshots[0]))
    # Fallback: let sentence-transformers resolve from HF hub / global cache.
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def split_sentences(text: str) -> list[str]:
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    return parts if parts else [text.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True)
    parser.add_argument("--out", dest="out", required=True)
    args = parser.parse_args()

    text = Path(args.inp).read_text(encoding="utf-8")
    sentences = split_sentences(text)

    model = load_model()
    vecs = model.encode(sentences, convert_to_numpy=True, normalize_embeddings=True)

    result = {
        "station":      STATION_ID,
        "model":        MODEL_ID,
        "n_sentences":  len(sentences),
        "dim":          int(vecs.shape[1]),
        "embeddings":   [v.tolist() for v in vecs],
        "sentences":    sentences,
        "computed_at":  datetime.now().isoformat(timespec="seconds"),
    }
    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")

    md = (
        f"# {STATION_ID} result\n\n"
        f"Sentences: **{len(sentences)}** | Dim: **{vecs.shape[1]}** | Model: `{MODEL_ID}` (MiniLM)\n\n"
        f"Embeddings stored in `{Path(args.out).name}`.\n"
    )
    Path(args.out).with_suffix(".md").write_text(md, encoding="utf-8")

    print(json.dumps({"status": "ok", "n": len(sentences), "dim": int(vecs.shape[1])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
