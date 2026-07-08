from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import build_artifact
from .storage import store_postgres, write_outputs
from .vector_space import project_artifacts


def run_one(args: argparse.Namespace) -> int:
    artifact = build_artifact(Path(args.input), vault_id=args.vault_id, note_version=args.note_version, embeddings=args.embeddings)
    json_path, html_path = write_outputs(artifact, Path(args.out))
    if args.postgres_dsn:
        store_postgres(artifact, args.postgres_dsn)
    print(f"JSON: {json_path}")
    print(f"HTML: {html_path}")
    print(f"ADDRESS: {artifact.address}")
    return 0


def run_batch(args: argparse.Namespace) -> int:
    root = Path(args.input_root)
    files = sorted(root.rglob(args.glob))
    count = 0
    for path in files:
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        out_dir = Path(args.out) / rel.parent / path.stem
        artifact = build_artifact(path, vault_id=args.vault_id, note_version=args.note_version, embeddings=args.embeddings)
        write_outputs(artifact, out_dir)
        if args.postgres_dsn:
            store_postgres(artifact, args.postgres_dsn)
        count += 1
        if args.limit and count >= args.limit:
            break
    print(f"Processed {count} Markdown files")
    return 0


def run_space(args: argparse.Namespace) -> int:
    csv_path, json_path = project_artifacts(Path(args.input_root), Path(args.out), mode=args.mode)
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Lossless Context Compression + Semantic Addressing pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    one = sub.add_parser("run")
    one.add_argument("--input", required=True)
    one.add_argument("--out", required=True)
    one.add_argument("--vault-id", required=True)
    one.add_argument("--note-version", default="1")
    one.add_argument("--embeddings", choices=["none", "sbert"], default="none")
    one.add_argument("--postgres-dsn")
    one.set_defaults(func=run_one)

    batch = sub.add_parser("batch")
    batch.add_argument("--input-root", required=True)
    batch.add_argument("--out", required=True)
    batch.add_argument("--vault-id", required=True)
    batch.add_argument("--note-version", default="1")
    batch.add_argument("--glob", default="*.md")
    batch.add_argument("--limit", type=int)
    batch.add_argument("--embeddings", choices=["none", "sbert"], default="none")
    batch.add_argument("--postgres-dsn")
    batch.set_defaults(func=run_batch)

    space = sub.add_parser("space")
    space.add_argument("--input-root", required=True)
    space.add_argument("--out", required=True)
    space.add_argument("--mode", choices=["sbert", "semantic"], default="sbert")
    space.set_defaults(func=run_space)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
