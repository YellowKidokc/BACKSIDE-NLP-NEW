"""
download_nlp_models.py
Download all 18 capability-folder NLP models from HuggingFace.
POF 2828 | 2026-06-17

Usage: python download_nlp_models.py
Models download to \\192.168.2.50\brain\05_MODELS\{folder}\
Resumable — safe to re-run if interrupted.
"""
import json, os, sys, time
from pathlib import Path
from datetime import datetime

MODELS_ROOT = Path(r"\\192.168.2.50\brain\05_MODELS")

# Each entry: (folder_name, hf_model_id, notes, priority)
# Priority: 1=critical, 2=important, 3=nice-to-have
DOWNLOADS = [
    # --- CONTRADICTION / NLI ---
    ("01_CONTRADICTION_PRIMARY",
     "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli",
     "Primary NLI: contradiction/entailment/neutral", 1),

    ("02_CONTRADICTION_FAST",
     "cross-encoder/nli-MiniLM2-L6-H768",
     "Fast NLI screening, low latency", 1),

    ("14_CONTRADICTION_TINY",
     "typeform/distilbert-base-uncased-mnli",
     "Tiny NLI for quick prefilter", 2),

    # --- EMBEDDINGS ---
    ("03_EMBEDDINGS_FAST",
     "sentence-transformers/all-MiniLM-L6-v2",
     "Fast semantic search/clustering (already have as sbert_minilm)", 2),

    # --- SCIENTIFIC CLAIM VERIFY ---
    # SciFact needs multiple components; download the NLI verifier
    ("05_SCIENTIFIC_CLAIM_VERIFY",
     "cross-encoder/nli-deberta-v3-base",
     "SciFact-style NLI verifier component", 1),

    # --- NER ---
    ("06_NER_GENERAL",
     "dslim/bert-base-NER",
     "General NER: PER/ORG/LOC/MISC", 1),

    ("16_NER_ENHANCED",
     "urchade/gliner_multi-v2.1",
     "Open-type entity extraction (zero-shot NER)", 2),

    # --- ZERO-SHOT CLASSIFIER ---
    ("07_ZERO_SHOT_CLASSIFIER",
     "MoritzLaurer/deberta-v3-large-zeroshot-v2.0",
     "NLI-based zero-shot classification", 1),

    # --- SUMMARIZER ---
    # Already have bart-large-cnn in M01, but download to new folder too
    ("08_SUMMARIZER",
     "facebook/bart-large-cnn",
     "General/news summarization (also in M01_summarizer)", 2),

    # --- RERANKER ---
    ("09_RERANKER",
     "BAAI/bge-reranker-v2-m3",
     "Post-embedding reranking", 1),

    # --- SENTIMENT ---
    ("10_SENTIMENT",
     "cardiffnlp/twitter-roberta-base-sentiment-latest",
     "Positive/neutral/negative sentiment", 2),

    # --- IMAGE CAPTION ---
    ("13_IMAGE_CAPTION",
     "Salesforce/blip-image-captioning-large",
     "Vision-language captioning", 3),

    # --- LONG NLI ---
    ("15_CONTRADICTION_ENSEMBLE_LONG",
     "tasksource/deberta-base-long-nli",
     "Long-context NLI for ensemble", 2),

    # --- QA EXTRACTOR ---
    ("18_QA_EXTRACTOR",
     "deepset/roberta-base-squad2",
     "Extractive QA (SQuAD2)", 1),
]


def download_model(folder, model_id, notes, priority):
    """Download a single model. Returns (success, message)."""
    dest = MODELS_ROOT / folder
    dest.mkdir(parents=True, exist_ok=True)
    
    # Write model info
    info = {
        "model_id": model_id,
        "folder": folder,
        "notes": notes,
        "priority": priority,
        "downloaded_at": datetime.now().isoformat(timespec="seconds"),
        "source": f"https://huggingface.co/{model_id}",
    }
    
    # Check if already downloaded (has model weights)
    weight_files = list(dest.glob("*.safetensors")) + list(dest.glob("*.bin")) + list(dest.glob("pytorch_model*"))
    if weight_files:
        print(f"  SKIP (already has weights): {folder}")
        return True, "already downloaded"
    
    try:
        from huggingface_hub import snapshot_download
        print(f"  Downloading {model_id} -> {folder}...")
        
        # Download, ignoring large unnecessary formats
        snapshot_download(
            repo_id=model_id,
            local_dir=str(dest),
            ignore_patterns=[
                "*.h5", "*.ot", "*.msgpack",  # skip TF/Flax/Rust
                "flax_model*", "tf_model*", "rust_model*",
                "*.onnx",  # skip ONNX unless needed
            ],
        )
        
        # Write manifest
        (dest / "_MODEL_INFO.json").write_text(
            json.dumps(info, indent=2) + "\n", encoding="utf-8"
        )
        
        return True, "downloaded"
    except Exception as e:
        return False, str(e)


def main():
    print("=" * 60)
    print("NLP Model Downloader")
    print(f"Target: {MODELS_ROOT}")
    print(f"Models: {len(DOWNLOADS)}")
    print("=" * 60)
    print()
    
    # Sort by priority
    sorted_downloads = sorted(DOWNLOADS, key=lambda x: x[3])
    
    results = []
    for folder, model_id, notes, priority in sorted_downloads:
        print(f"[P{priority}] {folder}")
        start = time.time()
        ok, msg = download_model(folder, model_id, notes, priority)
        elapsed = time.time() - start
        status = "OK" if ok else "FAIL"
        results.append((folder, model_id, status, msg, f"{elapsed:.1f}s"))
        print(f"  {status}: {msg} ({elapsed:.1f}s)")
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    ok_count = sum(1 for r in results if r[2] == "OK")
    fail_count = sum(1 for r in results if r[2] == "FAIL")
    print(f"  Downloaded: {ok_count}")
    print(f"  Failed: {fail_count}")
    print()
    
    for folder, model_id, status, msg, elapsed in results:
        flag = "[OK]  " if status == "OK" else "[FAIL]"
        print(f"  {flag} {folder}: {msg} ({elapsed})")
    
    # Write manifest
    manifest = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "models_root": str(MODELS_ROOT),
        "results": [
            {"folder": r[0], "model_id": r[1], "status": r[2], "message": r[3]}
            for r in results
        ]
    }
    manifest_path = MODELS_ROOT / "DOWNLOAD_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"\nManifest: {manifest_path}")
    print("\nDONE")


if __name__ == "__main__":
    main()
