You are working inside `metadata-extractor.station`.

Extract metadata that helps both humans and machines use the page later.

Rules:

- Prefer exact extraction over clever guessing.
- Distinguish `extracted`, `derived`, and `inferred`.
- Keep YAML compact.
- Put deeper machine structure in JSON, not in front matter.

Success condition:

- the final HTML page can expose page metadata cleanly and the workflow can use the JSON for routing and indexing.
