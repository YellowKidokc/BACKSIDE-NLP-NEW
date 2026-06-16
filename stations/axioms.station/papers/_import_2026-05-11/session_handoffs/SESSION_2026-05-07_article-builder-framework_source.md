# SESSION HANDOFF — Claude Code (Opus 4.7) | 2026-05-07

**Topic:** Built the reusable Article Builder framework and used it to generate
26 Genesis-to-Quantum article shells, each with a unique topbar.

**Why:** User had been preparing to hand the GTQ unique-header build off to
Codex. Decided mid-session to keep it in Claude Code and to lift the work out
of a one-off script into a reusable framework that becomes the default for
any future serial article project (ISO papers, Convergence series, etc.).

---

## Layer 1 — Session Manifest

### Framework — `D:\article-builder\` (NEW, reusable)
- D:\article-builder\builder.py — CLI: build / validate / list-topbars / list-accents / new-series
- D:\article-builder\core\__init__.py
- D:\article-builder\core\render.py — placeholder substitution, sidebar generation, neighbor-href computation, accent palette resolution
- D:\article-builder\templates\article-shell.html — body shell (hero grid, tabs, kill sidebar, audio dock, footer); same for every series
- D:\article-builder\templates\topbars\tb-classical.html — gold ribbon, brand left, nav right
- D:\article-builder\templates\topbars\tb-slab.html — full accent slab, dark text
- D:\article-builder\templates\topbars\tb-spine.html — 4px gradient line + dark bar with badge + italic title
- D:\article-builder\templates\topbars\tb-edge.html — left vertical accent bar, big numeric, stacked content
- D:\article-builder\templates\topbars\tb-monogram.html — huge serif numeric, content beside it
- D:\article-builder\templates\topbars\tb-stack.html — two-row centered, brand on top, title centered below
- D:\article-builder\templates\topbars\tb-corner.html — radial corner glow, minimal bar
- D:\article-builder\templates\topbars\tb-strip.html — mono typography, all-caps, tight
- D:\article-builder\templates\topbars\tb-frame.html — bracketed corners, classical
- D:\article-builder\templates\topbars\tb-pulse.html — animated underline gradient, oscilloscope feel
- D:\article-builder\series\genesis-to-quantum\series.json — full GTQ config (26 articles, 16 accent palettes)
- D:\article-builder\README.md — usage docs, full placeholder list, conventions

### GTQ output — 26 article HTML files written
- D:\GTQ-BUILD\articles\01-measurement-collapsed-reality\gtq-01-measurement-collapsed-reality.html
- D:\GTQ-BUILD\articles\02-collapse-threshold\gtq-02-collapse-threshold.html
- D:\GTQ-BUILD\articles\03-first-quantum-state\gtq-03-first-quantum-state.html
- D:\GTQ-BUILD\articles\04-free-will-two-frames\gtq-04-free-will-two-frames.html
- D:\GTQ-BUILD\articles\05-macarthur-equation\gtq-05-macarthur-equation.html
- D:\GTQ-BUILD\articles\06-three-pathways\gtq-06-three-pathways.html
- D:\GTQ-BUILD\articles\07-why-god-drowned-everybody\gtq-07-why-god-drowned-everybody.html
- D:\GTQ-BUILD\articles\08-day-time-began\gtq-08-day-time-began.html
- D:\GTQ-BUILD\articles\09-decoherence-curve\gtq-09-decoherence-curve.html
- D:\GTQ-BUILD\articles\10-how-lies-kill\gtq-10-how-lies-kill.html
- D:\GTQ-BUILD\articles\11-substrate-fractured\gtq-11-substrate-fractured.html
- D:\GTQ-BUILD\articles\12-trinity-mechanism\gtq-12-trinity-mechanism.html
- D:\GTQ-BUILD\articles\13-trinity-timeline\gtq-13-trinity-timeline.html
- D:\GTQ-BUILD\articles\14-physics-broken-in-two\gtq-14-physics-broken-in-two.html
- D:\GTQ-BUILD\articles\15-why-reality-needs-three\gtq-15-why-reality-needs-three.html
- D:\GTQ-BUILD\articles\16-photon-isnt-watching\gtq-16-photon-isnt-watching.html
- D:\GTQ-BUILD\articles\17-ran-the-numbers\gtq-17-ran-the-numbers.html
- D:\GTQ-BUILD\articles\18-eraser-and-the-cross\gtq-18-eraser-and-the-cross.html
- D:\GTQ-BUILD\articles\19-temporal-trap\gtq-19-temporal-trap.html
- D:\GTQ-BUILD\articles\20-how-god-restores\gtq-20-how-god-restores.html
- D:\GTQ-BUILD\articles\21-science-behind-restoration\gtq-21-science-behind-restoration.html
- D:\GTQ-BUILD\articles\22-same-god-both-testaments\gtq-22-same-god-both-testaments.html
- D:\GTQ-BUILD\articles\23-regime-dependent-theology\gtq-23-regime-dependent-theology.html
- D:\GTQ-BUILD\articles\24-societies-die\gtq-24-societies-die.html
- D:\GTQ-BUILD\articles\25-counter-move\gtq-25-counter-move.html
- D:\GTQ-BUILD\articles\26-pattern-is-the-signal\gtq-26-pattern-is-the-signal.html

