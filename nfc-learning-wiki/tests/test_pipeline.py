import tempfile
import unittest
from pathlib import Path

from app.ingest.models import FetchResult, Source
from app.ingest.pipeline import ingest_sources


class PipelineTests(unittest.TestCase):
    def test_success_persists_raw_cleaned_metadata_and_run(self):
        body = ("<html><main><h1>NFC</h1><p>" + "NFC is near field communication. " * 12 +
                "</p></main></html>").encode()
        source = Source("S01", "NFC", "Official", "https://example.test/nfc")
        def fetcher(url):
            return FetchResult(body, url, "text/html", 200, "2026-11-23T00:00:00+00:00")
        with tempfile.TemporaryDirectory() as folder:
            data_dir = Path(folder) / "data"
            report = ingest_sources([source], data_dir, fetcher=fetcher)
            self.assertEqual(report["summary"]["success"], 1)
            self.assertTrue((data_dir / "raw/S01.html").exists())
            self.assertTrue((data_dir / "cleaned/S01.json").exists())
            self.assertTrue(list((data_dir / "runs").glob("*.json")))
            self.assertEqual(source.ingest_status, "success")

    def test_duplicate_hash_does_not_count_as_second_success(self):
        body = ("<html><main><p>" + "NFC technology near field communication. " * 12 +
                "</p></main></html>").encode()
        sources = [Source("S01", "one", "Official", "https://example.test/1"),
                   Source("S02", "two", "Official", "https://example.test/2")]
        def fetcher(url):
            return FetchResult(body, url, "text/html", 200, "2026-11-23T00:00:00+00:00")
        with tempfile.TemporaryDirectory() as folder:
            report = ingest_sources(sources, Path(folder) / "data", fetcher=fetcher)
        self.assertEqual(report["summary"]["success"], 1)
        self.assertEqual(report["summary"]["duplicate"], 1)


if __name__ == "__main__": unittest.main()
