# X:\ Brain Consolidation + Front-Door / Intake-Engine Restructure

## Context

David opened X:\ and wants three things long-term:

1. **Root simple.** Open X:\ and it feels paste-or-click obvious. Today there are 21 items at root and a confusing nested `X:\brain\` subfolder that looks like a duplicate "second brain."
2. **A robust front door per NLP.** Drop a file in and the NLP either figures out what it is or reroutes it — not "you have to know which folder."
3. **An automated intake engine on the backside.** Today every NLP is a manual `.bat` click. No watcher, no router.

Plus a consolidation directive: **everything that deals with X drive lives on X drive.** Specifically pull in `D:\BIL`, `D:\C4C-wiki`, `D:\C4C`, `D:\FAP`.

Structure will evolve — David explicitly said it'll keep changing. Plan should make the *next* shape better, not chase a perfect end state.

## David's revised sequencing (2026-05-16)

After reading the first cut, David re-ordered the work. His staging:

1. **First, get everything onto X:** (consolidation — D:\ targets in, `X:\brain\` flattened).
2. **Then, redundancy sweep** — no duplicates left across X:.
3. **Then, push everything-except-the-NLPs to GitHub.** The high-level organization, maps, READMEs, automation scripts should live online so they're accessible and version-controlled. The NLPs themselves (model weights, output data, vault content) stay off git.
4. **Then, the nitty-gritty** — renaming all the batch-script paths after NLPs move, locking the front-door convention, building the intake engine. **David said this part should be delegated to cloud AIs via prompts ("more manageable through cloud programming than you yourself"), not done by me directly.** My job here is to map it cleanly so the prompts can be written.
5. The high-level map (`THEOPHYSICS_WORKFLOW_MAP.md` and friends) **goes online** — that's the artifact that travels with him.

This plan is reorganized to that sequence. The original front-door/intake-engine designs are preserved as Phase 4+ — they're the "lock-it-down" target state that gets prompted out to cloud AIs once the foundation is clean.

---

## Current State (verified 2026-05-16)

### What's at X:\ root (21 items)

A partial cleanup happened **2026-05-13** that built the bones of David's vision but didn't finish it. The skeleton already exists:

- `X:\David\` — human-facing maps/notes (has `README.md` + `maps-and-notes/`)
- `X:\00_WORKFLOWS\` — workflow lanes + shared scripts + healthcheck infrastructure
- `X:\Backside\` — archive zone (NOT yet an intake engine; it's leftovers + scratch + a chrome-plugin app)
- `X:\README.md` — already describes the human-front-door pattern
- `X:\RUN_PUBLIC_ARTICLE_REFINERY.bat` + `X:\RUN_FAP_ARTICLE_PIPELINE.bat` — two click buttons

But the 9 active NLPs and pipeline-data folders still sit at root, parked there for compatibility:
`ai-portal-generator`, `axioms`, `knowledge-refinery`, `link-pull-drop`, `ollama`, `paper-proof-grader`, `proof-architecture`, `proof-explorer`, `session-handoff-drop` — plus `captures/`, `digests/`, `embeddings/`, `models/`, `ratings/`, `github/`, `_LOGS/`, `brain/`, `#recycle/`.

### The X:\brain\ nest (the duplicate confusion)

