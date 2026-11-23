import json
import tempfile
import unittest
from pathlib import Path

from app.ingest.metadata import duplicate_of, load_sources, save_sources, sha256_hex
from app.ingest.models import Source


class MetadataTests(unittest.TestCase):
    def test_hash_and_duplicate(self):
        a = Source("A", "a", "org", "https://example.test/a", sha256=sha256_hex("same"))
        b = Source("B", "b", "org", "https://example.test/b", sha256=sha256_hex("same"))
        self.assertEqual(len(a.sha256), 64)
        self.assertEqual(duplicate_of(b, [a, b]).source_id, "A")
    def test_registry_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sources.json"
            original = [Source("S01", "NFC", "org", "https://example.test")]
            save_sources(path, original)
            restored = load_sources(path)
            self.assertEqual(restored[0].source_id, "S01")
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["sources"][0]["ingest_status"], "pending")


if __name__ == "__main__": unittest.main()
