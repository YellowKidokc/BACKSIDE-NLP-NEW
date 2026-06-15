# Run Prompt

Use the shared worker-5 runner.

```powershell
python ..\10_RIGOR\run.py
```

What it writes here:
- `sample_output/<paper-slug>/layer-ledger.json`
- `sample_output/<paper-slug>/section-pass-matrix.csv`

Why this is shared:
- the same stable `page_id` and `section_id` set must drive rigor, the ledger, and workbook append payloads
- keeping one runner avoids silent row drift across the three worker-5 deliverable surfaces
