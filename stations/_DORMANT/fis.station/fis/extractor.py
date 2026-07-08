"""Text extraction from files. Handles common formats."""
from pathlib import Path
import chardet

# Extensions we can extract text from
TEXT_EXTENSIONS = {
    '.txt', '.md', '.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.yaml',
    '.yml', '.toml', '.ini', '.cfg', '.conf', '.xml', '.html', '.htm',
    '.css', '.sql', '.sh', '.bat', '.ps1', '.r', '.lua', '.go', '.rs',
    '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.rb', '.pl', '.log',
    '.csv', '.tsv', '.env', '.gitignore', '.dockerfile', '.lean',
}

SKIP_EXTENSIONS = {
    '.exe', '.dll', '.so', '.bin', '.dat', '.db', '.sqlite', '.sqlite3',
    '.zip', '.tar', '.gz', '.7z', '.rar', '.iso', '.img',
    '.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.ico', '.svg',
    '.mp3', '.wav', '.flac', '.ogg', '.aac', '.wma',
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv',
    '.fcard',  # Skip our own manifest files
}


def extract_text(file_path: Path, max_chars: int = 10000) -> str:
    """Extract text from a file. Returns empty string if unsupported."""
    ext = file_path.suffix.lower()

    if ext in SKIP_EXTENSIONS:
        return ""

    if ext in TEXT_EXTENSIONS or ext == '':
        return _read_text_file(file_path, max_chars)

    if ext == '.pdf':
        return _read_pdf(file_path, max_chars)

    if ext == '.docx':
        return _read_docx(file_path, max_chars)

    # Try as text anyway
    try:
        return _read_text_file(file_path, max_chars)
    except Exception:
        return ""


def _read_text_file(path: Path, max_chars: int) -> str:
    """Read a text file with encoding detection."""
    raw = path.read_bytes()[:max_chars * 2]
    detected = chardet.detect(raw[:5000])
    encoding = detected.get('encoding', 'utf-8') or 'utf-8'
    try:
        return raw.decode(encoding)[:max_chars]
    except (UnicodeDecodeError, LookupError):
        return raw.decode('utf-8', errors='replace')[:max_chars]


def _read_pdf(path: Path, max_chars: int) -> str:
    """Extract text from PDF using pdfplumber."""
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages[:20]:  # Cap at 20 pages
                t = page.extract_text()
                if t:
                    text_parts.append(t)
                if sum(len(p) for p in text_parts) > max_chars:
                    break
        return '\n'.join(text_parts)[:max_chars]
    except Exception:
        return ""


def _read_docx(path: Path, max_chars: int) -> str:
    """Extract text from DOCX."""
    try:
        from docx import Document
        doc = Document(str(path))
        text_parts = [p.text for p in doc.paragraphs if p.text.strip()]
        return '\n'.join(text_parts)[:max_chars]
    except Exception:
        return ""
