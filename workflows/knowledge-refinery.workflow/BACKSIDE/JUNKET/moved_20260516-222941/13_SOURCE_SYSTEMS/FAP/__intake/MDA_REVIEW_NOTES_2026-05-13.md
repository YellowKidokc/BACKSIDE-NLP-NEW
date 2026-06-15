# Moral Decline of America intake review notes

Session started: 2026-05-13 evening
Reviewer: codex-forge
Scope: `mda-01-introduction.html` through `mda-10-way-back.html`

## Working rule

Capture David's talking notes per file first. Apply only low-risk fixes immediately. Defer larger copy/structure decisions until the series-level pattern is visible.

## File 01 - `mda-01-introduction.html`

Path: `\\dlowenas\brain\knowledge-refinery\13_SOURCE_SYSTEMS\FAP\__intake\mda-01-introduction.html`
Size: 54,718 bytes
Last modified before review: 2026-05-05 17:20:18

### Current structure

- H1: The Equation Nobody Wanted
- H2: The Dataset Nobody Compiled
- H2: The Five-Year Window
- H2: What the Equation Predicts
- H2: What This Series Will Do
- H2: The FACTS Framework
- H2: A Note on What This Is
- H2: Related Work

### Initial technical notes

- File loads external Tailwind, MathJax, Font Awesome, Google Fonts, analytics, and `/glossary-linker.js`.
- Local intake-folder link check: `mda-02-phase-transition.html` exists.
- Local intake-folder link check: `index.html`, `../index.html`, and `mda-america.html` do not exist in or above `__intake`.
- One `NaN` string is present only inside the audio time formatter guard, not as visible broken article content.

### David talking notes

- Pending.

### Fix/deploy decision

- 2026-05-13: David flagged visible body text running hard against the screen edge on the first pages.
- Confirmed root cause: missing constrained content wrappers around the post-hero audio/body region.
- Applied low-risk wrapper repair across all ten `mda-*.html` files:
  - `mda-01` and `mda-02`: restored matching outer `<main class="max-w-4xl mx-auto px-6 py-16">` wrappers and first section wrappers.
  - `mda-03` through `mda-10`: restored the missing top `<section class="max-w-4xl mx-auto px-6 py-10">` wrapper around the audio/intro block.
- Verification: all ten files now have balanced `<section>` counts; `mda-01` and `mda-02` also have balanced `<main>` counts.

## Series-wide follow-up notes

- `mda-02-phase-transition.html` and `mda-09-amish-proof.html` each still contain two `href="#"` placeholder links.
- All ten files point to `index.html`, `../index.html`, and `mda-america.html`, but those landing/index files are not present in the `__intake` folder. This may be a deployment-context issue rather than an article-content issue.
- Part 02 title says "The Anatomy of a Phase Transition" while the H1 says "Peak Signal"; that may be intentional series framing, but it is worth confirming.
