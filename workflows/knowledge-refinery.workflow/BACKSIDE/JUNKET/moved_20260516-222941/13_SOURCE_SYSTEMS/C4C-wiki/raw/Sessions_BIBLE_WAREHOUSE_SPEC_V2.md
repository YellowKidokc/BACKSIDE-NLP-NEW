# Bible Warehouse Master Spec
**POF 2828 | 2026-04-17**
**Target:** `bible.*` schema in `theophysics` PG on 192.168.1.97:5432
**Source folder:** `C:\Users\lowes\Desktop\Bible Studies E xcel-20251109T142609Z-1-001\Bible Studies E xcel\`

This supersedes `BIBLE_WAREHOUSE_MASTER_PLAN.md`. That plan had wrong row counts, missed files, and flattened multi-source structure. This spec is built from the actual 65-file census (see `_full_census.md`).

---

## 1. EUID grammar (LOCKED)

One rule: **dashes between components, underscores inside components, prefix for anything that isn't a verse.**

### Verse reference (the spine)
| Level | Pattern | Example | Meaning |
|---|---|---|---|
| Book | `BK-<code>` | `BK-GN` | Genesis |
| Chapter | `<code>-<ccc>` | `GN-001` | Genesis 1 |
| Verse | `<code>-<ccc>-<vvv>` | `GN-001-001` | Gen 1:1 |
| Word | `<code>-<ccc>-<vvv>-W<wwww>` | `GN-001-001-W0003` | 3rd word of Gen 1:1 |
| Pericope | `PER-<code>-<ccc>-<nn>` | `PER-MT-006-01` | Lord's Prayer |

Book codes: 2-letter, match existing `kj.book_codes` (GN, EX, LV, ..., MT, MK, LK, JN, ...).
Zero-padded: chapter 3 digits (max 150 in Psalms), verse 3 digits (max 176 in Ps 119), word 4 digits (longest verse ~90 words). Verified safe — no overflow anywhere in scripture.

### Content objects (attached to verses via attach_level)
| Type | Prefix | Example | Source |
|---|---|---|---|
| Person | `PPL-<slug>` | `PPL-jesus_905` | People.csv |
| Place | `PLC-<slug>` | `PLC-eden_354` | Places.csv |
| People Group | `GRP-<slug>` | `GRP-tribe_of_levi` | PeopleGroups.csv |
| Event | `EVT-<slug>` | `EVT-the_creation` | Events.csv |
| Epoch | `EPO-<slug>` | `EPO-life_adam_1` | BibleData-Epoch.csv |
| Period | `PRD-<year>` | `PRD-N4004` | Periods.csv (N=BC) |
| Commandment | `CMD-<nnn>` | `CMD-001` | BibleData-Commandments.csv |
| Prophecy | `PRP-<nnnn>` | `PRP-0001` | Bible prophecies full.csv |
| Strong's Hebrew | `STR-H<nnnn>` | `STR-H0430` | HebrewStrongs.csv |
| Strong's Greek | `STR-G<nnnn>` | `STR-G2316` | from bsb_interlinear |
| Cross-reference | `XRF-<from>-<nnn>` | `XRF-GN-001-001-001` | bsb_interlinear |
| Commentary | `CMT-<source>-<attach>` | `CMT-MACARTHUR-GN-001-001` | macarthur_complete_bible.xlsx |
| Dictionary entry | `DCT-<source>-<slug>` | `DCT-EASTON-aaron` | Tagging_Master Easton_Backend |
| Bible name | `NAM-<slug>` | `NAM-abraham` | Bible Names.csv |
| Tag (user) | `TAG-<category>-<slug>` | `TAG-EMOTION-fear` | Tagging_Master empty sheets |

### Attach-level convention (the big unlock)
Every "attached" table has:
```sql
attach_level  TEXT  -- 'book' | 'chapter' | 'verse' | 'word' | 'pericope' | 'epoch' | 'period'
attach_euid   TEXT  -- points at the level (e.g., 'GN-001-001' for verse, 'BK-GN' for book)
```
One query pattern returns everything attached to any level:
```sql
SELECT * FROM bible.commentary WHERE attach_euid = 'GN-001-001';
SELECT * FROM bible.person_verses WHERE attach_euid = 'GN-001-001';
-- Or for entire chapter context:
SELECT * FROM bible.commentary WHERE attach_euid LIKE 'GN-001-%' OR attach_euid = 'GN-001';
```

---

## 2. Prefix registry (will become `bible.euid_prefixes` table)

Every future prefix must be added here first before it can be used anywhere. Prevents namespace drift across sessions.

```
BK, PER, PPL, PLC, GRP, EVT, EPO, PRD, CMD, PRP,
STR, XRF, CMT, DCT, NAM, TAG
```

---

## 3. Testament handling

Testament is NOT in the EUID. It's a column on `bible.books`:
```sql
bible.books (
  book_euid  TEXT PRIMARY KEY,  -- 'BK-GN'
  book_code  TEXT,              -- 'GN'
  testament  TEXT,              -- 'OT' | 'NT'
  ...
)
```

---

## 4. Complete file → table mapping

### Load-priority order (David's priorities + technical dependencies)
1. **Spine** (required for all EUIDs) — books, chapters, verses
2. **Timeline / Chronology** (David's #1 priority) — periods, epochs, events, timeline narrative
3. **MacArthur commentary** (David's #2 priority) — commentary_macarthur
4. **People / Places / Groups** — persons, places, people_groups + label tables + verse linkages
5. **Translations** — 14 translation texts via bibles.xlsx (faster than per-file)
6. **Original languages** — bsb_interlinear, strongs (Hebrew + Greek), AlamoPolyglot
7. **Reference / Dictionaries** — references, Bible Names, Hitchcock, Easton
8. **Concordance + indices** (largest loads) — bsb_concordance, bsb_topical_index, word_index, words_en
9. **Special content** — commandments, prophecies, Matthew Henry commentary
10. **User tag scaffolds** — empty sheets from Tagging_Master ready for fill

### Master file map

| # | Source file | Sheet | Target table | Rows | EUID namespace | Attach level | Notes |
|---|---|---|---|---:|---|---|---|
| **SPINE** | | | | | | | |
| 1 | `Books.csv` + `BibleData-Book.csv` (merge) | — | `bible.books` | 66 | BK | self | Merge by book_code. BibleData-Book has Hebrew/Greek names; Books.csv has osisName + testament |
| 2 | `Chapters.csv` | — | `bible.chapters` | 1,189 | `<code>-<ccc>` | self | writer, verse list |
| 3 | `Verses.csv` | — | `bible.verses` | 31,102 | `<code>-<ccc>-<vvv>` | self | Canonical verse table |
| **TIMELINE** | | | | | | | |
| 4 | `Periods.csv` | — | `bible.periods` | 250 | `PRD-<year>` | self | Year ↔ events/births/deaths |
| 5 | `BibleData-Epoch.csv` | — | `bible.epochs` | 159 (real) | `EPO-<slug>` | self | Trim 840 empty padding rows |
| 6 | `Events.csv` | — | `bible.events` | 395 | `EVT-<slug>` | self | **Use this, not BibleData-Event.csv** — richer (verses, people, places, locations, predecessor chain) |
| 7 | `BibleData-Event.csv` | — | — | 210 | — | — | **SKIP** — subset of Events.csv with padding |
| 8 | `Bbile TGimeline .xlsx` | `Bible Timeline` | `bible.timeline_narrative` | 585 | `TLN-<nnnn>` | period OR verse | Narrative timeline text blocks |
| 9 | `Bible Timeline.csv` | — | — | broken | — | — | **SKIP** — use XLSX above |
| **COMMENTARY** | | | | | | | |
| 10 | `macarthur_complete_bible.xlsx` | `macarthur_complete_bible` | `bible.commentary` (source='MACARTHUR') | 42,485 | `CMT-MACARTHUR-<attach_euid>` | verse | **Authoritative** — rich cols, multiple per verse |
| 11 | `KJV_with_MacArthur_Commentary.xlsx` | — | — | 31,172 | — | — | **SKIP** — subset of above |
| 12 | `MacArthur_Commentary_Only.xlsx` | — | — | 31,172 | — | — | **SKIP** — subset of above |
| 13 | `matthew_henry_enhanced.xlsx` | `Sheet1` | `bible.commentary` (source='MATTHEW_HENRY') | 9,523 | `CMT-MATTHEW_HENRY-<attach>` | verse OR chapter | |
| 14 | `KJV_with_Matthew_Henry_Smart_Mapping.xlsx` | — | — | 31,102 | — | — | **SKIP** — redundant |
| **PEOPLE / PLACES / GROUPS** | | | | | | | |
| 15 | `People.csv` | — | `bible.persons` | 3,069 | `PPL-<slug>` | self | **Authoritative** — 36 rich cols (jesus_905 is here) |
| 16 | `BibleData-Person.csv` | — | — | 3,009 | — | — | **SKIP** — lean subset; People.csv is superset |
| 17 | `Bible_Tagging_Master_Workbook.csv` | — | — | 3,069 | — | — | **SKIP** — dupe of People.csv |
| 18 | `BibleData-PersonLabel.csv` | — | `bible.person_labels` | 3,749 | `PLB-<nnnnn>` | verse | How a person is *called* in each verse (Hebrew/Greek/English) |
| 19 | `BibleData-PersonRelationship.csv` | — | `bible.person_relationships` | 5,450 | `PRL-<nnnnn>` | person | 2-person relationships |
| 20 | `BibleData-PersonVerse.csv` | — | `bible.person_verses` (source='general') | 44,267 | `PPV-<nnnnn>` | verse | |
| 21 | `BibleData-PersonVerseApostolic.csv` | — | `bible.person_verses` (source='apostolic') | 9,751 | `PPV-<nnnnn>` | verse | |
| 22 | `BibleData-PersonVerseTanakh.csv` | — | `bible.person_verses` (source='tanakh') | 34,516 | `PPV-<nnnnn>` | verse | Total: 88,534 |
| 23 | `Places.csv` | — | `bible.places` | 1,274 | `PLC-<slug>` | self | **Authoritative** — 38 cols |
| 24 | `BibleData-Place.csv` | — | `bible.places_detail` | 118 | — | place | Supplementary: OpenBible IDs. Join to Places.csv |
| 25 | `BibleData-PlaceLabel.csv` | — | `bible.place_labels` | 141 | `PLL-<nnn>` | verse | |
| 26 | `BibleData-PlaceVerse.csv` | — | `bible.place_verses` | 2,091 | `PLV-<nnnnn>` | verse | |
| 27 | `PeopleGroups.csv` | — | `bible.people_groups` | 20 | `GRP-<slug>` | self | Tribes, nations |
| **TRANSLATIONS** | | | | | | | |
| 28 | `bibles.xlsx` | `Sheet1` | `bible.translation_verses` | 31,102 × 14 ≈ 435k | — | verse | 14 translations in one workbook — BSB, KJV, ASV, AKJV, CPDV, DBT + 8 more |
| 29 | `KJV.xlsx`, `ASV.csv`, `LEB.csv`, `BBE.csv`, individual translation files | — | — | 31,102 ea | — | — | **SKIP** — subsumed by bibles.xlsx if BSB/KJV/etc. confirmed present; otherwise fill gaps from these |
| **ORIGINAL LANGUAGES** | | | | | | | |
| 30 | `bsb_tables.xlsx` | `biblosinterlinear96` | `bible.bsb_interlinear` | ~754,649 | `<verse>-W<wwww>` | word | **Core** for Jesus Vocab Study — Heb/Grk with Strong's + morphology + BSB English |
| 31 | `AlamoPolyglot.csv` | — | `bible.alamo_polyglot` | 31,102 | — | verse | Parallel Heb/Grk/Eng/Aramaic per verse |
| 32 | `HebrewStrongs.csv` | — | `bible.strongs_hebrew` | 8,674 | `STR-H<nnnn>` | self | Unique Hebrew Strong's (not per-occurrence) |
| 33 | (derived from bsb_interlinear) | — | `bible.strongs_greek` | ~5,600 | `STR-G<nnnn>` | self | Extract unique Greek Strong's during Phase 6 |
| **REFERENCE / DICTIONARIES** | | | | | | | |
| 34 | `BibleData-Reference.csv` | — | `bible.refs` | 31,102 | — | verse | Verse_id lookup (legacy compat) |
| 35 | `Bible Names.csv` | — | `bible.bible_names` | 2,624 | `NAM-<slug>` | self | Broken headers — repair on load |
| 36 | `HitchcocksBibleNamesDictionary.csv` | — | `bible.hitchcocks_names` | 2,623 | `DCT-HITCHCOCK-<slug>` | self | |
| 37 | `Bible_Tagging_Master_Workbook.xlsx` | `Easton_Backend` | `bible.easton_dictionary` | 6,519 | `DCT-EASTON-<slug>` | self OR verse | **NEW — not in old plan.** Easton's Bible Dictionary |
| **CONCORDANCE / INDICES** | | | | | | | |
| 38 | `bsb_concordance.xlsx` | `Sheet1` | `bible.bsb_concordance` | ~741,527 | — | verse | Streaming load required |
| 39 | `bsb_topical_index.xlsx` | `bsb_topical_index` | `bible.bsb_topical_index` | 163,836 | — | verse | Use XLSX — CSV has voice-to-text artifact header |
| 40 | `WordIndex.csv` | — | `bible.word_index_kjv` | 790,685 | — | word | Streaming load |
| 41 | `words_en.csv` | — | `bible.words_en` | 9,823 | `WEN-<word>` | self | English word frequency (word, count, word_type) |
| **SPECIAL CONTENT** | | | | | | | |
| 42 | `BibleData-Commandments.csv` | — | `bible.commandments` | 613 | `CMD-<nnn>` | verse | |
| 43 | `Bible prophecies full.csv` | — | `bible.prophecies` | 2,982 | `PRP-<nnnn>` | verse | Broken headers — repair on load |
| **USER TAG SCAFFOLDS** (from Tagging_Master — sheets are empty, schema only) | | | | | | | |
| 44 | Tagging_Master `Emotions` | — | `bible.tag_emotions` | 0 | `TAG-EMOTION-<slug>` | verse | Ready for fill |
| 45 | Tagging_Master `TheologicalThemes` | — | `bible.tag_themes` | 0 | `TAG-THEME-<slug>` | verse | Ready for fill |
| 46 | Tagging_Master `Topics` | — | `bible.tag_topics` | 0 | `TAG-TOPIC-<slug>` | verse | Ready for fill |
| 47 | Tagging_Master `Objects` | — | `bible.tag_objects` | 0 | `TAG-OBJECT-<slug>` | verse | Ready for fill |
| 48 | Tagging_Master `Concepts` | — | `bible.tag_concepts` | 0 | `TAG-CONCEPT-<slug>` | verse | Ready for fill |

### Files NOT loaded into `bible.*`

| File | Reason |
|---|---|
| `ArXiv_old.csv` (21 MB, 27k rows) | Research papers, not Bible data |
| `Arguments_For_Against_God.xlsx` | Apologetics — belongs in `apologetics.*` schema |
| `Conversion_Flow_Workbook.xlsx` | Apologetics — belongs in `apologetics.*` schema |
| Duplicates: `kjv (1).xlsx`, `wbt (1).xlsx`, `KJV_with_MacArthur_Commentary (2).xlsx`, `BibleData-Event.csv` | Exact or near duplicates of kept files |
| `bsb_concordance.csv`, `bsb_topical_index.csv`, `Bible_Tagging_Master_Workbook.csv` | XLSX versions are cleaner (CSVs have corrupted headers) |

---

## 5. What this enables

One verse EUID reaches everything:
```sql
-- Get everything about Gen 1:1
WITH target AS (SELECT 'GN-001-001'::text AS euid)
SELECT 'verse'       AS layer, v.verse_text::text AS content FROM bible.verses v, target WHERE v.verse_euid = target.euid
UNION ALL
SELECT 'macarthur',  c.commentary FROM bible.commentary c, target WHERE c.attach_euid = target.euid AND c.source = 'MACARTHUR'
UNION ALL
SELECT 'person',     p.person_name FROM bible.person_verses pv JOIN bible.persons p ON pv.person_id = p.person_id, target WHERE pv.attach_euid = target.euid
UNION ALL
SELECT 'place',      pl.place_name FROM bible.place_verses plv JOIN bible.places pl ON plv.place_id = pl.place_id, target WHERE plv.attach_euid = target.euid
UNION ALL
SELECT 'event',      e.event_label FROM bible.events e, target WHERE target.euid = ANY(e.verse_euids)
UNION ALL
SELECT 'easton',     ed.dict_text FROM bible.easton_dictionary ed, target WHERE ed.attach_euid = target.euid;
```

Obsidian click-to-expand calls that one query. Settings toggle what layers it includes.

---

## 6. Open decisions before DDL

1. **Merge `Books.csv` into `BibleData-Book.csv`** — both exist, Books.csv has testament/osisName, BibleData-Book has Hebrew/Greek names. Merge on load — agree?
2. **MacArthur dedup** — `macarthur_complete_bible.xlsx` has 42,485 rows (11k more than 31,102 verses). Multiple entries per verse. Load all as one table with sequence column — agree?
3. **Translation strategy** — Load `bibles.xlsx` (one workbook, 14 translations) OR load each `.xlsx` file separately? Need to peek at bibles.xlsx to see if it has all 14 or just a subset. Next step.
4. **Tag scaffold sheets** — Create the 5 empty tables (`tag_emotions`, `tag_themes`, etc.) now so they're ready for your fill later — agree?

---

*This spec is the source of truth. Edit here, loader reads from here.*
