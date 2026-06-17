"""
stage_models.py - Stage the NLP API's models from NAS (storage of record) to local disk (runtime cache).

WHY: safetensors memory-maps the weight file. mmap over an SMB share does thousands of tiny
random reads and stalls indefinitely. Local mmap loads the same 1.5GB model in ~1.5s.
So: NAS holds the canonical models; the FastAPI service loads from the local copy.

SCOPE: only the 14 models main.py actually maps -- NOT the whole 05_MODELS tree (which also
holds large unrelated LLMs like Mistral-7B that this service never loads).

Engine: robocopy /MT (multithreaded), ~500 MB/s. Idempotent: skips files already present & identical.
Skips redundant weight formats (pytorch_model.bin / tf / flax) -- transformers loads safetensors.

Usage:  python stage_models.py
"""
import subprocess, sys
from pathlib import Path

NAS_ROOT   = r"\\192.168.2.50\brain\05_MODELS"
LOCAL_ROOT = r"D:\nlp_models"

# The exact folders main.py references (MODEL_PATHS). Keep in sync with main.py.
MODELS = [
    "M17_01_CONTRADICTION_PRIMARY",
    "M18_02_CONTRADICTION_FAST",
    "M19_03_EMBEDDINGS_FAST",
    "M20_05_SCIENTIFIC_CLAIM_VERIFY",
    "M21_06_NER_GENERAL",
    "M22_07_ZERO_SHOT_CLASSIFIER",
    "M23_08_SUMMARIZER",
    "M24_09_RERANKER",
    "M25_10_SENTIMENT",
    "M27_14_CONTRADICTION_TINY",
    "M28_15_CONTRADICTION_ENSEMBLE_LONG",
    "M29_16_NER_ENHANCED",
    "M30_18_QA_EXTRACTOR",
    "sbert_minilm",
]
SKIP = ["pytorch_model.bin", "tf_model.h5", "model.h5", "flax_model.msgpack"]

def stage():
    Path(LOCAL_ROOT).mkdir(parents=True, exist_ok=True)
    worst = 0
    for name in MODELS:
        src = Path(NAS_ROOT) / name
        dst = Path(LOCAL_ROOT) / name
        if not src.exists():
            print(f"  !! NAS missing: {name}")
            continue
        # Only skip pytorch_model.bin when a safetensors exists -- some models (e.g. the
        # sentiment model) ship bin-only, and excluding it would leave them with no weights.
        skip = list(SKIP)
        if not any(src.glob("*.safetensors")):
            skip = [x for x in skip if x != "pytorch_model.bin"]
        args = ["robocopy", str(src), str(dst), "/E", "/MT:16", "/R:1", "/W:1", "/NP", "/NDL", "/NJH", "/NJS"]
        for x in skip:
            args += ["/XF", x]
        rc = subprocess.call(args)
        worst = max(worst, rc)
        print(f"  {name}: robocopy rc={rc} {'OK' if rc < 8 else 'FAIL'}")
    print(f"\nDONE. worst rc={worst} ({'OK' if worst < 8 else 'FAIL'})")
    sys.exit(0 if worst < 8 else worst)

if __name__ == "__main__":
    stage()
