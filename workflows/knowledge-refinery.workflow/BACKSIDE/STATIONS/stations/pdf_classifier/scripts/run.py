"""
ST-CONV-027 pdf_classifier — run.py

Decide whether a PDF has selectable text (route to pdf_to_md) or is scanned
(route to ocr_scan). Dumb-layer: no reasoning, no LLM. Just sample the first
N pages, count extractable characters per page, threshold.

Output classifications:
  text     — every sampled page has >= MIN_CHARS_PER_PAGE selectable chars
  scanned  — every sampled page has < MIN_CHARS_PER_PAGE chars
  mixed    — some pages have text, others don't (route to OCR for safety)
  empty    — PDF opened but no pages

Usage:
  python run.py --in <path/to/source.pdf> --out <path/to/result.json>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pypdfium2 as pdfium


SAMPLE_PAGES = 5
MIN_CHARS_PER_PAGE = 100


ROUTING = {
    "text":    "ST-CONV-013",   # pdf_to_md (Docling, do_ocr=False)
    "scanned": "ST-CONV-024",   # ocr_scan (Marker)
    "mixed":   "ST-CONV-024",   # ocr_scan handles both layers
    "empty":   "ST-ERR-001",
}


def classify(pdf_path: Path) -> dict:
    pdf = pdfium.PdfDocument(str(pdf_path))
    total_pages = len(pdf)
    if total_pages == 0:
        return {
            "classification": "empty",
            "page_count": 0,
            "sampled_pages": 0,
            "per_page_chars": [],
            "chars_per_page_avg": 0,
            "text_pages": 0,
            "scanned_pages": 0,
        }

    sample_n = min(SAMPLE_PAGES, total_pages)
    per_page_chars = []
    for i in range(sample_n):
        page = pdf[i]
        try:
            tp = page.get_textpage()
            text = tp.get_text_bounded()
            per_page_chars.append(len(text.strip()))
        finally:
            page.close()
    pdf.close()

    text_pages = sum(1 for n in per_page_chars if n >= MIN_CHARS_PER_PAGE)
    scanned_pages = sample_n - text_pages
    avg = sum(per_page_chars) / sample_n if sample_n else 0

    if text_pages == sample_n:
        classification = "text"
    elif text_pages == 0:
        classification = "scanned"
    else:
        classification = "mixed"

    return {
        "classification": classification,
        "page_count": total_pages,
        "sampled_pages": sample_n,
        "per_page_chars": per_page_chars,
        "chars_per_page_avg": round(avg, 2),
        "text_pages": text_pages,
        "scanned_pages": scanned_pages,
    }


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="PDF text-vs-scanned classifier.")
    parser.add_argument("--in", dest="in_path", required=True)
    parser.add_argument("--out", dest="out_path", required=True)
    args = parser.parse_args()

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)
    if not in_path.is_file():
        err = {"status": "error", "error_code": "INPUT_MISSING", "error_msg": f"input file not found: {in_path}"}
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(err, indent=2), encoding="utf-8")
        print(json.dumps(err))
        return 2

    t0 = time.time()
    try:
        result = classify(in_path)
    except Exception as exc:
        err = {
            "status": "error",
            "error_code": "CLASSIFY_FAILED",
            "error_msg": f"{type(exc).__name__}: {exc}",
            "input_path": str(in_path),
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(err, indent=2), encoding="utf-8")
        print(json.dumps(err))
        return 1
    duration_ms = int((time.time() - t0) * 1000)

    classification = result["classification"]
    payload = {
        "status": "ok" if classification != "empty" else "review",
        "station_id": "ST-CONV-027",
        "classification": classification,
        "recommended_next": ROUTING[classification],
        "evidence": {
            "page_count": result["page_count"],
            "sampled_pages": result["sampled_pages"],
            "per_page_chars": result["per_page_chars"],
            "chars_per_page_avg": result["chars_per_page_avg"],
            "text_pages": result["text_pages"],
            "scanned_pages": result["scanned_pages"],
            "threshold_chars_per_page": MIN_CHARS_PER_PAGE,
        },
        "input_path": str(in_path),
        "input_sha256": sha256_of(in_path),
        "duration_ms": duration_ms,
        "ts_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "backend_used": "pypdfium2",
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md_path = out_path.with_suffix(".md")
    md_lines = [
        f"# PDF Classification — {in_path.name}",
        "",
        f"- **classification:** `{classification}`",
        f"- **recommended next station:** `{payload['recommended_next']}`",
        f"- **page_count:** {result['page_count']}",
        f"- **sampled_pages:** {result['sampled_pages']}",
        f"- **chars_per_page_avg:** {result['chars_per_page_avg']}",
        f"- **text_pages / scanned_pages:** {result['text_pages']} / {result['scanned_pages']}",
        f"- **per_page_chars:** {result['per_page_chars']}",
        f"- **duration_ms:** {duration_ms}",
        f"- **input_sha256:** `{payload['input_sha256']}`",
    ]
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(json.dumps({"status": payload["status"], "classification": classification,
                       "recommended_next": payload["recommended_next"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
