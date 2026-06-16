# Fruits Spirit Canon Station

This station has two tools:

1. **Canon index** (`station.py`) — builds the canon index for Fruits of the Spirit and their equation mappings.
2. **Fruits Coherence Engine** (`fruits_coherence_engine.py`) — a domain-aware, multi-layer Fruits detector for grading papers (word → sentence → paragraph-role → paper, plus domain polarity and structural-invariant checks).

---

## 1. Canon index

```powershell
python Backside\stations\fruits-spirit-canon.station\station.py --out X:\EXPORTS\canon-index\fruits-spirit
```

Output: `canon-index.json`, `canon-index.md`. Deterministic; does not write to Postgres.

---

## 2. Fruits Coherence Engine

A traceable detector (not a truth oracle): every score traces back to a word,
sentence, paragraph role, domain polarity, and invariant warning.

### Run (wired launcher)

```powershell
RUN_FRUITS_ENGINE.bat                          :: scores everything in DROP_HERE\
RUN_FRUITS_ENGINE.bat "X:\path\to\paper.md"     :: scores one file or folder
RUN_FRUITS_ENGINE.bat --context-window 70       :: passthrough engine option
RUN_FRUITS_ENGINE.bat --lexicon "X:\x\lex.xlsx" :: force a specific lexicon
```

### Convention-driven wiring (nothing to edit when inputs/lexicons change)

| Slot | Where | Behavior |
|---|---|---|
| Input | `DROP_HERE\` (or a path arg) | `.md` / `.txt` / `.html` scanned recursively |
| Lexicon | `LEXICON\` (or station root) | newest `*.xlsx`, names containing `lexicon` preferred; falls back to the built-in lexicon |
| Output | `EXPORTS\fruits_reports\run_<timestamp>\` | always station-root `EXPORTS\` |

### Output files (per run)

- `fruits_coherence_report.json` — full report (papers, paragraphs, sentences, word trace)
- `fruits_coherence_report.md` — human summary + top/low paragraphs
- `paper_scores.csv`, `paragraph_scores.csv`, `sentence_scores.csv`, `word_trace.csv`
- `fruits_coherence_report.xlsx` — all four trace layers as sheets

### Direct engine call (no wiring)

```powershell
python fruits_coherence_engine.py paper.md --lexicon "paper_grader_lexicons_master_enhanced.xlsx" --xlsx --outdir EXPORTS\fruits_reports\manual
```

Requires `openpyxl` (installed) for `.xlsx` input/output; without it the engine still runs JSON/MD/CSV on the built-in lexicon.

