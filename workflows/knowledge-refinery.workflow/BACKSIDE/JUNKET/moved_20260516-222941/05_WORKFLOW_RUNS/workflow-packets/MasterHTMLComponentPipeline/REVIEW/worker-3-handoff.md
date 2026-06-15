# Worker 3 Handoff

Callsign: claude-code-worker-3
Lane: PySide6 GUI backend/status contract (Lane 3)
Date: 2026-05-13
Mode: read-only (no production HTML touched, no scripts executed)

## Column Status

TODO:
- IMP-1 — add JSON report for `replace` (high)
- IMP-2 — add JSON report for `extract` (medium)
- IMP-3 — expand `status` enum to `PASS`/`UNMARKED`/`PARTIAL`/`BROKEN` + reason codes (high)
- IMP-5 — extend contract to cover `label_gtq_sections`, `wire_navigation`, `wire_media`, `series_polish` (high)
- IMP-6, IMP-7 — absolute paths and `schema_version` (low/medium)

IN_PROGRESS:
- (none — lane-3 deliverable shipped this pass)

REVIEW:
- `REVIEW/lane-3-gui-backend-contract.md` — needs Codex sign-off on Section 7 implementation items and David sign-off on Section 8 backup location

BLOCKED:
- (none)

DONE:
- Read README.md, docs_gui_snapshot.md, PROMPTS/MANAGER_DISPATCH.md, PROMPTS/gui_status_interpreter.md
- Read SCRIPTS/component_operator.py end-to-end
- Read CONFIG/source_roots.example.json, CONFIG/script_registry.json
- Inspected OUTPUT/component-inventory-worker-1.json and OUTPUT/k-production-ready.inventory.json
- Wrote REVIEW/lane-3-gui-backend-contract.md (sections 1–8: process interface, command catalog, JSON schemas, file status model, GUI state machine, pane wiring, gap list, open question)
- Posted ARRIVED to workflow-4 (comms id 718)

## Files Inspected

- D:\GitHub\pipeline-workflows\workflows\MasterHTMLComponentPipeline\README.md
- D:\GitHub\pipeline-workflows\workflows\MasterHTMLComponentPipeline\docs_gui_snapshot.md
- D:\GitHub\pipeline-workflows\workflows\MasterHTMLComponentPipeline\PROMPTS\MANAGER_DISPATCH.md
- D:\GitHub\pipeline-workflows\workflows\MasterHTMLComponentPipeline\PROMPTS\gui_status_interpreter.md
- D:\GitHub\pipeline-workflows\workflows\MasterHTMLComponentPipeline\SCRIPTS\component_operator.py
- D:\GitHub\pipeline-workflows\workflows\MasterHTMLComponentPipeline\CONFIG\source_roots.example.json
- D:\GitHub\pipeline-workflows\workflows\MasterHTMLComponentPipeline\CONFIG\script_registry.json
- D:\GitHub\pipeline-workflows\workflows\MasterHTMLComponentPipeline\OUTPUT\component-inventory-worker-1.json
- D:\GitHub\pipeline-workflows\workflows\MasterHTMLComponentPipeline\OUTPUT\k-production-ready.inventory.json

## Commands Run

Read-only inspection only. No scripts executed. No production HTML touched.

Comms only:
- `GET  https://comms.dlowehomelab.com/pinned`
- `GET  https://comms.dlowehomelab.com/channel/claude-code/unread`
- `GET  https://comms.dlowehomelab.com/channel/workflow-4/unread`
- `POST https://comms.dlowehomelab.com/channel/workflow-4` (ARRIVED, id 718)

## Results

Lane-3 deliverable shipped at `REVIEW/lane-3-gui-backend-contract.md`. Highlights:

1. **Process interface.** Every GUI-launched script: cwd = packet root, stdin = unused, stdout = human log (Run Console), stderr = errors (Error pane), exit code = 0/2/1 = success/partial/hard-fail, declared `--out` file is the structured report. Run is "done" only when both process exit and `--out` exist.
2. **Writes rule.** Only `replace --apply` mutates production HTML; all other modes are pure reads. Dry-run default is non-negotiable.
3. **Schemas pinned.** `InventoryReport` / `FileInventory` documented from the live JSON, plus non-breaking additions (`schema_version`, `reason_codes`, `command`, `exit_code`, `duration_ms`, `counts_by_*`).
4. **`extract.json` and `replace.json` proposed.** Neither currently exists — both are GUI blockers (IMP-1/IMP-2).
5. **Status enum expanded.** Today's `PASS`/`REVIEW` collapses "unmarked" and "broken markers" — confirmed by Worker 1's K-Production-Ready inventory (35/35 REVIEW, all because they have zero markers, not because anything is broken). Proposed split: `PASS` / `UNMARKED` / `PARTIAL` / `BROKEN` + per-file `reason_codes[]`. This is also what lets Worker 2's Phase 2 injection plan filter cleanly and lets the GUI Pipeline Board route into the right lane.
6. **State machine + pane wiring** defined so a PySide6 implementer can wire panes without re-deriving the protocol.

## Risks

- **Imported scripts are off-contract.** `label_gtq_sections`, `wire_navigation`, `wire_media`, `series_polish`, `tts_markdown_export`, `canonical_sort` all live in `SCRIPTS/imported/html_master_workflow/` and are "in-place capable" per `CONFIG/script_registry.json`. They have no JSON reports and no documented dry-run mode. If the GUI calls them as-is, the writes-rule is violated. Flag for Worker 4 (Safety Lane) — they likely need the same `--apply` gate before being GUI-exposed.
- **Replace backup model.** Current implementation drops `<file>.bak` as a sibling in production folders. May conflict with Kimi's authority over `Master HTMl/`. Section 8 of the contract proposes routing to `ARCHIVE/<utc>/` instead — decision needed before any apply runs.
- **Status enum change is breaking** if not done with `schema_version`. IMP-3 + IMP-7 must land together.
- **K-Production-Ready isn't marked yet.** The current inventory shows 0/35 files with PAGE_META or BEGIN markers. The GUI is being designed for a state of the source folder that doesn't exist yet. This is not a Lane-3 problem to solve — but it means a working GUI today would show "Intake: 35, Output: 0," which is correct but unsatisfying. Worker 2's injection plan is the input that changes this.

## Next Action

For the next worker on Lane 3 or for Codex:

1. Implement IMP-3 (status enum + `reason_codes`) and IMP-7 (`schema_version`) together in `component_operator.py`. Pure additive change; no GUI needed yet.
2. Implement IMP-1 (`replace.json` report). This unblocks the GUI's approve/apply gate.
3. Decide the Section 8 backup-location question with Kimi.
4. After IMP-1/IMP-3/IMP-7 land, write a minimal PySide6 prototype that just renders the Source Tree + Pipeline Board from `OUTPUT/k-production-ready.inventory.json`. That validates the contract end-to-end before any imported scripts are wired in.

Coordinate with Worker 4 on the imported scripts before extending the contract to cover them — Worker 4 owns the safety audit and may impose constraints that change the wrapper shape.
