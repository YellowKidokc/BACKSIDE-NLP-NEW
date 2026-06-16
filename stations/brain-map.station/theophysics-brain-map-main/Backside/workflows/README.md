# Backside Workflows

**What this is:** The future home for end-to-end X-drive processes.
**Owner:** shared
**Status:** live map
**Last updated:** 2026-05-16

Workflows belong in Backside because they are machinery. David should see their clean front doors through `X:\00_WORKFLOWS`, `X:\DROP_HERE`, `X:\EXPORTS`, packets, or the dashboard, not a sprawl of runtime folders at X:\ root.

A workflow is an ordered recipe that calls verified stations. It should not reimplement station logic inline.

## Composition rule

Workflows consume stations by contract:

```text
dependencies.json      declares stations the workflow may call
configs/default.json   declares the ordered station recipe
```

The detailed rule lives at:

```text
Backside\STATION_WORKFLOW_COMPOSITION.md
```

If the same capability is needed in 10 or 20 workflows, that is evidence for one shared station, not 10 or 20 copied implementations.

## Naming

Every workflow folder ends in `.workflow`:

```text
grade-paper.workflow
route-and-convert.workflow
handoff-session.workflow
pull-link.workflow
```

## Folder shape

```text
<name>.workflow\
  README.md
  _AGENT_BRIEF.md
  RUN.bat
  RUN_AGENT.bat
  health_check.bat
  pipeline.py
  dependencies.json
  workflow.dependencies.schema.json (repo-level schema)
  configs\
    default.json
  STATE\
  prompts\
  00_DROP\
  OUTPUT\
  ARCHIVE\
```

## Root exposure rule

A workflow can have a root click-button or dashboard tile, but the actual runtime folder lives here.

| Root/front door | Backside machinery |
|---|---|
| `X:\RUN_PAPER_GRADER.bat` | `X:\Backside\workflows\grade-paper.workflow\RUN.bat` |
| Dashboard "Paper Grader" tile | `X:\Backside\workflows\grade-paper.workflow\` |
| `X:\DROP_HERE` routed paper | `X:\Backside\workflows\grade-paper.workflow\00_DROP\` |

## Planned workflows

| Workflow | Current source |
|---|---|
| `grade-paper.workflow` | `X:\paper-proof-grader` |
| `refresh-axiom-snapshot.workflow` | `X:\axioms` |
| `route-and-convert.workflow` | `X:\Backside\workflows\knowledge-refinery.workflow` + `X:\Conversions\conversion-layer` |
| `build-ai-portal.workflow` | `X:\ai-portal-generator` |
| `handoff-session.workflow` | `X:\session-handoff-drop` |
| `pull-link.workflow` | `X:\link-pull-drop` |
| `brain-dashboard.workflow` | dashboard launcher/control surface |
| `lossless-context.workflow` | Markdown -> semantic address + JSON/HTML audit snapshot before vectorization |
| `first-article.workflow` | Markdown/HTML/image -> conversion -> summary/overview/math/image notes -> lossless context packet |
| `chi-tagging.workflow` | Cannon canon sources -> chi-variable reference index -> database tagging guardrail |
| `semantic-snapshot.workflow` | Source/lossless/tags/grader/axiom map -> Master Equation UUID route -> station shortcuts |

Do not move live folders here until the path sweep and junction plan are ready.

## Packet movement

Workflows should move a packet through stations:

```text
source
-> executive-summary
-> translation
-> seven-questions
-> axiom-candidates
-> review/promotion
-> public-export
```

Each station writes its outputs into the packet instead of scattering remnants across the drive.
