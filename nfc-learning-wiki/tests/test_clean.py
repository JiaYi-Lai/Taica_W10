import unittest

from app.ingest.clean import clean_html


class CleanTests(unittest.TestCase):
    def test_removes_navigation_and_keeps_article_paragraphs(self):
        html = "<nav>Menu Cookie</nav><main><h1>NFC</h1><p>" + ("NFC content. " * 15) + "</p><footer>Footer</footer></main>"
        result = clean_html(html)
        self.assertNotIn("Menu", result.text)
        self.assertNotIn("Footer", result.text)
        self.assertIn("NFC content", result.text)
        self.assertTrue(result.paragraphs[0]["paragraph_id"].startswith("p0001-"))
    def test_empty_and_short_rejected(self):
        with self.assertRaisesRegex(ValueError, "空"):
            clean_html("<script>not body</script>")
        with self.assertRaisesRegex(ValueError, "過短"):
            clean_html("<p>short</p>")


if __name__ == "__main__": unittest.main()
