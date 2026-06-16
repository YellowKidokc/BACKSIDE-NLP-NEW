# Excel Notes

- CSV file: `X:\Backside\workflows\knowledge-refinery.workflow\BACKSIDE\STATIONS\STATION_OUTPUT_INVENTORY_20260524_excel_ready.csv`
- Station count: `64`
- Best first sort in Excel: `Group`, then `Order`.
- Best filter for quantitative surfaces: `Quant/Score? = Yes`.
- Most stations use the generic pair `result.json` + `result.md`; special output names are already preserved in the CSV.

## Suggested Sheet Views

- Full inventory
- NLP metrics only
- Reasoning / 7Q only
- Extraction / Conversion only
- Validation / Contradiction only
- Graph / Routing / Publish only

## Fast Filters

- `Group = NLP Metrics` gives the 15 obvious measurement-style stations.
- `Folder` in `7q_forward, 7q_reverse, 7q_evidence, claim_extractor, lossless_summary` gives the reasoning spine.
- `Folder` in `knowledge_graph, route_classifier, publication_gate` gives the downstream routing/export spine.
