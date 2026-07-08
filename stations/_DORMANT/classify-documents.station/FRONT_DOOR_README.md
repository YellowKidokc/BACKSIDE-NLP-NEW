# Classify Documents — Quick Use

1. Drop one or more `paper.md` files into `_inbox\`.
2. Double-click `FRONT_DOOR.bat`.
3. Results appear in `_outbox\`.

## Optional: Fetch Source

Create `FETCH_SOURCE.txt` beside `FRONT_DOOR.bat` and put one folder path in it. The front door copies files from that folder into `_inbox\` before running.

## What You Get

- classification artifact with doc_type, tags, spine mappings, dependencies, word count, and reading level
- Standard station artifact JSON in `_outbox\`
- Original file archived to `_processed\` by `pipeline.py`

## What This Station Does

Classifies a paper/article into the downstream passport schema.
