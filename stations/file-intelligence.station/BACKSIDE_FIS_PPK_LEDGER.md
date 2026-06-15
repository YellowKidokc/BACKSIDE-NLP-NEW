# File Intelligence PPK Integration Ledger

## Decision

Use `17_portable_preference_kernel` as the preference and routing spine for `file-intelligence.station`.

`13_preference_implicit`, `18_river_streaming`, and `19_markovify_text` are support engines. They are not the first FIS integration point because their folders currently expose metadata/readme surfaces, while `17_portable_preference_kernel` contains the actual `fis_addons` bridge package.

## Boundary

- Model folders remain read-only for this wiring pass.
- FIS writes generated manifests under `_ppk_runtime/manifests/`, not beside watched source files.
- FIS skips `_ppk_runtime` and `*.fis_manifest.json` during watcher/backfill to avoid recursive ingestion.
- PPK prediction is allowed to fail closed; FIS classification and rename flow should continue.

## Entries

### 2026-06-03

- Captured pre-change snapshot under `_ppk_integration_audit/snapshots/`.
- Added `fis/ppk_manifest.py` adapter.
- Patched `fis/pipeline.py` to attach a PPK manifest to duplicate, no-text kickout, and normal classification results.
- Patched watcher/backfill generated-artifact skips.
- Patched `RUN.bat` to force UTF-8 console/Python mode.
- Verified syntax with `py_compile` for `fis/ppk_manifest.py`, `fis/pipeline.py`, `fis/watcher.py`, and `fis/backfill.py`.
- Verified direct bridge smoke test against `README.md`.
- Smoke manifest written: `_ppk_runtime/manifests/art-f8968678910b6e34.fis_manifest.json`.
- Smoke manifest result: 11 routes, 8 PPK recommendations, no raw text stored, safe-to-sync true.
- Corrected post-change snapshot: `_ppk_integration_audit/snapshots/20260603T043042Z_fis_postchange_snapshot.json`.
- Ignore `_ppk_integration_audit/snapshots/20260603T043025Z_fis_postchange_snapshot.json`; that snapshot command had a malformed PowerShell inline `if` expression.
