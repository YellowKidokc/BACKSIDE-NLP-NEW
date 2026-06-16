# TikTok Folder Organization — Claude CLI Prompt
## For use with Claude Code on O:\_Theophysics_v5\01_Tik Tok\

---

## PROMPT

You are organizing the TikTok apologetics and debate folder for David Lowe (POF 2828). This folder contains his combat doctrine, argument databases, research data, comparative religion references, and loose files accumulated over months of work.

**ABSOLUTE RULE: DO NOT DELETE ANYTHING. NOT ONE FILE. NOT ONE LINE. MOVE ONLY. If in doubt, leave it where it is.**

### PHASE 1: INVENTORY (do this first, report before proceeding)

Read every file in the folder and its subfolders. For each file, produce a one-line summary:
- Filename
- What it contains (2-5 words)
- Suggested category (see categories below)
- Quality assessment: CANONICAL (polished, load-bearing), DRAFT (has value, needs work), RAW (unprocessed dump), JUNK (empty, broken, or duplicate), UNKNOWN (can't tell without more context)

Pay special attention to:
- The 21+ "Untitled" files — read each one and figure out what it actually is
- Files named "new 1.txt", "the best.md", "good and evil.txt" — these are David's voice-to-text drops, probably contain real ideas
- The "Not Found" files in Religion/ — these are probably broken scrapes, confirm before moving
- Propaganda.txt — this is a CANONICAL Bernays dissection, do NOT treat as random

Report the full inventory and WAIT for approval before moving anything.

### PHASE 2: PROPOSED STRUCTURE

After inventory, propose this folder structure (adjust based on what you find):

```
O:\_Theophysics_v5\01_Tik Tok\
├── 00_INDEX.md                    ← master index of everything in this folder
├── 00_COMBAT_DOCTRINE/            ← the meta-strategy docs
│   ├── COMBAT_DOCTRINE.md
│   ├── ARGUMENT_STRUCTURE.md
│   ├── DEBATE_ARSENAL.md
│   └── NATHAN_METHOD.md           ← new doc to be written from tonight's session
│
├── 01_ATTACK_VECTORS/             ← what they throw at us
│   ├── TOP_20_ATTACK_VECTORS.md
│   ├── TWENTY_MOVES.md
│   └── [individual attack cards if they exist]
│
├── 02_APOLOGETIC/                 ← our arguments (the existing APO-01 through APO-20)
│   └── [keep existing structure, it's clean]
│
├── 03_THEOLOGICAL_WEAPONS/        ← standalone theological argument docs
│   ├── EVIL_IS_PARASITIC_PROOF.md
│   ├── GODS_JEALOUSY_IS_ARCHITECTURAL.md
│   ├── THREE_GATES_AND_SELF_REFUTATION.md
│   ├── PRESUPPOSITION_SIEGE_UNIFIED.md
│   ├── ROSETTA_STONE.md
│   ├── THE_CLAIMS.md
│   ├── SCIENCE_PRODUCES_MODELS_NOT_TRUTH.md
│   └── PHILOSOPHICAL_LITERACY_GATE.md
│
├── 04_BERNAYS_AND_PERSUASION/     ← propaganda analysis, Nathan Method, persuasion theory
│   ├── BERNAYS_DISSECTION.md      ← rename from Propaganda.txt
│   ├── NATHAN_METHOD_FRAMEWORK.md ← to be written
│   └── IDENTITY_CAPTURE_MECHANISM.md ← to be written
│
├── 05_RESEARCH_DATA/              ← raw research and data dumps
│   ├── Pew/                       ← keep as-is, it's reference data
│   ├── Religion/                  ← keep as-is, it's reference data
│   ├── Scientific_Method/         ← rename from "Scientific method"
│   └── Deep_Research_Prompts/     ← the DEEP_RESEARCH_PROMPT files
│
├── 06_DRAFTS_AND_FRAGMENTS/       ← the Untitled files and loose pieces
│   └── [everything that's DRAFT or RAW quality]
│
└── _ARCHIVE/                      ← broken files, empty files, true junk
    └── [Not Found files, empty Untitled files, duplicates]
```

Present the proposed structure with a file-by-file move plan. WAIT for approval before executing.

### PHASE 3: EXECUTE MOVES

After approval, execute all moves. Log every move in this format:
```
MOVED: [old path] → [new path]
```

Write the log to `00_ORGANIZATION_LOG.md` in the folder root.

### PHASE 4: BUILD THE INDEX

After all moves are complete, create `00_INDEX.md` — a master index of every file in the folder with:
- File path
- One-line description
- Category
- Quality rating
- Cross-references to related files

### CONTEXT

This folder supports David's TikTok apologetics operation — live debate rooms where atheists and Christians argue. The content ranges from formal argument cards to raw voice-to-text idea dumps to research data. The goal is to make everything findable, categorized, and ready for deployment.

**New addition from tonight's session:** David developed what we're calling the Nathan Method — a debate technique based on the prophet Nathan's confrontation of King David (2 Samuel 12). The method uses story-first engagement, lets the opponent build their own moral standard on safe ground, then reveals that their standard applies where they didn't expect. It was tested live against both Claude and GPT tonight and worked both times. The Bernays dissection (Propaganda.txt) maps the 12 mechanisms of propaganda and shows how the Nathan Method inverts each one. This is now a core component of the debate strategy alongside the existing Combat Doctrine.

**Treat Propaganda.txt as CANONICAL — it is the Bernays dissection, not a random text file. Rename it to BERNAYS_DISSECTION.md and place it in the persuasion folder.**
