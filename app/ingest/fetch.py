"""Bounded, low-rate HTTP fetcher for public source pages."""
from datetime import datetime, timezone
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .models import FetchResult


class FetchError(RuntimeError):
    def __init__(self, message: str, http_status: int | None = None):
        super().__init__(message)
        self.http_status = http_status


def fetch_url(url: str, timeout: float = 20.0, retries: int = 2,
              opener=urlopen, pause=sleep) -> FetchResult:
    """Fetch a public HTML page, retrying transient failures at most ``retries`` times."""
    last_error: FetchError | None = None
    for attempt in range(retries + 1):
        request = Request(url, headers={
            "User-Agent": "NFC-Learning-Wiki/0.1 (educational source ingestion)",
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.1",
        })
        try:
            with opener(request, timeout=timeout) as response:
                status = response.getcode()
                headers = response.headers
                content_type = headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
                if status < 200 or status >= 300:
                    raise FetchError(f"HTTP status {status}", status)
                if content_type not in {"text/html", "application/xhtml+xml"}:
                    raise FetchError(f"不接受的 Content-Type：{content_type or '(缺少)'}", status)
                body = response.read()
                if not body.strip():
                    raise FetchError("回應本文為空", status)
                return FetchResult(
                    body=body,
                    resolved_url=response.geturl(),
                    content_type=content_type,
                    http_status=status,
                    fetched_at=datetime.now(timezone.utc).isoformat(),
                )
        except HTTPError as exc:
            last_error = FetchError(f"HTTP status {exc.code}", exc.code)
            if exc.code < 500 and exc.code != 429:
                break
        except (TimeoutError, URLError, OSError) as exc:
            last_error = FetchError(f"網路擷取失敗：{exc}")
        except FetchError as exc:
            last_error = exc
            if exc.http_status is not None and exc.http_status < 500 and exc.http_status != 429:
                break
        if attempt < retries:
            pause(min(1.0 * (attempt + 1), 3.0))
    raise last_error or FetchError("未知擷取錯誤")
