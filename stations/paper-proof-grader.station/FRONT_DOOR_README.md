# Paper Proof Grader — Quick Use

1. Drop one or more `paper.md` files into `_inbox\`.
2. Double-click `FRONT_DOOR.bat`.
3. Results appear in `_outbox\`.

## Optional: Fetch Source

Create `FETCH_SOURCE.txt` beside `FRONT_DOOR.bat` and put one folder path in it. The front door copies files from that folder into `_inbox\` before running.

## What You Get

- proof grade, kill conditions, and FACTS artifact JSON
- Standard station artifact JSON in `_outbox\`
- Original file archived to `_processed\` by `pipeline.py`

## What This Station Does

Grades proof structure, rigor, and kill-condition readiness.
