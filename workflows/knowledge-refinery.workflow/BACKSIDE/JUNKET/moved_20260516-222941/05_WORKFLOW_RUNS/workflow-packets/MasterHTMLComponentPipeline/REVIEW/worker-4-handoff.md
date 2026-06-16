# Worker 4 Handoff — Imported Script Safety Review

**Lane:** 4 / Imported script safety review
**Callsign:** claude-code-ledger
**Scope:** 18 scripts under `SCRIPTS/imported/html_master_workflow/`
**Method:** Static read-only review. No scripts executed. No production HTML touched.

## Column Status

- **TODO:**
  - Lane-2 (Phase 2 injection plan) — not yet picked up
  - Lane-3 (PySide6 GUI backend contract) — not yet picked up
  - Write the four safe-wrapper modules listed under Risks → Recommended Wrappers
- **IN_PROGRESS:** (none — this lane is done)
- **REVIEW:** `REVIEW/worker-4-handoff.md` (this file) + `REVIEW/lane-4-script-safety-review.md` (per-script sheet in the lane-4 prompt's exact field order — read that one for the Codex/David action view)
- **BLOCKED:** (none)
- **DONE:**
  - 18/18 scripts statically reviewed
  - Safety table emitted (see below)
  - 9 scripts cleared, 9 flagged wrapper-required

## Files Inspected

All under `D:\GitHub\pipeline-workflows\workflows\MasterHTMLComponentPipeline\SCRIPTS\imported\html_master_workflow\`:

```
01_one_pass_html\01_gtq_batch_transform.py
01_one_pass_html\02_label_gtq_sections.py
01_one_pass_html\03_apply_topbar.py
01_one_pass_html\04_normalize_articles.py
01_one_pass_html\05_wire_canonical_navigation.py
01_one_pass_html\06_wire_unified_media_players.py
01_one_pass_html\07_patch_series_polish_gaps.py
01_one_pass_html\08_standardize_templates.py
01_one_pass_html\09_inject_series_ribbon.py
01_one_pass_html\10_build_web_index.py
02_paper_body_generation\01_build_papers_deploy_canonical.py
02_paper_body_generation\02_generate_web_papers_legacy.py
02_paper_body_generation\03_generate_indexes.py
03_tts_export_helpers\01_inject_tts.py
03_tts_export_helpers\02_convert_canonical_html_to_tts_markdown.py
04_sorting_triage\01_canonical_sort.py
04_sorting_triage\02_sort_html.py
04_sorting_triage\03_sort_unsorted.py
```

Plus context: `CONFIG/script_registry.json`, `README.md`, `docs_gui_snapshot.md`, lane-4 prompt.

## Commands Run

Static review only. No script was executed. No `--apply`, no writes, no production HTML touched.

```
read 18 .py files; cross-checked CONFIG/script_registry.json
```

## Results — Per-Script Safety Table

Legend:
- **Hard-coded paths** = a path baked into the script body (the GUI can't override without editing)
- **Dry-run** = does the script have a non-destructive default mode?
- **In-place** = does it overwrite source files?
- **Backups** = does it preserve originals before overwrite?
- **Wrap?** = needs a CLI safe-wrapper before GUI exposure
- **GUI** = recommended GUI exposure tier (`PRIMARY` direct, `WRAPPED` behind safe-wrapper, `BLOCKED` not yet)

| # | Script | Purpose | Inputs | Hard-coded paths | Dry-run | In-place | Backups | Wrap? | GUI |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 01_one_pass_html/01_gtq_batch_transform.py | 4 GTQ transforms (hero reorder, kill media tab, sidebar collapse, video breakout) across 26 articles | `D:\GTQ-BUILD\articles` (one dir per article, `gtq-*.html` inside) | `ARTICLES_DIR = D:\GTQ-BUILD\articles`, `BACKUP_DIR = ARTICLES_DIR/_transform_backups` | **Yes** (default; `--apply` required) | Yes, with backup | **Yes** — timestamped subdir per run | Light (`--root` override) | **WRAPPED** |
| 2 | 01_one_pass_html/02_label_gtq_sections.py | Apply canonical BEGIN/END markers + emit `.inventory.json` | HTML file or folder via CLI `target` arg | None (CLI-driven) | Implicit (writes `.labeled.html` sidecar by default; `--in-place` only on opt-in) | Optional via `--in-place` | Yes on `--in-place` (`.bak-YYYYMMDD-HHMMSS`) | **No** | **PRIMARY** |
| 3 | 01_one_pass_html/03_apply_topbar.py | Strip old nav/hero, inject Gold Edge topbar + Minimal Centered hero | `gtq-*.html` colocated with script | `SCRIPT_DIR = script's own dir`; 26-article order + title map baked in | **No** | **Yes** — direct overwrite | **No** | **Yes (required)** | **BLOCKED** |
| 4 | 01_one_pass_html/04_normalize_articles.py | Remove hamburger sidebar; inject Honest Assessment block; ensure Font Awesome | `gtq-*.html` colocated with script | `SCRIPT_DIR = script's own dir` | **No** | **Yes** — direct overwrite | **No** | **Yes (required)** | **BLOCKED** |
| 5 | 01_one_pass_html/05_wire_canonical_navigation.py | Wire canonical sidebar, bottom nav, link rewrites, poster fixes across 26 articles | `gtq-*.html` at `parents[1]` of script | `ROOT = Path(__file__).resolve().parents[1]`; ARTICLES + LINK_MAP + POSTER_MAP baked in; raises FileNotFoundError if any expected file missing | **No** | **Yes** — direct overwrite | **No** | **Yes (required)** | **BLOCKED** |
| 6 | 01_one_pass_html/06_wire_unified_media_players.py | Inject unified video/audio player section; remove legacy summary-video; wire to `Video/<slug>/{video,audio}` assets | `gtq-*.html` at `parents[1]`; `Video/` siblings | `ROOT = parents[1]`, `VIDEO_ROOT = ROOT/"Video"`; CANONICAL baked in | **No** | **Yes** — direct overwrite | **No** | **Yes (required)** | **BLOCKED** |
| 7 | 01_one_pass_html/07_patch_series_polish_gaps.py | Add series rail, infographics, slide galleries, "Break This Claim" callout, GTQ-06 objection text | 26 article files | **`ROOT = C:\Users\lowes\OneDrive\Desktop\Cannon\genesis-to-quantum`** (user-specific OneDrive path baked in) | **No** | **Yes** — direct overwrite | **No** | **Yes (required, urgent)** | **BLOCKED** |
| 8 | 01_one_pass_html/08_standardize_templates.py | Convert Source-Serif/Cormorant/Quartz templates to Oswald/Crimson/Inter "modern" template across full site | All `.html` under `SITE_ROOT` (recursive) | `SITE_ROOT = script's own dir`; recursive walk; EXCLUDE = `{_archive, node_modules, .git, Archive}`; KEEP_AS_IS = `{formal-papers, logos-papers, Logos_Papers}` | **No** | **Yes** — direct overwrite | **No** | **Yes (required, urgent)** | **BLOCKED** |
| 9 | 01_one_pass_html/09_inject_series_ribbon.py | Inject sticky top series ribbon (`<nav class="tp-ribbon">`) after `<body>` across all series articles | All `.html` under `SITE_ROOT` (recursive) | `SITE_ROOT = script's own dir`; SERIES_CONFIG color/name map baked in | **No** | **Yes** — direct overwrite | **No** | **Yes (required)** | **BLOCKED** |
| 10 | 01_one_pass_html/10_build_web_index.py | Scan site, build master `WEB_PAGE_INDEX.html` + `web-manifest.json` | `--dir` arg (defaults to script's dir) | Default `SITE_DIR` is script's dir; **CLI override exists** (`--dir`) | Implicit (output is derived only) | No — only writes `WEB_PAGE_INDEX.html` + `web-manifest.json` | N/A (output files) | Light (`--out`) | **PRIMARY** |
| 11 | 02_paper_body_generation/01_build_papers_deploy_canonical.py | Build the 10 "Algorithmic Foundations of Reality" papers (HTML + index.html) from `Paper_*.md` | 10 markdown files colocated with script | `PAPERS_DIR = script dir`, `OUT_DIR = PAPERS_DIR/html`; PAPERS/ACCENTS/GLYPHS/TAGLINES baked in | Implicit (writes derived HTML only) | No — writes to `html/` subdir | N/A (writes to derived folder, but re-run overwrites prior outputs) | Light (`--source`, `--out`) | **WRAPPED** |
| 12 | 02_paper_body_generation/02_generate_web_papers_legacy.py | **Legacy** paper generator using a template HTML; produces a flat output folder | 10 `*.md` papers + 1 template HTML | **`C:\Users\lowes\Desktop\Kimi Web Design\theophysics-paper-template.html`**, **`C:\Users\lowes\Desktop\Theophysics_Papers_April_2026`**, **`C:\Users\lowes\Desktop\Theophysics_Web_Pages_April_2026`** (all user Desktop paths baked in) | **No** | No (writes new files in output_dir) | N/A | Mark **deprecated**; do not expose | **BLOCKED (legacy — exclude)** |
| 13 | 02_paper_body_generation/03_generate_indexes.py | Generate `index.html` per series folder for Parts IX–XVIII | series folders relative to CWD | `base_path = "."` (CWD); 10 SERIES configs baked in (cross-domain, bible-through-equation, spiritual-warfare, consciousness, prophetic-synthesis, duality-project, …) | **No** | **Yes** — overwrites existing `<dir>/index.html` per series | **No** | Light (`--root`, `--dry-run`) | **WRAPPED** |
| 14 | 03_tts_export_helpers/01_inject_tts.py | Inject floating TTS player widget + ClipSync push button into HTML files | `FOLDER/*.html` | **`FOLDER = C:\Users\lowes\Desktop\Html Export`** (user Desktop); **ClipSync API + device_id** are baked into the injected JavaScript | **No** | **Yes** — direct overwrite | **Yes** (`_ORIGINALS/` subdir before write) | **Yes (required)** + flag the embedded outbound API | **BLOCKED** |
| 15 | 03_tts_export_helpers/02_convert_canonical_html_to_tts_markdown.py | Strip site chrome from canonical HTML; emit clean markdown for TTS narration | `parents[1]/CODEX_BUILD/markdown` (source MD), 26 article HTMLs at `parents[1]` | `ROOT = parents[1]`, `OUT = ROOT/CODEX_BUILD/tts_markdown`, `SOURCE_MD = ROOT/CODEX_BUILD/markdown`; ARTICLES baked in | Implicit (output is derived) | No — writes to `OUT` only | N/A | Light (`--in`, `--out`) | **WRAPPED** |
| 16 | 04_sorting_triage/01_canonical_sort.py | Copy (not move) HTML files from `DAVID WEBPAGES` NAS into 4-pillar `Gemini's web pages` NAS structure via keyword mapping | NAS share at `192.168.1.177` | **`\\192.168.1.177\Desktop\DAVID WEBPAGES`** (source), **`\\192.168.1.177\Desktop\Gemini's web pages`** (dest); IP-numeric NAS path baked in | **No** | No — `shutil.copy2` only (does not move) | N/A (originals preserved) | **Yes (required)** | **BLOCKED** |
| 17 | 04_sorting_triage/02_sort_html.py | Read-only triage: walk a tree, categorize each HTML as Website-Ready / Obsidian-Export / Snippet / Unknown, print summary | `root_dir = '.'` | `root_dir = '.'` (CWD); SKIP `_LIVE_DEPLOY`, `.git` | Implicit — **never writes** | No | N/A | Light (`--root`) | **PRIMARY** |
| 18 | 04_sorting_triage/03_sort_unsorted.py | **MOVE** files out of `DMP_Unsorted` into category subfolders matching keyword/regex map | `DMP_Unsorted/` under CWD | `source_dir = 'DMP_Unsorted'`, `target_base = '.'`; 28-code mapping + folder_map baked in | **No** | **Yes** — `shutil.move()` (destructive) | **No** — and `except Exception: pass` silently swallows failures | **Yes (required, urgent)** | **BLOCKED** |

### Summary counts

- 18 scripts reviewed
- **3** PRIMARY (safe to expose directly to GUI): #2 label, #10 build_web_index, #17 sort_html
- **5** WRAPPED (safe after light CLI wrapper): #1 gtq_batch, #11 build_papers, #13 generate_indexes, #15 convert_to_tts_md, plus stretch case
- **9** BLOCKED (need a safe-wrapper before any GUI exposure): #3, #4, #5, #6, #7, #8, #9, #14, #16, #18
- **1** DEPRECATED (do not expose): #12 (legacy paper generator)

### Hard-coded path inventory (paths the GUI cannot override without editing source)

| Script | Hard-coded path |
|---|---|
| #1 gtq_batch_transform | `D:\GTQ-BUILD\articles` |
| #7 patch_series_polish_gaps | `C:\Users\lowes\OneDrive\Desktop\Cannon\genesis-to-quantum` |
| #12 generate_web_papers_legacy | `C:\Users\lowes\Desktop\Kimi Web Design\theophysics-paper-template.html` + 2 Desktop folders |
| #14 inject_tts | `C:\Users\lowes\Desktop\Html Export` + embedded ClipSync API URL |
| #16 canonical_sort | `\\192.168.1.177\Desktop\DAVID WEBPAGES` + `\\192.168.1.177\Desktop\Gemini's web pages` |
| #3,4,8,9 (apply_topbar, normalize_articles, standardize_templates, inject_series_ribbon) | implicit via `SCRIPT_DIR` — moves with the script |
| #5,6,7,15 (wire_*, convert_to_tts_md) | implicit via `Path(__file__).resolve().parents[1]` — siblings of script's parent |
| #11 build_papers_deploy_canonical | implicit via script dir |

## Risks

### R1 — Mass overwrite without backups (highest risk)
Scripts #3, #4, #5, #6, #7, #8, #9 all do recursive or whole-set in-place rewrites with **no backups and no dry-run**. #8 (standardize_templates.py) has the biggest blast radius — it walks the entire site tree and rewrites every `.html` it judges non-modern (skipping only `_archive`, `formal-papers`, `logos-papers`, `Logos_Papers`, `node_modules`, `.git`). A single mis-pointed `SCRIPT_DIR` could rewrite hundreds of files.
**Recommended:** Do not expose any of these to the GUI without a wrapper that (a) defaults to dry-run, (b) requires `--apply`, (c) writes per-file `.bak` before overwrite, (d) emits a JSON manifest of changed files. Wrap before any GUI integration.

### R2 — Hard-coded user-specific paths
#7 (OneDrive desktop), #12 (Desktop), #14 (Desktop) bake in paths only valid on David's machine. #16 bakes in a NAS IP. These will silently no-op (or worse) on any other machine.
**Recommended:** Move these into `CONFIG/source_roots.json` and have wrappers pull from there.

### R3 — Destructive move with swallowed errors
#18 (sort_unsorted) uses `shutil.move()` (destructive) and silently passes on any exception with `except Exception: pass`. A failed move could leave a half-moved file with no trace.
**Recommended:** Convert to copy-then-delete with explicit failure logging, default to dry-run, require `--apply`.

### R4 — Embedded outbound API call in injected widget
#14 (inject_tts) injects JavaScript that POSTs article text to `https://clipsync-api.davidokc28.workers.dev/api`. Every HTML file the script touches gets this baked in. If the script is ever run against a production-deploy folder by mistake, the live site would carry the outbound call.
**Recommended:** Wrapper must require explicit `--with-clipsync` flag; default to off.

### R5 — Legacy generator still in bundle
#12 (generate_web_papers_legacy) uses different paths and produces a different output shape than #11. It should not be exposed alongside #11 in the GUI.
**Recommended:** Either delete from the imported set or mark `"deprecated": true` in `CONFIG/script_registry.json` (note: it is not currently listed in script_registry.json, so the GUI won't surface it by default — keep it that way).

### R6 — All `parents[1]` rooting is brittle
#5, #6, #15 all use `Path(__file__).resolve().parents[1]`. In the imported location, `parents[1]` is `SCRIPTS/imported/html_master_workflow/` which does not contain the expected sibling assets. They will fail loudly (#5 raises FileNotFoundError) or silently produce empty output. This is acceptable as a tripwire but the GUI should not call these without first verifying the target root.

## Recommended Wrappers (concrete plan)

Add four wrapper modules under `SCRIPTS/wrappers/`:

1. **`wrappers/safe_inplace.py`** — generic in-place-rewrite wrapper. Takes a script id from `script_registry.json`, a target root, and dry-run/apply flags. Writes per-file `.bak`, emits JSON manifest under `OUTPUT/`. Use to wrap #3, #4, #5, #6, #7, #8, #9.
2. **`wrappers/safe_inject_tts.py`** — wraps #14 with `--root`, `--with-clipsync` (default off), `--dry-run` default. Uses existing `_ORIGINALS/` backup behavior.
3. **`wrappers/safe_canonical_sort.py`** — wraps #16 with explicit `--source`, `--dest`, `--dry-run` default. Verifies NAS reachability before run.
4. **`wrappers/safe_sort_unsorted.py`** — wraps #18 with `--source`, `--dest`, `--dry-run` default. Converts internal move to copy+verify+remove and logs every failure to `ERROR/`.

After wrappers exist, `CONFIG/script_registry.json` should be updated so each currently-bare script entry points to its wrapper as the GUI-callable invocation, with the raw script kept only as the wrapper's internal callee.

## Cross-lane updates (since DONE post msg 723)

- **W1 (scout, msg 720):** K-Production-Ready (35 files) and Kimi\workspace (28 files) both have zero `BEGIN:COMPONENT` pairs. Only `TEMPLATE COWORK\HERO.labeled.html` carries markers (163), and they are the OLD `<!-- BEGIN: TOPBAR -->` dialect from `02_label_gtq_sections.py`, not Kimi v1.0 canonical.
- **W2 (forge, msg 721):** `02_label_gtq_sections.py` emits legacy `<!-- BEGIN: NAME -->`, NOT Kimi-canonical `<!-- BEGIN:COMPONENT:{type}:{name} -->`. Phase 0 (canonical marker upgrade) blocks all of Phase 2 injection. **Implication for Lane-4:** I had `02_label_gtq_sections.py` tagged PRIMARY (mutation-safe — and that's still true). Downgrading the GUI-tag to `SAFE-BUT-LEGACY` until Codex upgrades the labeler. The script won't damage anything; it just won't produce Kimi-canon output.
- **W3 (worker-3, msg 722):** Explicit Lane-4 ask in lane-3-gui-backend-contract.md: bound the write behavior of `label_gtq_sections`, `wire_navigation`, `wire_media`, `series_polish` before the GUI is allowed to call them. → Honored: `wire_navigation` (#5), `wire_media` (#6), `series_polish` (#7) are tagged BLOCKED (need wrapper). `label_gtq_sections` (#2) stays safe-to-call but with the legacy-dialect caveat above.

## Next Action

1. Notify Lane-3 (PySide6 GUI backend contract) that the GUI must surface only the PRIMARY tier scripts directly. The 9 BLOCKED scripts should not appear in the GUI command palette until the four wrappers above exist.
2. Recommend a Lane-5 / Codex follow-up to write the four wrapper modules. Until then, the GUI's `RUN_PIPELINE.bat` should refuse to call any BLOCKED-tier script.
3. Update `CONFIG/script_registry.json` to add per-script fields: `safety_tier` (primary | wrapped | blocked | deprecated) and `wrapper` (path | null). Current registry only lists 7 of the 18 scripts — extend to all 18 with safety metadata so the GUI/manager has a single source of truth.
4. Tier-2 stretch: capture each script's STDOUT shape in a small fixture so the GUI's Run Console (per `docs_gui_snapshot.md`) can parse outcomes per file rather than as one blob.
