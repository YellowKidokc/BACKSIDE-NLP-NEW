# Whisper Transcribe — Quick Use

1. Drop one or more `audio.mp3` files into `_inbox\`.
2. Double-click `FRONT_DOOR.bat`.
3. Results appear in `_outbox\`.

## Optional: Fetch Source

Create `FETCH_SOURCE.txt` beside `FRONT_DOOR.bat` and put one folder path in it. The front door copies files from that folder into `_inbox\` before running.

## What You Get

- transcript artifact / transcript text
- Standard station artifact JSON in `_outbox\`
- Original file archived to `_processed\` by `pipeline.py`

## What This Station Does

Transcribes audio files into text for downstream NLP.
