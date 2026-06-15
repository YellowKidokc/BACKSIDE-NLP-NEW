# Prompt For Portable Repo Rewrite

You are helping package the MDA publication workflow into a portable repo.

Goal: rewrite the scripts so the workflow can move to GitHub, a new drive, or a new machine without breaking path assumptions.

Do not start by changing article content. Start by mapping the system.

## Required Output

Produce:

1. A repo map.
2. A config contract.
3. A path-agnostic rewrite plan.
4. A migration checklist.
5. A test checklist.

## Core Rule

No script should hardcode:

- `X:\WORKFLOWS\MDA-PUBLICATION`
- `C:\Users\lowes\Documents\Codex\...`
- `\\dlowenas\...`

Those must become config values.

## Proposed Layers

Use this architecture:

```mermaid
flowchart TB
  subgraph L4["4. User-Facing Outputs"]
    Deploy["Deploy HTML"]
    Reader["Four-tab Reader HTML"]
    Snapshot["Axiom Black Snapshots"]
    GraphView["Keyword/Graph Views"]
    Packet["Export Packet"]
  end

  subgraph L3["3. Workflows / Stations"]
    Lossless["Lossless Source Station"]
    Reading["Reading-Level Station"]
    Pipeline["Paper Intelligence Station"]
    OpenAI["Two-Lane OpenAI Station"]
    Proof["Proof-Gate Station"]
    Build["HTML Build Station"]
    Export["Export Packet Station"]
  end

  subgraph L2["2. Scripts / Runners / Health"]
    GenReading["generate_reading_levels.py"]
    RunReading["run_all_reading_levels.ps1"]
    Combine["combine_mda_reader_html.py"]
    SnapshotBuild["build_mda_black_snapshot_html.py"]
    KeywordOverlay["build_mda_keyword_graph_overlay.py"]
    TwoLane["openai_mda_two_lane.py"]
    PipelineRun["run_pipeline.py / paper intelligence runners"]
    Health["health_check.ps1 / validate_paths.py"]
  end

  subgraph L1["1. Data Folders / Artifacts"]
    Articles["01_LOSSLESS/articles"]
    ReadingOut["05_READING_LEVELS"]
    HtmlOut["06_HTML_BUILD/reader_combined"]
    Analytics["paper_intelligence outputs"]
    Reports["two_lane reports"]
    Snapshots["snapshot JSON + HTML"]
    Graphs["knowledge_graph + keyword overlay"]
  end

  subgraph L0["0. Models / Preferences / Config"]
    Config["mda.config.json"]
    Models["models: primary, cheap, reasoning, fallback"]
    Prompts["prompt templates"]
    Paths["path aliases: repo_root, source, outputs, external_outputs"]
    Preferences["claim policy, proof policy, style policy"]
  end

  Config --> Models
  Config --> Paths
  Config --> Preferences
  Prompts --> GenReading
  Models --> GenReading
  Models --> TwoLane
  Paths --> Articles
  Paths --> ReadingOut
  Paths --> HtmlOut
  Paths --> Analytics
  Paths --> Reports

  Articles --> Lossless
  Lossless --> Reading
  Lossless --> Pipeline
  Reading --> ReadingOut
  Pipeline --> Analytics
  OpenAI --> Reports
  Analytics --> Snapshots
  Analytics --> Graphs
  Reports --> Proof
  ReadingOut --> Build
  Articles --> Build
  Proof --> Build
  Build --> HtmlOut

  GenReading --> Reading
  RunReading --> Reading
  PipelineRun --> Pipeline
  TwoLane --> OpenAI
  Combine --> Build
  SnapshotBuild --> Snapshot
  KeywordOverlay --> GraphView
  Health --> Export

  HtmlOut --> Reader
  Snapshots --> Snapshot
  Graphs --> GraphView
  Reader --> Packet
  Snapshot --> Packet
  GraphView --> Packet
  Reports --> Packet
  Analytics --> Packet
  Packet --> Deploy
```

## Proposed Config Contract

Create `mda.config.example.json`:

```json
{
  "paths": {
    "repo_root": ".",
    "lossless_articles": "01_LOSSLESS/articles",
    "reading_levels": "05_READING_LEVELS",
    "html_build": "06_HTML_BUILD/reader_combined",
    "export_packet": "09_EXPORT_PACKET",
    "pipeline_analytics": "outputs/paper_intelligence",
    "two_lane_reports": "outputs/two_lane_openai",
    "snapshot_html": "outputs/axiom_black_snapshots",
    "keyword_overlay": "outputs/keyword_graph_overlay"
  },
  "models": {
    "reading_primary": "gpt-4o",
    "reading_budget": "gpt-4o-mini",
    "math_review": "gpt-4o-mini",
    "reasoning_deep": "o3",
    "fallback": "gpt-4o-mini"
  },
  "policies": {
    "proof_gate_required": true,
    "no_proof_overclaim": true,
    "easy_academic_fallback_allowed": true,
    "source_spine_read_only": true
  }
}
```

## Rewrite Targets

Rewrite these first:

- `READING_LEVEL_GENERATOR/generate_reading_levels.py`
- `READING_LEVEL_GENERATOR/run_all_reading_levels.ps1`
- `05_HTML_BUILD/combine_mda_reader_html.py`
- `work/build_mda_black_snapshot_html.py`
- `work/build_mda_keyword_graph_overlay.py`
- `X:\apps\paper-intelligence-suite-python\12_HEARTBEAT\openai_mda_two_lane.py`

## Acceptance Tests

A rewrite is not accepted unless:

- It runs from a copied repo at a different path.
- It can run with `mda.config.json`.
- It can run with no `X:\` paths.
- It can build one article.
- It can build all 61 article shells.
- It reports missing Easy/Academic files instead of silently pretending they exist.
- It reports proof tabs as structural unless claims are actually promoted.

## Final Report Format

```markdown
PORTABLE_REPO_REWRITE_STATUS

Repo root tested:
Config file:
Scripts rewritten:
Hardcoded paths removed:
One-article build:
Full build:
Remaining blockers:
Proof overclaim safeguards:
Next command:
```
