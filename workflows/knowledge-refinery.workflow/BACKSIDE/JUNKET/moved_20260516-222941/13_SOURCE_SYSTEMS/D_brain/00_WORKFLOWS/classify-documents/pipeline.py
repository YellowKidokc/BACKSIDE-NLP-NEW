"""
classify-documents workflow.

For every text file under input_dir:
  1. Load the file (utf-8 with latin-1 fallback)
  2. SBERT embed (single vector saved to embeddings.npz at end)
  3. DeBERTa classify against the labels in 03_DEBERTA\\config.json
  4. Write a per-file JSON sidecar with embedding shape + top label + scores
  5. Write a single CSV summary in output_dir
"""
from __future__ import annotations

import csv
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
LOG_DIR = ROOT / "_LOGS"

for tool in ("02_SBERT", "03_DEBERTA"):
    p = ROOT / tool
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


def _setup_logging(name: str) -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    logfile = LOG_DIR / f"workflow_{name}_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger(f"workflow.{name}")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def main() -> int:
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    log = _setup_logging(cfg.get("name", "classify-documents"))

    input_dir = Path(cfg["input_dir"]) if cfg.get("input_dir") else None
    output_dir = Path(cfg["output_dir"]) if cfg.get("output_dir") else None
    if not input_dir or not output_dir:
        log.error("config.input_dir and config.output_dir must be set")
        return 1
    if not input_dir.exists():
        log.error("input_dir not found: %s", input_dir)
        return 1
    output_dir.mkdir(parents=True, exist_ok=True)

    exts = {e.lower() for e in cfg.get("text_extensions", [".txt"])}
    files = [p for p in sorted(input_dir.rglob("*")) if p.is_file() and p.suffix.lower() in exts]
    log.info("found %d files in %s", len(files), input_dir)
    if not files:
        return 0

    import sbert_runner
    import deberta_runner

    sb_cfg = json.loads((ROOT / "02_SBERT" / "config.json").read_text(encoding="utf-8"))
    db_cfg = json.loads((ROOT / "03_DEBERTA" / "config.json").read_text(encoding="utf-8"))
    labels = db_cfg["labels"]

    em = sbert_runner.Embedder(
        model_name=sb_cfg["model_settings"].get("model_name", "all-MiniLM-L6-v2"),
        device=sb_cfg["model_settings"].get("device", "auto"),
        cache_dir=sb_cfg.get("model_cache_dir"),
        max_seq_length=sb_cfg["model_settings"].get("max_seq_length"),
    )
    log.info("SBERT loaded dim=%d device=%s", em.dim, em.device)

    clf = deberta_runner.Classifier(
        model_name=db_cfg["model_settings"].get("model_name"),
        device=db_cfg["model_settings"].get("device", "auto"),
        cache_dir=db_cfg.get("model_cache_dir"),
        hypothesis_template=db_cfg["model_settings"].get("hypothesis_template", "This text is about {}."),
        multi_label=db_cfg["model_settings"].get("multi_label", False),
    )
    log.info("DeBERTa loaded device=%s labels=%d", clf.device, len(labels))

    texts: list[str] = []
    rels: list[str] = []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = f.read_text(encoding="latin-1", errors="replace")
        rels.append(str(f.relative_to(input_dir)))
        texts.append(content)

    log.info("embedding %d documents", len(texts))
    vecs = em.embed(texts, batch_size=int(sb_cfg["model_settings"].get("batch_size", 64)))

    summary_rows: list[dict] = []
    max_chars = int(db_cfg["model_settings"].get("max_text_chars", 2000))
    for i, (rel, text, vec) in enumerate(zip(rels, texts, vecs), 1):
        sidecar = {"path": rel, "embedding_dim": int(vec.size)}
        try:
            res = clf.classify(text[:max_chars] if max_chars > 0 else text, labels)
            sidecar["classification"] = res
            top_label, top_score = res["label"], res["score"]
        except Exception as e:
            log.exception("classify failed for %s: %s", rel, e)
            sidecar["classify_error"] = str(e)
            top_label, top_score = "", 0.0

        out = output_dir / Path(rel).with_suffix(".json")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(sidecar, ensure_ascii=False, indent=2), encoding="utf-8")
        summary_rows.append({"path": rel, "top_label": top_label, "top_score": round(top_score, 4)})
        if i % 25 == 0 or i == len(rels):
            log.info("[%d/%d]", i, len(rels))

    np.savez(output_dir / "embeddings.npz",
             ids=np.array(rels, dtype=object), vectors=vecs.astype(np.float32))

    summary_path = output_dir / cfg.get("summary_csv", "classify_summary.csv")
    with open(summary_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["path", "top_label", "top_score"])
        w.writeheader()
        w.writerows(summary_rows)
    log.info("summary -> %s", summary_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
