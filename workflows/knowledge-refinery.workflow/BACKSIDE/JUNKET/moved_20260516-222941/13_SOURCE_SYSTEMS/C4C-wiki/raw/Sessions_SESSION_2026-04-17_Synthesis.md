# Session Synthesis — 2026-04-17
**David Lowe / POF 2828 — Apologetics corpus + arc-reconstruction framework**

---

## What exists in the database now

`theophysics.apologetics` schema loaded to `192.168.1.97:5432`.

- **642 contradictions** with HUD codes, rationales, confidence levels
- **10 HUD categories** with essay strategies
- **5 empty tables** ready for intake: channels, videos, arguments, scripture_refs, battle_cards
- **12 empty columns** in the Master Tagged xlsx waiting to be filled per row

**Memory correction:** the axiom DB is no longer at `192.168.1.177:2665`. Everything is consolidated at `192.168.1.97:5432/theophysics`. Apologetics schema lives inside it alongside 246 other tables across 12 schemas.

---

## The shape of the attack — what the data says

### The 642 cluster at four peaks and leave four troughs

**Peaks (the load-bearing points of salvation history):**
- Genesis — 97 attacks (the foundation)
- Mosaic Law, Ex/Lev/Num/Deut — 92 attacks (the ethics)
- Samuel + Kings + Chronicles — 107 combined (parallel-history numerical variants)
- Gospels — 144 attacks (the climax)
- Matthew alone — 101 (ties Genesis; the beginning of the NT gets hit as hard as the beginning of the OT)

**Troughs:**
- Major + Minor Prophets combined — 16 attacks across 17 books
- General Epistles — 2 attacks across 8 books
- Revelation — 0 attacks
- Conquest/Judges — 21 (despite Jericho and the *herem* being TikTok favorites)

22 of the Bible's 66 books carry 85% of the attacks. The remaining 44 books carry 15%. Five of those 44 don't appear at all.

### The attack TYPE mutates to match the text TYPE

- **Law code → COVENANT attacks.** 23 of 44 total COVENANT rows (52%) live in the four Mosaic Law books. "This rule is abolished, so your book is wrong."
- **Parallel histories → SCRIBE attacks.** 53 of 115 total SCRIBE rows (46%) live in Samuel/Kings/Chronicles. Numerical variants between duplicate accounts.
- **Multi-witness narrative → VANTAGE attacks.** 40 of 53 total VANTAGE rows (75%) live in the Gospels. "The four gospels contradict each other."
- **Proverbial wisdom → STRIPPING attacks.** 23 of 32 Wisdom-literature rows (72%) are STRIPPING. Out-of-context verse pairs.

The attacker doesn't pick an attack and shop for a verse. The text form dictates which attack class is available.

### 74% of the database is procedural, not theological

- SCRIBE (115) + META (235) = 350 rows, **54%**, are copyist variants or skeptic logical fallacies
- Add in ROUNDING + AUDIENCE + DISTINCT + PHENOM + SEMANTIC = another ~125 procedural rows
- **Total procedural: ~475 of 642 (74%)**
- **Total real theological weight: ~167 rows (26%)** — these are the COVENANT, STRIPPING, VANTAGE rows that carry the "God is evil" / "Jesus contradicts himself" / "the OT is obsolete" content

### The Act 1 / Act 3 territory is almost untouched

- No attacks on Exodus 1–12 (the Egyptian bondage — Act 1 of the Mosaic Law)
- Minimal attacks on Joshua's covenant renewal (Act 3 of Sinai)
- Almost nothing on the prophets, who *criticize Israel's law-breaking from inside the text*
- Nothing on Revelation (Act 3 of the whole Bible)

**The attackers isolate Act 2.** This is the structural finding. The context that makes the middle coherent is the exact territory they don't engage with.

---

## What the framework already does

The three-act arc-reconstruction approach — what was happening before the ruling, the ruling itself, what the ruling produced or prevented — targets the precise gap in the attack surface.

The blue-dress analogy: the atheist shows Act 2 in isolation ("God said stone the girl") with Act 1 (what was actually happening — temple prostitution, Baal-Peor, child sacrifice) and Act 3 (what the ruling stopped — cultural collapse, generational sin transmission) stripped out.

