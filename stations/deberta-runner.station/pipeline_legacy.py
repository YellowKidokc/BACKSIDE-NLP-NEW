"""
03_DEBERTA — zero-shot classification via transformers' zero-shot pipeline.

Two source modes (set in config.json):

  source.type = "postgres":
      Pulls rows from `source.table` where `source.label_col` IS NULL,
      classifies the concatenation of `source.text_cols` against the
      labels in `config.labels`, writes top label + confidence back.
      Batched and resumable; per-row failures are logged and skipped.

  source.type = "files":
      Classifies every text file under `files_source.input_dir`, writing
      a JSON sidecar per file to `files_source.output_dir`.

Library mode: `import deberta_runner; clf = deberta_runner.Classifier(...);
              clf.classify(text, labels) -> {"label": ..., "score": ..., "scores": [...]}`

Self-test:   --self-test  classifies "I love this movie" against
             ["positive review", "negative review"] and asserts positive wins.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOG_DIR = HERE / "_LOGS"
EXPORTS_DIR = HERE / "EXPORTS"
PG_DIR = ROOT / "07_POSTGRES"

if str(PG_DIR) not in sys.path:
    sys.path.insert(0, str(PG_DIR))


def _setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    logfile = LOG_DIR / f"deberta_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger("deberta")
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


def _load_config() -> dict:
    return json.loads((HERE / "config.json").read_text(encoding="utf-8"))


def _station_path(value: str | os.PathLike[str]) -> Path:
    path = Path(value)
    return path if path.is_absolute() else HERE / path


def _resolve_device(device: str) -> int:
    """transformers pipeline expects an int device id (-1 for CPU)."""
    if device == "cpu":
        return -1
    if device == "cuda":
        return 0
    try:
        import torch  # type: ignore

        return 0 if torch.cuda.is_available() else -1
    except Exception:
        return -1


class Classifier:
    """Zero-shot NLI classifier wrapping transformers' pipeline."""

    def __init__(
        self,
        model_name: str = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli",
        device: str = "auto",
        cache_dir: str | None = None,
        hypothesis_template: str = "This text is about {}.",
        multi_label: bool = False,
    ):
        from transformers import pipeline  # type: ignore

        if cache_dir:
            os.environ.setdefault("HF_HOME", cache_dir)
            os.environ.setdefault("TRANSFORMERS_CACHE", cache_dir)
        self.model_name = model_name
        self.hypothesis_template = hypothesis_template
        self.multi_label = multi_label
        device_id = _resolve_device(device)
        self.device = "cuda" if device_id >= 0 else "cpu"
        self.pipe = pipeline(
            "zero-shot-classification",
            model=model_name,
            device=device_id,
        )

    def classify(self, text: str, labels: list[str]) -> dict:
        out = self.pipe(
            text,
            candidate_labels=labels,
            hypothesis_template=self.hypothesis_template,
            multi_label=self.multi_label,
        )
        return {
            "label": out["labels"][0],
            "score": float(out["scores"][0]),
            "scores": [float(s) for s in out["scores"]],
            "labels": list(out["labels"]),
        }

    def classify_batch(self, texts: list[str], labels: list[str], batch_size: int = 8) -> list[dict]:
        results: list[dict] = []
        for i in range(0, len(texts), batch_size):
            chunk = texts[i : i + batch_size]
            outs = self.pipe(
                chunk,
                candidate_labels=labels,
                hypothesis_template=self.hypothesis_template,
                multi_label=self.multi_label,
            )
            if isinstance(outs, dict):
                outs = [outs]
            for o in outs:
                results.append(
                    {
                        "label": o["labels"][0],
                        "score": float(o["scores"][0]),
                        "scores": [float(s) for s in o["scores"]],
                        "labels": list(o["labels"]),
                    }
                )
        return results


def _self_test(log: logging.Logger) -> int:
    cfg = _load_config()
    ms = cfg.get("model_settings", {})
    log.info("self-test: loading %s", ms.get("model_name"))
    try:
        clf = Classifier(
            model_name=ms.get("model_name", "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"),
            device=ms.get("device", "auto"),
            cache_dir=cfg.get("model_cache_dir"),
            hypothesis_template=ms.get("hypothesis_template", "This text is about {}."),
        )
    except Exception as e:
        log.error("model load failed: %s", e)
        return 2
    out = clf.classify(
        "Did Jesus actually rise from the dead, or is the resurrection a myth?",
        ["resurrection of Jesus", "ontological argument", "slavery in the Bible"],
    )
    log.info("device=%s top=%s score=%.3f", clf.device, out["label"], out["score"])
    if out["label"] == "resurrection of Jesus":
        log.info("self-test OK")
        return 0
    log.error("self-test FAILED: top label was %r", out["label"])
    return 3


def _join_text_cols(row: dict, cols: list[str]) -> str:
    parts = []
    for c in cols:
        v = row.get(c)
        if v is None:
            continue
        s = str(v).strip()
        if s:
            parts.append(s)
    return "\n".join(parts)


def _truncate(text: str, max_chars: int) -> str:
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    return text[:max_chars]


