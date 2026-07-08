# GTQ-03 Easy Workflow Map - 2026-05-20

Source artifact:

```text
\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready\02-genesis-to-quantum\gtq-03-first-quantum-state.html
```

Pilot outputs already generated:

```text
X:\EXPORTS\conversion-layer\20260520-133121_gtq-03-first-quantum-state_41cc8292c4\
X:\EXPORTS\lossless-context\gtq-03-first-quantum-state\
```

Click-run pilot:

```text
Backside\workflows\lossless-context.workflow\RUN_GTQ03_LOSSLESS_PILOT.bat
```

## First Read

GTQ-03 is a good calibration article because it contains every hard thing the future contradiction engine must handle:

- real HTML shell with tabs, media, style, and JavaScript
- main article body
- summary layer
- rigor/kill-condition layer
- bottom audit layer
- mathematics layer
- glossary layer
- quantum equations
- scripture/theology terms
- explicit cross-domain claims
- public-facing overstatement risk

The current deterministic pipeline can get close enough to prove the shape. It is not yet good enough to trust as the final contradiction substrate without a second pass.

## Actual Pilot Result

From the first real run over converted GTQ-03 Markdown:

| Object | Count |
|---|---:|
| Blocks | 229 |
| Claims | 74 |
| Evidence chains | 4 |
| Kill / repair items | 11 |
| Equation semantics | 48 |
| Domain boundaries | 5 |
| Mechanism edges | 13 |
| Open threads | 4 |

Address assigned:

```text
THEOPHYSICS/GTQ-03-FIRST-QUANTUM-STATE-CANONICAL/W/AI_RESEARCH/R/R1 :: G3M3E3S0T3K3R3Q0F3C3 :: E3Q0-C3S0-G3F3-K3R3-M3T3
```

Four-score dashboard from deterministic rules:

| Track | Result | Trust level |
|---|---|---|
| Academic Readiness | A / 100 | too generous; needs calibration |
| Framework Coherence | A / 100 | directionally useful |
| Public Communication | F / 46 | useful signal; overstatement-sensitive |
| Risk | HIGH / 100 | useful signal |

## What The Pipeline Got Right

- It found the article as a high-coherence, high-risk, cross-domain artifact.
- It extracted a large claim set rather than only summarizing the article.
- It found equations such as `|\psi\rangle = \alpha|0\rangle + \beta|1\rangle`, `|\alpha|^2 + |\beta|^2 = 1`, and the Eden-state expression.
- It flagged cross-domain terms: `entropy`, `coherence`, `information`, `field`, `meaning`.
- It separated permanent address from grades.
- It generated JSON and HTML snapshots without manual editing.

## What It Got Wrong

- Some layout fragments became claims, e.g. article labels and `PhysicsQuantumTheology`.
- Equation variable extraction is too naive for LaTeX; it treats commands/fragments like `rangle`, `pm`, and text labels as variables.
- Evidence extraction is weak because this HTML does not expose normal citation markup in the converted Markdown.
- Bridge detection is too conservative in some places and misses explicit bridge paragraphs.
- Academic Readiness scoring is inflated by equation count and block count.
- The conversion layer preserved mojibake from the source text, e.g. `Ã¢â‚¬â€`; this needs an encoding repair station or source cleanup.

## Easy Isolated Workflows

These are small enough to assign as isolated stations or one-prompt AI tasks.

### 1. HTML To Canonical Markdown

Input: GTQ HTML.

Output: clean canonical Markdown + conversion metadata.

Why easy: already works through `Backside/conversion_lib`.

Acceptance:

- removes navigation/script/style noise
- keeps main paper, audit, mathematics, glossary
- preserves equations
- logs warnings
- fixes mojibake if possible

### 2. Section Map Extractor

Input: canonical Markdown or HTML.

Output: `section-map.json`.

Why easy: headings and tab IDs are explicit.

Sections to preserve:

- Article identity
- Paper
- Summary
- Rigor & Kill Conditions
- Bottom Audit
- Media
- Blackboard
- Mathematics
- Glossary

### 3. Claim Candidate Cleaner

Input: `claim_arch` from lossless JSON.

Output: filtered claim list.

Why easy: remove obvious layout fragments and short non-claims.

Rules:

- drop blocks below useful length unless they contain equation/kill language
- drop nav/audio/media labels
- drop concatenated tag strings like `PhysicsQuantumTheology`
- keep high-density paragraphs

### 4. Equation Semantics Cleaner

Input: `eq_sem`.

Output: equation cards with better variable extraction.

Why easy: regex and LaTeX cleanup can improve this quickly.

Acceptance:

