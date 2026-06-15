# Backside

System-side storage for root cleanup, archived leftovers, app fragments, logs, scratch material, model cards, stations, workflows, services, control-plane repos, and prompt packs.

This folder exists to keep `X:\` readable without deleting potentially useful files.

## Folders

- `_models` - model/NLP registry. Stores model cards and routing contracts; large weights stay off git and live on X:\.
- `_state` - shared runtime state used by workflow dashboards and intake engines.
- `brain_dashboard` - source home for the dashboard MVP; user-facing runtime target is `X:\GUI\brain-dashboard`.
- `conversion_lib` - source home for the shared source/URL to canonical Markdown conversion library; user-facing runtime target is `X:\Conversions\conversion-layer`.
- `station_lab` - safe bench for tuning paper-grader stations before full workflow integration.
- `stations` - target home for reusable station services; folder names end in `.station`.
- `workflows` - target home for end-to-end pipelines; folder names end in `.workflow`.
- `prompts` - target home for reusable assignment/system prompt packs; folder names end in `.prompt-pack`.
- `control-plane` - target home for preference-engine and repo mirrors on live X:.
- `corpus` - target home for C4C, C4C-wiki, FAP, BIL, and other local corpus lanes.
- `services` - target home for local services such as Ollama.
- `_archive` - zip files, websets, extracted bundles, and old import payloads.
- `_logs` - old/root logs moved out of the top level.
- `_state` - captures, digests, embeddings, ratings, active run state.

## Rule

If something here becomes an active user-facing surface, expose it through `X:\GUI\`, `X:\Conversions\`, `X:\EXPORTS\`, or a root click-button. Do not scatter new NLP folders at X:\ root.

## Naming

Backside is allowed to be the messy workbench, but every folder should name its type:

```text
<name>.model        model card / local model runtime contract
<name>.workflow     end-to-end process with 00_DROP, RUN.bat, OUTPUT, ARCHIVE
<name>.station      reusable station called by one or more workflows
<name>.prompt-pack  reusable prompts meant to be handed to AI partners
```

That gives David a fast read: what it is, not just what it is called.
