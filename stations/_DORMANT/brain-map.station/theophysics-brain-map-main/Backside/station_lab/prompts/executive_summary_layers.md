# Executive Summary Layer Prompt

Use this prompt when the deterministic station output needs an LLM polish pass.

## Inputs

- Source opening hook
- Load-bearing claim signals
- First formal/math anchor
- Section map
- Math-layer candidate count

## Task

Write three summaries of the same paper.

### Accessible Layer

Audience: intelligent non-specialist.

Rules:

- No jargon unless immediately translated.
- Keep the central claim vivid and concrete.
- Do not overclaim proof.
- End by naming why the piece matters.

### Medium Layer

Audience: David / internal collaborator / serious reader.

Rules:

- Preserve Theophysics terms.
- Name the structural bridge being attempted.
- Identify the first load-bearing claim.
- Name what still needs tuning.

### Academic Layer

Audience: adversarial academic reviewer.

Rules:

- Formal, cautious, and falsification-aware.
- Separate model, analogy, evidence, and proof.
- Name the key equation or statistic only if it constrains the claim.
- Include one sentence on what would need to be operationalized.

## Output

Return Markdown with:

```markdown
## Accessible Layer

## Medium Layer

## Academic Layer

## Reviewer Risk
```
