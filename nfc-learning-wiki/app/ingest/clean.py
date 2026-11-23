"""Conservative HTML-to-text extraction with stable paragraph references."""
import hashlib
import re
from html.parser import HTMLParser

from .models import CleanResult

_SKIP_TAGS = {"script", "style", "nav", "footer", "header", "aside", "noscript", "svg", "form"}
_BLOCK_TAGS = {"article", "main", "section", "h1", "h2", "h3", "h4", "h5", "h6",
               "p", "li", "tr", "blockquote", "dd", "dt"}


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _SKIP_TAGS:
            self.skip_depth += 1
        elif not self.skip_depth and tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in _SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        elif not self.skip_depth and tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)


def clean_html(html: str | bytes, min_chars: int = 160) -> CleanResult:
    if isinstance(html, bytes):
        html = html.decode("utf-8", errors="replace")
    parser = _TextExtractor()
    parser.feed(html)
    text = re.sub(r"[\t\r\f\v ]+", " ", "".join(parser.parts))
    paragraphs = [re.sub(r"\s+", " ", p).strip() for p in text.split("\n")]
    paragraphs = [p for p in paragraphs if p]
    if not paragraphs:
        raise ValueError("清理後正文為空")
    full_text = "\n\n".join(paragraphs)
    if len(full_text) < min_chars:
        raise ValueError(f"清理後正文過短：{len(full_text)} 字元（最低 {min_chars}）")
    refs = []
    for index, paragraph in enumerate(paragraphs, start=1):
        digest = hashlib.sha256(paragraph.encode("utf-8")).hexdigest()[:10]
        refs.append({"paragraph_id": f"p{index:04d}-{digest}", "text": paragraph})
    return CleanResult(text=full_text, paragraphs=refs)
