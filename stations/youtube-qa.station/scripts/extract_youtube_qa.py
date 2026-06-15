from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pd = None


STATION_ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_EXTENSIONS = {".txt", ".srt", ".vtt", ".md"}
QUESTION_PREFIXES = (
    "who",
    "what",
    "when",
    "where",
    "why",
    "how",
    "is",
    "are",
    "was",
    "were",
    "do",
    "does",
    "did",
    "can",
    "could",
    "would",
    "should",
    "have",
    "has",
    "had",
)
SPEAKER_RE = re.compile(r"^(?P<speaker>[A-Z][A-Za-z0-9 .'-]{1,40}|[A-Z][A-Z0-9 _-]{1,30}):\s+(?P<text>.+)$")
TIMESTAMP_RANGE_RE = re.compile(
    r"(?P<start>\d{2}:\d{2}:\d{2}[.,]\d{3})\s*-->\s*(?P<end>\d{2}:\d{2}:\d{2}[.,]\d{3})"
)
SCRIPTURE_RE = re.compile(
    r"\b(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|1\s*Samuel|2\s*Samuel|1\s*Kings|2\s*Kings|"
    r"1\s*Chronicles|2\s*Chronicles|Ezra|Nehemiah|Esther|Job|Psalms?|Proverbs|Ecclesiastes|Song of Solomon|Isaiah|"
    r"Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|"
    r"Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|1\s*Corinthians|2\s*Corinthians|Galatians|Ephesians|"
    r"Philippians|Colossians|1\s*Thessalonians|2\s*Thessalonians|1\s*Timothy|2\s*Timothy|Titus|Philemon|Hebrews|"
    r"James|1\s*Peter|2\s*Peter|1\s*John|2\s*John|3\s*John|Jude|Revelation)\s+\d{1,3}:\d{1,3}(?:-\d{1,3})?\b",
    re.IGNORECASE,
)
TOPIC_KEYWORDS = {
    "resurrection": ["resurrection", "risen", "empty tomb", "raised from the dead"],
    "bible_reliability": ["manuscript", "canon", "textual", "bible", "scripture", "copyist"],
    "god_exists": ["god exist", "creator", "first cause", "fine-tuning", "design"],
    "morality": ["moral", "ethics", "evil", "suffering", "justice"],
    "jesus_identity": ["jesus", "messiah", "son of god", "divinity"],
    "atheism_objection": ["atheist", "atheism", "skeptic", "skeptical", "unbeliever"],
    "science_faith": ["science", "scientific", "physics", "evidence", "experiment"],
    "church_history": ["church", "apostle", "creed", "council", "martyr"],
}
OBJECTION_PATTERNS = {
    "problem_of_evil": ["why does god allow", "problem of evil", "why do people suffer", "evil and suffering"],
    "bible_reliability": ["can we trust the bible", "is the bible reliable", "copies of copies"],
    "resurrection_skepticism": ["did jesus really rise", "hallucination", "stolen body", "empty tomb"],
    "science_vs_faith": ["science disproves", "against science", "contradict science"],
    "moral_objection": ["isn't that immoral", "unfair", "cruel", "genocide", "drowned everybody"],
}
EVIDENCE_PATTERNS = [
    re.compile(r"\b(?:according to|as reported by|historians say|archaeology shows|manuscript evidence)\b", re.IGNORECASE),
    re.compile(r"\b\d{4}\b"),
    re.compile(r"\b(?:study|studies|experiment|evidence|data|artifact|manuscript|source|witness|historian|journal)\b", re.IGNORECASE),
]
CLAIM_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract question/answer cards from transcript files.")
    parser.add_argument("input_path", type=Path, help="Transcript file or folder of transcript files.")
    parser.add_argument("--metadata-json", type=Path, help="Optional metadata JSON file or folder.")
    parser.add_argument(
        "--workflow-root",
        type=Path,
        default=STATION_ROOT,
        help="Station root containing 02_QA_JSON, 03_QA_MARKDOWN, 04_QA_EXCEL, and 05_SNAPSHOTS.",
    )
    parser.add_argument("--xlsx", action="store_true", help="Also write .xlsx when pandas/openpyxl are available.")
    parser.add_argument(
        "--snapshot-partial",
        action="store_true",
        help="Also emit a .paper-snapshot.partial.json file compatible with the snapshot lane.",
    )
    return parser.parse_args()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "transcript"


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def clean_subtitle_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&nbsp;", " ")
    text = re.sub(r"\{\\an\d+\}", " ", text)
    return normalize_whitespace(text)


