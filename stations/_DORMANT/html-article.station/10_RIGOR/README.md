# 10_RIGOR

Purpose: produce a testable rigor packet and readiness decision without forking the schema.

What this lane does:
- preserves `paper_uuid`, `page_id`, and `section_id` as the stable identity surface
- records whether the rigor pass used real upstream packets or a documented source-only fallback
- leaves the 7Q and DeBERTa hooks explicit instead of pretending those model-backed passes already ran

What this runner does right now:
- reads the calibration markdown and GTQ HTML source from `00_DROP/`
- writes `rigor-report.json`, `rigor-report.md`, and `readiness-decision.json`
- emits aligned side outputs for `13_LAYER_LEDGER` and `12_EXPORTS`

Known gaps:
- no live `deberta-runner.station` was found in the current station tree
- the available `7q-classifier.station` is not invoked from this packet; this round focuses on stable contracts and row identity
- if upstream lanes later ship real packets, rerun `run.py` so the readiness payload can upgrade from mocked input to actual lane evidence

Run:

```powershell
python .\10_RIGOR\run.py
```
