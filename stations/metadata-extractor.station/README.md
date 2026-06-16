# metadata-extractor.station

## Purpose
Extracts YAML-ready metadata from a document: title, author, date, subject, law mappings, variable references, equation count, citation count, reading level, word count.

## Input
- Section-mapped document (output of section-splitter)
- Optional: existing YAML to merge/update

## Output
- YAML front matter block
- JSON metadata object
- Tag suggestions (separate from YAML — tags stay lightweight)

## Model Dependencies
- 02_embedder (topic classification)
- 09_claim_extract (claim count)
- Optional: 06_llm via Ollama for complex classification

## Workflow Lanes
- 03_YAML_METADATA (primary)
- 04_TAGS (tag generation subset)

## Status: SKELETON — needs implementation

## Notes
Must produce Obsidian-compatible YAML front matter.
Must detect Theophysics-specific metadata: which Laws referenced, which chi variables present, which axioms invoked.
Tag layer should be separable — tags are lightweight classifiers, YAML is structured metadata.
