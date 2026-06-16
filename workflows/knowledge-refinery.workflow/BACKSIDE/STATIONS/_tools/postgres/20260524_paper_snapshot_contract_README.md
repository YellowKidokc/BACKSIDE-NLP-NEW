# Paper Snapshot Contract Migration

Files:

- `20260524_paper_snapshot_contract_migration.sql`

Purpose:

- Adds a canonical `paper_snapshots` table to hold the shared machine object.
- Normalizes the contract into queryable side tables for claims, tags, derivations, evidence, contradictions, and station runs.
- Extends existing `graph_nodes` and `graph_edges` so Graphify and later stations can point back to the same snapshot truth instead of drifting.
- Creates `snapshot_embeddings` only if `pgvector` is already installed. The live `treaties` database currently exposes only `plpgsql`, so the migration will skip embeddings and emit a notice.

Why this is additive:

- Existing paper-grader tables stay untouched: `papers`, `paper_sections`, `paper_scores`, `paper_model_items`, `evidence_items`, `axiom_mappings`, `html_snapshots`, `graph_nodes`, and `graph_edges`.
- New snapshot-contract tables sit beside them.
- Existing graph tables are only extended with nullable linkage/provenance columns plus metadata indexes.

Table intent:

- `paper_snapshots`: one canonical paper snapshot object, plus top-level routing fields like `canon_folder_route`, `domain_code`, and `subject_code`.
- `station_runs`: per-station write marks, hashes, changed fields, warnings, and status.
- `paper_claims`: normalized claim ledger, including `not_claimed`, `tier_limited`, and defeat-condition payloads.
- `paper_tags`: graph-intake tags by category, optionally scoped to a claim.
- `paper_derivations`: ordered derivation chains with `weakest_link` and `break_if_false`.
- `paper_evidence`: support/oppose/context evidence rows tied to claims or the snapshot as a whole.
- `paper_contradictions`: contradiction ledger between claims, with severity and resolution state.
- `graph_nodes` / `graph_edges`: existing tables extended with snapshot-aware provenance fields.
- `snapshot_embeddings`: optional pgvector table for RAG/search if the extension is installed later.

Current live findings that shaped this migration:

- Existing tables already present: `papers`, `paper_sections`, `paper_scores`, `paper_model_items`, `evidence_items`, `axiom_mappings`, `ingest_documents`, `html_snapshots`, `paper_comparisons`, `graph_nodes`, `graph_edges`, `axioms`.
- Current row counts are small enough to extend safely: `papers=5`, `graph_nodes=78`, `graph_edges=53`.
- `pgvector` is not installed yet.
- `psql` is not on local `PATH`, but Python `3.13` with `psycopg2` is available, so the migration can still be applied from this machine.

Recommended apply path from this machine:

- Use Python + `psycopg2` against `treaties`, not `psql`, unless David already has a local `psql.exe` path he prefers.
