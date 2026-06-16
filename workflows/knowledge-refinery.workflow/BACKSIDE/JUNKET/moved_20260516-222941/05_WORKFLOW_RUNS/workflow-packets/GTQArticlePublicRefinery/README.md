# GTQArticlePublicRefinery

End-to-end public article refinery for Genesis-to-Quantum / Theophysics HTML pages.

This workflow is not the paper grader. It is the publishing workflow David needs first: take an HTML article, extract its readable content, map each section/paragraph to canon anchors, prepare AI review prompts, and produce the review artifacts needed before the page goes online.

## Purpose

For each article, produce:

- public-facing executive summary
- explain-it-simply pass
- Master Equation / variable / operator mapping
- axiom and formal-proof mapping
- math translation review packet
- rigor and kill-condition review packet
- glossary candidates above normal-reader level
- post-ready summary
- publish checklist

## Standard Run

Put `.html` files into `INPUT`, then run:

```text
RUN_PIPELINE.bat
```

Or run one file directly:

```text
python SCRIPTS\run_refinery.py --input "path\to\article.html"
```

Outputs go to:

```text
OUTPUT\<article-slug>\
REVIEW\<article-slug>\
```

## Current Design

The deterministic runner does extraction and first-pass candidate mapping. AI partners then use the generated prompt packet to fill the judgment-heavy layers:

- whether a mapping is real or only loose analogy
- whether a claim overreaches
- whether a math translation is coherent
- whether a kill condition actually breaks the article claim

## Canon Sources

The default canon reference list is configured in:

```text
CONFIG\canon_sources.example.json
CONFIG\canon_terms.json
```

Use this as the control-plane map. Do not copy heavy canon vaults into this repo.
