"""
transcribe-and-classify workflow.

For every media file under input_dir:
  1. Whisper transcribe (large-v3 by default; uses 01_WHISPER\\config.json)
  2. SBERT embed the transcript text
  3. DeBERTa classify the transcript against the apologetics labels
  4. Write a JSON sidecar with {transcript, embedding_dim, classification}
  5. Append to a CSV summary
"""
from __future__ import annotations

import csv
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATIONS_ROOT = HERE.parent
BACKSIDE_ROOT = STATIONS_ROOT.parent
LOG_DIR = BACKSIDE_ROOT / "_LOGS"

TOOL_STATIONS = {
    "whisper": STATIONS_ROOT / "whisper-transcribe.station",
    "sbert": STATIONS_ROOT / "sbert-embedder.station",
    "deberta": STATIONS_ROOT / "deberta-runner.station",
}

for p in TOOL_STATIONS.values():
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
    log = _setup_logging(cfg.get("name", "transcribe-and-classify"))

    input_dir = Path(cfg["input_dir"]) if cfg.get("input_dir") else None
    output_dir = Path(cfg["output_dir"]) if cfg.get("output_dir") else None
    if not input_dir or not output_dir:
        log.error("config.input_dir and config.output_dir must be set")
        return 1
    if not input_dir.exists():
        log.error("input_dir not found: %s", input_dir)
        return 1
    output_dir.mkdir(parents=True, exist_ok=True)

    exts = {e.lower() for e in cfg.get("audio_extensions", [".mp3", ".wav", ".m4a"])}
    files = [p for p in sorted(input_dir.rglob("*")) if p.is_file() and p.suffix.lower() in exts]
    log.info("found %d media files in %s", len(files), input_dir)
    if not files:
        return 0

    import whisper_runner
    import sbert_runner
    import deberta_runner

    w_cfg = json.loads((TOOL_STATIONS["whisper"] / "config.json").read_text(encoding="utf-8"))
    sb_cfg = json.loads((TOOL_STATIONS["sbert"] / "config.json").read_text(encoding="utf-8"))
    db_cfg = json.loads((TOOL_STATIONS["deberta"] / "config.json").read_text(encoding="utf-8"))
    labels = db_cfg["labels"]

    cache = w_cfg.get("model_cache_dir")
    if cache:
        os.environ.setdefault("HF_HOME", cache)
    ms = w_cfg.get("model_settings", {})
    log.info("loading Whisper %s", ms.get("model_size", "large-v3"))
    tx = whisper_runner.WhisperTranscriber(
        model_size=ms.get("model_size", "large-v3"),
        device=ms.get("device", "auto"),
        compute_type=ms.get("compute_type", "auto"),
        cache_dir=cache,
    )
    log.info("Whisper ready device=%s compute=%s", tx.device, tx.compute_type)

    em = sbert_runner.Embedder(
        model_name=sb_cfg["model_settings"].get("model_name", "all-MiniLM-L6-v2"),
        device=sb_cfg["model_settings"].get("device", "auto"),
        cache_dir=sb_cfg.get("model_cache_dir"),
        max_seq_length=sb_cfg["model_settings"].get("max_seq_length"),
    )
    clf = deberta_runner.Classifier(
        model_name=db_cfg["model_settings"].get("model_name"),
        device=db_cfg["model_settings"].get("device", "auto"),
        cache_dir=db_cfg.get("model_cache_dir"),
        hypothesis_template=db_cfg["model_settings"].get("hypothesis_template", "This text is about {}."),
    )

    summary_path = output_dir / cfg.get("summary_csv", "transcribe_summary.csv")
    new_csv = not summary_path.exists()
    with open(summary_path, "a", newline="", encoding="utf-8") as csv_f:
        w = csv.DictWriter(csv_f, fieldnames=["path", "duration", "language", "top_label", "top_score"])
        if new_csv:
            w.writeheader()

        for i, f in enumerate(files, 1):
            log.info("[%d/%d] %s", i, len(files), f.name)
            try:
                tr = tx.transcribe(
                    f,
                    language=ms.get("language"),
                    beam_size=ms.get("beam_size", 5),
                    vad_filter=ms.get("vad_filter", True),
                    word_timestamps=ms.get("word_timestamps", False),
                )
            except Exception as e:
                log.exception("transcribe failed: %s", e)
                continue

            text = tr["text"]
            sidecar: dict = {
                "path": str(f.relative_to(input_dir)),
                "duration": tr["duration"],
                "language": tr["language"],
                "transcript": text,
                "segments": tr["segments"],
            }
            try:
                vecs = em.embed([text])
                sidecar["embedding_dim"] = int(vecs.shape[1])
            except Exception as e:
                log.exception("embed failed: %s", e)
                sidecar["embed_error"] = str(e)

            top_label, top_score = "", 0.0
            try:
                max_chars = int(db_cfg["model_settings"].get("max_text_chars", 2000))
                res = clf.classify(text[:max_chars] if max_chars > 0 else text, labels)
                sidecar["classification"] = res
                top_label, top_score = res["label"], res["score"]
            except Exception as e:
                log.exception("classify failed: %s", e)
                sidecar["classify_error"] = str(e)

            rel = f.relative_to(input_dir)
            out_json = output_dir / rel.with_suffix(".json")
            out_txt = output_dir / rel.with_suffix(".txt")
            out_json.parent.mkdir(parents=True, exist_ok=True)
            out_json.write_text(json.dumps(sidecar, ensure_ascii=False, indent=2), encoding="utf-8")
            out_txt.write_text(text, encoding="utf-8")
            w.writerow({
                "path": str(rel),
                "duration": round(tr["duration"], 1),
                "language": tr["language"],
                "top_label": top_label,
                "top_score": round(top_score, 4),
            })
            csv_f.flush()

    log.info("summary -> %s", summary_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
