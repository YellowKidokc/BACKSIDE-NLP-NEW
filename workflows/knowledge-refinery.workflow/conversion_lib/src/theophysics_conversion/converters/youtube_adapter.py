from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse

from ..models import ConvertResult


def youtube_id(url: str) -> str | None:
    parsed = urlparse(url.strip())
    if "youtu.be" in parsed.netloc:
        return parsed.path.strip("/") or None
    query = parse_qs(parsed.query)
    if "v" in query and query["v"]:
        return query["v"][0]
    match = re.search(r"/(?:embed|shorts)/([^/?#]+)", parsed.path)
    return match.group(1) if match else None


def convert_youtube(url: str) -> ConvertResult:
    video_id = youtube_id(url)
    if not video_id:
        return ConvertResult(markdown="", warnings=["Could not detect YouTube video id."])
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except Exception as exc:  # pragma: no cover - environment-dependent
        return ConvertResult(
            markdown="",
            metadata={"video_id": video_id},
            warnings=[f"youtube-transcript-api is not available: {exc}"],
        )

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as exc:  # pragma: no cover - network/video-dependent
        return ConvertResult(
            markdown="",
            metadata={"video_id": video_id},
            warnings=[f"YouTube transcript unavailable: {exc}"],
        )

    lines = [f"# YouTube Transcript: {video_id}", "", f"Source: {url}", ""]
    lines.extend(item.get("text", "").strip() for item in transcript if item.get("text"))
    return ConvertResult(
        markdown="\n".join(lines).strip() + "\n",
        metadata={"video_id": video_id, "segments": len(transcript)},
    )

