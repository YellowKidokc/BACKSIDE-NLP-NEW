# Lane 4 — Imported Script Safety Review

**Worker 4 / claude-code-ledger**
**Scope:** 18 scripts under `SCRIPTS/imported/html_master_workflow/`
**Method:** Static read-only review. Zero scripts executed. Zero production HTML touched.

## TL;DR for Codex / David

- **Safe to expose in GUI today (3 scripts):** `02_label_gtq_sections`, `10_build_web_index`, `04/02_sort_html` — but `02_label_gtq_sections` emits legacy markers, see Note A below.
- **Safe behind a light wrapper (5 scripts):** `01_gtq_batch_transform`, `02/01_build_papers_deploy_canonical`, `02/03_generate_indexes`, `03/02_convert_canonical_html_to_tts_markdown`. Light = `--root`/`--out` arg + dry-run flag.
- **Do NOT expose in GUI until wrapped (9 scripts):** `03_apply_topbar`, `04_normalize_articles`, `05_wire_canonical_navigation`, `06_wire_unified_media_players`, `07_patch_series_polish_gaps`, `08_standardize_templates`, `09_inject_series_ribbon`, `03/01_inject_tts`, `04/01_canonical_sort`, `04/03_sort_unsorted`. (Counts to 10 — `08` is the urgent one.)
- **Do not expose at all (1 script):** `02/02_generate_web_papers_legacy` — legacy generator superseded by `02/01`.

### Cross-lane context that touches the safety conclusions

- **W1 finding:** K-Production-Ready (35 files) and Kimi\workspace (28 files) both show zero `BEGIN:COMPONENT` pairs. The only file in this packet's reach with markers is `TEMPLATE COWORK\HERO.labeled.html` (163 markers in the OLD `<!-- BEGIN: TOPBAR -->` dialect). So today the GUI has nothing canonical to operate on.
- **W2 finding:** `02_label_gtq_sections.py` emits the legacy `<!-- BEGIN: NAME -->` form, not Kimi v1.0 `<!-- BEGIN:COMPONENT:{type}:{name} -->`. Phase 0 (marker upgrade) is blocked on this. **Implication for my review:** even though `02_label_gtq_sections.py` is mutation-safe (writes a `.labeled` sidecar by default), running it in the GUI today will produce off-spec output. Mark it `SAFE-BUT-LEGACY` in the GUI command palette until Codex upgrades it.
- **W3 ask (lane-3-gui-backend-contract.md):** "Imported scripts (label_gtq_sections, wire_navigation, wire_media, series_polish) are off-contract and in-place-capable... Worker 4 (safety lane) should bound their write behavior before the GUI is allowed to call them." → covered below. All four are tagged BLOCKED or SAFE-BUT-LEGACY here; none should appear in the GUI's run-it-now path until the wrappers in Section "Recommended Wrappers" are in place.

---

## Per-Script Safety Sheet

Field order matches the lane-4 prompt exactly.

### 1. `SCRIPTS/imported/html_master_workflow/01_one_pass_html/01_gtq_batch_transform.py`

