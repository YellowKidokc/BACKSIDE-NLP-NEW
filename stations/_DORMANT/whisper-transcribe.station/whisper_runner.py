"""
01_WHISPER — speech-to-text via faster-whisper.

CLI mode:    walks config['input_dir'] for media files, transcribes each, writes
             <name>.txt and <name>.json (segments) to config['output_dir'].
Library mode: import WhisperTranscriber and call .transcribe(path) -> dict.

Self-test:   --self-test  (synthesizes a 1s sine WAV with the stdlib `wave`
             module, runs the tiny model on it, asserts no exception).
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import os
import struct
import sys
import tempfile
import wave
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOG_DIR = ROOT / "_LOGS"


def _setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    logfile = LOG_DIR / f"whisper_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger("whisper")
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


def _resolve_device(device: str) -> tuple[str, str]:
    """Return (device, compute_type) from 'auto' or explicit values."""
    if device != "auto":
        return device, "default"
    try:
        import torch  # type: ignore

        if torch.cuda.is_available():
            return "cuda", "float16"
    except Exception:
        pass
    return "cpu", "int8"


class WhisperTranscriber:
    """Thin wrapper over faster_whisper.WhisperModel with config defaults."""

    def __init__(
        self,
        model_size: str = "large-v3",
        device: str = "auto",
        compute_type: str = "auto",
        cache_dir: str | None = None,
    ):
        from faster_whisper import WhisperModel

        device_resolved, compute_resolved = _resolve_device(device)
        if compute_type != "auto":
            compute_resolved = compute_type
        self.device = device_resolved
        self.compute_type = compute_resolved
        self.model_size = model_size
        self.model = WhisperModel(
            model_size,
            device=device_resolved,
            compute_type=compute_resolved,
            download_root=cache_dir,
        )

    def transcribe(
        self,
        audio_path: str | Path,
        language: str | None = None,
        beam_size: int = 5,
        vad_filter: bool = True,
        word_timestamps: bool = False,
    ) -> dict:
        segments_iter, info = self.model.transcribe(
            str(audio_path),
            language=language,
            beam_size=beam_size,
            vad_filter=vad_filter,
            word_timestamps=word_timestamps,
        )
        segments = []
        for seg in segments_iter:
            segments.append(
                {
                    "id": seg.id,
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text.strip(),
                }
            )
        text = " ".join(s["text"] for s in segments).strip()
        return {
            "text": text,
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "segments": segments,
        }


def _iter_media(input_dir: Path, exts: list[str]):
    exts_lower = {e.lower() for e in exts}
    for p in sorted(input_dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in exts_lower:
            yield p


def _self_test(log: logging.Logger) -> int:
    log.info("self-test: synthesizing 1s sine WAV at 16kHz")
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "tone.wav"
        sr = 16000
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sr)
            for i in range(sr):
                sample = int(0.2 * 32767 * math.sin(2 * math.pi * 440 * i / sr))
                w.writeframes(struct.pack("<h", sample))
        log.info("loading tiny model (downloads on first run)")
        cfg = _load_config()
        cache = cfg.get("model_cache_dir") or None
        try:
            tx = WhisperTranscriber(
                model_size="tiny",
                device="auto",
                compute_type="auto",
                cache_dir=cache,
            )
        except Exception as e:
            log.error("model load failed: %s", e)
            return 2
        try:
            out = tx.transcribe(wav, beam_size=1, vad_filter=False)
        except Exception as e:
            log.error("transcribe failed: %s", e)
            return 3
        log.info(
            "self-test OK device=%s compute=%s text=%r duration=%.2fs",
            tx.device,
            tx.compute_type,
            out["text"],
            out["duration"],
        )
        return 0


def run(config: dict | None = None) -> int:
    log = _setup_logging()
    cfg = config or _load_config()

    input_dir = Path(cfg["input_dir"]) if cfg.get("input_dir") else None
    output_dir = Path(cfg["output_dir"]) if cfg.get("output_dir") else None
    if not input_dir or not output_dir:
        log.error("config.input_dir and config.output_dir must be set")
        return 1
    if not input_dir.exists():
        log.error("input_dir does not exist: %s", input_dir)
        return 1
    output_dir.mkdir(parents=True, exist_ok=True)

    ms = cfg.get("model_settings", {})
    cache = cfg.get("model_cache_dir") or None

    log.info("loading whisper model_size=%s", ms.get("model_size", "large-v3"))
    tx = WhisperTranscriber(
        model_size=ms.get("model_size", "large-v3"),
        device=ms.get("device", "auto"),
        compute_type=ms.get("compute_type", "auto"),
        cache_dir=cache,
    )
    log.info("model loaded device=%s compute=%s", tx.device, tx.compute_type)

    files = list(_iter_media(input_dir, cfg.get("audio_extensions", [".wav"])))
    log.info("found %d media files in %s", len(files), input_dir)

    failed = 0
    for i, f in enumerate(files, 1):
        log.info("[%d/%d] %s", i, len(files), f.name)
        try:
            out = tx.transcribe(
                f,
                language=ms.get("language"),
                beam_size=ms.get("beam_size", 5),
                vad_filter=ms.get("vad_filter", True),
                word_timestamps=ms.get("word_timestamps", False),
            )
        except Exception as e:
            log.exception("failed: %s", e)
            failed += 1
            continue
        rel = f.relative_to(input_dir)
        txt_path = output_dir / rel.with_suffix(".txt")
        json_path = output_dir / rel.with_suffix(".json")
        txt_path.parent.mkdir(parents=True, exist_ok=True)
        txt_path.write_text(out["text"], encoding="utf-8")
        json_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        log.info("    -> %s (%.1fs, lang=%s)", txt_path.name, out["duration"], out["language"])

    log.info("done. %d ok, %d failed", len(files) - failed, failed)
    return 0 if failed == 0 else 4


def main() -> int:
    ap = argparse.ArgumentParser(description="Whisper transcription runner")
    ap.add_argument("--self-test", action="store_true", help="quick smoke test")
    ap.add_argument("--input", help="override input_dir")
    ap.add_argument("--output", help="override output_dir")
    args = ap.parse_args()

    log = _setup_logging()
    cfg = _load_config()
    cache = cfg.get("model_cache_dir")
    if cache:
        os.environ.setdefault("HF_HOME", cache)

    if args.self_test:
        return _self_test(log)

    if args.input:
        cfg["input_dir"] = args.input
    if args.output:
        cfg["output_dir"] = args.output
    return run(cfg)


if __name__ == "__main__":
    sys.exit(main())
