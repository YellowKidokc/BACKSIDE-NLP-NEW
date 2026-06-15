from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


WORKFLOW_ROOT = Path(__file__).resolve().parent.parent
LANE_ROOT = Path(__file__).resolve().parent
EXPORTS_ROOT = WORKFLOW_ROOT / "EXPORTS"
LOOPBACK_DIR = EXPORTS_ROOT / "loopback_review"
STATION_CONFIG = WORKFLOW_ROOT.parent.parent / "stations" / "sbert-embedder.station" / "config.json"

VECTOR_DIM = 384
HTTP_BATCH_SIZE = 32


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "unknown"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")


def load_station_config() -> dict:
    if not STATION_CONFIG.exists():
        return {}
    return load_json(STATION_CONFIG)


def resolve_default_inputs(article: str) -> tuple[Path, Path | None, Path]:
    section_map = WORKFLOW_ROOT / "02_SECTION_MAP" / "sample_output" / article / "section-map.json"
    metadata = WORKFLOW_ROOT / "03_YAML_METADATA" / "sample_output" / article / "metadata.json"
    output_dir = EXPORTS_ROOT / "section_vectors" / article
    return section_map, (metadata if metadata.exists() else None), output_dir


def clean_packet_text(raw: str) -> str:
    lines = []
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            continue
        lines.append(line.rstrip())
    text = "\n".join(lines).strip()
    return re.sub(r"\n{3,}", "\n\n", text)


def synthesize_from_drop(drop_file: Path) -> dict:
    text = drop_file.read_text(encoding="utf-8", errors="replace")
    chunks = [chunk.strip() for chunk in re.split(r"\n\s*\n+", text) if chunk.strip()]
    sections = []
    for index, chunk in enumerate(chunks, start=1):
        first_line = chunk.splitlines()[0].strip().lstrip("# ").strip() or f"Section {index}"
        section_id = f"sec-{index:03d}-{slugify(first_line)}"
        sections.append(
            {
                "ordinal": index,
                "heading_text": first_line,
                "heading_path": [first_line],
                "section_id": section_id,
                "stable_uuid": sha256_text(section_id)[:32],
                "packet_path": None,
                "text_excerpt": chunk[:240],
                "word_count": len(chunk.split()),
                "passes": {"vectors": {"status": "pending"}},
                "_synthetic_text": chunk,
            }
        )
    return {
        "lane_id": "02",
        "lane_name": "Section Map",
        "article_slug": drop_file.stem,
        "paper_uuid": hashlib.sha1(drop_file.as_posix().encode("utf-8")).hexdigest()[:32],
        "source_file": drop_file.as_posix(),
        "generated_at_utc": utc_now(),
        "section_count": len(sections),
        "sections": sections,
        "loopback": {"triggered": True, "reasons": ["Synthetic section map generated because 02 output was missing."]},
    }


def resolve_section_text(section: dict, section_map_path: Path) -> tuple[str, str]:
    if section.get("_synthetic_text"):
        return section["_synthetic_text"], "synthetic"

    packet_path = section.get("packet_path")
    if packet_path:
        packet = section_map_path.parent / packet_path
        if packet.exists():
            return clean_packet_text(packet.read_text(encoding="utf-8", errors="replace")), "packet"

    excerpt = (section.get("text_excerpt") or "").strip()
    if excerpt:
        return excerpt, "excerpt"

    return "", "missing"