- ignore LaTeX commands as variables
- keep displayed equations
- identify presentational vs operational equations
- flag undefined variables
- flag derivation absent/present

### 5. Domain Boundary Pass

Input: Markdown + claim list.

Output: domain boundary table.

Why easy: terms are known and repeated.

Terms:

- entropy
- coherence
- information
- field
- proof
- law
- grace
- faith
- meaning
- measurement
- observer
- collapse

### 6. Evidence Bridge Pass

Input: claim list + nearby evidence/citation blocks.

Output: `evidence_chain.connection_to_claim`.

Why easy for LLM, hard for regex.

LLM should fill only:

- tested thing
- connection to claim
- gap
- counterevidence present

### 7. Kill Condition Extractor

Input: Falsification Criteria + bottom audit + rhythm aside kill-condition blocks.

Output: `kill_arch`.

Why easy: kill language is explicit.

Acceptance:

- distinguish stated kill from implicit kill
- preserve hostile physicist / careful theologian burden
- identify rhetorical armor

### 8. Overstatement Scanner

Input: canonical Markdown.

Output: overclaim table + safer rewrite candidates.

Why easy: keyword list and local sentence extraction.

High-risk words:

- proves
- impossible
- undeniable
- only
- definitive
- settled
- exact / precisely when used across domains

### 9. Bottom Audit Extractor

Input: HTML or Markdown.

Output: audit card JSON.

Why easy: bottom audit has strong headings:

- What We Got Carried Away With
- What Is Suggestive
- What Is Load-Bearing
- What We Got Right

This is valuable because the article already contains its own humility layer.

### 10. Glossary Extractor

Input: glossary tab.

Output: `term -> definition -> domain -> drift risk`.

Why easy: glossary is structurally isolated and already tabbed.

### 11. Reviewer Seed Generator

Input: top claims + domain boundaries + equation cards.

Output: hostile reviewer seeds.

Why easy for LLM.

Reviewers:

- skeptical physicist
- careful theologian
- academic philosopher
- information theorist
- methodologist
- friendly editor

### 12. Four-Score Calibration

Input: lossless JSON.

Output: revised score ledger.

Why needed: current Academic Readiness score is too generous.

Rule:

- do not reward equation count unless equation roles and derivations are filled
- do not reward claim count unless evidence bridge exists
- risk rises with cross-domain assertion without bridge

### 13. Reconstruction Test

Input: lossless JSON only.

Output: AI reconstruction report.

Why easy: prompt-only test.

Ask AI to reconstruct:

- thesis
- claim chain
- evidence bridge
- equation role
- domain boundaries
- kill conditions
- weakest point
- repair action

### 14. Vectorization Prep

Input: cleaned lossless JSON.

Output: vector-ready JSONL.

Why easy after cleanup.

Vectorize these separately:

- spine
- claim_arch.surface_claim
- evidence_chain.connection_to_claim
- kill_arch.testable_kill
- eq_sem.role
- domain_boundary
- mechanism_graph

Do not vectorize raw full article as the primary contradiction substrate.

## What Should Become Bat-Clickable

Minimum click surface:

```text
RUN_GTQ03_LOSSLESS_PILOT.bat
```

Next click surfaces:

```text
RUN_BATCH_LOSSLESS_C4C.bat
RUN_RECONSTRUCTION_TEST.bat
RUN_VECTOR_PREP.bat
RUN_CONTRADICTION_PREFLIGHT.bat
```

## Can An AI Partner Get Close To The Lossless Prompt?

Yes, but not from raw HTML and not without a scaffold.

The current deterministic pipeline already gets close enough to prove the concept:

- it creates the artifact shell
- it preserves stable IDs
- it extracts claims/equations/domain boundaries
- it outputs JSON/HTML

But the expensive/intelligent parts still require an LLM fill pass:

- buried claim
- operational claim
- evidence bridge
- implicit kill
- hostile reviewer attack
- repair recommendation

Conclusion: the lossless prompt is not too hard for them if the workflow is staged. It is too hard if they are asked to do everything in one giant pass over raw HTML.

## Recommended Next Build

Build the workflow as four stages:

```text
01_convert_html_to_markdown
02_deterministic_lossless_extract
03_llm_fill_required_fields
04_vector_ready_export
```

Then wire contradiction engine after stage 04.

## /PROBE

The billion-dollar part is not "summarize article as JSON." Lots of systems can do that.

The valuable part is:

```text
stable semantic address
+ claim archaeology
+ evidence bridge
+ kill condition
+ equation semantics
+ domain boundary
+ vector-ready sectioning
+ reconstruction test
```

That combination turns a document into a contradiction-readable object.
