# MCP server

`stubborn-mcp` **0.1.0b1** on [PyPI](https://pypi.org/project/stubborn-mcp/) exposes three tools over **stdio**. Implementation delegates to [`stubborn.api`](https://github.com/stubborn-ai/stubborn/blob/main/src/stubborn/api.py) from **`stubborn-stub`** (≥0.9.0b4).

## Install

```bash
pip install stubborn-stub stubborn-mcp
stubborn index --scip index.scip --out metadata/symbols.db
export STUBBORN_DB=metadata/symbols.db
stubborn-mcp
```

## Tools

| Tool | Purpose |
|------|---------|
| `get_context` | Prune symbol graph → LLM context (`format`, `prune_mode`, `member_signatures`, `javadoc`) |
| `list_symbols` | Browse/search indexed symbols (includes `documentation`) |
| `metrics` | Compression KPI vs Java `sources` tree |

## Cursor

```json
{
  "mcpServers": {
    "stubborn": {
      "command": "stubborn-mcp",
      "env": {
        "STUBBORN_DB": "${workspaceFolder}/metadata/symbols.db"
      }
    }
  }
}
```

## Typical agent workflow

1. `stubborn index --scip index.scip --out metadata/symbols.db`
2. Configure MCP with `STUBBORN_DB`
3. `list_symbols` with `query: "OrderService"` → pick `stable_id`
4. `get_context` with target before codegen
5. Optional: `metrics` with `sources: src/main/java`

Parameter tables and weave options: [stubborn STUBBORN-DSL-GUIDE](https://github.com/stubborn-ai/stubborn/blob/main/docs/STUBBORN-DSL-GUIDE.md).

## Related

- [stubborn-hub ECOSYSTEM](https://github.com/stubborn-ai/stubborn-hub/blob/main/docs/ECOSYSTEM.md)
- [stubborn ADR-006](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-006-mcp-first-agent-integration.md)
