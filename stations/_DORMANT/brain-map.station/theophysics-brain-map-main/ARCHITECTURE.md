# X:\ Brain — Architecture Map

**Owner:** David Lowe (POF 2828)
**Last updated:** 2026-05-16 by claude-code-forge
**Plan:** `C:\Users\lowes\.claude\plans\yes-i-want-togo-agile-puddle.md`

This is the live map of the X:\ brain. It mixes **current state (2026-05-16)** with **target state (post-Phase-4)** — each diagram labels which it shows.

X:\ is the NAS share `\\dlowenas\brain\` mounted as a drive. When this doc says "the brain," that's X:\ root.

## 0. 2026-05-20 root target

David's revised cleanup rule is that the root is a front door, not the runtime shelf.

```text
X:\
  David\        human-facing notes and session entrypoints
  GUI\          dashboards and control panels
  Conversions\  active conversion front door
  EXPORTS\      final reproducible HTML / Excel / metadata packages
  Backside\     workflows, models, services, stations, control plane, state, archives
```

Root workflow folders such as `knowledge-refinery`, `paper-proof-grader`, `session-handoff-drop`, `models`, `ollama`, and `Preference Engine Build` are transitional until migrated according to `ROOT_REORG_TARGET_2026-05-20.md`.

---

## 1. System overview — what lives on X:\

**Current shape (after Phase 1 consolidation).** Five zones.

```mermaid
flowchart TB
    classDef front fill:#e7f5ff,stroke:#1971c2,color:#000
    classDef work fill:#ffe8cc,stroke:#d9480f,color:#000
    classDef know fill:#fff4e6,stroke:#e67700,color:#000
    classDef pipe fill:#c5f6fa,stroke:#0c8599,color:#000
    classDef back fill:#e5dbff,stroke:#5f3dc4,color:#000
    classDef sys fill:#f8f9fa,stroke:#868e96,color:#000

    Root[("X:\ root")]:::front

    subgraph frontspace["FRONTSPACE — what David sees"]
        David["David\<br/>maps & notes"]:::front
        Readme["README.md<br/>signpost"]:::front
        Runs["RUN_*.bat<br/>click-buttons"]:::front
    end

    subgraph workflows["WORKFLOWS — the 9 NLPs"]
        KR[knowledge-refinery]:::work
        PPG[paper-proof-grader]:::work
        AX[axioms]:::work
        LPD[link-pull-drop]:::work
        SHD[session-handoff-drop]:::work
        OL[ollama]:::work
        APG[ai-portal-generator]:::work
        PA[proof-architecture]:::work
        PE[proof-explorer]:::work
    end

    subgraph knowledge["KNOWLEDGE — vault content"]
        C4C[C4C<br/>Case-for-Christ vault<br/>2497 files]:::know
        C4CW[C4C-wiki]:::know
        FAP[FAP<br/>article pipeline scaffold]:::know
    end

    subgraph pipeline["PIPELINE — shared data"]
        Captures[captures]:::pipe
        Digests[digests]:::pipe
        Embeddings[embeddings]:::pipe
        Models[models]:::pipe
        Ratings[ratings]:::pipe
    end

    subgraph backside["BACKSIDE — automation & infra"]
        Back[Backside<br/>scripts, archives, logs]:::back
        Logs["_LOGS"]:::back
        Github[github]:::back
        BIL[BIL<br/>placeholder]:::back
        WF00["00_WORKFLOWS<br/>healthcheck, map"]:::back
    end

    Recycle["#recycle<br/>system"]:::sys
    Deprecated["_brain_DEPRECATED<br/>empty marker"]:::sys

    Root --> frontspace
    Root --> workflows
    Root --> knowledge
    Root --> pipeline
    Root --> backside
    Root --> Recycle
    Root --> Deprecated
