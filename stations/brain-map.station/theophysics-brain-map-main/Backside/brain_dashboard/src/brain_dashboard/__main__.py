import argparse
from . import __version__
from .app import run_app


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="store_true")
    parser.add_argument("--headless-smoke-test", action="store_true")
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return 0
    return run_app(headless_smoke_test=args.headless_smoke_test)


if __name__ == "__main__":
    raise SystemExit(main())
