# Chrome Plugin Audit - 2026-05-11

## Status

The extension now has a working HTML surface wired into Chrome:

- `popup.html` is the toolbar popup.
- `dashboard.html` is the full options/dashboard page.
- `popup.css`, `popup.js`, `dashboard.css`, and `dashboard.js` keep script and style concerns separate.
- `manifest.json` now points Chrome to the popup and options page.
- The popup now includes Brain capture actions and local stack health checks.

## Checks Run

- Manifest JSON parse: PASS
- JavaScript syntax check: PASS
  - `popup.js`
  - `dashboard.js`
  - `background.js`
  - `content.js`
- HTML structure check: PASS
  - `popup.html`
  - `dashboard.html`
- Brain capture syntax check: PASS
  - `background.js`
  - `content.js`
- BIL API check: OFFLINE at time of audit
  - `http://localhost:8420/bil/summary?limit=3` was not reachable.
  - The new HTML pages handle this with an offline state.

## Primary Files

- Load as Chrome extension folder: `X:\chrome-plugin`
- Toolbar UI: `popup.html`
- Full dashboard: `dashboard.html`
- Capture fallback download folder: `Downloads\BIL-session-handoffs`
- Older dashboard mockups retained:
  - `PREFERENCE_MACHINE_DASHBOARD.html`
  - `preference_engine_dashboard.html`

## Notes

The older HTML files still use inline scripts, which is fine if they are opened as standalone local mockups, but they are not the right files to use as Chrome extension pages. The new popup and dashboard use external JavaScript files so they fit Chrome extension rules better.
