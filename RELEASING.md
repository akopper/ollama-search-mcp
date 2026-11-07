# Releasing

Releases are published to PyPI by `.github/workflows/release.yml` using
[PyPI trusted publishing](https://docs.pypi.org/trusted-publishers/) (OIDC, no API
token stored in the repository).

## One-time PyPI setup

The first release needs a pending trusted publisher on PyPI:

1. Sign in at <https://pypi.org>.
2. Open <https://pypi.org/manage/account/publishing/>.
3. Add a pending publisher with exactly these values:

   | Field | Value |
   | --- | --- |
   | PyPI project name | `ollama-search-mcp` |
   | Owner | `akopper` |
   | Repository name | `ollama-search-mcp` |
   | Workflow name | `release.yml` |
   | Environment name | `pypi` |

After the first successful publish, the project exists and the trusted publisher is
listed under the project's publishing settings.

The GitHub environment `pypi` is created automatically on the first run. Add required
reviewers there if releases should need manual approval.

## Release steps

1. Update the version in `pyproject.toml` and `src/ollama_search_mcp/__init__.py`.
   Keep them identical.
2. Move the `Unreleased` entries in `CHANGELOG.md` into a new version section and add
   the release date.
3. Open a pull request and wait for the `test`, `build`, and `docker` checks.
4. Merge to `main`.
5. Create and push the tag, then publish a GitHub release:

   ```bash
   git checkout main && git pull --ff-only
   git tag -a v0.2.1 -m "v0.2.1"
   git push origin v0.2.1
   gh release create v0.2.1 --title v0.2.1 --notes-from-tag
   ```

   The release event triggers `release.yml`, which builds the sdist and wheel, runs
   `twine check`, and uploads to PyPI.
6. Verify:

   ```bash
   uvx ollama-search-mcp </dev/null
   pip index versions ollama-search-mcp
   ```

   The server reads stdio, so redirecting from `/dev/null` makes it exit cleanly.

## Container images

The `docker` job in `test.yml` publishes `ghcr.io/akopper/ollama-search-mcp`:

- `latest` on every push to `main`
- `X.Y.Z` and `X.Y` for tags matching `v*`

## Manual publish

`release.yml` also supports `workflow_dispatch` for retries. A manual run publishes the
artifacts built from the selected ref; make sure the ref matches the intended version.
