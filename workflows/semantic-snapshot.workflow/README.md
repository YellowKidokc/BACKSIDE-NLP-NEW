# Semantic Snapshot Workflow

**Purpose:** one front door that stitches the article/lossless/tag/axiom/paper-grader stack into a visible operating surface.

This workflow does not replace the independent stations. It indexes them, verifies their expected locations, and writes a current snapshot map so a paper can move through:

```text
source HTML/Markdown
-> first-article.workflow
-> canonical Markdown
-> lossless artifact
-> Master Equation UUID
-> semantic tags
-> chi/canon tag reference
-> paper-proof-grader
-> axiom snapshot / rigor gates
-> Postgres append-only audit memory
```

## Why This Exists

The new identity layer is not just a filename. Each article receives:

- Nabla address: `D/N/V/A/U/R :: VECTOR :: HASH`
- `master_equation_uuid`
- stable block IDs
- claim/evidence/equation/kill IDs
- semantic tags tied back to block IDs

That packet is what lets Markdown, HTML, Excel, Postgres, the paper grader, and the axiom snapshot all point to the same semantic object.

## Run

```powershell
python X:\Backside\workflows\semantic-snapshot.workflow\pipeline.py
```

Or use:

```text
X:\RUN_SEMANTIC_SNAPSHOT_WORKFLOW.bat
```

## Outputs

```text
X:\EXPORTS\semantic-snapshot.workflow\<run_id>\
  semantic-snapshot-map.md
  semantic-snapshot-map.html
  semantic-snapshot-map.json
  00_STATION_SHORTCUTS\
```

## Location Rule

The paper grader stays as its own shared workflow:

```text
X:\Backside\workflows\paper-proof-grader.workflow
```

It is too central and too heavy to bury inside the first-article workflow. The semantic snapshot workflow calls it by contract and links to it.
