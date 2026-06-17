# Backside Station Export Hygiene Handoff

Date: 2026-06-02
Scope: `obsidian-export.station`, `ollama`, `paperqa2.station`
Root rule: active file exports must land under each station root `EXPORTS\` only.

## Workflow Classification

| Workflow | Status | Why |
| --- | --- | --- |
| `X:\Backside\stations\obsidian-export.station` | LIVE | Export-safe canary path is wired. Staged notes, routed notes, and validation reports now write under `EXPORTS\reports`. Direct copy to the Obsidian canon vault was disabled; target paths remain metadata only. |
| `X:\Backside\stations\ollama` | REVIEW_LATER | Filesystem exports are rewired to station `EXPORTS`, and old full-conversation source copies were preserved there. Runtime still depends on missing external input drop `X:\brain\00_WORKFLOWS\session-handoff-drop\DROP_HERE`; vector/Postgres side effects need David decision if those count as exports. |
| `X:\Backside\stations\paperqa2.station` | CONTEXT_ONLY | This is a vendored PaperQA2 codebase with no active nested export folders. Root `EXPORTS` lanes exist, but `RUN.bat` stops because the `pqa` CLI is not installed. |

## Protected Roots

Do not archive, rename, or mutate these roots from this station pass:

| Root | Classification | Verified |
| --- | --- | --- |
| `X:\Backside\knowledge-refinery` | DO_NOT_ARCHIVE | Exists; not touched by this pass. |
| `X:\Backside\brain` | DO_NOT_ARCHIVE | Exists; not touched by this pass. |
| `X:\Backside\apps` | DO_NOT_ARCHIVE | Exists; not touched by this pass. |

Checked alternates `X:\knowledge-refinery`, `X:\brain`, and `X:\apps`; they were not present during this pass.

## Heavy Lanes Parked

| Lane | Status | Evidence / Boundary |
| --- | --- | --- |
| Math translation layer | REVIEW_LATER | Mentioned only in GTQ context/export copies; no implementation touched. |
| File naming system | REVIEW_LATER | No active station work performed. |
| OpenAI / vector / o3 lane | REVIEW_LATER | `ollama` still has vector/Postgres code; PaperQA2 docs describe OpenAI/vector behavior. No new OpenAI/o3/vector implementation was started. |
| Proof injection | REVIEW_LATER | No active station work performed. |

## Export Hygiene Evidence

- Final active folder check found no `OUTPUT`, lowercase output/export/results/report dirs, artifacts dirs, or `__pycache__` active outside `EXPORTS` or `_ARCHIVE` for the three scoped stations.
- `obsidian-export.station` latest smoke report: `EXPORTS\reports\02_VALIDATION_REPORTS\obsidian_export_report_20260602_033425.json`.
- `obsidian-export.station` still returns nonzero because two GTQ-17 source artifacts are missing upstream:
  `X:\Backside\workflows\axioms.workflow\03_FINAL_READY\Genesis-to-Quantum\gtq-17-ran-the-numbers\JSON\gtq-17-ran-the-numbers.paper-snapshot.json`.
- `ollama` smoke log: `EXPORTS\reports\logs\ollama_handoff_20260602.log`.
- `ollama` copied 11 files from `Z:\Vault\AI-Chats History\full conversation` into `EXPORTS\source_copies\Z_Vault_AI-Chats_History_full_conversation`; SHA256 verification reported `Bad=0`.
- `paperqa2.station` root `EXPORTS` lanes exist, but no export artifacts were produced because `pqa` is not installed.

## Send-Home Decision

GREEN for export hygiene closure, with guardrails: do not archive protected roots; do not unpark heavy lanes; do not treat runtime blockers as export failures.
