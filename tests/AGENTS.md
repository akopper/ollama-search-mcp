# tests

## Purpose

Pytest suite for the MCP server: tool behavior, Ollama client configuration, server
registration, and command-line parsing.

## Ownership

Owns test layout, fixtures, and the local verification expectations for this repository.

## Local Contracts

- Single test module: `test_server.py`. Test classes group behavior: `TestWebSearch`,
  `TestWebFetch`, `TestOllamaClient`, `TestServer`.
- External calls are mocked. Patch `ollama_search_mcp.server.get_ollama_client` for tool calls
  and `ollama.Client` for client construction.
- Tests must not need network access, an Ollama account, or `OLLAMA_API_KEY`.
- Async server introspection uses `asyncio.run(mcp.list_tools())`.
- File names are `test_*.py`, class names `Test*`, test names `test_*`.
- Only `pytest` and `pytest-cov` are required; no custom pytest plugins or fixtures are
  configured, and `pytest` runs with `--strict-config --strict-markers`.
- Coverage is configured in `pyproject.toml` (`source = ["ollama_search_mcp"]`, branch
  coverage, `show_missing`, `skip_covered`).

## Work Guidance

- Add a test for every public contract change: tool name, parameters, defaults, return shape,
  CLI flag, or transport behavior.
- Patch at the module boundary (`ollama_search_mcp.server...`), not inside the `ollama` package.
- Purge or reload `ollama_search_mcp` modules when testing environment-driven client
  construction, following the existing pattern in `TestOllamaClient`.
- Shape mocks like real `ollama` responses (`results`, `title`, `content`, `links`).
- Keep the suite hermetic: no live HTTP, no environment assumptions beyond what a test sets
  explicitly.

## Verification

- `pytest --cov --cov-report=term-missing` from the repository root with the dev environment
  installed.
- `ruff check tests/` and `ruff format --check tests/`.
- The full suite must pass on Python 3.10 and 3.13 (the CI matrix).

## Child DOX Index

None.
