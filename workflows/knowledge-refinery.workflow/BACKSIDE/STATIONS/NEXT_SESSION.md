# NEXT SESSION — open items from claude-code-forge

*Left 2026-05-16 late. Pick up here.*

---

## What landed tonight (so you don't redo it)

- **16 CONV stations registered** — `ST-CONV-001` (dispatcher, demoted from `13_document_converter`) + `ST-CONV-012..026` (15 granular: html, pdf, docx, pptx, audio, video, youtube, md_cleaner, plaintext, equation, table, image, ocr, frontmatter, asset).
- **`ST-CONV-027 pdf_classifier`** — wired, smoke-tested, registered. Classifies a PDF as `text` / `scanned` / `mixed` / `empty` and recommends the next station. 157ms on a real text PDF.
- **`registry_rebuilder.py`** — the only legal writer of `stations_registry.yml`. Scans every `station.yml`, atomic backup → tmp → replace, `.lock` blocks concurrent rebuilds. `new_station.py` no longer touches the registry directly (the lost-write race is fixed).
- **Archived (in `STATIONS/_ARCHIVE/`):** `16_markitdown_converter`, `17_marker_pdf_converter` — both with reason files. MarkItDown and Marker are backends used inside granular stations, not stations themselves.
- **`EXCEL_OUTPUT_PLAN.md`** — full schema spec for xlsx outputs across `route, conv, claim, sum, sevenq` (22 stations). Joinable on `run_id` / `doc_id` / `claim_id`.
- **`INSTALL_REPORT.md` at `X:\00_CONVERSION\`** — 9 conversion tools installed + smoke-tested (markitdown, docling, marker, faster-whisper, yt-dlp, ffmpeg, etc.). Plus Codex's `theophysics-conversion` lib installed editable.
- **Broadcast msg id 827** — coordination post to all AIs about the new registry write protocol. Codex direct channel rejected (cross-channel block), broadcast went through.

---

## Tier 1 — high-value, finishable next session

### 1. Wire `run.py` for the 15 granular CONV stations
Right now they're scaffolded shells. Each needs a runner that calls the right tool:
- `html_to_md` → MarkItDown
- `pdf_to_md` → Docling (`do_ocr=False`)
- `docx_to_md`, `pptx_to_md` → MarkItDown
- `audio_to_txt`, `video_to_txt`, `youtube_to_txt` → yt-dlp + ffmpeg + faster-whisper
- `md_cleaner` → markdown-it-py
- `md_to_plaintext` → strip-markdown (or pandoc)
- `equation_extract`, `table_extract`, `image_extract` → filter station — reads pdf_to_md output, doesn't re-parse
- `ocr_scan` → Marker (first run downloads ~1GB models)
- `frontmatter_builder` → shared lib (every station calls it, this just standardizes)
- `asset_packager` → moves assets to canonical `/assets/{slug}/` + rewrites links

**Pattern to copy:** `stations/pdf_classifier/scripts/run.py`. Same `--in/--out` contract, same JSON+MD output, same error handling. Don't over-engineer — each is ~60-100 lines.

### 2. Build the dispatcher logic in `ST-CONV-001`
Currently has no runner. Should:
- Read input file
- Switch on extension (deterministic)
- Fall back to `magika` content sniffing for unknown/missing extensions
- Emit `routing.yml` with `picked_station_id` + reason
- For PDFs specifically, call `ST-CONV-027 pdf_classifier` first to decide text vs scanned routing
- No LLM — keep dumb-layer compatible

### 3. Build `xlsx_rebuilder.py`
Spec is in `EXCEL_OUTPUT_PLAN.md`. Same write protocol as `registry_rebuilder.py` (`.lock` + atomic). Concatenates per-station workbooks → per-lane → master rollups at `BACKSIDE\exports\workbooks\`. Schema is already defined; you just need the implementation.

---

## Tier 2 — station ideas I'd add (in priority order)

1. **`hash_dedupe`** — MinHash + Jaccard threshold. At 14k pages dupes WILL exist. Stops the refinery from doing N+1 work on identical content. `pip install datasketch`.
2. **`encoding_repair`** — detect Windows-1252 / cp866 / UTF-16 mojibake and re-encode to UTF-8. Catches garbage early. Use `chardet` or `ftfy`.
3. **`language_detect`** — flag non-English (Spanish/Greek/Hebrew for theology). `fastText` langid or `lingua-py`.
4. **`section_splitter`** — for 800-page books, split into chapters and emit one MD per section. Lets the refinery work at section granularity.
5. **`front_back_matter_strip`** — kill ISBNs, ToCs, blank pages, indexes. Stops the refinery from wasting cycles on "no claims here."
6. **`citation_extractor`** — pull bib refs to `citations.json`. Different from claim extraction.
7. **`audio_chapter_split`** — split long audio by silence/chapter markers BEFORE Whisper. Parallelizable + independently re-transcribable.

NOT in scope for conversion layer (deferred to refinery-output tier):
- `obsidian_link_builder` — injects `[[next]] [[prev]] [[home]]`. Needs corpus order, which only exists after refinery has decided.

---

## Real bugs to fix (not mine, but flagged)

### a. `stations/route_classifier/station.yml` line 30 — YAML parse error
A bare `*` is being parsed as an anchor reference. `registry_rebuilder.py` skips this station every rebuild. Whoever owns ST-ROUTE-001 should replace the `*` with the intended placeholder. Until fixed, this station won't appear in the registry.

### b. `new_station.py` per-lane counter assumes contiguous IDs
The refactored script counts existing stations in the lane and assigns `lane_count + 1`. My CONV stations skip 001 → 012, so a fresh CONV station gets ST-CONV-017 (collision with my video_to_txt). Tonight I worked around it by editing the `station.yml` after scaffolding. Long term: the counter should compute `max(existing_NNN) + 1` instead of `count + 1`. One-line fix.

### c. `pypdfium2.get_text_range()` deprecation warning
`stations/pdf_classifier/scripts/run.py` line ~55: `tp.get_text_range()` prints a `UserWarning: ... will be implicitly redirected to get_text_bounded()`. Cosmetic, not blocking. Swap to `tp.get_text_bounded()` when convenient.

### d. ID-naming drift between `7qs` and `sevenq`
STATION_INVENTORY notes there are 2 stations on the legacy `7qs` lane and 3 on `sevenq`. The Excel plan assumed `sevenq` only. Resolve before workflow tier reads either as canonical.

---

## Coordination snapshot (other AIs are active)

- Registry was at 44 stations after my pass, now at **64** — other LLMs scaffolded ~20 more in the same window. Lanes now include `axiom`, `facts`, `score`, `session`, `yaml` that didn't exist earlier tonight. Constant motion.
- Anyone touching `STATIONS/` should: (a) edit/create `station.yml` files only, (b) run `registry_rebuilder.py` after, (c) check broadcast for recent coordination. Posted broadcast msg 827 with the new write protocol.

---

## Where to start tomorrow

If you've got 30 minutes: wire `run.py` for `html_to_md`. Smallest, fastest, validates the pattern across the lane. Then duplicate the pattern to `docx_to_md` and `pptx_to_md` (all three use MarkItDown — copy-paste-tweak).

If you've got 2 hours: do above + `pdf_to_md` (Docling) + `audio_to_txt` (faster-whisper). That's 5 runners and the four most-common file types. Real conversion starts working at that point.

If you've got a day: wire all 15 + dispatcher + xlsx_rebuilder. Conversion layer goes from "scaffolded" to "production-ready" for the first 14k-page push.
