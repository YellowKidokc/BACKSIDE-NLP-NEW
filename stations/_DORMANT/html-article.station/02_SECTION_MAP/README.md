# 02_SECTION_MAP

Owner: worker-1 (claude-code) — Round 1.

## What this lane does

Splits a source document (HTML or Markdown) into ordered, stable, addressable sections. Produces the section ledger that every later lane joins against.

This lane is the keystone for section-level work. If section_ids drift, every downstream packet (tags, claims, vectors, math, rigor) drifts with them.

## What it consumes

Order of preference:

1. `01_LOSSLESS/{article}/normalized-text.md` if 01 has already run for this article
2. `00_DROP/{article}.html` raw HTML
3. `00_DROP/{article}.md` raw Markdown

If 01 is missing (Round 1 case), this lane reads the raw drop directly and notes that in the section-map header. Documented per work-order assumption #5 (mock or read upstream).

## What it produces

For each article, under `02_SECTION_MAP/{article-slug}/`:

- `section-map.json` — machine-readable section ledger (the canonical artifact)
- `section-map.md` — human-readable mirror with heading tree + counts
- `section_packets/{section_id}.md` — per-section text packets for downstream consumers

The packets folder is a working preview. The formal cross-lane section bundle is owned by `15_SECTION_PACKETS` once all wave-1 lanes have run.

## Section detection rules (deterministic-first)

HTML inputs:

- Every `<section id="...">` becomes a structural container. Its id is captured as `source_anchor`. The container itself is not a section node unless it carries a heading.
- Every `<h1>` through `<h6>` opens a new section node. `heading_level` = the tag number.
- `heading_path` is the chain of ancestor headings at shallower levels, with the current heading appended. The h1 is the root.
- A section spans from the byte immediately after its opening heading to the byte immediately before the next heading at same-or-shallower level, or to the end of its containing `<section>`, whichever comes first.
- Equations: count of `$...$` and `$$...$$` pairs, plus `<math>` and MathJax `\(...\)` / `\[...\]` constructs.
- Citations: count of `<sup>` runs, `<cite>` elements, and `\[\d+\]` markers in the spanned text.

Markdown inputs:

- ATX headings (`#`, `##`, `###`, etc.) open sections at their level.
- A leading content block before any heading is captured as `sec-001-intro` with `inferred=true` if no explicit heading exists.
- YAML frontmatter is excluded from section text but its presence is recorded in the header block of `section-map.json`.

Inference:

- Any boundary that is not anchored to an explicit heading or `<section id>` is flagged `inferred=true` with a one-line `inferred_reason`.
- If inferred boundaries exceed 10% of total sections, the lane writes a loopback artifact to `14_LOOPBACK_REVIEW`.

## section_id rules

- Format: `sec-{ord:03}-{slug(heading_text)}`. Ordinal is the global 1..N source order.
- `stable_uuid` is derived via `configs/shared_lib/ids.stable_uuid('section', paper_uuid, slug(heading_path), str(ordinal))`. Downstream lanes should prefer `stable_uuid` for storage joins; `section_id` is the human-readable handle.
- Headings that collide at the same `heading_path` after slugging gain a `-2`, `-3` suffix on the slug. The numbering is by source order.

## Pass markers

For each section, this lane sets:

```json
"passes": {
  "section_map": {"status": "passed", "timestamp_utc": "...", "worker": "worker-1"},
  "math_translation": {"status": "pending"},
  "claims":           {"status": "pending"},
  "vectors":          {"status": "pending"},
  "rigor":            {"status": "pending"}
}
```

Downstream lanes mutate their own pass slot only.

## How to run

```
python run.py --in 00_DROP/gtq-03-free-will-two-frames.html --out 02_SECTION_MAP/gtq-03
python run.py --in 00_DROP/CALIBRATION_pilot-preflight-checklist.md --out 02_SECTION_MAP/CALIBRATION
```

If a partner is running the lane via prompt rather than code, they should use `run_prompt.md` and emit the same JSON shape.

## Calibration result (expected vs produced)

`CALIBRATION_pilot-preflight-checklist.md` produces exactly 4 sections, matching `configs/CALIBRATION_EXPECTED.md`:

| ordinal | heading_text | inferred |
|---------|--------------|----------|
| 1 | Pilot Pre-Flight Checklist (intro) | false (h1 explicit) |
| 2 | Checklist | false |
| 3 | Kill Condition | false |
| 4 | Risk | false |

See `sample_output/CALIBRATION_section-map.json`.

## Known gaps / drift to flag

1. `01_LOSSLESS` is empty in Round 1. This lane reads raw HTML directly. When 01 lands, route should swap to its output.
2. `lane_registry.json` v2 overloads 02 into "Categorize + Address" with PDS station. The Round 1 work order (msg 1156) and `CALIBRATION_EXPECTED.md` both keep 02 narrow (section structure) and put `vector + semantic_address + hash` into 04. This lane executes the narrow contract. Codex/Opus to reconcile registry — see workflow-4 status post.
3. Inferred-boundary loopback is implemented but the loopback artifact schema is owned by 14_LOOPBACK_REVIEW; this lane writes a stub and points to 14.

## Files in this folder

- `contract.json` — formal contract
- `README.md` — this file
- `run.py` — deterministic Python runner (stdlib only)
- `run_prompt.md` — AI fallback prompt
- `sample_output/` — calibration + GTQ-03 outputs (partial for GTQ-03; full for calibration)
