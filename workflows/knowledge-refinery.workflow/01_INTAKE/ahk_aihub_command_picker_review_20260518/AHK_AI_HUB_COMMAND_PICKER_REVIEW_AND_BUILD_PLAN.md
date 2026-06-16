# AHK / AI-HUB Command Picker Review and Build Plan
## David Lowe | POF 2828 | 2026-05-18

## Source Archives Reviewed

- `C:\Users\lowes\Downloads\AHKCommandPicker-main (1).zip`
- `C:\Users\lowes\Downloads\Codex-Powershell_GUI-OBS-Plugin-Final-Claude.zip`

Extracted review copies:

- `X:\knowledge-refinery\01_INTAKE\ahk_aihub_command_picker_review_20260518\extracted_ahk_command_picker\`
- `X:\knowledge-refinery\01_INTAKE\ahk_aihub_command_picker_review_20260518\extracted_codex_powershell_commander\`

## Verdict

Build a new **AI-HUB Command Center v2** rather than directly adopting either
archive as-is.

Use AHK Command Picker as a design reference, not as the production base.
Use the Python PowerShell Commander as a prototype/reference for a script GUI,
not as the execution backbone without hardening.

Best architecture:

```text
AHK v2 hotkey/control layer
  -> command manifest / picker UI
  -> BAT bootstrap wrappers where useful
  -> Python workflow runner
  -> PowerShell/BAT/Python/AHK/scripts
  -> logs + state + AI-HUB integration
```

## Findings - AHK Command Picker

### Strengths

- Good command-palette concept.
- Fast keyboard-first interface.
- Supports searchable commands and parameter passing.
- Clean extension pattern via `UserCommands\MyCommands.ahk` and
  `UserCommands\MyHotkeys.ahk`.
- MIT license in local `License.md`.

### Problems

- It requires **AutoHotkey v1.1**.
- This machine currently has AutoHotkey **v2** installed under:
  `C:\Program Files\AutoHotkey\v2\`.
- Current `D:\GitHub\ai-hub-v2\AI-HUB.ahk` is already AHK v2:
  `#Requires AutoHotkey v2.0+`.
- Directly mixing this v1 picker into AI-HUB v2 would be brittle.

### Conclusion

Do not integrate the v1 AHK Command Picker directly into AI-HUB.

Two acceptable options:

1. Keep it as a separate v1 utility only if AutoHotkey v1.1 is installed.
2. Better: port the concept to AHK v2 / Python manifest architecture.

## Findings - PowerShell Commander

### Strengths

- Modern CustomTkinter GUI.
- Has categories and visual script buttons.
- Supports `.ps1` and `.py`.
- Supports input prompts.
- Has startup BAT wrapper.
- Good starting shape for a standalone command console.

### Problems

- Config declares 58 scripts, but the reviewed archive contains no matching
  actual script files in `script_dump`.
- It currently supports `.ps1` and `.py`, but not `.bat`, `.cmd`, `.ahk`, URLs,
  folders, apps, or AI-HUB actions.
- Execution uses `subprocess.Popen(..., shell=True)`, which should be replaced
  with safer argument-list execution.
- No command allowlist / risk flags / confirmation gates.
- No per-run JSON log.
- No active-window capture / restore / isolation.
- No AI-HUB tab/module integration.
- README says CC0, but no separate license file was found in the archive.

### Conclusion

Useful prototype, but not production-safe as the backbone.

## Recommended Product Shape

Name:

```text
AI-HUB Command Center
```

Purpose:

One searchable command surface for David's local workflows:

- `.bat`
- `.cmd`
- `.ps1`
- `.py`
- `.ahk`
- folders
- URLs
- apps
- AI-HUB actions
- comms posts
- proof/Lean builds
- ingestion/vectorization workflows

## Core Requirements

### 1. Manifest-Driven Commands

Use a JSON manifest:

```json
{
  "id": "lean.t1.build",
  "title": "Build T1 Lean Kernel",
  "category": "Theophysics",
  "type": "bat",
  "path": "X:\\knowledge-refinery\\...\\run_t1_build.bat",
  "working_dir": "X:\\knowledge-refinery\\...\\lean_t1_kernel",
  "args": [],
  "requires_confirm": false,
  "risk": "safe",
  "show_console": true,
  "capture_active_window": false,
  "tags": ["lean", "t1", "build"]
}
```

### 2. Safe Runner

