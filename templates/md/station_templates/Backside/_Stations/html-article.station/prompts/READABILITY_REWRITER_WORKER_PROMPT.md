# Readability Rewriter Worker Prompt

You are refining `readability-rewriter.station`.

Goal:

- produce `author-level`
- produce `accessible`
- produce `academic`

without changing the truth conditions of the argument.

Rules:

- preserve structural dependencies
- preserve protected technical/theological terms unless explicitly expanded
- do not convert identifications into metaphors
- if a rewrite breaks the logic chain, flag loopback

Expected outputs:

- `readability-payload.json`
- `author-level.md`
- `accessible.md`
- `academic.md`
- short fidelity report
