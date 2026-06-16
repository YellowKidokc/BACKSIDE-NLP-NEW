# Reading Levels

This folder holds generated reading-level outputs:

- `{stem}_ACADEMIC.md`
- `{stem}_EASY.md`
- `{stem}_TERM_INVENTORY.json`

This folder is partial until every one of the 61 source articles has all three files.

Run:

```powershell
powershell -ExecutionPolicy Bypass -File X:\WORKFLOWS\MDA-PUBLICATION\READING_LEVEL_GENERATOR\run_all_reading_levels.ps1 -UseMini
```

Then rebuild HTML:

```powershell
python X:\WORKFLOWS\MDA-PUBLICATION\05_HTML_BUILD\combine_mda_reader_html.py
```
