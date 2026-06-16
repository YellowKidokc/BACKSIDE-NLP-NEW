"""
ST-RERANK-008 — Cross-encoder reranker.

Scores (query, passage) pairs for retrieval ranking. Higher score = more relevant.

Usage (via scripts\\03_run_prompt.bat):
    python run.py --in <input.json> --out <output.json>

Input JSON:
    {
      "query":    "the search query",
      "passages": ["passage 1 text", "passage 2 text", ...]
    }

Output JSON: passages ranked by score (high to low).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

STATION_ID = "ST-RERANK-008"
MODEL_ID = "M-RERANK-001"

MODEL_PATH = Path(
    r"X:\knowledge-refinery\BACKSIDE\MODELS\_MODELS\OTHER_MODELS"
    r"\from_local_NLP_ACTIONS_models\nli\strong_cross_encoder"
)


def main() -> int:
    try:
        from sentence_transformers import CrossEncoder
    except ImportError:
        print('{"status":"error","reason":"sentence-transformers not installed."}', file=sys.stderr)
        return 4

    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True)
    parser.add_argument("--out", dest="out", required=True)
    args = parser.parse_args()

    payload = json.loads(Path(args.inp).read_text(encoding="utf-8"))
    query = payload["query"]
    passages = payload["passages"]

    model_arg = str(MODEL_PATH) if MODEL_PATH.exists() else "cross-encoder/ms-marco-MiniLM-L-6-v2"
    model = CrossEncoder(model_arg)
    pairs = [(query, p) for p in passages]
    scores = model.predict(pairs)

    ranked = sorted(
        [{"passage": p, "score": float(s)} for p, s in zip(passages, scores)],
        key=lambda x: x["score"],
        reverse=True,
    )

    result = {
        "station":     STATION_ID,
        "model":       MODEL_ID,
        "query":       query,
        "n_passages":  len(passages),
        "ranked":      ranked,
        "computed_at": datetime.now().isoformat(timespec="seconds"),
    }
    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")

    md_lines = [f"# {STATION_ID} ranked result", f"\nQuery: **{query}**\n"]
    for i, r in enumerate(ranked, 1):
        md_lines.append(f"{i}. ({r['score']:.4f}) {r['passage'][:200]}")
    Path(args.out).with_suffix(".md").write_text("\n".join(md_lines), encoding="utf-8")

    print(json.dumps({"status": "ok", "n": len(ranked)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
