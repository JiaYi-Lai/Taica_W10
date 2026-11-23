"""Orchestrates one source through Fetch, Clean, and persisted metadata."""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import uuid

from .clean import clean_html
from .fetch import FetchError, fetch_url
from .metadata import duplicate_of, sha256_hex, save_sources
from .models import Source


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def ingest_sources(sources: list[Source], data_dir: Path, *, fetcher=fetch_url) -> dict:
    raw_dir, cleaned_dir, run_dir = (data_dir / name for name in ("raw", "cleaned", "runs"))
    for directory in (raw_dir, cleaned_dir, run_dir):
        directory.mkdir(parents=True, exist_ok=True)
    run_id = str(uuid.uuid4())
    started = datetime.now(timezone.utc).isoformat()
    events = []
    seen = list(sources)
    for source in sources:
        event = {"source_id": source.source_id, "started_at": datetime.now(timezone.utc).isoformat(),
                 "status": "failed", "issues": []}
        try:
            fetched = fetcher(source.original_url)
            source.resolved_url = fetched.resolved_url
            source.content_type = fetched.content_type
            source.http_status = fetched.http_status
            source.fetched_at = fetched.fetched_at
            source.sha256 = sha256_hex(fetched.body)
            raw_path = raw_dir / f"{_safe_name(source.source_id)}.html"
            raw_path.write_bytes(fetched.body)
            source.raw_path = str(raw_path.relative_to(data_dir.parent))
            result = clean_html(fetched.body)
            if not re.search(r"\bNFC\b|近場通訊|near field communication", result.text, re.I):
                raise ValueError("正文未通過 NFC 主題相關性檢查")
            duplicate = duplicate_of(source, seen)
            if duplicate:
                source.ingest_status = "duplicate"
                source.error = f"正文 hash 與 {duplicate.source_id} 相同"
                event["status"] = "duplicate"
                event["issues"].append(source.error)
            else:
                clean_path = cleaned_dir / f"{_safe_name(source.source_id)}.json"
                clean_path.write_text(json.dumps({"source_id": source.source_id,
                    "sha256": source.sha256, "paragraphs": result.paragraphs},
                    ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                source.cleaned_path = str(clean_path.relative_to(data_dir.parent))
                source.ingest_status = "success"
                source.error = ""
                event["status"] = "success"
                event["output_refs"] = [source.raw_path, source.cleaned_path]
        except (FetchError, ValueError, OSError) as exc:
            source.ingest_status = "failed"
            source.error = str(exc)
            if isinstance(exc, FetchError):
                source.http_status = exc.http_status
            event["issues"].append(source.error)
        event.update({"ended_at": datetime.now(timezone.utc).isoformat(),
                      "sha256": source.sha256, "ingest_status": source.ingest_status})
        events.append(event)
    save_sources(data_dir / "sources.json", sources)
    report = {"run_id": run_id, "workflow": "source_ingest", "started_at": started,
              "ended_at": datetime.now(timezone.utc).isoformat(), "events": events,
              "summary": {"total": len(sources),
                          "success": sum(s.ingest_status == "success" for s in sources),
                          "failed": sum(s.ingest_status == "failed" for s in sources),
                          "duplicate": sum(s.ingest_status == "duplicate" for s in sources)}}
    (run_dir / f"{run_id}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                             encoding="utf-8")
    return report