```

---

## 2. Drop-to-output lifecycle — what happens to a file

**Target state (Phase 4 intake engine in place).** This is the end-to-end journey of a single dropped file.

```mermaid
flowchart LR
    classDef user fill:#d3f9d8,stroke:#2f9e44,color:#000
    classDef gate fill:#e7f5ff,stroke:#1971c2,color:#000
    classDef ai fill:#e5dbff,stroke:#5f3dc4,color:#000
    classDef work fill:#ffe8cc,stroke:#d9480f,color:#000
    classDef store fill:#fff4e6,stroke:#e67700,color:#000

    User((David))-->|paste / drop|MasterDrop
    MasterDrop["X:\DROP_HERE<br/>(master front door)"]:::gate
    MasterDrop --> Engine
    Engine["Backside\intake_engine.py<br/>watcher + classifier"]:::ai
    Engine -->|"file type?"|Decision{Mistral<br/>classify}:::ai
    Decision -->|PAPER|PPGdrop["paper-proof-grader\00_DROP"]:::work
    Decision -->|LINK|LPDdrop["link-pull-drop\00_DROP"]:::work
    Decision -->|SESSION|SHDdrop["session-handoff-drop\00_DROP"]:::work
    Decision -->|AXIOM|AXdrop["axioms\00_DROP"]:::work
    Decision -->|GENERAL|KRdrop["knowledge-refinery\00_DROP"]:::work

    PPGdrop --> NLPRun
    LPDdrop --> NLPRun
    SHDdrop --> NLPRun
    AXdrop --> NLPRun
    KRdrop --> NLPRun

    NLPRun["NLP\RUN.bat<br/>process file"]:::work
    NLPRun --> Output["NLP\OUTPUT"]:::work
    NLPRun --> SharedData

    SharedData["Pipeline layer:<br/>digests, embeddings,<br/>captures"]:::store
    SharedData --> Qdrant["Qdrant @<br/>192.168.1.177:6333<br/>vector store"]:::store
    SharedData --> AIChats["O:\Vault\AI Chats<br/>human-readable"]:::store
```

---

## 3. Backside intake engine — the layer "in between"

This is the bit that lives **between** "David drops a file" and "the NLP runs." Today: doesn't exist (everything is manual `.bat` clicks). Target state shown.

```mermaid
sequenceDiagram
    autonumber
    participant U as David
    participant FS as X:\DROP_HERE
    participant W as intake_engine.py<br/>(watchdog)
    participant M as Ollama Mistral<br/>localhost:11434
    participant NLP as NLP\00_DROP
    participant R as NLP\RUN.bat
    participant Q as Qdrant<br/>192.168.1.177:6333

    U->>FS: drop file (paste / copy)
    W->>FS: filesystem event fires
    W->>W: read first 500 chars + filename
    W->>M: classify (PAPER / LINK / SESSION / AXIOM / GENERAL)
    M-->>W: one-word answer
    W->>NLP: move file to matching NLP
    W->>W: debounce 30s (allow multi-file paste)
    W->>R: launch RUN.bat
    R->>R: extract / embed / score
    R->>Q: upsert vectors
    R-->>U: output ready
    W->>W: log to X:\_LOGS\intake_engine_*.log
```

**Key properties:**
- One watcher per NLP `00_DROP/` plus one for the master `X:\DROP_HERE\`
- Master-drop classification uses local Ollama Mistral (no cloud)
- Per-NLP drops skip classification and trigger that NLP's RUN directly
- 30-second debounce so a multi-file paste fires one run, not five
- Restart-safe: on boot, sweeps all drop folders for backlog

---

## 4. Per-NLP standard shape — the front door

**Target state (Appendix A of plan).** Every NLP folder follows this shape so new AIs / humans never have to guess.

```mermaid
flowchart LR
    classDef drop fill:#d3f9d8,stroke:#2f9e44,color:#000
    classDef run fill:#ffe8cc,stroke:#d9480f,color:#000
    classDef proc fill:#e5dbff,stroke:#5f3dc4,color:#000
    classDef out fill:#c5f6fa,stroke:#0c8599,color:#000
    classDef meta fill:#e7f5ff,stroke:#1971c2,color:#000

    Drop["00_DROP<br/>(intake)"]:::drop
    Run["RUN.bat<br/>(click button)"]:::run
    Cfg["config.json"]:::meta
    Readme["README.md<br/>WHAT/DROP/RUN/OUTPUT/OWNER"]:::meta
    Logic["pipeline.py<br/>(NLP-specific)"]:::proc
    Out["OUTPUT"]:::out
    Arch["ARCHIVE"]:::out

    Drop --> Run
    Cfg --> Run
    Run --> Logic
    Logic --> Out
    Logic --> Arch
    Readme -.-> Drop
    Readme -.-> Run
    Readme -.-> Out
