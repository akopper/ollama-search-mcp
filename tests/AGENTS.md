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

## Work Guidance

- Add a test for every public contract change: tool name, parameters, defaults, return shape,
  CLI flag, or transport behavior.
- Patch at the module boundary (`ollama_search_mcp.server...`), not inside the `ollama` package.
- Purge or reload `ollama_search_mcp` modules when testing environment-driven client
  construction, following the existing pattern in `TestOllamaClient`.
- Shape mocks like real `ollama` responses (`results`, `title`, `content`, `links`).

## Verification

- `pytest` from the repository root with the dev environment installed.
- `ruff check tests/` and `ruff format --check tests/`.

## Child DOX Index

None.
