# DPRDB

The DaBois Fantasy League Archives, built with **Sphinx**, the **Shibuya** theme,
and **MyST Markdown**. The landing page follows the original design at
https://www.dprdb.com/: a pale background, large league heading, and three colored
league cards with the original logos and footer links.

The cards open local DBA, DFL, and DLB sections. Each league has eight pages:
Managers, Standings, News, Championship History, Franchise History, Season History,
Playoff History, and Awards. All section pages contain only their heading.
A league selector keeps the current section when switching leagues. The sidebar
shows only the selected league's sections and an **All leagues** link.

## Local development

Use Python 3.13 or newer. From the repository root, set up dependencies once:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

With the virtual environment active, build and preview:

```sh
python3 -m server localhost:6700
```

Open http://localhost:6700. Stop with Ctrl+C. After edits, restart the command
and refresh the browser. The preview does not automatically reload.

To build and serve separately:

```sh
python3 build.py
python3 -m http.server 6700 --bind localhost --directory dist
```

## Editing the site

- `docs/_templates/dprdb-home.html`: landing-page markup and local league links.
- `docs/_static/landing.css`: the original DPRDB landing design with mobile,
  keyboard-focus, and reduced-motion refinements.
- `docs/dba/`, `docs/dfl/`, `docs/dlb/`: blank Markdown pages ready for content.
- `docs/conf.py`: theme settings, league names, and the ordered list of sections.
- `docs/index.md`: the root document and hidden site navigation tree.
- `docs/_templates/partials/league-picker.html`: section-preserving league selector.
- `docs/_templates/partials/globaltoc-above.html`: selected-league sidebar.
- `docs/_static/archive.css`: content-page styling.
- `docs/_static/league-selector.js`: league navigation behavior.
- `docs/_static/logos/`: original league SVGs from www.dprdb.com.

The Sphinx build runs with warnings treated as errors and generates relative
asset paths suitable for GitHub Pages at `/dprdb/`. It builds into a temporary
folder first, then replaces `dist/` only after success. Generated files and the
virtual environment are ignored by Git. Website visitors do not need Python.

## Checks and deployment

```sh
python3 -m unittest discover -s tests -v
python3 build.py
```

The tests build the site and check homepage content, all 24 section routes,
league selector destinations, local links and assets, and the Pages marker.
Browser checks cover switching leagues and responsive navigation. The automated
tests do not validate external sites or execute JavaScript.

The GitHub Actions workflow runs **test → build → deploy**. Both test and build
jobs install the pinned dependencies in `requirements.txt`. Warnings, test
failures, or build failures prevent deployment.

- Pull requests targeting `main` run tests and build without publishing.
- Pushes to `main` deploy after successful tests and build.
- Manual workflow runs deploy only from `main`.
- Separate CI workflows do not automatically block this deployment. Add required
  jobs to this workflow's dependency chain as checks grow.

GitHub Pages is configured to use **GitHub Actions** under
https://github.com/aevjotcham/dprdb/settings/pages. After committing and pushing,
watch **Test, build, and deploy Pages** in the Actions tab. The site is hosted at
https://aevjotcham.github.io/dprdb/.

## References

- [Sphinx](https://www.sphinx-doc.org/)
- [Shibuya](https://shibuya.lepture.com/)
- [MyST Markdown](https://myst-parser.readthedocs.io/)
- [GitHub Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
