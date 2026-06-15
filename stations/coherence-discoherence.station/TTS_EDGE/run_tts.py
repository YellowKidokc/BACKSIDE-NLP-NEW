import asyncio
import ctypes
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import edge_tts


BASE = Path(__file__).resolve().parent
INBOX = BASE / "inbox"
OUTBOX = BASE / "outbox"
PROCESSED = BASE / "processed"
LOGS = BASE / "logs"
CONFIG = BASE / "config.json"
LOCK = BASE / ".tts_running.lock"


def load_config():
    defaults = {
        "voice": "en-US-BrianMultilingualNeural",
        "rate": "+75%",
        "volume": "+0%",
        "pitch": "+0Hz",
        "chunk_chars": 3200,
        "part_timeout_seconds": 300,
        "input_extensions": [".md", ".markdown", ".txt"],
    }
    if CONFIG.exists():
        defaults.update(json.loads(CONFIG.read_text(encoding="utf-8")))
    return defaults


def clean_markdown(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.M)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.M)
    text = re.sub(r"[*_>#|]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def split_text(text, limit):
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks = []
    current = ""
    for paragraph in paragraphs:
        if len(paragraph) > limit:
            sentences = re.split(r"(?<=[.!?])\s+", paragraph)
        else:
            sentences = [paragraph]
        for piece in sentences:
            if not piece:
                continue
            if len(current) + len(piece) + 2 <= limit:
                current = f"{current}\n\n{piece}".strip()
            else:
                if current:
                    chunks.append(current)
                current = piece
    if current:
        chunks.append(current)
    return chunks


def safe_stem(path):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", path.stem).strip("._-") or "tts"


def progress_bar(done, total, width=28):
    if total <= 0:
        return "[" + "-" * width + "] 0%"
    filled = round(width * done / total)
    pct = round(100 * done / total)
    return "[" + "#" * filled + "-" * (width - filled) + f"] {pct:3d}%"


async def synthesize(text, output, cfg):
    communicate = edge_tts.Communicate(
        text,
        voice=cfg["voice"],
        rate=cfg["rate"],
        volume=cfg["volume"],
        pitch=cfg["pitch"],
    )
    await communicate.save(str(output))


async def synthesize_with_spinner(text, output, cfg):
    task = asyncio.create_task(synthesize(text, output, cfg))
    started = time.time()
    spinner = "|/-\\"
    timeout = int(cfg.get("part_timeout_seconds", 300))
    tick = 0
    while not task.done():
        elapsed = time.time() - started
        print(f"\r    working {spinner[tick % len(spinner)]} {elapsed:5.1f}s", end="", flush=True)
        if elapsed > timeout:
            task.cancel()
            print()
            raise TimeoutError(f"part exceeded {timeout}s")
        tick += 1
        await asyncio.sleep(1)
    print("\r" + " " * 40 + "\r", end="", flush=True)
    await task


def process_exists(pid):
    if pid <= 0:
        return False
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.OpenProcess(0x00100000, False, pid)
    if not handle:
        return False
    kernel32.CloseHandle(handle)
    return True


def acquire_lock():
    if LOCK.exists():
        try:
            old_pid = int(LOCK.read_text(encoding="ascii").strip())
            if process_exists(old_pid):
                return False
            release_lock()
        except ValueError:
            release_lock()
    try:
        fd = os.open(str(LOCK), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode("ascii"))
        os.close(fd)
        return True
    except FileExistsError:
        return False


def release_lock():
    try:
        LOCK.unlink()
    except FileNotFoundError:
        pass


async def process_file(path, cfg, log, file_index, file_total):
    file_start = time.time()
    print(f"\nFile {file_index}/{file_total}: {path.name}", flush=True)
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    text = clean_markdown(raw)
    if not text:
        log.append(f"SKIP empty after cleanup: {path.name}")
        print("  skipped: empty after cleanup", flush=True)
        return

    chunks = split_text(text, int(cfg["chunk_chars"]))
    stem = safe_stem(path)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_dir = OUTBOX / f"{stem}_{stamp}"
    target_dir.mkdir(parents=True, exist_ok=True)

    for index, chunk in enumerate(chunks, start=1):
        output = target_dir / f"{stem}_part_{index:03d}.mp3"
        before = progress_bar(index - 1, len(chunks))
        print(f"  {before} starting part {index}/{len(chunks)}", flush=True)
        log.append(f"TTS {path.name} part {index}/{len(chunks)} -> {output.name}")
        await synthesize_with_spinner(chunk, output, cfg)
        after = progress_bar(index, len(chunks))
        print(f"  {after} wrote {output.name}", flush=True)

    processed_name = f"{path.stem}_{stamp}{path.suffix}"
    shutil.move(str(path), str(PROCESSED / processed_name))
    log.append(f"DONE {path.name}: {len(chunks)} mp3 file(s)")
    elapsed = time.time() - file_start
    print(f"  done in {elapsed:.1f}s -> {target_dir}", flush=True)


async def main():
    for folder in (INBOX, OUTBOX, PROCESSED, LOGS):
        folder.mkdir(parents=True, exist_ok=True)

    if not acquire_lock():
        print("Another TTS run is already active in this folder.", flush=True)
        print(f"Lock file: {LOCK}", flush=True)
        print("Let it finish, or delete the lock only after confirming no run_tts.py is running.", flush=True)
        return

    cfg = load_config()
    allowed = {ext.lower() for ext in cfg["input_extensions"]}
    files = sorted(p for p in INBOX.iterdir() if p.is_file() and p.suffix.lower() in allowed)
    log = [
        f"started={datetime.now().isoformat(timespec='seconds')}",
        f"base={BASE}",
        f"voice={cfg['voice']} rate={cfg['rate']}",
        f"files={len(files)}",
    ]

    print("Starting Edge TTS", flush=True)
    print(f"Voice: {cfg['voice']}", flush=True)
    print(f"Rate:  {cfg['rate']}", flush=True)
    print(f"Files: {len(files)}", flush=True)

    try:
        if not files:
            log.append("No markdown/text files found in inbox.")
            print("\nNo markdown/text files found in inbox.", flush=True)
        for file_index, file_path in enumerate(files, start=1):
            try:
                await process_file(file_path, cfg, log, file_index, len(files))
            except Exception as exc:
                log.append(f"ERROR {file_path.name}: {exc}")
                print(f"  ERROR {file_path.name}: {exc}", flush=True)

        log_path = LOGS / f"tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_path.write_text("\n".join(log) + "\n", encoding="utf-8")
        print(f"\nLog: {log_path}", flush=True)
    finally:
        release_lock()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(130)
