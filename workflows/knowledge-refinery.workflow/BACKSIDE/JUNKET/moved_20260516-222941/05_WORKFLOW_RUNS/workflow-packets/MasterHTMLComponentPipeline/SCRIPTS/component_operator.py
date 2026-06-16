from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


BEGIN_RE = re.compile(r"<!--\s*BEGIN:COMPONENT:([^:]+):([^ ]+)\s*-->")
END_RE = re.compile(r"<!--\s*END:COMPONENT:([^:]+):([^ ]+)\s*-->")
PAGE_META_RE = re.compile(r"<!--\s*PAGE_META(?P<body>.*?)-->", re.DOTALL)
DATA_COMPONENT_RE = re.compile(r"\bdata-component\s*=")


@dataclass
class Component:
    component_type: str
    name: str
    start: int
    end: int | None = None
    matched: bool = False

    @property
    def key(self) -> str:
        return f"{self.component_type}:{self.name}"


@dataclass
class FileInventory:
    path: str
    page_meta: dict[str, str]
    begin_count: int
    end_count: int
    data_component_count: int
    matched_count: int
    unmatched_begins: list[str]
    unmatched_ends: list[str]
    duplicates: list[str]
    components: list[dict]
    status: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def html_files(root: Path) -> Iterable[Path]:
    if root.is_file() and root.suffix.lower() in {".html", ".htm"}:
        yield root
        return
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".html", ".htm"}:
            yield path


def parse_page_meta(html: str) -> dict[str, str]:
    match = PAGE_META_RE.search(html)
    if not match:
        return {}
    meta: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta


def parse_components(html: str) -> tuple[list[Component], list[str], list[str]]:
    events: list[tuple[int, str, str, str]] = []
    for match in BEGIN_RE.finditer(html):
        events.append((match.start(), "begin", match.group(1), match.group(2)))
    for match in END_RE.finditer(html):
        events.append((match.start(), "end", match.group(1), match.group(2)))
    events.sort(key=lambda item: item[0])

    stack: list[Component] = []
    components: list[Component] = []
    unmatched_ends: list[str] = []

    for pos, kind, component_type, name in events:
        key = f"{component_type}:{name}"
        if kind == "begin":
            component = Component(component_type, name, pos)
            stack.append(component)
            components.append(component)
            continue

        for index in range(len(stack) - 1, -1, -1):
            if stack[index].key == key:
                component = stack.pop(index)
                component.end = pos
                component.matched = True
                break
        else:
            unmatched_ends.append(key)

    unmatched_begins = [component.key for component in stack]
    return components, unmatched_begins, unmatched_ends


def inventory_file(path: Path, root: Path) -> FileInventory:
    html = read_text(path)
    page_meta = parse_page_meta(html)
    components, unmatched_begins, unmatched_ends = parse_components(html)
    keys = [component.key for component in components]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    matched_count = sum(1 for component in components if component.matched)
    status = "PASS"
    if not page_meta or unmatched_begins or unmatched_ends or duplicates:
        status = "REVIEW"
    return FileInventory(
        path=str(path.relative_to(root) if root.is_dir() else path),
        page_meta=page_meta,
        begin_count=len(components),
        end_count=len(list(END_RE.finditer(html))),
        data_component_count=len(DATA_COMPONENT_RE.findall(html)),
        matched_count=matched_count,
        unmatched_begins=unmatched_begins,
        unmatched_ends=unmatched_ends,
        duplicates=duplicates,
        components=[asdict(component) | {"key": component.key} for component in components],
        status=status,
    )


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def inventory(root: Path, out: Path) -> int:
    files = [inventory_file(path, root) for path in html_files(root)]
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "root": str(root),
        "file_count": len(files),
        "review_count": sum(1 for item in files if item.status != "PASS"),
        "files": [asdict(item) for item in files],
    }
    write_json(out, payload)
    print(f"Wrote inventory for {len(files)} HTML files to {out}")
    return 0


def component_pattern(component: str) -> re.Pattern[str]:
    try:
        component_type, name = component.split(":", 1)
    except ValueError as exc:
        raise SystemExit("Component must be formatted as type:name") from exc
    return re.compile(
        rf"<!--\s*BEGIN:COMPONENT:{re.escape(component_type)}:{re.escape(name)}\s*-->(?P<body>.*?)<!--\s*END:COMPONENT:{re.escape(component_type)}:{re.escape(name)}\s*-->",
        re.DOTALL,
    )


def extract(root: Path, component: str, out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    pattern = component_pattern(component)
    count = 0
    for path in html_files(root):
        html = read_text(path)
        match = pattern.search(html)
        if not match:
            continue
        rel = path.relative_to(root) if root.is_dir() else Path(path.name)
        safe_name = "__".join(rel.parts).replace(":", "_")
        target = out / f"{safe_name}.{component.replace(':', '.')}.html"
        target.write_text(match.group(0), encoding="utf-8")
        count += 1
    print(f"Extracted {count} copies of {component} to {out}")
    return 0


def replace(root: Path, component: str, template: Path, apply: bool) -> int:
    pattern = component_pattern(component)
    replacement = read_text(template).strip()
    changed = 0
    for path in html_files(root):
        html = read_text(path)
        if not pattern.search(html):
            continue
        new_html = pattern.sub(replacement, html, count=1)
        if new_html == html:
            continue
        changed += 1
        if apply:
            backup = path.with_suffix(path.suffix + ".bak")
            shutil.copy2(path, backup)
            path.write_text(new_html, encoding="utf-8")
            print(f"APPLIED {path} backup={backup}")
        else:
            print(f"DRY-RUN would replace {component} in {path}")
    print(f"{'Applied' if apply else 'Dry-run'} replacements: {changed}")
    return 0


def verify(root: Path, out: Path) -> int:
    return inventory(root, out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Operate on Kimi-marked HTML components.")
    sub = parser.add_subparsers(dest="command", required=True)

    inventory_parser = sub.add_parser("inventory")
    inventory_parser.add_argument("--root", required=True)
    inventory_parser.add_argument("--out", required=True)

    extract_parser = sub.add_parser("extract")
    extract_parser.add_argument("--root", required=True)
    extract_parser.add_argument("--component", required=True)
    extract_parser.add_argument("--out", required=True)

    replace_parser = sub.add_parser("replace")
    replace_parser.add_argument("--root", required=True)
    replace_parser.add_argument("--component", required=True)
    replace_parser.add_argument("--template", required=True)
    replace_parser.add_argument("--apply", action="store_true")

    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("--root", required=True)
    verify_parser.add_argument("--out", required=True)

    args = parser.parse_args()
    if args.command == "inventory":
        return inventory(Path(args.root), Path(args.out))
    if args.command == "extract":
        return extract(Path(args.root), args.component, Path(args.out))
    if args.command == "replace":
        return replace(Path(args.root), args.component, Path(args.template), args.apply)
    if args.command == "verify":
        return verify(Path(args.root), Path(args.out))
    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
