# PySide6 Snapshot GUI Design

The GUI should be a front door over the workflow packet, not a second implementation.

## Main Panes

- **Source Tree**: roots, selected files, PAGE_META summary.
- **Pipeline Board**: Intake, Inventory, Extract, Replace, Inject, Verify, Output, Error.
- **Component Inspector**: selected file's components, BEGIN/END pair status, data-component count.
- **Run Console**: script output, stderr, log file links.
- **Review Pane**: generated diffs, extracted components, approve/apply buttons.

## Backend Contract

The GUI calls scripts by subprocess and reads JSON reports from `OUTPUT` and `LOGS`.

Minimum command set:

```text
python SCRIPTS/component_operator.py inventory --root INPUT --out OUTPUT/inventory.json
python SCRIPTS/component_operator.py extract --root INPUT --component sidebar:sidebar-toc --out REVIEW/sidebar
python SCRIPTS/component_operator.py verify --root INPUT --out OUTPUT/verify.json
python SCRIPTS/component_operator.py replace --root INPUT --component sidebar:sidebar-toc --template REVIEW/sidebar-approved.html --apply
```

## Non-Negotiables

- Dry-run is default.
- Writes require an explicit apply action.
- Every write produces a backup or review artifact.
- The GUI shows errors per file, not only a single failure blob.
