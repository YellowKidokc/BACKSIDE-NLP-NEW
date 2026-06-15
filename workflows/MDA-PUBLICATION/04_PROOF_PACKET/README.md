# 04_PROOF_PACKET

Purpose: build the proof/citation/axiom/isomorphism packets that feed both article Proof tabs and the MDA series home.

This station consumes existing outputs. It should not re-grade papers unless an input is missing or stale.

## Inputs

- `\\dlowenas\HPWorkstation\Desktop\Moral_Decay_of_America\90_Data\citation_map.csv`
- `\\dlowenas\HPWorkstation\Desktop\Moral_Decay_of_America\90_Data\claims_needed.csv`
- Paper Intelligence rows and snapshots from `X:\apps\paper-intelligence-suite-python\OUTPUT\`
- o3/CDCM `scores_*.json` and `integration_*.md` packets when present
- vector evidence appendices when present
- `MDA_Methodology_and_Isomorphism_Appendix.md`
- Isomorphism Explorer records
- black axiom snapshot page/artifact

## Outputs

- `article-packets\{article}.proof-packet.json`
- `article-packets\{article}.proof-fragment.html`
- `citation-resolution\{article}.citation-status.csv`
- `axiom-map\{article}.axiom-map.json`
- `isomorphism-map\{article}.isomorphism-map.json`
- `series-packets\mda-series-grade.json`
- `series-packets\mda-proof-packet.html`

## Gate

Every promoted claim must have:

- claim level
- claim status
- source status
- citation quality
- methodology dependency
- proof destination
- kill condition or explicit not-yet-falsifiable flag

Do not label citation-map pointers as primary citations.
