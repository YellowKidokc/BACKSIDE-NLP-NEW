# HTML Article Workflow - Process Briefs

These are the current process intentions for the missing or newly promoted lanes.

## Section Map

Goal: produce stable section boundaries and `section_id` values.

Needs:

- heading detection
- hierarchy
- equation attachment
- citation attachment

## YAML Metadata

Goal: create page-level and section-level metadata without overloading tags.

Needs:

- extracted fields
- inferred fields
- front matter candidate
- machine metadata JSON

## Tags

Goal: attach lightweight semantic, law, variable, and workflow tags.

Needs:

- page tags
- section tags
- confidence or origin notes

## Claims

Goal: extract and packetize claims at section level.

Needs:

- explicit claims
- implied claims
- support-needed flags

## Contradictions

Goal: identify tensions and contradictions inside the article and against known structures.

Needs:

- contradiction edges
- challenge ledger
- review queue

## Math Translation

Goal: translate equations into faithful readable language and mark whether math has already been processed.

Needs:

- raw math
- translated math
- confidence
- loopback trigger when translation breaks meaning

## Section Vectors

Goal: embed every section as a reusable machine object.

Needs:

- `section_id`
- vector payload
- vector metadata

## Graph Links

Goal: generate edges from claims, vectors, variables, and tags.

Needs:

- edge type
- confidence
- source and target ids

## Rigor

Goal: apply 7Q, fact verification, and contradiction pressure.

Needs:

- readiness score
- kill conditions
- evidence gaps

## Layer Ledger

Goal: record which lanes each section has passed through.

Needs:

- section-by-section pass state
- timestamps
- status
- reviewer notes

## Loopback Review

Goal: send broken or questionable outputs back upstream.

Needs:

- reason for rejection
- upstream lane to revisit
- concrete fix request

## Readability Rewrite

Goal: support audience-tier switching on the website.

Needs:

- author-level version
- accessible version
- academic version
- preserved term ledger
