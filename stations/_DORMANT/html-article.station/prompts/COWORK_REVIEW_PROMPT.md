# Cowork Review Pass — HTML Article Workflow

You are doing a single review pass over the html-article.workflow that was just built tonight by a swarm of workers. Your job is NOT to rebuild anything. Your job is to look at what they produced and tell David what's solid, what's off, and what got missed.

## Where Everything Lives
Done. D:\html-article-workflow.lnk points to the whole workflow folder on X:. Cowork should be able to follow that and read everything inside.

Workflow root: `\\dlowenas\brain\Backside\workflows\html-article.workflow`
(Also mapped as `X:\Backside\workflows\html-article.workflow`)

## What to Read

Read these in this order:

1. `configs/lane_registry.json` — the lane definitions and pipeline order
2. `configs/ARTICLE_OUTPUT_REGISTRY.md` — what every lane should produce
3. `configs/MASTER_INDEX_WORKBOOK_CONTRACT.md` — the persistent workbook rules
4. `configs/SEMANTIC_ADDRESS_AND_ROUTING.md` — addressing and routing contract
5. `configs/CALIBRATION_EXPECTED.md` — the known-answer test
6. `prompts/WORKER_DISPATCH.md` — what every worker was told to do
7. `prompts/SWARM_WORK_ORDER_ROUND1.md` — how workers were assigned

Then read each testable lane's deliverables:
- `02_SECTION_MAP/` — contract.json, README.md, run.py, sample_output/
- `03_YAML_METADATA/` — contract.json, README.md, run.py, sample_output/
- `04_TAGS/` — contract.json, README.md, run_prompt.md, sample_output/
- `05_CLAIMS/` — contract.json, README.md, run_prompt.md, sample_output/
- `07_MATH_TRANSLATION/` — contract.json, README.md, run.py, sample_output/
- `10_RIGOR/` — contract.json, README.md, run.py, sample_output/
- `13_LAYER_LEDGER/` — contract.json, README.md, run_prompt.md, sample_output/
- `14_LOOPBACK_REVIEW/` — whatever Worker-3 left there

Also check:
- `configs/shared_lib/` — ids.py, address.py, schemas.py (the UUID and addressing system)
- `configs/NABLA_DESIGN_BIBLE.md` — the 30 design rules for semantic addressing
- `00_DROP/` — calibration test article + GTQ-03

## What to Look For

### 1. Contract Consistency
Do the contract.json files across lanes agree on field names? If lane 02 outputs `section_id` and lane 05 expects `sectionId`, that's a break. Check the joins.

### 2. Calibration Alignment
Did the sample outputs actually match CALIBRATION_EXPECTED.md? Workers said they did — verify at least 2-3 of them.

### 3. Schema Convergence
Are all lanes using schemas from `configs/shared_lib/schemas.py`, or did anyone invent their own data shapes? The rule was: converge, don't fork.

### 4. Pipeline Order vs Dependencies
Does the `pipeline_order` in lane_registry.json actually work? If lane 04 depends on lane 02 output, but the pipeline order puts something between them that breaks the chain, flag it.

### 5. Missing Lanes
These lanes are still empty or stub-only: 00_DROP, 01_LOSSLESS, 06_CONTRADICTIONS, 08_SECTION_VECTORS, 09_GRAPH_LINKS, 11_HTML_RENDER, 12_EXPORTS, 15_SECTION_PACKETS, 16_FINAL_PAGE_ASSEMBLY, 17_PUBLISH_READY. That's expected — not everything shipped in round 1. But check: is anything BLOCKING because of a missing lane that a testable lane claims to depend on?

### 6. Challenger Notes
Workers were told to produce `challenger_notes.json` with three overlooked strengths and three attack surfaces. Check if any of them actually did it (the requirement was added mid-round so some may have missed it).

### 7. Drift Between Docs
Worker-1 flagged that lane_registry.json and SWARM_WORK_ORDER_ROUND1.md disagreed on what lane 02 does. That was fixed. Are there other disagreements between the config docs?

### 8. The Addressing System
Is the Nabla semantic address (D/N/V/A/U/R :: VECTOR :: HASH) actually flowing through the lanes, or is it declared in the configs but not implemented in the outputs?

## What to Do

- **Small fixes**: just fix them. Typos, missing fields, obvious contract mismatches — fix in place and note what you changed.
- **Medium issues**: write them up clearly with the lane, the problem, and what the fix should be. Don't fix them yourself — flag for David and Opus.
- **Big structural problems**: if you find something that means the pipeline fundamentally won't work as designed, say so plainly. Don't sugarcoat it. David will handle the reroute.

## Output

Write your findings to:
`\\dlowenas\brain\Backside\workflows\html-article.workflow\configs\COWORK_REVIEW_PASS.md`

Structure it as:
1. Overall assessment (2-3 sentences)
2. What's solid
3. Small fixes made (list what you changed)
4. Medium issues (list with lane + problem + recommended fix)
5. Big issues (if any)
6. Recommended next actions

Do not overbuild. Do not redesign. One pass, honest eyes, write it up.
