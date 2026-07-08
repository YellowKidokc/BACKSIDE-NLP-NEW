# Axioms Paper Workflow

This folder is the working intake for paper scoring and axiom-facing outputs.

## Main Flow

1. Put `.txt`, `.md`, `.html`, or `.htm` papers in `00_INBOX_DROP_PAPERS_HERE`.
2. Run `RUN_AXIOMS_WORKFLOW.bat`.
3. Review reports in `01_OUTBOX_REPORTS`.
4. Open HTML reports from `02_HTML_OUTPUTS`.
5. Use `03_FINAL_READY\<series>\<paper>` when moving scored data into another series.
6. Originals are archived in `04_ARCHIVE_ORIGINALS`.

## Buttons

- `RUN_AXIOMS_WORKFLOW.bat` runs the whole intake.
- `TROUBLESHOOT_AXIOMS_WORKFLOW.bat` checks folders, Python, config, scripts, and reference HTML files.
- `UPDATE_AXIOMS_REFERENCE_HTML.bat` refreshes the required proof-explorer and paper-snapshot HTML outputs.

## Reference HTML Set

The required reference HTML outputs are kept in:

```text
papers\required_html_outputs_2026-05-11
```

and mirrored for quick browsing in:

```text
02_HTML_OUTPUTS\required_reference_outputs
```

These are the examples every future paper should pass through conceptually: axiom layers, closure, paper snapshot prototype, enhanced paper view, and the Genesis-to-Quantum black-axiom snapshot.

## Final Bundle Shape

Each scored paper gets `HTML`, `JSON`, `EXCEL`, `CLAIMS`, `MARKDOWN`, and `LOSSLESS_SUMMARY` folders under:

```text
03_FINAL_READY\<series>\<paper-id>
```
