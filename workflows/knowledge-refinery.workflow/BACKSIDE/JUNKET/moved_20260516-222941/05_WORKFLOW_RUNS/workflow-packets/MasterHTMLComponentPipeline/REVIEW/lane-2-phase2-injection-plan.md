# Lane 2 — Phase 2 Injection Plan

Author: claude-code-forge (Worker 2)
Date: 2026-05-13
Inputs read:
- `OUTPUT/k-production-ready.inventory.json` (Worker 1)
- `\\dlowenas\HPWorkstation\Desktop\Master HTMl\_KIMI-READ-FIRST\HTML-MARKING-STANDARD.md`
- `CONFIG/script_registry.json`, `CONFIG/source_roots.example.json`
- `SCRIPTS/component_operator.py`
- `SCRIPTS/imported/html_master_workflow/01_one_pass_html/{02,05,06,07,09}_*.py`

---

## Headline finding (read this first)

The folder Worker 1 inventoried — `\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready` — has **zero Kimi-canonical markers in all 35 files**. Inventory: `begin_count=0`, `end_count=0`, `data_component_count=0`, `page_meta={}` across the board.

Phase 2 in this packet is defined as "inject series nav, media, images, glossary, or article support blocks where markers exist." There are no markers. **Phase 2 cannot run on K-Production-Ready as the system is currently wired.**

Three independent blockers explain this:

- **Blocker A — no sockets.** Pages need `<!-- BEGIN:COMPONENT:{type}:{name} -->…<!-- END:… -->` pairs and a `PAGE_META` block before `component_operator.py replace` has anywhere to write.
- **Blocker B — wrong source root in imported scripts.** `05_wire_canonical_navigation.py`, `06_wire_unified_media_players.py`, and `07_patch_series_polish_gaps.py` are hardcoded to `Cannon/genesis-to-quantum` (or `Path(__file__).parents[1]`), not to `K-Production-Ready`. Running them today would touch the wrong tree.
- **Blocker C — non-canonical markers.** `02_label_gtq_sections.py` emits the legacy form `<!-- BEGIN: SECTION-NAME -->` (single-token), not the Kimi-canonical `<!-- BEGIN:COMPONENT:{type}:{name} -->`. Even after labeling, `component_operator.py` will still report zero canonical sockets.

The plan below addresses all three before scheduling any inject pass.

---

## Recommended sequence

```
PHASE 0  Marker upgrade        Worker 1 / Codex     produce sockets in K-Production-Ready
PHASE 1  Verify sockets        Worker 1             component_operator inventory must show pairs > 0
PHASE 2  Inject per socket     this plan            replace template content into sockets
PHASE 3  Verify post-inject    component_operator   re-inventory, diff against expected sockets
PHASE 4  Approve + apply       David (gate)         flip dry-run to --apply
```

Phase 2 itself is socket-by-socket; the lanes below are per-socket-type, not per-script. Scripts are picked to fit the socket, not the other way around.

---

## Phase 2 socket map (the actual injection plan)

For each canonical socket, this row gives: which Kimi `type:name` it targets, what asset/template fills it, which driver script should do the work, dry-run posture, risk, and whether human review is required.

