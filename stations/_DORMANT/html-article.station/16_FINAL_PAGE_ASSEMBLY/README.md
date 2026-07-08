# 16_FINAL_PAGE_ASSEMBLY

Purpose: assemble rendered blocks and workflow artifacts into one coherent article page payload.

## Inputs

- `11_HTML_RENDER/render-blocks.json`
- `03_YAML_METADATA/frontmatter.yaml`
- `08_SECTION_VECTORS/vector-metadata.json`
- `09_GRAPH_LINKS/graph-edges.json`
- `13_LAYER_LEDGER/layer-ledger.json`
- `12_EXPORTS/` supporting assets as needed

## Outputs

- `page-payload.json`
- `page-outline.md`
- `sample_output/article-assembly-preview.html`

## Notes

- this lane assembles the page payload
- it should not mutate station outputs
- it should keep audience-tier hooks available for readability switching