```

Every NLP gets the same 5-line README contract:

```
WHAT: <one sentence>
DROP HERE: ./00_DROP/
RUN: ./RUN.bat
OUTPUT: <path>
OWNER: <AI partner>
```

---

## 5. The 9 NLPs — what each one is for

**Current state.** Two have full automation, four have basic pipelines, three are publishing endpoints.

```mermaid
flowchart TB
    classDef full fill:#d3f9d8,stroke:#2f9e44,color:#000
    classDef basic fill:#ffe8cc,stroke:#d9480f,color:#000
    classDef pub fill:#e7f5ff,stroke:#1971c2,color:#000
    classDef hub fill:#e5dbff,stroke:#5f3dc4,color:#000

    Hub((NLP catalog)):::hub

    KR[knowledge-refinery<br/>13-stage refinery<br/>00_INTAKE → 13_SOURCE_SYSTEMS]:::full
    AX[axioms<br/>00→06 stages<br/>INBOX → RIGOR_GATES]:::full

    PPG[paper-proof-grader<br/>DeBERTa + claims + scoring<br/>OUTPUT to JSON/MD/Excel]:::basic
    LPD[link-pull-drop<br/>YouTube transcripts<br/>+ web fetch]:::basic
    SHD[session-handoff-drop<br/>Ollama Mistral<br/>session summarizer]:::basic
    OL[ollama<br/>Mistral handoff scripts<br/>shared model layer]:::basic

    APG[ai-portal-generator<br/>builds AI-facing HTML]:::pub
    PA[proof-architecture<br/>static HTML/MD]:::pub
    PE[proof-explorer<br/>static HTML/MD]:::pub

    Hub --> KR
    Hub --> AX
    Hub --> PPG
    Hub --> LPD
    Hub --> SHD
    Hub --> OL
    Hub --> APG
    Hub --> PA
    Hub --> PE
```

**Legend:**
- **Green (full):** structured multi-stage pipeline, can run end-to-end today.
- **Orange (basic):** working pipeline.py, single RUN.bat, no stage architecture.
- **Blue (publishing):** static output zone, no intake — content lands here from upstream.

---

## 6. knowledge-refinery — the most structured NLP

The 13-stage refinery is the template the others *could* converge to. Each stage is a numbered folder.

```mermaid
flowchart LR
    classDef stage fill:#d3f9d8,stroke:#2f9e44,color:#000
    classDef config fill:#fff4e6,stroke:#e67700,color:#000

    S00[00_INTAKE]:::stage --> S01[01_CONVERSION]:::stage
    S01 --> S02[02_NORMALIZATION]:::stage
    S02 --> S03[03_ROUTING]:::stage
    S03 --> S04[04_MODEL_STATIONS]:::stage
    S04 --> S05[05_WORKFLOW_RUNS]:::stage
    S05 --> S06[06_HTML_REPORTS]:::stage
    S06 --> S07[07_OBSIDIAN_EXPORT]:::stage
    S07 --> S08[08_ARCHIVE]:::stage

    S10[10_PROMPTS]:::config -.-> S04
    S11[11_CONFIG]:::config -.-> S00
    S12[12_HEALTH]:::config -.-> S05
    S13[13_SOURCE_SYSTEMS]:::config -.-> S03
