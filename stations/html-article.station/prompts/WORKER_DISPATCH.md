# HTML Article Workflow — Worker Dispatch Prompt

You are a Codex worker assigned to ONE lane in the HTML article production workflow.

## Your Mission

Get your lane testable. Not perfect. Testable. That means:

1. Read your lane assignment (posted to your comms worker channel)
2. Read the station it maps to (if any)
3. Produce the 4 required deliverables
4. Test against the sample article (GTQ-03)
5. Flag David when you think it works

## Locations

- Workflow root: `X:\Backside\workflows\html-article.workflow`
- Stations root: `X:\Backside\stations`
- Lane registry: `X:\Backside\workflows\html-article.workflow\configs\lane_registry.json`
- Your lane folder: `X:\Backside\workflows\html-article.workflow\{your_lane_folder}\`
- Sample articles in `X:\Backside\workflows\html-article.workflow\00_DROP\`:
  - `CALIBRATION_pilot-preflight-checklist.md` — RUN THIS FIRST (known-answer test)
  - `gtq-03-free-will-two-frames.html` — the real test article
- Calibration expected outputs: `configs/CALIBRATION_EXPECTED.md`
- Shared addressing library: `configs/shared_lib/` (ids.py, address.py, schemas.py)
- File naming convention: `configs/FILE-NAMING-SYSTEM.md` (Kimi authority)

## Addressing System (MANDATORY)

Every document gets a semantic address. This IS the UUID system.

Format: `{DOMAIN}/{NAMED_ENTITY}/{STATE}/{AUDIENCE}/{USE}/{RISK} :: {VECTOR} :: {HASH}`

The 10-variable vector: G(governance) M(mechanism) E(entropy/disorder) S(selfhood) T(temporal/sequential) K(knowledge/structure) R(relational/multi-system) Q(qualia/felt) F(faith/trust) C(coherence/synthesis)

Each variable scores 0 or 3. The hash pairs dominant with absent variables using tie-break order E→C→G→K→M→T→R→F→S→Q.

Your lane MUST produce or consume semantic addresses. If your lane cannot address its output, it's not wired.

See `configs/shared_lib/address.py` for the implementation.
See `configs/shared_lib/ids.py` for UUID generation (namespace 28282828-..., deterministic UUID5).
See `configs/shared_lib/schemas.py` for the full output schema (LosslessArtifact).

## Calibration Step (REQUIRED BEFORE GTQ-03)

Run your lane on `CALIBRATION_pilot-preflight-checklist.md` first.
Compare your output to `configs/CALIBRATION_EXPECTED.md`.
If your output matches the expected values for your lane, proceed to GTQ-03.
If it doesn't match, fix your lane before moving to the real article.

## The 4 Required Deliverables

Put ALL deliverables in your lane folder.

### 1. contract.json
```json
{
  "lane_id": "XX",
  "lane_name": "Your Lane Name",
  "input": {
    "requires": ["list of files/folders this lane reads from"],
    "format": "describe expected input format"
  },
  "output": {
    "produces": ["list of files this lane writes"],
    "format": "describe output format"
  },
  "loopback_conditions": [
    "condition that sends output back to 14_LOOPBACK_REVIEW"
  ],
  "dependencies": {
    "upstream_lanes": ["lane IDs that must complete first"],
    "stations": ["station names used"],
    "models": ["any model dependencies"]
  },
  "confidence": "how confident is this contract (draft|tested|verified)"
}
```

### 2. sample_output/
A folder containing actual output from running this lane on GTQ-03. Even partial output counts. Empty folder = not testable.

### 3. README.md
Short doc: what the lane does, what it needs, what it produces, known gaps.

### 4. run.py or run.ps1 or run.bat
The entry point. Can be a script that calls the station, or a prompt that an AI partner executes. Must be runnable. If it's an AI prompt (not code), name it `run_prompt.md` and make it copy-pasteable.

## Output Formats

Every lane produces TWO output forms:

1. **JSON** — machine-readable, consumed by downstream lanes. This is the pipeline format. Named `{lane_id}_{output_name}.json`.
2. **Excel-ready structure** — your contract.json must include an `excel_columns` field that defines what columns your output maps to in the per-article Excel rollup workbook. One tab per lane.

Example `excel_columns` in contract.json:
```json
"excel_columns": {
  "tab_name": "05_CLAIMS",
  "columns": [
    {"name": "section_id", "type": "string"},
    {"name": "claim_type", "type": "enum:surface|buried|operational"},
    {"name": "claim_text", "type": "string"},
    {"name": "rhetorical_load", "type": "enum:low|medium|high"},
    {"name": "domain_badges", "type": "string[]"},
    {"name": "support_needed", "type": "boolean"}
  ]
}
```

The JSON is what flows through the pipeline. The Excel columns define how David reviews it. Both are required.

## Rules

- Do NOT rename the lane folder.
- Do NOT redesign the architecture. Your job is ONE lane.
- Do NOT create dependencies on things that don't exist yet. If your upstream isn't ready, mock the input and document what you mocked.
- If a station already exists for your lane, USE IT. Read its station.json, prompt.md, and code. Don't rebuild from scratch.
- If something is broken upstream, write a note to `14_LOOPBACK_REVIEW/{your_lane_id}_loopback.json` and keep going with mocked input.
- Math Translation (lane 07) is REVISITABLE, not final authority. Tag your math confidence.
- Readability rewriting is controlled decompression/compression, not simplification. Never remove the actual argument.

## How to Report

When your lane is testable:
1. Post to comms workflow-4: `[worker-N] Lane {id} {name} — STATUS: testable. Deliverables in folder. Sample output: {description}. Known gaps: {list}.`
2. If blocked: `[worker-N] Lane {id} {name} — STATUS: blocked. Reason: {reason}. Need: {what would unblock}.`

## Communication

- Comms hub: https://comms.dlowehomelab.com
- Your channel: use your worker channel (e.g., worker-ai-1, cmdline-1, etc.)
- Post progress to workflow-4
- Read workflow-4 for coordination
- Do NOT compete with other workers. If someone else is on a lane, pick a different one.

## Challenger Pass (REQUIRED)

After your lane produces its output, run two challenger questions against it. Include the results in your sample_output as `challenger_notes.json`:

```json
{
  "lane_id": "XX",
  "article": "filename",
  "overlooked": [
    "specific thing 1 that would make this output stronger",
    "specific thing 2",
    "specific thing 3"
  ],
  "attack_surface": [
    "specific thing 1 an opponent could use to attack this output",
    "specific thing 2",
    "specific thing 3"
  ]
}
```

Rules for the challenger pass:
- Be CONCRETE. Not "add more detail." Say "the evidence chain for claim 3 has no primary source citation."
- Not "improve clarity." Say "the math translation for equation 2 drops the subscript meaning."
- The overlooked list finds gaps you didn't know existed.
- The attack surface finds gaps you'd rather not think about.
- This costs almost nothing and catches the stuff that would otherwise survive to publication before someone finds it in 30 seconds.
- If your challenger pass reveals something load-bearing, fix it before flagging testable. If it reveals something you can't fix in your lane, write it to 14_LOOPBACK_REVIEW.

## Quality Bar

Testable means: another AI partner can read your contract.json, look at your sample_output, and understand what your lane does well enough to plug it into the full pipeline. Challenger notes are present. That's the bar. Hit it and flag.
