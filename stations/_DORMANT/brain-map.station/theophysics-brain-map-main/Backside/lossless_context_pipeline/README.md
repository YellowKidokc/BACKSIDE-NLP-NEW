# Lossless Context Pipeline

Python controller for the Lossless Context Compression + Semantic Addressing Protocol.

## What It Produces

Given a Markdown file, the pipeline emits:

- a Nabla-style permanent address: `D/N/V/A/U/R :: VECTOR :: HASH`
- a deterministic Master Equation UUID for the paper snapshot
- semantic tag packets for claims, evidence, equations, kill conditions, relationships, and domain boundaries
- stable document, block, claim, equation, evidence, run, audit, and repair IDs
- claim archaeology, evidence chains, kill conditions, equation semantics, domain boundaries
- mechanism graph edges, reviewer seeds, score ledger, four-score dashboard, eight gaps
- JSON artifact, HTML snapshot, `.semantic-tags.md`, and `.semantic-tags.json`

The grade is audit metadata only. The permanent semantic identifier is the address. The Master Equation UUID is the deterministic database key for that address/content snapshot.

## Run

```powershell
cd D:\GitHub\theophysics-brain-map
python -m Backside.lossless_context_pipeline.cli run `
  --input Backside/lossless_context_pipeline/samples/sample_article.md `
  --out EXPORTS/lossless-context/sample `
  --vault-id theophysics-brain `
  --embeddings none
```

Use `--embeddings sbert` to add local sentence-transformer vectors when the local model is available.

## Batch

```powershell
python -m Backside.lossless_context_pipeline.cli batch `
  --input-root X:\Backside\corpus\C4C `
  --out EXPORTS/lossless-context/c4c `
  --vault-id theophysics-brain `
  --glob *.md `
  --embeddings none
```

## Store In Postgres

The DDL lives at `docs/postgres_schema.sql`. The CLI has a `--postgres-dsn` option, but storage is intentionally append-only: every run creates a new audit snapshot keyed by `run_id` and `content_hash`.

## Current Boundary

The deterministic pipeline extracts what rules can safely extract. Fields that need an LLM are marked `EXPAND_REQUIRED` or filled with conservative repair prompts:

- buried claim
- operational claim
- evidence bridge
- implicit kill
- hostile reviewer attack
- repair recommendation