```

Solid arrows = data flow. Dashed = configuration the stages read.

---

## 7. paper-proof-grader — DeBERTa scoring pipeline

```mermaid
flowchart TB
    classDef in fill:#d3f9d8,stroke:#2f9e44,color:#000
    classDef proc fill:#e5dbff,stroke:#5f3dc4,color:#000
    classDef ext fill:#fff4e6,stroke:#e67700,color:#000
    classDef out fill:#c5f6fa,stroke:#0c8599,color:#000

    Drop["DROP_PAPERS_HERE<br/>(future: 00_DROP)"]:::in
    Drop --> Extract[claims extraction<br/>D:\brain\08_CLAIMS]:::proc
    Extract --> Score[DeBERTa zero-shot<br/>D:\brain\03_DEBERTA<br/>MoritzLaurer/DeBERTa-v3-large]:::proc
    Score --> SevenQ[7-Question scoring]:::proc
    SevenQ --> Embed[Infinity embeddings<br/>192.168.1.177:7997<br/>all-MiniLM-L6-v2]:::ext
    Embed --> Qdrant[Qdrant upsert<br/>192.168.1.177:6333<br/>collection: paper_proof_grader]:::ext

    Score --> Output[OUTPUT<br/>JSON + MD + HTML + Excel]:::out
    Output --> Reports[O:\Vault\AI Chats\<br/>Paper Proof Grader Reports]:::out
