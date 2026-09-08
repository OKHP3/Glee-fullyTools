import importlib.util
import sys
from contextlib import redirect_stdout
from io import StringIO
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "check-links.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("check_links", SCRIPT)
check_links = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_links)


class FragmentLinkTests(unittest.TestCase):
    def test_parser_ignores_comments_and_data_ids(self):
        parser = check_links.PageLinks()
        parser.feed('<!-- <a href="missing.html#nope"> --> <div data-id="fake"></div>')
        self.assertEqual(parser.hrefs, [])
        self.assertEqual(parser.fragments, set())

    def test_same_document_and_cross_page_fragments_are_exact(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.html"
            target = root / "target.html"
            source.write_text('<h1 id="Résumé">x</h1><a name="legacy">x</a>')
            target.write_text('<h1 id="CaseSensitive">x</h1>')
            parser = check_links.PageLinks()
            parser.feed(source.read_text())
            self.assertTrue(check_links.resolves("#R%C3%A9sum%C3%A9", source, parser.fragments))
            self.assertTrue(check_links.resolves("#legacy", source, parser.fragments))
            self.assertFalse(check_links.resolves("#résumé", source, parser.fragments))
            self.assertTrue(check_links.resolves("target.html#CaseSensitive", source, parser.fragments))
            self.assertFalse(check_links.resolves("target.html#casesensitive", source, parser.fragments))

    def test_empty_top_and_text_fragments_are_browser_directives(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.html"
            source.write_text("<p>source</p>")
            parser = check_links.PageLinks()
            parser.feed(source.read_text())
            for href in ("#", "#top", "#:~:text=source"):
                self.assertTrue(check_links.resolves(href, source, parser.fragments))

    def test_protocol_relative_and_non_html_fragments(self):
        self.assertTrue(check_links.is_external("//cdn.example/site.css"))
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.html"
            pdf = Path(temp) / "guide.pdf"
            source.write_text("<p>source</p>")
            pdf.write_bytes(b"%PDF")
            parser = check_links.PageLinks()
            parser.feed(source.read_text())
            self.assertTrue(check_links.resolves("guide.pdf#page=2", source, parser.fragments))

    def test_main_reports_missing_fragments_and_resources(self):
        original_root = check_links.ROOT
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "index.html").write_text(
                '<link href="missing.css"><a href="index.html#missing">bad</a>'
            )
            (root / "sitemap.xml").write_text("<urlset></urlset>")
            check_links.ROOT = root
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(check_links.main(["--no-report"]), 1)
            self.assertIn("missing.css", output.getvalue())
            self.assertIn("index.html#missing", output.getvalue())
        check_links.ROOT = original_root


if __name__ == "__main__":
    unittest.main()
