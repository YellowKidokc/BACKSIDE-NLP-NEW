#!/usr/bin/env python3
"""
THEOPHYSICS APOLOGETICS RESEARCH PIPELINE
==========================================
POF 2828 | 2026-05-24

Download YouTube channels/playlists/videos → transcribe with Whisper →
organize transcripts for AI analysis.

Pipeline:
  1. yt-dlp pulls audio (or full channel metadata)
  2. youtube-transcript-api tries existing captions first (free, instant)
  3. faster-whisper transcribes anything without captions
  4. Transcripts organized by channel/video with metadata JSON
  5. Ready for AI partner ingestion (argument extraction, claim mapping)

Usage:
  # Single video
  python apologetics_pipeline.py https://www.youtube.com/watch?v=XXXXX

  # Entire channel
  python apologetics_pipeline.py https://www.youtube.com/@ChannelName

  # Playlist
  python apologetics_pipeline.py https://www.youtube.com/playlist?list=XXXXX

  # Multiple URLs from a file (one per line)
  python apologetics_pipeline.py --batch urls.txt

  # Skip Whisper, only grab existing captions
  python apologetics_pipeline.py --captions-only https://www.youtube.com/@Channel

  # Force Whisper even if captions exist
  python apologetics_pipeline.py --force-whisper https://www.youtube.com/watch?v=XXXXX

  # Use a specific Whisper model (default: medium)
  python apologetics_pipeline.py --model large-v3 https://www.youtube.com/watch?v=XXXXX

Requires: yt-dlp, faster-whisper, youtube-transcript-api
All pre-installed on this machine.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any


# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

# Station root = the folder this script lives in. All exports go to the
# station-root EXPORTS folder ONLY (transcripts + metadata JSON + manifests).
STATION_ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = STATION_ROOT / "EXPORTS"
DEFAULT_MODEL = "medium"  # whisper model: tiny, base, small, medium, large-v3
DEFAULT_LANGUAGE = "en"
AUDIO_FORMAT = "mp3"
MAX_CONCURRENT = 3


def sanitize_filename(name: str) -> str:
    """Make a string safe for filenames."""
    clean = re.sub(r'[<>:"/\\|?*]', '_', name)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean[:120]  # cap length


def get_channel_slug(url: str, meta: dict) -> str:
    """Extract a clean channel slug from metadata."""
    channel = meta.get("channel") or meta.get("uploader") or "unknown-channel"
    return sanitize_filename(channel)


# ═══════════════════════════════════════════════════════════════
# STEP 1: METADATA + AUDIO DOWNLOAD (yt-dlp)
# ═══════════════════════════════════════════════════════════════

def fetch_metadata(url: str) -> list[dict[str, Any]]:
    """Get video metadata without downloading. Returns list of video info dicts."""
    print(f"\n[META] Fetching metadata for: {url}")
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-json",
        "--no-warnings",
        "--ignore-errors",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    entries = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    print(f"[META] Found {len(entries)} video(s)")
    return entries


def download_audio(video_url: str, output_dir: Path) -> Path | None:
    """Download audio-only for a single video. Returns path to audio file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(output_dir / "%(id)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", AUDIO_FORMAT,
        "--audio-quality", "5",  # moderate quality, smaller files
        "--output", output_template,
        "--no-playlist",
        "--no-warnings",
        "--ignore-errors",
        "--write-info-json",  # saves metadata alongside audio
        video_url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"  [WARN] yt-dlp failed: {result.stderr[:200]}")
        return None

    # Find the downloaded file
    for f in output_dir.iterdir():
        if f.suffix == f".{AUDIO_FORMAT}":
            return f
    return None


# ═══════════════════════════════════════════════════════════════
# STEP 2: CAPTION GRAB (youtube-transcript-api)
# ═══════════════════════════════════════════════════════════════

