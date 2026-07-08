"""
CLIP + OCR Speed Test
Takes a screenshot, classifies it, reports timing.
Uses the local cached model at the NAS path.
"""
import time
import sys
import os
import json
import tempfile
from pathlib import Path

# Point to local model cache
MODEL_CACHE = r"\\dlowenas\brain\Backside\_models\_Models\M04_imager"
HF_FALLBACK = "openai/clip-vit-base-patch32"

# Labels tuned for screen activity classification
SCREEN_LABELS = [
    "a news website",
    "a code editor or IDE",
    "a social media feed",
    "an email inbox",
    "a research paper or article",
    "a chat or messaging app",
    "a video player",
    "a file explorer or directory listing",
    "a spreadsheet or data table",
    "a search engine results page",
    "a settings or configuration panel",
    "a terminal or command prompt",
    "a document editor",
    "a photo or image viewer",
    "an online store or shopping page",
]

def take_screenshot():
    """Grab primary monitor, return PIL Image."""
    import mss
    from PIL import Image
    import numpy as np
    with mss.mss() as sct:
        mon = sct.monitors[1]
        raw = sct.grab(mon)
        arr = np.array(raw)[:, :, [2, 1, 0]]  # BGRA -> RGB
        return Image.fromarray(arr)

def test_clip(img_path: str):
    """Load CLIP, classify, return results + timing."""
    from transformers import CLIPModel, CLIPProcessor
    import torch

    print(f"\n[1] Loading CLIP model...")
    t0 = time.perf_counter()

    # Try local path first, fall back to HF
    model_path = MODEL_CACHE if os.path.isdir(MODEL_CACHE) else HF_FALLBACK
    print(f"    Source: {model_path}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"    Device: {device}")

    model = CLIPModel.from_pretrained(model_path).to(device).eval()
    processor = CLIPProcessor.from_pretrained(model_path)
    load_time = time.perf_counter() - t0
    print(f"    Model loaded in {load_time:.2f}s")

    print(f"\n[2] Classifying screenshot against {len(SCREEN_LABELS)} labels...")
    from PIL import Image
    img = Image.open(img_path).convert("RGB")

    t1 = time.perf_counter()
    prompts = [f"a screenshot of {l}" for l in SCREEN_LABELS]
    text_inputs = processor(text=prompts, return_tensors="pt", padding=True).to(device)
    img_inputs = processor(images=img, return_tensors="pt").to(device)

    with torch.no_grad():
        text_feats = model.get_text_features(**text_inputs)
        img_feats = model.get_image_features(**img_inputs)

    text_feats = text_feats / text_feats.norm(dim=-1, keepdim=True)
    img_feats = img_feats / img_feats.norm(dim=-1, keepdim=True)

    sims = (img_feats @ text_feats.T).squeeze(0)
    probs = sims.softmax(dim=-1)
    classify_time = time.perf_counter() - t1

    # Sort by score
    scored = sorted(
        [(SCREEN_LABELS[i], float(probs[i])) for i in range(len(SCREEN_LABELS))],
        key=lambda x: -x[1]
    )

    print(f"    Classification done in {classify_time*1000:.0f}ms")

    return scored, load_time, classify_time


def test_ocr(img_path: str):
    """Run EasyOCR, return text + timing."""
    import easyocr
    print(f"\n[3] Running OCR (EasyOCR)...")
    t0 = time.perf_counter()
    reader = easyocr.Reader(["en"], gpu=False)
    ocr_load = time.perf_counter() - t0
    print(f"    OCR engine loaded in {ocr_load:.2f}s")

    t1 = time.perf_counter()
    result = reader.readtext(img_path)
    ocr_time = time.perf_counter() - t1

    texts = [text for _, text, conf in result if conf > 0.3]
    full_text = " ".join(texts)
    print(f"    OCR done in {ocr_time*1000:.0f}ms  ({len(texts)} text spans)")
    return full_text, ocr_load, ocr_time


def main():
    print("=" * 60)
    print("  CLIP + OCR SPEED TEST — Screen Activity Classifier")
    print("=" * 60)

    # Take screenshot
    print("\n[0] Taking screenshot...")
    t0 = time.perf_counter()
    img = take_screenshot()
    ss_time = time.perf_counter() - t0
    print(f"    Screenshot captured in {ss_time*1000:.0f}ms")
    print(f"    Resolution: {img.size[0]}x{img.size[1]}")

    # Save to temp
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(tmp.name)
    tmp.close()
    print(f"    Saved to: {tmp.name}")

    # CLIP classification
    scored, clip_load, clip_infer = test_clip(tmp.name)

    print(f"\n{'='*60}")
    print(f"  TOP CLASSIFICATIONS")
    print(f"{'='*60}")
    for label, score in scored[:5]:
        bar = "█" * int(score * 40)
        print(f"  {score:5.1%}  {bar}  {label}")

    # OCR
    text, ocr_load, ocr_infer = test_ocr(tmp.name)
    print(f"\n  OCR text preview (first 300 chars):")
    print(f"  {text[:300]}...")

    # Summary
    print(f"\n{'='*60}")
    print(f"  TIMING SUMMARY")
    print(f"{'='*60}")
    print(f"  Screenshot capture:    {ss_time*1000:>7.0f}ms")
    print(f"  CLIP model load:       {clip_load:>7.2f}s  (one-time)")
    print(f"  CLIP inference:        {clip_infer*1000:>7.0f}ms  <-- per-frame cost")
    print(f"  OCR model load:        {ocr_load:>7.2f}s  (one-time)")
    print(f"  OCR inference:         {ocr_infer*1000:>7.0f}ms  <-- per-frame cost")
    print(f"  TOTAL per-frame:       {(clip_infer+ocr_infer)*1000:>7.0f}ms")
    print(f"  Theoretical FPS:       {1/(clip_infer+ocr_infer):>7.1f}")
    print(f"{'='*60}")

    # Can we do 5-second intervals?
    budget = 5000  # ms
    per_frame = (clip_infer + ocr_infer) * 1000
    headroom = budget - per_frame
    if headroom > 0:
        print(f"\n  ✓ FITS in 5s interval with {headroom:.0f}ms headroom")
    else:
        print(f"\n  ✗ EXCEEDS 5s interval by {-headroom:.0f}ms")
        print(f"    Consider: GPU, skip OCR on unchanged screens, or longer interval")

    # Cleanup
    os.unlink(tmp.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
