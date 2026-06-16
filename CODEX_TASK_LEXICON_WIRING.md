# CODEX TASK: Wire Claim Extractor to Master Lexicon
## POF 2828 | June 16, 2026

### Goal
Upgrade `claim-extractor.station\extract.py` to load claim signals from the master lexicon Excel instead of hardcoded keywords in config.json.

### Current state
`config.json` has 6 keyword lists with ~30 total words:
```json
"claim_signals": {
    "definition": ["defined as", "≡", ":=", "we define", "let ", "denotes"],
    "theorem": ["it follows", "therefore", "we prove", "derived from", "implies", "consequently"],
    "prediction": ["predicts", "should show", "would expect", "falsifiable", "testable", "if true then"],
    "axiom": ["we assume", "taken as given", "axiomatic", "foundational assumption", "presuppose"],
    "evidence": ["sigma", "p-value", "data shows", "experiment", "observed", "measured", "correlation"],
    "theological": ["scripture", "God", "Christ", "grace", "sin", "Holy Spirit", "salvation", "Jesus"]
}
```

### Master lexicon location
`\\dlowenas\h_hp\Desktop\Combine\paper_grader_lexicons_master_COMBINED.xlsx`

### Sheet → Category mapping
| claim_signal category | Lexicon sheets to read from |
|---|---|
| definition | CLAIM_TERMS (filter key="definition") |
| theorem | CLAIM_TERMS (filter key="theorem") |
| prediction | FALSIFY_TERMS |
| axiom | CLAIM_TERMS (filter key="axiom") |
| evidence | EVIDENCE_TERMS, F_GROUNDING |
| theological | LAW_KEYWORDS, FRUITS (value column) |
| contradiction | F_CONTRADICTION, NEGATION_TERMS, HEDGE_TERMS |
| propaganda | F_PROPAGANDA |
| jargon | F_JARGON |

### Implementation
1. Add a `load_lexicon_signals(xlsx_path)` function that reads the sheets above using openpyxl
2. The `value` column in each sheet has the actual terms
3. Fall back to config.json hardcoded signals if the Excel file is not found
4. Add `"lexicon_path"` to config.json pointing at the master lexicon
5. Log how many terms loaded per category at startup
6. Add the new categories (contradiction, propaganda, jargon) to `classification_types` in config.json

### Config.json addition
```json
"lexicon_path": "\\\\dlowenas\\h_hp\\Desktop\\Combine\\paper_grader_lexicons_master_COMBINED.xlsx",
"lexicon_fallback": true
```

### Test
Run `extract.py` on one paper. Compare claim counts before (30 keywords) and after (30,000+ keywords). The extractor should find MORE claims with better classification, not fewer.

### Location
`X:\04_STATIONS\claim-extractor.station\`
