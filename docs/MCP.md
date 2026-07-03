# MCP server

`stubborn-mcp` exposes three tools over **stdio**. Implementation delegates to [`stubborn.api`](https://github.com/stubborn-ai/stubborn/blob/main/src/stubborn/api.py).

## Install

```bash
pip install stubborn-mcp
```

Build an index with the core compiler first:

```bash
pip install stubborn-stub
stubborn index --scip index.scip --out metadata/symbols.db
export STUBBORN_DB=metadata/symbols.db
stubborn-mcp
```

## Tools

| Tool | Purpose |
|------|---------|
| `get_context` | Prune symbol graph → LLM context |
| `list_symbols` | Browse/search indexed symbols |
| `metrics` | Compression KPI vs Java sources |

See [stubborn docs/MCP.md](https://github.com/stubborn-ai/stubborn/blob/main/docs/MCP.md) for parameters, workflows, and Cursor examples.

## Related

- [stubborn-hub ECOSYSTEM](https://github.com/stubborn-ai/stubborn-hub/blob/main/docs/ECOSYSTEM.md)
- [stubborn ADR-006](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-006-mcp-first-agent-integration.md)