def normalize_vector(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return [0.0 for _ in vector]
    return [value / norm for value in vector]


def hash_embedding(text: str, dim: int = VECTOR_DIM) -> list[float]:
    vec = [0.0] * dim
    tokens = re.findall(r"[A-Za-z0-9_]+", text.lower())
    if not tokens:
        return vec
    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dim
        sign = -1.0 if digest[4] % 2 else 1.0
        weight = 1.0 + (len(token) / 24.0)
        vec[index] += sign * weight
    return normalize_vector(vec)


def infinity_embed(texts: list[str], config: dict) -> list[list[float]]:
    base_url = (config.get("infinity_url") or "").rstrip("/")
    model = config.get("model_settings", {}).get("model_name", "sentence-transformers/all-MiniLM-L6-v2")
    if not base_url:
        raise RuntimeError("No infinity_url configured.")

    vectors: list[list[float]] = []
    for start in range(0, len(texts), HTTP_BATCH_SIZE):
        body = json.dumps({"input": texts[start : start + HTTP_BATCH_SIZE], "model": model}).encode("utf-8")
        request = urllib.request.Request(
            f"{base_url}/embeddings",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
        data = sorted(payload.get("data", []), key=lambda item: item.get("index", 0))
        chunk_vectors = [normalize_vector([float(value) for value in item["embedding"]]) for item in data]
        vectors.extend(chunk_vectors)
    if len(vectors) != len(texts):
        raise RuntimeError(f"Expected {len(texts)} embeddings, received {len(vectors)}.")
    dims = {len(vector) for vector in vectors}
    if len(dims) != 1:
        raise RuntimeError(f"Inconsistent embedding dimensions: {sorted(dims)}")
    return vectors


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def top_neighbors(rows: list[dict], limit: int = 3) -> list[dict]:
    pairs: list[tuple[float, str, str]] = []
    for i, left in enumerate(rows):
        for right in rows[i + 1 :]:
            pairs.append((cosine(left["embedding"], right["embedding"]), left["section_id"], right["section_id"]))
    pairs.sort(reverse=True)
    return [
        {"similarity": round(score, 4), "source_section_id": src, "target_section_id": dst}
        for score, src, dst in pairs[:limit]
    ]


def build_loopback(reasons: list[str], article_slug: str, section_map_path: Path, output_dir: Path) -> None:
    if not reasons:
        return
    ensure_dir(LOOPBACK_DIR)
    write_json(
        LOOPBACK_DIR / "08_section_vectors_loopback.json",
        {
            "lane_id": "08",
            "lane_name": "Section Vectors",
            "article_slug": article_slug,
            "generated_at_utc": utc_now(),
            "input_section_map": section_map_path.as_posix(),
            "output_dir": output_dir.as_posix(),
            "reasons": reasons,
        },
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit section vectors for the HTML article workflow.")
    parser.add_argument("--article", help="Named sample article under 02/03 sample_output, e.g. calibration or gtq-03.")
    parser.add_argument("--section-map", help="Explicit path to section-map.json.")
    parser.add_argument("--metadata", help="Explicit path to metadata.json.")
    parser.add_argument("--output-dir", help="Directory for section-vectors.jsonl and vector-metadata.json.")
    parser.add_argument("--prefer-fallback", action="store_true", help="Skip Infinity and emit deterministic hash vectors.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.article:
        section_map_path, metadata_path, output_dir = resolve_default_inputs(args.article)
        article_slug = args.article
    else:
        if not args.section_map:
            print("Need --article or --section-map", file=sys.stderr)
            return 2
        section_map_path = Path(args.section_map)
        metadata_path = Path(args.metadata) if args.metadata else None
        output_dir = Path(args.output_dir) if args.output_dir else LANE_ROOT
        article_slug = section_map_path.parent.name

    synthetic_upstream = False
    loopback_reasons: list[str] = []

    if section_map_path.exists():
        section_map = load_json(section_map_path)
    else:
        drop_dir = WORKFLOW_ROOT / "00_DROP"
        candidate = next(iter(sorted(drop_dir.glob(f"{article_slug}*"))), None)
        if candidate is None:
            print(f"Section map missing and no matching drop file found for {article_slug}.", file=sys.stderr)
            return 2
        section_map = synthesize_from_drop(candidate)
        synthetic_upstream = True
        loopback_reasons.append("02_SECTION_MAP missing; built synthetic section map from 00_DROP.")

    metadata = load_json(metadata_path) if metadata_path and metadata_path.exists() else {}
    ensure_dir(output_dir)

    text_rows = []
    for section in section_map.get("sections", []):
        text, text_source = resolve_section_text(section, section_map_path)
        if not text.strip():
            loopback_reasons.append(f"{section['section_id']} resolved to empty text.")
        text_rows.append(
            {
                "section": section,
                "text": text.strip(),
                "text_source": text_source,
                "text_hash": sha256_text(text.strip()),
            }
        )

    texts = [row["text"] for row in text_rows]
    vector_source = "hash-fallback"
    mocked = synthetic_upstream or args.prefer_fallback

    if args.prefer_fallback:
        vectors = [hash_embedding(text) for text in texts]
    else:
        try:
            vectors = infinity_embed(texts, load_station_config())
            vector_source = "infinity"
        except (RuntimeError, urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            mocked = True
            vector_source = "hash-fallback"
            loopback_reasons.append(f"Infinity embedding unavailable; used deterministic hash fallback. Detail: {exc}")
            vectors = [hash_embedding(text) for text in texts]

    dims = {len(vector) for vector in vectors}
    if len(dims) != 1:
        loopback_reasons.append(f"Inconsistent embedding dimensions detected: {sorted(dims)}")

    if len(texts) > 1 and len({tuple(round(value, 6) for value in vector[:24]) for vector in vectors}) == 1:
        loopback_reasons.append("All section vectors collapsed to the same value.")

    page_id = metadata.get("page_id") or f"page::{section_map.get('paper_uuid', article_slug)}"
    rows = []
    for row, vector in zip(text_rows, vectors):
        section = row["section"]
        norm = math.sqrt(sum(value * value for value in vector))
        rows.append(
            {
                "paper_uuid": metadata.get("paper_uuid") or section_map.get("paper_uuid"),
                "page_id": page_id,
                "section_id": section["section_id"],
                "stable_uuid": section.get("stable_uuid"),
                "ordinal": section.get("ordinal"),
                "heading_path": section.get("heading_path", []),
                "heading_text": section.get("heading_text"),
                "text_hash": row["text_hash"],
                "text_source": row["text_source"],
                "vector_dim": len(vector),
                "vector_source": "mocked-upstream" if synthetic_upstream else vector_source,
                "embedding_norm": round(norm, 6),
                "embedding": [round(value, 6) for value in vector],
                "provenance": {
                    "mocked": bool(mocked),
                    "synthetic_upstream": bool(synthetic_upstream),
                    "generated_at_utc": utc_now(),
                    "lane": "08_SECTION_VECTORS",
                },
            }
        )

    if len(rows) != int(section_map.get("section_count", len(rows))):
        loopback_reasons.append(
            f"Vector row count {len(rows)} does not match section_count {section_map.get('section_count')}."
        )

    write_jsonl(output_dir / "section-vectors.jsonl", rows)
    metadata_payload = {
        "lane_id": "08",
        "lane_name": "Section Vectors",
        "article_slug": article_slug,
        "paper_uuid": metadata.get("paper_uuid") or section_map.get("paper_uuid"),
        "page_id": page_id,
        "title": metadata.get("title") or section_map.get("article_slug"),
        "source_file_name": metadata.get("source_file_name"),
        "generated_at_utc": utc_now(),
        "section_count": len(rows),
        "vector_dim": len(rows[0]["embedding"]) if rows else 0,
        "vector_source": "mocked-upstream" if synthetic_upstream else vector_source,
        "mocked": bool(mocked),
        "synthetic_upstream": bool(synthetic_upstream),
        "top_neighbors": top_neighbors(rows),
        "loopback": {"triggered": bool(loopback_reasons), "reasons": loopback_reasons},
    }
    write_json(output_dir / "vector-metadata.json", metadata_payload)
    build_loopback(loopback_reasons, article_slug, section_map_path, output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
