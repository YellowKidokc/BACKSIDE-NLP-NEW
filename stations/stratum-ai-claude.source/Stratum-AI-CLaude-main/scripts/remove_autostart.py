from __future__ import annotations

import os
from pathlib import Path


def startup_shortcut() -> Path:
    startup = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    return startup / "FORGE Hub.lnk"


def main() -> int:
    shortcut = startup_shortcut()
    if shortcut.exists():
        shortcut.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
