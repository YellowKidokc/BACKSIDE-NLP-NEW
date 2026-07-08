# HTML Article Workflow - Swarm Execution Prompt

Use this prompt when handing one of the HTML article lanes to an AI partner.

## Core Objective

You are not redesigning the architecture. You are refining one lane inside the existing HTML article workflow.

Workflow root:

`\\dlowenas\brain\Backside\workflows\html-article.workflow`

Station root:

`\\dlowenas\brain\Backside\stations`

## Global Rules

- Keep the lane atomic.
- Do not silently rename architecture.
- If you find a structural problem, write it down explicitly instead of freelancing a new topology.
- Prefer machine-readable outputs.
- Preserve source traceability.
- Every section is a first-class unit, not just the whole page.
- Loopback is allowed and expected. If your lane detects a failure upstream, write a review artifact into `14_LOOPBACK_REVIEW`.

## Lane State Contract

Every lane should be able to answer:

- what came in
- what was produced
- what confidence level applies
- what failed
- what should happen next

If you do not know the final implementation yet, define the contract first.

## Required Per-Lane Outputs

At minimum, propose or produce:

- one JSON contract
- one human-readable Markdown note
- one list of downstream dependencies
- one list of loopback conditions

## Current High-Value Lanes

- `02_SECTION_MAP`
- `03_YAML_METADATA`
- `04_TAGS`
- `05_CLAIMS`
- `06_CONTRADICTIONS`
- `07_MATH_TRANSLATION`
- `08_SECTION_VECTORS`
- `09_GRAPH_LINKS`
- `10_RIGOR`
- `11_HTML_RENDER`
- `13_LAYER_LEDGER`
- `14_LOOPBACK_REVIEW`

## How To Work

1. Read the lane folder name and infer the lane goal narrowly.
2. Check whether a station already exists that should own the atomic work.
3. If the lane is orchestration-only, define the handoff contract rather than embedding logic everywhere.
4. Write the minimal schema and prompt needed to make the lane usable by the next partner.
5. Do not overbuild UI or code before the contract is clear.

## For Math Translation

- treat math as a revisitable lane
- expose whether the section has passed through math translation
- record the raw math, translated math, and confidence note
- if the translation seems structurally wrong, send it to loopback instead of blessing it

## For Readability Rewrites

- write at least two audience modes
- preserve structural meaning
- never fake simplification by removing the actual argument

## Deliverable Shape

Your result should help the next AI partner start immediately, not decode your intentions.
