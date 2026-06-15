# 04_TAGS — Run Prompt (LLM First Pass)

Use this prompt to run lane 04 on any article in `00_DROP/`. Round-1 implementation is LLM-driven; round-2 will wire `7q-classifier.station` (or a tag-classifier sibling) for deterministic execution.

---

## Setup

You are running lane **04_TAGS** of the HTML article workflow. Your output feeds `09_GRAPH_LINKS`, `10_RIGOR`, and `15_SECTION_PACKETS`. Stay in lane.

Read first (in order):
1. `\\dlowenas\brain\Backside\workflows\html-article.workflow\configs\SEMANTIC_ADDRESS_AND_ROUTING.md`
2. `\\dlowenas\brain\Backside\workflows\html-article.workflow\configs\ARTICLE_OUTPUT_REGISTRY.md` (sections 5 + 4A)
3. `\\dlowenas\brain\Backside\workflows\html-article.workflow\04_TAGS\contract.json`
4. `\\dlowenas\brain\Backside\workflows\html-article.workflow\04_TAGS\README.md`
5. The Master Equation, 10 variables, and 10 Laws from canon channel.

## Inputs to load

- `02_SECTION_MAP/section-map.json` (or mock from raw drop if absent)
- `03_YAML_METADATA/frontmatter.yaml` + `metadata.json`
- `01_LOSSLESS/normalized-text.md`
- The raw drop file under `00_DROP/` for ground truth.

If upstream is missing: split the raw drop file on `^#{1,4}\s+` headings, assign section_ids as `sec_{ordinal:02d}_{slug(heading)}`, and set `tags.json.provenance.mocked = true`.

## Per-section task

For each section, emit a list of `SemanticTag` objects. The schema is `configs/shared_lib/schemas.py:SemanticTag`:

```json
{
  "tag_id": "stable_uuid('tag', page_id, section_id, tag_type, label)",
  "tag_type": "chi_var|law|axiom|master_eq|workflow|domain_badge|series|seven_q",
  "label": "human-readable tag (e.g. 'Law_4 — Yukawa/Fruits' or 'chi_K')",
  "block_id": "section_id (or block_id when finer than section)",
  "source_quote": "the exact span in the section that triggered the tag",
  "chi_vars": ["chi_K"],
  "master_equation_uuid": "<uuid if master_eq tag, else empty>",
  "meta": {"confidence": 0.0_to_1.0, "rule": "keyword|inferred|llm"}
}
```

Tag types to emit:

| tag_type | When |
|---|---|
| `chi_var` | Section invokes a Master Equation variable (G/M/E/S/T/K/R/Q/F/C). Use chi_X label. |
| `law` | Section names or operates on a Law (Law_1 … Law_10). |
| `axiom` | Section cites an axiom from the 188 or 22-PUB corpus. Label = axiom id. |
| `master_eq` | Section invokes `C_i = A_i · log_2(1 + T_i / D_i)` or the full Master Equation. |
| `workflow` | Surface gates: needs-math, needs-citation, needs-rigor, needs-evidence, kill-condition, operational, story, calibration-input. |
| `domain_badge` | Per `shared_lib/schemas.py:DomainBadge` plus AVIATION/SAFETY/PROCEDURE if applicable. |
| `series` | Series membership (GTQ, 7Q, MDA, Cross-Domain). |
| `seven_q` | Q0–Q7 lens triggered by the section. |

## Page-level task

Emit a page tag block:

```json
{
  "paper_uuid": "<from upstream metadata.json>",
  "page_id": "<from section-map.json>",
  "tags": [ ...SemanticTag list spanning all sections... ],
  "dominant_chi_vars": ["chi_K","chi_T","chi_G","chi_M","chi_R"],
  "dominant_laws": [],
  "domain_badges": ["AVIATION","SAFETY","PROCEDURE"],
  "vector_recomputed": "G3M3E0S0T3K3R3Q0F0C0",
  "vector_from_lane_02": "<from section-map or metadata>",
  "address_status": "MATCH|DRIFT|MOCKED",
  "provenance": {
    "mocked": false,
    "lane": "04",
    "run_id": "<UTC iso>",
    "worker": "claude-code-worker-2"
  }
}
```

## Vector recompute (consistency gate)

Use `configs/shared_lib/address.py`:

```python
from configs.shared_lib.address import score_vector, vector_string, semantic_hash
vec = score_vector(block_types, domain_count, entity_count, full_text)
vstring = vector_string(vec)   # "G3M3E0..."
vhash = semantic_hash(vec)
```

If `vstring != section_map.vector_string`: write `14_LOOPBACK_REVIEW/04_tags_loopback.json` with both vectors, the deltas, and a short note.

## Outputs to write

| File | Format |
|---|---|
| `04_TAGS/tags.json` | All page + section tags, plus provenance and vector status. |
| `04_TAGS/section-tags.csv` | Flat rows matching `contract.json.excel_columns`. |
| `04_TAGS/page-tag-summary.md` | Human-readable rollup: top 10 tags, dominant chi vars, dominant Laws, drift status. |
| `04_TAGS/semantic-address.json` | `{address, vector_string, hash, status: MATCH|DRIFT|MOCKED}` |

## Calibration check (run BEFORE GTQ-03)

Input: `00_DROP/CALIBRATION_pilot-preflight-checklist.md`

Expected outputs (from `configs/CALIBRATION_EXPECTED.md`):

- Recomputed vector: `G3M3E0S0T3K3R3Q0F0C0`
- Semantic address: `AVIATION/PILOT_PRE_FLIGHT_CHECKLIST/F/TEAM/I/R4`
- Domain badges: `AVIATION, SAFETY, PROCEDURE`
- No `Law_X` tags (this is not a Theophysics article — calibration only)
- Workflow tags should include `operational`, `kill-condition`, `calibration-input`
- `C` must be 0 — checklists are organized but not synthesizing. If you produce C=3, your run drifted.

If sample output does not match calibration: do not advance to GTQ-03. Fix the run prompt or upstream input first.

## Reporting

Post to comms `workflow-4`:
```
[claude-code-worker-2] Lane 04 Tags — STATUS: testable. Sample output in 04_TAGS/sample_output/calibration/. Vector match: G3M3E0S0T3K3R3Q0F0C0 == expected. Drift: none. Known gaps: <list>.
```

If blocked, name exactly what is missing.
