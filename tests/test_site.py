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
        self.ids = set()
        self.options = []

    def handle_starttag(self, tag, attrs):
        self.urls.extend(value for key, value in attrs if key in ("href", "src") and value)
        self.ids.update(value for key, value in attrs if key == "id" and value)
        if tag == "option":
            option = dict(attrs)
            self.options.append(option)
            self.urls.append(option["value"])


class SiteTests(unittest.TestCase):
    def test_built_site(self):
        with TemporaryDirectory() as temporary:
            output = build(Path(temporary) / "site")
            self.assertTrue((output / "index.html").is_file())
            self.assertTrue((output / ".nojekyll").is_file())
            sections = ("managers", "standings", "news", "championship-history",
                        "franchise-history", "season-history", "playoff-history", "awards")
            expected = {"index.html", "search.html"} | {
                f"{league}/{section}.html"
                for league in ("dba", "dfl", "dlb") for section in sections
            }
            self.assertEqual({p.relative_to(output).as_posix() for p in output.rglob("*.html")}, expected)
            homepage = (output / "index.html").read_text(encoding="utf-8")
            for text in (
                "DaBois Fantasy League Archives", "Select A League",
                "Best viewed on desktop. Mobile layout is still in progress.",
                "DaBois Basketball Association", "DaBois Football League",
                "DaBois League Baseball",
            ):
                self.assertIn(text, homepage)
            for league in ("dba", "dfl", "dlb"):
                self.assertIn(f'{league}/managers.html', homepage)
            self.assertTrue((output / "searchindex.js").is_file())
            for page in output.rglob("*.html"):
                contents = page.read_text(encoding="utf-8")
                self.assertIn("<title>", contents, f"Missing page title: {page.name}")
                parser = References()
                parser.feed(contents)
                if page.parent.name in ("dba", "dfl", "dlb"):
                    self.assertEqual(len(parser.options), 3)
                    selected = [o for o in parser.options if "selected" in o]
                    self.assertEqual(len(selected), 1)
                    # The selector must stay in the same section in every league.
                    destinations = {
                        ((page.parent / o["value"]).resolve() if o["value"] != "#" else page.resolve())
                        for o in parser.options
                    }
                    self.assertEqual(destinations, {(output / league / page.name).resolve()
                                                  for league in ("dba", "dfl", "dlb")})
                for url in parser.urls:
                    with self.subTest(page=str(page.relative_to(output)), url=url):
                        parts = urlsplit(url)
                        if parts.scheme or parts.netloc:
                            continue
                        self.assertFalse(parts.path.startswith("/"), "Use relative URLs for /dprdb/ hosting")
                        target = (page.parent / unquote(parts.path)).resolve() if parts.path else page.resolve()
                        self.assertTrue(target.is_relative_to(output.resolve()), "Link escapes site")
                        if target.is_dir():
                            target /= "index.html"
                        self.assertTrue(target.is_file(), f"Broken local link: {url}")
                        if parts.fragment and target.suffix == ".html":
                            linked_page = References()
                            linked_page.feed(target.read_text(encoding="utf-8"))
                            self.assertIn(unquote(parts.fragment), linked_page.ids, f"Broken anchor: {url}")


if __name__ == "__main__":
    unittest.main()
