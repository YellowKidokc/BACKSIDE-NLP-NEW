# 13_LAYER_LEDGER

Purpose: make page/section pass state explicit so the workflow never has to guess which lanes have touched an artifact.

Current approach:
- treat `layer-ledger.json` as canonical
- mirror the same pass state into `section-pass-matrix.csv`
- keep upstream gaps visible as `pending` with notes, rather than inventing fake passes

Current runner:
- the shared worker-5 runner lives in `..\10_RIGOR\run.py`
- that runner writes ledger outputs here because rigor, layer ledger, and workbook append alignment are one lane family for this round

Known gaps:
- this lane is source-only unless upstream packets appear in the workflow tree
- no workbook file is created here; instead, aligned append payloads are written into `12_EXPORTS/sample_output/`