`X:\brain\` is a subfolder created by the 2026-05-13 migration. It contains 10 items, 5 of which **duplicate** folders that also exist at X:\ root. Live-vs-stale verdict (mtimes + file counts):

| X:\brain\ folder | X:\ root sibling | Verdict |
|---|---|---|
| `C4C/` (2,495 files, 678 MB) | — | **Promote** — only copy of the Obsidian Case-for-Christ vault |
| `C4C-wiki/` (844 files) | — | **Promote** — identical to D:\C4C-wiki, no root copy |
| `FAP/` (27 files, empty scaffold) | — | **Promote** — identical to D:\FAP, no root copy |
| `ollama/` (3 files) | `X:\ollama\` (empty dir) | **Promote** — brain copy is the live one |
| `ai-portal-generator/` | `X:\ai-portal-generator/` | **Drop brain copy** — root is newer (config.json hash differs) |
| `link-pull-drop/` (8 files) | `X:\link-pull-drop/` (9 files) | **Drop brain copy** — root is newer |
| `paper-proof-grader/` (205 files) | `X:\paper-proof-grader/` (498 files, May-14) | **Drop brain copy** — root is 3 days newer, 2× larger |
| `_LOGS/` (12 files, thru 5/11) | `X:\_LOGS/` (16 files, thru 5/14) | **Drop brain copy** — root is live |
| `theophysics-comms-hub/` (1 file) | `X:\theophysics-comms-hub/` (1 file) | **Drop brain copy** — identical |

### Per-NLP "front door" — pattern divergence

Every NLP invented its own intake-folder name:

| NLP | Intake folder name |
|---|---|
| `knowledge-refinery` | `00_INTAKE/` (most structured — 13-stage `00_INTAKE` → `13_SOURCE_SYSTEMS`) |
| `axioms` | `00_INBOX_DROP_PAPERS_HERE/` |
| `paper-proof-grader` | `INPUT/` AND `DROP_PAPERS_HERE/` (dual, inconsistent) |
| `link-pull-drop` | drops to `X:\captures\links\DROP_HERE/` (external to NLP folder) |
| `session-handoff-drop` | `DROP_HERE/` |
| `ai-portal-generator`, `proof-architecture`, `proof-explorer` | none (builder / static-output pattern) |

No shared standard. No NLP currently runs a classifier on dropped content.

### Backside intake engine — does not exist

- No `FileSystemWatcher`, no `watchdog`, no `Register-ObjectEvent`, no scheduled task watching drop folders.
- Each NLP self-orchestrates via its own `RUN_*.bat`.
- `X:\Backside\` is a cleanup-archive zone (README dated 2026-05-13), not running anything.
- `X:\00_WORKFLOWS\` has a healthcheck (`RUN_WORKFLOWS_HEALTHCHECK.bat`) and a `THEOPHYSICS_WORKFLOW_MAP.md` — closest thing to orchestration, but doesn't watch folders.

### D:\ consolidation targets (per David's directive)

| D:\ path | State on D: | State on X: | Action |
|---|---|---|---|
| `D:\C4C` | **Symlink** to `O:\_ Theophysics_Case_for_Christ\` — not real data | `X:\brain\C4C\` (2,495 files, already migrated) | Promote X:\brain\C4C → X:\C4C. Delete D: symlink. |
| `D:\C4C-wiki` | 862 files | `X:\brain\C4C-wiki\` (identical, 862 files) | Promote X:\brain\C4C-wiki → X:\C4C-wiki. Archive D: copy. |
| `D:\FAP` | 63 files | `X:\brain\FAP\` (identical, 63 files) | Promote X:\brain\FAP → X:\FAP. Archive D: copy. |
| `D:\BIL` | 264 files, **actively writing today** (postgres-sync at 07:45) | Not on X: | **See decision flag below.** |

---

## BIL — decision locked 2026-05-16: Option A (full move)

David's call: *"we need to move all that to X. That's where it belongs. I don't know why we don't move everything that works for X to X."*

Plan is now **Option A — full move D:\BIL → X:\BIL**. The May-10 "BIL = local, NAS = cold archive" lock is hereby revised: BIL runs on X:.

**Dependency order matters:** D:\BIL itself contains 78 refs to D:\FAP across 10 files. The FAP postgres sync runs every 12h and writes to D:\FAP\... If we move D:\BIL before updating those refs, the sync breaks the next time it fires.

Sequence:
1. Phase 4c (cloud-AI batch-script sweep) updates ALL refs: `D:\BIL\*` → `X:\BIL\*` and `D:\FAP` → `X:\FAP` across every `.py`, `.bat`, `.ps1`, `.json`, `.md`, and the relevant Task Scheduler XML.
2. Phase 5 then executes the actual move: `robocopy /MOVE D:\BIL X:\BIL`, `robocopy /MOVE D:\FAP X:\FAP`. Then re-import the Task Scheduler job pointing at X: paths.
3. Old D:\BIL and D:\FAP go to D:\_ARCHIVE\ (per no-delete rule) — empty after the move but preserved as marker.

---

## Plan — phased to David's revised sequencing

Each phase leaves the brain working. Don't push past a phase that breaks something.

### Phase 1 — Get everything onto X: (consolidation)

Goal: kill the duplicate-feeling nest AND pull in the D:\ targets. After this, X: is the single source of truth.

**1a. Flatten the X:\brain\ nest:**
- **Promote** (move up):
  - `X:\brain\C4C\` → `X:\C4C\`
  - `X:\brain\C4C-wiki\` → `X:\C4C-wiki\`
  - `X:\brain\FAP\` → `X:\FAP\`
  - `X:\brain\ollama\*` → `X:\ollama\` (root is currently empty, copy contents in)
- **Drop** (stale duplicates already live at X:\ root):
  - `X:\brain\ai-portal-generator\` — delete (root is newer)
  - `X:\brain\link-pull-drop\` — delete
  - `X:\brain\paper-proof-grader\` — delete (root has 2× more files, newer)
  - `X:\brain\_LOGS\` — delete (root has newer)
  - `X:\brain\theophysics-comms-hub\` — delete (identical 1-file folder)
- Move `X:\brain\C4C_FAP_MIGRATION_NOTE_2026-05-13.md` → `X:\Backside\` (provenance).
- Delete `X:\brain\` once empty.

**1b. Pull in D:\ targets:**
- `D:\C4C` → already a symlink to `O:\_ Theophysics_Case_for_Christ\`, and content already lives at `X:\C4C\` after 1a. Delete the D:\ symlink.
- `D:\C4C-wiki` (862 files, identical to X:\C4C-wiki after 1a) → archive D: copy to `D:\_ARCHIVE\` (per CLAUDE.md "no deletes" rule).
- `D:\FAP` (63 files, identical to X:\FAP after 1a) → archive D: copy to `D:\_ARCHIVE\`.
- `D:\BIL` — **see decision flag earlier in this doc.** Default plan: option B (mirror nightly to `X:\BIL\`). Phase 1b queues the mirror; does not move the working copy.

**Verify Phase 1:**
- `Test-Path X:\brain` → `False`
- `(Get-ChildItem X:\C4C -Recurse -File).Count` → ~2,495
- `Test-Path X:\BIL` → `True` (mirror in place if option B chosen, else empty placeholder)
- `X:\paper-proof-grader\RUN.bat` still exits 0 (no broken paths from the brain-flatten)

### Phase 2 — Redundancy sweep

Goal: no duplicates anywhere on X:. Run an audit before pushing anything to GitHub.

1. **Hash-based dedup scan**: PowerShell script under `X:\Backside\dedup_audit.ps1` — recursively hash every file on X: (skip `#recycle`, `_LOGS`, `embeddings\*.dat` which legitimately churn), group by hash, report any size-≥-1MB duplicates with paths and mtimes.
2. **Name-based collision scan**: list any folder name that appears more than once anywhere under X:. (`paper-proof-grader\OUTPUT\` vs `paper-proof-grader\ARCHIVE\OUTPUT\` etc.)
3. **Cross-drive dedup with D:**: any file still on D:\ that's now identical to one on X:\ → flag for archive. Don't delete D:\ originals automatically; move them to `D:\_ARCHIVE\` per the May-10 "no deletes" rule.
4. Output: `X:\Backside\DEDUP_REPORT_<date>.md` with three sections (within-X:, within-D:, cross-drive). David reviews before Phase 3.

**Verify Phase 2:** report exists; flagged duplicates have a decision noted on each (keep / archive / merge).

### Phase 3 — Push everything-except-NLPs to GitHub

Goal: the high-level map and orchestration live online and version-controlled. NLP code/data stays local.

**What goes to GitHub** (the "organization, understanding, and map" David named):
- `X:\README.md`
- `X:\David\` (his maps & notes)
- `X:\00_WORKFLOWS\` (workflow framework, healthcheck, `THEOPHYSICS_WORKFLOW_MAP.md`)
- `X:\Backside\` (intake-engine code once written, dedup script, mirror script)
- Root `RUN_*.bat` click-buttons
- A new `X:\ARCHITECTURE.md` describing the X:\ layout (written in Phase 3)
- Each NLP's `README.md` *only* (not the NLP body) — so the contract is visible online

**What stays local** (the "NLPs"):
- `X:\C4C\`, `X:\C4C-wiki\` — vault content, too large + private
- `X:\knowledge-refinery\`, `X:\paper-proof-grader\`, `X:\axioms\`, `X:\ai-portal-generator\`, `X:\link-pull-drop\`, `X:\ollama\`, `X:\proof-architecture\`, `X:\proof-explorer\`, `X:\session-handoff-drop\`, `X:\FAP\` — pipeline bodies (models, data, outputs)
- `X:\captures\`, `X:\digests\`, `X:\embeddings\`, `X:\models\`, `X:\ratings\` — pipeline data
- `X:\github\` — already its own repo space
- `X:\_LOGS\`, `X:\#recycle\` — runtime

**Repo shape suggestion**: new repo `theophysics-brain-map` at `\\dlowenas\github\` (matches existing convention), structured as a *thin* mirror of X:\ — only the included files/folders, with a `.gitignore` excluding everything else. The repo IS the map.

**Verify Phase 3:** repo exists on GitHub, `git status` clean, `README.md` shows the X:\ root layout, and a fresh clone gives someone the full org/map without any 100MB+ data.

### Phase 4 — Lock-it-down (delegate to cloud AIs)

> **David's note:** *"things like moving all the NLPs to a workflow... changing all the batch scripts because now it's at a different place... is going to be a lot more manageable through cloud programming than you yourself. Once we get an idea of how to lock it down we'll prompt it out."*

My job here is to write **clean prompts** that cloud AIs (Codex, Sonnet, etc.) can execute. I don't do the renames myself. The prompts cover:

**4a. Per-NLP front-door convention** (full design preserved below in Appendix A): every NLP gets a `00_DROP/` folder. Junctions left at old names for one cycle.

**4b. Root simplification** (Appendix B): NLP folders move under `X:\00_WORKFLOWS\<name>\`. Target ~10 items at root. NTFS junctions preserve old paths.

**4c. Batch-script path sweep** (the nitty-gritty David flagged): every `.bat`, `.ps1`, `.py`, `.md` on X:\ and D:\ that hardcodes a moved path gets updated. This is *exactly* the work to delegate — bulk find/replace with careful diff review.

**4d. The intake engine** (Appendix C): Python `watchdog` service at `X:\Backside\intake_engine.py`, Ollama-Mistral classifier for the master `X:\DROP_HERE\`, per-NLP `00_DROP/` watchers. Prompt out the implementation once 4a–4c are settled.

**Verify Phase 4:** prompts written and posted to comms-hub `prompts/x-drive-reorg` channel. Cloud AI execution comes after.

### Phase 5 — BIL + FAP migration to X: (Option A locked)

Prereq: Phase 4c (cloud-AI path sweep) must have rewritten every `D:\BIL\*` and `D:\FAP` reference first, otherwise FAP postgres sync (12h cadence) breaks the next time it fires.

Then:
1. Stop the FAP postgres sync Task Scheduler job temporarily.
2. `robocopy D:\BIL X:\BIL /MOVE /E /XD __pycache__ /XF *.pyc` (skip pycache, move everything else).
3. `robocopy D:\FAP X:\FAP /MOVE /E` (archive D:\FAP to D:\_ARCHIVE\FAP first if there's anything to preserve — there shouldn't be since X:\FAP was the migrated copy).
4. Re-export the Task Scheduler job, update XML paths from D:\BIL → X:\BIL, re-import. Re-enable.
5. Run one manual sync cycle to verify it writes to X:\FAP correctly.
6. Update `X:\BIL\README.md` to reflect "live BIL on NAS, May-10 lock superseded 2026-05-16".

Verify: Task Scheduler `FAP_POSTGRES_SYNC` last result 0. Next-fire timestamp produces `X:\FAP\...` output. D:\BIL no longer exists; D:\_ARCHIVE\ has the move provenance.

---

## Critical files to touch

- `X:\README.md` — rewrite top to reflect new layout (current version reflects the *partial* May-13 cleanup).
- `X:\00_WORKFLOWS\THEOPHYSICS_WORKFLOW_MAP.md` — refresh after Phase 4 prompt-out completes.
- `X:\paper-proof-grader\README.md` — fix `\\dlowenas\brain\paper-proof-grader\` references after Phase 1.
- `D:\BIL\PREFERENCE_ENGINE_REPO_SPEC.md` (line 17) — remove stale `D:\BIL\browser` reference.
- New: `X:\Backside\dedup_audit.ps1` (Phase 2), `X:\Backside\bil_mirror.ps1` (Phase 5 option B).
- New repo: `theophysics-brain-map` (Phase 3) — pushed to GitHub from `\\dlowenas\github\theophysics-brain-map\`.
- Appendix-A/B/C prompts live as `.md` files under `X:\00_WORKFLOWS\prompts\x-drive-reorg\` once written.

---

## Verification (end-to-end)

**After Phase 1 (consolidation):**
- `Test-Path X:\brain` → `False`
- `(Get-ChildItem X:\C4C -Recurse -File).Count` → ~2,495
- `Test-Path X:\BIL` → `True` (mirror placeholder if option B chosen)
- `X:\paper-proof-grader\RUN.bat` exits 0

**After Phase 2 (dedup):**
- `X:\Backside\DEDUP_REPORT_<date>.md` exists with three sections (within-X:, within-D:, cross-drive).
- Every flagged duplicate has a decision noted.

**After Phase 3 (GitHub):**
- Repo `theophysics-brain-map` exists on GitHub, default branch clean.
- Fresh clone gives a complete X:\ map without any NLP binaries or vault content.
- `ARCHITECTURE.md` renders cleanly in GitHub web view.

**After Phase 4 (cloud-AI lock-it-down — eventual):**
- Prompts A/B/C written and posted to comms-hub `prompts/x-drive-reorg`.
- Cloud AI executes: target root layout achieved (~10 items), every NLP has `00_DROP/`, intake engine running. Acceptance criteria match Appendix verifications.

**After Phase 5 (BIL, option B):**
- `Test-Path X:\BIL` → `True`. mtime tracks D:\BIL's after the first overnight run.
- Task Scheduler shows `BIL_NIGHTLY_MIRROR` enabled, last result 0.

---

## Open question for David

~~BIL — pick A / B / C.~~ **Resolved 2026-05-16: Option A locked.** Migration executes in Phase 5 after Phase 4c path sweep.

---

# Appendix — preserved designs for cloud-AI prompting (Phase 4)

These are the original Phase 2/3/4 designs from the first draft. Captured here so the ideas aren't lost. When David is ready to "prompt it out," these become the body of the prompts handed to Codex/Sonnet.

## Appendix A — Per-NLP front-door convention

Goal: every NLP has the same drop-zone name. New AIs and humans never have to guess.

**Standard: `00_DROP/` at the top of every NLP folder.** Numeric prefix matches knowledge-refinery's `00_INTAKE` pattern (sorts to top in Explorer). "DROP" is the literal verb David already uses (`DROP_HERE`, `DROP_PAPERS_HERE`).

Inside every NLP folder, add (or rename to) `00_DROP/`. Keep existing intake folders as junctions/aliases for one cycle so old scripts don't break.

Per-NLP rename map:

| NLP | Old intake | New intake (alias old → new) |
|---|---|---|
| `knowledge-refinery` | `00_INTAKE/` | `00_DROP/` (rename; junction `00_INTAKE` → `00_DROP`) |
| `axioms` | `00_INBOX_DROP_PAPERS_HERE/` | `00_DROP/` |
| `paper-proof-grader` | `INPUT/` + `DROP_PAPERS_HERE/` | `00_DROP/` (merge both, junction both old names) |
| `link-pull-drop` | external `X:\captures\links\DROP_HERE/` | `00_DROP/` inside `X:\link-pull-drop\` |
| `session-handoff-drop` | `DROP_HERE/` | `00_DROP/` |
| `ai-portal-generator` | none | add `00_DROP/` for ad-hoc inputs |
| `proof-architecture`, `proof-explorer` | none | leave alone — publish-only, not pipelines |

Also: each NLP gets a **`README.md` at its root** with a fixed 5-line shape:
```
WHAT: <one sentence>
DROP HERE: ./00_DROP/
RUN: ./RUN.bat
OUTPUT: <path>
OWNER: <AI partner>
```

Acceptance: for every NLP folder, `Test-Path .\00_DROP` → `True`; old intake-folder names are junctions, not deleted.

## Appendix B — Root simplification + click buttons

Goal: open X:\ and see ~10 well-named groups, not 26.

**Target root layout:**

```
X:\
  README.md                             ← signpost (already exists, update)
  DROP_HERE\                            ← master drop (Appendix C wires it up)
  RUN_*.bat                             ← 3-5 one-click buttons, all at root
  David\                                ← human maps & notes (already exists)
  00_WORKFLOWS\                         ← all 9 NLPs as subfolders (move them in)
  Knowledge\                            ← vault content
    C4C\
    C4C-wiki\
    FAP\
    axioms\        (if treated as knowledge, not pipeline)
  Pipeline\                             ← shared NLP data
    captures\
    digests\
    embeddings\
    models\
    ratings\
  Backside\                             ← intake engine + automation
  github\                               ← keep at root (tool-of-tools)
  _LOGS\
  #recycle\                             ← system, leave
```

The big move: **all 9 NLP folders move under `00_WORKFLOWS\`**. Every existing `.bat`, every comms-hub message that says `X:\paper-proof-grader\...` needs a path update — this is the batch-script sweep David named as the "nitty-gritty." Mitigation: leave NTFS directory junctions at the old root paths pointing into `00_WORKFLOWS\<name>\` for one transition cycle, so old scripts keep working while we update them.

**Click buttons at root** — keep tight, ≤5:
- `RUN_PUBLIC_ARTICLE_REFINERY.bat` (existing)
- `RUN_FAP_ARTICLE_PIPELINE.bat` (existing)
- `RUN_LINK_PULL.bat` (new — wraps link-pull-drop's PASTE_AND_RUN)
- `RUN_PAPER_GRADER.bat` (new — wraps paper-proof-grader/RUN.bat)
- `RUN_BRAIN_MENU.bat` (new — master menu for everything else)

Acceptance: `Get-ChildItem X:\ -Directory | Measure-Object` → ≤12; junctions at old root paths resolve correctly.

## Appendix C — Backside intake engine

Goal: drop a file anywhere, the engine routes/processes without a button click.

Build `X:\Backside\intake_engine.py` (Python `watchdog`). Runs as a Windows service via Task Scheduler `At Startup`. Responsibilities:

1. **Watch** every `00_DROP/` folder under `X:\00_WORKFLOWS\*\` AND the root `X:\DROP_HERE\` (the master drop).
2. **Classify** anything dropped at root `X:\DROP_HERE\`:
   - Call local Ollama Mistral (`http://localhost:11434`) with a short prompt: *"This file is being dropped into a knowledge pipeline. Filename: {name}. First 500 chars: {preview}. Classify as one of: PAPER, LINK, SESSION_HANDOFF, AXIOM, GENERAL. One word."*
   - Move file to the corresponding NLP's `00_DROP/`.
3. **Trigger** the NLP's `RUN.bat` when its `00_DROP/` gets a new file (debounced 30 s to allow multi-file paste).
4. **Log** every action to `X:\_LOGS\intake_engine_YYYY-MM-DD.log`.
5. **Restart-safe**: on startup, sweep all `00_DROP/` folders once to catch anything dropped while the service was down.

Available infrastructure to plug into:
- Ollama Mistral local (used by `X:\ollama\ollama_session_handoff.py`).
- Infinity embedding server at `192.168.1.177:7997`.
- Qdrant vector DB at `192.168.1.177:6333`.
- DeBERTa zero-shot classifier in `X:\paper-proof-grader\` (overkill for routing; Mistral is enough).

The router is the *minimum* smart layer. Per-NLP `RUN.bat` keeps existing logic. No big-bang rewrite.

Acceptance: drop a test `.pdf` into `X:\DROP_HERE\` → within 60s it lands in `X:\00_WORKFLOWS\paper-proof-grader\00_DROP\` and the grader RUN starts; log entry confirms.
