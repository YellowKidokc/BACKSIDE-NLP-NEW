# 12_EXPORTS

This folder does not create the final `MASTER_ARTICLE_INDEX.xlsx` in this round.

Worker-5 writes workbook-aligned append payloads to:

- `sample_output/<paper-slug>/workbook-append-payload.json`

That payload is keyed by the provisional canon sheets:

- `Master_Index`
- `Classification_Routing`
- `Layer_Ledger`
- `Readiness_Decision`
- `Vault_Export`

Reason:
- the workbook columns are treated as provisional canon for this build round
- the persistent workbook file itself can be created or updated later without changing row identity or field names
