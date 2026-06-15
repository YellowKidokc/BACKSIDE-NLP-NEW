# 05_YOUTUBE — Troubleshooting

## `403 Forbidden — quotaExceeded`

YouTube Data API daily quota is 10,000 units; `search.list` costs 100 each. So you can run ~100 search calls per day. The runner catches this and exits cleanly — re-run tomorrow.

To raise quota: Google Cloud Console → APIs & Services → Quotas → request increase. Free tier maxes around 1M/day after approval.

## `403 Forbidden — accessNotConfigured`

The API key works but the YouTube Data API v3 isn't enabled on its project. Console → APIs & Services → Library → "YouTube Data API v3" → Enable.

## `403 Forbidden — keyInvalid`

The key in `config.json` is wrong. Verify by visiting:

```
https://www.googleapis.com/youtube/v3/search?part=snippet&q=test&key=<KEY>
```

If that URL returns the same 403 in a browser, the key is bad.

## Self-test returns 0 results

The key is restricted (HTTP referrer / IP allowlist). For a local script you need either:
- An unrestricted server key, or
- An IP allowlist that includes your egress IP.

Console → Credentials → click the key → Application restrictions → "None" or add your IP.

## Lots of duplicates being inserted

Shouldn't happen — the runner pre-loads all `video_id` values, dedups in memory, and the table has `UNIQUE(video_id)` plus `ON CONFLICT DO NOTHING`. If you're seeing dupes, the table doesn't have the unique constraint. Check schema:

```
\d youtube_apologetics
```

If `video_id UNIQUE` is missing, the table was created outside this tool. Drop and re-create via `LOAD_YOUTUBE_JSON.bat` — it uses the canonical DDL.

## Bulk-load the existing 3,913 video JSON

```
RUN.bat --load-json D:\brain\_BILL_BRAIN_PACKAGE\BILL_BRAIN_PACKAGE\youtube_apologetics_data.json
```

or use `07_POSTGRES\LOAD_YOUTUBE_JSON.bat` (same effect).

## Adding new queries

Edit `config.json` → `queries` array. The runner deduplicates against the table at startup, so re-running the same queries won't duplicate work — it will just find new uploads.

## Want timestamps + view counts

`search.list` only returns snippet data. For statistics, after scraping run a follow-up `videos.list?part=statistics,contentDetails&id=...` per chunk of 50 video IDs (cost: 1 unit each). Not implemented here yet — add if you decide to go deeper.
