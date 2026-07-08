# Cowork Review Pass — html-article.workflow

Reviewer: Cowork (Claude, opus-4-7)
Date: 2026-05-22
Scope: single review pass over Round 1 swarm output. Not a redesign. Eight checks per brief.

---

## 1. Overall Assessment

Round 1 landed substantive, documented work on 7 of the 8 testable lanes (02, 03, 04, 05, 07, 10, 13; 14 is a sink + contract only). The contracts are real, the calibration article was actually processed, and most workers wrote thoughtful challenger notes. But the swarm ran in parallel without resolving the addressing-ownership question first, and that decision shows up as concrete drift in three places: section_id format, paper_uuid generation, and semantic-hash format. None of those are fatal — they're the kind of thing that surfaces exactly because contracts and sample outputs were both produced — but they have to be reconciled before lane 15 (Section Packets) or 16 (Final Assembly) can join across lanes.


---

## 2. What's Solid

- **`configs/shared_lib/` is real, deterministic, and importable.** `ids.py` (NAMESPACE `28282828-...`, `stable_uuid`, `slugify`), `address.py` (`score_vector`, `vector_string`, `semantic_hash`, `build_address`, TIE_BREAK), and `schemas.py` (pydantic models for `MarkdownBlock`, `ClaimArch`, `KillArch`, `SemanticTag`, `LosslessArtifact`) all exist and are self-consistent. This is the convergence point — every lane should be pulling from these, not inventing parallel formats.
- **Lane 02 (Section Map)** — strongest deliverable. Real `paper_uuid` derived deterministically, `section_id` rule documented and matches output (`sec-{ord:03}-{slug}`), `stable_uuid` joins to `ids.stable_uuid`, calibration produces exactly 4 sections as expected, GTQ-03 produces 87 sections and 192 equation candidates. Challenger notes are concrete and load-bearing-aware.
- **Lane 03 (YAML + Filing)** — inherits Lane 02's `paper_uuid` cleanly (the only lane that actually consumed upstream). Honest about `vector_string=null, hash=null, vector_owner_lane=04_TAGS`. Provenance ledger (`extracted` / `derived` / `inferred`) is exactly what the work order asked for.
- **Lane 05 (Claims)** — the three-layer arch is implemented, calibration `surface_claim` / `buried_claim` / `operational_claim` are exact textual matches to `CALIBRATION_EXPECTED.md`. Two-pass design (station first, LLM refine) is documented and traceable. `station-firstpass.json` is preserved.
- **Lane 07 (Math Translation)** — correctly returns `equation_count: 0, math_status: "passed-empty"` for the calibration article. Uses `shared_lib` `semantic_hash` format. Loopback-on-stale-preview is wired and documented.
- **Challenger notes that exist are concrete.** Lane 02 caught its own load-bearing bug (`source_offset_start/end` declared but never written) and a real attack surface (mal-formed HTML desyncs `html.parser`). Lane 04 caught the T-axis hardcoding in `score_vector`. Lane 05 caught the bool-vs-enum problem in `support_needed`. These are exactly the kind of catches the challenger pass was designed for.
- **Loopback channel exists.** Lane 14 has a contract, README, and run_prompt. Lane 07's run.py writes here automatically per the contract.


---

## 3. Small Fixes Made (in place)

1. **`04_TAGS/contract.json` — `semantic_address.policy` block rewritten.**
   Old text claimed *"Lane 04 does NOT mint the canonical semantic address. Lane 02 mints it."* This directly contradicted (a) `lane_registry.json` notes on lane 02 (*"Vector/address/hash owned by 04_TAGS"*), (b) Lane 02's own README + contract (which explicitly disclaim minting the address), (c) `CALIBRATION_EXPECTED.md` lane table (which puts vector + semantic address under 04), and (d) `SWARM_WORK_ORDER_ROUND1.md`. New text states that lane 04 mints the 10-variable vector + semantic_hash from upstream `address_candidate` (D/N/V/A/U/R) supplied by lane 03, and pins the implementation to `configs/shared_lib/address.py`.

