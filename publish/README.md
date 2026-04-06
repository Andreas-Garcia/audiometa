# Published docs bundle

The file `docs-bundle.json` in this directory is built by `scripts/build_docs_bundle.py`. It contains selected Markdown docs from `docs/` (see `DOC_SLUGS` in the script) with internal links rewritten to `/docs/<slug>` for consumption by the [Audiometa frontend](https://github.com/BehindTheMusicTree/audiometa-frontend).

**Published location (canonical URL):** The bundle is committed in this repo and consumed at the organization/repo path. The frontend should fetch it from a stable URL, for example:

- **Branch:** `https://raw.githubusercontent.com/BehindTheMusicTree/audiometa/main/publish/docs-bundle.json`
- **Tag (e.g. release):** `https://raw.githubusercontent.com/BehindTheMusicTree/audiometa/v1.3.0/publish/docs-bundle.json`

Using a tag URL is recommended for production so the frontend gets a pinned version. The path `publish/` is used (not `dist/`) because `dist/` is reserved for Python package build output (wheels, sdists) and is gitignored.

The frontend fetches this bundle at build time and renders the content under its `/docs` section for SEO and AEO. A demo web app is available at [audiometa.themusictree.org](https://audiometa.themusictree.org).

## Rebuilding

- **Locally**: From the repo root, run `python3 scripts/build_docs_bundle.py`.
- **CI**: The workflow `.github/workflows/publish-docs-bundle.yml` builds the bundle and commits `publish/docs-bundle.json` when changed. It runs on:

  - Push to tags matching `v*` (when `docs/**` or `scripts/build_docs_bundle.py` changed on that tag’s tree)
  - Manual run via `workflow_dispatch`

  **Pushing to `main`:** `GITHUB_TOKEN` cannot bypass branch protection/rulesets the way a user with **Maintain** permission can. Either:

  1. **Optional PAT (direct push):** Add a repository secret named `DOCS_BUNDLE_PUSH_PAT` whose value is a **fine-grained personal access token** (or classic PAT) for an account that may push to `main` under your rules (e.g. yours or a bot). Scope: this repository only, **Contents: Read and write**. If the org uses SAML SSO, authorize the token for the org. When this secret is set, the workflow checks out with that token and runs `git push origin HEAD:main` after committing the bundle.

  2. **No PAT (pull request):** If the secret is unset, the workflow force-pushes to `chore/update-docs-bundle` and opens a PR to `main` when needed; merge after CI passes so `main` stays the canonical raw URL above.
