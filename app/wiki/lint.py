"""Deterministic Markdown Wiki health checks; semantic review stays with the LLM."""
from collections import defaultdict
import json
from pathlib import Path
import re

_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
_PARAGRAPH_RE = re.compile(r"\bp\d{4}-[a-f0-9]{10}\b")


def _frontmatter(text: str) -> tuple[dict, list[str]]:
    issues = []
    if not text.startswith("---\n"):
        return {}, ["missing_frontmatter"]
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, ["unclosed_frontmatter"]
    values, sources = {}, []
    in_sources = False
    for raw in parts[1].splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line == "sources:":
            in_sources = True
            continue
        if in_sources and line.startswith("-"):
            sources.append(line[1:].strip().strip("\"'"))
            continue
        in_sources = False
        if ":" not in line:
            issues.append("invalid_frontmatter_line")
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("\"'")
    values["sources"] = sources
    return values, issues


def lint_wiki(*, project_dir: Path = Path("."), wiki_dir: Path = Path("wiki"),
              source_registry: Path = Path("data/sources.json")) -> dict:
    project_dir = project_dir.resolve()
    wiki_dir = (project_dir / wiki_dir).resolve()
    registry_path = (project_dir / source_registry).resolve()
    issues = []

    def add(severity: str, issue_type: str, path: str, message: str) -> None:
        issues.append({"severity": severity, "type": issue_type, "path": path, "message": message})

    if not (wiki_dir / "index.md").is_file():
        add("error", "missing_index", "wiki/index.md", "缺少必要的 Wiki 索引。")
    if not (wiki_dir / "log.md").is_file():
        add("error", "missing_log", "wiki/log.md", "缺少必要的 append-only 操作紀錄。")
    if not registry_path.is_file():
        add("error", "missing_registry", str(source_registry), "找不到來源 Registry。")
        sources = {}
    else:
        try:
            sources = {row["source_id"]: row for row in
                       json.loads(registry_path.read_text(encoding="utf-8"))["sources"]}
        except (ValueError, KeyError, TypeError):
            sources = {}
            add("error", "invalid_registry", str(source_registry), "來源 Registry JSON 格式無效。")

    pages = []
    for path in sorted(wiki_dir.rglob("*.md")) if wiki_dir.exists() else []:
        if path.name.startswith("_") or path.name in {"index.md", "log.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(project_dir).as_posix()
        metadata, meta_issues = _frontmatter(text)
        for problem in meta_issues:
            add("error", problem, relative, "front matter 缺漏或格式無效。")
        if not metadata:
            continue
        for field in ("id", "title", "type", "updated_at"):
            if not metadata.get(field):
                add("error", "missing_metadata", relative, f"缺少 front matter 欄位 {field}。")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", metadata.get("updated_at", "")):
            add("error", "invalid_updated_at", relative, "updated_at 必須使用 YYYY-MM-DD。")
        page_sources = metadata.get("sources", [])
        body = text.split("---", 2)[-1]
        for source_id in page_sources:
            source = sources.get(source_id)
            if not source:
                add("error", "unknown_source", relative, f"來源 ID {source_id} 不存在於 Registry。")
            elif source.get("ingest_status") != "success":
                add("error", "source_not_ingested", relative,
                    f"來源 {source_id} 狀態為 {source.get('ingest_status')}，不能支撐正式頁面。")
            elif not source.get("raw_path") or not (project_dir / source["raw_path"]).is_file():
                add("error", "missing_raw_snapshot", relative, f"來源 {source_id} 找不到 raw snapshot。")
            if source_id not in body:
                add("error", "source_not_cited", relative, f"正文未出現 front matter 列出的來源 ID {source_id}。")
        if page_sources and not _PARAGRAPH_RE.search(body):
            add("error", "missing_paragraph_citation", relative,
                "有來源的頁面至少須包含一個可定位的 paragraph ID。")
        required_sections = {
            "concept": ["核心概念", "詳細說明", "相關知識", "來源"],
            "comparison": ["核心概念", "詳細說明", "相關知識", "來源"],
            "synthesis": ["核心概念", "詳細說明", "相關知識", "來源"],
            "source": ["來源摘要", "可整合知識", "既有頁面異動", "來源限制", "相關知識"],
        }.get(metadata.get("type"), [])
        for section in required_sections:
            if f"## {section}" not in body:
                add("error", "missing_section", relative, f"缺少必要段落：{section}。")
        pages.append((path, relative, metadata, text))

    index_path = wiki_dir / "index.md"
    index_text = index_path.read_text(encoding="utf-8") if index_path.is_file() else ""
    inbound = defaultdict(int)
    indexed_targets = set()
    for target in _LINK_RE.findall(index_text):
        target = target.split(None, 1)[0].strip("<>")
        if target.startswith(("https://", "http://", "mailto:", "#")):
            continue
        target_path, _, _anchor = target.partition("#")
        resolved = (index_path.parent / target_path).resolve() if target_path else index_path.resolve()
        indexed_targets.add(resolved)
    known_page_paths = {item[0].resolve() for item in pages}
    for target in indexed_targets & known_page_paths:
        inbound[target] += 1
    for source_path, relative, metadata, text in pages:
        if source_path.resolve() not in indexed_targets:
            add("error", "not_indexed", relative, "正式 Wiki 頁面未列於 wiki/index.md。")
        for target in _LINK_RE.findall(text):
            target = target.split(None, 1)[0].strip("<>")
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target_path, _, _anchor = target.partition("#")
            resolved = (source_path.parent / target_path).resolve() if target_path else source_path.resolve()
            try:
                resolved.relative_to(project_dir)
            except ValueError:
                add("error", "link_escape", relative, f"連結超出專案目錄：{target}")
                continue
            if not resolved.is_file():
                add("error", "broken_link", relative, f"找不到相對連結目標：{target}")
            elif resolved in {item[0].resolve() for item in pages}:
                inbound[resolved] += 1
    duplicates = defaultdict(list)
    for path, relative, metadata, _text in pages:
        key = (metadata.get("type"), metadata.get("title", "").casefold().strip())
        if key[1]:
            duplicates[key].append(relative)
    for (_kind, title), locations in duplicates.items():
        if len(locations) > 1:
            add("warning", "duplicate_title", ", ".join(locations), f"同類頁面標題可能重複：{title}")
    for path, relative, metadata, _text in pages:
        if metadata.get("type") != "source" and inbound[path.resolve()] == 0:
            add("warning", "orphan_page", relative, "沒有其他 Wiki 頁面連入此頁。")

    # The semantic pass is intentionally not inferred from string checks.
    add("info", "semantic_review_required", "wiki/",
        "語意矛盾、過期主張、近重複概念與知識缺口需由 Codex/LLM 讀頁面後另行判斷。")
    counts = {severity: sum(issue["severity"] == severity for issue in issues)
              for severity in ("error", "warning", "info")}
    return {"status": "passed" if counts["error"] == 0 else "failed",
            "counts": counts, "issues": issues,
            "pages_checked": len(pages), "index_path": "wiki/index.md"}
