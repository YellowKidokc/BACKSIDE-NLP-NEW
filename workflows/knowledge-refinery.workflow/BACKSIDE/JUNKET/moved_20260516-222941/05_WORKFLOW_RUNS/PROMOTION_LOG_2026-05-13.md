# Promotion Log - 2026-05-13

Goal: bring D-drive workflow/source systems into X so the Brain/refinery runtime is in-house.

## Copied

- `D:\brain` -> `X:\knowledge-refinery\13_SOURCE_SYSTEMS\D_brain`
- `D:\C4C-wiki` -> `X:\knowledge-refinery\13_SOURCE_SYSTEMS\C4C-wiki`
- `D:\FAP` -> `X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP`
- `D:\GitHub\pipeline-workflows` -> `X:\github\pipeline-workflows`

## Runtime Packets Already Promoted

- `GTQArticlePublicRefinery`
- `MasterHTMLComponentPipeline`
- `KnowledgeRefineryBackplane`

Runtime home:

```text
X:\knowledge-refinery\05_WORKFLOW_RUNS\workflow-packets
```

## Blocked

`D:\C4C` was not copied because it is a broken junction:

```text
D:\C4C -> C:\O:\_ Theophysics_Case_for_Christ\
```

## Verification

`GTQArticlePublicRefinery` was smoke-tested from the X runtime path against GTQ-03 and produced output successfully.
