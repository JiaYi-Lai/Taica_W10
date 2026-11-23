import tempfile
import unittest
from pathlib import Path

from app.wiki.query import select_wiki_context


class WikiContextTests(unittest.TestCase):
    def test_reads_index_then_selected_wiki_pages_only(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            wiki = root / "wiki"
            (wiki / "concepts").mkdir(parents=True)
            (wiki / "index.md").write_text(
                "# Index\n- [NDEF](./concepts/ndef.md) — NDEF messages and records.\n"
                "- [Overview](./overview.md) — Wiki map.\n- [Legacy](../data/wiki/old.md)\n", encoding="utf-8")
            (wiki / "overview.md").write_text(
                "---\nid: overview\ntitle: Overview\ntype: overview\nupdated_at: 2026-11-23\nsources: []\n---\n# Overview\n",
                encoding="utf-8")
            (wiki / "concepts/ndef.md").write_text(
                "---\nid: ndef\ntitle: NDEF\ntype: concept\nupdated_at: 2026-11-23\nsources:\n  - S03\n---\n# NDEF\n",
                encoding="utf-8")
            result = select_wiki_context("NDEF records", project_dir=root, max_pages=3)
            self.assertEqual(result["index_path"], "wiki/index.md")
            self.assertTrue(any(page["path"] == "wiki/concepts/ndef.md" for page in result["pages_read"]))
            self.assertFalse(any("data/wiki/old.md" in page["path"] for page in result["pages_read"]))
            self.assertFalse(result["knowledge_gap"])

    def test_chinese_terms_select_matching_indexed_page(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            wiki = root / "wiki"
            concepts = wiki / "concepts"
            concepts.mkdir(parents=True)
            (wiki / "index.md").write_text(
                "# Index\n- [NFC 安全入門](./concepts/security.md) — NDEF 驗證與應用程式風險。\n",
                encoding="utf-8")
            (wiki / "overview.md").write_text(
                "---\nid: overview\ntitle: 概觀\ntype: overview\nupdated_at: 2026-11-23\nsources: []\n---\n# 概觀\n",
                encoding="utf-8")
            (concepts / "security.md").write_text(
                "---\nid: security\ntitle: NFC 安全\ntype: concept\nupdated_at: 2026-11-23\nsources:\n  - S09\n---\n# NFC 安全\n",
                encoding="utf-8")
            result = select_wiki_context("NFC 安全 NDEF 驗證", project_dir=root, max_pages=3)
            self.assertTrue(any(page["path"] == "wiki/concepts/security.md" for page in result["pages_read"]))

    def test_unmatched_query_reports_knowledge_gap(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            wiki = root / "wiki"
            wiki.mkdir()
            (wiki / "index.md").write_text(
                "# Index\n- [NFC 基礎](./nfc.md) — NFC short range wireless basics.\n",
                encoding="utf-8")
            (wiki / "overview.md").write_text(
                "---\nid: overview\ntitle: Overview\ntype: overview\nupdated_at: 2026-11-23\nsources: []\n---\n# Overview\n",
                encoding="utf-8")
            (wiki / "nfc.md").write_text(
                "---\nid: nfc\ntitle: NFC\ntype: concept\nupdated_at: 2026-11-23\nsources:\n  - S05\n---\n# NFC\n",
                encoding="utf-8")
            result = select_wiki_context("quantum teleportation", project_dir=root, max_pages=3)
            self.assertTrue(result["knowledge_gap"])
            self.assertEqual([page["path"] for page in result["pages_read"]], ["wiki/overview.md"])


if __name__ == "__main__":
    unittest.main()
