# .github

## Purpose

GitHub Actions automation and dependency updates for the repository.

## Ownership

Owns CI checks, packaging verification, PyPI trusted publishing, container image
publishing, and Dependabot configuration.

## Local Contracts

- `.github/workflows/test.yml` (`Test & Build`) runs on pushes and pull requests to
  `main`, plus `v*` tag pushes. It has three jobs:
  - `test`: matrix of Python 3.10 and 3.13; `pip install -e ".[dev]"`, then
    `pytest --cov --cov-report=term-missing`, `ruff check src/ tests/`, and
    `ruff format --check src/ tests/`.
  - `build`: Python 3.13; `python -m build` and `python -m twine check dist/*`; uploads the
    `dist` artifact.
  - `docker`: runs only for `main` pushes and `v*` tags, after `test` and `build`; builds
    `linux/amd64` and `linux/arm64` for `ghcr.io/${{ github.repository }}`. Tags:
    `latest` on the default branch, `X.Y.Z` and `X.Y` for `v*` tags via
    `docker/metadata-action`.
- `.github/workflows/release.yml` (`Release`) runs on published GitHub releases and on
  `workflow_dispatch`. The `build` job produces and checks distributions; the `pypi` job
  downloads them and publishes with `pypa/gh-action-pypi-publish` using OIDC.
- The `pypi` job uses `environment: pypi` and `permissions: id-token: write`. Never add a
  PyPI API token, `PYPI_API_TOKEN`, or `TWINE_PASSWORD` secret.
- `.github/dependabot.yml` updates pip, GitHub Actions, and Docker dependencies weekly with
  a limit of five open pull requests per ecosystem.
- Only the built-in `GITHUB_TOKEN` is used for GHCR; no publishing secrets are stored.

## Work Guidance

- Keep the CI matrix anchored at the minimum supported Python (3.10) and the newest
  supported version (3.13) so old-syntax and new-syntax breakage both surface early.
- Add new checks to the existing `test` job instead of creating overlapping workflows.
- Keep the action versions on their current major tags; Dependabot raises PRs for bumps.
- Docker image names derive from the repository name; renames propagate automatically.
- Keep workflow triggers limited to `main` pushes, `v*` tags, pull requests to `main`, and
  published releases.
- Treat `release.yml` as the only publisher. Do not add a second publishing path.

## Verification

- Open a pull request and run `gh pr checks <number>`; `test` and `build` must pass (and
  `docker` when the trigger matches).
- Reproduce CI locally with `pytest --cov --cov-report=term-missing`, `ruff check src/
  tests/`, `ruff format --check src/ tests/`, `python -m build`, and
  `python -m twine check dist/*`.
- Validate workflow YAML before pushing: `python -c "import yaml,
  pathlib; [yaml.safe_load(pathlib.Path(p).read_text()) for p in
  pathlib.Path('.github/workflows').glob('*.yml')]"`.

## Child DOX Index

None.
