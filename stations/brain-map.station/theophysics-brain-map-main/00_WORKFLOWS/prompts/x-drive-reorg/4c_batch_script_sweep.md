# Prompt 4c — Batch-script path sweep

**Owner:** Codex
**Risk:** Medium (touches the BIL pipeline that runs every 12h)
**Depends on:** Nothing (parallel with 4a/4d)
**Blocks:** Phase 5 (BIL+FAP migration cannot run until refs are updated)

---

## Goal

Rewrite all hardcoded `D:\BIL\*` and `D:\FAP` path references across the BIL codebase + Windows Task Scheduler so they point at the future `X:\BIL\*` and `X:\FAP` locations. **Do NOT move the actual files** — that's Phase 5. This prompt only edits source files.

Reason: D:\BIL has 78 hardcoded `D:\FAP` references across 10 files. The FAP postgres sync runs every 12h. If we move D:\FAP before sweeping refs, the next sync breaks. Sweep first, then move.

---

## Pre-conditions

- `D:\BIL\` exists with the BIL code (264 files, 3.5 MB).
- `D:\FAP\` exists (63 files, matches X:\FAP).
- BIL decision Option A is locked (full move to X:) per the approved plan and `project_x_drive_restructure.md` memory.
- The May-10 NAS=cold-archive lock is superseded by David 2026-05-16: *"we need to move all that to X."*

## Files known to need updates

From grep on 2026-05-16 (`Grep "D:\\FAP" D:\BIL`), 78 occurrences across these:

1. `D:\BIL\.gitignore` (1 hit) — adjust
2. `D:\BIL\data\fap_health\FAP_HEALTH.latest.md` (14 hits) — historical; OK to leave, but flag
3. `D:\BIL\data\fap_health\FAP_HEALTH_20260511_*.md` (multiple, 7–14 hits each) — historical, leave
4. `D:\BIL\engines\pipeline\fap_healthcheck.py` (14 hits) — **HOT, must update**
5. `D:\BIL\engines\pipeline\fap_boot.py` (1 hit) — **HOT, must update**
6. `D:\BIL\engines\pipeline\fap_postgres_sync.py` (1 hit) — **HOT, must update (runs every 12h)**
7. `D:\BIL\engines\pipeline\llm_hub.py` (4 hits) — **HOT, must update**
8. `D:\BIL\engines\pipeline\stations\media_router.py` — likely **HOT**
9. `D:\BIL\engines\pipeline\fap_dashboard.html` — **HOT** (dashboard UI)

Also grep for `D:\\BIL` references in BIL's own files — if anything inside D:\BIL points to D:\BIL by absolute path (config files, schedulers), rewrite those too. Use:
```powershell
Get-ChildItem D:\BIL -Recurse -File | Select-String -Pattern 'D:\\BIL\\','D:\\FAP[\\)\""]' -SimpleMatch
```

## Required outcome

### Stage 1 — Inventory

Run the grep, produce a complete file:occurrence list. Write to `X:\_LOGS\prompt_4c_inventory_2026-05-16.md`. **Halt and let David review the list before any writes.**

### Stage 2 — Rewrite hot files

For each hot file in the inventory:
- `D:\BIL\` → `X:\BIL\`
- `D:\FAP` → `X:\FAP`
- `D:\\BIL\\` (JSON-escaped) → `X:\\BIL\\`
- `D:\\FAP` (JSON-escaped) → `X:\\FAP`

Use the file's existing encoding (don't convert UTF-16 → UTF-8 or vice versa). Preserve line endings.

### Stage 3 — Historical files

For files in `D:\BIL\data\fap_health\FAP_HEALTH_*.md` — these are historical health-check reports. **Leave the file content alone** (they're a record of past state) but rename / mark them so they're not confused with current docs. Option: move to `D:\BIL\data\fap_health\_HISTORICAL_PRE-X-MIGRATION\` per the no-delete rule.

### Stage 4 — Task Scheduler XML

The 12h FAP postgres sync runs as a Task Scheduler job. Steps:

1. List tasks: `schtasks /Query /FO LIST /V | findstr /I "FAP BIL"`
2. Export the job XML: `schtasks /Query /XML /TN "<task name>"` → save to `D:\BIL\_TASK_SCHEDULER_BACKUP_<name>.xml`
3. Edit the saved XML: replace `D:\BIL\` and `D:\FAP` references with `X:\BIL\` and `X:\FAP`. Save as `D:\BIL\_TASK_SCHEDULER_NEW_<name>.xml`.
4. **DO NOT re-import yet.** That's Phase 5. Leave both files in place for Phase 5 to use.

### Stage 5 — Don't move files

Do NOT run `robocopy /MOVE` or any file-moving operation. Refs only. Phase 5 does the move.

---

## Acceptance check

```powershell
# After Stage 2, every hot file's reference to D:\FAP is gone:
$hotFiles = @(
  'D:\BIL\engines\pipeline\fap_healthcheck.py',
  'D:\BIL\engines\pipeline\fap_boot.py',
  'D:\BIL\engines\pipeline\fap_postgres_sync.py',
  'D:\BIL\engines\pipeline\llm_hub.py',
  'D:\BIL\engines\pipeline\stations\media_router.py',
  'D:\BIL\engines\pipeline\fap_dashboard.html'
)
$hotFiles | ForEach-Object {
  $hits = (Select-String -Path $_ -Pattern 'D:\\FAP|D:\\BIL' -SimpleMatch -ErrorAction SilentlyContinue).Count
  Write-Host "$_ — D:\* refs remaining: $hits (target: 0)"
}

# Task Scheduler XML backup + new versions exist
Get-ChildItem D:\BIL\_TASK_SCHEDULER_*.xml | Format-Table Name, Length

# FAP postgres sync still runs (dry-run only — don't write)
# python D:\BIL\engines\pipeline\fap_postgres_sync.py --dry-run
```

All hot files should report 0 remaining `D:\BIL\` / `D:\FAP` refs.

---

## Log

`X:\_LOGS\prompt_4c_log_2026-05-16.md`:
- Inventory output (Stage 1 file:line:context)
- Per-file replacement counts
- Task Scheduler job names found + XML paths
- Anything flagged as ambiguous (leave for review)

---

## Absolute rules

- **No file moves.** Only text-content edits + Task Scheduler XML exports.
- **No file deletions.** Historical health-check reports get archived to `_HISTORICAL_PRE-X-MIGRATION\`, not removed.
- **Halt after Stage 1** for David's eyes on the inventory before writing.
- **Preserve encoding + line endings** of source files (use `[IO.File]::WriteAllText(...)` with explicit encoding, not `Set-Content` which can re-encode).
- The `D:\brain\03_DEBERTA` and `D:\brain\08_CLAIMS` references in paper-proof-grader's config.json are **OUT OF SCOPE** — those are local ML model paths, separate system, don't touch.
