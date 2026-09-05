"""Regression checks for publication counts and offline asset releases."""
import importlib.util
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]


class ReconciliationTests(unittest.TestCase):
    def test_only_launch_buttons_count(self):
        launch = runpy.run_path(str(SCRIPTS / "audit-tool-ette-promises.py"))["launch_urls"]
        url = "https://chatgpt.com/g/g-123abc"
        self.assertEqual(launch(f'<a href="{url}">Sibling</a><a href="/">Launch</a>'), [])
        for classes in ("btn btn-primary", "button primary", "btn"):
            self.assertEqual(launch(f"<a href='{url}' class='{classes}'>Launch</a>"), [url])
        self.assertEqual(launch('<a class="btn" href="https://chatgpt.com/g/g-YOUR-GPT-ID-HERE">Launch</a>'), [])

    def test_worker_changes_when_precached_asset_changes(self):
        spec = importlib.util.spec_from_file_location("sync_css", SCRIPTS / "sync-css-version.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            css = root / "assets/css/theme.css"
            css.parent.mkdir(parents=True)
            css.write_text("body {}\n")
            (root / "index.html").write_text('<link href="/assets/css/theme.css?v=old">')
            asset = root / "asset.js"
            asset.write_text("one")
            worker = root / "sw.js"
            worker.write_text('const CACHE_NAME = "glee-fully-shell-v1";\nconst PRECACHE_URLS = ["/", "/asset.js"];\n')
            with patch.object(module, "REPO", root), patch.object(module, "THEME_CSS", css):
                with patch.object(sys, "argv", ["sync-css-version.py"]):
                    self.assertEqual(module.main(), 0)
                before = worker.read_bytes()
                asset.write_text("two")
                with patch.object(sys, "argv", ["sync-css-version.py", "--check"]):
                    self.assertEqual(module.main(), 1)
                    self.assertEqual(worker.read_bytes(), before)
                with patch.object(sys, "argv", ["sync-css-version.py"]):
                    self.assertEqual(module.main(), 0)
                    self.assertNotEqual(worker.read_bytes(), before)
                    synced = worker.read_bytes()
                    self.assertEqual(module.main(), 0)
                    self.assertEqual(worker.read_bytes(), synced)


if __name__ == "__main__":
    unittest.main()
