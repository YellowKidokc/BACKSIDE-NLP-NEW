# Generate Production Vault Page Layers

You are filling a Theophysics production vault page.

Do not erase David's article. Layer 3 is the source argument. Your job is to fill the surrounding layers, mark uncertainty, and preserve epistemic boundaries.

## Required Output

Return these sections:

1. Facts Header
2. Executive Summary
3. Plain English
4. Academic Summary
5. Cross-References
6. Data And Evidence
7A. Framework Impact
7B. Open Obligations

## Rules

- Every claim must preserve epistemic state.
- Do not upgrade a hypothesis into a proven result.
- Use `depends_on`, `supports`, `relates_to`, `contradicts`, and `supersedes` distinctly.
- If evidence is missing, write `[pending]`.
- If a contradiction is unresolved, mark it as a tension, not a failure.
- If a score is missing, write `0.0` and verdict `HOLD`.

## Facts Header Format

```markdown
> [!metadata] Facts
> **Paper ID:** ...
> **Status:** ...
> **Type:** ...
> **Epistemic State:** ...
> **Verdict:** ...
> **Composite Score:** ...
> **Provenance:** ...
> **Depends On:** ...
> **Supports:** ...
> **Contradicts / Tensions:** ...
```
