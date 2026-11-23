import json
import tempfile
import unittest
from pathlib import Path

from app.wiki.lint import lint_wiki


class WikiLintTests(unittest.TestCase):
    def make_project(self, root: Path):
        (root / "data").mkdir()
        (root / "wiki/concepts").mkdir(parents=True)
        (root / "data/sources.json").write_text(json.dumps({"sources": []}), encoding="utf-8")
        (root / "wiki/log.md").write_text("# append-only\n", encoding="utf-8")

    def test_valid_empty_wiki_skeleton_passes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.make_project(root)
            (root / "wiki/index.md").write_text("# Index\n\n- [Overview](./overview.md)\n", encoding="utf-8")
            (root / "wiki/overview.md").write_text(
                "---\nid: overview\ntitle: Overview\ntype: overview\nupdated_at: 2026-11-23\nsources: []\n---\n\n# Overview\n",
                encoding="utf-8")
            report = lint_wiki(project_dir=root)
            self.assertEqual(report["status"], "passed")
            self.assertEqual(report["pages_checked"], 1)

    def test_broken_relative_link_is_error(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.make_project(root)
            (root / "wiki/index.md").write_text("# Index\n\n- [Overview](./overview.md)\n", encoding="utf-8")
            (root / "wiki/overview.md").write_text(
                "---\nid: overview\ntitle: Overview\ntype: overview\nupdated_at: 2026-11-23\nsources: []\n---\n\n# Overview\n\n[Missing](./missing.md)\n",
                encoding="utf-8")
            report = lint_wiki(project_dir=root)
            self.assertEqual(report["status"], "failed")
            self.assertIn("broken_link", {item["type"] for item in report["issues"]})


if __name__ == "__main__":
    unittest.main()
