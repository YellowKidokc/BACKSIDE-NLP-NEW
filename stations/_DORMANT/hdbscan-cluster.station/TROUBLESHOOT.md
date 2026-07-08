# 04_HDBSCAN — Troubleshooting

## Install fails: `Microsoft Visual C++ 14.0 or greater is required`

`hdbscan` builds a Cython extension on install. Get the build tools:

https://visualstudio.microsoft.com/visual-cpp-build-tools/

Pick "Desktop development with C++". Re-run `INSTALL.bat`.

Alternative (faster): use `conda install -c conda-forge hdbscan` — but that requires conda. The pip wheel is preferred for this repo.

## `no rows with non-null embedding`

You haven't run `02_SBERT` yet on this table, or every row failed. Check:

```python
db.query("SELECT COUNT(*) FROM youtube_apologetics WHERE sbert_embedding IS NOT NULL")
```

## Everything ends up in cluster -1 (noise)

`min_cluster_size` is too high for your data, or your embeddings live on a sphere (cosine-like) and you're using euclidean. Two knobs:

- Lower `min_cluster_size` (try 5)
- Switch `metric` to `"cosine"` (only valid when embeddings are NOT normalized; SBERT default normalizes them, so euclidean already approximates cosine)

If embeddings are L2-normalized (default in 02_SBERT), `metric: "euclidean"` is correct.

## Many tiny clusters

Raise `min_cluster_size`. For 4,000 documents across 21 topics, 10–25 is the right neighborhood.

## Summary CSV looks right but `cluster_id` not set in DB

Look in the log for `bulk update failed` — the runner falls back to per-row updates. If many fail, check Postgres permissions on the cluster column.

## How to re-cluster

```
UPDATE youtube_apologetics SET cluster_id = NULL;
```

then re-run. (You don't have to NULL it before clustering — the runner overwrites — but doing so makes "what's done?" queries trivial.)

## Memory blowup on a large table

HDBSCAN holds the whole distance matrix-equivalent in memory. For tables larger than ~50k rows, switch to `algorithm="boruvka_kdtree"` and consider precomputing a UMAP-reduced embedding at dim=10–20 first. Not a problem at the current 3,913-video scale.
