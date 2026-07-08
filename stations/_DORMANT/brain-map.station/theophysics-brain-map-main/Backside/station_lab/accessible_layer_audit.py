from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path


DEFAULT_EXPORT_ROOT = Path(r"X:\EXPORTS\accessible-layer-audits")


class TextExtractor(HTMLParser):
    capture_tags = {"h1", "h2", "h3", "p", "blockquote", "li", "td", "th"}
    skip_tags = {"style", "script", "nav", "footer"}

    def __init__(self) -> None:
        super().__init__()
        self.skip_depth = 0
        self.stack: list[str] = []
        self.current: list[str] = []
        self.items: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.skip_tags:
            self.skip_depth += 1
        self.stack.append(tag)
        if tag in self.capture_tags:
            self.current = []

    def handle_endtag(self, tag: str) -> None:
        if tag in self.capture_tags:
            text = " ".join("".join(self.current).split())
            if text:
                self.items.append((tag, text))
            self.current = []
        if tag in self.skip_tags and self.skip_depth:
            self.skip_depth -= 1
        if self.stack:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        if self.stack and self.stack[-1] in self.capture_tags:
            self.current.append(data)


@dataclass
class Check:
    name: str
    status: str
    detail: str


def read_source(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in {".html", ".htm"}:
        parser = TextExtractor()
        parser.feed(raw)
        return "\n\n".join(text for _, text in parser.items)
    return raw


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def contains_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def check_required_structures(output: str) -> list[Check]:
    checks = [
        Check(
            "24-property table",
            "PASS" if re.search(r"\|\s*#\s*\|\s*Property\s*\|", output, re.I) and output.count("|") >= 80 else "FAIL",
            "Accessible layer should preserve the original table as simplified scannable evidence.",
        ),
        Check(
            "equation shown",
            "PASS" if "dC/dt" in output and "O * G" in output and "S * C" in output else "FAIL",
            "At least one simple formal equation should remain visible and explained.",
        ),
        Check(
            "9-vs-14 asymmetry",
            "PASS" if contains_any(output, [r"\bnine\b.*\bfourteen\b", r"\b9\b.*\b14\b"]) else "FAIL",
            "The Fruits/work asymmetry is a major argument, not a side note.",
        ),
        Check(
            "is-ought tense line",
            "PASS" if "Same fact. Different tense." in output else "WARN",
            "The accessible pass should preserve the truck/is-ought tense insight if possible.",
        ),
        Check(
            "falsification preserved",
            "PASS" if len(re.findall(r"\bFind\b|\bShow\b|\bBreak\b|\bchallenge\b|\bfals", output, re.I)) >= 5 else "FAIL",
            "The accessible layer must keep real break points.",
        ),
        Check(
            "Always Grace refrain",
            "PASS" if len(re.findall(r"Always grace", output, re.I)) >= 3 else "WARN",
            "Grace should land as structure, not decorative ending.",
        ),
        Check(
            "book-report voice",
            "PASS" if len(re.findall(r"the article (says|argues|claims)", output, re.I)) <= 2 else "FAIL",
            "Avoid distancing the reader from the claim.",
        ),
    ]
    return checks


def check_source_faithfulness(source: str, output: str) -> list[Check]:
    output_norm = normalize(output)
    source_norm = normalize(source)
    source_markers = {
        "truck": ["truck", "overloaded", "center of gravity"],
        "moral parallel": ["society", "betrayal", "fraud"],
        "98 percent": ["98"],
        "rejection trap": ["rejection", "moral framework"],
        "is ought": ["is-ought", "ought"],
        "properties": ["twenty-four", "24"],
        "fruit eigenstate": ["fruit", "eigenstate"],
        "eight schemata": ["eight", "schemata"],
        "open system": ["open system", "grace"],
        "falsification": ["falsification", "kill"],
    }
    checks: list[Check] = []
    for name, markers in source_markers.items():
        source_has = any(marker in source_norm for marker in markers)
        output_has = any(marker in output_norm for marker in markers)
        status = "PASS" if (not source_has or output_has) else "FAIL"
        checks.append(Check(name, status, f"Markers: {', '.join(markers)}"))
    return checks


def score(checks: list[Check]) -> int:
    points = 0
    total = 0
    for check in checks:
        total += 2
        if check.status == "PASS":
            points += 2
        elif check.status == "WARN":
            points += 1
    return round((points / total) * 100) if total else 0


def markdown_report(source: Path, output: Path, checks: list[Check], source_text: str, output_text: str) -> str:
    score_value = score(checks)
    failed = [c for c in checks if c.status == "FAIL"]
    warned = [c for c in checks if c.status == "WARN"]
    lines = [
        "# Accessible Layer Audit",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Source: `{source}`",
        f"- Output: `{output}`",
        f"- Source words: {word_count(source_text):,}",
        f"- Output words: {word_count(output_text):,}",
        f"- Score: {score_value}/100",
        f"- Failures: {len(failed)}",
        f"- Warnings: {len(warned)}",
        "",
        "| Check | Status | Detail |",
        "|---|---|---|",
    ]
    for check in checks:
        lines.append(f"| {check.name} | {check.status} | {check.detail} |")
    lines.extend(
        [
            "",
            "## Next-Pass Prompt",
            "",
            "Revise the accessible layer against this audit. Preserve the source order and direct voice. Fix every FAIL first, then every WARN. Do not add new claims that are not grounded in the source.",
        ]
    )
    return "\n".join(lines) + "\n"


def run(source: Path, output: Path, export_root: Path) -> Path:
    source_text = read_source(source)
    output_text = output.read_text(encoding="utf-8", errors="replace")
    checks = check_required_structures(output_text) + check_source_faithfulness(source_text, output_text)
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "_" + output.stem[:80]
    export_dir = export_root / run_id
    export_dir.mkdir(parents=True, exist_ok=True)
    report = markdown_report(source, output, checks, source_text, output_text)
    (export_dir / "audit.md").write_text(report, encoding="utf-8")
    (export_dir / "audit.json").write_text(
        json.dumps(
            {
                "source": str(source),
                "output": str(output),
                "score": score(checks),
                "checks": [check.__dict__ for check in checks],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return export_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit an accessible-layer rewrite against the original source.")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--export-root", type=Path, default=DEFAULT_EXPORT_ROOT)
    args = parser.parse_args()
    export_dir = run(args.source, args.output, args.export_root)
    print(f"Audit written: {export_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
