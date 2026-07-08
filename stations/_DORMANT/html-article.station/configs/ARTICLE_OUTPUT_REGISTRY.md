# Article Output Registry

Purpose: define every output family the HTML article workflow should be able to produce.

Rule: if an output is not listed here, it is optional, experimental, or not yet accepted into the workflow.

## Design Principles

- Every important output should exist in machine-readable form.
- Most important outputs should also exist in human-readable Markdown form.
- Excel is a rollup surface, not the only source of truth.
- Section-level packets are first-class outputs.

## Canonical Output Families

### 1. Source Provenance

Purpose:
- prove what was ingested
- preserve rerunability

Formats:
- JSON
- SHA-256 text
- Markdown note

Artifacts:
- `source-manifest.json`
- `source.sha256`
- `run-manifest.json`
- `run-summary.md`

Excel:
- `Source_Manifest`
- `Run_Manifest`

### 2. Lossless Text

Purpose:
- preserve the normalized text that every later lane refers back to

Formats:
- Markdown
- JSON

Artifacts:
- `normalized-text.md`
- `lossless-source-map.json`

Excel:
- `Lossless_Text_Index`

### 3. Section Structure

Purpose:
- define stable `section_id` units

Formats:
- JSON
- Markdown

Artifacts:
- `section-map.json`
- `section-map.md`
- `section-packets/`

Excel:
- `Section_Map`

### 4. YAML And Metadata

Purpose:
- page metadata plus section metadata

Formats:
- YAML
- JSON
- Markdown

Artifacts:
- `frontmatter.yaml`
- `metadata.json`
- `metadata.md`

Excel:
- `Page_Metadata`
- `Section_Metadata`

### 4A. Categorization And Routing

Purpose:
- decide where the artifact belongs structurally
- define naming, YAML, and downstream routing

Formats:
- JSON
- YAML
- CSV

Artifacts:
- `classification-routing.json`
- `semantic-address.json`
- `routing-tags.csv`

Required fields:
- `primary_bucket`
- `secondary_bucket`
- `type`
- `story_flag`
- `series`
- `status`
- `maturity`
- `website_layers`

Excel:
- `Classification_Routing`

### 5. Tags

Purpose:
- lightweight semantic and workflow labels

Formats:
- JSON
- CSV

Artifacts:
- `tags.json`
- `section-tags.csv`

Excel:
- `Tags`

### 6. Claims

Purpose:
- claim extraction and packetization

Formats:
- JSON
- CSV
- Markdown

Artifacts:
- `claim-ledger.csv`
- `claim-packets.json`
- `claims.md`

Excel:
- `Claim_Ledger`

### 7. Contradictions And Tensions

Purpose:
- record structural tensions and challenge points

Formats:
- JSON
- Markdown

Artifacts:
- `contradiction-ledger.json`
- `contradictions.md`

Excel:
- `Contradictions`

### 8. Math Translation

Purpose:
- preserve raw math and translated math side by side

Formats:
- JSON
- Markdown
- HTML snippet

Artifacts:
- `math-payload.json`
- `math-translation.md`
- `math-snippets.html`

Excel:
- `Math_Translation`

### 9. Readability Rewrites

Purpose:
- audience-tier rendering

Formats:
- JSON
- Markdown

Artifacts:
- `readability-payload.json`
- `author-level.md`
- `accessible.md`
- `academic.md`

Excel:
- `Readability_Modes`

### 10. Section Vectors

Purpose:
- vector-ready section objects

Formats:
- JSONL
- JSON

Artifacts:
- `section-vectors.jsonl`
- `vector-metadata.json`

Excel:
- `Vector_Index`

### 11. Graph Links

Purpose:
- candidate edges between sections, claims, and concepts

Formats:
- JSON
- CSV
- Markdown

Artifacts:
- `graph-edges.json`
- `graph-edges.csv`
- `graph-review.md`

Excel:
- `Graph_Edges`

### 12. Rigor

Purpose:
- record 7Q, fact, contradiction, and readiness outputs

Formats:
- JSON
- Markdown

Artifacts:
- `rigor-report.json`
- `rigor-report.md`
- `readiness-decision.json`

Excel:
- `Rigor`
- `Readiness_Decision`

### 13. Layer Ledger

Purpose:
- record where each section and page has already been

Formats:
- JSON
- CSV

Artifacts:
- `layer-ledger.json`
- `section-pass-matrix.csv`

Excel:
- `Layer_Ledger`

### 14. Loopback Review

Purpose:
- formalize returns upstream instead of hiding failure in chat

Formats:
- JSON
- Markdown

Artifacts:
- `loopback-review.json`
- `loopback-review.md`

Excel:
- `Loopback_Review`

### 15. HTML Render

Purpose:
- render human-facing page blocks

Formats:
- HTML
- JSON

Artifacts:
- `page-payload.json`
- `render-blocks/`
- `article.html`

Excel:
- `Render_Blocks_Index`

### 16. Vault Export

Purpose:
- immediate vault-ready artifact

Formats:
- Markdown
- YAML

Artifacts:
- `vault-ready.md`
- `vault-sidecar.yaml`

Excel:
- `Vault_Export`

## Required Workbook Sheets

- `Master_Index`
- `Dashboard`
- `Source_Manifest`
- `Run_Manifest`
- `Lossless_Text_Index`
- `Classification_Routing`
- `Section_Map`
- `Page_Metadata`
- `Section_Metadata`
- `Tags`
- `Claim_Ledger`
- `Contradictions`
- `Math_Translation`
- `Readability_Modes`
- `Vector_Index`
- `Graph_Edges`
- `Rigor`
- `Readiness_Decision`
- `Layer_Ledger`
- `Loopback_Review`
- `Render_Blocks_Index`
- `Vault_Export`

## Important Call

Excel should be a rollup of the workflow state, not the only place the workflow exists.

The authoritative order should be:

1. JSON / JSONL machine packets
2. Markdown / HTML human artifacts
3. Excel rollup workbook

One workbook should persist for the life of the workflow as the cumulative vault/article index. New papers append into that workbook instead of creating isolated one-off indexes only.
