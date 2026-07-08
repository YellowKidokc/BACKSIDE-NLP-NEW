"""
06_IMAGES — OCR (EasyOCR) + zero-shot tagging (CLIP) over a directory.

For each image under config.input_dir, writes a JSON sidecar to
config.output_dir containing:

  {
    "path": "...",
    "ocr": {"text": "...", "spans": [{"text": "...", "conf": 0.92, "bbox": [...]}, ...]},
    "tags": [{"label": "...", "score": 0.84}, ...]
  }

Either action can be disabled via config.actions.

Self-test: --self-test  generates a 256x96 PNG with the word "HELLO" and
           verifies OCR returns "HELLO" (case-insensitive substring match).
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _resolve_log_dir(cfg: dict | None = None) -> Path:
    """Logs go to config.log_dir (the central D:\\brain\\_LOGS sink) when set,
    else a station-local _LOGS folder. Previously this was ROOT/_LOGS, which
    both ignored config.log_dir AND scattered logs into the shared stations
    parent directory."""
    if cfg and cfg.get("log_dir"):
        return Path(cfg["log_dir"])
    return HERE / "_LOGS"


def _setup_logging(cfg: dict | None = None) -> logging.Logger:
    log_dir = _resolve_log_dir(cfg)
    log_dir.mkdir(parents=True, exist_ok=True)
    logfile = log_dir / f"images_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger("images")
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


def _resolve_device(device: str) -> str:
    if device != "auto":
        return device
    try:
        import torch  # type: ignore

        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


class OCREngine:
    def __init__(self, languages: list[str], gpu: bool = False, model_storage: str | None = None):
        import easyocr  # type: ignore

        kwargs = {"gpu": bool(gpu)}
        if model_storage:
            kwargs["model_storage_directory"] = model_storage
        self.reader = easyocr.Reader(languages, **kwargs)

    def read(self, image_path: str | Path, min_conf: float = 0.3) -> dict:
        result = self.reader.readtext(str(image_path))
        spans = []
        texts = []
        for box, text, conf in result:
            if conf < min_conf:
                continue
            spans.append({"text": text, "conf": float(conf), "bbox": [[float(x) for x in pt] for pt in box]})
            texts.append(text)
        return {"text": " ".join(texts), "spans": spans}


class CLIPClassifier:
    def __init__(
        self,
        model_name: str = "openai/clip-vit-base-patch32",
        device: str = "auto",
        cache_dir: str | None = None,
        prompt_template: str = "a photo of {}",
    ):
        from transformers import CLIPModel, CLIPProcessor  # type: ignore

        if cache_dir:
            os.environ.setdefault("HF_HOME", cache_dir)
            os.environ.setdefault("TRANSFORMERS_CACHE", cache_dir)
        self.device = _resolve_device(device)
        self.model = CLIPModel.from_pretrained(model_name).to(self.device).eval()
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.prompt_template = prompt_template
        self._cached_labels: list[str] | None = None
        self._cached_text_features = None

    def _encode_labels(self, labels: list[str]):
        import torch  # type: ignore

        prompts = [self.prompt_template.format(l) for l in labels]
        inputs = self.processor(text=prompts, return_tensors="pt", padding=True).to(self.device)
        with torch.no_grad():
            feats = self.model.get_text_features(**inputs)
        feats = feats / feats.norm(dim=-1, keepdim=True)
        self._cached_labels = list(labels)
        self._cached_text_features = feats
        return feats

    def classify(self, image_path: str | Path, labels: list[str], top_k: int = 3) -> list[dict]:
        import torch  # type: ignore
        from PIL import Image  # type: ignore

        if self._cached_labels != list(labels):
            self._encode_labels(labels)
        text_feats = self._cached_text_features

        img = Image.open(str(image_path)).convert("RGB")
        inputs = self.processor(images=img, return_tensors="pt").to(self.device)
        with torch.no_grad():
            img_feats = self.model.get_image_features(**inputs)
        img_feats = img_feats / img_feats.norm(dim=-1, keepdim=True)
        sims = (img_feats @ text_feats.T).squeeze(0)
        probs = sims.softmax(dim=-1)

        top_k = min(top_k, len(labels))
        topk = probs.topk(top_k)
        return [
            {"label": labels[int(idx)], "score": float(score)}
            for idx, score in zip(topk.indices.tolist(), topk.values.tolist())
        ]


def _self_test(log: logging.Logger) -> int:
    cfg = _load_config()
    try:
        from PIL import Image, ImageDraw, ImageFont  # type: ignore
    except Exception as e:
        log.error("PIL import failed: %s", e)
        return 2
    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "hello.png"
        img = Image.new("RGB", (256, 96), color="white")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 56)
        except Exception:
            font = ImageFont.load_default()
        draw.text((20, 20), "HELLO", fill="black", font=font)
        img.save(png)
        try:
            ocr = OCREngine(
                languages=cfg.get("ocr_settings", {}).get("languages", ["en"]),
                gpu=cfg.get("ocr_settings", {}).get("gpu", False),
                model_storage=cfg.get("model_cache_dir"),
            )
        except Exception as e:
            log.error("OCR init failed: %s", e)
            return 3
        try:
            res = ocr.read(png, min_conf=0.0)
        except Exception as e:
            log.exception("OCR read failed: %s", e)
            return 4
    text = (res.get("text") or "").upper()
    log.info("self-test text=%r", text)
    if "HELLO" in text:
        log.info("self-test OK")
        return 0
    log.error("self-test FAILED: 'HELLO' not found in OCR output")
    return 5


def _iter_images(input_dir: Path, exts: list[str]):
    exts_lower = {e.lower() for e in exts}
    for p in sorted(input_dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in exts_lower:
            yield p


def run(config: dict | None = None) -> int:
    cfg = config or _load_config()
    log = _setup_logging(cfg)
    input_dir = Path(cfg["input_dir"]) if cfg.get("input_dir") else None
    # Exports default to the station-root EXPORTS folder. config.output_dir
    # may override it (e.g. to feed a downstream pipeline location).
    output_dir = Path(cfg["output_dir"]) if cfg.get("output_dir") else (HERE / "EXPORTS")
    if not input_dir:
        log.error("config.input_dir must be set")
        return 1
    if not input_dir.exists():
        log.error("input_dir does not exist: %s", input_dir)
        return 1
    output_dir.mkdir(parents=True, exist_ok=True)

    actions = cfg.get("actions", {"ocr": True, "classify": True})
    do_ocr = bool(actions.get("ocr", True))
    do_clf = bool(actions.get("classify", True))

    ocr = None
    clf = None
    if do_ocr:
        os_ = cfg.get("ocr_settings", {})
        ocr = OCREngine(
            languages=os_.get("languages", ["en"]),
            gpu=os_.get("gpu", False),
            model_storage=cfg.get("model_cache_dir"),
        )
    if do_clf:
        cs = cfg.get("clip_settings", {})
        clf = CLIPClassifier(
            model_name=cs.get("model_name", "openai/clip-vit-base-patch32"),
            device=cs.get("device", "auto"),
            cache_dir=cfg.get("model_cache_dir"),
            prompt_template=cs.get("prompt_template", "a photo of {}"),
        )

    files = list(_iter_images(input_dir, cfg.get("image_extensions", [".jpg", ".png"])))
    log.info("processing %d images from %s", len(files), input_dir)

    cs = cfg.get("clip_settings", {})
    failed = 0
    for i, f in enumerate(files, 1):
        rec: dict = {"path": str(f.relative_to(input_dir))}
        if do_ocr:
            try:
                rec["ocr"] = ocr.read(f, min_conf=cfg.get("ocr_settings", {}).get("min_confidence", 0.3))
            except Exception as e:
                log.exception("OCR failed for %s: %s", f, e)
                rec["ocr_error"] = str(e)
                failed += 1
        if do_clf:
            try:
                rec["tags"] = clf.classify(f, cs.get("labels", []), top_k=cs.get("top_k", 3))
            except Exception as e:
                log.exception("classify failed for %s: %s", f, e)
                rec["classify_error"] = str(e)
                failed += 1
        out = output_dir / f.relative_to(input_dir).with_suffix(".json")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        if i % 25 == 0 or i == len(files):
            log.info("[%d/%d] -> %s", i, len(files), out.name)

    log.info("done. failed=%d", failed)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Image OCR + zero-shot tagging")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    cfg = _load_config()
    log = _setup_logging(cfg)
    if args.self_test:
        return _self_test(log)
    return run(cfg)


if __name__ == "__main__":
    sys.exit(main())
