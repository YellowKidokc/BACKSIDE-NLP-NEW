# BACKSIDE MAP

Legend (colors match `README.md` pills):

- **MODELS** (blue): workers/wrappers (what runs).
- **STATIONS** (green): steps (what gets done).
- **WORKFLOWS** (purple): routes (what order it runs in).
- **JUNKET** (gray): anything not part of runtime (kept, not deleted).

## One-sentence topology

`WORKFLOWS → STATIONS → MODELS → artifacts`

## Quick entrypoints

- Stations orientation: `X:\knowledge-refinery\BACKSIDE\STATIONS\READ_FIRST.md`
- Station inventory snapshot: `X:\knowledge-refinery\BACKSIDE\STATIONS\STATION_INVENTORY.md`
- Station registry (auto-generated): `X:\knowledge-refinery\BACKSIDE\STATIONS\stations_registry.yml`
- Excel outputs spec (analysis/substrate lanes): `X:\knowledge-refinery\BACKSIDE\STATIONS\EXCEL_OUTPUT_SPEC_MZ.md`

## Tidy rule

If a folder/file is not part of:

- `MODELS/`
- `STATIONS/`
- `WORKFLOWS/`

…it belongs in `JUNKET/` (move, don’t delete).