def standardize_timestamp(raw: str | None) -> str:
    if not raw:
        return ""
    return raw.replace(",", ".")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_metadata(path: Path | None, transcript_path: Path) -> dict[str, Any]:
    if path is None:
        return {}
    if path.is_file():
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and any(key in data for key in ("video_title", "youtube_url", "channel")):
            return data
        if isinstance(data, dict):
            stem = transcript_path.stem
            return data.get(stem) or data.get(transcript_path.name) or {}
        return {}
    candidates = [
        path / f"{transcript_path.stem}.json",
        path / f"{transcript_path.name}.json",
        path / "metadata.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            data = json.loads(candidate.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
    return {}


def iter_transcript_paths(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    return sorted(
        path
        for path in input_path.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def split_same_line_question(block: dict[str, Any]) -> list[dict[str, Any]]:
    text = block["text"]
    question_mark = text.find("?")
    if question_mark == -1 or question_mark == len(text) - 1:
        return [block]
    question = normalize_whitespace(text[: question_mark + 1])
    rest = normalize_whitespace(text[question_mark + 1 :])
    if not question or not rest:
        return [block]
    first = dict(block)
    first["text"] = question
    second = dict(block)
    second["text"] = rest
    return [first, second]


def parse_vtt_or_srt(text: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    raw_chunks = re.split(r"\n\s*\n", text.replace("\r\n", "\n"))
    for chunk in raw_chunks:
        lines = [line.strip("\ufeff") for line in chunk.splitlines() if line.strip()]
        if not lines:
            continue
        if lines[0].upper() == "WEBVTT":
            continue
        if lines[0].isdigit():
            lines = lines[1:]
        if not lines:
            continue
        match = TIMESTAMP_RANGE_RE.search(lines[0])
        if not match:
            continue
        payload = clean_subtitle_text(" ".join(lines[1:]))
        if not payload:
            continue
        speaker = ""
        speaker_match = SPEAKER_RE.match(payload)
        if speaker_match:
            speaker = normalize_whitespace(speaker_match.group("speaker"))
            payload = normalize_whitespace(speaker_match.group("text"))
        block = {
            "start": standardize_timestamp(match.group("start")),
            "end": standardize_timestamp(match.group("end")),
            "speaker": speaker,
            "text": payload,
        }
        blocks.extend(split_same_line_question(block))
    return merge_adjacent_blocks(blocks)


def parse_plain_text(text: str) -> list[dict[str, Any]]:
    normalized = text.replace("\r\n", "\n")
    paragraphs = [normalize_whitespace(chunk) for chunk in re.split(r"\n\s*\n", normalized) if normalize_whitespace(chunk)]
    if len(paragraphs) <= 1:
        paragraphs = [
            normalize_whitespace(line)
            for line in normalized.splitlines()
            if normalize_whitespace(line) and not line.strip().startswith("#")
        ]
    blocks: list[dict[str, Any]] = []
    for paragraph in paragraphs:
        speaker = ""
        payload = paragraph
        speaker_match = SPEAKER_RE.match(paragraph)
        if speaker_match:
            speaker = normalize_whitespace(speaker_match.group("speaker"))
            payload = normalize_whitespace(speaker_match.group("text"))
        block = {"start": "", "end": "", "speaker": speaker, "text": payload}
        blocks.extend(split_same_line_question(block))
    return merge_adjacent_blocks(blocks)


def merge_adjacent_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for block in blocks:
        if not block["text"]:
            continue
        if merged:
            prev = merged[-1]
            same_speaker = prev.get("speaker") == block.get("speaker")
            both_not_questions = not is_question_text(prev["text"]) and not is_question_text(block["text"])
            short_prev = len(prev["text"]) < 120
            if same_speaker and both_not_questions and short_prev:
                prev["text"] = normalize_whitespace(prev["text"] + " " + block["text"])
                if block.get("end"):
                    prev["end"] = block["end"]
                continue
        merged.append(dict(block))
    return merged


def parse_transcript(path: Path) -> tuple[str, list[dict[str, Any]]]:
    raw = read_text(path)
    suffix = path.suffix.lower()
    if suffix in {".vtt", ".srt"}:
        blocks = parse_vtt_or_srt(raw)
    else:
        blocks = parse_plain_text(raw)
    return raw, blocks


def is_question_text(text: str) -> bool:
    normalized = normalize_whitespace(text)
    if not normalized:
        return False
    if "?" in normalized:
        return True
    lowered = normalized.lower()
    if lowered.startswith(QUESTION_PREFIXES):
        return len(normalized.split()) <= 30 or lowered.startswith(("why ", "how ", "what ", "who ", "is ", "are "))
    return False


def detect_rhetorical(question: str) -> bool:
    lowered = question.lower()
    return any(
        marker in lowered
        for marker in (
            "isn't it obvious",
            "isn't that obvious",
            "who could deny",
            "wouldn't you agree",
            "doesn't that show",
            "of course",
        )
    )


def detect_topic_tags(*texts: str) -> list[str]:
    haystack = " ".join(texts).lower()
    tags = [tag for tag, keywords in TOPIC_KEYWORDS.items() if any(keyword in haystack for keyword in keywords)]
    return sorted(set(tags))


def detect_objection_type(question: str, answer: str) -> str:
    haystack = f"{question} {answer}".lower()
    for objection_type, patterns in OBJECTION_PATTERNS.items():
        if any(pattern in haystack for pattern in patterns):
            return objection_type
    if any(word in haystack for word in ("objection", "skeptic", "critic", "doubt", "challenge")):
        return "general_skepticism"
    return ""


def find_scripture_refs(*texts: str) -> list[str]:
    refs: list[str] = []
    seen: set[str] = set()
    for text in texts:
        for match in SCRIPTURE_RE.finditer(text):
            value = normalize_whitespace(match.group(0))
            key = value.lower()
            if key not in seen:
                seen.add(key)
                refs.append(value)
    return refs


def find_evidence_refs(*texts: str) -> list[str]:
    refs: list[str] = []
    seen: set[str] = set()
    for text in texts:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        for sentence in sentences:
            if any(pattern.search(sentence) for pattern in EVIDENCE_PATTERNS):
                value = normalize_whitespace(sentence)
                key = value.lower()
                if key not in seen and value:
                    seen.add(key)
                    refs.append(value)
    return refs[:6]


def infer_claims(answer: str, question: str, qa_id: str) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    if not answer:
        return claims
    sentences = [normalize_whitespace(s) for s in CLAIM_SENTENCE_RE.split(answer) if normalize_whitespace(s)]
    claim_index = 1
    for sentence in sentences:
        lowered = sentence.lower()
        if len(sentence.split()) < 5:
            continue
        if not any(
            token in lowered
            for token in (
                " is ",
                " are ",
                " shows ",
                " means ",
                " demonstrates ",
                " proves ",
                " indicates ",
                " because ",
                " therefore ",
                " can ",
                " did ",
                " was ",
            )
        ):
            continue
        claims.append(
            {
                "claim_id": f"{qa_id}-claim-{claim_index:02d}",
                "text": sentence,
                "source_qa_id": qa_id,
                "question_context": question,
            }
        )
        claim_index += 1
        if claim_index > 3:
            break
    return claims


def response_quality_notes(answer: str, evidence_refs: list[str], scripture_refs: list[str], answer_type: str) -> list[str]:
    notes: list[str] = []
    if not answer:
        notes.append("No explicit answer was detected in the nearby transcript window.")
    if answer_type == "implied":
        notes.append("Answer appears implied from nearby statements rather than directly stated.")
    if answer_type == "rhetorical":
        notes.append("Question appears rhetorical, so the answer was not treated as a normal direct response.")
    if evidence_refs:
        notes.append("Response cites or gestures toward evidence-bearing material.")
    else:
        notes.append("Response quality is weaker because no clear evidence reference was detected.")
    if scripture_refs:
        notes.append("Response includes scripture references.")
    return notes


def confidence_score(question: str, answer: str, explicit_question: bool, answer_type: str, speaker_question: str, speaker_answer: str) -> float:
    score = 0.45
    if explicit_question:
        score += 0.2
    if answer:
        score += 0.15
    if answer_type == "explicit":
        score += 0.1
    if answer_type == "implied":
        score -= 0.05
    if answer_type == "rhetorical":
        score -= 0.1
    if speaker_question and speaker_answer and speaker_question != speaker_answer:
        score += 0.05
    if len(question.split()) > 20:
        score -= 0.05
    return round(max(0.1, min(score, 0.98)), 2)


def build_reusable_card(question: str, answer: str, tags: list[str], objection_type: str) -> dict[str, Any]:
    return {
        "front": question,
        "back": answer,
        "tagline": tags[0] if tags else objection_type or "qa",
        "card_type": "youtube_qa",
    }


def collect_answer(blocks: list[dict[str, Any]], question_index: int) -> tuple[str, str, str, str]:
    question_block = blocks[question_index]
    fragments: list[str] = []
    answer_speaker = ""
    timestamp_start = question_block.get("start", "")
    timestamp_end = question_block.get("end", "")
    if question_index + 1 >= len(blocks):
        return "", answer_speaker, timestamp_start, timestamp_end
    for offset in range(1, 7):
        idx = question_index + offset
        if idx >= len(blocks):
            break
        block = blocks[idx]
        text = block["text"]
        if is_question_text(text):
            if not fragments:
                return "", answer_speaker, timestamp_start, timestamp_end
            break
        fragments.append(text)
        if not answer_speaker and block.get("speaker"):
            answer_speaker = block["speaker"]
        if block.get("end"):
            timestamp_end = block["end"]
        if sum(len(fragment) for fragment in fragments) >= 700:
            break
    return normalize_whitespace(" ".join(fragments)), answer_speaker, timestamp_start, timestamp_end


def build_qa_pairs(blocks: list[dict[str, Any]], source_slug: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    qa_pairs: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    objections: list[dict[str, Any]] = []
    qa_index = 1
    for idx, block in enumerate(blocks):
        question = block["text"]
        explicit_question = "?" in question
        if not is_question_text(question):
            continue
        answer, answer_speaker, timestamp_start, timestamp_end = collect_answer(blocks, idx)
        rhetorical = detect_rhetorical(question)
        answer_type = "rhetorical" if rhetorical else "explicit"
        if not answer and not rhetorical:
            answer_type = "unanswered"
        elif answer and not explicit_question:
            answer_type = "implied"
        tags = detect_topic_tags(question, answer)
        objection_type = detect_objection_type(question, answer)
        evidence_refs = find_evidence_refs(question, answer)
        scripture_refs = find_scripture_refs(question, answer)
        qa_id = f"{source_slug}-qa-{qa_index:03d}"
        qa_claims = infer_claims(answer, question, qa_id)
        claims.extend(qa_claims)
        qa_pair = {
            "qa_id": qa_id,
            "question": question,
            "answer": answer,
            "speaker_question": block.get("speaker", ""),
            "speaker_answer": answer_speaker,
            "timestamp_start": timestamp_start,
            "timestamp_end": timestamp_end,
            "topic_tags": tags,
            "claim_ids": [claim["claim_id"] for claim in qa_claims],
            "evidence_refs": evidence_refs,
            "scripture_refs": scripture_refs,
            "objection_type": objection_type,
            "answer_type": answer_type,
            "confidence": confidence_score(
                question=question,
                answer=answer,
                explicit_question=explicit_question,
                answer_type=answer_type,
                speaker_question=block.get("speaker", ""),
                speaker_answer=answer_speaker,
            ),
            "response_quality_notes": response_quality_notes(answer, evidence_refs, scripture_refs, answer_type),
            "reusable_card": build_reusable_card(question, answer, tags, objection_type),
        }
        qa_pairs.append(qa_pair)
        if objection_type:
            objections.append(
                {
                    "qa_id": qa_id,
                    "objection_type": objection_type,
                    "question": question,
                    "response_present": bool(answer),
                }
            )
        qa_index += 1
    return qa_pairs, claims, objections


def dedupe_list(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        key = value.lower()
        if key not in seen and value:
            seen.add(key)
            ordered.append(value)
    return ordered


def build_json_payload(transcript_path: Path, metadata: dict[str, Any], raw_text: str, qa_pairs: list[dict[str, Any]], claims: list[dict[str, Any]], objections: list[dict[str, Any]]) -> dict[str, Any]:
    content_hash = sha256_text(raw_text)
    all_scripture_refs = dedupe_list([ref for qa in qa_pairs for ref in qa.get("scripture_refs", [])])
    all_topic_tags = dedupe_list([tag for qa in qa_pairs for tag in qa.get("topic_tags", [])])
    return {
        "source": {
            "video_title": metadata.get("video_title", transcript_path.stem),
            "youtube_url": metadata.get("youtube_url", ""),
            "channel": metadata.get("channel", ""),
            "transcript_path": str(transcript_path),
            "content_hash": content_hash,
            "created_at": iso_now(),
        },
        "qa_pairs": qa_pairs,
        "claims": claims,
        "objections": objections,
        "scripture_refs": all_scripture_refs,
        "topic_tags": all_topic_tags,
        "station_marks": {
            "youtube_qa_extractor": "complete",
        },
    }


def build_snapshot_partial(payload: dict[str, Any]) -> dict[str, Any]:
    source = payload["source"]
    qa_pairs = payload["qa_pairs"]
    claims = payload["claims"]
    return {
        "schema_version": "paper_snapshot.partial.youtube_qa.v1",
        "source_id": slugify(source["video_title"]),
        "source_path": source["transcript_path"],
        "title": source["video_title"],
        "source": source,
        "claims": [
            {
                "claim_id": claim["claim_id"],
                "text": claim["text"],
                "source_qa_id": claim["source_qa_id"],
                "claim_type": "video_qa_claim",
            }
            for claim in claims
        ],
        "classifier_tags": payload["topic_tags"],
        "graph_tags": payload["topic_tags"],
        "evidence_refs": dedupe_list([ref for qa in qa_pairs for ref in qa.get("evidence_refs", [])]),
        "scripture_refs": payload["scripture_refs"],
        "qa_cards": [
            {
                "qa_id": qa["qa_id"],
                "question": qa["question"],
                "answer": qa["answer"],
                "topic_tags": qa["topic_tags"],
                "objection_type": qa["objection_type"],
                "confidence": qa["confidence"],
            }
            for qa in qa_pairs
        ],
        "station_marks": {
            "youtube_qa_extractor": "complete",
        },
    }


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    source = payload["source"]
    lines = [
        f"# {source['video_title']} - YouTube Q/A Extraction",
        "",
        f"- Channel: {source['channel'] or 'unknown'}",
        f"- Source URL: {source['youtube_url'] or 'n/a'}",
        f"- Transcript: `{source['transcript_path']}`",
        f"- Content hash: `{source['content_hash']}`",
        "",
        "## Topic Tags",
        "",
        ", ".join(payload["topic_tags"]) if payload["topic_tags"] else "_none detected_",
        "",
        "## Q/A Cards",
        "",
    ]
    for qa in payload["qa_pairs"]:
        lines.extend(
            [
                f"### {qa['qa_id']}",
                "",
                f"**Question:** {qa['question']}",
                "",
                f"**Answer:** {qa['answer'] or '_no explicit answer found_'}",
                "",
                f"**Speakers:** Q=`{qa['speaker_question'] or 'unknown'}` A=`{qa['speaker_answer'] or 'unknown'}`",
                "",
                f"**Timestamps:** `{qa['timestamp_start'] or 'n/a'}` -> `{qa['timestamp_end'] or 'n/a'}`",
                "",
                f"**Tags:** {', '.join(qa['topic_tags']) if qa['topic_tags'] else '_none_'}",
                "",
                f"**Objection type:** `{qa['objection_type'] or 'none'}`",
                "",
                f"**Answer type:** `{qa['answer_type']}` | **Confidence:** `{qa['confidence']}`",
                "",
                f"**Evidence refs:** {json.dumps(qa['evidence_refs'], ensure_ascii=False)}",
                "",
                f"**Scripture refs:** {json.dumps(qa['scripture_refs'], ensure_ascii=False)}",
                "",
                "**Response quality notes:**",
                "",
            ]
        )
        for note in qa["response_quality_notes"]:
            lines.append(f"- {note}")
        lines.extend(["", "**Reusable card:**", "", f"- Front: {qa['reusable_card']['front']}", f"- Back: {qa['reusable_card']['back'] or '_blank_'}", ""])
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def write_csv(path: Path, payload: dict[str, Any]) -> None:
    fieldnames = [
        "qa_id",
        "question",
        "answer",
        "speaker_question",
        "speaker_answer",
        "timestamp_start",
        "timestamp_end",
        "topic_tags",
        "claim_ids",
        "evidence_refs",
        "scripture_refs",
        "objection_type",
        "answer_type",
        "confidence",
        "response_quality_notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for qa in payload["qa_pairs"]:
            writer.writerow(
                {
                    "qa_id": qa["qa_id"],
                    "question": qa["question"],
                    "answer": qa["answer"],
                    "speaker_question": qa["speaker_question"],
                    "speaker_answer": qa["speaker_answer"],
                    "timestamp_start": qa["timestamp_start"],
                    "timestamp_end": qa["timestamp_end"],
                    "topic_tags": "; ".join(qa["topic_tags"]),
                    "claim_ids": "; ".join(qa["claim_ids"]),
                    "evidence_refs": "; ".join(qa["evidence_refs"]),
                    "scripture_refs": "; ".join(qa["scripture_refs"]),
                    "objection_type": qa["objection_type"],
                    "answer_type": qa["answer_type"],
                    "confidence": qa["confidence"],
                    "response_quality_notes": " | ".join(qa["response_quality_notes"]),
                }
            )


def write_xlsx(path: Path, payload: dict[str, Any]) -> bool:
    if pd is None:
        return False
    qa_rows = []
    for qa in payload["qa_pairs"]:
        qa_rows.append(
            {
                "qa_id": qa["qa_id"],
                "question": qa["question"],
                "answer": qa["answer"],
                "speaker_question": qa["speaker_question"],
                "speaker_answer": qa["speaker_answer"],
                "timestamp_start": qa["timestamp_start"],
                "timestamp_end": qa["timestamp_end"],
                "topic_tags": "; ".join(qa["topic_tags"]),
                "claim_ids": "; ".join(qa["claim_ids"]),
                "evidence_refs": "; ".join(qa["evidence_refs"]),
                "scripture_refs": "; ".join(qa["scripture_refs"]),
                "objection_type": qa["objection_type"],
                "answer_type": qa["answer_type"],
                "confidence": qa["confidence"],
            }
        )
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        pd.DataFrame(qa_rows).to_excel(writer, index=False, sheet_name="qa_pairs")
        pd.DataFrame(payload["claims"]).to_excel(writer, index=False, sheet_name="claims")
        pd.DataFrame(payload["objections"]).to_excel(writer, index=False, sheet_name="objections")
    return True


def ensure_dirs(workflow_root: Path) -> dict[str, Path]:
    mapping = {
        "json": workflow_root / "02_QA_JSON",
        "markdown": workflow_root / "03_QA_MARKDOWN",
        "excel": workflow_root / "04_QA_EXCEL",
        "snapshots": workflow_root / "05_SNAPSHOTS",
    }
    for path in mapping.values():
        path.mkdir(parents=True, exist_ok=True)
    return mapping


def process_transcript(transcript_path: Path, metadata_path: Path | None, workflow_root: Path, want_xlsx: bool, want_snapshot_partial: bool) -> dict[str, Any]:
    metadata = load_metadata(metadata_path, transcript_path)
    raw_text, blocks = parse_transcript(transcript_path)
    source_slug = slugify(metadata.get("video_title", transcript_path.stem))
    qa_pairs, claims, objections = build_qa_pairs(blocks, source_slug)
    payload = build_json_payload(transcript_path, metadata, raw_text, qa_pairs, claims, objections)

    dirs = ensure_dirs(workflow_root)
    json_path = dirs["json"] / f"{source_slug}.qa.json"
    md_path = dirs["markdown"] / f"{source_slug}.qa.md"
    csv_path = dirs["excel"] / f"{source_slug}.qa.csv"
    xlsx_path = dirs["excel"] / f"{source_slug}.qa.xlsx"
    snapshot_path = dirs["snapshots"] / f"{source_slug}.paper-snapshot.partial.json"

    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(md_path, payload)
    write_csv(csv_path, payload)
    xlsx_written = want_xlsx and write_xlsx(xlsx_path, payload)

    snapshot_written = False
    if want_snapshot_partial:
        snapshot_path.write_text(json.dumps(build_snapshot_partial(payload), ensure_ascii=False, indent=2), encoding="utf-8")
        snapshot_written = True

    return {
        "transcript": str(transcript_path),
        "qa_pairs": len(qa_pairs),
        "claims": len(claims),
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "csv_path": str(csv_path),
        "xlsx_path": str(xlsx_path) if xlsx_written else "",
        "snapshot_partial_path": str(snapshot_path) if snapshot_written else "",
    }


def main() -> int:
    args = parse_args()
    inputs = iter_transcript_paths(args.input_path)
    if not inputs:
        print(json.dumps({"error": "No transcript files found.", "input_path": str(args.input_path)}, indent=2))
        return 1

    results = [
        process_transcript(
            transcript_path=path,
            metadata_path=args.metadata_json,
            workflow_root=args.workflow_root,
            want_xlsx=args.xlsx,
            want_snapshot_partial=args.snapshot_partial,
        )
        for path in inputs
    ]
    print(json.dumps({"processed": len(results), "results": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
