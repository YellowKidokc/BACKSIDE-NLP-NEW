# link-pull-drop Troubleshooting

## What this workflow does

- Reads a `.txt` or `.md` file full of links from `X:\captures\links\DROP_HERE`
- Sends YouTube links through transcript-first handling and optional `yt-dlp` download
- Sends normal web links through fetch + HTML save + text extraction

## Common failures

### Python not found

Expected:
`C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe`

Fix:
- install Python 3.12
- or update the `.bat` files to the real Python path

### `yt-dlp` fails

Fix:
- run `UPDATE.bat`
- test manually with `yt-dlp --version`
- some videos block transcript/media access

### Web page fetch fails

Fix:
- check whether the site blocks bots
- retry later
- some pages require login or JavaScript rendering

### No output appears

Check:
- `X:\Backside\stations\link-pull.station\DROP_HERE`
- `X:\Backside\stations\link-pull.station\EXPORTS`
- `X:\Backside\_LOGS\workflow_link-pull-drop_*.log`

