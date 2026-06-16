---
# EVIDENCE TEMPLATE
# =================
# Evidence items support claims. They are data points, not arguments.
# Must be: specific, sourced, typed, and rated for strength.

uuid: {{UUID}}
type: evidence
id: EV-{{NUMBER}}
status: draft | verified | contested | retracted

# Evidence classification
evidence_type: empirical | theoretical | testimonial | historical | mathematical

# Source information
source:
  author: {{AUTHOR}}
  title: {{TITLE}}
  year: {{YEAR}}
  publication: {{JOURNAL/BOOK/SOURCE}}
  doi: {{DOI_IF_AVAILABLE}}
  url: {{URL_IF_AVAILABLE}}

# Quality assessment
peer_reviewed: true | false
replication_status: replicated | unreplicated | failed_replication | NA
strength: ⬛⬜⬜⬜⬜ | ⬛⬛⬜⬜⬜ | ⬛⬛⬛⬜⬜ | ⬛⬛⬛⬛⬜ | ⬛⬛⬛⬛⬛

# What this evidence supports
supports_claims: []  # UUIDs of claims

created: {{DATE}}
last_reviewed: {{DATE}}
---

# EV-{{NUMBER}}: {{EVIDENCE_TITLE}}

## Summary

> {{ONE_SENTENCE_SUMMARY_OF_EVIDENCE}}

---

## Source Details

| Field | Value |
|-------|-------|
| Author(s) | {{AUTHOR}} |
| Title | {{TITLE}} |
| Year | {{YEAR}} |
| Publication | {{PUBLICATION}} |
| DOI | {{DOI}} |
| URL | {{URL}} |

---

## Evidence Type

- [ ] **Empirical** — Experimental or observational data
- [ ] **Theoretical** — Mathematical derivation or proof
- [ ] **Testimonial** — Expert opinion or historical testimony
- [ ] **Historical** — Historical records or events
- [ ] **Mathematical** — Formal proof or calculation

---

## Key Finding

What specifically does this evidence show?

> {{SPECIFIC_FINDING}}

### Data/Quote

```
{{RELEVANT_DATA_OR_QUOTE}}
```

---

## Strength Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Source credibility | low / medium / high | |
| Methodology quality | poor / adequate / rigorous | |
| Sample size (if applicable) | small / medium / large / NA | |
| Replication | yes / no / partial / NA | |
| Peer review | yes / no | |

**Overall strength:** {{⬛⬛⬛⬜⬜}}

---

## What This Evidence Supports

| Claim ID | Claim Statement | Support Type |
|----------|-----------------|--------------|
| CL-{{X}} | | direct / indirect / circumstantial |

---

## What This Evidence Does NOT Support

> ⚠️ **Explicit limitations:**

- This evidence does NOT prove...
- This evidence does NOT address...
- Extrapolating to {{X}} would be...

---

## Alternative Interpretations

Could this evidence support a different conclusion?

| Alternative Interpretation | Plausibility |
|---------------------------|--------------|
| | low / medium / high |

---

## Potential Weaknesses

1. 
2. 

---

## Related Evidence

| Evidence ID | Relationship |
|-------------|--------------|
| EV-{{Y}} | corroborates / contradicts / independent |

---

## Verification Notes

How was this evidence verified?

- [ ] Source checked
- [ ] Quote/data verified
- [ ] Replication status confirmed
- [ ] Peer review status confirmed

---

%%semantic
{
  "uuid": "{{UUID}}",
  "type": "evidence",
  "id": "EV-{{NUMBER}}",
  "evidence_type": "{{EVIDENCE_TYPE}}",
  "strength": "{{STRENGTH}}",
  "classifications": [
    {"content": "{{EVIDENCE_TITLE}}", "type": "evidence"}
  ]
}
%%
