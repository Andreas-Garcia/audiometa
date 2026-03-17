# Published docs bundle

The file `docs-bundle.json` in this directory is built by `scripts/build_docs_bundle.py`. It contains selected Markdown docs from `docs/` (see `DOC_SLUGS` in the script) with internal links rewritten to `/docs/<slug>` for consumption by the [Audiometa frontend](https://github.com/BehindTheMusicTree/audiometa-frontend).

The frontend fetches this bundle at build time and renders the content under its `/docs` section for SEO and AEO. A demo web app is available at [audiometa.themusictree.org](https://audiometa.themusictree.org).

## Rebuilding

- **Locally**: From the repo root, run `python3 scripts/build_docs_bundle.py`.
- **CI**: The workflow `.github/workflows/publish-docs-bundle.yml` builds the bundle and commits `publish/docs-bundle.json` when changed. It runs on:
  - Push to tags matching `v*`
  - Pushes that touch `docs/**` or `scripts/build_docs_bundle.py`
  - Manual run via `workflow_dispatch`
