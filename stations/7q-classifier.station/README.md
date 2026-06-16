# 7QS Refined Toolkit

This package is a cleaned-up version of the uploaded 7Q scripts.

The big change is conceptual:

**The Seven Questions are the center.**

Each paper can be processed through three modes:

| Mode | Public Name | Purpose |
|---|---|---|
| F | Foundations | What the claim builds and requires |
| R | Reversals | What breaks it, collapses it, or falsifies it |
| E | Evidence | What reality, literature, or data says about it |

This keeps the human layer simple while preserving the machine layer underneath.

---

## Files

### `seven_q_core.py`
Shared utilities, scoring, JSON parsing, OpenAI client wrapper, canonical question registry.

### `seven_q_runner_refined.py`
Runs the full Seven Questions analysis:

- Foundations
- Reversals
- Evidence

Outputs:

- JSON
- readable Markdown
- legacy-compatible `forward_7q` and `reverse_7q` keys

### `integration_pass_refined.py`
Renamed and cleaned-up version of the old Promotion Pass.

It runs after a claim survives Reversals Mode and builds:

- framework posture
- confidence gradient
- isomorphism map
- literature targets
- equivalent forms
- predictions
- integration verdict

### `seven_q_template_builder_refined.py`
Builds a clean Proof Explorer / Obsidian-ready Markdown page from 7QS JSON and optional Integration JSON.

---

## Basic Usage

Set your API key:

```bash
set OPENAI_API_KEY=your_key_here
```

Run one paper:

```bash
python seven_q_runner_refined.py --paper "path/to/paper.md" --output "path/to/_7QS_ANALYSIS"
```

Run a folder:

```bash
python seven_q_runner_refined.py --folder "path/to/series" --output "path/to/_7QS_ANALYSIS"
```

Run Integration Pass:

```bash
python integration_pass_refined.py --paper "path/to/paper.md" --seven-q "path/to/paper_7QS_YYYY-MM-DD.json" --output "path/to/_7QS_ANALYSIS"
```

Build a Proof Explorer page:

```bash
python seven_q_template_builder_refined.py --seven-q "path/to/paper_7QS_YYYY-MM-DD.json" --integration "path/to/paper_INTEGRATION_YYYY-MM-DD.json" --output "path/to/PAGES"
```

---

## Naming Grammar

Use this publicly:

- **Seven Questions**
- **Foundations**
- **Reversals**
- **Evidence**
- **Integration Pass**

Use this internally:

- `Q1-F`, `Q1-R`, `Q1-E`
- `Q2-F`, `Q2-R`, `Q2-E`
- etc.

That keeps the public language human while leaving machine structure intact.

---

## Important Note

This toolkit does not make the framework true.

It makes the framework auditable.

That is the point.
