# Start Here

The new Chrome plugin UI files are in this folder:

- `popup.html` - the small toolbar popup
- `dashboard.html` - the full dashboard page
- `OPEN_DASHBOARD.bat` - opens the dashboard directly

If you already loaded this extension in Chrome, Chrome will not show the new popup until you reload it:

1. Open `chrome://extensions`
2. Turn on Developer mode
3. Find `Bill - Behavioral Intelligence Layer`
4. Click Reload
5. Click the puzzle-piece icon in Chrome
6. Pin `Bill - Behavioral Intelligence Layer`

Then the toolbar popup should appear.

The popup now has:

- `Capture Page` - captures the current page into a markdown handoff.
- `Capture Selection` - captures selected text when available.
- `Health` - checks BIL, Ollama, Qdrant, and Infinity.
- `Dashboard` - opens the full dashboard page.

Capture behavior:

- If BIL is running and accepts `http://localhost:8420/bil/handoff`, the capture is sent there.
- If BIL is offline, Chrome downloads a markdown file under `Downloads\BIL-session-handoffs`.

If you only want to see the dashboard right now, run:

`OPEN_DASHBOARD.bat`

If you do not see **Bill - Behavioral Intelligence Layer** anywhere on `chrome://extensions`, it is not loaded yet.

Run:

`INSTALL_OR_RELOAD_EXTENSION.bat`

Then click **Load unpacked** and select the whole folder:

`X:\chrome-plugin`

Do not select `dashboard.html`, `popup.html`, or any single file.

After this update, Chrome may ask for one new permission: downloads. That is used only for the offline markdown fallback.
