# Downstream Integration Handoff — READ THIS FIRST
**Source:** D:\GitHub\organize\DOWNSTREAM_INTEGRATION_HANDOFF.md
**Created:** 2026-06-03 by Opus (Claude)
**Context:** Worked out with David. The GUI builder session doesn't have this context.

## Quick summary for FIS work:

1. `/approve` needs to call `PPK.learn()` — this is THE missing piece
2. New SQLite WAL event log decouples learning from the hot path
3. OpenRecall at `C:\Users\lowes\Downloads\openrecall-main\` is a third input stream via `/bil/recall`
4. Everything stays on port 8420 — no new servers
5. Full details in `D:\GitHub\organize\DOWNSTREAM_INTEGRATION_HANDOFF.md`
