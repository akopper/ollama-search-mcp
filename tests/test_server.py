"""Tests for the Ollama web search MCP server."""

import asyncio
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_ollama_client():
    """Create a mock Ollama client."""
    with patch("ollama_search_mcp.server.get_ollama_client") as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


@pytest.fixture
def import_server():
    """Import the server module with mocked dependencies."""
    with patch("ollama.Client"):
        import importlib

        import ollama_search_mcp.server as server_module

        importlib.reload(server_module)
        return server_module


class TestWebSearch:
    """Tests for the web_search tool."""

    def test_web_search_returns_dict(self, mock_ollama_client):
        """Test that web_search returns a dictionary."""
        from ollama_search_mcp.server import web_search

        mock_response = MagicMock()
        mock_response.model_dump.return_value = {
            "results": [
                {
                    "title": "Test Result",
                    "url": "https://example.com",
                    "content": "Test snippet",
                }
            ]
        }
        mock_ollama_client.web_search.return_value = mock_response

        result = web_search(query="test query", max_results=5)

        assert isinstance(result, dict)
        mock_ollama_client.web_search.assert_called_once_with(query="test query", max_results=5)

    def test_web_search_default_max_results(self, mock_ollama_client):
        """Test that web_search uses default max_results."""
        from ollama_search_mcp.server import web_search

        mock_response = MagicMock()
        mock_response.model_dump.return_value = {"results": []}
        mock_ollama_client.web_search.return_value = mock_response

        web_search(query="test")

        mock_ollama_client.web_search.assert_called_once_with(query="test", max_results=10)


class TestWebFetch:
    """Tests for the web_fetch tool."""

    def test_web_fetch_returns_dict(self, mock_ollama_client):
        """Test that web_fetch returns a dictionary."""
        from ollama_search_mcp.server import web_fetch

        mock_response = MagicMock()
        mock_response.model_dump.return_value = {
            "title": "Test Page",
            "content": "Test",
            "links": ["https://example.com/next"],
        }
        mock_ollama_client.web_fetch.return_value = mock_response

        result = web_fetch(url="https://example.com")

        assert isinstance(result, dict)
        mock_ollama_client.web_fetch.assert_called_once_with(url="https://example.com")


class TestOllamaClient:
    """Tests for the Ollama client initialization."""

    def test_client_uses_default_host(self):
        """Test that client uses default Ollama host."""
        import sys

        for mod_name in list(sys.modules.keys()):
            if mod_name.startswith("ollama_search_mcp"):
                del sys.modules[mod_name]

        with patch("ollama.Client") as mock_client, patch.dict("os.environ", {}, clear=True):
            from ollama_search_mcp.server import get_ollama_client

            get_ollama_client()

            mock_client.assert_called_once_with(host="https://ollama.com", headers={})

    def test_client_uses_custom_host(self):
        """Test that client uses custom OLLAMA_HOST."""
        import sys

        for mod_name in list(sys.modules.keys()):
            if mod_name.startswith("ollama_search_mcp"):
                del sys.modules[mod_name]

        with (
            patch("ollama.Client") as mock_client,
            patch.dict("os.environ", {"OLLAMA_HOST": "https://custom.example.com"}),
        ):
            from ollama_search_mcp.server import get_ollama_client

            get_ollama_client()

            mock_client.assert_called_once_with(host="https://custom.example.com", headers={})

    def test_client_uses_api_key(self):
        """Test that client uses OLLAMA_API_KEY."""
        import sys

        for mod_name in list(sys.modules.keys()):
            if mod_name.startswith("ollama_search_mcp"):
                del sys.modules[mod_name]

        with (
            patch("ollama.Client") as mock_client,
            patch.dict(
                "os.environ",
                {"OLLAMA_API_KEY": "test-api-key"},
                clear=False,
            ),
        ):
            from ollama_search_mcp.server import get_ollama_client

            get_ollama_client()

            mock_client.assert_called_once()
            call_kwargs = mock_client.call_args.kwargs
            assert call_kwargs["host"] == "https://ollama.com"
            assert call_kwargs["headers"]["Authorization"] == "Bearer test-api-key"


class TestServer:
    """Tests for the MCP server registration and command line."""

    def test_exposes_web_tools(self):
        """Test that both tools are registered on the server."""
        from ollama_search_mcp.server import mcp

        tools = asyncio.run(mcp.list_tools())

        assert {tool.name for tool in tools} == {"web_search", "web_fetch"}

    def test_parse_args_defaults(self):
        """Test that the CLI defaults to stdio on localhost."""
        from ollama_search_mcp.server import _parse_args

        assert _parse_args([]) == ("stdio", "127.0.0.1", 8000)

    def test_parse_args_http(self):
        """Test that HTTP mode accepts host and port overrides."""
        from ollama_search_mcp.server import _parse_args

        assert _parse_args(["--http", "--host", "0.0.0.0", "--port", "9000"]) == (
            "streamable-http",
            "0.0.0.0",
            9000,
        )

    def test_parse_args_rejects_unknown(self):
        """Test that unknown arguments fail fast."""
        from ollama_search_mcp.server import _parse_args

        with pytest.raises(SystemExit):
            _parse_args(["--nope"])
