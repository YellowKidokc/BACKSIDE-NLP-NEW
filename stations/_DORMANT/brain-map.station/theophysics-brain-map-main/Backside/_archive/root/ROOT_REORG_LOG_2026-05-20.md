# X Drive Root Reorg Log - 2026-05-20

Started: 2026-05-20T12:15:39.6146489-05:00

## Moves
- MOVED: `X:\_brain_DEPRECATED_20260516` -> `X:\Backside\_archive\root\_brain_DEPRECATED_20260516` (Deprecated root material)
- MOVED: `X:\00_CONVERSION` -> `X:\Backside\_archive\root\00_CONVERSION` (Legacy conversion staging)
- MOVED: `X:\_LOGS` -> `X:\Backside\_logs_MERGE_20260520-121539` (Root logs)
- MOVED: `X:\captures` -> `X:\Backside\_state\captures` (Capture state)
- MOVED: `X:\digests` -> `X:\Backside\_state\digests` (Digest state)
- MOVED: `X:\embeddings` -> `X:\Backside\_state\embeddings` (Embedding cache)
- MOVED: `X:\ratings` -> `X:\Backside\_state\ratings` (Rating state)
- MOVED: `X:\models` -> `X:\Backside\_models\downloaded` (Downloaded model weights)
- MOVED: `X:\Backside\models` -> `X:\Backside\_models\legacy-model-layer` (Existing model wrappers and scripts)

## Deferred
- DEFER path-sensitive: `X:\knowledge-refinery`
- DEFER path-sensitive: `X:\paper-proof-grader`
- DEFER path-sensitive: `X:\link-pull-drop`
- DEFER path-sensitive: `X:\ai-portal-generator`
- DEFER path-sensitive: `X:\axioms`
- DEFER path-sensitive: `X:\Preference Engine Build`
- DEFER path-sensitive: `X:\github`
- DEFER path-sensitive: `X:\ollama`
- DEFER path-sensitive: `X:\C4C`
- DEFER path-sensitive: `X:\C4C-wiki`
- DEFER path-sensitive: `X:\FAP`
- DEFER path-sensitive: `X:\BIL`
- DEFER path-sensitive: `X:\proof-architecture`
- DEFER path-sensitive: `X:\proof-explorer`

## Verification
- Low-risk move pass completed: 2026-05-20T12:15:41.4596599-05:00

## Pass 2 - corpus/control/export/service moves 2026-05-20T12:16:54.9451296-05:00
- MOVED: X:\BIL -> X:\Backside\corpus\BIL (BIL corpus placeholder/lane)
- MOVED: X:\C4C -> X:\Backside\corpus\C4C (C4C corpus)
- MOVED: X:\C4C-wiki -> X:\Backside\corpus\C4C-wiki (C4C wiki corpus)
- MOVED: X:\FAP -> X:\Backside\corpus\FAP (FAP source corpus/scaffold)
- MOVED: X:\github -> X:\Backside\control-plane\github (Repo mirror shelf)
- MOVED: X:\Preference Engine Build -> X:\Backside\control-plane\Preference Engine Build (Preference engine control-plane)
- MOVED: X:\theophysics-comms-hub -> X:\Backside\control-plane\theophysics-comms-hub (Comms hub control-plane)
- MOVED: X:\ollama -> X:\Backside\services\ollama (Local Ollama service scripts)
- MOVED: X:\proof-architecture -> X:\EXPORTS\proof-architecture (Publish/output sink)
- MOVED: X:\proof-explorer -> X:\EXPORTS\proof-explorer (Publish/output sink)
- Vectorization queue: X:\Backside\_state\vectorization_queue\root-corpus-moves-20260520.csv

## Pass 3 - workflow moves 2026-05-20T12:17:26.2514556-05:00
- MOVED: X:\knowledge-refinery -> X:\Backside\workflows\knowledge-refinery.workflow (Live knowledge refinery workflow runtime)
- MOVED: X:\paper-proof-grader -> X:\Backside\workflows\paper-proof-grader.workflow (Live paper proof grader workflow runtime)
- MOVED: X:\link-pull-drop -> X:\Backside\workflows\link-pull.workflow (Live link pull workflow runtime)
- MOVED: X:\ai-portal-generator -> X:\Backside\workflows\ai-portal-generator.workflow (Live AI portal generator workflow runtime)
- MOVED: X:\axioms -> X:\Backside\workflows\axioms.workflow (Live axioms workflow runtime)

## Final root verification 2026-05-20T12:18:01.8768458-05:00
- ROOT: #recycle
- ROOT: ARCHITECTURE.md
- ROOT: Axiom Workflow.txt
- ROOT: Backside
- ROOT: BACKSIDE_ARCHITECTURE.md
- ROOT: Conversions
- ROOT: David
- ROOT: EXPORTS
- ROOT: FOLDER_CONVENTIONS.md
- ROOT: GUI
- ROOT: README.md
- ROOT: RUN_FAP_ARTICLE_PIPELINE.bat
- ROOT: RUN_PUBLIC_ARTICLE_REFINERY.bat
- ROOT: THEOPHYSICS_PRIMER.md
- Root README refreshed to new front-door contract.

## Pass 4 - root document cleanup 2026-05-20T12:18:18.9387718-05:00
- MOVED DOC: X:\Axiom Workflow.txt -> X:\David\maps-and-notes\root-cleanup-20260520\Axiom Workflow.txt
- MOVED DOC: X:\BACKSIDE_ARCHITECTURE.md -> X:\David\maps-and-notes\root-cleanup-20260520\BACKSIDE_ARCHITECTURE.md
- MOVED DOC: X:\FOLDER_CONVENTIONS.md -> X:\David\maps-and-notes\root-cleanup-20260520\FOLDER_CONVENTIONS.md

## Final verification after document cleanup 2026-05-20T12:18:29.0526104-05:00
- ROOT: #recycle
- ROOT: ARCHITECTURE.md
- ROOT: Backside
- ROOT: Conversions
- ROOT: David
- ROOT: EXPORTS
- ROOT: GUI
- ROOT: README.md
- ROOT: RUN_FAP_ARTICLE_PIPELINE.bat
- ROOT: RUN_PUBLIC_ARTICLE_REFINERY.bat
- ROOT: THEOPHYSICS_PRIMER.md

## GUI promotion 2026-05-20
- COPIED FROM REPO: D:\GitHub\theophysics-brain-map\Backside\brain_dashboard -> X:\GUI\brain-dashboard
- ADDED: X:\GUI\brain-dashboard\RUN.bat
- VERIFIED: python -m pytest tests passed from X:\GUI\brain-dashboard
- VERIFIED: brain-dashboard --headless-smoke-test exited cleanly from X:\GUI\brain-dashboard
- VERIFIED: visible Brain Dashboard launched from X:\GUI\brain-dashboard\RUN.bat
