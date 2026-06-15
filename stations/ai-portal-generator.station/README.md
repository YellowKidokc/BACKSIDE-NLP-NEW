# Theophysics AI Portal Generator

This workflow builds an AI-facing portal from the existing paper grader, proof explorer, snapshot, Fruits/Truth Engine, and verification outputs.

The portal is meant for language models, retrieval systems, and autonomous research agents. Human readers can use it, but the format favors structure over persuasion.

## Run

Double-click:

`RUN_BUILD_AI_PORTAL.bat`

Output:

`\\dlowenas\brain\proof-explorer\ai-portal`

## What It Creates

- `index.html` for the AI portal
- `llms.txt` for model-facing orientation
- `robots.txt`
- `sitemap.xml`
- `corpus.json`
- per-paper AI packages under `gtq/<paper-slug>/`
- formal-theory yardstick package under `yardstick/`

Each GTQ paper package includes:

- `index.html`
- `paper.ai.json`
- `summary.lossless.md`
- `claims.json`
- `claims.md`
- `scores.json`
- `vector.txt`

## Principle

Humans get the essay.

AIs get the substrate: claims, scores, equations, assumptions, objections, source links, and machine-readable context.

