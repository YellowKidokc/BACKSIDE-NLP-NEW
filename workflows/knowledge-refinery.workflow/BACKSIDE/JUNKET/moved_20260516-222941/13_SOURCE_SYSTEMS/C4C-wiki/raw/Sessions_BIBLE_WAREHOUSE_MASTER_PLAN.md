# Bible Data Warehouse — Master Load Plan
**POF 2828 | Theophysics Project | 2026-04-17**
**Target:** `bible.*` schema in `theophysics` PostgreSQL DB on 192.168.1.97:5432
**Source:** `C:\Users\lowes\Desktop\Bible Studies E xcel-20251109T142609Z-1-001\Bible Studies E xcel\`

---

## ⚠ READ THIS FIRST — For the session picking up this work

You are resuming a Bible data warehouse build for David Lowe (POF 2828). The scoping is done. Your job is to execute phase by phase with approval gates.

**David's priorities, in order (this is non-negotiable):**
1. Timeline first — "the timeline is probably the most important to me right now"
2. MacArthur commentary second — second most important
3. Everything else by technical dependency order

**Current state:**
- Nothing is loaded in `bible.*` yet — the schema doesn't exist
- Source folder audited: 87 files, 44 with data, ~1.7M unique rows
- The interlinear pickle may still be cached at `C:\Users\lowes\AppData\Local\Temp\tp_query\interlinear.pkl` (133MB) — use it if present, re-load from `bsb_tables.xlsx` if gone

**Postgres connection:**
- Host: `192.168.1.97:5432`
- Database: `theophysics`
- User: `postgres`
- Password: `Moss9pep28$` (rotate when David is at the NAS — leaked in earlier chat)
- psql path: `C:\Program Files\PostgreSQL\17\bin\psql.exe`
- Python: `C:\Python313\python.exe`

**Existing schemas to preserve and NOT touch:**
`kj`, `theology`, `grace_study`, `hell_study`, `apologetics`, `compressed`, `epistemic`, `foundation`, `journal`, `master`, `moral_decay`, `ov4`, `public`, `vault`, `claude_memory`

**Non-negotiable rules from David:**
1. Match existing naming conventions (lowercase snake_case, schema = domain)
2. Verify nothing is already loaded before loading (query information_schema)
3. Show DDL + sample data + dedup decisions BEFORE running each phase
4. Get explicit "go" before executing each phase
5. Every table gets a `verse_euid` column where applicable (pattern: `BC-CCC-VVV`)
6. No word `"tools"` applied to AI collaborators
7. Claude in Chrome for browsing, not web_search plugin

---

## Mission

Load 44+ Bible data files from the source folder into a properly organized `bible.*` schema in PostgreSQL. Queryable by Obsidian via live SQL (recommended plugin: `obsidian-sql-seal`). This is the foundation for all future Bible-related theological, apologetic, and linguistic work across the Theophysics project.

---

## Source Inventory (summary)

- **87 total files** (250 MB CSV + 186 MB XLSX = 436 MB)
- **44 files with actual data** (rest are scripts, docs, empty SQLite schemas)
- **~1.7 million unique rows** deduplicated across all files
- Duplicates identified: `bsb_concordance` exists as both .csv and .xlsx; `KJV.xlsx` and `kjv (1).xlsx` are the same file; `KJV_with_MacArthur_Commentary (2).xlsx` duplicates (1); etc. Load CSV where CSV exists, skip xlsx duplicate.

---

## PHASE 1: TIMELINE (David's #1 priority) — ~1 hour

Goal: A queryable timeline. "Who was alive in -930 BC?" "What events happened during the United Kingdom period?" "What verses mention David (person_1282)?" All answerable with one JOIN.

| Table | Source file | Rows | Notes |
|---|---|---|---|
| `bible.books` | `BibleData-Book.csv` | 66 | Load first — needed for EUIDs |
| `bible.chapters` | `Chapters.csv` | 1,189 | Chapter metadata |
| `bible.verses` | `Verses.csv` | 31,102 | Canonical verse table; joins `kj.verses` via EUID |
| `bible.timeline` | `Bible Timeline.csv` | 584 | Timeline markers |
| `bible.periods` | `Periods.csv` | 250 | Historical periods |
| `bible.epochs` | `BibleData-Epoch.csv` | 1,991 | Time-period classifications |
| `bible.events` | `BibleData-Event.csv` + `Events.csv` (deduped) | ~1,700 | Biblical events |
| `bible.persons` | `BibleData-Person.csv` | 3,009 | Needed for timeline — persons have birth/death years |
| `bible.persons_detail` | `People.csv` | 3,793 | Extended info — reconcile overlap with `persons` on load |
| `bible.person_verses` | `BibleData-PersonVerse.csv` + `-Apostolic.csv` + `-Tanakh.csv` | 88,534 | Add `source` column marking which file (general/apostolic/tanakh) |
| `bible.people_groups` | `PeopleGroups.csv` | 20 | Tribes, nations |

Jesus Christ = `person_905` in this system. Verify on load.

---

## PHASE 2: MACARTHUR COMMENTARY (David's #2 priority) — ~1 hour

Goal: David writes a note about any verse → one SQL query returns MacArthur's commentary on that verse.

| Table | Source | Rows | Notes |
|---|---|---|---|
| `bible.commentary_macarthur` | `macarthur_complete_bible.xlsx` (5.2MB) OR `MacArthur_Commentary_Only.xlsx` (0.7MB) | TBD | Inspect both xlsx sheets before committing. Pick cleaner source. Load with `verse_euid` FK. |

First task in Phase 2: read both xlsx files, show sample rows, let David pick which is authoritative.

---

## PHASE 3: ADDITIONAL TRANSLATIONS — ~1.5 hours

| Table | Source | Rows | Notes |
|---|---|---|---|
| `bible.translations` | derived from xlsx filenames | ~15 | Translation catalog |
| `bible.translation_verses` | all xlsx + ASV.csv, BBE.csv, LEB.csv | 31,102 × ~15 ≈ 467k | One row per translation-verse |
| `bible.commentary_matthew_henry` | `matthew_henry_enhanced.xlsx` (cleanest) | TBD | Second commentary source |

Translations to load: KJV, AKJV, ASV, BBE, LEB, YLT, BSB, BRB, DBT, DRB, ERV, JPS, WBT, WEB.

---

## PHASE 4: ORIGINAL LANGUAGES + STRONG'S — ~2 hours

This is what the Jesus Vocabulary Study needs. Full Greek NT + Hebrew OT with word-level tagging.

| Table | Source | Rows | Notes |
|---|---|---|---|
| `bible.bsb_interlinear` | `bsb_tables.xlsx` → `biblosinterlinear96` | 754,649 | Word-level Hebrew OT + Greek NT with Strong's + morphology + BSB English |
| `bible.alamo_polyglot` | `AlamoPolyglot.csv` | 31,102 | Parallel Hebrew/Greek/English/Aramaic per verse |
| `bible.strongs_heb` | `HebrewStrongs.csv` | 45,859 | Hebrew Strong's lexicon |
| `bible.strongs_grk` | extracted from `bsb_interlinear` | ~5,600 | Greek Strong's lexicon |
| `bible.cross_refs` | extracted from `bsb_interlinear` Crossref column | ~7,000 | 1,328 source rows × ~5 hrefs each |
| `bible.section_hdgs` | extracted from `bsb_interlinear` Hdg column | ~1,500 | Section headings |

---

## PHASE 5: PLACES + BIBLE NAMES — ~30 min

| Table | Source | Rows |
|---|---|---|
| `bible.places` | `BibleData-Place.csv` + `Places.csv` (deduped) | ~2,030 |
| `bible.place_labels` | `BibleData-PlaceLabel.csv` | 141 |
| `bible.place_verses` | `BibleData-PlaceVerse.csv` | 2,091 |
| `bible.person_labels` | `BibleData-PersonLabel.csv` | 3,749 |
| `bible.person_relationships` | `BibleData-PersonRelationship.csv` | 5,450 |
| `bible.bible_names` | `Bible Names.csv` | 2,624 |
| `bible.hitchcocks_names` | `HitchcocksBibleNamesDictionary.csv` | 2,623 |

---

## PHASE 6: CONCORDANCE + REFERENCE — ~2 hours (largest loads)

| Table | Source | Rows |
|---|---|---|
| `bible.bsb_concordance` | `bsb_concordance.csv` | 741,528 |
| `bible.bsb_topical_index` | `bsb_topical_index.csv` | 163,836 |
| `bible.word_index_kjv` | `WordIndex.csv` | 790,686 |
| `bible.references` | `BibleData-Reference.csv` | 31,102 |

Plan for streaming load (COPY FROM or chunked INSERT) — these are the only loads that benefit from batch optimization.

---

## PHASE 7: SPECIAL CONTENT — ~30 min

| Table | Source | Rows |
|---|---|---|
| `bible.commandments` | `BibleData-Commandments.csv` | 613 |
| `bible.prophecies` | `Bible prophecies full.csv` | 2,982 |
| `bible.tagging_master` | `Bible_Tagging_Master_Workbook.csv` | 3,793 |

---

## Files EXCLUDED (not loaded — and why)

| File | Reason |
|---|---|
| `ArXiv_old.csv` (21 MB, 266k rows) | Likely research papers, not Bible data |
| `Arguments_For_Against_God.xlsx` | Apologetics content — belongs in `apologetics` schema, not `bible` |
| `Conversion_Flow_Workbook.xlsx` | Tiny, unclear purpose |
| All `.db` files | Empty SQLite schemas (verified) |
| `.py`, `.ps1`, `.md`, `.txt` | Infrastructure files |
| `kjv (1).xlsx`, `asv.xlsx` (duplicates), `KJV_with_MacArthur_Commentary (2).xlsx`, `wbt (1).xlsx` | Duplicates |
| `bsb_concordance.xlsx`, `bsb_topical_index.xlsx`, `Bible_Tagging_Master_Workbook.xlsx`, `Bbile TGimeline .xlsx` | Redundant XLSX where CSV exists |
| `KJV_with_Matthew_Henry_Smart_Mapping.xlsx` | Use `matthew_henry_enhanced.xlsx` instead (cleaner) |

---

## EUID Convention (how everything joins)

- **Verse EUID:** `BC-CCC-VVV` (e.g., `MT-005-022` = Matthew 5:22)
- **Word EUID:** `BC-CCC-VVV-WWWW` (e.g., `MT-005-022-0015` = 15th word of Matthew 5:22)
- **Book codes:** 2-letter, matching existing `kj.book_codes` table. Verify mapping on Phase 1 load.

All `bible.*` tables with verse-level data include `verse_euid` for FK joins to `bible.verses`, `kj.verses`, `grace_study`, `hell_study`.

---

## Approval Gates (before each phase)

The session running this plan MUST:
1. Show the DDL (`CREATE TABLE` statements)
2. Show a 3-row sample of each source file
3. Show dedup decisions with row counts before/after
4. Wait for explicit "go" from David

If David deviates from the phase order mid-execution, follow his lead. His priorities override the plan.

---

## Obsidian Integration (set up after Phase 2 for testing)

Recommended plugin: `obsidian-sql-seal`. Test with:
```sql
SELECT verse_text FROM bible.verses WHERE verse_euid = 'JN-003-016';
```
If that returns "For God so loved the world..." the infrastructure works and more sophisticated queries follow.

---

## Session Kickoff (paste this into the new conversation)

> Continue the Bible data warehouse build for David Lowe (POF 2828). Read the master plan at `C:\Users\lowes\Desktop\Apologetics\tiktok_analysis\BIBLE_WAREHOUSE_MASTER_PLAN.md` — it has all scoping, priorities, and rules. Start with Phase 1 (Timeline): show me the DDL for the 11 tables, sample rows from each source, dedup decisions for the three overlapping person files, then wait for my "go" before loading. Postgres is at 192.168.1.97:5432/theophysics, password in the plan. Source folder is `C:\Users\lowes\Desktop\Bible Studies E xcel-20251109T142609Z-1-001\Bible Studies E xcel\`.

---

## Session Handoff Notes (from the 2026-04-17 scoping session)

What was delivered this session beyond this plan:
- `Hell_Full_Data_Study.md` — 1.6% Jesus hell ratio, 65% to disciples finding, John's zero, Mt 25:41 reframe, full audience breakdown. SQL schema `theophysics.hell_study` populated.
- `Hell_Attack_Taxonomy.md` — 11-move TikTok atheist attack taxonomy with Epstein counter integrated for Move 8, visceral anchor rule formalized
- `Epstein_Counter_Move8and5.md` — standalone deployable counter
- `JESUS_VOCAB_STUDY_SCOPE.md` — 6-phase scope for Jesus terminology study (enables after Phase 4 of this warehouse build)
- This plan

All saved in `C:\Users\lowes\Desktop\Apologetics\tiktok_analysis\`.

---

*Saved 2026-04-17. Phase 1 awaits green light in next session.*
