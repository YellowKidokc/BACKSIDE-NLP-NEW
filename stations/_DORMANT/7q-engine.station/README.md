# 7Q Engine v2

**Seven Questions. Any Claim. Any Domain. Two Directions. One Engine.**

An adversarial truth-testing framework that scores any claim through seven dimensions, outputs scored Obsidian notes with colored callouts, and optionally routes through LLMs for maximum rigor analysis.

---

## What It Does

Feed in a claim. The engine:

1. **Classifies** it across 211 labels (entity type, evidence strength, vulnerability flags, kill conditions...)
2. **Scores** it using three-channel evidence scoring (PS × CF), six category pillars (S/E/L/D/P/C), cross-domain multiplier
3. **Outputs** a fully formatted Obsidian note with YAML frontmatter, colored Q0–Q7 callouts, verdict, and knowledge graph

Two modes:
- **Forward** (Q0→Q7): Interactive intake — "What is this? What supports it? Can we kill it?"
- **Backward** (Q7→Q1): Destruction mode — "Try to kill it first. Whatever survives earns its identity."

## Quick Start

```bash
# Run the test claim
python main.py test

# Interactive forward intake
python main.py forward

# Destruction mode
python main.py backward

# LLM Maximum Rigor (requires OpenAI API key)
export OPENAI_API_KEY=sk-...
python main.py llm-full
```

## Architecture

```
7q-engine/
├── main.py              CLI entry point (6 modes)
├── id_system.py         211 classification labels, weights, domain adjustments
├── scorer.py            Three-channel evidence scoring, truth score computation
├── intake.py            Forward mode interactive CLI (Q0→Q7)
├── destroy.py           Backward destruction mode (Q7→Q1)
├── obsidian_writer.py   Generates .md notes with custom callout formatting
├── html_report.py       Per-claim HTML cover pages (dark theme, SVG tree)
├── llm_bridge.py        OpenAI API integration (full/compact/judge)
├── domains/
│   └── physics.py       Physics domain plugin (theories, isomorphisms, kill tests)
├── obsidian/
│   └── snippets/
│       └── 7q-scored-callouts.css   Custom callout colors for Obsidian
├── docs/
│   ├── 7q-explorer.html             Interactive visual explorer
│   ├── 7q-evidence.html             Evidence protocol deep dive
│   ├── 7q-reverse.html              Reverse method walkthrough
│   └── 7q-tree.html                 Animated tree visualization
└── examples/
    ├── CL-PHY-0001_example.md       Engine-generated scored note
    └── FP-008_SCORED_CLEAN.md        Reference template (the gold standard)
```

## The Seven Questions

| Q | Name | Tree Part | What It Asks |
|---|------|-----------|-------------|
| Q0 | **Arrive** | Empty soil | Why are you here? Investigation or advocacy? |
| Q1 | **Define** | Seed | What IS this thing? (theorem, law, hypothesis, claim...) |
| Q2 | **Locate** | Soil | Where does it live? How many domains? Cross-domain multiplier. |
| Q3 | **Commit** | Sprout | What exactly is being claimed? How precise? |
| Q4 | **Support** | Rain | What evidence supports it? Three-channel scoring. |
| Q5 | **Ground** | Roots | What does it depend on? Where does the chain terminate? |
| Q6 | **Propagate** | Canopy | What does it predict? Anything unique? |
| Q7 | **Destroy** | Axe | Five death types. Whatever survives is true. |

## Scoring

**Truth Score:** `T = (S + E + L + D + P + C) / 6 × XDM`

| Pillar | Source | What It Measures |
|--------|--------|-----------------|
| S | Q1 + Q3 | Structural quality (identity + assertion) |
| E | Q4 | Evidence strength (PS × CF, vulnerability penalties) |
| L | Q5 | Logical foundation (terminus quality) |
| D | Q6 | Discriminatory power (predictions, uniqueness) |
| P | Q0 | Posture (investigation vs advocacy) |
| C | Q7 | Combat survival (death test results) |

**Evidence Three-Channel:**
- PS = Phenomenon Strength (0–1)
- CF = (0.5 + 0.5 × ED) × (0.5 + 0.5 × EC)
- E = PS × CF
- WHY-PENALTY: if ED < 0.3, E capped at 0.50

