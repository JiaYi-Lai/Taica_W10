"""Publish a passed article as Markdown plus JSON metadata, without silent overwrite."""
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re


def _plain_markdown(value: str) -> str:
    """Render model text as inert Markdown prose, never as raw markup or links."""
    value = re.sub(r"\s+", " ", str(value)).strip()
    value = html.escape(value, quote=False)
    return re.sub(r"([\\`*_{}\[\]<>()#+\-.!|>])", r"\\\1", value)


def publish_article(*, article_id: str, chapter: str, draft: dict,
                    evidence: list[dict], validation: dict, run_id: str,
                    wiki_dir: Path) -> tuple[Path, Path]:
    if validation.get("status") != "passed":
        raise ValueError("只有 validation_status=passed 的文章可以發布")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,63}", article_id):
        raise ValueError("article_id 僅允許 2–64 位小寫英數字與連字號")
    wiki_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = wiki_dir / f"{article_id}.md"
    metadata_path = wiki_dir / f"{article_id}.json"
    if markdown_path.exists() or metadata_path.exists():
        raise FileExistsError(f"文章 {article_id} 已存在；不會自動覆蓋")

    source_lookup = {item["source_id"]: item for item in evidence}
    used = {}
    body = [f"# {_plain_markdown(draft['title'])}", "", _plain_markdown(draft["summary"]), "",
            "摘要來源：" + "、".join(
                f"[{ref['source_id']} · {ref['paragraph_id']}]({source_lookup[ref['source_id']]['url']})"
                for ref in draft["summary_refs"]), "",
            "## 內容", ""]
    for index, claim in enumerate(draft["claims"], start=1):
        body.append(f"{index}. {_plain_markdown(claim['text'])}")
        citations = []
        for ref in claim["source_refs"]:
            source = source_lookup[ref["source_id"]]
            used[ref["source_id"]] = source
            citations.append(f"[{ref['source_id']} · {ref['paragraph_id']}]({source['url']})")
        body.append("   \n   來源：" + "、".join(citations))
        body.append("")
    body.extend(["## 參考來源", ""])
    for source_id, source in sorted(used.items()):
        body.append(f"- [{source_id}]({source['url']}) — {_plain_markdown(source['organization'])}，"
                    f"{_plain_markdown(source['title'])}。SHA-256：`{source['sha256']}`")
    metadata = {
        "article_id": article_id, "title": draft["title"], "chapter": chapter,
        "summary": draft["summary"], "source_ids": sorted(used),
        "references": ([{"source_id": ref["source_id"], "paragraph_id": ref["paragraph_id"]}
                       for ref in draft["summary_refs"]] +
                       [{"source_id": ref["source_id"], "paragraph_id": ref["paragraph_id"]}
                        for claim in draft["claims"] for ref in claim["source_refs"]]),
        "related_articles": [], "updated_at": datetime.now(timezone.utc).isoformat(),
        "validation_status": "passed", "run_id": run_id,
    }
    markdown_path.write_text("\n".join(body) + "\n", encoding="utf-8")
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return markdown_path, metadata_path
