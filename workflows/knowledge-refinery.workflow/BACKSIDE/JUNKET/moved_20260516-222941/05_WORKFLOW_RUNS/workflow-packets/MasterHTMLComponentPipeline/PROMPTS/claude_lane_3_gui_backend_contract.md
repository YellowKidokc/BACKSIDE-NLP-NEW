# Claude Lane 3: GUI Backend Contract

Assignment: design the command/status contract for a PySide6 snapshot GUI.

Inputs:

- `docs_gui_snapshot.md`
- `SCRIPTS/component_operator.py`
- `CONFIG/script_registry.json`

Return:

- buttons/actions the GUI needs
- subprocess commands per action
- JSON files the GUI should read
- status fields per file
- error display shape
- minimum viable GUI screen layout

Rules:

- The GUI must call scripts; do not duplicate workflow logic inside the GUI.
- Dry-run by default.
- Writes require an explicit Apply button.
- Every stage must show per-file status.
