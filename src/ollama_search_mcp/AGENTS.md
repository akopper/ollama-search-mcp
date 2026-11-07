# src/ollama_search_mcp

## Purpose

Runtime implementation of the MCP server: the `MCPServer` instance, the `web_search` and
`web_fetch` tools, the cached Ollama client, and the CLI/transport entry point.

## Ownership

Owns the public MCP contract: tool names and parameters, return shapes, server name and version,
environment variables, and command-line flags.

## Local Contracts

- `mcp = MCPServer("ollama-search-mcp", version=__version__)`. Keep the server name stable; clients key off it.
- Tool signatures are public API:
  - `web_search(query: str, max_results: int = 10) -> dict[str, Any]`
  - `web_fetch(url: str) -> dict[str, Any]`
- Return values come from the `ollama` response models via `.model_dump()`:
  - `web_search` → `{"results": [{"title", "url", "content"}, ...]}`
  - `web_fetch` → `{"title", "content", "links"}`
- `get_ollama_client()` returns one cached `ollama.Client`, using `OLLAMA_HOST` (default
  `https://ollama.com`) and an `Authorization: Bearer` header when `OLLAMA_API_KEY` is set.
- `_parse_args()` accepts `--http`, `--sse`, `--host HOST`, and `--port PORT`. The default is
  stdio; HTTP defaults to `127.0.0.1:8000` with the MCP endpoint at `/mcp`.
- `main()` is the `ollama-search-mcp` console-script entry point.
- Use MCP SDK v2 imports: `from mcp.server.mcpserver import MCPServer`. Never reintroduce
  `mcp.server.fastmcp`, which no longer exists in `mcp>=2`.

## Work Guidance

- Keep tool docstrings descriptive; MCP clients send them to the model.
- Keep handlers synchronous unless a concrete need for `async` appears; v2 runs sync handlers on
  a worker thread.
- Read configuration with `os.environ.get()` and sensible defaults. Never hardcode or log keys.
- Keep process state limited to the cached client. Multiple sessions share one process.
- Keep HTTP defaults conservative (`127.0.0.1`). Containers opt into `--host 0.0.0.0` via the
  Dockerfile.
- Raise `SystemExit` with a clear message for invalid CLI arguments.

## Verification

- `pytest` from the repository root; tool registration is covered in `tests/`.
- `ruff check src/ tests/` and `ruff format --check src/ tests/`.
- Optional end-to-end: start the server with an MCP stdio client and list tools. Expect
  `web_search` and `web_fetch` and a server version equal to `__version__`.

## Child DOX Index

None.
