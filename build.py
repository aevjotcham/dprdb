"""Build the static website using only Python's standard library."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent


def build(destination=None):
    source = ROOT / "site"
    destination = Path(destination) if destination is not None else ROOT / "dist"
    if not (source / "index.html").is_file():
        raise FileNotFoundError("site/index.html is required")
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    (destination / ".nojekyll").touch()
    return destination


if __name__ == "__main__":
    print(f"Built site in {build()}")
