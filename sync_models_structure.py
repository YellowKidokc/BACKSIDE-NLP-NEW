"""
sync_models_structure.py
Copy model folder structure + configs to D: WITHOUT the heavy weight files.
Weights stay on NAS. Codex gets configs, tokenizers, READMEs, manifests.

Usage: python sync_models_structure.py
"""
import shutil, os
from pathlib import Path

SRC = Path(r"\\192.168.2.50\brain\05_MODELS")
DST = Path(r"D:\GitHub\BACKSIDE-NLP-NEW\models")

# Skip these extensions (the heavy files)
SKIP_EXT = {
    ".safetensors", ".bin", ".pt", ".pth",
    ".h5", ".onnx", ".msgpack", ".ot",
    ".tar", ".gz", ".zip",
    ".npy", ".npz",
}

# Skip these folders entirely
SKIP_DIRS = {
    ".git", "__pycache__", ".cache", "node_modules",
    ".venv", ".venv_science_nlp", "onnx",
}

# Max single file size to copy (5 MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

copied = 0
skipped = 0
dirs_created = 0

for root, dirs, files in os.walk(str(SRC)):
    # Filter out skip dirs
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    
    rel = Path(root).relative_to(SRC)
    dst_dir = DST / rel
    
    if not dst_dir.exists():
        dst_dir.mkdir(parents=True, exist_ok=True)
        dirs_created += 1
    
    for f in files:
        src_file = Path(root) / f
        dst_file = dst_dir / f
        ext = src_file.suffix.lower()
        
        # Skip heavy weight files
        if ext in SKIP_EXT:
            skipped += 1
            continue
        
        # Skip files over 5MB (catches any weight files we missed)
        try:
            size = src_file.stat().st_size
        except OSError:
            skipped += 1
            continue
            
        if size > MAX_FILE_SIZE:
            # But write a placeholder so Codex knows it exists
            placeholder = dst_dir / f"{f}.WEIGHT_ON_NAS"
            if not placeholder.exists():
                placeholder.write_text(
                    f"# Weight file: {f}\n"
                    f"# Size: {size / 1e6:.1f} MB\n"
                    f"# Location: {src_file}\n"
                    f"# This file lives on NAS, not synced to D:\n"
                )
            skipped += 1
            continue
        
        # Copy the file
        try:
            shutil.copy2(str(src_file), str(dst_file))
            copied += 1
        except Exception as e:
            print(f"  SKIP {rel / f}: {e}")
            skipped += 1

print(f"\nDone!")
print(f"  Dirs created: {dirs_created}")
print(f"  Files copied: {copied}")
print(f"  Files skipped: {skipped} (weights stay on NAS)")
print(f"  Source: {SRC}")
print(f"  Dest:   {DST}")
