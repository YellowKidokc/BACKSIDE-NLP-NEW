# Two Command-Line Split

David's operating suggestion is now the workflow rule for this pass.

## Lane A: Station Repair

Purpose: make or repair station outputs.

Allowed work:

- Generate missing two-lane reports.
- Generate missing Easy/Academic reading files.
- Rebuild one article or all reader HTML.
- Repair scripts when a station cannot run.

Do not judge final readiness from Lane A. Lane A can say "built", but Lane B proves "ready".

## Lane B: Export Judge

Purpose: sync and judge the root export surface.

Run order:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File X:\WORKFLOWS\MDA-PUBLICATION\00_WORKFLOW_TESTS\test_mda_workflow.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File X:\WORKFLOWS\MDA-PUBLICATION\00_WORKFLOW_TESTS\sync_root_exports.ps1
```

Then inspect:

```text
X:\WORKFLOWS\MDA-PUBLICATION\EXPORTS
```

## Guardrail

Only root `EXPORTS` is the judged handoff surface. Station folders are working state. `09_EXPORT_PACKET` remains a legacy/export packet source until root `EXPORTS` fully replaces it.

