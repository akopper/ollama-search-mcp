# Ollama Search MCP Server

MCP server for Ollama web search and web fetch APIs.

## Overview

This MCP server exposes two tools for interacting with Ollama's web services:

- **web_search**: Perform a web search using Ollama's hosted search API
- **web_fetch**: Fetch the content of a web page

## Requirements

- Python 3.10+
- [MCP Python SDK](https://pypi.org/project/mcp/) v2
- Ollama account (for cloud API access)

## Installation

### Clone

```bash
git clone https://github.com/akopper/ollama-search-mcp.git
cd ollama-search-mcp
```

### From Source

```bash
pip install -e .
```

### With uvx

uvx runs the server in stdio mode by default (for Claude Desktop/Cursor):

```bash
uvx --from git+https://github.com/akopper/ollama-search-mcp ollama-search-mcp
```

For HTTP mode with uvx:

```bash
uvx --from git+https://github.com/akopper/ollama-search-mcp ollama-search-mcp --http
```

Pin a release with `@<tag>`:

```bash
uvx --from 'git+https://github.com/akopper/ollama-search-mcp@v0.2.0' ollama-search-mcp
```

### Docker

The Docker image defaults to HTTP mode.

```bash
# HTTP mode (default) - for remote usage
docker run -d -p 8000:8000 -e OLLAMA_API_KEY=your-api-key ghcr.io/akopper/ollama-search-mcp

# stdio mode - for Claude Desktop/Cursor
docker run -it --rm -e OLLAMA_API_KEY=your-api-key ghcr.io/akopper/ollama-search-mcp --stdio
```

### Docker Compose

```bash
cp .env.example .env
# Edit .env with your API key
docker-compose up -d
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_API_KEY` | API key for Ollama cloud services | None |
| `OLLAMA_HOST` | Host URL for Ollama | `https://ollama.com` |

### Getting an API Key

1. Go to [ollama.com](https://ollama.com)
2. Sign in to your account
3. Navigate to API settings
4. Generate an API key

## Usage

### Running the Server

#### stdio mode (default, for Claude Desktop/Cursor)

```bash
# Using the installed command
ollama-search-mcp

# Or directly with Python
python -m ollama_search_mcp.server
```

#### HTTP mode (for remote usage)

```bash
python -m ollama_search_mcp.server --http
```

The server will start on `http://localhost:8000/mcp` by default. Use `--host` and
`--port` to change the bind address, for example inside a container:

```bash
python -m ollama_search_mcp.server --http --host 0.0.0.0 --port 8000
```

### Claude Desktop Integration

Add the following to your Claude Desktop configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ollama-search": {
      "command": "ollama-search-mcp",
      "env": {
        "OLLAMA_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Or with a custom Python environment:

```json
{
  "mcpServers": {
    "ollama-search": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "ollama_search_mcp.server"],
      "env": {
        "OLLAMA_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Cursor Integration

Add to Cursor settings (or `.cursor/mcp.json` in project):

```json
{
  "mcpServers": {
    "ollama-search": {
      "command": "ollama-search-mcp",
      "env": {
        "OLLAMA_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### OpenCode Integration

Add the server to your `~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "mcp": {
    "servers": {
      "ollama-search": {
        "type": "local",
        "command": [
          "uvx",
          "--from",
          "git+https://github.com/akopper/ollama-search-mcp",
          "ollama-search-mcp"
        ],
        "environment": {
          "OLLAMA_API_KEY": "{env:OLLAMA_API_KEY}"
        }
      }
    }
  }
}
```

Then run `opencode mcp list` to verify the connection.

### MCPorter Integration

MCPorter can discover and use this MCP server. Create a config file:

```json
// config/mcporter.json
{
  "mcpServers": {
    "ollama-search": {
      "description": "Ollama web search and web fetch MCP server",
      "command": "ollama-search-mcp",
      "env": {
        "OLLAMA_API_KEY": "$env:OLLAMA_API_KEY"
      }
    }
  }
}
```

Or run ad-hoc:

```bash
# List tools
npx mcporter list ollama-search

# Call a tool
npx mcporter call ollama-search.web_search query:python max_results:10
```

## Available Tools

### web_search

Perform a web search using Ollama's hosted search API.

**Parameters:**
- `query` (required): The search query string
- `max_results` (optional): Maximum number of results to return (default: 10)

**Returns:** Dictionary with a `results` list, each entry containing `title`, `url`, and
`content`.

### web_fetch

Fetch the content of a web page.

**Parameters:**
- `url` (required): The absolute URL to fetch

**Returns:** Dictionary containing the page `title`, `content`, and `links`.

## Development

### Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run a single test
pytest tests/test_server.py::TestWebSearch::test_web_search_returns_dict

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src --cov-report=html
```

### Linting

```bash
# Check code style
ruff check src/ tests/

# Auto-fix issues
ruff check src/ tests/ --fix
```

### Running the Server for Development

```bash
# stdio mode with mcp dev
mcp dev src/ollama_search_mcp/server.py

# Or run directly
python -m ollama_search_mcp.server
```

## License

MIT