**The data confirms this isn't an interpretive hunch. It's measurable.** The atheists who built the 642-corpus selected their targets by structural vulnerability. The arc reconstruction reverses that selection.

---

## What the substrate thread adds (the meta-move)

The "moral vocabulary ceiling" theory handles the CATEGORY of attack that individual arc-reconstructions can't efficiently handle one-by-one.

Key points, all already in your vault's deep-research doc:

- Lex Talionis was a **proportionality cap** on violence, not a mandate for it — historically attested as a moral upgrade from unlimited blood feud
- The linguistic substrate for concepts like "grace," "justification," "individual conscience" was built progressively — Hebrew nominalization (`-ut` suffix), Greek forensic vocabulary, Axial-age universalism
- NT ethics couldn't have been delivered at Sinai because the linguistic DAG for them wasn't complete yet
- The atheist's own moral vocabulary — the tools they use to critique the OT — was manufactured by the tradition they're critiquing

**This is the meta-argument.** Not per-row refutation. One structural move that neutralizes the entire "bronze-age morality" category at once.

---

## The 613 question and the Torah concentration

The 613 mitzvot hunch was close but no resonance — 642 vs 613 doesn't align. The Torah is 29.4% of attacks, not dominant.

But the real signal: **COVENANT attacks are 14.5× concentrated in the Torah** (15.9% of Torah attacks vs 1.1% of rest-of-Bible attacks). When atheists do the "your God is a bronze-age monster" move, they run it against Mosaic law specifically — because that's where the law IS.

Your Torah-as-separate-study is queued. The 189 Torah rows are the natural first pilot set for the arc-reconstruction template.

---

## What ties together

Two complementary moves against the same attack:

1. **Per-contradiction arc reconstruction (~100 rows)** — the 26% theological-weight subset, each row getting Act 1 + Act 2 + Act 3 + peer-era comparison. Neutralizes individual attacks decisively.
2. **Substrate meta-move (one argument)** — neutralizes the "bronze-age morality" attack category as a whole.

Together these cover:
- The moral attacks (substrate theory + arc reconstruction on COVENANT/STRIPPING)
- The witness attacks (VANTAGE arc reconstruction on Gospels)
- The textual attacks (SCRIBE dismissal via documented transmission science — already done in the database, just needs packaging)
- The logical-fallacy attacks (META — name the fallacy, move on)

The book architecture that falls out:
- **Part 1:** The substrate argument (one meta-move)
- **Part 2:** 10 atheist opening moves, one chapter per move
- **Part 3:** Worked examples — ~100 arc-reconstructed contradictions as case studies
- **Appendix A:** Nine hard cases (Num 31, Canaanite conquest, Ps 137, Jephthah, Levite concubine, Elisha bears, firstborn, Amalek, Uzzah)
- **Appendix B:** The 5 root fallacies (collapsed from 20)
- **Appendix C:** Ngram chart + peer-era comparison tables

---

## Threads parked (pick up when you want them)

1. Torah-as-separate-study — query built, ready to run deeper
2. COVENANT template build — 44 rows, smallest + cleanest pilot set for arc reconstruction
3. Schema ALTER — 15 new columns (12 from xlsx + 3 added: act_1_context, act_3_aftermath, peer_era_comparison)
4. Intelligence-substrate concept-timeline chart — visual anchor for the substrate argument
5. Ngram JSON → CSV export (waiting on the correct path on this machine)
6. STT artifact fix in xlsx SEMANTIC sheet (column A header: `Damn. Look at this Excel dude...`)
7. Memory update — NAS consolidation, apologetics schema location

---

## What the data doesn't tell us yet (honest gaps)

- The per-row Act 1 + Act 3 context is not in the database. You fill this by hand (or by targeted LLM-assisted research per row).
- Peer-era comparisons (Hammurabi, Hittite, Assyrian) aren't in the database either. Needs its own table or field.
- The ngram data isn't yet linked to the apologetics corpus — two separate evidence streams right now.
- The 177 TikTok transcripts referenced in the apologetics_db README haven't been loaded. That's the bulk intake work still waiting.

---

*Session closed with artifacts loaded, structure mapped, and the arc-reconstruction workflow ready to begin on COVENANT as pilot.*
