# Prompt 4e (revised) — PySide6 Workflow Composer

**Owner:** Codex
**Risk:** Medium (new program, no existing-state mutation)
**Depends on:** Backside architecture locked (see `BACKSIDE_ARCHITECTURE.md`) + 4a foundation complete
**Supersedes:** the original "PySide 6 dashboard" brief — scope widened to workflow composer + monitor + health surface

---

## Goal

Build a PySide 6 desktop application that is **the operating surface for the brain.** David should never need to click a `.bat` file directly. Four panes + one startup health sequence.

The app reads/writes JSON contracts already defined in `BACKSIDE_ARCHITECTURE.md` — workflow-configs, state-manifests, dependencies. It does not invent new schemas.

---

## Pre-conditions

- Read `X:\BACKSIDE_ARCHITECTURE.md` first — that document is the contract you implement against. Especially:
  - Workflow folder shape (`configs/`, `STATE/`, `dependencies.json`)
  - State manifest schema
  - Workflow config schema
  - Dependencies declaration
  - `BRAIN_ROOT` env-var pattern
- Read `X:\THEOPHYSICS_PRIMER.md` — framework anchor
- Reference (style + structure precedent, NOT direct fork): `O:\999_IGNORE\Python_Backend_Dashboards\` — the Obsidian-side dashboard David calls "indestructible." Mine the `engine/` split for patterns; do not copy the GUI directly (different scope).

---

## Where it lives

```
Backside/workflows/_composer/                ← yes, the composer is itself a "workflow"
  README.md
  _AGENT_BRIEF.md
  RUN.bat                                    ← double-click launches the GUI
  health_check.bat
  pipeline.py                                ← actually the GUI entry (main.py-style)
  main.py                                    ← PySide6 app entry
  app/
    __init__.py
    main_window.py
    panes/
      monitor.py
      compose.py
      run.py
      health.py
    widgets/
      station_chip.py
      run_card.py
      health_lamp.py
      log_tail.py
    services/
      state_watcher.py                       ← polls _state/active_runs.json + STATE/*.json
      config_io.py                           ← reads/writes configs/<name>.json
      runner.py                              ← subprocess spawn for workflow RUN.bat
      health_runner.py                       ← orchestrates startup health sequence
    models/
      run.py                                 ← Pydantic models matching state.json schema
      config.py                              ← Pydantic models matching workflow config schema
      dependencies.py
  requirements.txt                           ← PySide6, pydantic, watchdog
  configs/
    default.json                             ← composer's own settings: poll interval, theme
```

`RUN.bat` (drive-agnostic preamble):
```batch
@echo off
if not defined BRAIN_ROOT (
  for %%i in ("%~dp0..\..\..") do set "BRAIN_ROOT=%%~fi"
)
cd /d "%~dp0"
if exist venv\Scripts\activate.bat call venv\Scripts\activate.bat
python main.py
```

---

## Startup sequence (the first thing the user sees)

1. Splash window. Title: "Theophysics Brain — starting."
2. **Health ticker walks through:**
   - Read `BRAIN_ROOT/Backside/workflows/*/dependencies.json`
   - For each declared station: check `Backside/stations/<id>/health_check.bat` exit code
   - For each declared external service: HTTP probe with 5s timeout
   - For each declared model: confirm file exists at `Backside/_models/<name>/`
   - Show each as a row: `[●] claim-extract` (orange) → `[●] claim-extract` (green) once passed
3. **Aggregate:** PASS / DEGRADED / FAIL
4. If FAIL, still let user enter the app (Health pane is the landing) but disable Run pane.
5. If PASS or DEGRADED, splash dismisses → Monitor pane is the landing.

---

## The four panes

### 1. Monitor (default view)

- Top: list of active runs (polled every 2s from `Backside/_state/active_runs.json`)
- Each run rendered as a card: workflow name, config name, elapsed time, station chips colored by status
- Click a run → drill into per-run detail: input file list, output file list (clickable to open), full station call log, errors
- Filter: all / running / failed-last-24h
- Below: log tail from the most recent run (live-following the workflow's `_LOGS/` or stdout)

### 2. Compose (the workflow builder)

- Left sidebar: list of workflows (from `Backside/workflows/*/`)
- Pick a workflow → main area shows its `dependencies.json` stations as draggable chips
- Below: list of saved configs from `configs/*.json`
- Click a config → station chips highlight per their `enabled` state
- Toggle a chip (click to enable/disable, drag to reorder)
- Edit params: each station has an expandable params section
- Right sidebar: live JSON preview of the config being built
- "Save As..." → writes to `configs/<name>.json`
- "Save" → overwrites current config
- "Delete" → confirm dialog, removes config file (except `default.json` which is protected)

### 3. Run

- Top: workflow selector + config selector (both populated from filesystem)
- Middle: drop zone — drag a file in OR pick a file. Sets it as `00_DROP/` target.
- "Run" button → spawns `RUN.bat` with `--config <name>` argument via subprocess
- Live: stdout streams into a panel below, state updates flow into Monitor automatically
- "Cancel" button kills the subprocess and writes a `cancelled` status to the run's state.json

### 4. Health

- Re-runs the startup health sequence on demand
- Per-station, per-service, per-model status row
- Each row clickable → shows the health_check.bat stdout + the `dependencies.json` block that declared it
- "Re-run all" / "Re-run failed only" buttons
- Last-checked timestamp per row

---

## Required behavior contracts

- **Filesystem-as-truth.** No internal cache. Every poll reads the JSON files fresh. If David edits a config file in a text editor while the GUI is open, the change appears within one poll cycle.
- **No state mutation except through explicit writes** — saving a config, deleting a config, starting a run. Never silently rewrite anything.
- **Subprocess for workflow runs**, not in-process. The composer is a control surface; workflows run in their own process so a workflow crash doesn't kill the GUI.
- **PySide6 ≥ 6.5.** Use QWidgets, not QML, for compatibility with the Obsidian-dashboard pattern.
- **Theme:** dark by default, system-aware on toggle. Use one accent color (David's call — propose `#5f3dc4` purple to match the Mermaid diagrams in `ARCHITECTURE.md`).
- **Drive-agnostic:** every file path goes through `BRAIN_ROOT`. No hardcoded `X:\`.

---

## Acceptance check

```powershell
# 1. Structure exists
Test-Path "$env:BRAIN_ROOT\Backside\workflows\_composer\main.py"
Test-Path "$env:BRAIN_ROOT\Backside\workflows\_composer\RUN.bat"
Test-Path "$env:BRAIN_ROOT\Backside\workflows\_composer\requirements.txt"

# 2. Launches without error (close the window after splash to test)
cd $env:BRAIN_ROOT\Backside\workflows\_composer
.\RUN.bat
# expect: splash window appears, health ticker runs to completion, main window appears

# 3. Compose pane round-trips a config edit
# Create a config via GUI: "test-config", save
Test-Path "$env:BRAIN_ROOT\Backside\workflows\grade-paper\configs\test-config.json"
# Edit it externally in notepad
notepad "$env:BRAIN_ROOT\Backside\workflows\grade-paper\configs\test-config.json"
# Modify a station's enabled flag, save
# Within 2s the GUI's Compose pane reflects the change

# 4. Monitor pane sees a manually-created run
$run = @{
  run_id = "test-run-001"
  workflow = "grade-paper"
  config = "test-config"
  started_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
  status = "running"
  stations_called = @()
}
$run | ConvertTo-Json | Out-File "$env:BRAIN_ROOT\Backside\workflows\grade-paper\STATE\test-run-001.json"
# Within 2s the Monitor pane shows "test-run-001"
# Clean up: Remove-Item "$env:BRAIN_ROOT\Backside\workflows\grade-paper\STATE\test-run-001.json"

# 5. Health pane re-runs all checks
# Click "Re-run all" in Health pane, observe ticker walks through every station/service/model

# 6. No hardcoded X:\ anywhere
Select-String -Path "$env:BRAIN_ROOT\Backside\workflows\_composer\**\*.py" -Pattern '[XB]:\\' | Select-Object Path, LineNumber, Line
# expected: empty (or only inside string literals that are clearly user-facing examples)
```

All six should pass.

---

## Log

Write `X:\_LOGS\prompt_4e_log_2026-05-16.md` with:
- All files created (path + size + LOC)
- Screenshots of each pane (saved to the log folder)
- Any place you had to deviate from this brief (and why)
- Any `dependencies.json` or `configs/` file you assumed exists but doesn't yet (so we can backfill before launch)

---

## Absolute rules

- **No `.bat` clicks required.** Every action a user wants to take must be available through the GUI.
- **No hardcoded paths.** `BRAIN_ROOT` everywhere.
- **Filesystem is the database.** Do not introduce SQLite/Postgres for composer state. Configs and runs are JSON files on disk.
- **Subprocess workflows, never in-process.** Composer is a control surface, not a runtime.
- **No emoji in code/UI labels.** Use icons (QStyle.SP_*) or one-character glyphs (●, ○, ✓, ✗) only where semantically needed.
- **PR or branch on `theophysics-brain-map` repo** when done — do not strand the commit in your sandbox. Push the branch + open the PR + confirm with the GitHub URL.
- **One-shot push instruction:**
  ```
  git push -u origin codex/4e-composer
  gh pr create --base main --head codex/4e-composer \
    --title "4e: PySide6 workflow composer" \
    --body "Implements 4a-anchored architecture. See log for screenshots and deviations."
  ```

---

## Next prompt after this (preview, not your scope)

4h — "build the migration script that moves current `X:\paper-proof-grader\`, `X:\axioms\`, `X:\knowledge-refinery\`, etc. into the new `Backside/workflows/` shape with junctions at old paths." Depends on 4a + this 4e + the architecture lock.
