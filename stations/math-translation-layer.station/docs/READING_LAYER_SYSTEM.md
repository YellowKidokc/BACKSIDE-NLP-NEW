# Reading Layer System

Source: Opus architecture spec from David direction, received 2026-06-01.

## Purpose

The page ships as one article with five reader layers:

- `easy`
- `standard`
- `math`
- `academic`
- `claims`

`standard` is active by default and remains the source voice. Other layers are generated sidecars or station outputs, then woven into the page.

## Source Contract

Use Option B:

- `article.md` - standard source of truth
- `article.easy.md` - 8th grade rewrite
- `article.academic.md` - formal academic rewrite
- `article.claims.json` - claim cards from claim extractor / paper proof grader
- `article.math.json` - math catalog and translation output from math translation layer

The standard markdown should stay untouched.

## HTML Contract

Content that swaps by reading level is wrapped:

```html
<div data-level="standard">...</div>
<div data-level="easy">...</div>
<div data-level="academic">...</div>
```

Math and claims do not replace the standard article. They add panels/cards:

```html
<div class="math-expand" data-level="math">...</div>
<div class="claim-card" data-level="claims">...</div>
```

## Layer Behavior

- `standard`: default article, David voice.
- `easy`: simpler register, same facts.
- `math`: opens math panels beneath equations.
- `academic`: formal academic register.
- `claims`: shows inline claim cards with maturity, 7Q fields, kill conditions, and verification status.

## Build Order

1. Topbar and toggle JS.
2. Claims integration.
3. Math integration.
4. Scanner for missing easy/academic work.
5. Easy rewrite generation.
6. Academic rewrite generation.
7. Final HTML assembler.

## Boundary Rule

The Claims layer does not make the page unquestionable. It exposes what can be questioned, what has evidence, what is personal belief, what is formal, and what still needs repair.
