"""Small deterministic paragraph retriever over ingested official sources."""
import json
import re
from pathlib import Path


def _terms(text: str) -> set[str]:
    return {term.casefold() for term in re.findall(r"[\w-]+", text, flags=re.UNICODE)
            if len(term) > 1}


def retrieve_paragraphs(query: str, data_dir: Path, *, top_k: int = 16,
                        source_ids: set[str] | None = None) -> list[dict]:
    registry = json.loads((data_dir / "sources.json").read_text(encoding="utf-8"))
    source_map = {item["source_id"]: item for item in registry["sources"]
                  if item.get("ingest_status") == "success"}
    wanted = source_ids or set(source_map)
    query_terms = _terms(query)
    candidates = []
    for source_id in sorted(wanted & source_map.keys()):
        source = source_map[source_id]
        clean_path = data_dir.parent / source["cleaned_path"]
        if not clean_path.is_file():
            continue
        cleaned = json.loads(clean_path.read_text(encoding="utf-8"))
        for paragraph in cleaned.get("paragraphs", []):
            text = paragraph.get("text", "")
            terms = _terms(text)
            overlap = len(query_terms & terms)
            if overlap:
                candidates.append({
                    "source_id": source_id,
                    "title": source["title"],
                    "organization": source["organization"],
                    "url": source["resolved_url"] or source["original_url"],
                    "sha256": source["sha256"],
                    "paragraph_id": paragraph["paragraph_id"],
                    "text": text,
                    "score": overlap,
                })
    candidates.sort(key=lambda item: (-item["score"], item["source_id"], item["paragraph_id"]))
    return candidates[:max(0, top_k)]
