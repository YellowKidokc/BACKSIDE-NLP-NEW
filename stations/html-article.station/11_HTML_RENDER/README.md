# 11_HTML_RENDER

Purpose: turn validated section/page packets into renderable HTML blocks without owning the final page assembly.

## Inputs

- `15_SECTION_PACKETS/`
- `03_YAML_METADATA/metadata.json`
- `04_TAGS/tags.json`
- `07_MATH_TRANSLATION/math-payload.json`
- `10_RIGOR/rigor-report.json`
- optional `13_LAYER_LEDGER/layer-ledger.json`

## Outputs

- `render-blocks.json`
- `render-blocks.md`
- `sample_output/rendered-section.html`

## Notes

- this lane renders blocks, not the whole site shell
- it should preserve workflow badges during stabilization
- math, tags, and rigor badges must remain inspectable

## Known Gaps

- no final template binding yet
- no shared component library wired yet
