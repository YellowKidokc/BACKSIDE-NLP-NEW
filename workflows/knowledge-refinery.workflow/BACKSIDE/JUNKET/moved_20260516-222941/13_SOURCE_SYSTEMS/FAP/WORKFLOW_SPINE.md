# FAP Workflow Spine

This is the missing workflow spine David was looking for.

```text
intake
-> classified
-> media-routed
-> lossless
-> vectorized
-> graded
-> axiom-mapped
-> output
```

Support lanes:

```text
_queue
_review
_rejected
logs
wiki
wiki-compiler
```

## Why It Matters

`lossless` is the AI website / AI portal preservation lane. It should become the canonical handoff shape before vectorization, grading, axiom mapping, and public packaging.

## Control Plane

```text
X:\github\pipeline-workflows\workflows\FolderAutomationPipeline
```

Runtime:

```text
X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP
```

## Click Launcher

```text
X:\RUN_FAP_ARTICLE_PIPELINE.bat
```

This runs the current manufacturing line:

```text
intake -> classified -> media-routed -> lossless -> vectorized -> graded -> axiom-mapped -> output
```

It also queues review/model station requests for executive summary, explain-it-simply, math translation, contradiction check, Bible reference check, Master Equation mapping, axiom/derivation review, Axiom Rigor Protocol, 7Q forward pass, 7R reverse pass, 7E evidence pass, decision-tree/swap-test review, and post summary.
