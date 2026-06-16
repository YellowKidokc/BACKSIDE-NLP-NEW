import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "input" / "sample_input.md"


def split_sentences(paragraph):
    pieces = re.split(r"(?<=[.!?])\s+", paragraph.strip())
    return [piece for piece in pieces if piece]


def main():
    text = SOURCE.read_text(encoding="utf-8")
    spans = []
    section_id = "SEC-000"
    section_title = ""
    paragraph_index = 0
    trace_number = 1

    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue

        block_start = text.find(block)

        if block.startswith("#"):
            section_id = f"SEC-{trace_number:03d}"
            section_title = block.lstrip("#").strip()
            spans.append({
                "trace_id": f"trace-{trace_number:06d}",
                "trace_scope": "section",
                "section_id": section_id,
                "section_title": section_title,
                "paragraph_index": 0,
                "sentence_index": 0,
                "char_start": block_start,
                "char_end": block_start + len(block),
                "quoted_span": block,
                "trace_status": "anchored",
            })
            trace_number += 1
            continue

        paragraph_index += 1
        for sentence_index, sentence in enumerate(split_sentences(block), start=1):
            char_start = text.find(sentence, block_start)
            spans.append({
                "trace_id": f"trace-{trace_number:06d}",
                "trace_scope": "sentence",
                "section_id": section_id,
                "section_title": section_title,
                "paragraph_index": paragraph_index,
                "sentence_index": sentence_index,
                "char_start": char_start,
                "char_end": char_start + len(sentence),
                "quoted_span": sentence,
                "trace_status": "anchored",
            })
            trace_number += 1

    print(json.dumps({
        "document_id": SOURCE.stem,
        "source_type": "markdown",
        "trace_contract_version": "2026-05-25",
        "spans": spans,
        "warnings": [],
    }, indent=2))


if __name__ == "__main__":
    main()
