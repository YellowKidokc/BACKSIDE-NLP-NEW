# MasterHTMLComponentPipeline

Public HTML production workflow for pages that follow Kimi's component marking standard.

This packet is the control-plane home for Master HTML extraction, replacement, injection, and production status reporting. It does not replace the Master HTML workspace; it gives David and future AI partners a stable command layer over it.

## Source Anchors

- Marking standard: `\\dlowenas\HPWorkstation\Desktop\Master HTMl\_KIMI-READ-FIRST\HTML-MARKING-STANDARD.md`
- Curated script bundle: `\\dlowenas\HPWorkstation\Desktop\Master HTMl\Scripts\HTML Master Workflow`
- Local imported scripts: `SCRIPTS\imported\html_master_workflow`

## Operating Model

The marked HTML comment pairs are the sockets:

```html
<!-- BEGIN:COMPONENT:sidebar:sidebar-toc -->
...
<!-- END:COMPONENT:sidebar:sidebar-toc -->
```

The scripts in this packet should be used to discover, extract, replace, or inject those sockets without hand-editing every page.

## Stages

1. `INVENTORY`: scan marked HTML, PAGE_META, component pairs, and data-component attributes.
2. `EXTRACT`: pull one component type/name across pages into reviewable files.
3. `REPLACE`: replace a marked component with an approved template.
4. `INJECT`: add series nav, media, images, glossary, or article support blocks where markers exist.
5. `VERIFY`: confirm matched BEGIN/END pairs, PAGE_META, and required components.
6. `REPORT`: emit JSON/CSV status for PySide6 snapshot view.

## Safety

Default behavior must be dry-run. Any operation that writes files should require `--apply` and should write backups or route originals into `ARCHIVE`.

## GUI Target

The PySide6 GUI should call these scripts instead of embedding workflow logic. The GUI should show:

- source folder and selected files
- PAGE_META and component inventory
- current stage per file
- dry-run diff/review status
- output and error lanes
- script stdout/stderr logs
- approve/apply controls

## Imported Script Groups

- `01_one_pass_html`: GTQ transforms, component labels, topbar, media, navigation, series polish, web index.
- `02_paper_body_generation`: formal paper HTML generation and legacy generators.
- `03_tts_export_helpers`: TTS injection and markdown export.
- `04_sorting_triage`: canonical sorting and HTML triage.
