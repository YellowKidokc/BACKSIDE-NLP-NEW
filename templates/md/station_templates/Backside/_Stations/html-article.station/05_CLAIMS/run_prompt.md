# 05_CLAIMS — Run Prompt (Two-Pass: Station + LLM Refinement)

Use this prompt to run lane 05 on any article in `00_DROP/`. Round-1 implementation is station + LLM; round-2 will move pass 2 to a deterministic claim-arch model.

---

## Setup

You are running lane **05_CLAIMS**. Your output feeds `06_CONTRADICTIONS`, `09_GRAPH_LINKS`, `10_RIGOR`, `15_SECTION_PACKETS`. Stay in lane.

Read first:
1. `\\dlowenas\brain\Backside\workflows\html-article.workflow\configs\ARTICLE_OUTPUT_REGISTRY.md` (section 6)
2. `\\dlowenas\brain\Backside\workflows\html-article.workflow\05_CLAIMS\contract.json`
3. `\\dlowenas\brain\Backside\workflows\html-article.workflow\05_CLAIMS\README.md`
4. `\\dlowenas\brain\Backside\workflows\html-article.workflow\configs\shared_lib\schemas.py` (focus on `ClaimArch`)
5. Master Equation, 10 variables, 10 Laws from canon channel — needed for domain_badges and rhetorical_load calibration on Theophysics articles.

## Pass 1 — Station first pass

Run the existing station classifier:

```powershell
python "\\dlowenas\brain\Backside\stations\claim-extractor.station\extract.py" `
  "\\dlowenas\brain\Backside\workflows\html-article.workflow\00_DROP" `
  --format both
```

The station writes to its hard-coded `D:\brain\08_CLAIMS\_OUTPUT\claims_<run_id>.json`. Copy that file into `05_CLAIMS/station-firstpass.json` (round-1 manual step; round-2 wraps with `run.py`).

Each station claim has: `claim_id, source_file, section, text, classification, confidence, length, has_equation, has_scripture_ref`.

## Pass 2 — LLM refinement into ClaimArch

For each station claim block, produce a `ClaimArch`:

```json
{
  "claim_id": "stable_uuid('claim', page_id, section_id, surface_claim_hash)",
  "block_id": "<section_id from 02_SECTION_MAP>",
  "surface_claim": "<what the section explicitly states>",
  "buried_claim": "<the presupposition the surface claim depends on>",
  "operational_claim": "<what the surface claim commits the reader/system to do or measure>",
  "rhetorical_load": "low|medium|high",
  "domain_shift": false,
  "domain_badges": ["<from DomainBadge plus AVIATION|SAFETY|PROCEDURE>"],
  "support_needed": false,
  "station_classification": "<carried from pass 1>",
  "confidence": 0.0
}
```

### Three-layer rules

- **surface_claim** is verbatim or near-verbatim from the section. Do not paraphrase past recognition.
- **buried_claim** asks: what must be true for the surface claim to be coherent? It is usually one sentence and often more general than the surface claim.
- **operational_claim** asks: if a reader, a system, or a test wanted to act on this claim, what would they do or measure? If there is no operational consequence, write `"EXPAND_REQUIRED"` (the schema default) — do not invent one.

If buried or operational comes out identical to surface, your refinement failed. Re-read the section and try again.

### rhetorical_load scale

- **low** — measured, neutral, procedural, defensive ("may", "could", "is generally").
- **medium** — assertive, structured, claims authority through formal language ("must", "follows that", "we prove").
- **high** — totalizing, evangelical, framework-overclaim ("everything is", "this proves", "the only way", emotional appeals).

For Theophysics-domain articles, calibrate rhetorical_load against the framework's own `load-bearing | suggestive | overclaimed` gradient. Overclaimed → high.

### domain_shift

True if the section moves from one DomainBadge to another *within itself* and does not bridge cleanly (e.g., PHYSICS → THEOLOGY without an explicit isomorphism). False if the section stays in one domain or if it bridges with a named structural mapping.

### support_needed

True if the surface claim makes an empirical, formal, or scriptural claim that requires citation or evidence and the section does not provide it. This feeds the `needs-evidence` workflow tag in lane 04.

## Outputs to write

| File | Content |
|---|---|
| `05_CLAIMS/claim-packets.json` | Page + section ClaimArch lists, plus provenance and run_id. |
| `05_CLAIMS/claim-ledger.csv` | One row per (claim × layer). 3 layers × N claims = 3N rows max. |
| `05_CLAIMS/claims.md` | Human-readable rollup: top claims per section, rhetorical load distribution, support-needed list. |
| `05_CLAIMS/station-firstpass.json` | Verbatim station output for traceability. |

## Calibration check (run BEFORE GTQ-03)

Input: `00_DROP/CALIBRATION_pilot-preflight-checklist.md`

Expected ClaimArch for the page intro:

```json
{
  "surface_claim": "This checklist ensures aircraft, crew, instruments, fuel, communication systems, and safety controls are ready before flight.",
  "buried_claim": "Flight safety depends on completing standardized checks before takeoff.",
  "operational_claim": "Each checklist item must have a pass/fail state.",
  "rhetorical_load": "low",
  "domain_shift": false,
  "domain_badges": ["AVIATION","SAFETY","PROCEDURE"]
}
```

The kill condition section emits its own ClaimArch with operational_claim about determining pass/fail for every required safety item.

If sample output does not match the calibration target: stop and fix pass 2 before running GTQ-03.

## Loopback

If you see any of:
- a claim referencing a span that does not exist in `01_LOSSLESS`,
- 0 station claims on a section with > 200 chars,
- buried == surface across all sections,
- math-bearing claim without `07_MATH_TRANSLATION` entry,

write `14_LOOPBACK_REVIEW/05_claims_loopback.json` with the specific failure and stop emitting downstream rows for that section.

## Reporting

Post to comms `workflow-4`:
```
[claude-code-worker-2] Lane 05 Claims — STATUS: testable. Sample output in 05_CLAIMS/sample_output/calibration/. Station first pass: <N> claims. LLM refinement: <M> ClaimArchs. Loopback: 0|<count>. Known gaps: <list>.
```
