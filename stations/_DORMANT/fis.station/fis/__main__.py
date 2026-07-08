"""CLI entry point for FIS."""
import argparse
import sys
from pathlib import Path
from fis.pipeline import FISPipeline


def main():
    parser = argparse.ArgumentParser(description="FIS - File Intelligence System")
    parser.add_argument("target", nargs="?", help="Folder or file path to process")
    parser.add_argument("--file", action="store_true", help="Process single file")
    parser.add_argument("--init-db", action="store_true", help="Initialize SQLite database")
    parser.add_argument("--no-bart", action="store_true", help="Skip BART summarizer (use extractive)")
    parser.add_argument("--no-deberta", action="store_true", help="Skip DeBERTa (use rule-based)")
    args = parser.parse_args()

    if args.init_db:
        from fis.db import init_db
        init_db()
        print("SQLite database initialized.")
        return

    if not args.target:
        parser.print_help()
        sys.exit(1)

    target = Path(args.target)
    pipeline = FISPipeline(use_bart=not args.no_bart, use_deberta=not args.no_deberta)

    if args.file:
        if not target.is_file():
            print(f"Not a file: {target}")
            sys.exit(1)
        card = pipeline.process_file(target)
        pipeline.write_card(card, target.parent)
        print(f"Card written for: {target.name}")
    else:
        if not target.is_dir():
            print(f"Not a directory: {target}")
            sys.exit(1)
        cards = pipeline.process_folder(target)
        pipeline.write_manifest(cards, target)
        print(f"Manifest written: {len(cards)} files classified in {target}")


if __name__ == "__main__":
    main()
