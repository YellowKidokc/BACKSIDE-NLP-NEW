PROCESS_MODEL_DOWNLOADS.bat

What it does:
- Creates/uses X:\05_MODELS by default, or a custom folder passed as argument.
- Creates a local Python venv: .venv_science_nlp
- Installs huggingface_hub + hf_transfer
- Downloads public Hugging Face model snapshots into capability-named folders.
- Writes a manifest to _state\model_manifest.json.
- Writes failures to _state\download_failures.json.

How to run:
1. Put PROCESS_MODEL_DOWNLOADS.bat anywhere.
2. Double-click it, or run from Command Prompt:
      PROCESS_MODEL_DOWNLOADS.bat

Custom destination:
      PROCESS_MODEL_DOWNLOADS.bat D:\05_MODELS

For gated/private models:
      set HF_TOKEN=hf_your_token_here
      PROCESS_MODEL_DOWNLOADS.bat

Notes:
- Some models are large. Make sure X: has room.
- Mistral may require accepting terms on Hugging Face and using HF_TOKEN.
- The script uses snapshot_download, not git clone, so Git LFS is not required.
- If a model fails, rerun the same BAT. Hugging Face download resumes.
