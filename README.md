# Ollama Search MCP Server

[![Test & Build](https://github.com/akopper/ollama-search-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/akopper/ollama-search-mcp/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/ollama-search-mcp.svg)](https://pypi.org/project/ollama-search-mcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/ollama-search-mcp.svg)](https://pypi.org/project/ollama-search-mcp/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

MCP server exposing Ollama's hosted web search and web fetch APIs as tools for any MCP
client.

## Overview

The server provides two tools:

- **web_search**: search the web through Ollama's hosted search API
- **web_fetch**: fetch a web page and return its content

It works with any MCP client, including Claude Desktop, Cursor, OpenCode, and MCPorter.
An Ollama account and API key are required for the cloud endpoints.

## Requirements

- Python 3.10+
- [MCP Python SDK](https://pypi.org/project/mcp/) v2
- Ollama account (for cloud API access)

## Installation

### PyPI

```bash
uvx ollama-search-mcp
# or install the console script
pip install ollama-search-mcp
```

`uvx` runs the server on demand, which is the recommended command for MCP client
configuration.

### From Git

```bash
uvx --from git+https://github.com/akopper/ollama-search-mcp ollama-search-mcp
```

Pin a release with `@<tag>`:

```bash
uvx --from 'git+https://github.com/akopper/ollama-search-mcp@v0.2.1' ollama-search-mcp
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

### From Source

```bash
git clone https://github.com/akopper/ollama-search-mcp.git
cd ollama-search-mcp
pip install -e .
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

Search queries and fetched URLs are sent to Ollama's cloud service. Do not send
confidential data in search queries.

## Usage

### Running the Server

#### stdio mode (default, for Claude Desktop/Cursor)

```bash
# Using the installed command
ollama-search-mcp

# Explicit stdio (same as the default)
ollama-search-mcp --stdio

# Or on demand with uvx
uvx ollama-search-mcp

# Or directly with Python
python -m ollama_search_mcp.server
```

#### HTTP mode (for remote usage)

```bash
python -m ollama_search_mcp.server --http
```

The server starts on `http://localhost:8000/mcp` by default. Use `--host` and `--port`
to change the bind address, for example inside a container:

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
      "command": "uvx",
      "args": ["ollama-search-mcp"],
      "env": {
        "OLLAMA_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

A globally installed `ollama-search-mcp` console script also works as `command`.

### Cursor Integration

Add to Cursor settings (or `.cursor/mcp.json` in the project):

```json
{
  "mcpServers": {
    "ollama-search": {
      "command": "uvx",
      "args": ["ollama-search-mcp"],
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
        "command": ["uvx", "ollama-search-mcp"],
        "environment": {
          "OLLAMA_API_KEY": "{env:OLLAMA_API_KEY}"
        }
      }
    }
  }
}
```

Then run `opencode mcp list` to verify the connection; it should report
`✓ ollama-search connected`.

If OpenCode is started from a desktop session instead of a login shell, it
usually does not inherit `~/.bashrc`. Two things then break: `~/.local/bin` is
missing from `PATH` (so `uvx` cannot be spawned) and exported variables like
`OLLAMA_API_KEY` are unset (so `{env:OLLAMA_API_KEY}` becomes an empty string).
In that case use an absolute command path and read the key from a file:

```bash
mkdir -p ~/.config/opencode/secrets
printf '%s' 'your-api-key-here' > ~/.config/opencode/secrets/ollama-search.key
chmod 600 ~/.config/opencode/secrets/ollama-search.key
```

```jsonc
{
  "mcp": {
    "servers": {
      "ollama-search": {
        "type": "local",
        "command": ["/home/you/.local/bin/uvx", "ollama-search-mcp"],
        "environment": {
          "OLLAMA_API_KEY": "{file:./secrets/ollama-search.key}"
        }
      }
    }
  }
}
```

`{file:…}` paths are resolved relative to the config file, and `~/` is
expanded, so `{file:~/.config/opencode/secrets/ollama-search.key}` works as
well. Keep the file free of a trailing newline, otherwise it becomes part of
the header value. If your OpenCode version does not support `{file:…}` yet,
put the key into `environment` literally instead.

| Symptom | Cause | Fix |
| --- | --- | --- |
| `mcp connect failed … NotFound: ChildProcess.spawn (uvx ollama-search-mcp)` | `uvx` is not on the `PATH` OpenCode inherited | use the absolute `uvx` path as shown above |
| Tools work but `web_search` returns `Error executing tool web_search`, log says `Authorization header with Bearer token is required for web search` | `OLLAMA_API_KEY` was substituted with an empty string | read it from a file as shown above, set it literally, or export it in the environment that starts OpenCode |

### OpenCode Skill

The repository ships an OpenCode skill that teaches the agent how to call the
server's tools. It lives at `.opencode/skills/ollamawebsearch/SKILL.md`.

Install it globally so it is available in every OpenCode project:

```bash
mkdir -p ~/.config/opencode/skills/ollamawebsearch
cp .opencode/skills/ollamawebsearch/SKILL.md \
  ~/.config/opencode/skills/ollamawebsearch/SKILL.md
```

To keep the installed skill in sync with this repository, link it instead:

```bash
mkdir -p ~/.config/opencode/skills
ln -s "$PWD/.opencode/skills/ollamawebsearch" \
  ~/.config/opencode/skills/ollamawebsearch
```

For a single project, copy the directory to
`<project>/.opencode/skills/ollamawebsearch/`. OpenCode also discovers skills
in `~/.claude/skills` and `~/.agents/skills`.

The skill is registered as `ollamawebsearch`; load it with `@ollamawebsearch`
or the `skill` tool. OpenCode reloads skills automatically, so no restart is
required. When working inside this repository, OpenCode already discovers the
skill from `.opencode/skills`.

### MCPorter Integration

MCPorter can discover and use this server. Example `config/mcporter.json`:

```json
{
  "mcpServers": {
    "ollama-search": {
      "description": "Ollama web search and web fetch MCP server",
      "command": "uvx",
      "args": ["ollama-search-mcp"],
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

Search the web through Ollama's hosted search API.

**Parameters:**
- `query` (required): the search query
- `max_results` (optional): maximum number of results (default: 10)

**Returns:** a dictionary with a `results` list; each entry contains `title`, `url`, and
`content`.

### web_fetch

Fetch a single web page.

**Parameters:**
- `url` (required): the absolute URL to fetch

**Returns:** a dictionary containing the page `title`, `content`, and `links`.

## Development

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Or with uv
uv sync --extra dev
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report=term-missing

# Run a single test
pytest tests/test_server.py::TestWebSearch::test_web_search_returns_dict
```

### Linting and Formatting

```bash
ruff check src/ tests/
ruff format --check src/ tests/
```

### Building Distributions

```bash
python -m build
python -m twine check dist/*
```

### Running the Server for Development

```bash
# stdio mode with mcp dev
mcp dev src/ollama_search_mcp/server.py

# Or run directly
python -m ollama_search_mcp.server
```

## Releasing

See [RELEASING.md](RELEASING.md) for versioning, tagging, and PyPI trusted publishing.

## License

MIT. See [LICENSE](LICENSE).
