# Lossless Context Pipeline Build Spec

## Folder Structure

```text
Backside/lossless_context_pipeline/
  __init__.py
  address.py              # Nabla address, 10-variable vector, semantic hash
  classify.py             # deterministic block/domain/overstatement classifiers
  cli.py                  # run and batch commands
  embeddings.py           # optional SBERT adapter
  ids.py                  # stable UUID/content hash helpers
  markdown_parser.py      # frontmatter, heading, paragraph split
  pipeline.py             # controller and object extraction
  render_html.py          # HTML snapshot renderer
  schemas.py              # Pydantic artifact schemas
  storage.py              # JSON/HTML + optional Postgres append-only storage
  docs/
    postgres_schema.sql
    BUILD_SPEC.md
  samples/
    sample_article.md
    sample_output.json
    sample_output.html
  tests/
    test_pipeline.py
Backside/workflows/lossless-context.workflow/
  dependencies.json
  configs/default.json
```

## Python Modules

- `markdown_parser.py`: loads Markdown, parses YAML frontmatter, splits by headings and paragraph boundaries.
- `classify.py`: classifies blocks as `CLAIM`, `EVIDENCE`, `EQUATION`, `DEFINITION`, `KILL_CONDITION`, `DOMAIN_SHIFT`, or `OTHER`.
- `ids.py`: produces required stable IDs: `vault_id`, `doc_id`, `note_version`, `content_hash`, `block_id`, `claim_id`, `equation_id`, `evidence_id`, `run_id`, `audit_snapshot_id`, `repair_item_id`.
- `address.py`: computes Nabla address, 10-variable semantic vector, and deterministic semantic hash.
- `pipeline.py`: orchestrates extraction and builds the full Pydantic artifact.
- `render_html.py`: renders a compact reader/auditor HTML snapshot.
- `storage.py`: writes JSON/HTML locally and optionally stores append-only snapshots in Postgres.
- `embeddings.py`: optional SBERT embedding adapter for block vectors.
- `cli.py`: user-facing command entrypoint.

## Pydantic Schemas

Schemas live in `schemas.py`:

- `IdSet`
- `MarkdownBlock`
- `ClaimArch`
- `EvidenceChain`
- `KillArch`
- `EquationSemantics`
- `DomainBoundary`
- `MechanismEdge`
- `ReviewerSeed`
- `ScoreLedgerEntry`
- `FourScoreDashboard`
- `GapItem`
- `LosslessArtifact`

## Design Notes

Calibration rules and edge failures live in:

```text
Backside/lossless_context_pipeline/docs/DESIGN_NOTES_2026-05-20.md
```

Key implementation constraints:

- score artifact function, not topic
- binary `0/3` determines address
- confidence must not alter canonical address
- use Hamming distance for inter-model agreement
- `C` is explicit synthesis/integration, not quality
- `E` is artifact disorder, not dark subject matter
- grade is audit metadata, never filename identity
- `R_sem` means Relation/Bond; `R_file` means Risk

## Postgres Tables

DDL lives in `docs/postgres_schema.sql`.

Tables:

- `lcc_documents`
- `lcc_audit_runs`
- `lcc_audit_snapshots`
- `lcc_blocks`
- `lcc_claims`
- `lcc_equations`
- `lcc_evidence`
- `lcc_repair_items`

`lcc_blocks.embedding vector(384)` is ready for `pgvector`. Storage is append-only by `run_id`, `audit_snapshot_id`, and `content_hash`.

## CLI Commands

Single file:

```powershell
python -m Backside.lossless_context_pipeline.cli run `
  --input Backside/lossless_context_pipeline/samples/sample_article.md `
  --out EXPORTS/lossless-context/sample `
  --vault-id theophysics-brain `
  --embeddings none
```

Batch:

```powershell
python -m Backside.lossless_context_pipeline.cli batch `
  --input-root X:\Backside\corpus\C4C `
  --out EXPORTS/lossless-context/c4c `
  --vault-id theophysics-brain `
  --glob *.md `
  --limit 100 `
  --embeddings none
```

3D semantic projection over generated artifacts:

```powershell
python -m Backside.lossless_context_pipeline.cli space `
  --input-root X:\EXPORTS\lossless-context\calibration-corpus `
  --out X:\EXPORTS\lossless-context\calibration-corpus\semantic-space `
  --mode sbert
```

With SBERT block embeddings:

```powershell
python -m Backside.lossless_context_pipeline.cli run `
  --input path\to\article.md `
  --out EXPORTS/lossless-context\article `
  --vault-id theophysics-brain `
  --embeddings sbert
```

With Postgres:

```powershell
python -m Backside.lossless_context_pipeline.cli run `
  --input path\to\article.md `
  --out EXPORTS/lossless-context\article `
  --vault-id theophysics-brain `
  --postgres-dsn "postgresql://user:pass@host:5432/db"
```

## Sample Output

- JSON: `samples/sample_output.json`
- HTML: `samples/sample_output.html`

## Test Plan

1. `python -m pytest Backside/lossless_context_pipeline/tests -q`
2. Verify stable IDs are unchanged across repeated runs on identical content.
3. Verify a changed Markdown paragraph changes `content_hash`, `run_id`, and affected `block_id`.
4. Verify the grade is not present in `filename_safe_address`.
5. Verify `address`, `semantic_vector`, `hash`, `claim_arch`, `evidence_chain`, `kill_arch`, `eq_sem`, `domain_boundary`, `mechanism_graph`, `ledger_schema`, `four_score_dashboard`, `eight_gaps`, and `decompress` exist in JSON.
6. Verify HTML snapshot renders address, four scores, claims, and Eight Gaps.
7. Apply `docs/postgres_schema.sql` to a pgvector-enabled Postgres database.
8. Run with `--postgres-dsn`; verify no overwrite on repeated run and new audit snapshots on changed content.
9. Run a batch over a small corpus folder with `--limit 10`.
10. Reconstruction test: give only `sample_output.json` to an AI and ask it to reconstruct thesis, claim chain, evidence bridge, equation role, domain boundaries, kill conditions, weakest point, and repair action.

## Known Boundaries

The first pass is intentionally deterministic and conservative. LLM-fill fields remain `EXPAND_REQUIRED` until a second pass is wired:

- `buried_claim`
- `operational_claim`
- `evidence_chain.connection_to_claim`
- `kill_arch.implicit_kill`
- hostile-review repair detail
