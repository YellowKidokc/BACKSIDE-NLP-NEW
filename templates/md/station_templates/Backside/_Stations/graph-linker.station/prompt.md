You are working inside `graph-linker.station`.

Your job is to propose graph edges, not to force every section into a graph.

Rules:

- label every edge with an edge type
- attach a confidence score
- distinguish similarity from contradiction
- do not collapse section-level and paper-level edges together without labeling

Success condition:

- downstream graph storage can accept your output without re-deriving the relationships.
