"""Build the Sphinx/Shibuya landing page, failing on documentation warnings."""

from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent


def build(destination=None):
    source = ROOT / "docs"
    destination = Path(destination) if destination is not None else ROOT / "dist"
    destination = destination.resolve()
    if destination == ROOT or destination in ROOT.parents or destination == source or source in destination.parents:
        raise ValueError("Build output must not overwrite the repository or documentation source")
    if not (source / "index.md").is_file():
        raise FileNotFoundError("docs/index.md is required")
    # Build separately so a failed build preserves the last working preview.
    with TemporaryDirectory(prefix="dprdb-build-") as temporary:
        output = Path(temporary) / "html"
        subprocess.run([
            sys.executable, "-m", "sphinx", "-b", "html", "-W", "--keep-going",
            "-d", str(Path(temporary) / "doctrees"), str(source), str(output),
        ], check=True)
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(output, destination)
    return destination


if __name__ == "__main__":
    print(f"Built site in {build()}")
