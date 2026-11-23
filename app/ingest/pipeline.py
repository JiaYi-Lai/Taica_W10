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


def _write_immutable(path: Path, content: bytes) -> None:
    """Create a snapshot once; an existing path is accepted only if bytes match."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != content:
            raise ValueError(f"不可變快照路徑已存在但內容不同：{path}")
        return
    try:
        with path.open("xb") as stream:
            stream.write(content)
    except FileExistsError:
        if path.read_bytes() != content:
            raise ValueError(f"不可變快照路徑發生衝突：{path}") from None


def ingest_sources(sources: list[Source], data_dir: Path, *, fetcher=fetch_url,
                   registry_sources: list[Source] | None = None) -> dict:
    raw_dir, cleaned_dir, run_dir = (data_dir / name for name in ("raw", "cleaned", "runs"))
    for directory in (raw_dir, cleaned_dir, run_dir):
        directory.mkdir(parents=True, exist_ok=True)
    run_id = str(uuid.uuid4())
    started = datetime.now(timezone.utc).isoformat()
    events = []
    seen = list(registry_sources if registry_sources is not None else sources)
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
            snapshot_dir = raw_dir / _safe_name(source.source_id) / source.sha256
            raw_path = snapshot_dir / "source.html"
            _write_immutable(raw_path, fetched.body)
            source.raw_path = raw_path.relative_to(data_dir.parent).as_posix()
            snapshot_metadata = {
                "source_id": source.source_id, "title": source.title,
                "organization": source.organization, "original_url": source.original_url,
                "resolved_url": source.resolved_url, "content_type": source.content_type,
                "fetched_at": source.fetched_at, "http_status": source.http_status,
                "sha256": source.sha256, "raw_path": source.raw_path,
                "rights_or_access_note": source.rights_or_access_note,
                "notes": source.notes,
            }
            metadata_path = snapshot_dir / "metadata.json"
            metadata_bytes = (json.dumps(snapshot_metadata, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            if metadata_path.exists():
                existing = json.loads(metadata_path.read_text(encoding="utf-8"))
                if existing.get("sha256") != source.sha256:
                    raise ValueError(f"不可變快照 Metadata 衝突：{metadata_path}")
            else:
                _write_immutable(metadata_path, metadata_bytes)
            source.metadata_path = metadata_path.relative_to(data_dir.parent).as_posix()
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
                clean_path = cleaned_dir / _safe_name(source.source_id) / f"{source.sha256}.json"
                clean_bytes = (json.dumps({"source_id": source.source_id,
                    "sha256": source.sha256, "paragraphs": result.paragraphs},
                    ensure_ascii=False, indent=2) + "\n").encode("utf-8")
                _write_immutable(clean_path, clean_bytes)
                source.cleaned_path = clean_path.relative_to(data_dir.parent).as_posix()
                source.ingest_status = "success"
                source.error = ""
                event["status"] = "success"
                event["output_refs"] = [source.raw_path, source.metadata_path, source.cleaned_path]
        except (FetchError, ValueError, OSError) as exc:
            source.ingest_status = "failed"
            source.error = str(exc)
            if isinstance(exc, FetchError):
                source.http_status = exc.http_status
            event["issues"].append(source.error)
        event.update({"ended_at": datetime.now(timezone.utc).isoformat(),
                      "sha256": source.sha256, "ingest_status": source.ingest_status})
        events.append(event)
    save_sources(data_dir / "sources.json", registry_sources if registry_sources is not None else sources)
    report = {"run_id": run_id, "workflow": "source_ingest", "started_at": started,
              "ended_at": datetime.now(timezone.utc).isoformat(), "events": events,
              "summary": {"total": len(sources),
                          "success": sum(s.ingest_status == "success" for s in sources),
                          "failed": sum(s.ingest_status == "failed" for s in sources),
                          "duplicate": sum(s.ingest_status == "duplicate" for s in sources)}}
    (run_dir / f"{run_id}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                             encoding="utf-8")
    return report