- **Purpose:** Run 4 batch transforms across 26 GTQ articles (hero reorder under topbar, kill Watch-and-Listen tab, add sidebar-collapse CSS+button+JS, widen video on sidebar collapse).
- **Expected input:** A `D:\GTQ-BUILD\articles\` tree where each article has its own subdir and the article file is `gtq-*.html` inside it.
- **Hard-coded paths:** `ARTICLES_DIR = Path(r"D:\GTQ-BUILD\articles")`, `BACKUP_DIR = ARTICLES_DIR / "_transform_backups"`.
- **Supports dry-run:** Yes (default mode; `--apply` is required to write).
- **Writes in place:** Yes, with backup.
- **Backup behavior:** Per-run timestamped subdir under `_transform_backups/<YYYYMMDD-HHMMSS>/`; original copied via `shutil.copy2` before overwrite.
- **Needs wrapper before GUI use:** Light wrapper for `--root` override. Not safety-critical because dry-run + backups exist.
- **Safe to expose in PySide6 GUI:** **Yes, behind a light wrapper.**

### 2. `SCRIPTS/imported/html_master_workflow/01_one_pass_html/02_label_gtq_sections.py`

- **Purpose:** Apply BEGIN/END comment markers around recognizable article components; emit per-file JSON inventory sidecar.
- **Expected input:** One HTML file or a folder, via positional `target` arg. Supports `--recursive`.
- **Hard-coded paths:** None. CLI-driven.
- **Supports dry-run:** Implicit — default writes a `.labeled.html` sidecar; only `--in-place` mutates the source.
- **Writes in place:** Only with `--in-place`.
- **Backup behavior:** On `--in-place`, creates `<file>.bak-YYYYMMDD-HHMMSS` before overwrite.
- **Needs wrapper before GUI use:** No, for mutation safety. **Yes, for output format** — emits legacy `<!-- BEGIN: NAME -->`, not Kimi-canonical `<!-- BEGIN:COMPONENT:{type}:{name} -->`. (See W2 finding above; Phase 0 fix needed.)
- **Safe to expose in PySide6 GUI:** **Yes, with a "legacy dialect" tag** until Codex upgrades the labeler to emit Kimi v1.0 markers. Without the upgrade, its output won't show in `component_operator.py inventory` counts.

### 3. `SCRIPTS/imported/html_master_workflow/01_one_pass_html/03_apply_topbar.py`

- **Purpose:** Strip old nav/header/hero, inject Gold Edge topbar + Minimal Centered hero with prev/next links.
- **Expected input:** `gtq-*.html` files **colocated with the script**.
- **Hard-coded paths:** `SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))`. The 26-article order map and title/subtitle map are baked into the script body.
- **Supports dry-run:** No.
- **Writes in place:** Yes, direct overwrite.
- **Backup behavior:** None.
- **Needs wrapper before GUI use:** Yes, required.
- **Safe to expose in PySide6 GUI:** **No.**

### 4. `SCRIPTS/imported/html_master_workflow/01_one_pass_html/04_normalize_articles.py`

- **Purpose:** Remove hamburger sidebar (button + overlay + nav + CSS); inject "Honest Assessment" block; add Font Awesome.
- **Expected input:** `gtq-*.html` files colocated with the script.
- **Hard-coded paths:** `SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))`.
- **Supports dry-run:** No.
- **Writes in place:** Yes, direct overwrite.
- **Backup behavior:** None.
- **Needs wrapper before GUI use:** Yes, required.
- **Safe to expose in PySide6 GUI:** **No.**

### 5. `SCRIPTS/imported/html_master_workflow/01_one_pass_html/05_wire_canonical_navigation.py`

- **Purpose:** Wire canonical sidebar nav, bottom prev/next nav, link rewrites (28-entry LINK_MAP), poster fixes, absolute-prefix strip, index.html cleanup.
- **Expected input:** All 26 `gtq-*.html` files sitting at `Path(__file__).resolve().parents[1]`.
- **Hard-coded paths:** `ROOT = Path(__file__).resolve().parents[1]`. The ARTICLES list, LINK_MAP, POSTER_MAP, and `ABSOLUTE_GTQ_PREFIX` are baked in. Raises `FileNotFoundError` on first missing article — fails loud.
- **Supports dry-run:** No.
- **Writes in place:** Yes, direct overwrite.
- **Backup behavior:** None.
- **Needs wrapper before GUI use:** Yes, required. (W3 explicitly named this script.)
- **Safe to expose in PySide6 GUI:** **No.**

### 6. `SCRIPTS/imported/html_master_workflow/01_one_pass_html/06_wire_unified_media_players.py`

- **Purpose:** Inject a unified video+TTS+deep-dive+debate media player section; remove legacy summary-video figure; wire each article to its `Video/<slug>/{video,audio}/*` assets.
- **Expected input:** 26 `gtq-*.html` at `parents[1]`; sibling `Video/` tree with per-slug subdirs.
- **Hard-coded paths:** `ROOT = Path(__file__).resolve().parents[1]`, `VIDEO_ROOT = ROOT / "Video"`. CANONICAL slug map baked in.
- **Supports dry-run:** No.
- **Writes in place:** Yes, direct overwrite.
- **Backup behavior:** None.
- **Needs wrapper before GUI use:** Yes, required. (W3 explicitly named this script.)
- **Safe to expose in PySide6 GUI:** **No.**

### 7. `SCRIPTS/imported/html_master_workflow/01_one_pass_html/07_patch_series_polish_gaps.py`

- **Purpose:** Add series rail (prev/next + position), infographic figures, slide galleries (`images/<slug>/slide_*.webp`), GTQ-07 "Break This Claim" callout, GTQ-06 Born-Rule objection text.
- **Expected input:** 26 articles + per-slug image directories.
- **Hard-coded paths:** **`ROOT = Path(r"C:\Users\lowes\OneDrive\Desktop\Cannon\genesis-to-quantum")`** — user-specific OneDrive path baked into the script. ARTICLES + INFOGRAPHICS dicts baked in.
- **Supports dry-run:** No.
- **Writes in place:** Yes, direct overwrite.
- **Backup behavior:** None.
- **Needs wrapper before GUI use:** Yes, required. (W3 explicitly named this script.) The OneDrive path also needs to move into `CONFIG/source_roots.json`.
- **Safe to expose in PySide6 GUI:** **No.**

### 8. `SCRIPTS/imported/html_master_workflow/01_one_pass_html/08_standardize_templates.py`

- **Purpose:** Convert Source-Serif / Cormorant / Quartz-themed pages to the Oswald / Crimson Text / Inter "modern" template (font links, CSS root vars, body fonts, Font Awesome).
- **Expected input:** Every `.html` file under `SITE_ROOT` (recursive walk).
- **Hard-coded paths:** `SITE_ROOT = os.path.dirname(os.path.abspath(__file__))`. EXCLUDE = `{_archive, node_modules, .git, Archive}`. KEEP_AS_IS = `{formal-papers, logos-papers, Logos_Papers}`. Files over 500 KB are skipped.
- **Supports dry-run:** No.
- **Writes in place:** Yes, direct overwrite, across the entire matched tree.
- **Backup behavior:** None.
- **Needs wrapper before GUI use:** **Yes, urgent.** This is the biggest blast radius in the bundle — one wrong `SITE_ROOT` rewrites the whole site.
- **Safe to expose in PySide6 GUI:** **No.**

### 9. `SCRIPTS/imported/html_master_workflow/01_one_pass_html/09_inject_series_ribbon.py`

- **Purpose:** Inject a sticky top series ribbon (`<nav class="tp-ribbon">`) into articles that don't have one; colors by series.
- **Expected input:** Every `.html` under `SITE_ROOT` (recursive); 22-series color/name map baked in.
- **Hard-coded paths:** `SITE_ROOT = script's own dir`. SERIES_CONFIG baked in.
- **Supports dry-run:** No.
- **Writes in place:** Yes, direct overwrite.
- **Backup behavior:** None.
- **Needs wrapper before GUI use:** Yes, required.
- **Safe to expose in PySide6 GUI:** **No.**

### 10. `SCRIPTS/imported/html_master_workflow/01_one_pass_html/10_build_web_index.py`

- **Purpose:** Scan a site tree, extract `<title>` from every HTML, build the master `WEB_PAGE_INDEX.html` + a `web-manifest.json`.
- **Expected input:** Site root via `--dir` arg (defaults to script's own dir).
- **Hard-coded paths:** Default `SITE_DIR` is script dir, but **`--dir` CLI override exists.** SECTION_META map baked in (cosmetic only).
- **Supports dry-run:** Implicit — only derived files are written.
- **Writes in place:** No. Writes only `WEB_PAGE_INDEX.html` + `web-manifest.json` in the chosen dir.
- **Backup behavior:** N/A (derived output).
- **Needs wrapper before GUI use:** Light — add `--out` separate from `--dir` so the index doesn't always land alongside the source tree.
- **Safe to expose in PySide6 GUI:** **Yes.**

### 11. `SCRIPTS/imported/html_master_workflow/02_paper_body_generation/01_build_papers_deploy_canonical.py`

- **Purpose:** Build the 10 "Algorithmic Foundations of Reality" formal-paper HTML files plus their index.html ("Illuminated Codex" design — watermark glyphs, accent colors, KaTeX, reading progress bar, TOC).
- **Expected input:** 10 `Paper_NN_*.md` files colocated with the script.
- **Hard-coded paths:** `PAPERS_DIR = script dir`, `OUT_DIR = PAPERS_DIR / "html"`. PAPERS list, ACCENTS, GLYPHS, TAGLINES baked in.
- **Supports dry-run:** Implicit — output is derived. No CLI flags.
- **Writes in place:** No. Writes to `html/` subdir.
- **Backup behavior:** N/A on inputs; re-running overwrites prior outputs without preservation.
- **Needs wrapper before GUI use:** Light — `--source` and `--out`.
- **Safe to expose in PySide6 GUI:** **Yes, behind a light wrapper.**

### 12. `SCRIPTS/imported/html_master_workflow/02_paper_body_generation/02_generate_web_papers_legacy.py`

- **Purpose:** Legacy paper generator — applies a Kimi template HTML to the 10 papers; predates `02/01_build_papers_deploy_canonical.py`.
- **Expected input:** 10 markdown papers + 1 Kimi template HTML.
- **Hard-coded paths:** Three user-Desktop paths baked in: `C:\Users\lowes\Desktop\Kimi Web Design\theophysics-paper-template.html`, `C:\Users\lowes\Desktop\Theophysics_Papers_April_2026`, `C:\Users\lowes\Desktop\Theophysics_Web_Pages_April_2026`.
- **Supports dry-run:** No.
- **Writes in place:** No (writes new files in a separate output dir), but the dir auto-creates and overwrites siblings.
- **Backup behavior:** None.
- **Needs wrapper before GUI use:** N/A — recommend mark deprecated and exclude.
- **Safe to expose in PySide6 GUI:** **No — deprecated, do not expose.** Not currently listed in `script_registry.json`; keep it that way.

### 13. `SCRIPTS/imported/html_master_workflow/02_paper_body_generation/03_generate_indexes.py`

- **Purpose:** Generate per-series `index.html` for Parts IX–XVIII (cross-domain, bible-through-equation, spiritual-warfare, consciousness, prophetic-synthesis, duality-project, prophetic, etc. — 10 series in total).
- **Expected input:** Series folders under CWD.
- **Hard-coded paths:** `base_path = "."` (CWD). 10 SERIES configs (dir/title/color/articles list) baked in.
- **Supports dry-run:** No.
- **Writes in place:** Yes — overwrites each series' existing `index.html`.
- **Backup behavior:** None.
- **Needs wrapper before GUI use:** Light — `--root` + `--dry-run`.
- **Safe to expose in PySide6 GUI:** **Yes, behind a light wrapper.**

### 14. `SCRIPTS/imported/html_master_workflow/03_tts_export_helpers/01_inject_tts.py`

- **Purpose:** Inject a floating TTS player widget + a ClipSync push button into every HTML in a folder.
- **Expected input:** HTML files in `FOLDER`.
- **Hard-coded paths:** **`FOLDER = Path(r"C:\Users\lowes\Desktop\Html Export")`** — user Desktop path. **`CLIPSYNC_API = "https://clipsync-api.davidokc28.workers.dev/api"`** and **`DEVICE_ID = "html-articles"`** are baked into the JavaScript that gets written into every touched file.
- **Supports dry-run:** No.
- **Writes in place:** Yes, direct overwrite.
- **Backup behavior:** Yes — copies originals to `_ORIGINALS/` before write.
- **Needs wrapper before GUI use:** Yes, required. Wrapper must also surface a `--with-clipsync` opt-in flag (default off), because the embedded JavaScript makes outbound POSTs to the ClipSync worker from every page it touches.
- **Safe to expose in PySide6 GUI:** **No.**

### 15. `SCRIPTS/imported/html_master_workflow/03_tts_export_helpers/02_convert_canonical_html_to_tts_markdown.py`

- **Purpose:** Strip site chrome (script/style/nav/footer/player/sidebar) from canonical HTML; emit clean markdown suitable for TTS narration.
- **Expected input:** 26 `gtq-*.html` at `parents[1]`; fallback markdown at `parents[1]/CODEX_BUILD/markdown`.
- **Hard-coded paths:** `ROOT = Path(__file__).resolve().parents[1]`, `OUT = ROOT/"CODEX_BUILD"/"tts_markdown"`, `SOURCE_MD = ROOT/"CODEX_BUILD"/"markdown"`. ARTICLES baked in.
- **Supports dry-run:** Implicit — derived output only.
- **Writes in place:** No.
- **Backup behavior:** N/A (derived output).
- **Needs wrapper before GUI use:** Light — `--in` + `--out`.
- **Safe to expose in PySide6 GUI:** **Yes, behind a light wrapper.**

### 16. `SCRIPTS/imported/html_master_workflow/04_sorting_triage/01_canonical_sort.py`

- **Purpose:** Copy HTML files from a "DAVID WEBPAGES" NAS share into a 4-pillar (THO / PHY / THE / APP) NAS structure by keyword mapping.
- **Expected input:** Source NAS share with HTML files.
- **Hard-coded paths:** **`source = r'\\192.168.1.177\Desktop\DAVID WEBPAGES'`**, **`dest_base = r'\\192.168.1.177\Desktop\Gemini\'s web pages'`** — NAS IP-numeric paths baked in.
- **Supports dry-run:** No.
- **Writes in place:** No — `shutil.copy2` only (originals preserved).
- **Backup behavior:** N/A (originals not modified).
- **Needs wrapper before GUI use:** Yes, required. Wrapper must verify NAS reachability before run and externalize the IP/share into `CONFIG/source_roots.json`.
- **Safe to expose in PySide6 GUI:** **No.**

### 17. `SCRIPTS/imported/html_master_workflow/04_sorting_triage/02_sort_html.py`

- **Purpose:** Read-only triage — walk a tree, categorize every HTML as Website-Ready / Obsidian-Export / Snippet / Unknown by sniffing the first 2000 bytes; print summary.
- **Expected input:** Root dir (CWD).
- **Hard-coded paths:** `root_dir = r'.'`. Skips `_LIVE_DEPLOY` and `.git`.
- **Supports dry-run:** Implicit — never writes anything.
- **Writes in place:** No.
- **Backup behavior:** N/A.
- **Needs wrapper before GUI use:** Light — `--root` + `--out` (currently dumps to stdout only).
- **Safe to expose in PySide6 GUI:** **Yes.**

### 18. `SCRIPTS/imported/html_master_workflow/04_sorting_triage/03_sort_unsorted.py`

- **Purpose:** Move (not copy) files out of `DMP_Unsorted/` into category subfolders by regex-on-filename mapping (28 codes).
- **Expected input:** `DMP_Unsorted/` under CWD; 27 category dirs (`folder_map`) also under CWD.
- **Hard-coded paths:** `source_dir = 'DMP_Unsorted'`, `target_base = '.'`. Mapping + folder_map baked in.
- **Supports dry-run:** No.
- **Writes in place:** Yes — **`shutil.move()` is destructive.** All exceptions silently swallowed by `except Exception: pass`, so failures leave no log trace.
- **Backup behavior:** None.
- **Needs wrapper before GUI use:** **Yes, urgent.** Wrapper must convert internal move to copy-verify-delete with explicit failure logging, default to dry-run, require `--apply`.
- **Safe to expose in PySide6 GUI:** **No.**

---

## Recommended Wrappers (concrete plan)

Add under `SCRIPTS/wrappers/`:

1. `safe_inplace.py` — generic in-place rewrite wrapper. Drives a registry-id script through dry-run-by-default, `.bak`-per-file, `--apply` gate, manifest emit. Covers #3, #4, #5, #6, #7, #8, #9.
2. `safe_inject_tts.py` — wraps #14 with `--root`, `--with-clipsync` (default off), dry-run default.
3. `safe_canonical_sort.py` — wraps #16 with explicit `--source`/`--dest`, dry-run default, NAS reachability probe.
4. `safe_sort_unsorted.py` — wraps #18: converts `move` to copy-verify-delete with failure logs to `ERROR/`, dry-run default.

After wrappers exist, extend `CONFIG/script_registry.json` to cover all 18 scripts with two new fields per entry: `safety_tier` (`primary` | `wrapped` | `blocked` | `deprecated`) and `wrapper` (path | null). Today the registry lists only 7 of 18 — the GUI has no source of truth for the other 11.

## Open Ask

W3's contract suggests the GUI's Run Console parses per-file errors rather than a single failure blob. None of the 18 scripts emit structured per-file JSON to stdout today — they all print free-form lines. A wrapper-layer JSON manifest is the cheapest fix; trying to patch each script's logging individually is not.
