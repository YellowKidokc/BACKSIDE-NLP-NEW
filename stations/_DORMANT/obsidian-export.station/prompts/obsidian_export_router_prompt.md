Canon vault root:
`\\dlowenas\z obsidian\_ __THEOPHYSICS_CANON`

Important:
Do not write directly into the canon folders until the note passes validation.
First export to:
`X:\Backside\stations\obsidian-export.station\02_OBSIDIAN_NOTES\`

Then generate a routing manifest:
`X:\Backside\stations\obsidian-export.station\04_REPORTS\canon_routing_manifest.json`

Routing rules:

- Series/article notes -> `03_SERIES\`
- Canonical theory/framework notes -> `01_CANON\` or `04_FRAMEWORKS\`
- Physics-law/math notes -> `02_PHYSICS_CORE\`
- Philosophy of science notes -> `03_PHILOSOPHY_OF_SCIENCE\`
- Evidence notes -> `05_EVIDENCE\`
- Objections/counterarguments -> `06_ADVERSARIAL_LAYER\`
- Publication-ready notes -> `07_PUBLICATION_TRACK\` or `07_PUBLISH\`
- Media/video transcript Q&A notes -> `09_MEDIA\`
- Templates -> `09_TEMPLATE_ENGINE\`
- Uncertain notes -> `10_HOLDING_BAY\`

Validation before routing:

- YAML frontmatter present and parseable.
- `id`, `type`, `source_path`, `content_hash`, and `tags` present.
- No raw JSON dump as the body.
- Wikilinks are valid Markdown.
- Source artifact path exists.
- File has deterministic stable name.
- Destination folder exists.
- If destination is uncertain, route to `10_HOLDING_BAY`.

After validation:

- Copy, do not move, clean Markdown into the canon destination.
- Never overwrite a canon note unless `content_hash` changed and a backup/version is made.
- Write a route report listing:
  - source note
  - destination note
  - route reason
  - validation status
  - backup path if overwritten
  - warnings

Test mode:

- Use GTQ-17 only.
- Do not bulk-route the whole vault yet.
