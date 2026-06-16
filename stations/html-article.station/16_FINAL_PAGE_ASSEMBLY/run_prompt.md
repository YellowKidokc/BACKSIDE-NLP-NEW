Assemble the final article page payload from previously rendered blocks.

Rules:

- do not re-grade or re-interpret the article here
- preserve metadata, tags, graph hooks, and readability hooks
- keep the page inspectable by both humans and downstream machines
- if assembly reveals missing required block families, write loopback and stop pretending the page is ready

Deliver:

- `page-payload.json`
- `page-outline.md`
- one preview HTML output in `sample_output/`
