# READ_FIRST — Stations Orientation for Any LLM

**You are an AI partner (Opus, Codex, Sonnet, Haiku, Kimi, Gemini, GPT, or other) being brought in to work on stations in David Lowe's Theophysics Backside.** Read this file in full before touching anything. If anything here conflicts with what you remember, this file wins.

---

## 1. Where you are

```
X:\knowledge-refinery\BACKSIDE\STATIONS\
```

The **station tier** of the 3-tier Backside topology:

```
BACKSIDE/
  MODELS/      <-- model wrappers (substrate workers — built)
  STATIONS/    <-- you are here (one step in a pipeline)
  WORKFLOWS/   <-- routes that chain stations (not built yet)
```

**Mental model — memorize this:**

```
WORKFLOW -> STATION -> MODEL -> PROMPT -> SCRIPT -> OUTPUT -> GATE -> NEXT STATION
```

A workflow is a route. A station is one step. A model is the worker. A prompt is the instruction. A script is the machine. A gate decides if work passes downstream.

## 2. The contract

You are bound by David Lowe's R1–R7. Operationally:

- **R5:** if you think a binding, structure, or naming decision is wrong, say so BEFORE building. Don't silently "fix" it.
- **No file deletion.** Every "delete" is a move to `_ARCHIVE/`.
- **Label gradient.** When stating what a station does or claims, mark as **load-bearing**, **suggestive**, or **overclaimed**.
- **Independence rule.** Don't auto-converge with what other AIs posted in comms. Disagreement is signal.

## 3. Layout

```
STATIONS/
  READ_FIRST.md                <-- this file
  README.md                    <-- short pointer back here
  STATION_INVENTORY.md         <-- what exists (prose summary)
  stations_registry.yml        <-- single source of truth (yaml). AUTO-GENERATED — never hand-edit.
  stations_registry.lock       <-- present only during a rebuild
  _registry_backups/           <-- previous registries (timestamped)
  new_station.py               <-- duplicator (creates folders only — does NOT touch registry)
  new_station.bat              <-- thin wrapper
  registry_rebuilder.py        <-- ONLY legal writer of the registry. Reads station.yml from every folder.
  _tools/
    migrate_drop_numbers.py    <-- one-shot migration (already run 2026-05-16)
    _ARCHIVE/                  <-- deprecated tools
  stations/
    _TEMPLATE/                 <-- canonical template. DO NOT EDIT for one-offs.
    sci_embed/                 <-- 54 stations, plain names (no NN_ prefix). See STATION_INVENTORY.md.
    7q_forward/
    route_classifier/
    ...
```

## 4. CRITICAL — naming conventions (2026-05-16 decision)

```
Folder name = human-readable role     (e.g. html_to_md/)
station_id  = machine-readable identity (e.g. ST-CONV-008)
order:      = display/sort hint in station.yml (integer, NOT strict)
registry    = source of truth
```

**Folders DO NOT have number prefixes.** The old `NN_name` convention created collisions when multiple AIs scaffolded in parallel (three folders all numbered `12_`). Sort order moved into the `order:` field inside `station.yml`. Identity is `station_id`.

**Station IDs are per-lane:** `ST-NLI-001` is the first NLI station, `ST-NLI-002` is the second, etc. — independent of `order`.

## 5. How to create a new station — the only correct way

```cmd
cd X:\knowledge-refinery\BACKSIDE\STATIONS
new_station.bat name --lane LANE --model M-XXX --purpose "..." --status draft
```

Example:
```cmd
new_station.bat claim_dedup --lane CLAIM --model M-EMB-GEN-001 --purpose "Dedup new claims against the claim store." --status draft
```

**Arguments:**

| Flag           | What                                                          | Example                  |
|----------------|---------------------------------------------------------------|--------------------------|
| `name` (pos 1) | snake_case role name. Becomes the folder name.                | `claim_dedup`            |
| `--lane`       | Lane code, UPPERCASE.                                         | `--lane CLAIM`           |
| `--model`      | Bound model id from `..\MODELS\model_registry.yml`, OR API id.| `--model M-EMB-GEN-001` or `--model gpt-4o-mini` |
| `--provider`   | `local_wrapper` (default), `openai`, `anthropic`, `hf`.       | `--provider openai`      |
| `--purpose`    | One-line description.                                          | `--purpose "..."`        |
| `--status`     | `draft` (default), `active`, `paused`, `retired`.             | `--status draft`         |
| `--next-pass`  | Station ID to route to on gate pass.                          | `--next-pass ST-NLI-005` |
| `--order`      | Sort hint (default: max existing + 1).                        | `--order 50`             |
| `--dry-run`    | Preview without writing.                                       |                          |

**What it does:**
1. Slugifies `name` to derive the folder name (no number prefix).
2. Auto-derives `station_id` as `ST-LANE-NNN` (counts existing stations in that lane).
3. Auto-derives `order` as max existing order + 1.
4. Copies `stations/_TEMPLATE/` → `stations/<name>/` and substitutes placeholders.
5. **Does NOT write the registry.** Run `registry_rebuilder.py` afterward.
6. Aborts if folder exists (no clobber).

