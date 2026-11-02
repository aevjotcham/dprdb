# DPRDB

A static website published to GitHub Pages after its tests and build pass.
Python 3.9 or newer is required locally; no packages need to be installed.

## Local development

Edit the website in `site/`, then run from the repository root:

```sh
python3 -m server localhost:6700
```

Open http://localhost:6700. This command rebuilds `dist/` and serves it.
After editing source files, stop with Ctrl+C and run the command again, then
refresh your browser. It does not watch files or automatically reload the page.

The equivalent separate build and standard-library server commands are:

```sh
python3 build.py
python3 -m http.server 6700 --bind localhost --directory dist
```

Python's built-in module is `http.server`; `server.py` provides the shorter
custom command above. HTTP serving itself does not compile or build a site.
This project builds by copying the static source into a clean `dist/` folder.
GitHub Pages serves HTML, CSS, JavaScript and other static files; it does not
run a Python backend.

## Enable GitHub Pages once

1. Open https://github.com/aevjotcham/dprdb/settings/pages.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Commit these files and push them to `main`:

   ```sh
   git add .gitignore .github/workflows/pages.yml README.md build.py server.py site tests
   git commit -m "Set up tested GitHub Pages deployment and local preview"
   git push -u origin main
   ```

4. Watch the **Actions** tab for **Test, build, and deploy Pages**.
5. After successful deployment, open https://aevjotcham.github.io/dprdb/.

Pages availability depends on repository visibility and your GitHub plan.
If the `github-pages` environment requires reviewers, deployments also wait
for their approval. For unattended deployment, configure that environment
to permit `main` without required reviewers.

## How CI and deployment work

- Pull requests targeting `main` run tests and build the site without deploying.
- Pushes to `main` (including merged pull requests) run tests, build, and deploy.
- Failed tests or builds block deployment; the last successful site stays live.
- Manual runs from the Actions tab deploy only when run on `main`.
- Local commits trigger nothing until pushed to GitHub.

Run the same checks locally:

```sh
python3 -m unittest discover -s tests -v
python3 build.py
```

The initial checks verify that the built entry page exists, HTML pages have
titles, and local `href`/`src` references resolve within the site. They do not
check external links, CSS URLs, JavaScript behavior, or accessibility.
Add application-specific tests to `tests/` as the site grows.

The workflow's `needs` dependencies enforce **test → build → deploy**.
If you add other CI jobs that must block publication, include those jobs in
the dependency chain. Separate workflows are not automatically deployment gates.
You can also protect `main` with a repository ruleset requiring the **Test site**
check before merging.

Use relative asset paths (for example `./assets/style.css`) so they work both
locally and under the deployed `/dprdb/` path. Only files in `site/` are published.
The generated `dist/` directory is ignored by Git.

References: [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
and [Python HTTP server](https://docs.python.org/3/library/http.server.html).