**Cross-Domain Multiplier (XDM):**
| Status | Multiplier |
|--------|-----------|
| ISO-CONFIRMED 3+ domains | ×1.50 |
| ISO-CONFIRMED 2 domains | ×1.30 |
| ISO-PARALLEL 3+ domains | ×1.15 |
| Domain-bound (isolated) | ×0.90 |

**Confidence Classes:**
| Class | T Range | Meaning |
|-------|---------|---------|
| ESTABLISHED | ≥ 0.85 | Rock solid |
| WELLSUP | ≥ 0.65 | Strong |
| TENTATIVE | ≥ 0.40 | Promising |
| SPECULATIVE | ≥ 0.15 | Shaky |
| UNSUPPORTED | < 0.15 | In trouble |

## Obsidian Integration

The engine outputs `.md` files with:
- **YAML frontmatter** — searchable scores, tags, metadata
- **Tabbed overview strip** — quick glance at scores, kills, claims
- **Colored callouts** — each Q dimension has its own color via CSS snippet
- **Verdict callout** — executive summary in gold
- **Knowledge graph YAML** — machine-parseable node/edge structure
- **Machine-parseable scoring block** — hidden in `%%` comments

### Setup

1. Copy `obsidian/snippets/7q-scored-callouts.css` to your vault's `.obsidian/snippets/` folder
2. Enable it: Settings → Appearance → CSS Snippets → toggle on
3. Run `python main.py test` to generate a sample scored note
4. Open it in Obsidian — colors should render

### Callout Colors

| Callout | Color | Tree Metaphor |
|---------|-------|--------------|
| `[!q0-arrive]` | Gray (#8a8d9b) | Empty soil |
| `[!q1-define]` | Gold (#d4a853) | Seed |
| `[!q2-locate]` | Brown (#7c6340) | Soil |
| `[!q3-commit]` | Green (#6b8c42) | Sprout |
| `[!q4-support]` | Blue (#38bdf8) | Rain |
| `[!q5-ground]` | Earth (#a0724a) | Roots |
| `[!q6-propagate]` | Emerald (#34d399) | Canopy |
| `[!q7-destroy]` | Red (#ef4444) | Axe |
| `[!verdict]` | Gold (#d4a853) | — |
| `[!theory-map]` | Purple (#a855f7) | — |
| `[!graph]` | Blue (#38bdf8) | — |

## Five Universal Death Types (Q7)

| Type | What Kills It |
|------|--------------|
| **SELFREF** | Claim destroys itself if true |
| **REGRESS** | Justification chain never terminates |
| **EMPIRICAL** | Reality directly contradicts it |
| **INCOHERENT** | Contains logical contradiction (A and ¬A) |
| **EXPLAIN** | A simpler theory explains the same data |

## LLM Integration

Three prompt modes for API pipelines:

- **Full** (`llm-full`): Maximum rigor — cross-domain discovery, theory resonance (15+ families), blind spot detection, knowledge graph
- **Compact** (`llm-compact`): Quick scoring — Q0–Q7 classifications + scoring block
- **Judge** (`llm-judge`): Verification — checks a prior assessment for errors, missed vulns, inflated scores

```bash
python main.py llm-full --model gpt-4o
python main.py llm-judge --model gpt-4o
```

## Interactive Explorer

Open `docs/7q-explorer.html` in any browser. It's a self-contained visual walkthrough of the entire 7Q method with:

- **Forward/Reverse toggle** — see both directions
- **Three trace examples** — General Relativity, consciousness, entropy/moral decay
- **Layer filters** — show/hide epistemic types
- **Click-to-expand** — full detail on every node
- **Color-coded** — same Q0–Q7 palette as the Obsidian callouts

No server needed. Just open the HTML file.

## Requirements

- Python 3.10+
- No dependencies for core engine (intake, scorer, writer)
- `openai` package for LLM bridge: `pip install openai`
- `pyyaml` for knowledge graph parsing: `pip install pyyaml`

## License

MIT

## Author

David Lowe · POF 2828 · Theophysics
