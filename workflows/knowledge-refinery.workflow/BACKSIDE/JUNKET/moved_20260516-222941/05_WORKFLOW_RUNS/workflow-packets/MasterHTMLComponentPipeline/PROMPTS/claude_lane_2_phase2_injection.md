# Claude Lane 2: Phase 2 Injection Planner

Assignment: plan series navigation, audio/video, images, and support component injection for marked pages.

Inputs:

- `OUTPUT/component-inventory.json`
- available templates/assets
- target series

Return:

- injection target socket for each file
- component type/name to add or replace
- assets required
- whether the operation can be scripted safely
- script recommendation
- human review items

Rules:

- Prefer marked component sockets.
- Do not inject into raw HTML unless no marked socket exists.
- Do not apply writes; produce an injection plan only.
