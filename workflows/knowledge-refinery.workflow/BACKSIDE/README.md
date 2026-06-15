# BACKSIDE (runtime + junket)

This folder is the **Backside runtime root** for Knowledge-Refinery.

<div style="display:flex;gap:10px;flex-wrap:wrap;margin:10px 0;">
  <span style="background:#0b5fff;color:#fff;padding:4px 10px;border-radius:999px;font-weight:700;">MODELS</span>
  <span style="background:#2da44e;color:#fff;padding:4px 10px;border-radius:999px;font-weight:700;">STATIONS</span>
  <span style="background:#8250df;color:#fff;padding:4px 10px;border-radius:999px;font-weight:700;">WORKFLOWS</span>
  <span style="background:#6e7781;color:#fff;padding:4px 10px;border-radius:999px;font-weight:700;">JUNKET</span>
</div>

Goal: keep only the **live runtime surfaces** obvious at the root, and push everything else into one non-destructive bucket.

## Root folders

- `MODELS/` = model wrappers + weights/caches (canonical location).
- `STATIONS/` = station system (scaffold + runners + registry).
- `WORKFLOWS/` = workflow routes that chain stations.
- `JUNKET/` = everything else (non-destructive holding pen; never delete, only move here).

## Current move bucket

- `JUNKET/moved_20260516-222941/` contains the prior lane tree that was removed from the root.

Next map: see `BACKSIDE_MAP.md`.

