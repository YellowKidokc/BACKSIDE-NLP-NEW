# 02_SECTION_MAP — Run Prompt (AI fallback)

Use this prompt only if `run.py` is not available in your environment. The deterministic Python runner is the preferred path. Stay aligned to `contract.json` field names exactly.

## Inputs

You are given ONE source file path. Read it.

If it is HTML, parse the visible body. If it is Markdown, parse from the line after the YAML frontmatter block.

## Task

Produce two files under `02_SECTION_MAP/{article-slug}/`:

1. `section-map.json` — full machine ledger.
2. `section-map.md` — heading tree mirror.

Plus per-section files under `section_packets/{section_id}.md` containing only the section text body.

## Rules

- Preserve source order. Ordinals are global, 1..N.
- Every `<h1>..<h6>` opens a section at that level. ATX headings in Markdown work the same way.
- `<section id="...">` is a container, not a section node. Capture its id as `source_anchor` on every section node nested inside it.
- `heading_path` is the chain of ancestor headings at shallower levels plus the current heading.
- If a section has no explicit heading (intro before first heading, or content gap), open one with `inferred=true` and `heading_text` derived from the first 5 non-stopword tokens. Set `inferred_reason`.
- Do NOT rewrite text. Excerpts in the JSON should be the literal first 200 characters of the section body.
- Equations: count `$...$` pairs, `$$...$$` blocks, `<math>`, `\(...\)`, `\[...\]`.
- Citations: count `<sup>` runs, `<cite>` tags, and `\[\d+\]` patterns in the body.

## Field names (mandatory, do not invent synonyms)

For each section emit:

```
section_id, stable_uuid, ordinal, heading_level, heading_text,
heading_path (list of strings), parent_section_id, source_anchor,
source_offset_start, source_offset_end, inferred, inferred_reason,
equation_count, citation_count, word_count, text_excerpt,
packet_path, passes
```

`section_id` format: `sec-{ord:03}-{slug(heading_text)}`. Slugify lower-cases, replaces non-alphanumerics with `-`, strips edges.

`stable_uuid` is a UUIDv5 against namespace `28282828-0000-0000-0000-000000000001` over the string `section::{paper_uuid}::{slug(heading_path)}::{ordinal}`.

`passes` is the fixed dict shape in README.md, with `section_map.status="passed"` and all other lanes pending.

## Output JSON shape

```json
{
  "lane_id": "02",
  "lane_name": "Section Map",
  "article_slug": "...",
  "paper_uuid": "...",
  "source_file": "00_DROP/...",
  "source_kind": "html|markdown|lossless",
  "generated_at_utc": "...Z",
  "worker": "worker-1",
  "section_count": N,
  "equation_count_total": N,
  "citation_count_total": N,
  "inferred_section_count": N,
  "sections": [ { ...as above... } ],
  "loopback": { "triggered": false, "reasons": [] }
}
```

## Loopback triggers

If you detect any of these, write a stub to `14_LOOPBACK_REVIEW/02_section-map_loopback.json` and set `loopback.triggered=true` in your output:

- Inferred sections exceed 10% of total.
- Same `heading_path` appears more than once with no ancestor disambiguation.
- A heading_level jumps by more than 1 (e.g. h2 → h4) and there is no `<section>` ancestor.
- Equation count differs from the raw `$`-pair count by more than 2.

## When done

Post to workflow-4:

```
[worker-1] Lane 02 Section Map — STATUS: testable. Article: {slug}. Sections: {N}. Inferred: {n}. Loopback: {true|false}. Sample: 02_SECTION_MAP/{slug}/section-map.json
```
