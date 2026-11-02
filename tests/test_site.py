"""Deployment checks for the built site's entry point and local HTML links."""

from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from urllib.parse import unquote, urlsplit

from build import build


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        self.urls.extend(value for key, value in attrs if key in ("href", "src") and value)


class SiteTests(unittest.TestCase):
    def test_built_site(self):
        with TemporaryDirectory() as temporary:
            output = build(Path(temporary) / "site")
            self.assertTrue((output / "index.html").is_file())
            self.assertTrue((output / ".nojekyll").is_file())
            for page in output.rglob("*.html"):
                contents = page.read_text(encoding="utf-8")
                self.assertIn("<title>", contents, f"Missing page title: {page.name}")
                parser = References()
                parser.feed(contents)
                for url in parser.urls:
                    with self.subTest(page=str(page.relative_to(output)), url=url):
                        parts = urlsplit(url)
                        if parts.scheme or parts.netloc or not parts.path:
                            continue
                        self.assertFalse(parts.path.startswith("/"), "Use relative URLs for /dprdb/ hosting")
                        target = (page.parent / unquote(parts.path)).resolve()
                        self.assertTrue(target.is_relative_to(output.resolve()), "Link escapes site")
                        if target.is_dir():
                            target /= "index.html"
                        self.assertTrue(target.is_file(), f"Broken local link: {url}")


if __name__ == "__main__":
    unittest.main()
