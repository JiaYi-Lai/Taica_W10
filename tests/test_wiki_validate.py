import unittest

from app.wiki.validate import validate_draft


class CitationValidationTests(unittest.TestCase):
    def setUp(self):
        self.evidence = [{"source_id": "S03", "paragraph_id": "p0001-a1", "text": "NFC data."}]
        self.draft = {"title": "NFC", "summary": "簡介。", "summary_refs": [
            {"source_id": "S03", "paragraph_id": "p0001-a1"}], "claims": [
            {"text": "NFC 可傳輸資料。", "source_refs": [
                {"source_id": "S03", "paragraph_id": "p0001-a1"}]}]}
        self.reviews = {"summary_supported": True, "summary_reason": "段落直接支持。",
                        "reviews": [{"claim_index": 0, "supported": True, "reason": "段落直接說明。"}]}

    def test_valid_claim_passes(self):
        self.assertEqual(validate_draft(self.draft, self.evidence, self.reviews)["status"], "passed")

    def test_unknown_source_or_paragraph_is_rejected(self):
        self.draft["claims"][0]["source_refs"][0]["source_id"] = "S99"
        report = validate_draft(self.draft, self.evidence, self.reviews)
        self.assertEqual(report["status"], "needs_review")
        self.assertIn("invalid_citation", {issue["type"] for issue in report["issues"]})

    def test_missing_citation_is_rejected(self):
        self.draft["claims"][0]["source_refs"] = []
        report = validate_draft(self.draft, self.evidence, self.reviews)
        self.assertIn("missing_citation", {issue["type"] for issue in report["issues"]})

    def test_unsupported_claim_is_rejected(self):
        self.reviews["reviews"][0]["supported"] = False
        report = validate_draft(self.draft, self.evidence, self.reviews)
        self.assertIn("unsupported_claim", {issue["type"] for issue in report["issues"]})

    def test_no_review_is_not_publishable(self):
        self.assertEqual(validate_draft(self.draft, self.evidence)["status"], "needs_review")


if __name__ == "__main__":
    unittest.main()
