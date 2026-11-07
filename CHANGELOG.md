# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2026-11-07

### Added

- PyPI publishing through GitHub Actions trusted publishing
- MIT `LICENSE` file
- `CHANGELOG.md`, `RELEASING.md`, and Dependabot configuration
- CI matrix for Python 3.10 and 3.13, packaging checks, and coverage reporting
- Docker image tags for releases (`vX.Y.Z` and `X.Y`)
- Explicit `--stdio` flag for the default stdio transport

### Changed

- Switched package metadata to PEP 639 license expressions and added classifiers,
  keywords, and project URLs
- Replaced unused dev dependencies with `pytest-cov` and `build`

## [0.2.0] - 2026-11-07

### Added

- Server version reporting in the initialize response
- Tests for tool registration and CLI parsing
- `--host` and `--port` options for HTTP transports
- OpenCode integration example

### Changed

- Renamed the project from `ollama-websearch-mcp` to `ollama-search-mcp`
- Renamed the Python package to `ollama_search_mcp`
- Migrated to the MCP Python SDK v2 (`MCPServer`); requires `mcp>=2,<3`
- Bumped the minimum `ollama` dependency to `0.6.0`

### Fixed

- Dockerfile now copies `src/` before installing, so the image builds
- The container binds `0.0.0.0`, so published ports work
- Documented the real `web_search` and `web_fetch` return shapes

## [0.1.0] - 2026-03-04

### Added

- Initial MCP server with `web_search` and `web_fetch` tools
- stdio, Streamable HTTP, and SSE transports
- Docker image and Docker Compose example
