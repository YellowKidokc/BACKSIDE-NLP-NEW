"""Baseline rename — mechanical, no NLP. Runs BEFORE classification."""
import re
from pathlib import Path
from datetime import date


def to_baseline(filename: str) -> str:
    """Convert any filename to lowercase-hyphen form.
    
    Clipboard Text (2).txt -> clipboard-text-2.txt
    My Report_FINAL v3.docx -> my-report-final-v3.docx
    """
    stem = Path(filename).stem
    ext = Path(filename).suffix.lower()
    # Replace underscores, spaces, dots (not extension) with hyphens
    clean = re.sub(r'[_\s.]+', '-', stem)
    # Replace non-alphanumeric (except hyphens) with hyphens
    clean = re.sub(r'[^a-zA-Z0-9\-]', '-', clean)
    # Collapse multiple hyphens
    clean = re.sub(r'-{2,}', '-', clean)
    # Strip leading/trailing hyphens, lowercase
    clean = clean.strip('-').lower()
    return f"{clean}{ext}" if clean else f"unnamed{ext}"


def to_slug(keywords: list[str], max_chars: int = 50) -> str:
    """Build a filename-ready slug from keywords."""
    parts = [re.sub(r'[^a-z0-9]+', '-', kw.lower()).strip('-') for kw in keywords]
    slug = '-'.join(p for p in parts if p)
    return slug[:max_chars].rstrip('-')
"""Rename preview generator — builds naming presets from NLP output."""
from datetime import date
from pathlib import Path


def build_rename_preview(
    domain: str, keywords: list[str], file_type: str,
    slug: str, ext: str
) -> dict:
    """Generate rename presets from classification data."""
    today = date.today().isoformat()
    domain_clean = domain.lower().replace(' ', '_')
    topic = keywords[0].replace(' ', '_') if keywords else "unknown"
    type_clean = file_type.lower().replace(' ', '_')

    baseline = f"{domain_clean}_{topic}_{type_clean}"
    return {
        "baseline": baseline,
        "baseline_rule": "domain_topic_type",
        "slug": slug,
        "keywords": [k.replace(' ', '_') for k in keywords[:3]],
        "presets": {
            "short": f"{today}__{domain_clean}__{topic}__v01{ext}",
            "descriptive": f"{today}__{domain_clean}__{topic}_{type_clean}__v01{ext}",
            "archive": f"{domain_clean}__{topic}_{type_clean}__{today}{ext}",
        }
    }
