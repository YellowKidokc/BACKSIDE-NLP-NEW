"""
04_HDBSCAN — density-based clustering over SBERT embeddings.

Postgres mode (default):
  Loads (id, embedding[, label, title]) for every row in `source.table`
  where the embedding is NOT NULL. Runs HDBSCAN with `min_cluster_size`
  and writes `cluster_id` back to each row. Then emits a CSV summary:

    cluster_id, count, dominant_label, dominant_label_share,
    sample_titles (up to N), flag_unmapped (bool)

  flag_unmapped = True when the dominant label's share is below
  `summary.flag_unmapped_threshold` — i.e. the cluster doesn't sit
  cleanly under any of the 21 attack vectors and may be a new one.

Files mode:
  Loads embeddings.npz (produced by 02_SBERT files mode) and writes a
  clusters.csv with id,cluster_id.

Self-test: --self-test  generates 3 gaussian blobs in 8D and asserts >=2
           clusters discovered.
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOG_DIR = HERE / "_LOGS"
EXPORTS_DIR = HERE / "EXPORTS"
PG_DIR = ROOT / "07_POSTGRES"

if str(PG_DIR) not in sys.path:
    sys.path.insert(0, str(PG_DIR))


def _setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    logfile = LOG_DIR / f"hdbscan_{datetime.now():%Y%m%d}.log"
    logger = logging.getLogger("hdbscan")
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


def _station_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else HERE / path


class Clusterer:
    """Wrapper over hdbscan.HDBSCAN."""

    def __init__(
        self,
        min_cluster_size: int = 10,
        min_samples: int | None = None,
        metric: str = "euclidean",
        cluster_selection_method: str = "eom",
        cluster_selection_epsilon: float = 0.0,
    ):
        import hdbscan  # type: ignore

        kwargs = {
            "min_cluster_size": int(min_cluster_size),
            "metric": metric,
            "cluster_selection_method": cluster_selection_method,
            "cluster_selection_epsilon": float(cluster_selection_epsilon),
        }
        if min_samples is not None:
            kwargs["min_samples"] = int(min_samples)
        self.model = hdbscan.HDBSCAN(**kwargs)

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.fit_predict(X)


def _self_test(log: logging.Logger) -> int:
    rng = np.random.default_rng(42)
    centers = np.array([[0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 0], [0, 10, 0, 0, 0, 0, 0, 0]])
    points = np.vstack(
        [centers[i] + 0.5 * rng.standard_normal((40, 8)) for i in range(3)]
    ).astype(np.float32)
    try:
        clr = Clusterer(min_cluster_size=10)
        labels = clr.fit_predict(points)
    except Exception as e:
        log.error("clusterer failed: %s", e)
        return 2
    distinct = sorted(set(int(l) for l in labels) - {-1})
    log.info("self-test labels distribution: %s", Counter(int(l) for l in labels))
    if len(distinct) >= 2:
        log.info("self-test OK (found %d clusters)", len(distinct))
        return 0
    log.error("self-test FAILED: only %d cluster(s)", len(distinct))
    return 3


def _summarize_clusters(
    cluster_ids: np.ndarray,
    labels: list[str | None],
    titles: list[str | None],
    top_n: int,
    flag_threshold: float,
) -> list[dict]:
    rows: list[dict] = []
    for cid in sorted(set(int(c) for c in cluster_ids)):
        mask = cluster_ids == cid
        idxs = np.where(mask)[0]
        cluster_labels = [labels[i] for i in idxs if labels[i]]
        cluster_titles = [titles[i] for i in idxs if titles[i]]
        n = int(mask.sum())
        if cluster_labels:
            counts = Counter(cluster_labels)
            top_label, top_count = counts.most_common(1)[0]
            share = top_count / len(cluster_labels)
        else:
            top_label, share = "", 0.0
        flag = (cid != -1) and (share < flag_threshold)
        rows.append(
            {
                "cluster_id": int(cid),
                "count": n,
                "dominant_label": top_label,
                "dominant_label_share": round(share, 3),
                "sample_titles": " | ".join(t[:120] for t in cluster_titles[:top_n]),
                "flag_unmapped": "Y" if flag else "N",
            }
        )
    return rows


def _write_summary_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["cluster_id", "count", "dominant_label", "dominant_label_share", "sample_titles", "flag_unmapped"],
        )
        w.writeheader()
        w.writerows(rows)


def _run_postgres(cfg: dict, log: logging.Logger) -> int:
    from db_utils import Database, decode_vector

    src = cfg["source"]
    table = src["table"]
    id_col = src.get("id_col", "id")
    emb_col = src["embedding_col"]
    cluster_col = src["cluster_col"]
    label_col = src.get("label_col")
    title_col = src.get("title_col")
    where = src.get("where")

    ms = cfg.get("model_settings", {})
    summ = cfg.get("summary", {})
    top_n = int(summ.get("top_titles_per_cluster", 5))
    flag_threshold = float(summ.get("flag_unmapped_threshold", 0.5))
    report_path = _station_path(summ.get("report_path", str(EXPORTS_DIR / "csv" / "hdbscan_summary.csv")))

    select_cols = [id_col, emb_col]
    if label_col:
        select_cols.append(label_col)
    if title_col:
        select_cols.append(title_col)

    clause = f"{emb_col} IS NOT NULL"
    if where:
        clause = f"({where}) AND {clause}"

    sql = f"SELECT {', '.join(select_cols)} FROM {table} WHERE {clause} ORDER BY {id_col}"

    with Database(application_name="hdbscan_runner") as db:
        log.info("loading embeddings from %s", table)
        rows = db.query(sql)
        if not rows:
            log.warning("no rows with non-null embedding in %s", table)
            return 0
        log.info("loaded %d rows", len(rows))

        ids: list = []
        vecs: list[np.ndarray] = []
        labels_l: list = []
        titles_l: list = []
        bad = 0
        dim = None
        for r in rows:
            buf = r[emb_col]
            if buf is None:
                continue
            try:
                v = decode_vector(bytes(buf))
            except Exception as e:
                log.warning("row %s decode failed: %s", r[id_col], e)
                bad += 1
                continue
            if dim is None:
                dim = v.size
            elif v.size != dim:
                log.warning("row %s dim mismatch %d vs %d, skipping", r[id_col], v.size, dim)
                bad += 1
                continue
            ids.append(r[id_col])
            vecs.append(v)
            labels_l.append(r.get(label_col) if label_col else None)
            titles_l.append(r.get(title_col) if title_col else None)

        if not vecs:
            log.error("no usable embeddings (bad=%d)", bad)
            return 1
        X = np.vstack(vecs)
        log.info("clustering shape=%s min_cluster_size=%s metric=%s", X.shape,
                 ms.get("min_cluster_size", 10), ms.get("metric", "euclidean"))

        clr = Clusterer(
            min_cluster_size=ms.get("min_cluster_size", 10),
            min_samples=ms.get("min_samples"),
            metric=ms.get("metric", "euclidean"),
            cluster_selection_method=ms.get("cluster_selection_method", "eom"),
            cluster_selection_epsilon=ms.get("cluster_selection_epsilon", 0.0),
        )
        cluster_ids = clr.fit_predict(X)
        n_clusters = len(set(int(c) for c in cluster_ids) - {-1})
        n_noise = int(np.sum(cluster_ids == -1))
        log.info("clusters=%d noise=%d", n_clusters, n_noise)

        # Write cluster_id back per row.
        update_rows = [(int(c), idv) for c, idv in zip(cluster_ids, ids)]
        log.info("writing cluster_id back to %d rows", len(update_rows))
        try:
            db.update_rows_bulk(table, id_col, [cluster_col], update_rows)
        except Exception as e:
            log.exception("bulk update failed: %s — fallback per-row", e)
            ok = 0
            for cid, idv in update_rows:
                try:
                    db.update_row(table, id_col, idv, {cluster_col: cid})
                    ok += 1
                except Exception as ee:
                    log.error("row %s update failed: %s", idv, ee)
            log.info("per-row updates ok=%d", ok)

        summary_rows = _summarize_clusters(cluster_ids, labels_l, titles_l, top_n, flag_threshold)
        _write_summary_csv(summary_rows, report_path)
        log.info("summary -> %s", report_path)

        flagged = [r for r in summary_rows if r["flag_unmapped"] == "Y"]
        if flagged:
            log.warning("%d cluster(s) flagged as potentially unmapped (label share < %.2f):",
                        len(flagged), flag_threshold)
            for r in flagged[:10]:
                log.warning(
                    "  cluster %s n=%d top=%r share=%.2f sample=%s",
                    r["cluster_id"], r["count"], r["dominant_label"],
                    r["dominant_label_share"], r["sample_titles"][:160],
                )

    return 0


def _run_files(cfg: dict, log: logging.Logger) -> int:
    fs = cfg.get("files_source", {})
    npz = _station_path(fs["input_npz"]) if fs.get("input_npz") else None
    out_dir = _station_path(fs["output_dir"]) if fs.get("output_dir") else EXPORTS_DIR / "csv"
    if not npz:
        log.error("files mode requires files_source.input_npz")
        return 1
    if not npz.exists():
        log.error("missing %s", npz)
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)

    data = np.load(npz, allow_pickle=True)
    ids = list(data["ids"])
    X = np.asarray(data["vectors"], dtype=np.float32)
    log.info("loaded %s shape=%s", npz, X.shape)

    ms = cfg.get("model_settings", {})
    clr = Clusterer(
        min_cluster_size=ms.get("min_cluster_size", 10),
        min_samples=ms.get("min_samples"),
        metric=ms.get("metric", "euclidean"),
        cluster_selection_method=ms.get("cluster_selection_method", "eom"),
        cluster_selection_epsilon=ms.get("cluster_selection_epsilon", 0.0),
    )
    cluster_ids = clr.fit_predict(X)
    out = out_dir / "clusters.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "cluster_id"])
        for idv, cid in zip(ids, cluster_ids):
            w.writerow([idv, int(cid)])
    log.info("wrote %s", out)
    return 0


def run(config: dict | None = None) -> int:
    log = _setup_logging()
    cfg = config or _load_config()
    src_type = cfg.get("source", {}).get("type", "postgres")
    if src_type == "postgres":
        return _run_postgres(cfg, log)
    if src_type == "files":
        return _run_files(cfg, log)
    log.error("unknown source.type: %s", src_type)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description="HDBSCAN clustering runner")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--source", choices=["postgres", "files"])
    args = ap.parse_args()
    log = _setup_logging()
    cfg = _load_config()
    if args.self_test:
        return _self_test(log)
    if args.source:
        cfg["source"]["type"] = args.source
    return run(cfg)


if __name__ == "__main__":
    sys.exit(main())
