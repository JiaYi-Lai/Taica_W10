import json
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
            self.assertTrue((data_dir / "raw/S01" / source.sha256 / "source.html").exists())
            self.assertTrue((data_dir / "raw/S01" / source.sha256 / "metadata.json").exists())
            self.assertTrue((data_dir / "cleaned/S01" / f"{source.sha256}.json").exists())
            self.assertTrue(list((data_dir / "runs").glob("*.json")))
            self.assertEqual(source.ingest_status, "success")

    def test_raw_snapshot_is_versioned_and_never_overwritten(self):
        first_body = ("<html><main><p>" + "NFC near field communication. " * 12 + "</p></main></html>").encode()
        second_body = ("<html><main><p>" + "NFC technology data exchange. " * 12 + "</p></main></html>").encode()
        source = Source("S01", "NFC", "Official", "https://example.test/nfc")
        def make_fetcher(body):
            return lambda url: FetchResult(body, url, "text/html", 200, "2026-11-23T00:00:00+00:00")
        with tempfile.TemporaryDirectory() as folder:
            data_dir = Path(folder) / "data"
            ingest_sources([source], data_dir, fetcher=make_fetcher(first_body))
            first_path = data_dir.parent / source.raw_path
            first_hash = source.sha256
            ingest_sources([source], data_dir, fetcher=make_fetcher(second_body))
            second_path = data_dir.parent / source.raw_path
            self.assertNotEqual(first_hash, source.sha256)
            self.assertEqual(first_path.read_bytes(), first_body)
            self.assertEqual(second_path.read_bytes(), second_body)
            self.assertTrue(first_path.exists())

    def test_single_source_run_preserves_the_full_registry(self):
        body = ("<html><main><p>" + "NFC registry preservation. " * 12 + "</p></main></html>").encode()
        first = Source("S01", "NFC", "Official", "https://example.test/nfc")
        other = Source("S02", "Other NFC", "Official", "https://example.test/other")
        with tempfile.TemporaryDirectory() as folder:
            data_dir = Path(folder) / "data"
            fetcher = lambda url: FetchResult(body, url, "text/html", 200, "2026-11-23T00:00:00+00:00")
            ingest_sources([first], data_dir, fetcher=fetcher, registry_sources=[first, other])
            saved = json.loads((data_dir / "sources.json").read_text(encoding="utf-8"))
            self.assertEqual([item["source_id"] for item in saved["sources"]], ["S01", "S02"])

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
