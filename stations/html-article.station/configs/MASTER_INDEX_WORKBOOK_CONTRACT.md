# Master Index Workbook Contract

Purpose: define the one persistent Excel workbook that stays with the workflow and keeps cataloging papers over time.

This is not a one-run report. It is the long-lived index for the vault/article pipeline within a lossless framework.

## Core Rule

Every processed paper should append at least one master row to the workbook.

Section-level rows may live in additional sheets, but the paper itself must always be indexable from the master workbook.

## Why This Exists

- reduce duplicates
- give the AI layer and snapshot layer a stable index surface
- provide a durable catalog from now forward
- let David inspect routing, maturity, and publication state from one place

## Workbook Identity

Suggested filename:

`MASTER_ARTICLE_INDEX.xlsx`

Suggested location:

`\\dlowenas\brain\Backside\workflows\html-article.workflow\12_EXPORTS\MASTER_ARTICLE_INDEX.xlsx`

## Minimum Required Sheets

- `Master_Index`
- `Classification_Routing`
- `Layer_Ledger`
- `Readiness_Decision`
- `Vault_Export`

## Master_Index Required Columns

- `paper_uuid`
- `page_id`
- `title`
- `source_file_name`
- `semantic_address`
- `primary_bucket`
- `secondary_bucket`
- `type`
- `story_flag`
- `series`
- `status`
- `maturity`
- `website_layers`
- `section_count`
- `equation_count`
- `claim_count`
- `contradiction_count`
- `math_status`
- `vector_status`
- `graph_status`
- `rigor_status`
- `publish_status`
- `vault_export_path`
- `html_export_path`
- `last_run_uuid`
- `last_updated_utc`

## Naming Rule

The semantic address identifies the artifact.

The grade, readiness, and audit results do not become the permanent filename because those values can change after repair.

## Classification Rule

`story_flag` should be explicit so stories do not get mixed with generic papers, notes, or argument modules.

## Append Rule

When a paper is rerun:

- update the existing row if `paper_uuid` already exists
- append new run-level details to supporting sheets
- do not create silent duplicate master rows unless a new artifact identity is intentionally created
