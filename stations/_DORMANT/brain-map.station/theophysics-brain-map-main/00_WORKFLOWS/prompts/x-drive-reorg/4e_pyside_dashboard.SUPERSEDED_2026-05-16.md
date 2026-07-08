# Prompt 4e — PySide 6 brain dashboard (GUI)

**Owner:** Codex
**Risk:** High (new GUI surface — scope creep risk)
**Depends on:** 4d delivered (state.json schema is the data source)
**Blocks:** Nothing downstream — but this is what makes the brain *legible* day-to-day

---

## Goal

Build a PySide 6 GUI dashboard that gives David a **100-foot overview** of the brain's runtime state at a glance. He explicitly said this should multiply his throughput by ~4× — "doing more in the same amount of time because I'm looking at things from a 100-foot overview."

**MVP is read-only.** Control (start/stop/retry), architecture editing (drag pipelines), and scheduling-editor are explicitly deferred to later phases. Don't build them now.

---

## Architecture

```
X:\Backside\brain_dashboard\
  pyproject.toml                       ← packaging
  README.md                            ← Layer 1 + Layer 2
  src\brain_dashboard\
    __init__.py
    __main__.py                        ← `python -m brain_dashboard` entry
    app.py                             ← QApplication bootstrap
    main_window.py                     ← QMainWindow with tab views
    views\
      overview.py                      ← top-level "100-ft" page
      nlp_detail.py                    ← per-NLP status + recent runs
      pipeline_state.py                ← live drop-queue + in-flight files
      schedule.py                      ← Task Scheduler readout
      logs.py                          ← tail of X:\_LOGS\*.log
    data\
      state_reader.py                  ← reads intake_engine state.json
      task_scheduler.py                ← subprocess `schtasks /Query /XML`
      log_tail.py                      ← reads tail of X:\_LOGS\
    widgets\
      status_pill.py                   ← reusable colored status indicator
      ascii_chart.py                   ← simple bar chart for queue depths
  assets\
    icon.png                           ← app icon (no emoji)
  tests\
    test_state_reader.py
    test_log_tail.py
```

Dependencies:
- `PySide6>=6.6`
- `qt-material>=2.14` (theming, optional but recommended)
- `pyyaml>=6.0` (read engine config)

Installable: `pipx install -e X:\Backside\brain_dashboard` → `brain-dashboard` launches.

---

## MVP scope — five views (tabs)

### Tab 1 — Overview ("the 100-foot view")

Single page. Auto-refreshes every 5s. Shows:

- **Big status grid:** one card per NLP. Each card shows:
  - NLP name
  - Status pill: green (healthy) / yellow (queued) / red (errored) / grey (idle)
  - Queue depth (files in `00_DROP/`)
  - Last run: timestamp + duration + exit code
  - Mini-trend: last 10 run exit codes as a row of colored squares

- **Top bar:** total queue depth across all NLPs, last engine event time, system status (engine running yes/no).

- **Errors panel** (right side): recent errors from any NLP, last 5 visible.

### Tab 2 — NLP detail

Pick an NLP from the dropdown. Shows:
- The NLP's full README.md (Layer 1+2+3 content) rendered as markdown.
- Recent 20 runs as a table (started, duration, exit code, files processed).
- Drop folder content (live list of files in `00_DROP/`).
- Output folder size + latest file.

### Tab 3 — Pipeline state ("where things are")

A simple flowchart-style widget:
- Master `X:\DROP_HERE` on the left
- An arrow per route, labeled with the class
- Each NLP's `00_DROP/` with current count visible
- Each NLP's `OUTPUT/` with latest file timestamp

Live count, refreshes 5s.

### Tab 4 — Schedule

Read Task Scheduler tasks tagged with `Theophysics_*`. Show:
- Task name
- Last run time + result
- Next scheduled time
- Status (ready / running / disabled)

Read-only — no enable/disable buttons in MVP.

### Tab 5 — Logs

Tab pane with a sub-dropdown of available log files. Selected log: tail -n 200 view, monospace font, auto-scroll, optional `Pause` button.

---

## Required outcome

### Stage 1 — Package skeleton + window

`pyproject.toml` + entry point + a blank QMainWindow that launches without crashing.

### Stage 2 — Data readers

`state_reader.py` reads `intake_engine/state.json` (schema from prompt 4d). Pure-data, no Qt imports. Tested.

`task_scheduler.py` shells out to `schtasks /Query /XML /TN "*"` (Windows-only), parses XML, returns list of task dicts. Filters to tasks with `Theophysics_` or `FAP_` prefix.

`log_tail.py` reads last N lines of a log file, safe with rolling files.

### Stage 3 — Views (build in order, ship after each)

1. Overview tab (most value, fastest to build)
2. Schedule tab (small, well-defined)
3. NLP detail tab
4. Pipeline state widget
5. Logs tab

Ship after tab 1 works. Don't gold-plate before David sees it.

### Stage 4 — Theme + polish

Apply `qt-material` dark theme. App icon. Keyboard shortcuts (Ctrl+1..5 for tabs, F5 to refresh, Ctrl+Q to quit).

### Stage 5 — Out of MVP scope (do NOT build)

These are explicitly deferred to later prompts:
- Starting / stopping / retrying NLPs from the GUI
- Editing config.json from the GUI
- Drag-to-rearrange pipeline architecture
- Creating / editing Task Scheduler jobs
- Authentication, multi-user
- Web version

---

## Acceptance check

```powershell
# Package installs and launches without error
pipx install -e X:\Backside\brain_dashboard
brain-dashboard --version

# Smoke test — launches GUI, no exception in 30s
timeout 30 brain-dashboard --headless-smoke-test

# Tests pass (data readers only — Qt UI tested manually)
cd X:\Backside\brain_dashboard
pytest tests\

# David runs it for real and confirms:
#  - Tab 1 shows live queue depths
#  - Schedule tab shows the FAP postgres sync job
#  - Logs tab tails X:\_LOGS\intake_engine_*.log
```

---

## Log

`X:\_LOGS\prompt_4e_log_2026-05-16.md` — screenshots (use Pillow / Qt screenshot API to save PNG) of each tab, test results.

---

## Absolute rules

- **MVP is READ-ONLY.** No buttons that mutate state. None.
- **No web framework, no Electron, no Tauri.** PySide 6 only.
- **Don't reinvent state — read `intake_engine/state.json`.** If the schema needs new fields, propose them in prompt 4d revision, don't fork.
- **Refresh interval ≥5s.** Don't hammer the filesystem.
- **No emoji in UI, no emoji in code.**
- **Don't auto-launch at startup.** David runs it manually for now.
