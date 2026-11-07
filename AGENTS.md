# Agent Guidelines for ollama-search-mcp

This project uses the DOX AGENTS.md hierarchy. Read this file and every child AGENTS.md on the
path to the files you touch before editing.

# DOX framework

- DOX is highly performant AGENTS.md hierarchy installed here
- Agent must follow DOX instructions across any edits

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Read every AGENTS.md found along each route
5. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
6. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
7. If docs conflict, the closer doc controls local work details, but no child doc may weaken DOX

Do not rely on memory. Re-read the applicable DOX chain in the current session before editing.

## Update After Editing

Every meaningful change requires a DOX pass before the task is done.

Update the closest owning AGENTS.md when a change affects:

- purpose, scope, ownership, or responsibilities
- durable structure, contracts, workflows, or operating rules
- required inputs, outputs, permissions, constraints, side effects, or artifacts
- user preferences about behavior, communication, process, organization, or quality
- AGENTS.md creation, deletion, move, rename, or index contents

Update parent docs when parent-level structure, ownership, workflow, or child index changes. Update child docs when parent changes alter local rules. Remove stale or contradictory text immediately. Small edits that do not change behavior or contracts may leave docs unchanged, but the DOX pass still must happen.

## Hierarchy

- Root AGENTS.md is the DOX rail: project-wide instructions, global preferences, durable workflow rules, and the top-level Child DOX Index
- Child AGENTS.md files own domain-specific instructions and their own Child DOX Index
- Each parent explains what its direct children cover and what stays owned by the parent
- The closer a doc is to the work, the more specific and practical it must be

## Child Doc Shape

- Create a child AGENTS.md when a folder becomes a durable boundary with its own purpose, rules, responsibilities, workflow, materials, or quality standards
- Work Guidance must reflect the current standards of the project or user instructions; if there are no specific standards or instructions yet, leave it empty
- Verification must reflect an existing check; if no verification framework exists yet, leave it empty and update it when one exists

Default section order:

- Purpose
- Ownership
- Local Contracts
- Work Guidance
- Verification
- Child DOX Index

## Style

- Keep docs concise, current, and operational
- Document stable contracts, not diary entries
- Put broad rules in parent docs and concrete details in child docs
- Prefer direct bullets with explicit names
- Do not duplicate rules across many files unless each scope needs a local version
- Delete stale notes instead of explaining history
- Trim obvious statements, repeated rules, misplaced detail, and warnings for risks that no longer exist

## Closeout

1. Re-check changed paths against the DOX chain
2. Update nearest owning docs and any affected parents or children
3. Refresh every affected Child DOX Index
4. Remove stale or contradictory text
5. Run existing verification when relevant
6. Report any docs intentionally left unchanged and why

## User Preferences

When the user requests a durable behavior change, record it here or in the relevant child AGENTS.md

## Project Overview

- `ollama-search-mcp` is an MCP (Model Context Protocol) server that exposes Ollama's hosted `web_search` and `web_fetch` APIs as tools.
- It works with any MCP client, including Claude Desktop, Cursor, OpenCode, and MCPorter.
- Runtime: Python 3.10+, MCP Python SDK v2 (`mcp>=2,<3`), `ollama>=0.6.0`.
- Distributed as `ollama-search-mcp`; the Python package is `ollama_search_mcp`; the console script is `ollama-search-mcp`.
- Transports: stdio (default), Streamable HTTP (`--http`, default `127.0.0.1:8000/mcp`), SSE (`--sse`).
- Configuration: `OLLAMA_API_KEY` (optional Bearer token) and `OLLAMA_HOST` (default `https://ollama.com`).
- The version must stay in sync between `pyproject.toml` and `src/ollama_search_mcp/__init__.py`.

## Repository Layout

```text
ollama-search-mcp/
├── src/ollama_search_mcp/   # server implementation
├── tests/                   # pytest suite
├── .github/workflows/       # CI and GHCR publishing
├── config/mcporter.json     # MCPorter example config
├── Dockerfile               # container image (HTTP mode)
├── docker-compose.yml
└── pyproject.toml
```

## Setup And Commands

```bash
# Setup (pip, as used by CI)
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Alternative (uses uv.lock)
uv sync --extra dev

# Verification
pytest
ruff check src/ tests/
ruff format --check src/ tests/

# Run
python -m ollama_search_mcp.server            # stdio
python -m ollama_search_mcp.server --http     # Streamable HTTP
python -m ollama_search_mcp.server --sse      # SSE
```

## Global Code Rules

- Use type hints for every parameter and return value; use `dict[str, Any]` for loosely typed dictionaries.
- ruff: line length 100, 4-space indent, double quotes, trailing commas in multi-line collections.
- Import order: standard library, third-party, local; use absolute imports from `ollama_search_mcp`.
- Naming: `snake_case` functions and modules, `PascalCase` classes, `UPPER_SNAKE_CASE` constants, `_private` helpers.
- Docstrings: Google style with Args/Returns/Raises; keep the first line under 79 characters.
- Let unexpected exceptions propagate; give expected failures descriptive messages.
- Keep dependencies minimal and pin minimum versions in `pyproject.toml`.

## Cross-Cutting Workflows

### Add or change a tool

1. Change the tool in `src/ollama_search_mcp/server.py`.
2. Add or update tests in `tests/`.
3. Run pytest, ruff check, and ruff format check.
4. Update the README tool docs if the public contract changed.

### Change dependencies or versions

1. Edit `pyproject.toml`.
2. Refresh the lockfile with `uv lock` and reinstall.
3. Keep `__version__` in `src/ollama_search_mcp/__init__.py` aligned with the project version.
4. Run the full test and lint suite.

### Release

1. Merge to `main` only after CI is green.
2. Tag the release as `vX.Y.Z` and push the tag.
3. Pushes to `main` publish `ghcr.io/<repository>:latest`.

## Child DOX Index

- [src/ollama_search_mcp/AGENTS.md](src/ollama_search_mcp/AGENTS.md) — server implementation, tools, client, transports, and CLI.
- [tests/AGENTS.md](tests/AGENTS.md) — pytest suite, fixtures, and verification.
- [.github/AGENTS.md](.github/AGENTS.md) — CI test job and GHCR image publishing.