2. **`04_TAGS/contract.json` — `loopback_conditions` updated.**
   Removed the impossible condition *"Vector recomputed from section_map disagrees with lane 02 vector"* (lane 02 stores no vector). Replaced with a deterministic-computability check and an address_candidate-from-lane-03 check.

3. **`04_TAGS/README.md` — ownership paragraph rewritten** to match the contract fix above. Added a one-line note that the contract was corrected in this review pass.

No other inline edits made. All other findings are flagged below for David / Opus rather than freelanced.


---

## 4. Medium Issues (flagged — do not freelance the fix)

### M-1. `section_id` format drift across lanes
**Where:** lane 02 vs lane 04, lane 05, lane 10.

- Lane 02 (canon): `sec-001-pilot-pre-flight-checklist` — hyphens, 3-digit zero-pad, slug from `heading_text`.
- Lane 04 sample: `sec_01_pilot-pre-flight-checklist-intro` — underscores, 2-digit pad, `-intro` suffix.
- Lane 05 sample: `sec_01_pilot-pre-flight-checklist-intro` — same as 04 (they coordinated, but with each other, not with 02).
- Lane 10 sample (GTQ-03): bare UUID like `1b0ba8c7-2cfa-5a0f-9b74-bf742ecd1993` — no human-readable handle at all.

**Why it matters:** every downstream join is keyed on `section_id`. If any lane downstream tries to merge tags ↔ claims ↔ rigor for the same section, it cannot — there is no shared key. Lane 15 (Section Packets) and lane 16 (Final Assembly) are blocked structurally.

**Why it happened:** lanes 04, 05, and 10 ran while lane 02 was still in flight and mocked their upstream from the raw drop file. They each invented a format and documented it as `provenance.mocked=true`. That's honest, but the re-run hasn't happened.

**Recommended fix:** pin the format in `configs/shared_lib/ids.py` as `section_id(paper_uuid, ordinal, heading_text)` returning lane 02's format. Have every downstream lane import that helper. Then re-emit 04 / 05 / 10 sample outputs against real lane 02 output.

### M-2. `paper_uuid` and `page_id` formats fork per lane
**Where:** lanes 02/03 vs lanes 04, 05, 07, 10.

- Lane 02/03 (calibration): `paper_uuid = 26d2c80e-e695-552e-882e-c3b6de87d2a1`, `page_id = page::26d2c80e-...`.
- Lane 04 (calibration): `paper_uuid = "MOCK-paper-uuid-calibration-pilot-preflight"`, `page_id = "MOCK-page-id-..."`.
- Lane 05 (calibration): same MOCK strings as 04.
- Lane 07 (calibration): `page_id = "calibration-pilot-preflight-checklist"` (slug).
- Lane 10 (GTQ-03): `paper_uuid = d95ef020-3fdb-5ddc-a05e-3b3d6309b1ea`, `page_id = c3cb7838-99aa-5845-b3c8-1f4274b057b0` — both bare UUIDs, neither matches lane 02's `f853617b-baf2-50d0-9b9b-96dd23501625` for the same article.

**Why it matters:** same as M-1. The Master_Index workbook is keyed on `paper_uuid`. If lane 02 inserts row A with one UUID and lane 10 attempts to update with a different UUID, the workbook gains duplicate rows and the append rule in `MASTER_INDEX_WORKBOOK_CONTRACT.md` fails silently.

**Recommended fix:** add `paper_uuid(source_path, content_hash)` and `page_id(paper_uuid)` helpers to `shared_lib/ids.py`. Mandate that every lane call these helpers, never invent. Then re-emit samples.

### M-3. Lane 04 forked the semantic_hash format
**Where:** `04_TAGS/sample_output/calibration/semantic-address.json` and `tags.json`.

