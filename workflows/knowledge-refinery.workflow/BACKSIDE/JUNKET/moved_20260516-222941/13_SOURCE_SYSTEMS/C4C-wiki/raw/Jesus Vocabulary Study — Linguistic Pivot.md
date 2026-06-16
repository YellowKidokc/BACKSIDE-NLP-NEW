# Jesus Vocabulary Study — Architecture & Scoping
**POF 2828 | Theophysics Apologetics | 2026-04-17**
**Status: SCOPING — not yet started. Review and approve before Phase 0 launches.**

---

## The Thesis (sharpened)

**Original (David):** *"Jesus brought in significant terminology that irreversibly changed the course of history."*

**Trap in the original:** If we claim Jesus INVENTED love, grace, mercy, justice, etc., we lose the first query. Love existed (Deut 6:5, Lev 19:18, Micah 6:8). Greek ethics had virtue vocabulary (Aristotle, Stoics). Mercy existed (chesed, 248x OT). The Wikipedia version of any educated atheist will destroy the "Jesus invented virtue" framing instantly.

**Defensible version (provable, more important):** Jesus is the linguistic pivot point of moral history. Not because he invented new words, but because:

1. **He radicalized scope.** Enemy-love (Mt 5:44) has NO surviving pre-Christian parallel. Stoics had "don't return evil for evil" (neutral). Rabbis had "love your neighbor" (Lev 19:18). Jesus's positive command to LOVE your enemies is structurally unique.
2. **He loaded existing words with new semantic weight.** *Agape*, *charis*, *pistis*, *basileia*, *metanoia* all existed pre-Christian. Their semantic content after Jesus is different and more morally loaded than their semantic content before.
3. **He unified them in a coherent operator.** The Justice-Mercy Operator (R(α)) shows justice and mercy are the same function parameterized differently — a unification pre-Christian ethical systems did not achieve.
4. **He embodied them in a historical person whose cross became the linguistic pivot.** Post-cross vocabulary is recalibrated because the reference event changed. Every language Christianity touched had its moral vocabulary restructured around this event.

This is provable. And it's more important than "Jesus invented virtue."

---

## What We Have (data audit, 2026-04-17)

### On Postgres (192.168.1.97:5432/theophysics):
- `kj.verses` — KJV, 31,102 verses
- `kj.translations` — 4 additional English translations (AKJV, ASV, BBE, YLT)
- `kj.words` — 31k verse-linked words, strongs_number column EXISTS but EMPTY
- `kj.translation_words` — 3.1M word rows across translations
- `kj.people` — misses Jesus of Nazareth (only Bar-Jesus and a minor NT Jesus)
- `kj.person_verse_links` — 27k links (unclear if useful for speaker attribution)
- `public.bible_words` — correct schema (lemma + strong_number columns) but ZERO rows
- `grace_study` schema (populated, Apr 16)
- `hell_study` schema (populated, Apr 17)

### On filesystem (C:\Users\lowes\Desktop\Bible Studies E xcel-...):
- **WordIndex.csv** (73MB, 790,686 rows) — every word in English Bible with BookID/Chapter/Verse/Word + PersonID (person MENTIONED, not speaker)
- **BibleData-Person.csv** — person catalog, Jesus Christ = person_id **905**
- **BibleData-PersonVerse.csv** (2.5MB, 44k rows) — person-to-verse links
- **bsb_concordance.csv** (56MB, 741k rows) — Berean Standard Bible word concordance
- **HebrewStrongs.csv** (1.8MB) — Hebrew Strong's data with 1,210 entries
- **AlamoPolyglot.csv** (29MB) — Parallel Bible incl. Codex Alexandrinus Greek
- **Verses.csv** (16MB) — Full verse text with people mentioned

### What's missing:
- **Greek NT text with word-level Strong's tagging.** This is the central gap. Without it we cannot do real lexicographic analysis of agape, charis, pistis, etc.
- **Jesus-speaker attribution.** Must be built — either from a red-letter Bible source or by manual passage-boundary construction.
- **Pre-Christian Greek corpus counts.** For comparative claims ("agape was less common before Christianity") we need TLG-style corpus statistics. Can be sourced from scholarly literature citations rather than raw corpus.

---

## The Phased Build

### Phase 0 — Data Acquisition (estimated: 4–6 hours)