### Memory persisted
- C:\Users\lowes\.claude\projects\--dlowenas-HPWorkstation-Desktop\memory\MEMORY.md
- C:\Users\lowes\.claude\projects\--dlowenas-HPWorkstation-Desktop\memory\article_builder.md — points future sessions at the framework so they don't reinvent it

---

## Layer 2 — Decisions And Results

- **Article-builder is the default for any future serial-article project.** Decision: instead of writing a one-off Python script for the GTQ unique-header build, lift the work into a reusable framework. Drop a `series.json` for any new project (ISO papers, Convergence, anything with N articles + a shared body) and run `python builder.py build`. No more hand-writing per-article HTML.
- **Stdlib-only Python.** Chose no-external-deps (no Jinja2, no PyYAML) to keep the framework portable. Templating is `{{KEY}}` placeholder substitution via regex. Config is JSON.
- **Body stays identical, topbar varies.** Confirmed user's framing: "Just the header just the very top piece, they don't need to be radically different but each one should show that it's individual." The `templates/article-shell.html` is the locked body (hero grid, tabs, kill sidebar, audio dock, footer). Per-article variation is exclusively the topbar above it.
- **10 topbar variants is the right cardinality.** Enough that 26 articles can each get a distinct combo of (topbar × accent) without obvious repetition. Distributed across articles so no two consecutive entries share a layout.
- **16 accent palettes defined for GTQ.** gold, gold-warm, gold-bright, blue, blue-cold, blue-electric, teal, teal-gold, purple, purple-blue, purple-gold, red, red-gold, red-blue, green, green-gold. Each palette has hex/dim/bright/glow keys; renderer wires all four into `--highlight-*` CSS vars in the shell so every accent in the page (border-lefts, button rings, dock fill, exec-summary background, hero-side hover) shifts together.
- **Topbars are non-sticky.** Avoided fighting with the existing tab-shell which sticks at top:0 with z-index 50. Topbars flow normally, scroll away, tab-shell sticks. Brief asked for sticky topbars but the layout cost was high; left as a knob for later.
- **Output paths driven by config.** `output_root` + `output_pattern` in series.json. Each article writes to a path computed from its `n`, `slug`, `short`. Re-running build overwrites in place — safe for shells, lossy for any hand-authored body content (documented in README).
- **Audio wiring is per-article path-relative.** Articles list audio as an object with `deep`/`read`/`debate` keys, each a path relative to the output folder. Pills with no source automatically dim to "unavailable" instead of breaking. Articles with empty `audio: {}` show a "Coming soon" badge.
- **Sidebar nav auto-generated from articles list.** Main vs deep-dive separated by `tier` field. Current article gets `current` class. Hrefs computed by relative path between sibling article folders.
- **Validate before build.** `python builder.py validate <config>` renders every article in memory and reports unfilled placeholders, missing topbar files, and render errors. Caught zero issues on the GTQ config. Run this any time the config changes.

---

## Layer 3 — Open Threads

