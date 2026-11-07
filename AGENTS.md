# Agent Guidelines for ollama-search-mcp

## Project Overview

This is an MCP (Model Context Protocol) server that exposes Ollama's web search and web fetch APIs as tools for AI assistants like Claude, Cursor, and other MCP clients.

## Build / Test Commands

### Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_server.py

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

### Running the Server

```bash
# stdio mode (default, for Claude Desktop/Cursor)
python -m ollama_search_mcp.server
ollama-search-mcp

# HTTP mode (for remote usage)
python -m ollama_search_mcp.server --http
```

## Code Style Guidelines

### General

- **Language**: Python 3.10+
- **Linter**: ruff
- **Formatter**: ruff (using default settings)
- **Testing**: pytest

### Import Conventions

- Standard library imports first
- Third-party imports second
- Local imports third
- Use absolute imports for package modules: `from ollama_search_mcp.server import ...`
- Sort imports alphabetically within each group

### Formatting

- Line length: 100 characters
- Indent: 4 spaces
- Quotes: double quotes (`"`) for strings
- Use trailing commas for multi-line collections

### Type Hints

- Use type hints for all function parameters and return types
- Use `dict[str, Any]` for dictionary returns that are not statically typed
- Import types from `typing` module when needed (e.g., `Optional`, `List`)

Example:
```python
def web_search(query: str, max_results: int = 10) -> dict[str, Any]:
    """Perform a web search using Ollama's hosted search API.

    Args:
        query: The search query to run.
        max_results: Maximum number of results to return (default: 10).

    Returns:
        A dictionary containing search results with title, url, and snippet.
    """
    ...
```

### Naming Conventions

- **Functions**: snake_case (`get_ollama_client`, `web_search`)
- **Classes**: PascalCase (`MCPServer`, `MyClass`)
- **Constants**: UPPER_SNAKE_CASE
- **Modules**: snake_case
- **Private functions**: prefix with underscore (`_internal_function`)

### Docstrings

- Use Google-style docstrings
- Include Args, Returns, and Raises sections for functions
- Keep the first line concise (under 79 characters)
- Add description for complex functions

### Error Handling

- Let exceptions propagate for unexpected errors
- Use descriptive error messages
- Handle expected error cases gracefully

### Testing

- Use pytest as the testing framework
- Use `unittest.mock` for mocking
- Name test files: `test_*.py`
- Test class names: `Test*`
- Test method names: `test_*`

Example test structure:
```python
class TestWebSearch:
    """Tests for the web_search tool."""

    def test_web_search_returns_dict(self, mock_ollama_client):
        """Test that web_search returns a dictionary."""
        ...
```

### Project Structure

```
ollama-search-mcp/
├── src/
│   └── ollama_search_mcp/
│       ├── __init__.py
│       └── server.py
├── tests/
│   ├── __init__.py
│   └── test_server.py
├── pyproject.toml
├── README.md
├── AGENTS.md
└── .env.example
```

### MCP Server Guidelines

- Use `MCPServer` from `mcp.server.mcpserver` for simple stdio servers (MCP Python SDK v2)
- Define tools with the `@mcp.tool()` decorator
- Tools should return JSON-serializable dictionaries
- Use descriptive docstrings for tools (exposed to LLM clients)
- Support both stdio and HTTP transports

### Environment Variables

- Use `os.environ.get()` to read environment variables
- Provide sensible defaults
- Document all environment variables in docstrings

### Dependencies

- Keep dependencies minimal
- Pin minimum versions in `pyproject.toml`
- Use `ollama` for Ollama API interactions
- Use `mcp>=2,<3` for the MCP server implementation

## Common Tasks

### Adding a New Tool

1. Add the tool function to `src/ollama_search_mcp/server.py`
2. Decorate with `@mcp.tool()`
3. Add type hints and docstring
4. Add tests in `tests/test_server.py`
5. Run tests to verify

### Updating Dependencies

1. Edit `dependencies` or `project.optional-dependencies` in `pyproject.toml`
2. Run `pip install -e ".[dev]"` to update
3. Run tests to ensure everything still works

### Running MCP Inspector

```bash
mcp dev src/ollama_search_mcp/server.py
```

This starts the MCP development server for testing tools.
