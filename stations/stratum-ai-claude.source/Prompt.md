# CODEX BUILD — Stratum → FORGE Hub
## POF 2828 | June 10, 2026
## Extend the existing Stratum PySide6 app into the FORGE control plane

---

## SOURCE

Base repo: `Stratum-AI-CLaude-main` (Python, PySide6, ~7 months old)
Target repo: `https://github.com/YellowKidokc/stratum-forge` (or rename existing)

This is NOT a rewrite. The architecture is correct. Extend it.

---

## REMOVE

- `core/tts_engine.py` — delete entirely
- `ui/tabs/audio_tab.py` — delete
- `ui/tabs/audio_tab_simple.py` — delete
- `ui/tabs/tts_preprocessor_tab.py` — delete
- All TTS references in `app.py`, `main_window.py`, `manifest references`
- `ui/tabs/spelling_tab.py` — delete (never used)
- Remove TTS from command registry defaults

---

## KEEP AS-IS (these work, don't touch)

- `core/hotkeys.py` — `keyboard` library global hotkeys
- `core/hotstrings.py` — hotstring engine
- `core/command_registry.py` — JSON command pattern
- `core/settings_manager.py` — INI settings
- `core/ai_clients.py` — Claude + OpenAI + DeepSeek clients
- `ui/tabs/chat_tab.py` — AI chat
- `ui/tabs/shortcuts_manager_tab.py` — hotkey editor
- `ui/tabs/prompts_tab.py` — prompt picker
- `ui/tabs/prompts_manager_tab.py` — prompt editor
- `ui/tabs/settings_tab.py` — settings UI
- `ui/tabs/search_scraper_tab.py` — search/scraper
- `ui/tabs/adapters.py` — client adapters
- `ui/api_key_dialog.py` — first-run dialog
- `config/commands.json` — command definitions
- `config/workflows.json` — workflow definitions (extend, don't replace)

---

## ADD: System Tray (core/tray.py)

Stratum should minimize to system tray, not close.

```
- QSystemTrayIcon with FORGE icon
- Right-click menu: Show, Pipeline Status, Comms, Settings, Quit
- Minimize to tray on window close (override closeEvent)
- Double-click tray icon → show window
- Tray tooltip shows: "FORGE — X packets in flight, Y in review"
```

---

## ADD: Clipboard Tab (ui/tabs/clipboard_tab.py)

Restore the clipboard functionality that was commented out.

```
- win32clipboard monitor (OnClipboardChange equivalent)
- 20 hotkey slots (Ctrl+Shift+1-0, Ctrl+Alt+1-0)
- Pin/tag/search
- Aggregate copy mode (rapid successive copies auto-stack)
- History with reorder
- Every clipboard event → POST to BIL at $env:BIL_SERVER/bil/clipboard
- Signal weight: copied_text = 0.8
```

Do NOT use a separate Python bridge server. The clipboard monitor runs inside the Stratum process. No port 3456 needed.

---

## ADD: Pipeline Tab (ui/tabs/pipeline_tab.py)

The FORGE control panel. This is the main new feature.

```
Layout:
- Left panel: Workflow selector (dropdown of all workflows from WORKFLOW_REGISTRY.json)
- Center panel: Current packets in flight (read from MANIFEST.json)
  - Each packet shows: name, workflow, current stage, status, time elapsed
  - Color coding: running=blue, review=amber, error=red, done=green
- Right panel: Review queue
  - Files waiting for human approval
  - For each: filename, FIS classification, BIL relevance score, proposed route
  - Buttons: Approve, Reject, Reclassify (dropdown)
  - Reason field (optional, for correction logging)
- Bottom panel: Station health (canary output)
  - Grid of all stations: green=active, yellow=degraded, red=dead

Data sources:
- MANIFEST.json at $env:STATIONS_ROOT\..\MANIFEST.json
- STATION_REGISTRY.json from pipeline-workflows repo
- WORKFLOW_REGISTRY.json from pipeline-workflows repo
- BIL relevance scores via GET $env:BIL_SERVER/bil/clipboard/predict

Actions:
- Approve → move file from REVIEW/ to OUTPUT/, log correction event
- Reject → move file to ERROR/kickout/, log correction event
- Reclassify → update FIS metadata, log correction event
- All corrections → POST to $env:BIL_SERVER/bil/signal with event_type="human_correction"
- Run workflow → call orchestrator.py with selected workflow
```

---

## ADD: Comms Tab (ui/tabs/comms_tab.py)

Embed the multi-AI communications hub.

```
- QWebEngineView loading $env:COMMS_HUB (https://comms.dlowehomelab.com)
- Or if offline: show last-known messages from local cache
- Refresh button
- Unread badge on tab header
- On session start: check unread automatically
```

---

## ADD: Knowledge Wiki Tab (ui/tabs/wiki_tab.py)

Browse the Theophysics knowledge wiki.

```
- Left panel: searchable entity list (from Postgres graph_nodes or vault index)
- Right panel: rendered markdown (QTextBrowser or QWebEngineView)
- Wikilinks are clickable → navigate within the tab
- Search bar with fuzzy matching
- Data source: $env:THEOPHYSICS_VAULT/wiki/ folder (markdown files)
- Fallback: query Postgres graph_nodes table
```

---

## ADD: BIL Integration (core/bil_client.py)

Lightweight client for the Behavioral Intelligence Layer.

```python
class BILClient:
    def __init__(self, base_url="http://localhost:8420"):
        self.base_url = base_url

    def post_event(self, endpoint, data):
        # POST to /bil/web, /bil/clipboard, /bil/signal
        pass

    def get_predictions(self):
        # GET /bil/clipboard/predict
        pass

    def get_status(self):
        # GET /bil/status
        pass

    def post_correction(self, correction):
        # POST /bil/signal with event_type="human_correction"
        pass
```

Wire into:
- Clipboard tab: every copy event → bil_client.post_event("/bil/clipboard", ...)
- Pipeline tab: every approve/reject → bil_client.post_correction(...)
- Search scraper tab: every search → bil_client.post_event("/bil/web", ...)

Signal weights (hardcoded in bil_client):
```
manual_approval: 1.0
file_reused: 0.9
copied_text: 0.8
bookmark_save: 0.7
long_dwell_scroll: 0.5
opened_tab: 0.2
accidental_visit: 0.0
```

---

## ADD: Pipeline Runner (core/pipeline_runner.py)

Thin wrapper that calls the pipeline-workflows orchestrator.

```
- Reads workflow JSON from $env:STATIONS_ROOT\..\pipeline-workflows\workflows\
- Calls orchestrator.py as subprocess
- Streams stdout to Pipeline tab log panel
- Updates MANIFEST.json on completion
- Can run in background thread (QThread) so GUI doesn't freeze
```

---

## MODIFY: app.py

Updated startup sequence:

```python
def main():
    # Settings
    settings = SettingsManager(...)
    settings.load()

    app = QApplication([])

    # First-run API key dialog (keep existing)

    # Core systems
    registry = CommandRegistry(...)
    vault = VaultManager(...)
    ai_manager = create_ai_manager_from_settings(settings)
    bil_client = BILClient(os.environ.get("BIL_SERVER", "http://localhost:8420"))

    # Hotkeys + hotstrings (keep existing)
    register_hotkeys(registry)
    hotstring_engine = HotstringEngine(registry)
    hotstring_engine.register_all()

    # Clipboard monitor (new — runs in-process)
    clipboard_monitor = ClipboardMonitor(bil_client)
    clipboard_monitor.start()

    # System tray (new)
    tray = ForgeTrayIcon(app, ...)

    # Main window (updated tab list)
    window = create_main_window(
        settings=settings,
        command_registry=registry,
        vault_manager=vault,
        ai_manager=ai_manager,
        bil_client=bil_client
    )

    # Minimize to tray on close
    window.closeEvent = lambda e: (window.hide(), e.ignore())

    tray.show()
    window.show()
    app.exec()
```

---

## MODIFY: main_window.py

Updated tab order:

```python
def _add_all_tabs(self):
    # 1. Pipeline (FORGE control panel) — the main event
    self.tab_widget.addTab(PipelineTab(...), "Pipeline")

    # 2. Chat (AI chat — existing)
    self.tab_widget.addTab(ChatTab(...), "Chat")

    # 3. Clipboard (restored + BIL integration)
    self.tab_widget.addTab(ClipboardTab(...), "Clipboard")

    # 4. Comms (multi-AI hub)
    self.tab_widget.addTab(CommsTab(...), "Comms")

    # 5. Prompts (existing)
    self.tab_widget.addTab(PromptsTab(...), "Prompts")

    # 6. Knowledge Wiki (new)
    self.tab_widget.addTab(WikiTab(...), "Wiki")

    # 7. Search (existing)
    self.tab_widget.addTab(SearchScraperTab(...), "Search")

    # 8. Shortcuts (existing)
    self.tab_widget.addTab(ShortcutsManagerTab(...), "Shortcuts")

    # 9. Settings (existing)
    self.tab_widget.addTab(SettingsTab(...), "Settings")
```

---

## MODIFY: config/settings.ini

Add FORGE sections:

```ini
[forge]
stations_root = X:\Backside\stations
models_root = X:\Backside\_models\_Models
vault_path = O:\_Theophysics_v4
pipeline_repo = C:\path\to\pipeline-workflows

[bil]
server = http://localhost:8420
enabled = true

[comms]
hub_url = https://comms.dlowehomelab.com
check_on_start = true

[postgres]
host = 192.168.1.97
port = 5432
database = theophysics
user = postgres
password = Moss9pep28$
```

---

## MODIFY: Window title

```python
self.setWindowTitle("FORGE — File-Oriented Research Graph Engine")
```

---

## TAB ORDER (final)

| # | Tab | Source | Status |
|---|-----|--------|--------|
| 1 | Pipeline | NEW | FORGE control panel |
| 2 | Chat | EXISTING | AI chat (Claude/OpenAI/DeepSeek) |
| 3 | Clipboard | RESTORED | Clipboard manager + BIL feed |
| 4 | Comms | NEW | Multi-AI comms hub |
| 5 | Prompts | EXISTING | Prompt picker + manager |
| 6 | Wiki | NEW | Knowledge wiki browser |
| 7 | Search | EXISTING | Search scraper |
| 8 | Shortcuts | EXISTING | Hotkey editor |
| 9 | Settings | EXISTING | Settings (extended with FORGE config) |

---

## CRITICAL RULES

- Do NOT rewrite existing working tabs. Extend them.
- Do NOT add a Python bridge server. Everything runs in-process.
- Do NOT add TTS. It's removed.
- Pipeline tab is tab 1 — it's the first thing David sees.
- Every user action that implies preference (approve, reject, copy, search) feeds BIL.
- Use QThread for background tasks (pipeline runs, BIL calls) so GUI never freezes.
- Use environment variables ($env:*) for paths. Fall back to settings.ini values.
- The `keyboard` library handles global hotkeys. Do not switch to pynput.
- Postgres password is in settings.ini, NOT hardcoded in source files.
- Window title is "FORGE" not "Stratum."