def try_existing_captions(video_id: str) -> str | None:
    """Try to grab existing YouTube captions. Returns transcript text or None."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try manual captions first (higher quality), then auto-generated
        transcript = None
        for t in transcript_list:
            if not t.is_generated:
                transcript = t
                break
        if transcript is None:
            for t in transcript_list:
                if t.language_code.startswith("en"):
                    transcript = t
                    break
        if transcript is None:
            # Take whatever we can get
            transcript = next(iter(transcript_list))

        fetched = transcript.fetch()
        lines = []
        for entry in fetched:
            text = entry.text if hasattr(entry, 'text') else entry.get('text', '')
            lines.append(text)
        full_text = " ".join(lines)
        if len(full_text.strip()) < 50:
            return None
        return full_text

    except Exception as e:
        return None


# ═══════════════════════════════════════════════════════════════
# STEP 3: WHISPER TRANSCRIPTION (faster-whisper)
# ═══════════════════════════════════════════════════════════════

_whisper_model = None


def get_whisper_model(model_size: str):
    """Lazy-load the Whisper model (expensive, only load once)."""
    global _whisper_model
    if _whisper_model is None:
        from faster_whisper import WhisperModel
        print(f"\n[WHISPER] Loading model: {model_size}")
        print(f"[WHISPER] This may take a minute on first run...")
        # Use CPU by default; switch to "cuda" if you have GPU
        _whisper_model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",  # fast on CPU
        )
        print(f"[WHISPER] Model loaded.")
    return _whisper_model


def transcribe_audio(audio_path: Path, model_size: str = DEFAULT_MODEL) -> str:
    """Transcribe an audio file with faster-whisper. Returns full text."""
    model = get_whisper_model(model_size)
    print(f"  [WHISPER] Transcribing: {audio_path.name}")
    start = time.time()

    segments, info = model.transcribe(
        str(audio_path),
        language=DEFAULT_LANGUAGE,
        beam_size=5,
        word_timestamps=False,
        vad_filter=True,  # skip silence
    )

    full_text = " ".join(seg.text.strip() for seg in segments)
    elapsed = time.time() - start
    print(f"  [WHISPER] Done in {elapsed:.1f}s ({len(full_text)} chars)")
    return full_text


# ═══════════════════════════════════════════════════════════════
# STEP 4: ORGANIZE OUTPUT
# ═══════════════════════════════════════════════════════════════

def write_transcript(
    output_dir: Path,
    channel_slug: str,
    video_id: str,
    title: str,
    transcript: str,
    source: str,  # "captions" or "whisper"
    metadata: dict[str, Any],
) -> Path:
    """Write transcript and metadata to organized folder structure."""
    channel_dir = output_dir / channel_slug
    channel_dir.mkdir(parents=True, exist_ok=True)

    safe_title = sanitize_filename(title)
    txt_path = channel_dir / f"{video_id}_{safe_title}.txt"
    json_path = channel_dir / f"{video_id}_{safe_title}.meta.json"

    # Write transcript
    txt_path.write_text(transcript, encoding="utf-8")

    # Write metadata
    meta_out = {
        "video_id": video_id,
        "title": title,
        "channel": metadata.get("channel") or metadata.get("uploader", ""),
        "channel_id": metadata.get("channel_id", ""),
        "upload_date": metadata.get("upload_date", ""),
        "duration": metadata.get("duration", 0),
        "view_count": metadata.get("view_count", 0),
        "description": (metadata.get("description") or "")[:500],
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "transcript_source": source,
        "transcript_chars": len(transcript),
        "transcript_words": len(transcript.split()),
        "processed_at": datetime.now().isoformat(timespec="seconds"),
        "tags": metadata.get("tags", []),
    }
    json_path.write_text(
        json.dumps(meta_out, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return txt_path


def write_channel_manifest(output_dir: Path, channel_slug: str, results: list[dict]):
    """Write a manifest for the channel with all processed videos."""
    channel_dir = output_dir / channel_slug
    manifest_path = channel_dir / "_MANIFEST.json"
    manifest = {
        "channel": channel_slug,
        "processed_at": datetime.now().isoformat(timespec="seconds"),
        "total_videos": len(results),
        "captions_used": sum(1 for r in results if r.get("source") == "captions"),
        "whisper_used": sum(1 for r in results if r.get("source") == "whisper"),
        "failed": sum(1 for r in results if r.get("source") == "failed"),
        "total_words": sum(r.get("words", 0) for r in results),
        "videos": results,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\n[MANIFEST] {manifest_path}")
    print(f"  Videos: {manifest['total_videos']}")
    print(f"  Captions: {manifest['captions_used']}")
    print(f"  Whisper: {manifest['whisper_used']}")
    print(f"  Failed: {manifest['failed']}")
    print(f"  Total words: {manifest['total_words']:,}")


# ═══════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════

def process_video(
    entry: dict[str, Any],
    output_dir: Path,
    audio_dir: Path,
    channel_slug: str,
    *,
    captions_only: bool = False,
    force_whisper: bool = False,
    model_size: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """Process a single video: captions → whisper fallback → save."""
    video_id = entry.get("id", "")
    title = entry.get("title") or entry.get("fulltitle") or video_id
    url = entry.get("url") or entry.get("webpage_url") or f"https://www.youtube.com/watch?v={video_id}"

    # Ensure we have a proper video URL
    if not video_id:
        return {"video_id": "unknown", "source": "failed", "error": "no video ID"}

    if "youtube.com/watch" not in url and "youtu.be/" not in url:
        url = f"https://www.youtube.com/watch?v={video_id}"

    print(f"\n{'='*60}")
    print(f"[{video_id}] {title}")
    print(f"{'='*60}")

    result = {
        "video_id": video_id,
        "title": title,
        "source": "failed",
        "words": 0,
    }

    # Check if already processed
    channel_dir = output_dir / channel_slug
    existing = list(channel_dir.glob(f"{video_id}_*.txt")) if channel_dir.exists() else []
    if existing:
        print(f"  [SKIP] Already processed: {existing[0].name}")
        text = existing[0].read_text(encoding="utf-8")
        result["source"] = "cached"
        result["words"] = len(text.split())
        return result

    transcript = None
    source = "failed"

    # Step 1: Try existing captions (unless force_whisper)
    if not force_whisper:
        print(f"  [CAPTIONS] Trying YouTube captions...")
        transcript = try_existing_captions(video_id)
        if transcript:
            source = "captions"
            print(f"  [CAPTIONS] Got {len(transcript.split())} words")

    # Step 2: Whisper fallback (unless captions_only)
    if transcript is None and not captions_only:
        print(f"  [DOWNLOAD] Downloading audio...")
        audio_path = download_audio(url, audio_dir / video_id)
        if audio_path and audio_path.exists():
            transcript = transcribe_audio(audio_path, model_size)
            source = "whisper"
            # Clean up audio to save space (keep if you want)
            # audio_path.unlink()
        else:
            print(f"  [FAIL] Could not download audio")

    # Step 3: Save
    if transcript and len(transcript.strip()) > 50:
        txt_path = write_transcript(
            output_dir, channel_slug, video_id,
            title, transcript, source, entry,
        )
        result["source"] = source
        result["words"] = len(transcript.split())
        result["file"] = str(txt_path)
        print(f"  [SAVED] {txt_path.name} ({result['words']:,} words, source={source})")
    else:
        print(f"  [FAIL] No transcript obtained")

    return result


def run_pipeline(
    urls: list[str],
    output_dir: Path,
    *,
    captions_only: bool = False,
    force_whisper: bool = False,
    model_size: str = DEFAULT_MODEL,
    limit: int | None = None,
):
    """Run the full pipeline on one or more URLs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    # Keep intermediate audio OUT of EXPORTS so the export folder stays clean
    # (only transcripts / metadata / manifests live under output_dir).
    audio_dir = output_dir.parent / "_scratch_audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'#'*60}")
    print(f"# THEOPHYSICS APOLOGETICS RESEARCH PIPELINE")
    print(f"# Output: {output_dir}")
    print(f"# Mode: {'captions-only' if captions_only else 'captions + whisper'}")
    print(f"# Model: {model_size}")
    print(f"{'#'*60}")

    for url in urls:
        # Get metadata for all videos
        entries = fetch_metadata(url)

        if limit:
            entries = entries[:limit]

        if not entries:
            print(f"[WARN] No videos found for: {url}")
            continue

        # Determine channel slug from first entry
        channel_slug = get_channel_slug(url, entries[0])
        print(f"\n[CHANNEL] {channel_slug} ({len(entries)} videos)")

        results = []
        for i, entry in enumerate(entries, 1):
            print(f"\n--- Video {i}/{len(entries)} ---")
            r = process_video(
                entry, output_dir, audio_dir, channel_slug,
                captions_only=captions_only,
                force_whisper=force_whisper,
                model_size=model_size,
            )
            results.append(r)

        write_channel_manifest(output_dir, channel_slug, results)

    print(f"\n{'#'*60}")
    print(f"# PIPELINE COMPLETE")
    print(f"# Transcripts: {output_dir}")
    print(f"{'#'*60}")


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Theophysics Apologetics Research Pipeline — "
                    "Download YouTube → Transcribe → Organize for AI analysis",
    )
    parser.add_argument(
        "urls", nargs="*",
        help="YouTube video, channel, or playlist URLs",
    )
    parser.add_argument(
        "--batch", type=Path,
        help="File containing URLs, one per line",
    )
    parser.add_argument(
        "--output", "-o", type=Path, default=DEFAULT_OUTPUT,
        help=f"Output directory (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--captions-only", action="store_true",
        help="Only grab existing captions, skip Whisper",
    )
    parser.add_argument(
        "--force-whisper", action="store_true",
        help="Force Whisper even if captions exist",
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL,
        choices=["tiny", "base", "small", "medium", "large-v3"],
        help=f"Whisper model size (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Max videos per URL (for testing)",
    )

    args = parser.parse_args()

    urls = list(args.urls or [])
    if args.batch and args.batch.exists():
        urls.extend(
            line.strip()
            for line in args.batch.read_text().splitlines()
            if line.strip() and not line.startswith("#")
        )

    if not urls:
        parser.error("No URLs provided. Pass URLs or use --batch file.txt")

    run_pipeline(
        urls,
        args.output,
        captions_only=args.captions_only,
        force_whisper=args.force_whisper,
        model_size=args.model,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()
