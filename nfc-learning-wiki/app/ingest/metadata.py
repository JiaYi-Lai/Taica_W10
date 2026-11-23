"""Source registry loading, saving, and content deduplication."""
import hashlib
import json
from pathlib import Path

from .models import Source


def sha256_hex(content: bytes | str) -> str:
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def load_sources(path: Path) -> list[Source]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [Source.from_dict(row) for row in payload["sources"]]


def save_sources(path: Path, sources: list[Source]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"sources": [s.to_dict() for s in sources]},
                               ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def duplicate_of(source: Source, sources: list[Source]) -> Source | None:
    return next((other for other in sources
                 if other.source_id != source.source_id and other.sha256 == source.sha256
                 and source.sha256), None)
