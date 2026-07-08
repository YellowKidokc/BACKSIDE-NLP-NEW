# Genesis to Quantum — Agent Handoff

## What This Project Is
A website with 25 articles (10 main + 15 tangents) about the intersection of quantum physics and theology. Each article is a single self-contained HTML file. Dark theme, gold (#d4af37) and black.

## The Gold Standard
`gtq-01-measurement-collapsed-reality.html` is the template every other article should match. Study it before touching anything else.

### What GTQ-01 Has That Others Don't Yet
1. **Player strip** at top of Paper tab — 3 inline audio players (blue Deep Dive, gold Read Aloud, purple Debate) in a slim horizontal bar
2. **Player strip duplicated** on the Tangent tab
3. **Oversized Born Rule section** — 3-column gold/teal/white grid
4. **Decoherence Steps 1/2/3** — large cards with Oswald headers + Crimson Text descriptions
5. **Red gradient falsification criteria** — container that visually deteriorates claim by claim
6. **Sign-out cards** — side-by-side at bottom before footer
7. **Slide images** embedded throughout the Paper tab (7 slides from `slides/` folder — GTQ-01 specific, don't copy to other articles)
8. **Chalkboard** embedded in Media & Tools tab (canvas-based, GTQ-01 specific sketch)
9. **Custom audio players** (not default browser chrome) with play/pause/seek/mute
10. **Tab rename**: "The Paper" → article title, tangent tab → "01-A: [tangent name]"
11. **NotebookLM link** in tab bar (teal external link)

### What To Stamp Across All Articles
- The full CSS block (copy verbatim — ~800 lines)
- The player strip HTML structure (update audio URLs per article)
- The JavaScript block (audio players, tab switching, sidebar, progress bar)
- The tab bar structure
- The sidebar navigation (identical across all)
- The footer pattern
- Font stack: Crimson Text, Inter, Oswald, JetBrains Mono, Caveat, Courier Prime

### What Changes Per Article
- `<title>` and `<meta name="paper-slug">`
- Header: article number, title, subtitle, domain tags, date
- Tab button labels (article title replaces "The Paper", tangent names)
- Audio source URLs: `https://r2.faiththruphysics.com/audio/gtq-XX/read.mp3`
- Article body content (the `<section id="paper">` innerHTML)
- Summary tab content
- Rigor & Kill Conditions tab content
- Tangent tab(s) — some articles have 0, some have 3
- Media tab content (video, NotebookLM links vary)
- Prev/Next navigation links

## Audio URL Pattern
```
Read Aloud:  /audio/gtq-XX/read.mp3
Deep Dive:   /audio/gtq-XX/[filename].m4a  (if exists)
Debate:      /audio/gtq-XX/[filename].m4a  (if exists)
```

Not all articles have deep dive or debate podcasts yet. If no audio exists, hide that player.

## File Locations
- HTML output: `D:\GitHub\genesis-to-quantum\genesis-to-quantum\`
- Markdown sources: `O:\_Theophysics_v3\04_THEOPYHISCS\___THE CONVERGENCE TX 6.6\GENESIS TO QUANTUM The Seven-Article Series\`
- Pipeline data: `D:\GitHub\genesis-to-quantum\THEOPHYSICS_PAPER_INTELLIGENCE\OUTPUT\`
- Slides (GTQ-01 only): `D:\GitHub\genesis-to-quantum\genesis-to-quantum\slides\`
- Audio upload script: `D:\GitHub\genesis-to-quantum\UPLOAD_GTQ_AUDIO_STRUCTURED.ps1`

## Pipeline Data Available
The pipeline JSON has per-paper scores for:
- L1: word_count, reading_time, header_count, keywords
- L2: academic_grade, structure_score, external_theories
- L3: chi_score, chi_status, ckg_tier, wisdom_knowledge_ratio, fruits_composite, dominant_fruit, scripture_refs, cross_domain_bridges
- L5: key_sentence_1/2/3 (useful for auto-summary)
- L6: truth_score, coherence_score

## Design System
```
Colors:
  --gold: #d4af37      (primary accent)
  --blue: #4a9eff      (deep dive player)
  --purple: #a855f7    (debate player)
  --teal: #2dd4bf      (NotebookLM, bridges)
  --red: #ef4444       (falsification, kill conditions)
  --surface: #0a0a0a   (background)
  --border: #333333

Fonts:
  Crimson Text   — body text (serif)
  Inter          — UI, labels (sans)
  Oswald         — display headings, step labels
  JetBrains Mono — code, equations, metadata
```

## Task For Codex
For each of the 24 non-GTQ-01 articles:
1. Open the existing HTML file
2. Replace the CSS block with GTQ-01's CSS (verbatim)
3. Replace the JS block with GTQ-01's JS (minus the chalkboard engine — that's GTQ-01 specific)
4. Add the player strip to the top of the Paper tab
5. Add the player strip to the top of the Tangent tab (if it has one)
6. Update audio URLs to match that article's slug
7. Rename tab buttons (article title, tangent names)
8. Keep all existing article body content — DO NOT rewrite or regenerate content
9. Keep existing Summary and Rigor tab content
10. Verify the file renders (no unclosed tags, no broken CSS)

## What NOT To Do
- Don't regenerate article body text from markdown — the HTML versions may have been hand-edited
- Don't add slide images to articles other than GTQ-01
- Don't add the chalkboard canvas to other articles
- Don't change the sidebar navigation structure
- Don't modify the index.html landing page
- Don't touch the pipeline code
