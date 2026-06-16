# MDA Citation Spine Station

Copied OpenAI/NLP runner for building MDA proof packets without touching source articles.

## What It Borrows

The station copies the old OpenAI workflow shape from:

`Z:\_Theophysics_v3\00_SYSTEM\01_ENGINE\81_OPENAI_BLANK`

It does not move or depend on that folder at runtime. The copied runner lives in:

`X:\Backside\stations\mda-citation-spine.station\openai_runner`

## What It Runs

- `7q_judge`: claim decomposition and kill conditions.
- `academic`: citation, evidence, math, and logic review.
- `extractor`: missing citations, axiom mapping, theory resonance, and structural completion.

## Safe Defaults

- Writes to `EXPORTS\runs\run_*`.
- Passes an explicit `--output` folder to the copied runner.
- Forces `OPENAI_RUNNER_ANNOTATE_SOURCE=0`.
- Does not copy a live `config.txt` or API key.
- Uses the `OPENAI_API_KEY` environment variable when real calls are made.

## Commands

Claim inventory first:

```powershell
python X:\Backside\stations\mda-citation-spine.station\claim_inventory.py
```

This writes:

- `all_claim_candidates.csv` - every deterministic claim-audit row.
- `7q_queue.csv` - core paper claims only.
- `proof_layer_claims.seed.json` - website-facing claim seed with article, paragraph, sentence, and proof anchor fields.
- `citation_fact_queue.csv` - factual/support rows that need citation checks but should not consume 7Q.
- `review_queue.csv` - ambiguous or composite rows for human triage.
- `parked_or_excluded.csv` - author voice, shell text, narrative examples, and metadata.

Dry run one article:

```powershell
python X:\Backside\stations\mda-citation-spine.station\pipeline.py --article MDA-043-amish-proof-THE-PROOF.md --dry-run
```

Run one article:

```powershell
python X:\Backside\stations\mda-citation-spine.station\pipeline.py --article MDA-043-amish-proof-THE-PROOF.md
```

Run first N articles:

```powershell
python X:\Backside\stations\mda-citation-spine.station\pipeline.py --limit 3
```

Run all MDA articles:

```powershell
python X:\Backside\stations\mda-citation-spine.station\pipeline.py --all
```

## Output Shape

Each article gets:

- `raw_openai\..._7Q_JUDGE.json`
- `raw_openai\..._ACADEMIC.json`
- `raw_openai\..._extractor.md` or JSON when parseable
- `packets\{article}\claims.json`
- `packets\{article}\citation-status.csv`
- `packets\{article}\falsification.json`
- `RUN_REPORT.md`
- `run_manifest.json`

These are review packets, not canonical website files.
