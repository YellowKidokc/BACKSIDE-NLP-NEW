# Next Worker Prompt - FAP Article Pipeline

You are continuing FolderAutomationPipeline.

Read:

```text
X:\github\pipeline-workflows\workflows\FolderAutomationPipeline\README.md
X:\github\pipeline-workflows\workflows\FolderAutomationPipeline\CONFIG\article_manufacturing_line.json
X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\WORKFLOW_SPINE.md
```

A canary run has already passed:

```text
X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\output\20260513-081940_gtq-03-first-quantum-state\job_manifest.json
```

Your job:

1. Read the latest job manifest.
2. Inspect the queued station request files under `_queue\pending`.
3. Fill one station output at a time into `_review\<job_id>`.
4. Do not move files unless the prompt says APPLY WRITES.

Priority station outputs:

- executive summary
- explain it simply
- math translation
- contradiction check
- Bible reference check
- Master Equation / formal proof / axiom map
- axiom derivation echoes
- post summary

Return exact paths and PASS / REVIEW / FAIL.
