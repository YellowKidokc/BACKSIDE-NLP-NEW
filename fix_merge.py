"""Fix merge duplicates: remove second Section 07 from each Core 8 pipeline."""
import re
from pathlib import Path

stations = [
    "exec-summary.station",
    "plain-language.station",
    "claim-extraction.station",
    "claim-classification.station",
    "load-bearing-claims.station",
    "falsification.station",
    "evidence-map.station",
    "contradiction-scan.station",
]
base = Path(r"D:\GitHub\BACKSIDE-NLP-NEW\stations")

for s in stations:
    p = base / s / "pipeline.py"
    if not p.exists():
        print(f"  {s}: NOT FOUND")
        continue
    text = p.read_text(encoding="utf-8")
    marker = "# 07_PROCESS"
    positions = [m.start() for m in re.finditer(re.escape(marker), text)]
    if len(positions) < 2:
        print(f"  {s}: {len(positions)} section 07 headers - SKIP")
        continue

    # Find start of the second section 07 block
    second_07 = positions[1]
    # Walk back to get the full section header (separator line above)
    before = text.rfind("\n", 0, second_07)
    before2 = text.rfind("\n", 0, before)
    cut_start = before2 if "====" in text[before2:before] else before

    # Find the next section 08 header after the second 07
    sec08_match = re.search(r"# 08_ARTIFACTS", text[second_07:])
    if not sec08_match:
        print(f"  {s}: no section 08 after second 07 - SKIP")
        continue
    sec08_pos = second_07 + sec08_match.start()
    # Walk back to separator
    before_08 = text.rfind("\n", 0, sec08_pos)
    before_082 = text.rfind("\n", 0, before_08)
    cut_end = before_082 if "====" in text[before_082:before_08] else before_08

    removed_lines = text[cut_start:cut_end].count("\n")
    new_text = text[:cut_start] + text[cut_end:]
    p.write_text(new_text, encoding="utf-8")
    print(f"  {s}: removed {removed_lines} duplicate lines - DONE")

print("\nAll pipelines cleaned.")
