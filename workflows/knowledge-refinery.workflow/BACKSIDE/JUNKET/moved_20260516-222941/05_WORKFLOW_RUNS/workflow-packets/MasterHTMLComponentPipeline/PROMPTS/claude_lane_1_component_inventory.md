# Claude Lane 1: Component Inventory

Assignment: audit the marked HTML set only. Do not rewrite page content.

Inputs:

- Kimi marking standard
- target folder or file list from David
- `SCRIPTS/component_operator.py`

Run:

```text
python SCRIPTS/component_operator.py inventory --root <TARGET_HTML_ROOT> --out OUTPUT/component-inventory.json
python SCRIPTS/component_operator.py verify --root <TARGET_HTML_ROOT> --out OUTPUT/component-verify.json
```

Return:

- files scanned
- files passing PAGE_META
- files with unmatched BEGIN/END pairs
- duplicate component names
- data-component coverage count
- exact blockers for Phase 2 injection

Rules:

- No content edits.
- No in-place writes.
- If a file fails, quote the component key and file path.
