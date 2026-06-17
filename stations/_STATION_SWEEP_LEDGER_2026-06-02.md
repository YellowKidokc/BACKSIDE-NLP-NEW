# Station Sweep Handoff Ledger — 2026-06-02

Operator: Claude (Opus 4.8). Scope: export-safety + wiring + cleanup pass on the
stations below. Status tags: **LIVE** (wired, verified, safe) ·
**REVIEW_LATER** (works but needs a human decision) · **CONTEXT_ONLY** (kept for
reference, not an active pipeline) · **DO_NOT_ARCHIVE** (must stay; do not zip/
ship/delete yet).

## Status table

| Station | Tag | State / what was done | Open item |
|---|---|---|---|
| apologetic-pipeline.station | LIVE | DEFAULT_OUTPUT → station `EXPORTS\`; audio scratch moved out of EXPORTS. Syntax-verified. | none |
| image-processor.station (06_IMAGES) | LIVE | Default output → `EXPORTS\`; logging fixed to honor config.log_dir (central `D:\brain\_LOGS`) instead of polluting shared `stations\_LOGS`. `.gitignore` added. | none (logging fix diverges from sibling scaffold — propagate later) |
| series-flow-auditor.station | LIVE | `12_EXPORTS` → `EXPORTS\`; loose root HTML artifacts → `EXPORTS\html_trace\`; RUN.bat rewired; smoke-run verified (md/json/csv/xlsx). | none |
| master-equation-canon.station | LIVE | Stale `OLD canonical\` source paths → `LEAN4\canonical\`; verified run = 4/4 sources, 0 skipped, 323 blocks. Exports stay **drive-global** `X:\EXPORTS\canon-index\` (convention). | David: add FORMAL_LAYER_PART2.md? |
| session-handoff-drop.station | LIVE | `OUTPUT\` → `EXPORTS\` (config updated); no-op run verified. | REVIEW_LATER: vault/NAS mirrors point at LOCAL stub folders, not real external paths |
| whisper-transcribe.station | LIVE | Relocated out of vault-rater to be a top-level sibling. Self-contained; NOT re-swept this pass. | REVIEW_LATER: run its own export-safety pass |
| vault-rater-tsr100.station | REVIEW_LATER / **DO_NOT_ARCHIVE** | Key scrubbed from config.txt; env-var + config.local.txt + .gitignore + template added; nested whisper station moved out; `--output` constrained under EXPORTS. | **BLOCKER: rotate/revoke the exposed key provider-side, then set new key via OPENAI_API_KEY. Do NOT zip/share/commit until rotated.** |
| session-handoff-combined.station | REVIEW_LATER | Empty stub — only `test.txt` ("hello"). Not scaffolded, not deleted. | David: build it out (mirror the drop station) or delete |
| brain-map.station | CONTEXT_ONLY | Map-layer repo clone (`theophysics-brain-map`). Created station-root `EXPORTS\` + pointer README; exports are **drive-global** `X:\EXPORTS\` by the repo's own EXPORTS_CONVENTION.md — deliberately NOT rewired. `4a-output/` is live workflow scaffolding (kept). 7Q: one canonical `seven-questions.station` + an identical vendored `seven_q_core.py` in `axiom-candidates.station` (keep separate). | none — do NOT rewire engines to per-station EXPORTS |
| link-pull.station | LIVE | `OUTPUT\` → `EXPORTS\` (folder renamed, run subfolders preserved; 3 config paths rewired). Fixed stale wiring: `PASTE_AND_RUN.bat` drop path → `%~dp0DROP_HERE`; `TROUBLESHOOT.md` `X:\captures\links\*` → station paths. Config-verified, no stale `OUTPUT` refs. | none |
| link-research.station | REVIEW_LATER | Registry marked `type:remote` → NAS `\\dlowenas\brain\Backside\apps\link-research-engine-main` (per the station's own REMOTE placeholder; registry had said `local`). Local engine/export/handoff files left **untouched** ("Do NOT copy files here"). `HANDOFF_BUNDLE/samples` are intentional byte-identical copies of `data/output`+`data/workbooks`. | David: retire/sync the local copy on the NAS; any export-centralization happens there, not locally |
| fruits-spirit-canon.station | LIVE | Added the **Fruits Coherence Engine** verbatim + wired launcher (`run_fruits_engine.py` / `RUN_FRUITS_ENGINE.bat`): `DROP_HERE\` → auto-discovered `LEXICON\` xlsx → `EXPORTS\fruits_reports\run_<ts>\` (json/md/4×csv/xlsx). Canon-index `station.py`/`RUN.bat` untouched (2 tools now). Smoke-tested (sample → B+, xlsx written). | none — David's `*.xlsx` lexicon/template sit at station root; optional move into `LEXICON\` |
| claim-extractor.station | LIVE | (sweep 3) Centralized exports to per-station `EXPORTS\` (json/excel/csv/source_copies); nested 7Q export folder hash-verified then archived; `config.output_dir` → `EXPORTS`; **EXTRACT.bat rewritten** portable (killed `D:\brain\08_CLAIMS\` + Desktop leaks), original at `_ARCHIVE\legacy_runners\`. One 7Q engine, no collisions. | none |
| harvest-links.station | LIVE (static) | (sweep 3) **Broken post-reorg imports fixed**: `pipeline.py` rewired off missing `ROOT\02_SBERT`-style paths to sibling stations via `TOOL_STATIONS` map (compile + static-resolve verified). Export leak fixed: `summary_csv` → per-station `EXPORTS\`; dead `config.log_dir` → `X:\Backside\_LOGS`; RUN.bat msg fixed; `__pycache__` removed. | David: live RUN.bat with Infinity/Qdrant/Postgres/DeBERTa up to confirm one CSV + DB/Qdrant side effects |
| postgres-sync.station (07_POSTGRES) | LIVE (static) | (sweep 3) Shared `db_utils` (6 importers). **Zero-lockout secret wiring** (David's call, exposure OK): password resolves env→multi-path `.env`→`config.json` literal; `.env` copied on-drive to `X:\Backside\.env`. Log dir → shared `X:\Backside\_LOGS`; per-station `EXPORTS\`; EXPORT/IMPORT examples de-stale'd; `__pycache__` removed. Compile + 3-source resolution verified. | David: run `db_utils test` against the live host to confirm auth |
| preference-engine.station | CONTEXT_ONLY | (sweep 3) **Intentional scaffold** — README says stub, RUN.bat deliberately exits code 2 until runtime exists; model artifacts live under `X:\Backside\_models\_Models\13–15`. No exports, no code to wire. Left untouched (no fabricated structure). | David: build logger/API/runtime here, or leave as placeholder |

## Protected roots — NOT touched this sweep
- `knowledge-refinery` — untouched.
- `brain` (incl. `D:\brain\...`) — untouched (image-processor code now *targets* `D:\brain\_LOGS` per its config, but it was not run, so nothing written there).
- `apps` — untouched. NOTE (sweep 2): the `link-research` registry entry now *references* `\\dlowenas\brain\Backside\apps\link-research-engine-main` as its canonical path, but **no file under `apps`/`brain`/`knowledge-refinery` was created, modified, or deleted** — only the registry JSON in `stations\` was edited.
- All writes this sweep were confined to: the twelve station folders above, `STATION_REGISTRY.json`, the verification artifact `X:\EXPORTS\canon-index-test\master-equation\`, `X:\Backside\_logs\` (drop run log), and the Claude memory index. (Sweep-2 fruits smoke-test output under `fruits-spirit-canon.station\EXPORTS\` was deleted after verifying.)

## Heavy / unfinished lanes — confirmed PARKED (untouched)
- Math translation layer (`math-translation-layer.station`, `math-layer.station`) — parked.
- File naming system — parked.
- OpenAI / vector / o3 — parked. (Sweep-2 note: the Fruits Coherence Engine is pure stdlib + `openpyxl`, no OpenAI/vector calls; vault-rater's existing OpenAI use is the station itself, not this lane.)
- Proof injection (`paper-proof-grader.workflow`) — parked (only read indirectly via series-flow-auditor's manifest content; no writes).

## Cross-cutting findings (worth a dedicated pass)
1. **Canon family stale sources:** every `*-canon.station` likely has the same `OLD canonical\` → `LEAN4\canonical\` break. The shared engine `_shared/canon_index.py` *silently skips* missing sources, so a broken station looks fine. Verify `summary.skipped_sources == []` after each run.
2. **Scaffold logging bug:** the shared `NN_NAME` scaffold writes logs to `parent\_LOGS` and ignores `config.log_dir`. Fixed only in image-processor so far.

## One external blocker before full GREEN
- Rotate the vault-rater-tsr100 API key (provider-side). Everything else is filesystem-clean.

## ⚠ SCOPE BOUNDARY — read before any cleanup
**This sweep assessed 12 of 49 stations. UNTAGGED ≠ DELETABLE.** A station/workflow
with no tag below means **"not assessed this sweep, RETAIN"** — it does NOT mean
"cruft." Do not bulk-archive, zip, or delete anything on the basis of a missing
tag. The only removals this entire sweep were verified temp/test artifacts
(noted inline). When in doubt, leave it and tag it REVIEW_LATER.

### Full station inventory (49 on disk)
Swept + tagged (16): `apologetic-pipeline`, `brain-map`, `claim-extractor`,
`fruits-spirit-canon`, `harvest-links`, `image-processor`, `link-pull`,
`link-research`, `master-equation-canon`, `postgres-sync`, `preference-engine`,
`series-flow-auditor`, `session-handoff-combined`, `session-handoff-drop`,
`vault-rater-tsr100`, `whisper-transcribe`. (sweep 3 added: claim-extractor,
harvest-links, postgres-sync, preference-engine.)

NOT swept — UNTAGGED = NOT ASSESSED, RETAIN (33): `7q-classifier`, `7q-engine`,
`ai-portal-generator`, `ai-research-agents`, `axioms`,
`classify-documents`, `deberta-runner`, `file-intelligence`, `graph-linker`,
`hdbscan-cluster`, `html-article`, `math-layer`,
`math-translation-layer`, `mda-publication`, `metadata-extractor`,
`obsidian-export`, `open-brain-map`, `operators-canon`, `paper-grader-nlp`,
`paper-intelligence-suite`, `paper-proof-grader`, `paper-recommender`, `paperqa2`,
`readability-rewriter`, `sbert-embedder`,
`section-splitter`, `summarizer`, `theophysics-engine`, `transcribe-and-classify`,
`trinity-canon`, `youtube-fetch`, `youtube-qa`, `youtube-scrape`.
NOTE: sweep 3 added an on-drive secrets copy `X:\Backside\.env` (from `D:\brain\.env`,
read-only) — `D:\brain` itself remains write-untouched.
(`math-layer` + `math-translation-layer` are the PARKED math lane — retain.)

### Non-`.station` folders at stations root — RETAIN (not cruft)
`Treaties/`, `_shared/` (shared engine code — many stations import it),
`axioms/`, `lossless_context_pipeline/`, `ollama/`, `overview_generator/`.

### Workflows on disk — RETAIN
`X:\Backside\workflows\`: `chi-tagging.workflow`, `first-article.workflow`,
`knowledge-refinery.workflow` (⚠ touches the PROTECTED `knowledge-refinery` root —
do not run/clean), `semantic-snapshot.workflow`, `youtube-qa.workflow`.
⚠ Stray: `X:\Backside\EXPORTS\semantic-snapshot.workflow` — a workflow def nested
under EXPORTS. REVIEW_LATER (likely misplaced); do NOT delete — confirm vs the
`workflows\` copy first.

### Registry ↔ disk gaps — DO NOT auto-resolve by deleting
Registry has 52 entries; disk has 49 folders. Mismatches are naming/form, not losses:
- `vault-rater` (registry key) ↔ `vault-rater-tsr100.station` (disk) — name mismatch; a name-keyed reconcile would falsely see both as orphan+missing.
- `lossless-context` (registry) ↔ `lossless_context_pipeline/` (disk, no `.station`).
- `treaties` (registry) ↔ `Treaties/` (disk).
- `hybrid-7q-rigor` — registry-only, no folder on disk (remote/planned?). Needs a human; do not purge the entry.

## Final pass sign-off (2026-06-02, sweep 2)
- [x] **Every SWEPT workflow tagged** — all 12 assessed stations carry LIVE / CONTEXT_ONLY / REVIEW_LATER / DO_NOT_ARCHIVE. The other 37 are listed above as UNTAGGED = NOT ASSESSED = RETAIN (explicitly not deletable).
- [x] **Protected roots clean** — no writes under `knowledge-refinery`, `D:\brain`, or `apps` (the `link-research` registry only *points* at the apps path; `knowledge-refinery.workflow` left untouched).
- [x] **Parked lanes still parked** — math-translation-layer, file-naming system, OpenAI/vector/o3, proof-injection: untouched.
- [x] **No bulk cleanup performed** — only verified temp/test artifacts removed. Registry↔disk gaps recorded, NOT auto-resolved. Full 49-station inventory written so nothing depends on memory.
- [x] **Ledger saved** — this file + the `sweep-ledger-2026-06-02` memory index entry.
- **Status: GREEN to hand off — within the 12-station scope.** Standing external action: vault-rater key rotation. The 37 untagged stations + workflows + registry gaps are a *future* assessment lane, not a cleanup target. Nothing blind; nothing vanishes on a missing tag.
