# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.1.0b2] - 2026-07-04

### Added

- Source-neutral MCP tools: `workspace_info`, `list_contracts`, and structured contract endpoint context via `get_context`.

### Changed

- `stubborn-mcp` now expects `stubborn-stub>=0.9.0b5`, matching the source-neutral contract query release.

## [0.1.0b1] - 2026-07-03

### Added

- MCP stdio server: `get_context`, `list_symbols`, `metrics` over [`stubborn.api`](https://github.com/stubborn-ai/stubborn).
- Console entry: `stubborn-mcp` / `python -m stubborn_mcp`.
- CI: pytest + ruff on Python 3.11–3.13.

[0.1.0b1]: https://github.com/stubborn-ai/stubborn-mcp/releases/tag/v0.1.0b1
[0.1.0b2]: https://github.com/stubborn-ai/stubborn-mcp/compare/v0.1.0b1...v0.1.0b2
