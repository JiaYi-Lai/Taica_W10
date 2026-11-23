import json
import tempfile
import unittest
from pathlib import Path

from app.wiki.search import search_articles
from app.wiki.workflow import run_article_workflow


class FakeProvider:
    model = "test-model"
    def __init__(self, supported=True):
        self.calls = []
        self.supported = supported
    def complete_json(self, system, user):
        self.calls.append((system, user))
        if len(self.calls) == 1:
            return {"title": "NFC 基礎", "summary": "初學者認識 NFC 與 NDEF。",
                    "summary_refs": [{"source_id": "S03", "paragraph_id": "p0001-abcd"}], "claims": [
                {"text": "Android NFC 文件介紹 NDEF 資料交換。", "source_refs": [
                    {"source_id": "S03", "paragraph_id": "p0001-abcd"}]}]}
        return {"summary_supported": self.supported, "summary_reason": "摘要核對。",
                "reviews": [{"claim_index": 0, "supported": self.supported,
                             "reason": "來源直接支持。" if self.supported else "來源沒有支持。"}]}


class WikiWorkflowTests(unittest.TestCase):
    def make_data(self, root):
        data = root / "data"
        (data / "cleaned").mkdir(parents=True)
        (data / "sources.json").write_text(json.dumps({"sources": [{
            "source_id": "S03", "title": "NFC basics", "organization": "Android Developers",
            "original_url": "https://developer.android.com/nfc",
            "resolved_url": "https://developer.android.com/nfc", "sha256": "a" * 64,
            "ingest_status": "success", "cleaned_path": "data/cleaned/S03.json",
        }]}), encoding="utf-8")
        (data / "cleaned/S03.json").write_text(json.dumps({"source_id": "S03", "paragraphs": [
            {"paragraph_id": "p0001-abcd", "text": "Android NFC uses NDEF to exchange NFC messages."},
        ]}), encoding="utf-8")
        return data

    def test_passed_draft_publishes_indexes_and_is_searchable(self):
        with tempfile.TemporaryDirectory() as folder:
            data = self.make_data(Path(folder))
            provider = FakeProvider()
            result = run_article_workflow(article_id="ch01-nfc", title="NFC 基礎",
                chapter="chapter-1", query="NFC NDEF Android", data_dir=data, provider=provider)
            self.assertEqual(result["status"], "passed")
            self.assertEqual(len(provider.calls), 2)
            self.assertTrue((data / "wiki/ch01-nfc.md").exists())
            hits = search_articles("NFC", db_path=data / "index/wiki.sqlite")
            self.assertEqual(hits[0]["article_id"], "ch01-nfc")

    def test_unsupported_draft_is_saved_for_review_but_not_published(self):
        with tempfile.TemporaryDirectory() as folder:
            data = self.make_data(Path(folder))
            result = run_article_workflow(article_id="ch01-nfc", title="NFC 基礎",
                chapter="chapter-1", query="NFC NDEF Android", data_dir=data,
                provider=FakeProvider(supported=False))
            self.assertEqual(result["status"], "needs_review")
            self.assertTrue((data / "drafts" / Path(result["draft_path"]).name).exists())
            self.assertFalse((data / "wiki/ch01-nfc.md").exists())


if __name__ == "__main__":
    unittest.main()
