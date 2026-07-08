# Series Math Packet Workflow

Purpose: inventory every math item in a series so David can translate from one review packet, then move completed translations into the MTL Excel workbook.

This station does not generate translations. It only collects math and prepares review/intake rows.

## Input

Series HTML root, for example:

`\\dlowenas\HPWorkstation\Desktop\Master HTMl\_____ KIMI WORKFLOW\canonical\site\moral-decline`

## Outputs

Each run writes a timestamped folder under:

`X:\Backside\stations\math-translation-layer.station\exports\series-math-packets\`

Inside each run:

- `series_math_review_packet.html` - printable one-paper packet grouped by article/page
- `series_math_inventory.csv` - detailed extraction ledger
- `excel_intake_rows.csv` - rows shaped like the MTL Excel workbook
- `manifest.json` - run summary

## Command

From:

`X:\Backside\stations\math-translation-layer.station`

Run:

```cmd
RUN_SERIES_MATH_PACKET.cmd
```

## Human Workflow

1. Run the packet.
2. Open `series_math_review_packet.html`.
3. Translate the rows that actually need MTL support.
   Required fields are `easy` and `audioSafe`.
   `standard` and `academic` are optional compatibility fields.
4. Paste or merge the completed rows into:

`X:\Backside\stations\math-translation-layer.station\data\math_translation_table_updated_1.xlsx`

5. Export the completed Excel to website JSON from the Kimi workflow:

```cmd
scripts\RUN_export_mtl.cmd
```

## ID Rule

The final Excel `id` must match article `data-eq-id`, unless the workbook/exporter gets an explicit alias column.

Do not guess id mappings.
