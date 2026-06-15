# MDA Math NLP Review Gate

Purpose: verify Math Translation Layer output before it enters reading levels, HTML, TTS, or deploy-ready artifacts.

This station reviews translated math spans. It does not prove equations and does not rewrite articles. It checks whether MTL preserved the mathematical structure while making the terms readable.

## Required Inputs

- `math_translation_layer.translated_spans` from the paper snapshot or standalone MTL JSON
- original equation span from Markdown or HTML
- same-structure word equation emitted by MTL
- plain-language explanation emitted by MTL or reviewed Easy Math text
- dictionary/canon version used

## Required Output

Write:

`math_nlp_review.csv`

Required columns:

- `article_id`
- `source_span_id`
- `original_equation`
- `word_equation`
- `plain_explanation`
- `structure_callouts`
- `structure_preserved`
- `layman_terms_clear`
- `added_meaning_risk`
- `dictionary_coverage`
- `review_notes`

## Pass Conditions

- `structure_preserved=pass`
- `layman_terms_clear=pass`
- `added_meaning_risk=none` or `low`
- all symbols are dictionary/canon-backed or explicitly marked `unmapped`
- `structure_callouts` points back into the equation and explains the load-bearing pieces

## Structure Callout Rule

The explanation must not float away from the math. It should point back to the visible equation structure one to three times so the reader can see why the equation works.

For small equations, call out the one or two decisive parts.

For large equations, call out the five or so parts that matter most, such as:

- the term that multiplies everything
- the denominator that suppresses output
- the exponent or threshold that creates nonlinear transition
- the derivative that shows rate of change
- the source, sink, conserved remainder, or loss term

Each callout should say why that part matters in simple language. Examples: multiplication means every factor participates; division means one part suppresses or normalizes another; a threshold means the behavior changes after a boundary; a derivative means the equation is about change over time.

## Fail / Hold Conditions

Send the span to `..\04_EDIT_QUEUE\math-layer\` if:

- the word equation changes operator order, arity, term count, or dependency structure
- the explanation adds a new causal claim, certainty level, theological conclusion, or mathematical conclusion
- a symbol is translated without reviewed dictionary/canon support
- the output is only an analogy and does not preserve the equation shape
- the explanation does not refer back to the equation structure or fails to identify the load-bearing parts

## HTML Requirement

Any promoted math span should expose three layers where applicable:

1. original equation
2. same-structure word equation
3. simple explanation
