from __future__ import annotations

import json
import logging
import re
import subprocess
import sys
from datetime import datetime
from html import unescape
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def _setup_logging(name: str) -> logging.Logger:
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8-sig"))
    log_dir = Path(cfg.get("log_dir") or (ROOT / "_LOGS"))
    log_dir.mkdir(parents=True, exist_ok=True)
    logfile = log_dir / f"workflow_{name}_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger(f"workflow.{name}")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def _slug(text: str, max_len: int = 80) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip("-")
    return (text or "item")[:max_len]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="replace")


def _extract_urls(text: str) -> list[str]:
    matches = re.findall(r"https?://[^\s)>\]]+", text)
    seen: set[str] = set()
    urls: list[str] = []
    for match in matches:
        cleaned = match.rstrip(".,;")
        if cleaned not in seen:
            seen.add(cleaned)
            urls.append(cleaned)
    return urls


def _youtube_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if "youtu.be" in host:
        return parsed.path.strip("/").split("/")[0] or None
    if "youtube.com" in host:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        if parsed.path.startswith("/shorts/"):
            parts = parsed.path.split("/")
            return parts[2] if len(parts) > 2 else None
        if parsed.path.startswith("/embed/"):
            parts = parsed.path.split("/")
            return parts[2] if len(parts) > 2 else None
    return None


def _is_youtube(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return "youtube.com" in host or "youtu.be" in host


def _fetch_youtube_metadata(url: str, timeout_sec: int) -> dict:
    oembed = requests.get(
        "https://www.youtube.com/oembed",
        params={"url": url, "format": "json"},
        timeout=timeout_sec,
    )
    oembed.raise_for_status()
    return oembed.json()


def _pull_youtube_transcript(video_id: str) -> dict:
    from youtube_transcript_api import YouTubeTranscriptApi

    try:
        api = YouTubeTranscriptApi()
        result = api.fetch(video_id, languages=["en"])
        transcript = " ".join(snippet.text for snippet in result.snippets).strip()
        return {
            "success": True,
            "transcript": transcript,
            "language": result.language_code,
            "source": "auto" if result.is_generated else "manual",
            "char_count": len(transcript),
        }
    except Exception as exc:
        return {
            "success": False,
            "error": type(exc).__name__,
            "error_detail": str(exc),
        }


def _download_youtube_media(url: str, out_dir: Path, log: logging.Logger) -> dict:
    cmd = [
        "yt-dlp",
        "--write-info-json",
        "--write-description",
        "--write-thumbnail",
        "--write-auto-sub",
        "--write-sub",
        "--sub-langs",
        "en.*",
        "-o",
        str(out_dir / "%(title)s [%(id)s].%(ext)s"),
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return {"success": True}
    log.warning("yt-dlp failed for %s: %s", url, result.stderr.strip())
    return {
        "success": False,
        "error": "yt_dlp_failed",
        "stderr": result.stderr.strip(),
    }


def _extract_visible_text(html: str) -> str:
    html = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?>.*?</style>", " ", html)
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return unescape(soup.get_text(separator=" ", strip=True))


def _process_web(url: str, out_dir: Path, cfg: dict) -> dict:
    response = requests.get(
        url,
        headers={"User-Agent": cfg["user_agent"]},
        timeout=int(cfg["timeout_sec"]),
    )
    response.raise_for_status()
    parsed = urlparse(url)
    stem = _slug(f"{parsed.netloc}_{parsed.path or 'root'}")
    html_path = out_dir / f"{stem}.html"
    text_path = out_dir / f"{stem}.txt"
    html_path.write_text(response.text, encoding="utf-8", errors="replace")
    text = _extract_visible_text(response.text)[: int(cfg["max_web_chars"])]
    text_path.write_text(text, encoding="utf-8")
    return {
        "success": True,
        "status_code": response.status_code,
        "html_path": str(html_path),
        "text_path": str(text_path),
        "char_count": len(text),
    }


def main() -> int:
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8-sig"))
    log = _setup_logging(cfg["name"])

    input_dir = Path(cfg["input_dir"])
    output_dir = Path(cfg["output_dir"])
    archive_dir = Path(cfg["archive_dir"])
    youtube_output_dir = Path(cfg["youtube_output_dir"])
    web_output_dir = Path(cfg["web_output_dir"])

    for path in (input_dir, output_dir, archive_dir, youtube_output_dir, web_output_dir):
        path.mkdir(parents=True, exist_ok=True)

    files = sorted(
        p for p in input_dir.iterdir()
        if p.is_file() and p.suffix.lower() in {ext.lower() for ext in cfg["text_extensions"]}
    )
    log.info("found %d link list files", len(files))
    if not files:
        log.info("nothing to do")
        return 0

    latest = max(files, key=lambda p: p.stat().st_mtime)
    text = _read_text(latest)
    urls = _extract_urls(text)
    log.info("processing %s with %d urls", latest, len(urls))

    run_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = output_dir / f"run_{run_stamp}_{_slug(latest.stem, 40)}"
    run_dir.mkdir(parents=True, exist_ok=True)
    yt_run_dir = youtube_output_dir / run_dir.name
    web_run_dir = web_output_dir / run_dir.name
    yt_run_dir.mkdir(parents=True, exist_ok=True)
    web_run_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []
    for url in urls:
        item: dict = {"url": url, "kind": "youtube" if _is_youtube(url) else "web"}
        try:
            if item["kind"] == "youtube":
                video_id = _youtube_video_id(url)
                item["video_id"] = video_id
                if video_id:
                    item["transcript"] = _pull_youtube_transcript(video_id)
                try:
                    item["metadata"] = _fetch_youtube_metadata(url, int(cfg["timeout_sec"]))
                except Exception as exc:
                    item["metadata_error"] = str(exc)
                if bool(cfg.get("download_youtube_media", True)):
                    download_dir = yt_run_dir / _slug(video_id or url, 60)
                    download_dir.mkdir(parents=True, exist_ok=True)
                    item["download"] = _download_youtube_media(url, download_dir, log)
                    item["download_dir"] = str(download_dir)
            else:
                if bool(cfg.get("fetch_web_pages", True)):
                    item["fetch"] = _process_web(url, web_run_dir, cfg)
        except Exception as exc:
            item["error"] = f"{type(exc).__name__}: {exc}"
        results.append(item)

    manifest = {
        "source_file": str(latest),
        "processed_at": datetime.now().isoformat(timespec="seconds"),
        "url_count": len(urls),
        "results": results,
    }
    manifest_path = run_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    archived = archive_dir / latest.name
    if archived.exists():
        archived.unlink()
    latest.replace(archived)

    log.info("manifest -> %s", manifest_path)
    log.info("archived input -> %s", archived)
    log.info("youtube output -> %s", yt_run_dir)
    log.info("web output -> %s", web_run_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())

