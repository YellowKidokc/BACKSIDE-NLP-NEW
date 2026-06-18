# SESSION HANDOFF — 2026-06-17 (Opus)

**For:** next session (Opus / Codex / Kimi / Jim) · **Status:** rigor card located; NLP service green; chain-mode pending

---

## ✅ RESOLVED THIS SESSION

### 1. The "rigor card" — FOUND (this was the hunt)
David was looking for an HTML built ~last month that takes the MDA series
from "quaint statistic" → "no offense, prove me wrong." Named "rigor card"
*after* the fact, so it does NOT contain the string "rigor card." It's on disk.

**Primary file:**
`D:\GitHub\faiththruphysics-site\moral-decline\02-method-and-metrics\MDA-038-coherence-metric.html`  (dated 2026-06-04)
- §3.3 **Curve-Fitting** + source badges tagging the claim honestly as
  "Curve Fitting | Preliminary — R²=0.87" (owns the quaint version up front)
- §6 **Falsification Tests** w/ **Kill Condition** table (R²<0.70 kills it) = the "prove me wrong"

**Supporting files (same root):**
- `...\05-amish-and-case-studies\MDA-049-coherence-factory-THE-SYNTHESIS.html`
  → line ~641: *"Each rule, taken alone, looks quaint. Together they form a multi-layered membrane."*
- `...\90-appendices-and-source-packets\MDA-902-appendix-trans-domain-analysis.html`
  → Methodology & Kill Conditions / Curve Fitting / analogy-vs-isomorphism defense

**Canonical folder = `moral-decline\`** (NOT the older `mda\` tree — near-dupes).

### 2. NLP FastAPI service — repaired & committed (58f240c)
4 stacked blockers fixed in `nlp_api\main.py` (transformers 5.5.4 task aliases,
numpy serialization, NAS-mmap hang → run from LOCAL `D:\nlp_models`, wrong 3.12
interpreter). All 5 endpoints pass over HTTP. Service runs under
`C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe` via `nlp_api\RUN.bat`.

### 3. Weekly model backup — registered
Task **"POF2828 Weekly Model Backup"**, Sundays 03:00 →
`backup_models.ps1` mirrors `D:\nlp_models` → `\\192.168.2.50\brain\13_ARCHIVE\nlp_models`.

---

## ▶ NEXT (ranked)

1. **Populate the rigor card so it RENDERS.** The block exists in MDA-038 but the
   Ring 1/2/3 panel says "No connections mapped yet" and the rigor slot is data-empty.
   This is a *data-population* job, not missing content. Pull from the §6 Falsification
   /Kill-Condition table already in the file. Surgical edit → goes up on next launch.
2. **NLP station CHAIN-MODE smoke test.** Core 8 is a chain, not parallel. Wire
   `smoke_test.py` to run extract → classify → load-bearing → falsify → evidence →
   contradiction, feeding each station the prior `.json` artifact. (2/8 pass today
   = correct; 5 are downstream, 1 needs a generative endpoint.)
3. **Build the generative/register endpoint** for the plain-language station (404 now).

---

## ⚠ GOTCHAS (do not relearn)
- Inline PowerShell via start_process **strips `$` vars** and chokes on `&`/nested quotes.
  ALWAYS write a `.ps1`/`.py` to disk and run it. (This session's find scripts: `D:\nlp_models\_find_rigor*.ps1`)
- Models load from **`D:\nlp_models`** (local), NOT the NAS — mmap over SMB hangs. X: IS the NAS.
- Service interpreter is **3.12**, not 3.14 (3.14 lacks transformers).

## KEY PATHS
- NLP repo: `D:\GitHub\BACKSIDE-NLP-NEW\`  (branch OBS-Plugin-Final-Claude)
- Stations: `D:\GitHub\BACKSIDE-NLP-NEW\stations\*.station\` · registry `STATION_REGISTRY.json`
- MDA canonical: `D:\GitHub\faiththruphysics-site\moral-decline\`
- Local model cache: `D:\nlp_models` (regenerable: `python nlp_api\stage_models.py`)
