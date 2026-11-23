"""Data types used by the source ingestion pipeline."""
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Source:
    source_id: str
    title: str
    organization: str
    original_url: str
    notes: str = ""
    rights_or_access_note: str = "公開官方網頁；保留來源連結，原文僅供本機驗證。"
    resolved_url: str = ""
    content_type: str = ""
    fetched_at: str = ""
    http_status: int | None = None
    sha256: str = ""
    ingest_status: str = "pending"
    error: str = ""
    raw_path: str = ""
    cleaned_path: str = ""

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Source":
        allowed = cls.__dataclass_fields__.keys()
        return cls(**{key: value[key] for key in allowed if key in value})

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class FetchResult:
    body: bytes
    resolved_url: str
    content_type: str
    http_status: int
    fetched_at: str


@dataclass
class CleanResult:
    text: str
    paragraphs: list[dict[str, str]] = field(default_factory=list)
