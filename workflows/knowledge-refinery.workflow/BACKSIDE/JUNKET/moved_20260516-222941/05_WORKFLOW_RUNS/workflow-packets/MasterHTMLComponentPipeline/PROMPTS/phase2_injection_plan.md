# Phase 2 Injection Plan Prompt

You are preparing marked public HTML pages for Phase 2 enrichment.

Inputs:

- PAGE_META
- component inventory
- target series nav template
- available audio/video/image assets
- requested injection type

Decide the safest insertion point using existing markers. Prefer replacing or filling a marked component over raw string insertion.

Return:

- target component socket
- proposed injected component type/name
- dependencies
- risk level
- whether human review is required before apply
- exact script or station that should run next
