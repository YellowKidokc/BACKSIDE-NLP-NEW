# Postgres Ledger Schema Prompt

Design the Postgres ledger for FAP.

Track:

- transport jobs
- station actions
- files/manifests
- hashes
- conflicts
- review/fail/pass verdicts
- model/prompt calls
- output packages
- round-trip syncs

Postgres records the truth. Files stay on X/NAS.

Return SQL-style table proposals and a short explanation of what each table is for.