- shared_lib `semantic_hash()` returns: `G3Q0-K3S0-M3F0-T3C0-R3E0` (matches lane 07 and lane 10 output).
- Lane 04 emitted: `G3-Q0-K3-S0-M3-F0-T3-C0-R3-E0` (different separator pattern).

**Why it matters:** the address is the artifact identity. If lane 04's hash doesn't byte-equal lane 07's / lane 10's / shared_lib's, then any downstream lane that joins on `semantic_address` string sees two different artifacts. `CALIBRATION_EXPECTED.md` shows the pattern as `[G·Q][K·S][M·F][T·C][R·E]` which is the pair-template — the lane 07/shared_lib format honors it; lane 04 does not.

**Recommended fix:** lane 04 must `from shared_lib.address import semantic_hash` and use it directly. No hand-rolled format. Re-emit samples. (The contract edit already pins this; the sample output still needs to be regenerated.)

### M-4. `pipeline_order` is defined in two places and they disagree
**Where:** `configs/lane_registry.json` vs `configs/MOVEMENT_AND_TRACE_CONTRACT.md`.

- `lane_registry.json`: `00 → 01 → 08 → 02 → 03 → 04 → 07 → 05 → 06 → 10 → 09 → 11 → 12 → 15 → 16 → 17` (vectors-before-section-map).
- `MOVEMENT_AND_TRACE_CONTRACT.md` "Recommended Processing Order": `07 → 01 → 02 → 03 → 04 → 05 → 06 → 08 → 09 → 10 → 11 → 16 → 17` (math-first, no 15, no 12, no 13/14).

**Why it matters:** workers chose one or the other. Lane 07's contract has `upstream_lanes: []`, consistent with MOVEMENT (math first). Lane 04 lists `08` in upstream, consistent with lane_registry (vectors before tags). They can't both be right.

**Recommended fix:** pick one canon, delete or downgrade the other (e.g. mark MOVEMENT as "historical notes" if lane_registry is canon). The registry's `pipeline_order` is the more recent and more complete artifact.

### M-5. `03_YAML_METADATA` overloads `status` and `state`
**Where:** `03_YAML_METADATA/sample_output/CALIBRATION/metadata.json`.

Output shows `"status": "F"` AND `"state": "F"` — same value, two field names. The Master Index workbook contract has a `status` column (publish lifecycle: draft/review/published). `SEMANTIC_ADDRESS_AND_ROUTING.md` has `state` (the V component of the address: F = final). They are not the same axis. Calibration source frontmatter declares `state: F` (the address V), but lane 03 copied it into `status` too.

