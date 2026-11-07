# .github

## Purpose

GitHub Actions automation for the repository.

## Ownership

Owns CI checks and container image publishing.

## Local Contracts

- `.github/workflows/test.yml` runs on pushes and pull requests targeting `main`.
- The `test` job uses Python 3.10, installs with `pip install -e ".[dev]"`, then runs `pytest`
  and `ruff check src/ tests/`.
- The `docker` job runs only for pushes to `main`, builds `linux/amd64` and `linux/arm64`, and
  pushes `ghcr.io/${{ github.repository }}:latest`.
- Only the built-in `GITHUB_TOKEN` is used; do not add publishing secrets.

## Work Guidance

- Keep CI on the minimum supported Python (3.10) so newer syntax is rejected early.
- Add new checks to the existing `test` job instead of creating overlapping workflows.
- Docker image names derive from the repository name; renames propagate automatically.
- Keep the workflow triggers limited to `main` pushes and pull requests.

## Verification

- Open a pull request and run `gh pr checks <number>`; the `test` job must pass.
- Reproduce CI locally with `pytest` and `ruff check src/ tests/`.

## Child DOX Index

None.
