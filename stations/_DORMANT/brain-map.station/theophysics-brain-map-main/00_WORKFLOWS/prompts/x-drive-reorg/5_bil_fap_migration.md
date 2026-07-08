# Prompt 5 — BIL + FAP migration execution

**Owner:** Codex
**Risk:** High (touches the only currently-running scheduled task on the system)
**Depends on:** 4c complete and verified (all D:\BIL/D:\FAP refs rewritten)
**Blocks:** Final phase — closes out the X-drive consolidation

---

## Goal

Execute the full move of D:\BIL → X:\BIL and D:\FAP → X:\FAP per David's Option A decision 2026-05-16. After this, **the May-10 NAS=cold-archive lock is fully superseded — BIL runs on X:**.

---

## Pre-conditions (must all be true)

- Prompt 4c delivered: all hot D:\BIL files have refs rewritten to X:\BIL\* and X:\FAP. Acceptance check from 4c passed.
- Task Scheduler XML backup exists at `D:\BIL\_TASK_SCHEDULER_BACKUP_*.xml` and updated version at `D:\BIL\_TASK_SCHEDULER_NEW_*.xml`.
- X:\BIL\ exists with only the placeholder README.md from Phase 1b.
- X:\FAP\ exists with 63 files (mirrored copy from Phase 1a).
- D:\BIL\ exists with 264 files (live working copy).
- D:\FAP\ exists with 63 files (matches X:\FAP per Phase 2 dedup verification).

If ANY pre-condition fails, halt and post status to comms before doing anything.

---

## Required outcome

### Stage 1 — Stop the FAP postgres sync task

```powershell
$taskName = (Get-ScheduledTask | Where-Object {$_.TaskName -match 'FAP|BIL'} | Select-Object -First 1).TaskName
Disable-ScheduledTask -TaskName $taskName
Write-Host "Disabled: $taskName"
```

Verify the task is disabled (Task Scheduler GUI or `Get-ScheduledTask`).

Wait 60 seconds to ensure any in-flight run completes.

### Stage 2 — Pre-move snapshot

Before any moves, snapshot the source state for rollback:
- File count: `(Get-ChildItem D:\BIL -Recurse -File).Count` → save to log
- Total size: `(Get-ChildItem D:\BIL -Recurse -File | Measure-Object Length -Sum).Sum / 1MB`
- Latest mtime: `(Get-ChildItem D:\BIL -Recurse -File | Sort-Object LastWriteTime -Desc | Select-Object -First 1).LastWriteTime`

Same for D:\FAP.

### Stage 3 — Archive the X:\BIL placeholder

Phase 1b created X:\BIL\README.md as a placeholder. Move it aside so it doesn't conflict with the incoming files:

```powershell
Move-Item X:\BIL\README.md X:\Backside\X_BIL_PLACEHOLDER_README_PRE_MIGRATION.md
```

### Stage 4 — Move D:\BIL → X:\BIL

```powershell
robocopy D:\BIL X:\BIL /MOVE /E /R:3 /W:5 /XD __pycache__ .git /XF *.pyc *.pyo /LOG:X:\_LOGS\prompt_5_robocopy_bil.log
```

Robocopy `/MOVE` deletes source after successful copy. `/XD __pycache__ .git` skips junk; `/XF *.pyc *.pyo` skips compiled. `/R:3 /W:5` = retry 3× with 5s wait on errors.

Check exit code. Robocopy success codes: 0, 1, 2, 3. Anything ≥8 is failure — halt.

### Stage 5 — Move D:\FAP → X:\FAP

X:\FAP already has 63 files (mirrored from Phase 1a). The D:\FAP copy is identical. So this is a **D:\FAP → D:\_ARCHIVE\FAP** archive (per no-delete rule), not an overwrite.

```powershell
robocopy D:\FAP D:\_ARCHIVE\FAP /MOVE /E /R:3 /W:5 /LOG:X:\_LOGS\prompt_5_robocopy_fap.log
```

If any new files have appeared in D:\FAP since the 4c sweep, they get archived here — flag in log for David's review.

### Stage 6 — Import new Task Scheduler XML

```powershell
$newXml = (Get-ChildItem D:\BIL\_TASK_SCHEDULER_NEW_*.xml -ErrorAction SilentlyContinue | Select-Object -First 1).FullName
# WAIT — D:\BIL no longer exists after Stage 4. Move the XML files first.
```

Actually correct order: **before Stage 4, move the XML files to a safe location:**

```powershell
# Insert between Stage 3 and Stage 4:
New-Item -ItemType Directory X:\Backside\task_scheduler_migration -Force
Move-Item D:\BIL\_TASK_SCHEDULER_*.xml X:\Backside\task_scheduler_migration\
```

Then after Stage 5:

```powershell
$newXml = (Get-ChildItem X:\Backside\task_scheduler_migration\_TASK_SCHEDULER_NEW_*.xml | Select-Object -First 1).FullName
$taskName = "Theophysics_FAP_Postgres_Sync"  # or whatever the original was
Register-ScheduledTask -Xml (Get-Content $newXml -Raw) -TaskName $taskName -Force
Enable-ScheduledTask -TaskName $taskName
Write-Host "Re-imported and enabled: $taskName"
```

