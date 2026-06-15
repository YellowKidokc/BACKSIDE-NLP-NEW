# Manager Column Audit - 2026-05-13

This audits the worker "done" claims against actual usable outputs.

## Verdict

The workers mostly completed their assigned read-only diagnostic lanes, but the pipeline itself is **not ready to run**.

The recurring issue is that "DONE" means "I produced my report," not "the workflow is executable."

## Column Board

| Lane | Claimed State | Verified State | Usable Now? | Reason |
| --- | --- | --- | --- | --- |
| Worker 1 - inventory | DONE / REVIEW | Accurate diagnostic complete | No | Inventory found 35/35 files unmarked: 0 PAGE_META, 0 BEGIN:COMPONENT pairs, 0 data-component attrs. |
| Worker 2 - injection plan | DONE / BLOCKED | Plan complete, execution blocked | No | Phase 2 has no sockets to inject into; imported scripts target wrong roots or old marker dialect. |
| Worker 3 - GUI contract | DONE / REVIEW | Contract complete, implementation gaps remain | Partly | Good GUI contract, but component_operator needs richer JSON reports and status enums before GUI is useful. |
| Worker 4 - script safety | DONE / REVIEW | Safety audit complete | Partly | Useful audit, but it found many scripts unsafe until wrappers exist. |

## Hard Blockers

1. **No Kimi-canonical markers in target files.**
   - `OUTPUT/component-inventory-worker-1.json`
   - `file_count=35`
   - `review_count=35`
   - `pass_count=0`
   - `total_begin=0`
   - `total_data_component=0`

2. **Old labeler emits wrong marker dialect.**
   - Existing `02_label_gtq_sections.py` is safe-ish because it writes sidecars by default.
   - But it emits old `<!-- BEGIN: NAME -->` markers, not `<!-- BEGIN:COMPONENT:type:name -->`.

3. **Imported scripts are unsafe for GUI/direct execution.**
   - Worker 4 found many direct overwrite scripts with no dry-run and no backup.
   - Several scripts hard-code old roots like `D:\GTQ-BUILD`, OneDrive Cannon paths, Desktop paths, or NAS IP paths.

4. **GUI cannot honestly show success yet.**
   - Worker 3's contract is good, but the current status model collapses `UNMARKED` and `BROKEN` into `REVIEW`.
   - Replace/extract also need JSON reports for the GUI review/apply flow.

## What Is Actually Done

- Read-only source inventory.
- Phase 2 injection plan.
- GUI backend/status contract.
- Imported script safety review.
- X runtime copies exist.

## What Is Not Done

- Kimi-canonical marker pass.
- Safe wrappers for dangerous imported scripts.
- Full script registry safety metadata.
- GUI prototype.
- Actual Phase 2 injection.

## Recommended Next Column

Create a new implementation lane:

```text
Worker 5 / Codex: Phase 0 Marker Upgrade
```

Tasks:

1. Upgrade or replace `02_label_gtq_sections.py` so it emits Kimi v1 markers:
   `<!-- BEGIN:COMPONENT:type:name -->`.
2. Run it on one canary file only.
3. Verify canary with `component_operator.py inventory`.
4. If canary passes, batch the marker upgrade.
5. Only then reopen Worker 2 for injection.

Second lane:

```text
Worker 6 / Codex: Safe Wrapper Layer
```

Tasks:

1. Add `safety_tier` and `wrapper` fields to `CONFIG/script_registry.json`.
2. Hide blocked scripts from GUI/run surface.
3. Write wrappers for dangerous in-place scripts.

## Manager Note

Do not let "DONE" posts move this into production. Treat current output as scout/review work. The real next executable step is the Phase 0 canonical marker upgrade.
