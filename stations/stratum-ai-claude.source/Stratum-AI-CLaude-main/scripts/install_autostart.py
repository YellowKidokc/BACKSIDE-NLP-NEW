from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def startup_shortcut() -> Path:
    startup = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    return startup / "FORGE Hub.lnk"


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    app_py = repo / "app.py"
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    if not pythonw.exists():
        pythonw = Path(sys.executable)
    shortcut = startup_shortcut()
    shortcut.parent.mkdir(parents=True, exist_ok=True)
    ps = f"""
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut('{shortcut}')
$shortcut.TargetPath = '{pythonw}'
$shortcut.Arguments = '"{app_py}" --minimized'
$shortcut.WorkingDirectory = '{repo}'
$shortcut.IconLocation = '{pythonw},0'
$shortcut.Save()
"""
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
