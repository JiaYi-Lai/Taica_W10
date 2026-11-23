import json
import tempfile
import unittest
from pathlib import Path

from app.wiki.runlog import record_wiki_operation


class WikiRunLogTests(unittest.TestCase):
    def test_records_structured_run_and_appends_markdown_entry(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "wiki").mkdir()
            log = root / "wiki/log.md"
            log.write_text("# log\n", encoding="utf-8")
            started = "2026-11-23T10:00:00+00:00"
            record = record_wiki_operation(operation="lint", status="passed",
                input_refs=["wiki/index.md"], output_refs=["wiki/index.md"],
                validation={"errors": 0}, project_dir=root, started_at=started)
            payload = json.loads((root / record["run_path"]).read_text(encoding="utf-8"))
            self.assertEqual(payload["started_at"], started)
            self.assertIn("lint", log.read_text(encoding="utf-8"))
            self.assertEqual(len(list((root / "data/runs").glob("*.json"))), 1)


if __name__ == "__main__":
    unittest.main()
