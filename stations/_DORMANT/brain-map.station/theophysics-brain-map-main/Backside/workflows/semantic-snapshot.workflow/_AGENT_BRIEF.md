# Agent Brief - Semantic Snapshot Workflow

Mission: keep the source-to-Postgres semantic audit path visible and repeatable.

Do not collapse the independent stations into one script. The point is orchestration:

1. `first-article.workflow` creates canonical Markdown and per-article lossless packets.
2. `lossless_context_pipeline` assigns address, vector, hash, Master Equation UUID, semantic tags, and block anchors.
3. `chi-tagging.workflow` provides canon tag reference for `G,M,E,S,T,K,R,Q,F,C`.
4. `paper-proof-grader.workflow` grades and pressure-tests claims.
5. `axioms.workflow` surfaces axiom snapshot and rigor-gate review.
6. Postgres stores append-only audit snapshots and semantic tags.

When expanding this workflow, prefer adding station contracts and merge adapters over copying station logic.