| Lane | Socket (`type:name`) | Asset / template source | Driver | Dry-run default | Risk | Human review |
|------|----------------------|-------------------------|--------|-----------------|------|--------------|
| NAV-1 series rail (sticky top) | `topbar:topbar-gold-ribbon` | One template per series; ribbon color from `SERIES_CONFIG` in `09_inject_series_ribbon.py` | `component_operator.py replace` w/ extracted template | YES | low | first per-series, then batch |
| NAV-2 sidebar TOC | `sidebar:sidebar-toc` | `sidebar_for(current_file)` output in `05_wire_canonical_navigation.py` (per-file: needs the article filename) | new wrapper script `phase2_inject_sidebar.py` that templatizes per-file then calls component_operator | YES | medium (per-file template; not a single static template) | first 3 articles, then batch |
| NAV-3 series rail (inline) | `cta:cta-prev-next` or new `nav:series-rail` (extend marking standard) | `series_rail(i)` in `07_patch_series_polish_gaps.py` | wrapper script `phase2_inject_series_rail.py` (per-file index) | YES | medium | first per-series-tier (main vs deep) |
| AUDIO-1 unified player audio source | `audio:audio-{slug}-read` | R2 audio under `\\dlowenas\cloudflarer2media\` — confirm exact path before wire | `06_wire_unified_media_players.py` adapted: replace inside `audio` socket only | YES | medium (asset existence per article) | first article + audit asset map |
| VIDEO-1 unified player video source | `video:video-{slug}` | Video assets in `\\dlowenas\cloudflarer2media\` (path to confirm) | same as AUDIO-1 | YES | medium | same as AUDIO-1 |
| VIDEO-2 video library page tiles | `section:video-library-grid` (extend) on `video-library.html` only | tile template from existing video-library content | one-off wrapper, not batch | YES | low | one-off |
| IMAGE-1 infographic figure | `image:image-{slug}-infographic` | `INFOGRAPHICS` dict in `07_patch_series_polish_gaps.py`; assets in `images/` | new wrapper `phase2_inject_infographic.py` | YES | medium (asset path mapping per article) | first 3 + audit |
| IMAGE-2 slide gallery | `image:image-{slug}-slides` or `chart:chart-{slug}` | slide-strip block in `07_patch_series_polish_gaps.py` | same wrapper as IMAGE-1, gallery mode | YES | medium | first per-series |
| SUPPORT-1 executive summary | `executive-summary:executive-summary` | per-article body — likely already inline, just needs socket wrap | label pass, not inject (Worker 1 lane) | n/a | low | n/a |
| SUPPORT-2 TTS controls | `tts:tts-player` | template in `01_one_pass_html` — confirm before wiring | wrapper `phase2_inject_tts.py` | YES | low | first article |
| SUPPORT-3 glossary | `glossary:glossary-{term}` | glossary entries authored separately; not yet in any script | DEFERRED — needs glossary source-of-truth resolved first | n/a | n/a | block |
| SUPPORT-4 footer | `footer:footer-global` | single template extracted from a known-good page | `component_operator.py replace` | YES | low | one-time approval |
| SUPPORT-5 mode-toggle | `mode-toggle:mode-toggle` | extract from labeled HERO template | `component_operator.py replace` | YES | low | one-time approval |

Notes on the table:
- "extend marking standard" cells flag where the current Kimi type list does not have a clean home for the legacy block. Those decisions go to Kimi, not Worker 2. See *Open questions to Kimi* below.
- Where the driver is `component_operator.py replace`, the template must be `extract`ed from an approved donor page first (Phase 2.0 sub-step), reviewed, then replayed across the corpus.
- Every row is dry-run by default. `--apply` requires David's go-ahead per lane, not once per packet.

---

## Per-socket safety contract

Every Phase 2 driver must, before write:

1. Require `--root <K-Production-Ready path>` explicitly. No `Path(__file__).parents[1]` defaults.
2. Refuse to run on files where the target `BEGIN/END` pair is absent (don't insert into raw HTML).
3. Refuse to run on files where the pair appears more than once (duplicate-name fail).
4. Honor a `--dry-run` default and require `--apply` to write.
5. On apply: backup as `<file>.bak.<timestamp>` (component_operator already does `.bak` — extend to timestamped backup so re-runs don't clobber the first backup).
6. Emit a per-file JSON status entry: `{file, socket, action, before_hash, after_hash, status}`.

The PySide6 GUI (Lane 3) consumes that JSON. Worker 2 does not block on GUI work — the plan is GUI-ready by emitting JSON, but does not require the GUI to exist.

---

## Risk ledger

- **R1 (high):** Imported scripts have in-place write paths and hardcoded ROOTs. If invoked accidentally they touch `Cannon/genesis-to-quantum`, not the target tree. Mitigation: do not call those scripts directly in Phase 2; lift their template strings and per-file logic into new wrappers that route through `component_operator.py replace`.
- **R2 (medium):** Asset existence per article. Audio/video/image rows assume R2 has the file at a deterministic path. Need an asset-existence pre-flight (`HEAD` on each expected URL, or `Test-Path` on the R2-synced share) before inject.
- **R3 (medium):** Sidebar and series-rail templates are per-file (current-article highlighting, prev/next pointers). Treating them as "one template, replay everywhere" will silently corrupt — they must be re-rendered per file. The component_operator's current `replace` takes a single static template; Phase 2 needs a templater on top.
- **R4 (low):** Marking standard does not have a `nav` type. `topbar` and `sidebar` cover most, but the inline series rail does not fit cleanly. Either reuse `cta` or add `nav` — Kimi's call.

---

## Open questions to Kimi (workflow-4)

1. Should the inline series rail be `cta:cta-prev-next` or do we add a `nav` type to the marking standard?
2. Glossary sockets — is there a canonical glossary source file yet, or should SUPPORT-3 stay blocked?
3. Should `executive-summary` always be its own socket even when the article does not have a hand-written summary?
4. For audio/video sockets, is `audio-{slug}-read` and `video-{slug}` the right naming, or do you want a separate naming convention?

---

## What Phase 2 does NOT do

- Does not rewrite article bodies.
- Does not change Phase 1 marker labeling (that's the upstream lane).
- Does not run the legacy `01_one_pass_html` scripts in place. Those become template donors only.
- Does not delete anything; per packet rule, "every delete is a move to `_ARCHIVE/`."

---

## Concrete next actions (in order)

1. Worker 1 (or Codex): upgrade `02_label_gtq_sections.py` to emit canonical Kimi pairs, run on `K-Production-Ready`, re-inventory. Confirm `begin_count > 0` on every file. **Phase 2 is blocked until this is true.**
2. Worker 2 (this lane, next pass): pick one donor page per socket type, run `component_operator.py extract` to capture an approved template, store under `REVIEW/templates/<type>__<name>.html`.
3. Worker 2: write one wrapper script per per-file lane (sidebar, series-rail, infographic) that renders the right template per file and shells out to `component_operator.py replace`.
4. Worker 3 (GUI lane): reads the JSON status emitted by step 3.
5. David approves per lane, then `--apply`.

---

## Status (Worker 2 lane)

```
TODO        socket-by-socket inject (table above) — blocked on Phase 0
IN_PROGRESS none (this plan finishes the orientation pass)
REVIEW      this document
BLOCKED     Phase 0 marker upgrade in K-Production-Ready (Worker 1 / Codex)
DONE        inventory read, marking standard read, script audit, plan written
```
