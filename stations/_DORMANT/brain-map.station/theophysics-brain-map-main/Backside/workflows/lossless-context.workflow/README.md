# Lossless Context Workflow

This workflow describes the Lossless Context Compression and Semantic Addressing pass.

## Contract

- Inputs: canonical Markdown articles or packet Markdown.
- Working state: `X:\Backside\_state\lossless-context`.
- Final exports: `X:\EXPORTS\lossless-context\<run-id>`.
- Config: `configs\default.json`.
- Dependencies: `dependencies.json`.

## Stations

1. `markdown-parse`
2. `block-classify`
3. `semantic-address`
4. `audit-snapshot`
5. `postgres-store` optional

Final human-readable JSON and HTML artifacts belong under `X:\EXPORTS`; intermediate state stays under `X:\Backside\_state`.
