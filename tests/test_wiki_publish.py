import tempfile
import unittest
from pathlib import Path

from app.wiki.publish import publish_article


class WikiPublishTests(unittest.TestCase):
    def test_only_passed_articles_publish_with_references(self):
        draft = {"title": "NFC 入門", "summary": "摘要", "summary_refs": [
            {"source_id": "S03", "paragraph_id": "p0001-a1"}], "claims": [
            {"text": "NFC 交換資料。", "source_refs": [
                {"source_id": "S03", "paragraph_id": "p0001-a1"}]}]}
        evidence = [{"source_id": "S03", "paragraph_id": "p0001-a1", "url": "https://example.test/nfc",
                     "organization": "Official", "title": "NFC docs", "sha256": "abc"}]
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "只有"):
                publish_article(article_id="ch01-nfc", chapter="chapter-1", draft=draft,
                    evidence=evidence, validation={"status": "needs_review"}, run_id="run",
                    wiki_dir=Path(folder))
            md, metadata = publish_article(article_id="ch01-nfc", chapter="chapter-1", draft=draft,
                evidence=evidence, validation={"status": "passed"}, run_id="run", wiki_dir=Path(folder))
            self.assertIn("S03 · p0001-a1", md.read_text(encoding="utf-8"))
            self.assertEqual(__import__("json").loads(metadata.read_text(encoding="utf-8"))["source_ids"], ["S03"])

    def test_model_markup_is_rendered_as_inert_text(self):
        draft = {"title": "NFC", "summary": "摘要", "summary_refs": [
            {"source_id": "S03", "paragraph_id": "p0001-a1"}], "claims": [
            {"text": "<script>alert(1)</script> [click](javascript:alert(1)) **bold**",
             "source_refs": [{"source_id": "S03", "paragraph_id": "p0001-a1"}]}]}
        evidence = [{"source_id": "S03", "paragraph_id": "p0001-a1", "url": "https://example.test/nfc",
                     "organization": "Official", "title": "NFC docs", "sha256": "abc"}]
        with tempfile.TemporaryDirectory() as folder:
            md, _ = publish_article(article_id="ch01-nfc", chapter="chapter-1", draft=draft,
                evidence=evidence, validation={"status": "passed"}, run_id="run", wiki_dir=Path(folder))
            text = md.read_text(encoding="utf-8")
            self.assertNotIn("<script>", text)
            self.assertNotIn("[click]", text)
            self.assertNotIn("**bold**", text)


if __name__ == "__main__":
    unittest.main()
