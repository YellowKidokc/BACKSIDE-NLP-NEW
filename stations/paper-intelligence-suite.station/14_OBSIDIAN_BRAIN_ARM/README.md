# 14_OBSIDIAN_BRAIN_ARM

This module is the vault-intake companion to the paper intelligence suite.

It answers a different question than the 12-layer paper scorer:

- `00_ORCHESTRATOR/run_pipeline.py` asks: **What does this paper score on the full intelligence stack?**
- `14_OBSIDIAN_BRAIN_ARM/obsidian_pipeline.py` asks: **What is this vault folder structurally made of, how should each document be classified, and what browser-ready digest should we emit?**

Together they provide the programmable trail from raw vault material to
paper-grade scoring:

1. Run the folder through **Paper Intelligence** for rigorous metrics.
2. Run the same folder through the **Brain Arm** for document inventory,
   classification, digest HTML, and sidecar CSV/JSON.
3. Compare the outputs with
   `00_ORCHESTRATOR/run_brain_alignment.py`.

## Files

- `obsidian_pipeline.py`
  The intake/classification engine ported from the working deployment build.
- `run_obsidian_brain.py`
  Small CLI wrapper for vault/subfolder sync into this suite's `OUTPUT/`.

## Quick start

```bash
cd T:\THEOPHYSICS_PAPER_INTELLIGENCE
python 14_OBSIDIAN_BRAIN_ARM\run_obsidian_brain.py --vault "O:\_Theophysics_v5\04_THEOPYHISCS\AI Knowledge"
```

## Alignment mode

```bash
cd T:\THEOPHYSICS_PAPER_INTELLIGENCE
python 00_ORCHESTRATOR\run_brain_alignment.py --folder "O:\_Theophysics_v5\04_THEOPYHISCS\AI Knowledge"
```

That command runs both systems and writes:

- Paper-intelligence outputs
- Brain-arm digest outputs
- `alignment_summary.json`
- `alignment_join.csv`

The goal is not duplication. The goal is traceable agreement between
document classification and paper scoring.
