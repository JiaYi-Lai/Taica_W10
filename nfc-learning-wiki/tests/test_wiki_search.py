import json
import tempfile
import unittest
from pathlib import Path

from app.wiki.search import rebuild_index, search_articles


class WikiSearchTests(unittest.TestCase):
    def test_search_returns_article_summary_and_sources(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            wiki = root / "wiki"
            wiki.mkdir()
            (wiki / "ch01-nfc.md").write_text("# NFC 基礎\nNFC 可交換 NDEF 資料。", encoding="utf-8")
            (wiki / "ch01-nfc.json").write_text(json.dumps({
                "article_id": "ch01-nfc", "title": "NFC 基礎", "summary": "近場通訊入門",
                "source_ids": ["S03"], "validation_status": "passed",
            }, ensure_ascii=False), encoding="utf-8")
            db = root / "index" / "wiki.sqlite"
            mode = rebuild_index(wiki, db)
            result = search_articles("NFC", db_path=db)
            self.assertIn(mode, {"fts5", "like"})
            self.assertEqual(result[0]["article_id"], "ch01-nfc")
            self.assertEqual(result[0]["source_ids"], ["S03"])

    def test_unverified_articles_are_not_indexed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            wiki = root / "wiki"
            wiki.mkdir()
            (wiki / "draft.md").write_text("NFC", encoding="utf-8")
            (wiki / "draft.json").write_text(json.dumps({
                "article_id": "draft", "title": "NFC", "summary": "draft",
                "source_ids": [], "validation_status": "needs_review",
            }), encoding="utf-8")
            db = root / "wiki.sqlite"
            rebuild_index(wiki, db)
            self.assertEqual(search_articles("NFC", db_path=db), [])


if __name__ == "__main__":
    unittest.main()
