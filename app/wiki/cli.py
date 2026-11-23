"""CLI for drafting, publishing, and searching the local NFC Wiki."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from app.llm.provider import ProviderError
from .lint import lint_wiki
from .query import select_wiki_context
from .runlog import record_wiki_operation
from .search import rebuild_index, search_articles
from .workflow import run_article_workflow


def main() -> int:
    parser = argparse.ArgumentParser(description="NFC Markdown Wiki 的 index-first context、Lint 與相容工具")
    commands = parser.add_subparsers(dest="command", required=True)
    draft = commands.add_parser("legacy-draft", help="舊式來源段落草稿流程（非 Wiki-first 核心流程）")
    draft.add_argument("--article-id", required=True)
    draft.add_argument("--title", required=True)
    draft.add_argument("--chapter", required=True)
    draft.add_argument("--query", required=True, help="從已擷取來源檢索段落的查詢詞")
    draft.add_argument("--data-dir", type=Path, default=Path("data"))
    draft.add_argument("--top-k", type=int, default=16)
    draft.add_argument("--source-id", action="append", help="限定來源；可重複指定")
    search = commands.add_parser("search", help="查詢已發布 Wiki 文章")
    search.add_argument("query")
    search.add_argument("--data-dir", type=Path, default=Path("data"))
    rebuild = commands.add_parser("reindex", help="從已發布文章重建 SQLite 搜尋索引")
    rebuild.add_argument("--data-dir", type=Path, default=Path("data"))
    context = commands.add_parser("context", help="先讀 Wiki index，再選取相關 Markdown 頁面")
    context.add_argument("query")
    context.add_argument("--project-dir", type=Path, default=Path("."))
    context.add_argument("--wiki-dir", type=Path, default=Path("wiki"))
    context.add_argument("--max-pages", type=int, default=5)
    lint = commands.add_parser("lint", help="檢查 Wiki 結構、連結、來源與孤立頁")
    lint.add_argument("--project-dir", type=Path, default=Path("."))
    lint.add_argument("--wiki-dir", type=Path, default=Path("wiki"))
    args = parser.parse_args()
    started_at = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    try:
        if args.command == "legacy-draft":
            result = run_article_workflow(
                article_id=args.article_id, title=args.title, chapter=args.chapter,
                query=args.query, data_dir=args.data_dir, top_k=args.top_k,
                source_ids=set(args.source_id) if args.source_id else None)
        elif args.command == "search":
            db = args.data_dir / "index" / "wiki.sqlite"
            result = search_articles(args.query, db_path=db)
        elif args.command == "reindex":
            result = {"index_mode": rebuild_index(args.data_dir / "wiki",
                                                   args.data_dir / "index" / "wiki.sqlite")}
        elif args.command == "context":
            result = select_wiki_context(args.query, project_dir=args.project_dir,
                                         wiki_dir=args.wiki_dir, max_pages=args.max_pages)
            record = record_wiki_operation(operation="query_context",
                status="knowledge_gap" if result["knowledge_gap"] else "context_ready",
                input_refs=["wiki/index.md", args.query],
                output_refs=[page["path"] for page in result["pages_read"]],
                validation={"index_read_first": True, "knowledge_gap": result["knowledge_gap"]},
                project_dir=args.project_dir,
                details={"answer_generated": False, "pages_read": len(result["pages_read"])},
                started_at=started_at)
            result["run_id"] = record["run_id"]
            result["run_path"] = record["run_path"]
        else:
            result = lint_wiki(project_dir=args.project_dir, wiki_dir=args.wiki_dir)
            record = record_wiki_operation(operation="lint", status=result["status"],
                input_refs=["wiki/index.md"], output_refs=["wiki/index.md"],
                validation={"counts": result["counts"], "pages_checked": result["pages_checked"]},
                project_dir=args.project_dir,
                details={"issues": result["issues"]}, started_at=started_at)
            result["run_id"] = record["run_id"]
            result["run_path"] = record["run_path"]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.command == "legacy-draft" and result["status"] != "passed":
            return 2
        if args.command == "lint" and result["status"] != "passed":
            return 1
        return 0
    except (ProviderError, RuntimeError, ValueError, OSError) as exc:
        print(f"執行失敗：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
