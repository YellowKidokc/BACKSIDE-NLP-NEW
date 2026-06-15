"""
02_SBERT — embeddings via Infinity service + storage in Qdrant.

Architecture (post-Cannon refactor, 2026-05-02):
  - Embeddings: HTTP POST to Infinity at infinity_url (canonical model is
    sentence-transformers/all-MiniLM-L6-v2, dim=384, hardcoded into the
    NAS Brain deploy).
  - Storage: Qdrant point upsert into the collection named after the
    source table. Postgres is NOT touched for vectors anymore (DeBERTa
    labels and cluster IDs still live in Postgres — those are scalars
    and belong there).

Two source modes (set in config.json):

  source.type = "postgres":
      Streams rows from `source.table`, skips IDs already present in the
      Qdrant collection, embeds the concatenation of `source.text_cols`
      via Infinity, upserts (id, vector, payload) into Qdrant. The
      collection is created on first run if missing. Resume is automatic:
      kill the process and re-run; the existing-IDs scan picks up where
      it left off.

  source.type = "files":
      Embeds every text file under `files_source.input_dir` via Infinity
      and writes embeddings.npz to `files_source.output_dir`.

Library mode:
  import sbert_runner
  client = sbert_runner.InfinityClient(...)
  vecs = client.embed([...])

Self-test:   --self-test  hits Infinity with three sentences (two near-
             duplicates, one unrelated) and asserts the cosine of the
             duplicates is meaningfully higher than the cosine to the
             unrelated.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOG_DIR = ROOT / "_LOGS"
PG_DIR = ROOT / "07_POSTGRES"

if str(PG_DIR) not in sys.path:
    sys.path.insert(0, str(PG_DIR))


# ── Logging ─────────────────────────────────────────────────────────────────

def _setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    logfile = LOG_DIR / f"sbert_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger("sbert")
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


def _load_config() -> dict:
    return json.loads((HERE / "config.json").read_text(encoding="utf-8"))


# ── Infinity HTTP client ────────────────────────────────────────────────────

class InfinityClient:
    """Thin client for Infinity's OpenAI-compatible /embeddings endpoint."""

    def __init__(
        self,
        base_url: str,
        model: str = "sentence-transformers/all-MiniLM-L6-v2",
        timeout: float = 60.0,
        http_batch_size: int = 32,
    ):
        import httpx

        self.base_url = base_url.rstrip("/")
        self.model = model
        self.http_batch_size = http_batch_size
        self.client = httpx.Client(base_url=self.base_url, timeout=timeout)
        # Probe dim by embedding a one-token string.
        probe = self._post([""])
        self.dim = len(probe[0])

    def close(self):
        try:
            self.client.close()
        except Exception:
            pass

    def _post(self, texts: list[str]) -> list[list[float]]:
        body = {"input": [t or "" for t in texts], "model": self.model}
        resp = self.client.post("/embeddings", json=body)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        # Sort by index just in case the server returns them out of order.
        data = sorted(data, key=lambda d: d.get("index", 0))
        return [d["embedding"] for d in data]

    def embed(self, texts: list[str], normalize: bool = True) -> np.ndarray:
        if not texts:
            return np.zeros((0, self.dim or 0), dtype=np.float32)
        all_vecs: list[list[float]] = []
        for i in range(0, len(texts), self.http_batch_size):
            chunk = texts[i : i + self.http_batch_size]
            all_vecs.extend(self._post(chunk))
        arr = np.asarray(all_vecs, dtype=np.float32)
        if normalize and arr.size:
            norms = np.linalg.norm(arr, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            arr = arr / norms
        return arr


# ── Qdrant helpers ──────────────────────────────────────────────────────────

def _qdrant_client(url: str, timeout: float = 60.0):
    from qdrant_client import QdrantClient
    return QdrantClient(url=url, timeout=timeout)


def ensure_collection(client, name: str, dim: int, distance: str = "cosine") -> None:
    from qdrant_client.http.models import Distance, VectorParams

    distance_map = {
        "cosine": Distance.COSINE,
        "dot": Distance.DOT,
        "euclid": Distance.EUCLID,
        "manhattan": Distance.MANHATTAN,
    }
    dist = distance_map[distance.lower()]
    existing = {c.name for c in client.get_collections().collections}
    if name in existing:
        return
    client.create_collection(
        collection_name=name,
        vectors_config=VectorParams(size=dim, distance=dist),
    )


def existing_point_ids(client, collection: str) -> set:
    """Scroll the collection and return the set of all point IDs."""
    ids: set = set()
    next_page = None
    while True:
        points, next_page = client.scroll(
            collection_name=collection,
            limit=2048,
            with_payload=False,
            with_vectors=False,
            offset=next_page,
        )
        for p in points:
            ids.add(p.id)
        if next_page is None:
            break
    return ids


# ── Postgres row streaming ──────────────────────────────────────────────────

def stream_rows(db, table: str, id_col: str, select_cols: list[str],
                where: str | None, batch_size: int):
    """Yield rows ordered by id_col, batched, with optional WHERE filter.
    Resume tracking is done by the caller via the Qdrant exclusion set —
    we don't filter on a NULL column here."""
    cols = ", ".join([id_col] + [c for c in select_cols if c != id_col])
    last_id = 0
    while True:
        clause = f"{id_col} > %s"
        if where:
            clause = f"({where}) AND {clause}"
        sql = f"SELECT {cols} FROM {table} WHERE {clause} ORDER BY {id_col} LIMIT %s"
        rows = db.query(sql, (last_id, batch_size))
        if not rows:
            return
        last_id = rows[-1][id_col]
        yield rows


# ── Self-test ───────────────────────────────────────────────────────────────

def _self_test(log: logging.Logger) -> int:
    cfg = _load_config()
    base = cfg["infinity_url"]
    model = cfg.get("model_settings", {}).get("model_name", "sentence-transformers/all-MiniLM-L6-v2")
    log.info("self-test: hitting Infinity at %s with model %s", base, model)
    try:
        em = InfinityClient(base_url=base, model=model)
    except Exception as e:
        log.error("Infinity reachable check failed: %s", e)
        return 2
    a = "Did Jesus rise from the dead?"
    b = "What is the evidence for the resurrection of Christ?"
    c = "How do I bake sourdough bread?"
    vecs = em.embed([a, b, c], normalize=True)
    sim_ab = float(np.dot(vecs[0], vecs[1]))
    sim_ac = float(np.dot(vecs[0], vecs[2]))
    log.info("dim=%d  sim(a,b)=%.3f  sim(a,c)=%.3f", em.dim, sim_ab, sim_ac)
    em.close()
    if sim_ab > 0.5 and sim_ab > sim_ac + 0.1:
        log.info("self-test OK")
        return 0
    log.error("self-test FAILED: similarities look wrong (need ab>0.5 and ab>ac+0.1)")
    return 3


# ── Postgres-to-Qdrant pipeline ─────────────────────────────────────────────

def _join_text_cols(row: dict, cols: list[str], max_chars: int = 0) -> str:
    parts: list[str] = []
    for c in cols:
        v = row.get(c)
        if v is None:
            continue
        s = str(v).strip()
        if s:
            parts.append(s)
    text = "\n".join(parts)
    if max_chars > 0 and len(text) > max_chars:
        text = text[:max_chars]
    return text


def _run_postgres(cfg: dict, log: logging.Logger) -> int:
    from db_utils import Database
    from qdrant_client.http.models import PointStruct

    src = cfg["source"]
    table = src["table"]
    id_col = src.get("id_col", "id")
    text_cols = src["text_cols"]
    where = src.get("where")
    payload_cols = src.get("payload_cols") or text_cols
    text_preview_chars = int(src.get("text_preview_chars", 300))

    collection = cfg.get("qdrant_collection") or table
    distance = cfg.get("vector_distance", "cosine")
    batch_size = int(cfg.get("model_settings", {}).get("batch_size", 100))

    em = InfinityClient(
        base_url=cfg["infinity_url"],
        model=cfg.get("model_settings", {}).get("model_name", "sentence-transformers/all-MiniLM-L6-v2"),
        http_batch_size=int(cfg.get("model_settings", {}).get("http_batch_size", 32)),
    )
    log.info("Infinity ready: model=%s dim=%d", em.model, em.dim)

    qd = _qdrant_client(cfg["qdrant_url"])
    ensure_collection(qd, collection, em.dim, distance)
    log.info("Qdrant collection ready: %s (dim=%d, distance=%s)", collection, em.dim, distance)

    log.info("loading existing point IDs from %s ...", collection)
    already = existing_point_ids(qd, collection)
    log.info("collection has %d existing points", len(already))

    select_cols = [id_col] + list(set(list(text_cols) + list(payload_cols)))
    total_done = 0
    total_skipped = 0
    total_failed = 0

    with Database(application_name="sbert_runner") as db:
        try:
            remaining = db.query(f"SELECT COUNT(*) AS c FROM {table}")[0]["c"]
            log.info("source rows in %s: %d", table, remaining)
        except Exception as e:
            log.exception("source count failed: %s", e)
            em.close()
            return 1

        for batch in stream_rows(db, table, id_col, select_cols, where, batch_size):
            # Filter out IDs already in Qdrant.
            new_rows = [r for r in batch if r[id_col] not in already]
            total_skipped += len(batch) - len(new_rows)
            if not new_rows:
                continue

            ids = [r[id_col] for r in new_rows]
            texts = [_join_text_cols(r, text_cols) for r in new_rows]

            try:
                vecs = em.embed(texts, normalize=True)
            except Exception as e:
                log.exception("batch embed failed (size=%d): %s — falling back row-by-row", len(texts), e)
                vecs_list: list[np.ndarray | None] = []
                for t in texts:
                    try:
                        vecs_list.append(em.embed([t], normalize=True)[0])
                    except Exception as ee:
                        log.error("row embed failed: %s", ee)
                        vecs_list.append(None)
                vecs = None
                points: list[PointStruct] = []
                for idv, row, v in zip(ids, new_rows, vecs_list):
                    if v is None:
                        total_failed += 1
                        continue
                    points.append(_make_point(idv, row, v, table, payload_cols, text_preview_chars))
            else:
                points = [
                    _make_point(idv, row, vecs[i], table, payload_cols, text_preview_chars)
                    for i, (idv, row) in enumerate(zip(ids, new_rows))
                ]

            if not points:
                continue

            try:
                qd.upsert(collection_name=collection, points=points, wait=True)
                already.update(p.id for p in points)
                total_done += len(points)
                log.info("[+%d] upserted. embedded=%d skipped=%d failed=%d",
                         len(points), total_done, total_skipped, total_failed)
            except Exception as e:
                log.exception("Qdrant upsert failed (size=%d): %s — retrying one-by-one", len(points), e)
                for p in points:
                    try:
                        qd.upsert(collection_name=collection, points=[p], wait=True)
                        already.add(p.id)
                        total_done += 1
                    except Exception as ee:
                        log.error("single upsert failed for id=%s: %s", p.id, ee)
                        total_failed += 1

    em.close()
    log.info("postgres run complete. embedded=%d skipped=%d failed=%d",
             total_done, total_skipped, total_failed)
    return 0


def _make_point(point_id, row: dict, vec: np.ndarray, source_table: str,
                payload_cols: list[str], text_preview_chars: int):
    from qdrant_client.http.models import PointStruct

    payload = {
        "source_table": source_table,
        "source_id": point_id,
        "embedded_at": datetime.now().isoformat(timespec="seconds"),
    }
    for c in payload_cols:
        v = row.get(c)
        if v is None:
            continue
        s = str(v)
        if text_preview_chars > 0 and len(s) > text_preview_chars:
            s = s[:text_preview_chars]
        payload[c] = s
    return PointStruct(id=int(point_id) if isinstance(point_id, (int, float)) else str(point_id),
                       vector=vec.tolist(), payload=payload)


# ── Files mode ──────────────────────────────────────────────────────────────

def _run_files(cfg: dict, log: logging.Logger) -> int:
    fs = cfg.get("files_source", {})
    input_dir = Path(fs["input_dir"]) if fs.get("input_dir") else None
    output_dir = Path(fs["output_dir"]) if fs.get("output_dir") else None
    if not input_dir or not output_dir:
        log.error("files mode requires files_source.input_dir and files_source.output_dir")
        return 1
    if not input_dir.exists():
        log.error("input_dir does not exist: %s", input_dir)
        return 1
    output_dir.mkdir(parents=True, exist_ok=True)

    em = InfinityClient(
        base_url=cfg["infinity_url"],
        model=cfg.get("model_settings", {}).get("model_name", "sentence-transformers/all-MiniLM-L6-v2"),
        http_batch_size=int(cfg.get("model_settings", {}).get("http_batch_size", 32)),
    )
    log.info("Infinity ready: model=%s dim=%d", em.model, em.dim)

    exts = {e.lower() for e in fs.get("text_extensions", [".txt"])}
    files = [p for p in sorted(input_dir.rglob("*")) if p.is_file() and p.suffix.lower() in exts]
    log.info("found %d text files in %s", len(files), input_dir)

    ids: list[str] = []
    texts: list[str] = []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = f.read_text(encoding="latin-1", errors="replace")
        ids.append(str(f.relative_to(input_dir)))
        texts.append(content)

    vecs = em.embed(texts, normalize=True)
    em.close()
    out_path = output_dir / "embeddings.npz"
    np.savez(out_path, ids=np.array(ids, dtype=object), vectors=vecs)
    log.info("wrote %s shape=%s", out_path, vecs.shape)
    return 0


# ── Entrypoints ─────────────────────────────────────────────────────────────

def run(config: dict | None = None) -> int:
    log = _setup_logging()
    cfg = config or _load_config()
    src_type = cfg.get("source", {}).get("type", "postgres")
    if src_type == "postgres":
        return _run_postgres(cfg, log)
    if src_type == "files":
        return _run_files(cfg, log)
    log.error("unknown source.type: %s (expected 'postgres' or 'files')", src_type)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description="SBERT-via-Infinity embedding runner")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--source", choices=["postgres", "files"], help="override source.type")
    ap.add_argument("--table", help="override source.table")
    ap.add_argument("--collection", help="override qdrant_collection")
    args = ap.parse_args()

    log = _setup_logging()
    cfg = _load_config()

    if args.self_test:
        return _self_test(log)
    if args.source:
        cfg.setdefault("source", {})["type"] = args.source
    if args.table:
        cfg.setdefault("source", {})["table"] = args.table
    if args.collection:
        cfg["qdrant_collection"] = args.collection
    return run(cfg)


if __name__ == "__main__":
    sys.exit(main())
