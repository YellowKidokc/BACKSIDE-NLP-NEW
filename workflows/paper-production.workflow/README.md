# Paper Production Workflow

Small, reusable paper pipeline for Theophysics content with explicit artifact handoff.

## What it runs

By default, this workflow executes in this order:

1. `math-translation-layer`
2. `classify-documents`
3. `plain-language`
4. `claim-extraction`
5. `claim-classification` (fed from `claim-extraction` output)
6. `master-equation-canon`
7. `fruits-spirit-canon`
8. `sbert-embedder`
9. `paper-intelligence-suite`
10. `paper-proof-grader`

Station output artifacts are collected from each station’s `_outbox` and copied into:

`<export-root>/<run_id>/artifacts/`

Each run writes:

- `manifest.json` — full stage-by-stage status and timing
- `paper_output_bundle.json` — compact outputs for downstream publishing
- `run_id` is deterministic per source file + mtime
- `paper_output_bundle.md` — one-file markdown summary with counts + key metrics

Station-level output policy is defined in `station_output_contract.json` so each station knows what to emit:
- narrative outputs: easy/academic/summary-style fields
- statistical/analytic outputs: claim counts, scores, cluster counts, verification flags, etc.
- mixed outputs are allowed for stations that should produce both.

## Run modes

- One file:

```powershell
python .\pipeline.py --input "D:\path\to\paper.md"
```

- Folder batch:

```powershell
python .\pipeline.py --input-root "D:\path\to\papers" --glob "*.html" --max-files 3
```

- Partial stages (for quick smoke checks):

```powershell
python .\pipeline.py --input "D:\path\to\paper.md" --stages plain-language claim-extraction claim-classification
```

## Defaults

- Export root: `\\192.168.2.50\brain\10_EXPORTS\1 Exports TEST`
- State root: `\\192.168.2.50\brain\Backside\_state\paper-production`
- Per-station timeout: 600s (or `STATION_TIMEOUT` env var)

## Failure behavior

- `--fail-fast` stops on first failed station.
- Without `--fail-fast`, later stages can continue for diagnostics.

## Notes

- The runner executes `pipeline.py` directly to avoid batch `pause` hooks.
- Outputs depend on each station’s current `_shared` helper behavior and model/API availability.
- Station-by-station output contract is tracked in:
  - `station_output_contract.json`
  - `station-by-station-audit.md`

## What runs in this workflow (default)

1. `math-translation-layer`
2. `classify-documents`
3. `plain-language`
4. `claim-extraction`
5. `claim-classification`
6. `master-equation-canon`
7. `fruits-spirit-canon`
8. `sbert-embedder`
9. `paper-intelligence-suite`
10. `paper-proof-grader`

## Excluded from this workflow

- `obsidian-export`
- YouTube family: `youtube-fetch`, `youtube-scrape`, `youtube-qa`
- `whisper-transcribe`, `whisper-qa`
