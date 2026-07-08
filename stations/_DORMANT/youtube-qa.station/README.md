# youtube-qa.workflow

File-based YouTube transcript Q/A extraction lane for Case for Christ and related apologetics material.

## Inputs

- Transcript file or folder of transcript files
- Supported formats: `.txt`, `.srt`, `.vtt`, `.md`
- Optional metadata JSON with keys such as:
  - `video_title`
  - `youtube_url`
  - `channel`

## Outputs

Per transcript, the workflow writes:

- `02_QA_JSON\*.qa.json`
- `03_QA_MARKDOWN\*.qa.md`
- `04_QA_EXCEL\*.qa.csv`
- `04_QA_EXCEL\*.qa.xlsx` when `--xlsx` is used and the writer dependency is available
- `05_SNAPSHOTS\*.paper-snapshot.partial.json` when `--snapshot-partial` is used

## Run

Single file:

```powershell
python "X:\Backside\workflows\youtube-qa.workflow\scripts\extract_youtube_qa.py" "X:\Backside\workflows\youtube-qa.workflow\00_INBOX_TRANSCRIPTS\sample_apologetics_dialogue.vtt" --metadata-json "X:\Backside\workflows\youtube-qa.workflow\00_INBOX_TRANSCRIPTS\sample_apologetics_dialogue.json" --xlsx --snapshot-partial
```

Whole folder:

```powershell
python "X:\Backside\workflows\youtube-qa.workflow\scripts\extract_youtube_qa.py" "X:\Backside\workflows\youtube-qa.workflow\00_INBOX_TRANSCRIPTS" --xlsx --snapshot-partial
```

## Notes

- Question detection is conservative when punctuation is weak.
- Answers are only drawn from nearby transcript blocks; no invented answers.
- Rhetorical and implied answers are marked explicitly.
- Speaker detection only fires when the transcript has clear `Speaker: text` patterns.
