# AAA Export Templates

This folder contains export workbook templates.

- `BRAIN_EXPORT_TEMPLATE.xlsx` is the target shape for website-focused exports.
- The exporter writes the `AAA_Website_Payload` sheet with one row per section and two payload fields:
  - `Website Payload JSON` (machine-read JSON)
  - `Website Payload Markdown` (human-readable)
- For each payload row, the JSON includes:
  - `rewrites.grade_8_markdown`
  - `rewrites.academic_markdown`
  - `lossless_summary`
  - `stats` (tokens + claim/evidence/contradiction counts)