def _run_postgres(cfg: dict, log: logging.Logger) -> int:
    from db_utils import Database

    src = cfg["source"]
    table = src["table"]
    id_col = src.get("id_col", "id")
    text_cols = src["text_cols"]
    label_col = src["label_col"]
    conf_col = src["confidence_col"]
    where = src.get("where")

    labels = cfg["labels"]
    if not labels:
        log.error("config.labels is empty — nothing to classify against")
        return 1

    ms = cfg.get("model_settings", {})
    batch_size = int(ms.get("batch_size", 50))
    max_chars = int(ms.get("max_text_chars", 2000))
    pipe_chunk = max(1, min(8, batch_size // 4))

    clf = Classifier(
        model_name=ms.get("model_name", "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"),
        device=ms.get("device", "auto"),
        cache_dir=cfg.get("model_cache_dir"),
        hypothesis_template=ms.get("hypothesis_template", "This text is about {}."),
        multi_label=ms.get("multi_label", False),
    )
    log.info(
        "model loaded: %s on %s. table=%s label_col=%s labels=%d",
        clf.model_name, clf.device, table, label_col, len(labels),
    )

    select_cols = [id_col] + list(text_cols)
    total_done = 0
    total_failed = 0

    with Database(application_name="deberta_runner") as db:
        clause = f"{label_col} IS NULL"
        if where:
            clause = f"({where}) AND {clause}"
        try:
            remaining = db.query(f"SELECT COUNT(*) AS c FROM {table} WHERE {clause}")[0]["c"]
            log.info("rows pending: %d", remaining)
        except Exception as e:
            log.exception("pre-flight count failed: %s", e)
            return 1
        if remaining == 0:
            log.info("nothing to do.")
            return 0

        for batch in db.iter_null_rows(
            table=table,
            id_col=id_col,
            target_col=label_col,
            select_cols=select_cols,
            where=where,
            batch_size=batch_size,
        ):
            ids = [r[id_col] for r in batch]
            texts = [_truncate(_join_text_cols(r, text_cols), max_chars) for r in batch]

            try:
                results = clf.classify_batch(texts, labels, batch_size=pipe_chunk)
            except Exception as e:
                log.exception("batch classify failed: %s — falling back row-by-row", e)
                results = []
                for t in texts:
                    try:
                        results.append(clf.classify(t, labels))
                    except Exception as ee:
                        log.error("row classify failed: %s", ee)
                        results.append(None)

            update_rows: list[tuple] = []
            for idv, res in zip(ids, results):
                if res is None or not res.get("label"):
                    total_failed += 1
                    continue
                update_rows.append((res["label"], float(res["score"]), idv))

            if not update_rows:
                continue
            try:
                db.update_rows_bulk(table, id_col, [label_col, conf_col], update_rows)
            except Exception as e:
                log.exception("bulk update failed: %s — retry per-row", e)
                ok = 0
                for label_v, conf_v, idv in update_rows:
                    try:
                        db.update_row(table, id_col, idv, {label_col: label_v, conf_col: conf_v})
                        ok += 1
                    except Exception as ee:
                        log.error("row update %s failed: %s", idv, ee)
                        total_failed += 1
                total_done += ok
                continue

            total_done += len(update_rows)
            log.info("[+%d] total classified=%d failed=%d", len(update_rows), total_done, total_failed)

    log.info("postgres run complete. classified=%d failed=%d", total_done, total_failed)
    return 0


def _run_files(cfg: dict, log: logging.Logger) -> int:
    fs = cfg.get("files_source", {})
    input_dir = _station_path(fs["input_dir"]) if fs.get("input_dir") else None
    output_dir = _station_path(fs["output_dir"]) if fs.get("output_dir") else EXPORTS_DIR / "json"
    if not input_dir:
        log.error("files mode requires files_source.input_dir")
        return 1
    if not input_dir.exists():
        log.error("input_dir does not exist: %s", input_dir)
        return 1
    output_dir.mkdir(parents=True, exist_ok=True)

    labels = cfg["labels"]
    ms = cfg.get("model_settings", {})
    max_chars = int(ms.get("max_text_chars", 2000))

    clf = Classifier(
        model_name=ms.get("model_name"),
        device=ms.get("device", "auto"),
        cache_dir=cfg.get("model_cache_dir"),
        hypothesis_template=ms.get("hypothesis_template", "This text is about {}."),
        multi_label=ms.get("multi_label", False),
    )
    log.info("model loaded: %s on %s", clf.model_name, clf.device)

    exts = {e.lower() for e in fs.get("text_extensions", [".txt"])}
    files = [p for p in sorted(input_dir.rglob("*")) if p.is_file() and p.suffix.lower() in exts]
    log.info("classifying %d files", len(files))

    failed = 0
    for i, f in enumerate(files, 1):
        try:
            content = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = f.read_text(encoding="latin-1", errors="replace")
        try:
            res = clf.classify(_truncate(content, max_chars), labels)
        except Exception as e:
            log.exception("classify failed: %s", e)
            failed += 1
            continue
        rel = f.relative_to(input_dir)
        out = output_dir / rel.with_suffix(".json")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
        if i % 25 == 0 or i == len(files):
            log.info("[%d/%d] -> %s (top=%s %.3f)", i, len(files), out.name, res["label"], res["score"])
    log.info("done. ok=%d failed=%d", len(files) - failed, failed)
    return 0


def run(config: dict | None = None) -> int:
    log = _setup_logging()
    cfg = config or _load_config()
    src_type = cfg.get("source", {}).get("type", "postgres")
    if src_type == "postgres":
        return _run_postgres(cfg, log)
    if src_type == "files":
        return _run_files(cfg, log)
    log.error("unknown source.type: %s", src_type)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description="DeBERTa zero-shot classification runner")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--source", choices=["postgres", "files"])
    ap.add_argument("--table", help="override source.table")
    args = ap.parse_args()

    log = _setup_logging()
    cfg = _load_config()
    if args.self_test:
        return _self_test(log)
    if args.source:
        cfg["source"]["type"] = args.source
    if args.table:
        cfg["source"]["table"] = args.table
    return run(cfg)


if __name__ == "__main__":
    sys.exit(main())