**Why it matters:** when GTQ-03 hits the workbook, `status` will read "F" (which means "final" in the address but isn't a valid Master_Index `status` value). The append rule will silently accept it and you'll lose the publish-lifecycle signal.

**Recommended fix:** treat `state` (address V) and `status` (lifecycle) as separate fields with separate vocabularies. Default `status` to `draft` when source doesn't say.

### M-6. `source_offset_start` / `source_offset_end` are contract fields in lane 02 but always `null`
**Where:** lane 02's section objects.

Lane 02 declared its own challenger note 02-O2 about this: the parser tracks `_char_offset` but never writes the offsets onto emitted sections. So 14_LOOPBACK_REVIEW cannot do byte-precise reattachment, and lane 11_HTML_RENDER cannot slice the original source HTML cleanly. This is the cheapest of all the medium fixes (a few lines in `HtmlSectionWalker.parse_html`), and it's load-bearing for rendering fidelity.

**Recommended fix:** capture offset at `heading_open` and at the next `heading_open` (or `section_close`) and write them into the section dict.

### M-7. Three lanes did not write `challenger_notes.json`
**Where:** lane 03 (yaml), lane 07 (math), lane 10 (rigor), lane 13 (ledger).

Lanes 02, 04, 05 produced detailed, concrete challenger notes. The other four did not. The requirement was added mid-round so this is partly expected, but per `WORKER_DISPATCH.md` it's "REQUIRED" — meaning whatever Opus decides is canon, the four missing files should land before round 2.

**Recommended fix:** ask worker-1 to write `03_YAML_METADATA/sample_output/CALIBRATION/challenger_notes.json`; worker-3 for 07; worker-5 for 10 and 13. Each should follow the format in `WORKER_DISPATCH.md` (`overlooked[]` + `attack_surface[]`).

### M-8. Lane 13 (Layer Ledger) sample output not at advertised path
**Where:** `13_LAYER_LEDGER/sample_output/`.

The README says the runner lives at `..\10_RIGOR\run.py` and writes ledger outputs into 13's folder. The contract advertises `layer-ledger.json` and `section-pass-matrix.csv` as products. Neither file exists at `13_LAYER_LEDGER/sample_output/layer-ledger.json` (root) or `13_LAYER_LEDGER/sample_output/calibration/layer-ledger.json`. Lane 10's rigor-report.json carries section pass markers internally, but the dedicated ledger artifact is missing.

**Recommended fix:** either run worker-5's runner end-to-end and commit the ledger output, or update the contract to document that the ledger lives inside rigor-report.json for round 1.

### M-9. `configs/NABLA_DESIGN_BIBLE.md` doesn't exist
**Where:** referenced in the review brief and arguably in shared cognitive vocab; no file at that path.

The brief told me to read it ("the 30 design rules for semantic addressing"). It is not in `configs/`. Either it never landed in round 1, or it lives under a different name. The closest documents present are `SEMANTIC_ADDRESS_AND_ROUTING.md` (60 lines, partial), `MOVEMENT_AND_TRACE_CONTRACT.md`, and `FILE-NAMING-SYSTEM.md`. None of them is "30 rules."

**Recommended fix:** if the Bible exists somewhere else (e.g. an Obsidian vault), drop a copy or a wikilink stub in `configs/`. If it was never written, declare it a round-2 deliverable explicitly — multiple workers are operating against assumed rules that no shared document codifies.


---

## 5. Big Issues

### B-1. The addressing system is declared in the configs but only partially flowing through the lanes.

The brief asked whether the Nabla semantic address (`D/N/V/A/U/R :: VECTOR :: HASH`) is actually flowing or just declared. Honest answer: **it's flowing in 02→03→07→10 (mostly), but the vector + hash portion is broken at lane 04**, which is the lane that's supposed to mint them.

Concretely:
- `shared_lib/address.py` correctly implements `score_vector`, `vector_string`, `semantic_hash`, `build_address` — these are real and deterministic.
- Lane 02 produces stable `paper_uuid` + `section_id` + `stable_uuid` — good.
- Lane 03 produces D/N/V/A/U/R `address_candidate` cleanly — good.
- **Lane 04 (which the registry says owns vector + hash) ran on mocked upstream**, used a hand-rolled hash format, and its contract until this review pass claimed lane 02 owned the address. Vector + hash were emitted but they're not byte-equal to what `shared_lib.semantic_hash` would produce.
- Lane 07 uses `shared_lib` properly and emits a clean address.
- Lane 10 emits a clean address for GTQ-03 but with a different `paper_uuid` than lane 02 produced for the same file.

**The pipeline cannot actually claim that a single semantic address propagates end-to-end yet.** It can claim that the components exist, the helpers are correct, and three lanes touch the system. To close the gap, lanes 04, 05, and 10 must re-run on real upstream (not mocked), call `shared_lib` helpers (not their own format), and produce identical address bytes for the same source article.

This is not fatal — it's the natural consequence of running five workers in parallel without first locking the address protocol. The fix is mechanical, not architectural. But it has to happen before any joins downstream.

### B-2. Mock provenance is being used as a substitute for upstream coordination.

Three workers (lanes 04, 05, 10) marked `provenance.mocked = true` and proceeded. That was explicitly authorized by the work order ("If upstream is missing, mock input and document it"). But the mocks are not interchangeable with real upstream — they used different `paper_uuid`, different `section_id` format, different `page_id` shape. So when the real upstream arrives, those samples don't validate anything except "the lane ran." They need to be re-emitted, not just relabeled.

Recommendation: in round 2, gate "testable" status on at least one calibration run against REAL upstream output for at least 02 → 04 → 05 (the critical join chain). A lane is only testable if its output can be joined to its real upstream's output on stable keys.


---

## 6. Recommended Next Actions

Ordered, smallest blast radius first.

1. **Pick canon for pipeline_order.** Resolve M-4. Either `lane_registry.json` or `MOVEMENT_AND_TRACE_CONTRACT.md` is canon — mark the other "historical." Five-minute decision; unblocks everything else because workers stop having two playbooks.

2. **Add ID helpers to `shared_lib/ids.py`.** Resolve M-1 + M-2. Three helpers:
   - `section_id(paper_uuid, ordinal, heading_text) -> str` returning `sec-{ord:03}-{slug}`.
   - `paper_uuid(source_path, content_hash) -> str` (already exists as `file_doc_id` — promote and rename).
   - `page_id(paper_uuid) -> str` returning a stable format (pick: `page::{uuid}` or bare uuid; commit to one).
   Then forbid lanes from inventing their own.

3. **Re-emit lane 04, 05, 10 sample outputs against real lane 02 + 03 upstream.** Resolves M-1, M-2, M-3, and provides a real cross-lane join for B-2. The calibration article is small enough that this is a 20-minute exercise.

4. **Patch lane 02 to record `source_offset_start/end`.** Cheap, load-bearing, lane 02 already flagged it (M-6 / challenger 02-O2).

5. **Have lane 04 import `shared_lib.semantic_hash` and drop the hand-rolled hash.** Resolve M-3 by sample re-emit.

6. **Fix `03_YAML_METADATA` `state` vs `status` overload.** Resolve M-5. Small contract + runner fix.

7. **Backfill missing `challenger_notes.json`** for lanes 03, 07, 10, 13 (M-7). Each note is < 200 lines and gets it on parity with 02 / 04 / 05.

8. **Either commit lane 13's ledger output or update its contract** (M-8). Small.

9. **Resolve NABLA_DESIGN_BIBLE.md** (M-9): either drop the file in `configs/` or schedule it explicitly. Workers are operating on an assumed shared document that doesn't exist.

10. **After 1–6 land, run the full calibration article end-to-end through 02 → 03 → 04 → 05 → 07 → 10 → 13.** That's the readiness gate for round 2. Until then, this round shipped *contracts and intent*, not a working pipeline.

---

## Coverage Note

I did not redesign anything. I did not touch lane code. Inline fixes were limited to (a) one contract.json text block in lane 04 and (b) one README paragraph in lane 04 — both correcting documented internal contradictions in that lane's own description of who owns the semantic address. Everything else is flagged here for David and Opus to route.

Eight brief checks accounted for:
1. Contract field consistency → see M-1, M-2, M-5.
2. Calibration alignment → verified for 02, 03, 05, 07. Lane 04 vector matches expected; hash format wrong (M-3). Lane 10 didn't run against calibration (only GTQ-03).
3. Schema convergence → `shared_lib/schemas.py` is real and well-shaped; lane 04 forked the hash format (M-3); lane 10 invented its own paper_uuid format (M-2).
4. Pipeline order vs dependencies → conflict found (M-4).
5. Missing blocking lanes → 01_LOSSLESS is the biggest gap; lanes 02/04/05 all flag they're reading raw `00_DROP` instead. Not blocking testable status of those lanes but blocking real production runs. 08_SECTION_VECTORS is referenced by lane 04 contract as upstream but doesn't exist — lane 04 currently can't actually consume it.
6. Challenger notes → 3 of 7 testable lanes wrote them (M-7).
7. Doc drift → M-4, M-5, and the lane 04 ownership flip I fixed inline.
8. Addressing system flow → see B-1.

— Cowork, 2026-05-22