## 6. Registry — DO NOT hand-edit

`stations_registry.yml` is auto-generated by `registry_rebuilder.py` from every `station.yml`. Never edit by hand. After making any change (new station, status flip, model rebind, next-pass rewire), run:

```cmd
python registry_rebuilder.py
```

**Concurrency:** the rebuilder uses `stations_registry.lock` to block parallel runs. If you see `ERROR: lock present`, another rebuild is in progress — wait. If genuinely stale (no other process), delete the lock manually.

**Backups:** every rebuild snapshots the prior registry to `_registry_backups/stations_registry_<timestamp>.yml.bak`.

**Duplicate detection:** the rebuilder warns about duplicate `station_id` values and exits non-zero — humans resolve. Don't flip a duplicated station to `status: active`.

## 7. Customizing your station after scaffold

1. **Drop your Python runner at `scripts/run.py`.** The template's `03_run_prompt.bat` auto-detects it and calls `python run.py --in <input> --out <output>`. Your runner should:
   - Read input from `--in` (file path).
   - Write JSON to `--out`.
   - Write a `.md` companion alongside the JSON.
   - On gate failure, write to `../errors/`. On borderline, write to `../review/`.

2. **Fill in remaining `TODO` markers in `station.yml`.** Especially `gate.pass_if`.

3. **Update `PROMPT_SYSTEM.md`** if the station calls an LLM.

4. **Flip `status: draft` → `status: active`** in `station.yml`.

5. **Run `registry_rebuilder.py`** to reflect the change.

6. **Smoke-test:** `scripts\02_smoke_test.bat`.

## 8. Bound models

Models live at `X:\knowledge-refinery\BACKSIDE\MODELS\model_registry.yml`:

| Model id            | Wrapper folder                                 | What                              |
|---------------------|------------------------------------------------|-----------------------------------|
| `M-EMB-SCI-001`     | `MODELS/models/01_sci_embed`                   | SPECTER2 science paper embeddings |
| `M-TIME-001`        | `MODELS/models/02_timeline`                    | Timeline / temporal extraction    |
| `M-NLI-STRONG-001`  | `MODELS/models/03_nli_strong`                  | DeBERTa v3 large NLI              |
| `M-NLI-CLAIM-001`   | `MODELS/models/04_nli_claim`                   | MNLI / FEVER / ANLI claim NLI     |
| `M-NLI-ALT-001`     | `MODELS/models/05_nli_alt`                     | RoBERTa large NLI                 |
| `M-EMB-GEN-001`     | `MODELS/models/06_embed_general`               | MiniLM general embeddings         |
| `M-NLI-BASE-001`    | `MODELS/models/07_nli_base`                    | Baseline NLI (legacy)             |
| `M-RERANK-001`      | `MODELS/models/08_rerank`                      | Cross-encoder reranker            |

LLM bindings: use API names (`gpt-4o-mini`, `claude-opus-4-7`) with `--provider openai` or `--provider anthropic`.

Note: MODELS still uses `NN_` folder prefixes. That's their convention. STATIONS doesn't.

## 9. Spine wiring (refinery pipeline)

```
RAW FILE
  └→ ST-ROUTE-001  (route_classifier)
       └→ ST-CONV-001  (document_converter — dispatches to MarkItDown/Docling/Marker)
            └→ ST-CLAIM-001  (claim_extractor)
                 └→ ST-SUM-001  (lossless_summary)
                      └→ ST-SEVENQ-001  (7q_forward)
                           └→ ST-SEVENQ-002  (7q_reverse)
                                └→ ST-SEVENQ-003  (7q_evidence)
                                     └→ ST-GRAPH-001  (knowledge_graph)
                                          └→ ST-PUB-001  (publication_gate)
                                               └→ TERMINAL
                                                   (website|substack|zenodo|
                                                    proof_explorer|canon|review|archive)
```

Beyond the spine: substrate stations (NLI, embeddings, rerank) are parallel primitives called on demand; format stations (html_to_md, pdf_to_md, audio_to_txt, etc.) are alternatives ROUTE/CONV can dispatch to; content-analysis stations (semantic_drift, tone_consistency, etc.) are an emerging family — see STATION_INVENTORY.md for the full picture.

## 10. When in doubt

- **Post to comms hub** (channel `claude-code` or your own AI's channel) before guessing on model bindings, gate rules, or workflow wiring.
- **Check `stations_registry.yml` first** before scaffolding — your role may already exist.
- **Don't edit `_TEMPLATE/`** for one-off work. Template changes affect every future station — raise with David first.
- **Don't hand-edit `stations_registry.yml`** — your edits get overwritten on the next rebuild.

---

*Updated 2026-05-16 after the folder-number drop migration. Last verified: 54 stations in the registry.*
