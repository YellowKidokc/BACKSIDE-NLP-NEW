Build the first HTML render pass for this workflow lane.

Rules:

- consume section packets instead of reparsing the article
- produce renderable section blocks, not the full page shell
- keep workflow badges visible
- keep raw and translated math linkable to the correct section
- if required upstream artifacts are missing, mock them and document the mock

Deliver:

- `render-blocks.json`
- `render-blocks.md`
- one sample rendered HTML section in `sample_output/`
