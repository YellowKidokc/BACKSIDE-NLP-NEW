# Front And Center Approval Prompt

You are reviewing the Axiom Black Snapshot folder for the MDA publication packet.

Do not skim this folder and call it done. Your task is to read it coherently one time, confirm what is complete, confirm what is partial, and sign an explicit approval or hold.

## What This Folder Is

This folder is the black-panel inspection view for every MDA paper snapshot.

Start here:

`index.html`

That page links to one snapshot page per paper. Each page exposes:

- paper title and identity
- truth / coherence / chi metrics
- claim surface counts
- risky and supported sentences
- keyword chips from the graph overlay
- raw JSON snapshot references
- pipeline trace excerpts

## What This Folder Is Not

This is not the final proof gate.

This is not proof that every claim survived.

This is not proof that Easy and Academic versions are complete.

This is an inspection console. It tells you where the paper stands and where the next work is.

## Required Source Locations

Use these exact locations. Do not invent a second workspace.

### Main Export Packet

`X:\WORKFLOWS\MDA-PUBLICATION\09_EXPORT_PACKET`

Read:

- `00_READ_ME_FIRST.md`
- `EXPORT_MANIFEST.json`

### Lossless Article Spine

`X:\WORKFLOWS\MDA-PUBLICATION\09_EXPORT_PACKET\01_LOSSLESS_SOURCE\articles`

Original home:

`X:\WORKFLOWS\MDA-PUBLICATION\01_LOSSLESS\articles`

These are the Standard source articles.

### Reader HTML Build

`X:\WORKFLOWS\MDA-PUBLICATION\09_EXPORT_PACKET\03_READER_HTML`

Original build output:

`X:\WORKFLOWS\MDA-PUBLICATION\06_HTML_BUILD\reader_combined`

Build script:

`X:\WORKFLOWS\MDA-PUBLICATION\05_HTML_BUILD\combine_mda_reader_html.py`

### Reading Level Generator

Generator script:

`X:\WORKFLOWS\MDA-PUBLICATION\READING_LEVEL_GENERATOR\generate_reading_levels.py`

Batch runner:

`X:\WORKFLOWS\MDA-PUBLICATION\READING_LEVEL_GENERATOR\run_all_reading_levels.ps1`

Generated output home:

`X:\WORKFLOWS\MDA-PUBLICATION\05_READING_LEVELS`

Packet copy:

`X:\WORKFLOWS\MDA-PUBLICATION\09_EXPORT_PACKET\02_READING_LEVELS`

### Two-Lane OpenAI Reports

Packet copy:

`X:\WORKFLOWS\MDA-PUBLICATION\09_EXPORT_PACKET\07_TWO_LANE_OPENAI_REPORTS`

Original output:

`C:\Users\lowes\Documents\Codex\2026-05-30\okay-let-find-the-open-ai\outputs\deploy_ready_two_lane_openai_20260530`

Use these for math/isomorphism notes and attention/rhythm notes.

### Pipeline Analytics

Packet copy:

`X:\WORKFLOWS\MDA-PUBLICATION\09_EXPORT_PACKET\06_PIPELINE_ANALYTICS`

Original output:

`C:\Users\lowes\Documents\Codex\2026-05-30\okay-let-find-the-open-ai\outputs\deploy_ready_full_pipeline_20260530\paper_intelligence`

Important files:

- `paper_rows.json`
- Excel workbook
- knowledge graph JSON
- knowledge graph GraphML
- `snapshots\*_snapshot.json`

### Keyword Graph Overlay

Packet copy:

`X:\WORKFLOWS\MDA-PUBLICATION\09_EXPORT_PACKET\05_KEYWORD_GRAPH_OVERLAY`

Original output:

`C:\Users\lowes\Documents\Codex\2026-05-30\okay-let-find-the-open-ai\outputs\mda_keyword_graph_overlay_20260530`

Use this to explain why two papers connect. Do not treat lexical bridge terms as proof.

### Axiom Black Snapshot Generator

Script source:

`C:\Users\lowes\Documents\Codex\2026-05-30\okay-let-find-the-open-ai\work\build_mda_black_snapshot_html.py`

Original output:

`C:\Users\lowes\Documents\Codex\2026-05-30\okay-let-find-the-open-ai\outputs\mda_axiom_black_snapshots_20260530`

Packet copy:

`X:\WORKFLOWS\MDA-PUBLICATION\09_EXPORT_PACKET\04_AXIOM_BLACK_SNAPSHOTS`

## Approval Checklist

Before signing approval, verify:

- `index.html` opens.
- It links to individual paper pages.
- Paper pages show metrics, claims, risky/supporting sentences, and keywords.
- The folder does not imply Proof is complete.
- The packet README clearly says Easy/Academic are partial until all generated files exist.
- The scripts above are locatable.
- The next commands are clear.

## Required Signature

Write one of these at the top of your review result:

`APPROVED_FOR_NEXT_STAGE`

or

`HOLD_FOR_FIXES`

Then include:

```markdown
Reviewer:
Date:
Folder reviewed:
Approval status:
What is complete:
What is partial:
What must not be claimed yet:
Next required command:
Notes:
```

## Default Verdict If Unsure

If you are unsure, choose `HOLD_FOR_FIXES`.

Do not be nice. Be accurate.