### Stage 7 — Update X:\BIL\README.md (post-migration)

Replace the placeholder README with a live one:

```markdown
# X:\BIL — Behavioral Intelligence Layer

**What this is:** Live BIL runtime (preference engine, FAP postgres sync, dashboards, adapters).
**Owner:** Codex (X drive infrastructure)
**Status:** live
**Last updated:** 2026-05-16

Moved from D:\BIL on 2026-05-16 per David Option A decision. Supersedes May-10 "BIL=local, NAS=cold archive" lock.

## What's inside
- `engines\pipeline\` — FAP postgres sync, healthcheck, LLM hub, media router
- `data\` — fap_sync output, fap_health reports, exa searches
- `adapters\` — video, behavior, etc.
- `scripts\` — bil_overlay.ahk and utility scripts
- `bil_service.py` — the running service
- `bil-dashboard.html` — HTML dashboard (consider replacing with PySide 6 dashboard from prompt 4e)

## How to interact
- Scheduled task `Theophysics_FAP_Postgres_Sync` runs every 12h
- Manual run: `python X:\BIL\bil_service.py`
- Dashboard: `X:\BIL\bil-dashboard.html` or upcoming PySide 6 dashboard

## Migration notes
- May-10 lock superseded. NAS is now the hot path for BIL writes.
- Pre-migration snapshot: see `X:\_LOGS\prompt_5_log_2026-05-16.md`
- D: archive: `D:\_ARCHIVE\BIL_pre_X_migration\` (originally D:\BIL — empty after /MOVE, but preserved as marker)
- D:\FAP archived to D:\_ARCHIVE\FAP\
```

### Stage 8 — Verify FAP sync runs clean

```powershell
# Trigger the task manually (one cycle):
Start-ScheduledTask -TaskName "Theophysics_FAP_Postgres_Sync"
Start-Sleep -Seconds 60
# Check it produced an X:\FAP\... output (not D:)
Get-ChildItem X:\BIL\data\fap_sync\ | Sort-Object LastWriteTime -Desc | Select-Object -First 3 Name, LastWriteTime
```

The latest file should be timestamped today, and its content should reference `X:\FAP\` not `D:\FAP\`.

If exit code is non-zero OR the new file's content has `D:\FAP\` strings, **roll back** (see Stage 9) and report.

### Stage 9 — Rollback procedure (if anything fails)

1. `Disable-ScheduledTask -TaskName "Theophysics_FAP_Postgres_Sync"`
2. Re-import the BACKUP XML: `Register-ScheduledTask -Xml (Get-Content $backupXml -Raw) -TaskName $taskName -Force`
3. `robocopy X:\BIL D:\BIL /MOVE /E /R:3 /W:5` (reverse move)
4. `Move-Item D:\_ARCHIVE\FAP D:\FAP` (un-archive)
5. Restore the placeholder X:\BIL\README.md from `X:\Backside\X_BIL_PLACEHOLDER_README_PRE_MIGRATION.md`
6. `Enable-ScheduledTask -TaskName "Theophysics_FAP_Postgres_Sync"`
7. Post rollback status to comms broadcast.

---

## Acceptance check

```powershell
# D:\BIL is gone (empty marker preserved in D:\_ARCHIVE)
Test-Path D:\BIL                                    # False
Test-Path D:\_ARCHIVE\BIL_pre_X_migration           # True (or however archive is named)

# X:\BIL is live and has the BIL content
(Get-ChildItem X:\BIL -Recurse -File).Count          # ~260+ (was 264; -1 for placeholder, +matching moves)
Test-Path X:\BIL\engines\pipeline\fap_postgres_sync.py  # True
Test-Path X:\BIL\README.md                           # True, with new content

# D:\FAP archived; X:\FAP unchanged
Test-Path D:\FAP                                     # False
Test-Path D:\_ARCHIVE\FAP                            # True
(Get-ChildItem X:\FAP -Recurse -File).Count          # 63 (unchanged from Phase 1)

# Task scheduler points at X:
(Get-ScheduledTaskInfo -TaskName "Theophysics_FAP_Postgres_Sync").LastTaskResult   # 0

# Latest FAP sync output references X:
Get-Content (Get-ChildItem X:\BIL\data\fap_sync\*.json | Sort LastWriteTime -Desc | Select -First 1).FullName | Select-String 'D:\\FAP|D:\\BIL'  # 0 hits
```

---

## Log

`X:\_LOGS\prompt_5_log_2026-05-16.md` — pre-snapshot, robocopy outputs, task scheduler import result, smoke-test cycle result. If rollback was triggered, full rollback log.

---

## Absolute rules

- **Halt at the first sign of trouble.** This is the most destructive operation in the X-drive reorg. No silent recovery — if anything goes wrong, log it, post to comms, ask David.
- **Pre-snapshot is mandatory.** Without it, rollback is guesswork.
- **No file deletions.** D:\BIL becomes empty after `/MOVE` — preserve it as a marker (rename `D:\_BIL_MOVED_TO_X_20260516\` or create that empty folder). Same for D:\FAP.
- **Task Scheduler XML must use the exact original task name.** Codex doesn't get to rename it.
- **Verify ONE cycle runs clean before declaring done.** Don't trust that the rewrite was complete — actual execution is the proof.