Python runner should execute by type:

- `bat/cmd`: `cmd.exe /c <file>`
- `ps1`: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <file>`
- `py`: `python <file>`
- `ahk`: `AutoHotkey64.exe <file>`
- `url`: open browser
- `folder`: open Explorer
- `app`: launch executable

Avoid `shell=True` except for carefully wrapped `.bat/.cmd` launches.

### 3. AHK v2 Hotkey Layer

AHK should:

- open the picker with one hotkey, likely `CapsLock`;
- optionally preserve `Shift+CapsLock` for normal Caps Lock toggle;
- capture active window title/class/process/id;
- pass active-window context to Python runner;
- restore focus after command if requested;
- isolate/target the active window when a command is window-specific.

### 4. Window Isolation

Each command may specify:

```json
{
  "window_policy": "none | active | restore | target_class | target_process"
}
```

This matters for preference-system workflows where the command should act on the
window David was using, not whichever window happens to be focused later.

### 5. Logs

Every run should write:

```text
logs/YYYY-MM-DD/<timestamp>_<command-id>.log
logs/YYYY-MM-DD/<timestamp>_<command-id>.json
```

JSON should include:

- command id/title/category;
- start/end time;
- exit code;
- stdout/stderr path;
- active window context;
- cwd;
- arguments;
- runner version.

### 6. Risk Gates

Commands should be marked:

- `safe`
- `writes_files`
- `network`
- `destructive`
- `admin`

`destructive` and `admin` require confirmation by default.

### 7. AI-HUB Integration

Start standalone, then integrate into AI-HUB as:

```text
D:\GitHub\ai-hub-v2\modules\command_center.ahk
D:\GitHub\ai-hub-v2\modules\command_center.html
D:\GitHub\ai-hub-v2\command_center\
```

Do not merge into AI-HUB core until the standalone pilot works.

## Recommended Build Order

### Phase 1 - Standalone Pilot

Create:

```text
D:\GitHub\ai-hub-v2\command_center\
  command_center.ahk
  command_picker.py
  run_command.py
  commands.json
  logs\
  scripts\
    bat\
    ps1\
    py\
    ahk\
```

Goal:

`CapsLock` opens a searchable command picker and can launch a few safe commands.

### Phase 2 - Workflow Registry

Add real workflows:

- open Theophysics argument folder;
- build T1 Lean kernel;
- open comms dashboard;
- run prediction registry hash;
- launch AI-HUB;
- open Q chain index;
- start ClipSync / sync server;
- run intake/vectorization scripts.

### Phase 3 - Window Context

Add active-window capture and restore:

- title;
- process name;
- class;
- HWND;
- monitor position.

### Phase 4 - AI-HUB Tab

Embed the command registry as an AI-HUB tab after standalone proof.

## Build vs Prompt-Out Decision

### Build locally if:

- we want it tied to current paths and actual workflows immediately;
- we want AHK v2 compatibility with existing AI-HUB;
- we want safety/logging/risk gates from the beginning.

### Prompt out if:

- we want a generic command-picker UI first;
- we want another model to draft a clean AHK v2 port;
- we are not ready to connect it to real workflows.

## Prompt-Out Spec

If sending this to another AI, use:

```text
Build an AutoHotkey v2 + Python command picker for Windows.

Requirements:
- AHK v2 hotkey opens searchable command picker.
- Python manifest-driven runner launches bat/cmd/ps1/py/ahk/url/folder/app commands.
- Use JSON command manifest with id/title/category/type/path/working_dir/args/tags/risk/requires_confirm/window_policy.
- Capture active window context in AHK and pass it to Python.
- Write per-run log and JSON metadata.
- Avoid shell=True except for controlled cmd.exe /c wrappers.
- Include risk gates for destructive/admin commands.
- Keep standalone first; design for later integration into an existing AHK v2 app.
- Provide clean file layout, README, install BAT, and sample commands.
```

## Final Recommendation

Build it locally as a standalone AI-HUB-adjacent pilot.

Do not install AutoHotkey v1 just to use the old picker. Do not use the current
Python commander as-is for real workflows. Take the best idea from each:

- AHK Command Picker: keyboard-first command palette.
- PowerShell Commander: visual categories and script manager.
- AI-HUB v2: existing AHK v2 ecosystem and startup surface.

Then build the robust backbone around a manifest-driven Python runner with AHK
v2 as the front panel.
