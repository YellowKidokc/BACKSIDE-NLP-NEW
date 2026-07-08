# obsidian-export.workflow

Manifest-driven Obsidian export and canon routing layer for X-drive artifacts.

Current scope is intentionally narrow:

- one paper snapshot: `GTQ-17`
- one YouTube Q/A artifact: `sample-apologetics-dialogue`

No bulk routing is enabled in this manifest.

## Explicit GTQ-17 Split

GTQ-17 has two canon outputs on purpose:

- `03_SERIES/GTQ/gtq-17-ran-the-numbers.md`
  - the human article or series-facing note
- `06_ADVERSARIAL_LAYER/Paper_Grader_PDS1/GTQ-17-Ran-the-Numbers-Paper-Snapshot.md`
  - the audit and proof-grader artifact note

These are separate routes in `routing_manifest.json` and must cross-link to each other. Do not collapse them into one note, and do not infer the route from filename alone.

## What it does

1. Reads a routing manifest with explicit source artifacts and canon targets.
2. Renders clean Markdown notes with YAML frontmatter.
3. Validates:
   - YAML frontmatter presence and required keys
   - `source_path` exists and matches the route source artifact
   - `content_hash` matches the source artifact hash
   - wikilinks are syntactically balanced
4. Stages validated notes under this workflow root.
5. Copies validated notes into `\\dlowenas\z obsidian\_ __THEOPHYSICS_CANON`.
6. Refuses to overwrite an existing target note unless the content is identical.
7. Keeps GTQ-17 split into explicit `03_SERIES` and `06_ADVERSARIAL_LAYER` outputs from the same snapshot source.

## Files

- `routing_manifest.json` — explicit route list
- `scripts/export_obsidian_notes.py` — exporter, validator, and router
- `01_STAGING_NOTES\` — validated notes before route copy
- `02_VALIDATION_REPORTS\` — JSON run reports
- `03_ROUTED_NOTES\` — local copy of note text that was routed

## Run

```powershell
RUN.bat
```

Optional single-route run:

```powershell
RUN.bat --route-id gtq17-paper-snapshot
```

Series-only rerun:

```powershell
RUN.bat --route-id gtq17-series-note
```
