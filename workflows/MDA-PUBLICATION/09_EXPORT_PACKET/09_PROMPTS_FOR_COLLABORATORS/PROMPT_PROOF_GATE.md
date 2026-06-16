# Prompt For Proof-Gate Work

You are working on the MDA Proof tabs.

Do not promote a claim because it sounds strong.

For each article:

1. Identify the central claim.
2. Identify the evidence attached to it.
3. Identify assumptions.
4. Identify kill conditions.
5. Identify whether the math/isomorphism layer is definitionally complete, partially mapped, or only analogical.
6. Promote only claims that survive the 7Q gate.

Use:

- `07_TWO_LANE_OPENAI_REPORTS`
- `06_PIPELINE_ANALYTICS/paper_rows.json`
- raw snapshot JSON files under `06_PIPELINE_ANALYTICS/snapshots`

Output for each promoted claim:

```markdown
## Promoted Claim

Article:
Claim:
Status: SURVIVES / PARTIAL / HOLD
7Q result:
Evidence:
Assumptions:
Kill condition:
Math/isomorphism status:
Public wording:
```

If the claim does not survive, say HOLD. Do not decorate it.
