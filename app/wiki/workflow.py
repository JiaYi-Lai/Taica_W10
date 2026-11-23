"""One-article draft, evidence validation, review, publish, and indexing workflow."""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import uuid

from app.llm.provider import OpenAICompatibleProvider
from .prompts import DRAFT_SYSTEM, REVIEW_SYSTEM, draft_user_prompt, review_user_prompt
from .publish import publish_article
from .retrieval import retrieve_paragraphs
from .search import rebuild_index
from .validate import validate_draft, validate_structure


def _safe_article_id(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.casefold()).strip("-")


def run_article_workflow(*, article_id: str, title: str, chapter: str, query: str,
                         data_dir: Path = Path("data"), provider=None,
                         top_k: int = 16, source_ids: set[str] | None = None) -> dict:
    article_id = _safe_article_id(article_id)
    run_id = str(uuid.uuid4())
    started = datetime.now(timezone.utc).isoformat()
    events = []
    drafts_dir = data_dir / "drafts"
    runs_dir = data_dir / "runs"
    drafts_dir.mkdir(parents=True, exist_ok=True)
    runs_dir.mkdir(parents=True, exist_ok=True)
    event = {"node": "retrieve_sources", "started_at": datetime.now(timezone.utc).isoformat(),
             "attempt": 1, "status": "running", "input_refs": [query]}
    paragraphs = retrieve_paragraphs(query, data_dir, top_k=top_k, source_ids=source_ids)
    if not paragraphs:
        event.update({"status": "failed", "issues": ["沒有符合條件的已 Ingest 官方段落"],
                      "ended_at": datetime.now(timezone.utc).isoformat()})
        events.append(event)
        result = _write_run(runs_dir, run_id, started, events, "insufficient_sources")
        raise RuntimeError(f"沒有可用來源段落；run_id={result['run_id']}")
    event.update({"status": "success", "output_refs": [
        f"{item['source_id']}:{item['paragraph_id']}" for item in paragraphs],
        "ended_at": datetime.now(timezone.utc).isoformat()})
    events.append(event)
    try:
        provider = provider or OpenAICompatibleProvider.from_env()
        event = {"node": "draft_claims", "started_at": datetime.now(timezone.utc).isoformat(),
                 "attempt": 1, "status": "running", "input_refs": [
                     f"{item['source_id']}:{item['paragraph_id']}" for item in paragraphs]}
        draft = provider.complete_json(DRAFT_SYSTEM,
            draft_user_prompt(title=title, chapter=chapter, query=query, paragraphs=paragraphs))
        event.update({"status": "success", "ended_at": datetime.now(timezone.utc).isoformat()})
        events.append(event)

        preflight_issues = validate_structure(draft, paragraphs)
        preflight_event = {"node": "validate_schema_and_citations",
                           "started_at": datetime.now(timezone.utc).isoformat(),
                           "ended_at": datetime.now(timezone.utc).isoformat(), "attempt": 1,
                           "status": "success" if not preflight_issues else "needs_review",
                           "decision": "continue_to_review" if not preflight_issues else "skip_review",
                           "issues": preflight_issues}
        events.append(preflight_event)
        reviews = None
        if not preflight_issues:
            event = {"node": "review_claim_support", "started_at": datetime.now(timezone.utc).isoformat(),
                     "attempt": 1, "status": "running", "input_refs": [
                         f"{item['source_id']}:{item['paragraph_id']}" for item in paragraphs]}
            reviews = provider.complete_json(REVIEW_SYSTEM, review_user_prompt(
                draft["summary"], draft["summary_refs"], draft["claims"], paragraphs))
            validation = validate_draft(draft, paragraphs, reviews)
            event.update({"status": "success", "decision": validation["status"],
                          "issues": validation["issues"],
                          "ended_at": datetime.now(timezone.utc).isoformat()})
            events.append(event)
        else:
            validation = validate_draft(draft, paragraphs, None)

        draft_record = {"article_id": article_id, "chapter": chapter, "run_id": run_id,
                        "model": getattr(provider, "model", "test-provider"), "draft": draft,
                        "reviews": reviews, "validation": validation,
                        "evidence_refs": [{"source_id": item["source_id"],
                                           "paragraph_id": item["paragraph_id"],
                                           "sha256": item["sha256"]} for item in paragraphs]}
        draft_path = drafts_dir / f"{article_id}--{run_id}.json"
        draft_path.write_text(json.dumps(draft_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        published = []
        if validation["status"] == "passed":
            evidence_map = {}
            for item in paragraphs:
                evidence_map[item["source_id"]] = item
            paths = publish_article(article_id=article_id, chapter=chapter, draft=draft,
                evidence=evidence_map.values(), validation=validation, run_id=run_id,
                wiki_dir=data_dir / "wiki")
            mode = rebuild_index(data_dir / "wiki", data_dir / "index" / "wiki.sqlite")
            published = [str(path.relative_to(data_dir.parent)) for path in paths]
        else:
            mode = "not_built"
        report = _write_run(runs_dir, run_id, started, events, validation["status"],
                            draft_path=str(draft_path.relative_to(data_dir.parent)),
                            published=published, index_mode=mode, model=getattr(provider, "model", "unknown"))
        return {"run_id": run_id, "article_id": article_id, "status": validation["status"],
                "draft_path": str(draft_path.relative_to(data_dir.parent)),
                "published_paths": published, "issues": validation["issues"],
                "index_mode": mode, "run_path": report["path"]}
    except Exception as exc:
        events.append({"node": "workflow", "started_at": datetime.now(timezone.utc).isoformat(),
                       "ended_at": datetime.now(timezone.utc).isoformat(), "attempt": 1,
                       "status": "failed", "issues": [f"{type(exc).__name__}: {exc}"]})
        _write_run(runs_dir, run_id, started, events, "failed")
        raise


def _write_run(runs_dir: Path, run_id: str, started: str, events: list[dict], status: str,
               **details) -> dict:
    path = runs_dir / f"{run_id}.json"
    report = {"run_id": run_id, "workflow": "wiki_article", "status": status,
              "started_at": started, "ended_at": datetime.now(timezone.utc).isoformat(),
              "events": events, **details}
    report["path"] = str(path)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report
