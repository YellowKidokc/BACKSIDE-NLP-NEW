# Axioms

Axioms is the formal structure layer for paper decomposition, claim extraction, proof architecture, canonical mappings, and paper-grade outputs.

## Working Folders

- `00_INBOX_DROP_PAPERS_HERE` - drop `.txt`, `.md`, `.html`, or `.htm` papers here.
- `01_OUTBOX_REPORTS` - raw grader outputs.
- `02_HTML_OUTPUTS` - browser-ready HTML reports and required reference HTML outputs.
- `03_FINAL_READY` - per-series, per-paper bundles ready to reuse in another series.
- `04_ARCHIVE_ORIGINALS` - originals after successful grading.
- `05_MANIFESTS` - queue, update, and organizer manifests.
- `papers` - imported paper corpus and required reference snapshots.
- `claims`, `proofs`, `mappings` - downstream decomposition lanes.
- `scripts` - workflow code.

## Buttons

- `RUN_AXIOMS_WORKFLOW.bat` - refreshes required HTML references, grades the inbox, organizes outputs, renders one-page dashboard surfaces, runs the rigor gate, and pauses at the end.
- `QUEUE_IMPORTED_PAPERS_TO_INBOX.bat` - copies canonical imported papers into the inbox while skipping backup/system folders.
- `UPDATE_AXIOMS_REFERENCE_HTML.bat` - refreshes the proof-explorer and paper-snapshot HTML reference set.
- `TROUBLESHOOT_AXIOMS_WORKFLOW.bat` - checks folders, Python, config, scripts, reference HTML files, and optional vector services.

## Reference HTML Outputs

The required HTML outputs live in:

```text
papers\required_html_outputs_2026-05-11
```

and are mirrored into:

```text
02_HTML_OUTPUTS\required_reference_outputs
```

These are the reusable paper-processing views: axiom layers, closure, paper snapshot prototype, enhanced paper view, proof explorer index, and the Genesis-to-Quantum black-axiom snapshot.

## One-Page Snapshot Surface

Each graded paper can also render a dark one-page dashboard:

```text
03_FINAL_READY\<series>\<paper-id>\HTML\<paper-id>.paper-grade-dashboard.html
```

This is the fast visual snapshot surface for claims, equations, repair pressure, station marks, and any loaded snapshot metadata.

## Final Bundle Shape

Each scored paper gets its own folder:

```text
03_FINAL_READY\<series>\<paper-id>\
```

Inside that paper folder:

```text
HTML
JSON
EXCEL
CLAIMS
MARKDOWN
LOSSLESS_SUMMARY
```

For example, a Genesis-to-Quantum article becomes:

```text
03_FINAL_READY\Genesis-to-Quantum\gtq-01-measurement-collapsed-reality\
```