**Deliverables:**
1. Download and import **MorphGNT** (SBLGNT morphologically-tagged Greek NT, free MIT-licensed, GitHub-hosted). Result: Greek NT with lemma + morphology for every word in `public.bible_words`.
2. Build a **Jesus speech boundaries** reference table — the well-established red-letter passages for the 4 Gospels. Manually curated from standard scholarly sources (UBS Greek NT red-letter decisions + synopsis). Attribution confidence: HIGH / MIXED / INTERPRETIVE.
3. Optionally: Download and import **Open Scriptures Hebrew Bible** (also free) for OT Hebrew with Strong's. Only needed for OT comparative work.

**Output:** Greek NT loaded into `public.bible_words`. Speech boundaries table created.

---

### Phase 1 — Schema Build (estimated: 1–2 hours)

**Deliverables:**
Create `theophysics.jesus_vocab_study` schema following grace_study / hell_study pattern:
- `jesus_utterances` — every Jesus discourse with book/ch/v range, audience, setting, attribution_confidence (HIGH/MIXED/INTERPRETIVE), setting_type, total_words
- `key_concepts` — the 10–15 concepts we're testing (agape, charis, pistis, basileia, dikaiosyne, eleos, eirēnē, phōs, zōē, aiōnios, metanoia, huios, pater, sōtēria, hamartia)
- `concept_usage` — per-concept: Jesus uses, non-Jesus NT uses, LXX uses, classical pre-Christian estimate, notes
- `signature_phrases` — multi-word combinations Jesus deploys uniquely (enemy-love, love-neighbor-as-yourself applied universally, kingdom-of-God-in-your-midst, etc.)
- `semantic_shift` — documented pre-Christian vs Christian semantic loading, with citations

---

### Phase 2 — Speech Extraction & Word Frequency (estimated: 2–3 hours)

**Deliverables:**
1. Extract every Jesus utterance — KJV text and (where loaded) Greek text
2. Total word count across Jesus speech corpus — confirms the ~42,000 figure or corrects it
3. Word frequency analysis: what words does Jesus use? What's his signature vocabulary?
4. Comparison: what words does Jesus use DISPROPORTIONATELY vs. non-Jesus gospel narrative?

**Output:** `jesus_utterances` populated. Frequency tables produced. "Signature word" list identified.

---

### Phase 3 — Concept Deep-Dive (estimated: 8–12 hours — the main research)

For each of the ~12 key concepts:

| Concept | Questions answered |
|---|---|
| agape | How many times does Jesus use it? In what combinations? What was its pre-Christian weight? What weight did Jesus load into it? |
| charis | Did Jesus use it? (Hint: 0 times.) Who loaded it? What was it before? |
| pistis | Jesus's usage patterns. Pre-Christian meaning. Post-Christian "saving faith" loading. |
| basileia | How central is "kingdom of God/heaven" to Jesus's speech? Compare to pre-Christian Jewish apocalyptic. |
| dikaiosyne | Jesus's use of "righteousness." Classical Greek vs NT loading. |
| eleos | Mercy vocabulary in Jesus's speech. |
| metanoia | Classical "change of mind" vs Christian "repentance as whole-life reorientation." |
| plēsion | "Neighbor" and the Good Samaritan universalization. |
| phōs / zōē / aiōnios | "Light," "life," "eternal" as loaded concepts. |
| huios tou theou | "Son of God" — pre-Christian usage vs Christological loading. |

**Output:** `key_concepts` table populated with full semantic history per concept.

---

### Phase 4 — Signature Phrases & Unprecedented Combinations (estimated: 3–4 hours)

The single strongest claim: **specific Jesus phrases have no surviving pre-Christian parallel.**

Test cases:
- "Love your enemies, bless them that curse you" (Mt 5:44) — search TLG / pre-Christian Greek / DSS / intertestamental Jewish literature for any precedent
- "The kingdom of God is within you" (Lk 17:21)
- "Whosoever shall humble himself as this little child, the same is greatest" (Mt 18:4) — children as moral exemplars was *not* a Greek concept
- "The Sabbath was made for man, not man for the Sabbath" (Mk 2:27)
- "Blessed are the poor in spirit... the meek... those who mourn..." — the Beatitudes as inverted-status blessing structure
- "Whosoever will be great among you, let him be your servant" (Mt 20:26) — servant-leader inversion

**Method:** For each candidate phrase, document:
1. Jesus's attestation (gospel references)
2. Surviving pre-Christian precedent (if any)
3. Scholarly consensus on novelty

**Output:** `signature_phrases` populated with the strongest "Jesus-only" vocabulary candidates. This is the defensible hard claim.

---

### Phase 5 — Irreversibility Evidence (estimated: 2–3 hours)

Claim: post-Christian languages have moral vocabulary restructured around Jesus.

