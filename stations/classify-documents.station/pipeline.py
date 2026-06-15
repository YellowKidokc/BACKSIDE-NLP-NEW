"""
classify-documents workflow.

For every text file under input_dir:
  1. Load the file (utf-8 with latin-1 fallback)
  2. SBERT embed (single vector saved to embeddings.npz at end)
  3. DeBERTa classify against the labels in 03_DEBERTA\\config.json
  4. Write per-file JSON sidecars under output_dir/json
  5. Write a CSV summary under output_dir/csv
"""
from __future__ import annotations

import csv
import hashlib
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
STATIONS_ROOT = HERE.parent
ROOT = STATIONS_ROOT.parent
SBERT_DIR = STATIONS_ROOT / "sbert-embedder.station"
DEBERTA_DIR = STATIONS_ROOT / "deberta-runner.station"
LOG_DIR = ROOT / "_logs"

for p in (SBERT_DIR, DEBERTA_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


def _setup_logging(name: str) -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
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


def _fallback_embed(texts: list[str], dim: int = 384) -> np.ndarray:
    vectors = np.zeros((len(texts), dim), dtype=np.float32)
    for row, text in enumerate(texts):
        tokens = [t.lower() for t in text.split() if len(t) > 2]
        if not tokens:
            tokens = [text[:64] or "empty"]
        for token in tokens[:2000]:
            digest = hashlib.sha256(token.encode("utf-8", errors="ignore")).digest()
            idx = int.from_bytes(digest[:4], "little") % dim
            vectors[row, idx] += 1.0
        norm = np.linalg.norm(vectors[row])
        if norm:
            vectors[row] /= norm
    return vectors


def _fallback_classify(text: str, labels: list[str]) -> dict:
    lower = text.lower()
    scored = []
    for label in labels:
        label_terms = [t for t in label.lower().split() if len(t) > 2]
        hits = sum(1 for term in label_terms if term in lower)
        score = hits / max(len(label_terms), 1)
        scored.append((label, score))
    scored.sort(key=lambda item: item[1], reverse=True)
    top_label, top_score = scored[0] if scored else ("unclassified", 0.0)
    if top_score == 0:
        top_label = "unclassified"
    return {
        "label": top_label,
        "score": float(top_score),
        "labels": [label for label, _ in scored],
        "scores": [float(score) for _, score in scored],
        "engine": "deterministic-fallback",
    }


def main() -> int:
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    log = _setup_logging(cfg.get("name", "classify-documents"))

    input_dir = Path(cfg["input_dir"]) if cfg.get("input_dir") else HERE / "INPUT"
    output_dir = Path(cfg["output_dir"]) if cfg.get("output_dir") else HERE / "EXPORTS"
    if not input_dir or not output_dir:
        log.error("config.input_dir and config.output_dir must be set")
        return 1
    if not input_dir.exists():
        log.error("input_dir not found: %s", input_dir)
        return 1
    output_dir.mkdir(parents=True, exist_ok=True)
    json_dir = output_dir / "json"
    csv_dir = output_dir / "csv"
    reports_dir = output_dir / "reports"
    vectors_dir = output_dir / "vectors"
    for export_dir in (json_dir, csv_dir, reports_dir, vectors_dir):
        export_dir.mkdir(parents=True, exist_ok=True)

    exts = {e.lower() for e in cfg.get("text_extensions", [".txt"])}
    files = [p for p in sorted(input_dir.rglob("*")) if p.is_file() and p.suffix.lower() in exts]
    log.info("found %d files in %s", len(files), input_dir)
    if not files:
        return 0

    sb_cfg = json.loads((SBERT_DIR / "config.json").read_text(encoding="utf-8"))
    db_cfg = json.loads((DEBERTA_DIR / "config.json").read_text(encoding="utf-8"))
    labels = db_cfg["labels"]
    model_mode = cfg.get("model_mode", "fallback")
    em = None
    clf = None
    engine_notes = []
    if model_mode != "fallback":
        try:
            import sbert_runner
            em = sbert_runner.InfinityClient(
                base_url=sb_cfg["infinity_url"],
                model=sb_cfg["model_settings"].get("model_name", "sentence-transformers/all-MiniLM-L6-v2"),
                http_batch_size=int(sb_cfg["model_settings"].get("http_batch_size", 32)),
            )
            log.info("Infinity SBERT loaded dim=%d", em.dim)
        except Exception as e:
            engine_notes.append(f"sbert_fallback: {e}")
            log.warning("SBERT unavailable, using deterministic fallback: %s", e)
        try:
            import deberta_runner
            clf = deberta_runner.Classifier(
                model_name=db_cfg["model_settings"].get("model_name"),
                device=db_cfg["model_settings"].get("device", "auto"),
                cache_dir=db_cfg.get("model_cache_dir"),
                hypothesis_template=db_cfg["model_settings"].get("hypothesis_template", "This text is about {}."),
                multi_label=db_cfg["model_settings"].get("multi_label", False),
            )
            log.info("DeBERTa loaded device=%s labels=%d", clf.device, len(labels))
        except Exception as e:
            engine_notes.append(f"deberta_fallback: {e}")
            log.warning("DeBERTa unavailable, using deterministic fallback: %s", e)
    else:
        engine_notes.append("model_mode=fallback")

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
    if em is not None:
        vecs = em.embed(texts, normalize=bool(sb_cfg["model_settings"].get("normalize_embeddings", True)))
        embedding_engine = "infinity-sbert"
    else:
        vecs = _fallback_embed(texts)
        embedding_engine = "deterministic-fallback"

    summary_rows: list[dict] = []
    max_chars = int(db_cfg["model_settings"].get("max_text_chars", 2000))
    for i, (rel, text, vec) in enumerate(zip(rels, texts, vecs), 1):
        sidecar = {"path": rel, "embedding_dim": int(vec.size)}
        try:
            if clf is not None:
                res = clf.classify(text[:max_chars] if max_chars > 0 else text, labels)
                res["engine"] = "deberta-zero-shot"
            else:
                res = _fallback_classify(text[:max_chars] if max_chars > 0 else text, labels)
            sidecar["classification"] = res
            sidecar["embedding_engine"] = embedding_engine
            sidecar["engine_notes"] = engine_notes
            top_label, top_score = res["label"], res["score"]
        except Exception as e:
            log.exception("classify failed for %s: %s", rel, e)
            sidecar["classify_error"] = str(e)
            top_label, top_score = "", 0.0

        out = json_dir / Path(rel).with_suffix(".json")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(sidecar, ensure_ascii=False, indent=2), encoding="utf-8")
        summary_rows.append({
            "path": rel,
            "top_label": top_label,
            "top_score": round(top_score, 4),
            "embedding_engine": embedding_engine,
            "classification_engine": sidecar.get("classification", {}).get("engine", "error"),
        })
        if i % 25 == 0 or i == len(rels):
            log.info("[%d/%d]", i, len(rels))

    np.savez(vectors_dir / "embeddings.npz",
             ids=np.array(rels, dtype=object), vectors=vecs.astype(np.float32))

    summary_path = csv_dir / cfg.get("summary_csv", "classify_summary.csv")
    with open(summary_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["path", "top_label", "top_score", "embedding_engine", "classification_engine"])
        w.writeheader()
        w.writerows(summary_rows)
    (reports_dir / "RUN_STATUS.json").write_text(json.dumps({
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "export_subdirs": {
            "json": str(json_dir),
            "csv": str(csv_dir),
            "reports": str(reports_dir),
            "vectors": str(vectors_dir),
        },
        "file_count": len(files),
        "embedding_engine": embedding_engine,
        "engine_notes": engine_notes,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("summary -> %s", summary_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
