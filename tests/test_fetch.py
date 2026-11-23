import io
import unittest
from email.message import Message
from urllib.error import HTTPError

from app.ingest.fetch import FetchError, fetch_url


class FakeResponse:
    def __init__(self, body=b"<html>content</html>", content_type="text/html; charset=utf-8", status=200):
        self.body, self.status, self.headers = body, status, Message()
        self.headers["Content-Type"] = content_type
    def __enter__(self): return self
    def __exit__(self, *_): return False
    def getcode(self): return self.status
    def geturl(self): return "https://example.test/final"
    def read(self): return self.body


class FetchTests(unittest.TestCase):
    def test_success(self):
        result = fetch_url("https://example.test", opener=lambda *a, **k: FakeResponse(), pause=lambda _: None)
        self.assertEqual(result.http_status, 200)
        self.assertEqual(result.resolved_url, "https://example.test/final")
    def test_non_html_rejected(self):
        with self.assertRaisesRegex(FetchError, "Content-Type"):
            fetch_url("https://example.test", opener=lambda *a, **k: FakeResponse(content_type="application/pdf"), pause=lambda _: None)
    def test_empty_body_rejected(self):
        with self.assertRaisesRegex(FetchError, "為空"):
            fetch_url("https://example.test", opener=lambda *a, **k: FakeResponse(body=b" "), pause=lambda _: None)
    def test_404_not_retried(self):
        calls = []
        def fail(*args, **kwargs):
            calls.append(1)
            raise HTTPError("https://example.test", 404, "not found", Message(), io.BytesIO())
        with self.assertRaisesRegex(FetchError, "404"):
            fetch_url("https://example.test", opener=fail, pause=lambda _: None)
        self.assertEqual(len(calls), 1)
    def test_timeout_retries_are_bounded(self):
        calls = []
        def timeout(*args, **kwargs):
            calls.append(1)
            raise TimeoutError("slow")
        with self.assertRaisesRegex(FetchError, "網路擷取失敗"):
            fetch_url("https://example.test", retries=2, opener=timeout, pause=lambda _: None)
        self.assertEqual(len(calls), 3)


if __name__ == "__main__": unittest.main()
