# Theophysics Page Compiler

## Rule

The Markdown owns meaning. The registry owns features. The builder owns design. The HTML owns nothing.

## Purpose

This folder is the first scaffold for the feature-aware Markdown compiler described in the reading-layer architecture.
It prevents each article from becoming a one-off HTML hack.

## Flow

1. `scan_article.py`
   - Reads Markdown or HTML.
   - Detects known features.
   - Writes `feature_manifest.json`.

2. Future `tag_article.py`
   - Suggests feature tags.
   - Does not blindly rewrite source.

3. Future `validate_article.py`
   - Checks proposed tags against the registry.
   - Rejects unknown or unsafe placements.

4. Future `build_layers.py`
   - Pulls sidecars: easy, academic, claims, math.

5. Future `render_html.py`
   - Uses approved renderers only.
   - Produces final layered HTML.

6. Future `report_gaps.py`
   - Lists missing layers, unknown structures, and required review.

## Current Files

- `registry/site_feature_registry.json`
- `scan_article.py`

## Output Contract

Each scan writes:

```json
{
  "source_file": "...",
  "detected_features": {},
  "missing_optional_features": [],
  "unknown_patterns": [],
  "sidecar_candidates": {},
  "builder_gates": {}
}
```

The manifest becomes the truth source for the builder.
