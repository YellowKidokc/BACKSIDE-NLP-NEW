# AI Hub / ClipSync / AHK Workflow

## What This Is

AI-HUB v2 is the local desktop edge for prompts, clipboard, links, hotkeys, and HTML panels.

The runtime copy lives here:

`C:\Users\lowes\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ai-hub-v2`

The GitHub/source copy lives here:

`D:\GitHub\physics-of-faith\ai-hub`

## Main Flow

1. `AI-HUB.ahk` starts AutoHotkey.
2. AutoHotkey starts `sync_server.py`.
3. `sync_server.py` serves the local API on `http://localhost:3456`.
4. Standalone HTML panels use that API:
   - Clipboard: `GET/POST /api/clips`
   - Prompts: `GET/POST /api/prompts`
   - Links/bookmarks: `GET/POST /api/bookmarks`
5. AHK reads `config\prompts.json` and registers slash shortcuts as hotstrings.

## Prompt To Slash Command

When the standalone prompt HTML saves a new prompt, the Python bridge now normalizes it:

- `content` becomes `template`
- `/name` or `meta.slash=true` becomes `shortcut`
- AHK watches `config\prompts.json` every 5 seconds
- New slash prompts become available without restarting AI-HUB

Example:

`/fixit` saved in the prompt HTML becomes an AHK hotstring. Typing `/fixit` pastes the saved prompt template.

## Backup And Sync

Backups now prefer the large backup drive:

`B:\AI-HUB-BACKUP`

If `B:` is unavailable, it falls back to:

`D:\AI-HUB-BACKUP`, then `C:\AI-HUB-BACKUP`

The live sync folder now prefers:

`B:\AI-HUB-SYNC`

and falls back to:

`D:\AI-HUB-SYNC`, then `C:\AI-HUB-SYNC`

Backup snapshots include:

- `config\settings.ini`
- `config\prompts.json`
- `config\hotkeys.ini`
- `config\hotstrings.sav`
- `config\storage.json`
- `config\sysprompts.json`
- `config\research_links.json`
- `Data\clipboard.db` and related SQLite files

## Cloudflare / PWA Relationship

The Cloudflare PWA is the installable/shared surface. The local desktop bridge is the Windows-only edge that can touch clipboard, local files, and AHK.

The clean pattern is:

Desktop HTML -> localhost bridge -> local config/Data -> AHK hotkeys

Cloudflare PWA -> remote API/storage -> shared phone/other-computer view

Anything that needs Windows clipboard or AHK must pass through the local bridge. Anything that needs phone/installable access should live in the Cloudflare/PWA layer.


