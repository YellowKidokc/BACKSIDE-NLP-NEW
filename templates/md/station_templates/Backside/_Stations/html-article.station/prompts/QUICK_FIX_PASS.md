# Quick Fix Pass — Post-Cowork Review

You are fixing 6 specific issues identified by the Cowork review pass.
Read `configs/COWORK_REVIEW_PASS.md` first for full context.

Workflow root: `X:\Backside\workflows\html-article.workflow`

## Fix List (do these in order)

### Fix 1: M-4 — Pick canon for pipeline_order
- `configs/lane_registry.json` pipeline_order is CANON.
- Open `configs/MOVEMENT_AND_TRACE_CONTRACT.md`, add a header line: `# HISTORICAL — pipeline_order in lane_registry.json is canon. This document is retained for reference only.`
- Do NOT delete the file.

### Fix 2: M-1 + M-2 — Add ID helpers to shared_lib/ids.py
Add three functions to `configs/shared_lib/ids.py`:

```python
def section_id(ordinal: int, heading_text: str) -> str:
    """Canonical section_id format. All lanes MUST use this."""
    return f"sec-{ordinal:03d}-{slugify(heading_text)}"

def paper_uuid(source_path: str, content_hash: str) -> str:
    """Canonical paper UUID. All lanes MUST use this."""
    return stable_uuid("doc", source_path.lower(), content_hash[:16])

def page_id(paper_uuid_str: str) -> str:
    """Canonical page ID. All lanes MUST use this."""
    return f"page::{paper_uuid_str}"
```

### Fix 3: M-3 — Lane 04 must use shared_lib.semantic_hash
- Open `04_TAGS/contract.json`
- Ensure `semantic_hash` implementation field references `configs/shared_lib/address.py semantic_hash()`
- Check `04_TAGS/run_prompt.md` — if it hand-rolls the hash format, replace with instruction to call shared_lib

### Fix 4: M-5 — Fix state vs status in lane 03
- Open `03_YAML_METADATA/contract.json`
- Separate: `state` = address V-component (D/W/F), `status` = lifecycle (draft/review/published)
- Default `status` to `draft` when source doesn't declare
- Update `03_YAML_METADATA/run.py` if it conflates the two

### Fix 5: M-6 — Lane 02 source offsets
- Open `02_SECTION_MAP/run.py`
- Find where sections are emitted
- Add `source_offset_start` and `source_offset_end` to each section dict
- These should capture the character offset of the heading and the start of the next heading (or EOF)

### Fix 6: M-8 — Lane 13 ledger output
- Check if `13_LAYER_LEDGER/sample_output/` has `layer-ledger.json`
- If not, either run the worker-5 runner to generate it, OR update `13_LAYER_LEDGER/contract.json` to note that the ledger lives inside `10_RIGOR/rigor-report.json` for round 1

## Rules
- Do NOT redesign anything.
- Do NOT touch lanes you weren't assigned.
- Post to workflow-4 when done: `[cli-fix] Quick fix pass complete. Fixed: M-1, M-2, M-3, M-4, M-5, M-6, M-8. Files changed: [list].`
