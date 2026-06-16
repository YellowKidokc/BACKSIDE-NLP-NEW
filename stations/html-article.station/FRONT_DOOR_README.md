# Html Article — Quick Use

1. Drop one or more `paper.md + classification JSON` files into `_inbox\`.
2. Double-click `FRONT_DOOR.bat`.
3. Results appear in `_outbox\`.

## Optional: Fetch Source

Create `FETCH_SOURCE.txt` beside `FRONT_DOOR.bat` and put one folder path in it. The front door copies files from that folder into `_inbox\` before running.

## What You Get

- formatted HTML page
- Standard station artifact JSON in `_outbox\`
- Original file archived to `_processed\` by `pipeline.py`

## What This Station Does

Generates final HTML article output from paper content and classification context.