```

Note: DeBERTa model + claims extractor still live on D:\brain\ (different system from X:\). Won't migrate as part of this restructure.

---

## 8. Shared data layer — where outputs converge

All NLPs feed into the same downstream stores. This is the "memory" of the brain.

```mermaid
flowchart TB
    classDef nlp fill:#ffe8cc,stroke:#d9480f,color:#000
    classDef store fill:#fff4e6,stroke:#e67700,color:#000
    classDef ext fill:#c5f6fa,stroke:#0c8599,color:#000

    subgraph nlps["NLPs (producers)"]
        KR[knowledge-refinery]:::nlp
        PPG[paper-proof-grader]:::nlp
        AX[axioms]:::nlp
        LPD[link-pull-drop]:::nlp
        SHD[session-handoff-drop]:::nlp
        OL[ollama]:::nlp
    end

    subgraph filestores["File stores on X:\"]
        Captures[captures<br/>raw drops]:::store
        Digests[digests<br/>session summaries]:::store
        Embeddings[embeddings<br/>local cache]:::store
        Models[models<br/>cached weights]:::store
        Ratings[ratings]:::store
    end

    subgraph network["Network services @ 192.168.1.177"]
        Infinity[Infinity<br/>:7997<br/>embedding API]:::ext
        Qdrant[Qdrant<br/>:6333<br/>vector DB]:::ext
        Postgres[Postgres<br/>:2665<br/>metadata ledger]:::ext
    end

    AIChats[O:\Vault\AI Chats<br/>readable record]:::store

    LPD --> Captures
    SHD --> Digests
    OL --> Digests
    KR --> Digests
    PPG --> Embeddings
    PPG --> Infinity
    SHD --> Infinity
    Infinity --> Qdrant
    SHD --> AIChats
    PPG --> AIChats
    KR --> Postgres
```

---

## 9. Consolidation status — what moved and what's still pending

**Phase status as of 2026-05-16.** Tracks the actual restructure progress.

```mermaid
stateDiagram-v2
    [*] --> Phase1: 2026-05-16

    state Phase1 {
        [*] --> P1a
        P1a: Phase 1a flatten brain
        P1a --> P1b: complete
        P1b: Phase 1b pull D drive
        P1b --> P1ok
        P1ok: VERIFIED
    }
    Phase1 --> Phase2: complete

    state Phase2 {
        [*] --> Dedup
        Dedup: dedup sweep running
        Dedup --> DedupReport
        DedupReport: report at X:\Backside\DEDUP_REPORT_20260516.md
    }

    Phase2 --> Phase3: pending
    Phase3: Phase 3 push non-NLPs to GitHub
    Phase3 --> Phase4: pending

    state Phase4 {
        [*] --> Prompts
        Prompts: write prompts for cloud AIs
        Prompts --> P4a
        P4a: 4a per-NLP front-door rename
        P4a --> P4b
        P4b: 4b root simplification
        P4b --> P4c
        P4c: 4c batch-script path sweep
        P4c --> P4d
        P4d: 4d intake engine build
    }

    Phase4 --> Phase5: pending
    Phase5: Phase 5 BIL + FAP move to X (Option A locked)
    Phase5 --> [*]
```

---

## 10. The D-drive consolidation — what's coming to X:

David's directive 2026-05-16: *everything that deals with X: lives on X:*. BIL decision: **Option A — full move** (supersedes May-10 cold-archive lock).

```mermaid
flowchart LR
    classDef done fill:#d3f9d8,stroke:#2f9e44,color:#000
    classDef pending fill:#ffe3e3,stroke:#c92a2a,color:#000
    classDef arch fill:#f8f9fa,stroke:#868e96,color:#000

    subgraph d["D:\ (source)"]
        DC4C[D:\C4C symlink]:::done
        DCW[D:\C4C-wiki]:::done
        DFAP[D:\FAP]:::pending
        DBIL[D:\BIL<br/>264 files, 3.5MB]:::pending
    end

    subgraph x["X:\ (target)"]
        XC4C[X:\C4C<br/>2497 files]:::done
        XCW[X:\C4C-wiki<br/>862 files]:::done
        XFAP[X:\FAP<br/>63 files]:::pending
        XBIL[X:\BIL<br/>placeholder<br/>README only]:::pending
    end

    subgraph archD["D:\_ARCHIVE\"]
        ACW[C4C-wiki<br/>archived]:::arch
    end

    DC4C -.->|"removed<br/>(junction only)"|XC4C
    DCW -->|archived|ACW
    DCW -.->|already mirrored|XCW
    DFAP -->|"BLOCKED:<br/>BIL has 78 refs<br/>Phase 4c first"|XFAP
    DBIL -->|"Phase 4c sweeps refs<br/>then Phase 5 robocopy /MOVE"|XBIL
```

**Why D:\FAP is blocked:** D:\BIL\engines\pipeline\* hardcodes `D:\FAP` in 78 places across 10 files (fap_postgres_sync.py, fap_healthcheck.py, llm_hub.py, fap_dashboard.html, etc.). The FAP postgres sync runs every 12h. If we move D:\FAP before sweeping the refs, the next sync fails. So:

1. **Phase 4c (cloud AI):** find/replace `D:\BIL\` → `X:\BIL\` and `D:\FAP` → `X:\FAP` across all D:\BIL scripts. Update Task Scheduler XML.
2. **Phase 5:** stop the FAP scheduled task, `robocopy /MOVE D:\BIL X:\BIL`, `robocopy /MOVE D:\FAP X:\FAP`, re-import the task pointing at X:, re-enable, verify one cycle runs clean.

---

## 11. Mental model — the simplest possible version

If you forget everything else, remember this:

```mermaid
flowchart LR
    classDef in fill:#d3f9d8,stroke:#2f9e44,color:#000
    classDef brain fill:#e5dbff,stroke:#5f3dc4,color:#000
    classDef out fill:#c5f6fa,stroke:#0c8599,color:#000

    Drop[drop file]:::in --> Front[front door<br/>00_DROP]:::brain
    Front --> Engine[intake engine<br/>routes / runs]:::brain
    Engine --> NLP[NLP processes]:::brain
    NLP --> Out[output ready]:::out
    NLP --> Vec[searchable later<br/>via Qdrant]:::out
```

That's the whole brain. Everything else is detail.

---

## Where to dig deeper

- **Plan with phased execution:** `C:\Users\lowes\.claude\plans\yes-i-want-togo-agile-puddle.md`
- **Phase 1 logs:** `X:\Backside\PHASE1A_LOG_20260516.md`, `PHASE1B_LOG_20260516.md`, `PHASE1_PATH_FIX_LOG_20260516.md`
- **Dedup report (Phase 2, running):** `X:\Backside\DEDUP_REPORT_20260516.md`
- **CLAUDE.md (operating manual):** `C:\Users\lowes\AppData\Local\Programs\Warp\CLAUDE.md`
- **Canon (locked theory):** comms-hub `canon` channel — canon wins on drift
