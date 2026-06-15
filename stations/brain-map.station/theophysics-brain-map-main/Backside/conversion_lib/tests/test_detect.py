from pathlib import Path

from theophysics_conversion.detect import Format, detect_format


def test_detect_common_extensions() -> None:
    assert detect_format("paper.pdf") is Format.PDF
    assert detect_format("deck.pptx") is Format.PPTX
    assert detect_format("notes.md") is Format.MARKDOWN
    assert detect_format("audio.mp3") is Format.AUDIO
    assert detect_format("image.png") is Format.IMAGE


def test_detect_urls() -> None:
    assert detect_format("https://www.youtube.com/watch?v=dQw4w9WgXcQ") is Format.YOUTUBE_URL
    assert detect_format("https://example.com/article") is Format.WEB_URL


def test_detect_txt_file_containing_url(tmp_path: Path) -> None:
    source = tmp_path / "link.txt"
    source.write_text("https://youtu.be/dQw4w9WgXcQ\n", encoding="utf-8")

    assert detect_format(source) is Format.YOUTUBE_URL


def test_detect_magic_number_pdf(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.write_bytes(b"%PDF-1.7\nbody")

    assert detect_format(source) is Format.PDF
