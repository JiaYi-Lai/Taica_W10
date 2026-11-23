"""Index-first context selection for Codex/LLM queries over Markdown Wiki pages."""
import json
from pathlib import Path
import re

from .lint import _LINK_RE, _frontmatter


def _tokens(text: str) -> set[str]:
    tokens = {value.casefold() for value in re.findall(r"[\w-]+", text, flags=re.UNICODE)
              if len(value) > 1}
    # Chinese and Japanese text often has no spaces between words. Add overlapping
    # character pairs so a query such as "NFC 安全" can match "NFC 安全入門".
    cjk = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]+")
    for run in cjk.findall(text):
        tokens.update(run[index:index + 2] for index in range(len(run) - 1))
    return tokens


def select_wiki_context(query: str, *, project_dir: Path = Path("."),
                        wiki_dir: Path = Path("wiki"), max_pages: int = 5) -> dict:
    """Read the Wiki index first, then select linked Markdown pages and one-hop context."""
    project_dir = project_dir.resolve()
    wiki_dir = (project_dir / wiki_dir).resolve()
    index_path = wiki_dir / "index.md"
    if not index_path.is_file():
        raise FileNotFoundError("wiki/index.md 不存在；無法以 Wiki-first 方式查詢。")
    index_text = index_path.read_text(encoding="utf-8")
    query_tokens = _tokens(query)
    candidates = {}
    lines = index_text.splitlines()
    for index, line in enumerate(lines):
        for target in _LINK_RE.findall(line):
            target = target.split(None, 1)[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path, _, _anchor = target.partition("#")
            path = (index_path.parent / target_path).resolve() if target_path else index_path.resolve()
            try:
                path.relative_to(wiki_dir)
            except ValueError:
                continue
            if path.suffix.lower() != ".md" or path in {index_path.resolve(), (wiki_dir / "log.md").resolve()}:
                continue
            if not path.is_file():
                continue
            context_line = " ".join(lines[max(0, index - 1):min(len(lines), index + 2)])
            score = len(query_tokens & _tokens(context_line))
            candidates[path] = max(candidates.get(path, 0), score)

    ranked = sorted((path for path, score in candidates.items() if score > 0),
                    key=lambda path: (-candidates[path], path.as_posix()))
    selected = []
    for path in ranked:
        if len(selected) >= max(1, max_pages):
            break
        selected.append(path)
    # Overview is the first Wiki context after index, even when the query is broad.
    overview = (wiki_dir / "overview.md").resolve()
    if overview.is_file() and overview not in selected:
        selected.insert(0, overview)
        selected = selected[:max(1, max_pages)]

    pages = []
    for path in selected:
        text = path.read_text(encoding="utf-8")
        metadata, _ = _frontmatter(text)
        pages.append({"path": path.relative_to(project_dir).as_posix(),
                      "title": metadata.get("title", path.stem),
                      "sources": metadata.get("sources", []), "content": text})
    return {"query": query, "index_path": "wiki/index.md", "index": index_text,
            "pages_read": pages, "knowledge_gap": not any(path != overview for path in selected)}
