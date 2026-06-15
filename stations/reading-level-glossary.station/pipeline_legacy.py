"""Reading level glossary station.

Scans dropped text files, estimates reading level, and produces glossary
support for words above the configured audience level. This station does not
rewrite source text.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


STATION_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = STATION_ROOT / "config.json"

EASY_WORDS = {
    "a", "able", "about", "above", "after", "again", "against", "age", "ago",
    "air", "all", "almost", "alone", "along", "already", "also", "always",
    "am", "america", "an", "and", "another", "any", "are", "around", "as",
    "ask", "at", "back", "bad", "be", "because", "become", "been", "before",
    "began", "begin", "behind", "being", "best", "better", "between", "big",
    "both", "boy", "bring", "but", "by", "call", "came", "can", "cannot",
    "case", "change", "child", "children", "city", "come", "could", "country",
    "day", "did", "different", "do", "does", "done", "down", "during", "each",
    "early", "earth", "easy", "end", "enough", "even", "ever", "every",
    "example", "eye", "face", "fact", "family", "far", "father", "feel",
    "few", "find", "first", "five", "for", "form", "found", "four", "from",
    "gave", "get", "give", "go", "god", "good", "got", "great", "group",
    "had", "hand", "hard", "has", "have", "he", "head", "help", "her",
    "here", "high", "him", "his", "home", "house", "how", "i", "idea", "if",
    "in", "into", "is", "it", "its", "jesus", "just", "keep", "kind", "know",
    "last", "law", "learn", "left", "less", "let", "life", "like", "line",
    "little", "live", "long", "look", "made", "make", "man", "many", "may",
    "me", "mean", "men", "might", "more", "most", "mother", "move", "much",
    "must", "my", "name", "near", "need", "never", "new", "next", "night",
    "no", "not", "now", "number", "of", "off", "old", "on", "one", "only",
    "or", "other", "our", "out", "over", "own", "part", "people", "place",
    "point", "put", "question", "read", "real", "right", "said", "same",
    "saw", "say", "school", "see", "seem", "set", "she", "should", "show",
    "side", "since", "small", "so", "some", "something", "son", "soon",
    "sound", "start", "state", "still", "story", "strong", "such", "system",
    "take", "tell", "ten", "than", "that", "the", "their", "them", "then",
    "there", "these", "they", "thing", "think", "this", "those", "three",
    "through", "time", "to", "today", "together", "too", "true", "truth", "try",
    "two", "under", "up", "us", "use", "very", "want", "was", "way", "we",
    "well", "went", "were", "what", "when", "where", "which", "while", "who",
    "why", "will", "with", "word", "work", "world", "would", "write", "year",
    "yes", "you", "young", "your"
}

CANONICAL_DEFINITIONS = {
    "academic": "Written for advanced study, often with formal terms, citations, and careful claims.",
    "acceleration": "A speed-up in change, growth, or decline.",
    "ai-assisted": "Made with help from an AI system, while still needing human review.",
    "ai-generated": "Created by an AI system rather than written directly by a person.",
    "annotations": "Notes added to explain, mark, or comment on a source.",
    "architecture": "The way a system is structured and how its parts connect.",
    "atonement": "The act by which a moral debt is answered and relationship can be restored.",
    "attribution": "A statement showing where an idea, quote, source, or claim came from.",
    "authority": "The accepted power to decide, judge, teach, or govern.",
    "axiom": "A starting truth that the system uses before it proves anything else.",
    "biaxiosum": "A two-axis measurement frame used in the MDA work to compare moral and structural change.",
    "bureaucracy": "A rule-heavy institution or office system that can slow or control decisions.",
    "canonical": "Approved as the current source of truth for this workflow.",
    "categories": "Groups used to sort things that share the same kind of feature.",
    "civilization": "A large organized society with shared institutions, laws, culture, and memory.",
    "civilizations": "Large organized societies with shared institutions, laws, culture, and memory.",
    "coherence": "How well parts fit together without contradiction or collapse.",
    "coherence-metric": "A measurement used to estimate how strongly a system holds together.",
    "collaborator": "A person or AI partner working with someone else on the same task.",
    "communication": "The act of sharing meaning between people, groups, or systems.",
    "complexity": "The amount of interacting parts or difficulty inside a system.",
    "consciousness": "Aware experience: the capacity to notice, choose, and respond.",
    "constraint-removal": "Taking away a limit or boundary that was holding a system in place.",
    "constitutional": "Related to the basic rules or structure that governs a society or system.",
    "contaminates": "Adds something that pollutes, weakens, or corrupts the result.",
    "contradiction": "A conflict where two claims cannot both be true in the same way at the same time.",
    "contradictions": "Conflicts where two claims cannot both be true in the same way at the same time.",
    "counterarguments": "The strongest reasons someone could give against a claim.",
    "criticality": "The point where a system is close to changing state or breaking into a new pattern.",
    "curve-fitting": "Forcing a model to match data too closely, often so it looks stronger than it really is.",
    "decoherence": "The loss of stable order when a system stops holding together.",
    "deterministic": "Describes a process where the same causes always produce the same result.",
    "disciplines": "Fields of study or organized areas of work.",
    "domain-general": "Useful across many areas, not just one narrow field.",
    "domain-specific": "Useful inside one particular area or field.",
    "econometrica": "A major academic journal in economics and statistics.",
    "empirically": "Based on observation, measurement, or evidence rather than theory alone.",
    "entropy": "The drift from order toward disorder when no restoring force acts.",
    "epistemology": "The study of how we know what we claim to know.",
    "falsification": "A test that could show a claim is wrong.",
    "ferromagnetism": "A physics pattern where many tiny magnetic parts line up together.",
    "ferromagnets": "Materials whose tiny magnetic parts can line up together.",
    "fragmentation": "The breaking of a whole into separated pieces.",
    "grace": "Restoring action that moves against collapse and makes repair possible.",
    "hypothesis": "A proposed explanation that can be tested.",
    "institutional": "Related to organizations, systems, rules, or public structures.",
    "institutions": "Organizations or systems that shape public life, such as schools, courts, churches, or governments.",
    "intergenerational": "Passing across generations, such as from parents to children and grandchildren.",
    "interpretation": "An explanation of what something means.",
    "interpretations": "Different explanations of what something means.",
    "isomorphism": "A shared structure between two domains, not just a loose similarity.",
    "isomorphisms": "Shared structures between domains, not just loose similarities.",
    "longitudinal": "Studied across time rather than at only one moment.",
    "logos": "Ordered truth, reason, and meaning as the structure behind reality.",
    "mathematical": "Related to numbers, formulas, structure, or formal reasoning.",
    "measurement-based": "Grounded in measurement rather than impression alone.",
    "methodology": "The method or process used to study a question.",
    "metaphorically": "As a comparison or image, not as a literal identity.",
    "normalization": "Changing values into a common scale so they can be compared fairly.",
    "noether": "A reference to Noether's theorem: preserved symmetry implies conserved quantity.",
    "operationalization": "Turning an idea into something that can be measured or tested.",
    "operationalizations": "Ways of turning ideas into things that can be measured or tested.",
    "operationalized": "Turned into a measurable or testable form.",
    "ontology": "The study of what exists and what kind of thing it is.",
    "percentage-point": "A direct difference between percentages, such as 40 percent to 45 percent being 5 percentage points.",
    "polarization": "A split into opposing sides that become harder to reconcile.",
    "preliminary": "Early or first-stage, before final proof or final judgment.",
    "primary-source": "Original evidence from the time, person, dataset, or document being studied.",
    "probability": "The chance that something will happen or be true.",
    "psychological": "Related to the mind, behavior, feeling, or thought.",
    "quantitative": "Based on numbers or measurement.",
    "relationship": "A connection between people, ideas, events, or variables.",
    "research-method": "The process used to investigate a question and test claims.",
    "resolution": "The point where a conflict, question, or uncertainty is answered or settled.",
    "sigma": "A statistical distance from chance; higher sigma means stronger evidence.",
    "signal-to-noise": "The amount of useful information compared with distracting background noise.",
    "statistically": "In a way that uses data, probability, or measurement.",
    "sigma": "A statistical distance from chance; higher sigma means stronger evidence.",
    "superconductivity": "A physics state where electrical resistance drops away under special conditions.",
    "superconductors": "Materials that can carry electricity with no resistance under special conditions.",
    "synchronization": "Separate parts lining up in timing, behavior, or pattern.",
    "synchronized": "Made to line up in timing, behavior, or pattern.",
    "systematically": "Done according to a clear method or repeated pattern.",
    "substrate": "The deeper layer or base structure that something else rests on.",
    "symmetry": "A pattern that stays true when something is changed, moved, or viewed differently.",
    "theophysics": "David's framework treating physics and theology as two views of one ordered reality.",
    "thermodynamics": "The physics of heat, energy, work, and disorder.",
    "threshold-crossing": "Passing the point where a system changes state or enters a new phase.",
    "transformation": "A major change in form, structure, or state.",
    "universality": "The quality of applying across many cases rather than only one case.",
    "verification": "A check that tests whether a claim, result, or source is actually correct.",
    "visualization": "A chart, image, or display that helps people see a pattern.",
    "virtue-related": "Connected to moral qualities such as honesty, courage, self-control, or faithfulness."
}

NO_GLOSSARY_WORDS = {
    "accumulates", "accurately", "authors", "authorship", "commitment",
    "connections", "decorative", "everything", "genuinely", "incomplete",
    "precisely", "publications", "researcher's", "significant", "summarized",
    "suggestions", "supporting", "understanding", "uncomfortable"
}


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def strip_html(text: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return html.unescape(text)


def normalize_text(raw: str, suffix: str) -> str:
    text = strip_html(raw) if suffix.lower() in {".html", ".htm"} else raw
    text = re.sub(r"`{1,3}.*?`{1,3}", " ", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.M)
    text = re.sub(r"[_*~>#|]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def read_text(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def iter_inputs(config: dict, explicit: Path | None) -> list[Path]:
    extensions = {ext.lower() for ext in config.get("text_extensions", [])}
    if explicit:
        return [explicit]
    input_dir = Path(config["input_dir"])
    if not input_dir.exists():
        return []
    globber = input_dir.rglob("*") if config.get("recursive", False) else input_dir.glob("*")
    return sorted(
        path for path in globber
        if path.is_file() and path.suffix.lower() in extensions
    )


def split_sentences(text: str) -> list[str]:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    return sentences or ([text] if text else [])


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]*", text)


def count_syllables(word: str) -> int:
    word = word.lower()
    word = re.sub(r"[^a-z]", "", word)
    if not word:
        return 0
    vowels = "aeiouy"
    groups = 0
    prev = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev:
            groups += 1
        prev = is_vowel
    if word.endswith("e") and groups > 1 and not word.endswith(("le", "ye")):
        groups -= 1
    return max(1, groups)


def flesch_kincaid_grade(word_count: int, sentence_count: int, syllable_count: int) -> float:
    if word_count <= 0:
        return 0.0
    sentence_count = max(1, sentence_count)
    return max(0.0, (0.39 * (word_count / sentence_count)) + (11.8 * (syllable_count / word_count)) - 15.59)


def estimated_word_grade(term: str, syllables: int) -> float:
    letters = len(re.sub(r"[^A-Za-z]", "", term))
    grade = 1.5 + (syllables * 2.2) + max(0, letters - 6) * 0.55
    if "-" in term:
        grade += 0.5
    return round(grade, 1)


def simple_definition(term: str) -> str:
    key = term.lower()
    if key in CANONICAL_DEFINITIONS:
        return CANONICAL_DEFINITIONS[key]
    if key.endswith("tion"):
        return "A process or result connected to this article's argument. Define it in one plain sentence."
    if key.endswith("ity"):
        return "A quality or state named by the article. Define what quality is being measured or described."
    if key.endswith("ism"):
        return "A system of belief, practice, or explanation. Define which system the article means."
    return "Definition needed: write one plain sentence explaining this term in context."


def glossary_terms(text: str, config: dict) -> list[dict]:
    target_grade = float(config.get("target_grade", 8.0))
    always = {t.lower() for t in config.get("always_glossary_terms", [])}
    counts = Counter(w.lower().strip("'") for w in words(text))
    display_seen: dict[str, str] = {}
    for token in words(text):
        key = token.lower().strip("'")
        display_seen.setdefault(key, token.strip("'"))

    entries = []
    for key, count in counts.items():
        if not key or key in EASY_WORDS or key in NO_GLOSSARY_WORDS or len(key) <= 3:
            continue
        syllables = count_syllables(key)
        word_grade = estimated_word_grade(key, syllables)
        reason = []
        if key in always:
            reason.append("canonical term")
        if word_grade > target_grade:
            reason.append(f"estimated grade {word_grade} > target {target_grade:g}")
        if syllables >= 4:
            reason.append(f"{syllables} syllables")
        if len(key) >= 12:
            reason.append(f"{len(key)} letters")
        if not reason:
            continue
        entries.append({
            "term": display_seen.get(key, key),
            "key": key,
            "count": count,
            "syllables": syllables,
            "estimated_word_grade": word_grade,
            "reason": "; ".join(reason),
            "definition": simple_definition(key),
            "context": context_for(text, key)
        })
    entries.sort(key=lambda e: (-e["estimated_word_grade"], -e["count"], e["key"]))
    return entries[: int(config.get("max_glossary_terms", 80))]


def context_for(text: str, key: str) -> str:
    pattern = re.compile(rf"\b{re.escape(key)}s?\b", re.IGNORECASE)
    match = pattern.search(text)
    if not match:
        return ""
    start = max(0, match.start() - 90)
    end = min(len(text), match.end() + 120)
    snippet = text[start:end].strip()
    snippet = re.sub(r"\s+", " ", snippet)
    return snippet


def analyze_file(path: Path, config: dict, run_dir: Path) -> dict:
    raw = read_text(path)
    text = normalize_text(raw, path.suffix)
    token_list = words(text)
    sentence_count = len(split_sentences(text))
    syllable_count = sum(count_syllables(w) for w in token_list)
    word_count = len(token_list)
    grade = flesch_kincaid_grade(word_count, sentence_count, syllable_count)
    target = float(config.get("target_grade", 8.0))
    status = "PASS" if grade <= target else "REVIEW"
    if word_count < int(config.get("min_word_count", 20)):
        status = "TOO_SHORT"

    glossary = glossary_terms(text, config)
    result = {
        "source_file": str(path),
        "source_name": path.name,
        "timestamp": now_iso(),
        "target_label": config.get("target_label", "8th grade"),
        "target_grade": target,
        "estimated_grade": round(grade, 2),
        "status": status,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "syllable_count": syllable_count,
        "glossary_count": len(glossary),
        "glossary": glossary
    }

    stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", path.stem)[:90]
    json_path = run_dir / f"{stem}.readability_glossary.json"
    md_path = run_dir / f"{stem}.readability_glossary.md"
    csv_path = run_dir / f"{stem}.glossary.csv"

    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_markdown_report(md_path, result)
    write_csv(csv_path, glossary)
    result["report_json"] = str(json_path)
    result["report_md"] = str(md_path)
    result["glossary_csv"] = str(csv_path)
    return result


def write_csv(path: Path, glossary: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = ["term", "count", "syllables", "estimated_word_grade", "reason", "definition", "context"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in glossary:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_markdown_report(path: Path, result: dict) -> None:
    lines = [
        f"# Reading Level Glossary Report - {result['source_name']}",
        "",
        f"- Status: {result['status']}",
        f"- Target: {result['target_label']} (grade {result['target_grade']:g})",
        f"- Estimated grade: {result['estimated_grade']}",
        f"- Words / sentences / syllables: {result['word_count']} / {result['sentence_count']} / {result['syllable_count']}",
        f"- Glossary terms: {result['glossary_count']}",
        "",
        "## Glossary Support",
        "",
        "| Term | Count | Est. grade | Reason | Draft definition | Context |",
        "|---|---:|---:|---|---|---|",
    ]
    for item in result["glossary"]:
        definition = str(item["definition"]).replace("|", "\\|")
        reason = str(item["reason"]).replace("|", "\\|")
        context = str(item.get("context", "")).replace("|", "\\|")
        lines.append(
            f"| {item['term']} | {item['count']} | {item['estimated_word_grade']} | {reason} | {definition} | {context} |"
        )
    if not result["glossary"]:
        lines.append("| None | 0 | 0 | No above-target terms detected | | |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_index(run_dir: Path, results: list[dict], config: dict) -> None:
    summary = {
        "station": config.get("name", "reading-level-glossary"),
        "timestamp": now_iso(),
        "target_grade": config.get("target_grade", 8.0),
        "files": results,
    }
    (run_dir / "run_index.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    lines = [
        "# Reading Level Glossary Run Index",
        "",
        f"- Generated: {summary['timestamp']}",
        f"- Target: {config.get('target_label', '8th grade')} (grade {config.get('target_grade', 8.0)})",
        f"- Files processed: {len(results)}",
        "",
        "| Status | Grade | Glossary terms | File |",
        "|---|---:|---:|---|",
    ]
    for result in results:
        lines.append(
            f"| {result['status']} | {result['estimated_grade']} | {result['glossary_count']} | {result['source_name']} |"
        )
    (run_dir / "run_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def maybe_archive_inputs(paths: Iterable[Path], config: dict, run_id: str) -> None:
    if not config.get("archive_inputs", False):
        return
    archive_dir = Path(config["archive_dir"]) / run_id
    archive_dir.mkdir(parents=True, exist_ok=True)
    for path in paths:
        shutil.move(str(path), str(archive_dir / path.name))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan reading level and emit glossary support.")
    parser.add_argument("--file", type=Path, action="append", help="File to scan instead of DROP_HERE. Repeat for multiple files.")
    parser.add_argument("--target-grade", type=float, help="Override configured target grade.")
    parser.add_argument("--max-terms", type=int, help="Override maximum glossary terms per file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config()
    if args.target_grade is not None:
        config["target_grade"] = args.target_grade
        config["target_label"] = f"grade {args.target_grade:g}"
    if args.max_terms is not None:
        config["max_glossary_terms"] = args.max_terms

    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    run_dir = output_dir / f"run_{run_id}"
    run_dir.mkdir(parents=True, exist_ok=True)

    if args.file:
        inputs = args.file
    else:
        inputs = iter_inputs(config, None)
    if not inputs:
        print(f"No input files found. Drop .txt/.md/.html files into {config['input_dir']}")
        write_index(run_dir, [], config)
        return 0

    results = [analyze_file(path, config, run_dir) for path in inputs]
    write_index(run_dir, results, config)
    maybe_archive_inputs(inputs, config, run_id)

    review_count = sum(1 for result in results if result["status"] == "REVIEW")
    print(f"Processed {len(results)} file(s). Reports: {run_dir}")
    print(f"Target grade: {config.get('target_grade', 8.0):g}; review files: {review_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