Evidence angles:
- *Agape* → Latin *caritas* → English *charity* — the semantic chain preserves the Christian loading
- Modern language moral terms (grace, mercy, charity, redemption, atonement) trace to Christian semantic loading
- Non-Christian philosophical systems (Kantian duty, utilitarian ethics, human rights frameworks) inherit Christian vocabulary even when they reject Christian metaphysics
- Universal Declaration of Human Rights vocabulary is structurally Christian-derived

**Output:** Brief documentation of the propagation. Not exhaustive — the goal is to ground the claim, not prove it to a skeptic linguist.

---

### Phase 6 — Paper / Output (estimated: 4–6 hours)

Draft a convergence-series paper: **"The Jesus Vocabulary Pivot: A Data Study."**

Structure (tentative):
1. What Jesus did NOT do (invent virtue terminology)
2. What Jesus DID do (4 structural moves)
3. The data — word frequencies, concept-usage patterns, signature phrases
4. The Justice-Mercy Operator as the unification proof
5. The propagation — how Christian-loaded words restructured subsequent moral vocabulary
6. What this means for the atheist claim that Christianity is "derivative"

---

## Total Estimated Effort

| Phase | Time | Can parallelize? |
|---|---|---|
| 0. Data acquisition | 4–6 hrs | Sequential |
| 1. Schema build | 1–2 hrs | Sequential |
| 2. Speech extraction + word freq | 2–3 hrs | Sequential |
| 3. Concept deep-dive | 8–12 hrs | YES — can split concepts across sessions |
| 4. Signature phrases | 3–4 hrs | Parallel to Phase 3 |
| 5. Irreversibility | 2–3 hrs | Can come later |
| 6. Paper | 4–6 hrs | Sequential |
| **Total** | **25–36 hrs** | — |

Over 3 focused days (8–12 hrs/day): achievable.
Over 5–7 normal days: comfortable.

---

## Honesty Notes (before we commit)

1. **Greek text quality depends on source.** MorphGNT uses SBLGNT (Society of Biblical Literature Greek NT, 2010). This is one modern critical text. Nestle-Aland 28th edition is another. They differ in a small number of verses. The conclusions don't depend on which we use, but a hostile scholar could quibble with text-choice.

2. **Jesus spoke Aramaic, not Greek.** The gospels are Greek translations. So when we say "Jesus used agape," we mean "the gospel writers chose agape to translate what Jesus said in Aramaic." The terminology pivot is at the gospel-writer layer, not necessarily Jesus's original Aramaic speech. This doesn't weaken the thesis — the Greek is what propagated — but it's an honesty caveat that matters for academic rigor.

3. **Red-letter tagging varies by edition.** Different publishers disagree on where Jesus's speech ends and narrator commentary begins in John. We'll tag each utterance with attribution confidence (HIGH / MIXED / INTERPRETIVE) so the core findings rest on the unambiguous red-letter core, not on disputed passages.

4. **"No pre-Christian parallel" is stronger than we can strictly prove.** To prove "no surviving pre-Christian parallel for enemy-love" we'd have to search the entire TLG (Thesaurus Linguae Graecae) and every surviving Aramaic/Hebrew source. We can cite scholarly consensus instead — scholars working on this question for 200 years have not produced a direct parallel. That's strong but not absolute. Fair for the paper, strong enough for TikTok.

---

## Recommended Starting Point

**Phase 0 — data acquisition.**

Specifically:
1. Download MorphGNT (Greek NT with lemma + morphology, SBLGNT text)
2. Load into `public.bible_words`
3. Verify: can I query agape? charis? pistis? Find every occurrence in NT.

Once that's done and verified, Phase 1 (schema) and Phase 2 (speech extraction) come fast.

---

## Questions Before I Start

1. **Do you want the Greek NT?** If no, we can do the English-level study + lexical references only. This saves Phase 0 entirely but limits us to "we know from scholarship that agape had this weight" rather than "here's every agape verse with morphology."

2. **Scope the concept list.** My default: agape, charis, pistis, basileia, dikaiosyne, eleos, eirēnē, phōs, zōē, aiōnios, metanoia, plēsion. Add/remove?

3. **Do you want the Hebrew OT too?** Adds ~2 hours acquisition, mostly not needed for the NT-focused Jesus-vocab thesis but useful for showing "Jesus recalibrated concepts that existed in OT Hebrew."

4. **Deployment target.** Paper for the Convergence series? TikTok battle cards derived from the data? Both? This affects how I write up.

5. **Is `/_Theophysics_v4/` accessible from this session?** O:\ isn't in my allowed paths. If you want artifacts landing in the vault directly, we need to adjust.

---

*Ready to start. Waiting for green light + any adjustments above.*
