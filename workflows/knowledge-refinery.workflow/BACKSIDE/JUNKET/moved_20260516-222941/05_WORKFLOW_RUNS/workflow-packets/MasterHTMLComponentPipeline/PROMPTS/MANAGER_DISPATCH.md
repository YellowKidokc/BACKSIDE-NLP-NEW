# Manager Dispatch: Master HTML Component Pipeline

Use this when David assigns multiple Claude command lines.

## Lanes

1. **Inventory Lane**: run/read component inventory and verify marked HTML readiness.
2. **Injection Lane**: plan Phase 2 injections into marked sockets.
3. **GUI Lane**: design PySide6 command/status contract.
4. **Safety Lane**: review imported scripts for hard-coded paths, writes, dry-run, and GUI readiness.

## Coordination Rule

Each lane writes only into its own review artifact unless David or Codex explicitly approves edits.

Suggested outputs:

- `REVIEW/lane-1-component-inventory.md`
- `REVIEW/lane-2-phase2-injection-plan.md`
- `REVIEW/lane-3-gui-backend-contract.md`
- `REVIEW/lane-4-script-safety-review.md`

## Current Manager Position

The key system is not "make pages by hand." The key system is:

```text
Marked HTML sockets -> script inventory -> reviewable plan -> scripted injection/replacement -> GUI status -> approved output
```

The PySide6 GUI should be a window into that process, not the process itself.
