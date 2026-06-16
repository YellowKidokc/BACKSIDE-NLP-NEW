from __future__ import annotations

import platform
import subprocess
import xml.etree.ElementTree as ET
from typing import Any

PREFIXES = ("Theophysics_", "FAP_")


def read_tasks() -> list[dict[str, Any]]:
    if platform.system() != "Windows":
        return []
    proc = subprocess.run(
        ["schtasks", "/Query", "/XML", "/TN", "*"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return []
    return parse_tasks_xml(proc.stdout)


def parse_tasks_xml(xml_text: str) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return tasks
    for task in root.findall(".//Task"):
        name = task.findtext("RegistrationInfo/URI", default="").strip("\\")
        if not name.startswith(PREFIXES):
            continue
        tasks.append(
            {
                "name": name,
                "status": task.findtext("Settings/Enabled", "true"),
                "last_run_time": task.findtext("Principals/Principal/RunLevel", ""),
                "next_run_time": "",
                "last_result": "",
            }
        )
    return tasks
