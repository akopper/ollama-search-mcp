"""MCP server for Ollama web search and web fetch APIs.

This server exposes two tools:
- web_search: Perform a web search using Ollama's hosted search API
- web_fetch: Fetch the content of a web page

Environment Variables:
- OLLAMA_API_KEY (optional): API key for Ollama cloud services
- OLLAMA_HOST (optional): Host URL for Ollama (default: https://ollama.com)

Command line:
    ollama-search-mcp               # stdio transport (default)
    ollama-search-mcp --http        # Streamable HTTP transport
    ollama-search-mcp --sse         # SSE transport
    --host HOST                     # HTTP bind address (default: 127.0.0.1)
    --port PORT                     # HTTP port (default: 8000)
"""

from __future__ import annotations

import os
import sys
from typing import Any, Literal

from mcp.server.mcpserver import MCPServer
from ollama import Client

from ollama_search_mcp import __version__

Transport = Literal["stdio", "streamable-http", "sse"]

mcp = MCPServer("ollama-search-mcp", version=__version__)

_ollama_client: Client | None = None


def get_ollama_client() -> Client:
    """Get or create the Ollama client instance."""
    global _ollama_client
    if _ollama_client is None:
        api_key = os.environ.get("OLLAMA_API_KEY")
        host = os.environ.get("OLLAMA_HOST", "https://ollama.com")

        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        _ollama_client = Client(host=host, headers=headers)
    return _ollama_client


@mcp.tool()
def web_search(query: str, max_results: int = 10) -> dict[str, Any]:
    """Perform a web search using Ollama's hosted search API.

    Args:
        query: The search query to run.
        max_results: Maximum number of results to return (default: 10).

    Returns:
        A dictionary containing search results with title, url, and content.
    """
    client = get_ollama_client()
    result = client.web_search(query=query, max_results=max_results)
    return result.model_dump()


@mcp.tool()
def web_fetch(url: str) -> dict[str, Any]:
    """Fetch the content of a web page.

    Args:
        url: The absolute URL to fetch.

    Returns:
        A dictionary containing the page title, content, and links.
    """
    client = get_ollama_client()
    result = client.web_fetch(url=url)
    return result.model_dump()


def _parse_args(argv: list[str]) -> tuple[Transport, str, int]:
    """Parse command-line arguments into transport settings."""
    transport: Transport = "stdio"
    host = "127.0.0.1"
    port = 8000

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--http":
            transport = "streamable-http"
        elif arg == "--sse":
            transport = "sse"
        elif arg in ("--host", "--port"):
            if i + 1 >= len(argv):
                raise SystemExit(f"{arg} requires a value")
            value = argv[i + 1]
            if arg == "--host":
                host = value
            else:
                port = int(value)
            i += 1
        else:
            raise SystemExit(f"unknown argument: {arg}")
        i += 1

    return transport, host, port


def main() -> None:
    """Main entry point for the MCP server."""
    transport, host, port = _parse_args(sys.argv[1:])

    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)


if __name__ == "__main__":
    main()