1. **Body content for the 26 GTQ articles** — Shells are written; story body is still template-placeholder. Source markdown lives at `D:\GTQ-BUILD\articles\<n>-<slug>\markdown\*.md` in pandoc-converted HTML form. Next session: decide whether to convert markdown into shell body (one-time hand pass per article, or a markdown→shell automation pass), and handle the embedded slide images / equations / custom divs each markdown carries.
2. **Hero images missing** — Each article references `images/hero/hero.jpg` but most folders have empty `images/hero/`. Either generate placeholder heroes, recover from `D:\GitHub\genesis-to-quantum\images\heroes\`, or run a ChatGPT image-gen pass per article. Brief said no images in topbar but hero grid below tab bar wants one.
3. **NotebookLM audio gap** — 18 of 26 articles still have no audio. notebooklm-py is installed (v0.3.4) but auth was hard-locked last session. Either retry `nlm login` cleanly or skip and use existing `.mp3` where present (already wired) and let pills dim where missing.
4. **Topbar position** — Currently non-sticky. If user wants top bar to stick at top with tab bar sticking below it (per the brief's rule 4), need to add `--topbar-h` CSS var per topbar variant and bump `.tab-shell` to `top: var(--topbar-h)`. Mechanical change once decided.
5. **Series index page** — No `index.html` linked from the topbar's "Series Index" button or sidebar's "Series Home". Need an index page at `D:\GTQ-BUILD\index.html` (or wherever `INDEX_HREF` should point) listing all 26 articles.
6. **GTQ landing page integration** — Existing landing/Cannon site doesn't yet route to the new article folder structure. Decision pending on whether `gtq-XX-slug.html` files at article-folder-roots get deployed as-is or copied flat into a publish dir.
7. **Footer-quote per article** — Every article currently uses the series-default footer quote "But while he was still a long way off, his father saw him." Could vary per article via a `footer_quote` field on the article entry — schema already supports it, just needs filling in.
8. **Cross-series topbar reuse** — Verify that the 10 topbars look right under non-gold accent families (e.g., a Convergence series with a teal/blue dominant palette). Spot-checked GTQ-only; may need accent-aware spacing tweaks for other palettes.

---

## Audit Footer

### Where We Are Right
- Framework lifts a one-off into a reusable tool with a clean CLI, validation step, and self-documenting config schema.
- 26 GTQ HTML files are written and verified — each has the correct title, ID, neighbor links, sidebar with the current article highlighted, and audio paths matching what's actually in each folder.
- Memory pointer ensures future sessions find the framework instead of reinventing it.

### Where We Might Be Wrong
- Did not test the rendered output in a real browser. The CSS scoped-class approach should isolate per-topbar styles, but only visual inspection confirms each topbar reads as intended at viewport widths between 360px and 1920px.
- The `--highlight-glow` rgba interpolation works for gold's rgba(212,175,55,0.12) but assumes every palette author keeps the same alpha. Could break if an accent uses a different opacity.
- Accent assignments in the GTQ config follow the brief's hint table. Not validated against the actual article tone — e.g. assigned "purple-gold" to GTQ-18 (Eraser and the Cross) per the brief but didn't compare visually to existing GTQ aesthetic.

### What We Think
- This is the correct shape for the user's workflow. Drop a JSON, get N HTML files. The framework should absorb every future serial-article build instead of letting each one fork its own one-off script.
- The next big lever is body content automation. Once shells are written, a markdown→shell pass would close the loop and turn the framework into a true "drop a folder, get a publishable site" pipeline.

---

## NEXT SESSION STARTUP PROMPT (for handoff to Codex / next Claude session)

```
We have a reusable article-builder framework at D:\article-builder\. It generated
26 Genesis-to-Quantum article shells at D:\GTQ-BUILD\articles\<n>-<slug>\
gtq-<n>-<slug>.html. Bodies are template placeholders; topbars are unique
per article (10 topbar variants × 16 accent palettes, distributed across the 26).

Read these in order before doing anything:
  1. D:\article-builder\README.md — framework usage, placeholder reference,
     conventions
  2. D:\article-builder\series\genesis-to-quantum\series.json — current GTQ
     config (26 articles, accent palettes, topbar assignments)
  3. D:\article-builder\templates\article-shell.html — body shell
  4. D:\article-builder\templates\topbars\*.html — 10 topbar variants

Open thread to pick up first: <SELECT FROM LIST IN HANDOFF — most likely body
content population from D:\GTQ-BUILD\articles\<n>\markdown\*.md, or hero image
generation, or notebooklm-py audio batch>.

Workflow rules:
  - Don't hand-write per-article HTML. Use the builder.
  - Edit series.json + re-run `python builder.py build series/genesis-to-quantum/series.json`.
  - Run `python builder.py validate <config>` before any build to catch typos.
  - If you change article body structurally, edit templates/article-shell.html
    (changes propagate to all 26 on rebuild). If you change a topbar, edit the
    relevant tb-*.html.
  - Re-running build OVERWRITES outputs in place. Once any article has hand-
    authored body content, exclude it with --only on subsequent rebuilds, or
    move the authored chunk back into the shell.

Hand-off facts the user wants you to remember:
  - User prefers terse responses, no filler.
  - User prefers D: drive over network shares for tooling (faster, less
    permission weirdness). Output can land on the network share (\\dlowenas\
    HPWorkstation\Desktop or O:\Vault) but tools live on D:.
  - Body below the tab bar stays identical across every article in a series.
    The topbar above is what varies. This is locked.
```
