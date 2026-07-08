# readability-rewriter.station

## Purpose
Takes a section written at one reading level and produces a rewrite at a target level WITHOUT breaking structural fidelity. This is controlled decompression (academic -> 8th grade) or controlled compression (natural -> formal academic), not simplification.

## Input
- Section text
- Source reading level (auto-detected or specified)
- Target reading level: "8th-grade" | "undergraduate" | "academic" | "formal"
- Constraint set: { preserve_equations: bool, preserve_terms: [list], preserve_logic_chain: bool }

## Output
- Rewritten section at target level
- Flesch-Kincaid score before and after
- Structural fidelity report: which logical dependencies survived, which were decomposed
- Diff summary: what changed and why

## Model Dependencies
- 06_llm via Ollama (primary rewriter — needs carefully crafted prompts)
- Optional: external LLM API for higher quality rewrites
- 02_embedder (semantic similarity check: original vs rewrite)

## Workflow Lanes
- Publication Layer (multi-tier article generation)
- Website content pipeline (click-to-switch reading levels)

## Status: SKELETON — needs implementation, heavy prompt engineering required

## Notes
This is the hardest station to get right. The failure modes are:
1. Decompression that loses structural relationships (dumbing down)
2. Academic tightening that introduces jargon the original didn't need
3. Either direction breaking equation context or term meaning

The prompt engineering will go through many iterations. The station shape stays the same — input section + target level + constraints, output rewrite + fidelity report.

Two separate prompt chains needed:
- DECOMPRESS: academic -> 8th grade (harder — must explain without metaphorizing)
- COMPRESS: natural -> formal academic (easier — tighten, cite, formalize)

The preference engine should eventually bias this station: if the user consistently edits the 8th-grade output to add back certain technical terms, the rewriter learns to keep those terms.

Key constraint for Theophysics: "structural mapping" must never become "metaphor." The rewriter must understand that when we say entropy IS the adversary, that's not a comparison — it's an identification. The 8th-grade version must preserve that claim even if it takes three paragraphs to set it up.
