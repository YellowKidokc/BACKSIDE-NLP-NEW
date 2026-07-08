# Reading Modes + Inline Trace Design

Date: 2026-05-25

## Core Decision

The public HTML system needs multiple reader modes and exact traceability.

The proof packet cannot only say:

```text
This article has claim X.
This article has fruit profile Y.
This article has Master Equation profile Z.
```

It must also answer:

```text
Where in the paper?
Which paragraph?
Which sentence?
Which quoted span?
Why did the grader interpret that span this way?
```

## Reader Modes

Use three primary modes, with optional fourth internal/debug mode:

1. **Easy Read**
   - Public reader path.
   - Minimal jargon.
   - Claims shown as plain-language insights.
   - Evidence links visible but not intrusive.

2. **David / Theophysics Read**
   - Middle layer.
   - Keeps framework language, Master Equation terms, 7Q, laws, fruits, coherence, entropy, etc.
   - This is the author/workshop layer.

3. **Academic / Audit Read**
   - Critic-facing and institution-facing.
   - Shows claim type, evidence status, source span, falsification condition, objection state, formal target.
   - This is the layer that sells to academia because it exposes provenance and auditability.

4. **Debug / Station Read** (optional, not default public)
   - Shows station outputs, model/rubric versions, trace IDs, char offsets, missing-span repair flags.

## HTML Interaction Pattern

Each claim-bearing sentence should be able to open an inline audit drawer directly under the sentence.

Pattern:

```html
<span
  class="claim-span"
  data-claim-id="claim-001"
  data-section-id="SEC-0004"
  data-paragraph-index="12"
  data-sentence-index="3"
  data-char-start="1842"
  data-char-end="1975"
>
  Sentence text here.
</span>

<aside class="claim-audit-drawer" id="claim-001-drawer">
  <h4>Claim Audit</h4>
  <p><strong>Claim:</strong> ...</p>
  <p><strong>Why flagged:</strong> ...</p>
  <p><strong>Evidence status:</strong> ...</p>
  <p><strong>Falsification:</strong> ...</p>
  <p><strong>Objections:</strong> ...</p>
  <p><strong>Formal target:</strong> ...</p>
</aside>
```

The drawer opens in place. It does not send the reader to a separate report unless they choose "Open full proof packet."

## Markdown Pattern

Markdown cannot provide the same interactive drawer by itself, but it can preserve the same trace contract.

Use block anchors and footnote-style audit blocks:

```markdown
<a id="claim-001"></a>
The claim-bearing sentence appears here. [Claim audit](#claim-001-audit)

<a id="claim-001-audit"></a>
> **Claim Audit claim-001**
> - Section: SEC-0004
> - Paragraph: 12
> - Sentence: 3
> - Span: 1842-1975
> - Evidence status: partial
> - Falsification: ...
> - Objection status: unresolved
```

The same IDs must be shared across HTML, Markdown, JSON, CSV, and XLSX.

## Required Data Contract

Every scored signal needs this shape:

```json
{
  "trace_id": "trace-000001",
  "claim_id": "claim-001",
  "signal_type": "fruit|master_equation|claim|risk|7q|evidence|formal",
  "signal_name": "Peace|C|Q4 evidence|overclaim risk",
  "source_path": "",
  "section_id": "SEC-0004",
  "section_title": "",
  "paragraph_index": 12,
  "sentence_index": 3,
  "char_start": 1842,
  "char_end": 1975,
  "quoted_span": "",
  "why_it_counts": "",
  "confidence": 0.0,
  "trace_status": "traced|missing-span|needs-review"
}
```

## Build Order

1. Add span extraction for Markdown and HTML.
2. Generate stable section/paragraph/sentence IDs.
3. Attach claims, fruits, Master Equation variables, 7Q markers, and risk flags to spans.
4. Emit trace ledger:
   - JSON
   - CSV
   - XLSX sheet
   - Markdown audit blocks
   - HTML inline drawers
5. Make charts click into the trace ledger.
6. Only then treat charts as critic-facing proof surfaces.

## Structural Rule

No chart without a trace.

If the chart says a paper has high `C` coherence, `Peace`, `Faithfulness`, overclaim risk, or Q4 evidence strength, the reader must be able to click the chart signal and see the exact sentence(s) that caused it.
