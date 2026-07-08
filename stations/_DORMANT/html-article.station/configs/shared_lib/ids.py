from __future__ import annotations

import hashlib
import re
import uuid
from pathlib import Path


NAMESPACE = uuid.UUID("28282828-0000-0000-0000-000000000001")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def slugify(value: str, fallback: str = "x") -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or fallback


def stable_uuid(kind: str, *parts: str) -> str:
    raw = "::".join([kind, *[str(part) for part in parts]])
    return str(uuid.uuid5(NAMESPACE, raw))


def short_hash(*parts: str, length: int = 16) -> str:
    return sha256_text("::".join(parts))[:length]


def file_doc_id(path: Path, content_hash: str) -> str:
    return stable_uuid("doc", str(path).lower(), content_hash[:16])
