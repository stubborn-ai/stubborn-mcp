# stubborn-mcp

**MCP server for [Stubborn](https://github.com/stubborn-ai/stubborn)** — exposes `get_context`, `list_symbols`, and `metrics` to Cursor and other MCP clients.

Thin adapter over [`stubborn.api`](https://github.com/stubborn-ai/stubborn/blob/main/src/stubborn/api.py). All compile logic lives in **`stubborn-stub`**.

Part of the [stubborn-ai](https://github.com/stubborn-ai) program — see [stubborn-hub](https://github.com/stubborn-ai/stubborn-hub).

## Install

```bash
pip install stubborn-mcp
```

Requires a **SCIP-derived** `symbols.db` — build with the core compiler:

```bash
pip install stubborn-stub
stubborn index --scip index.scip --out metadata/symbols.db
```

## Run

```bash
export STUBBORN_DB=/path/to/metadata/symbols.db
stubborn-mcp
```

## Cursor configuration

`.cursor/mcp.json`:

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

Module entry: `python -m stubborn_mcp`

## Tools

| Tool | Purpose |
|------|---------|
| `get_context` | Prune + weave LLM context (`java-stub` or `stubborn-dsl`) |
| `list_symbols` | Browse/search symbols by `stable_id` |
| `metrics` | Compression KPI vs source tree |

Full parameter reference: [docs/MCP.md](docs/MCP.md) · [stubborn MCP docs](https://github.com/stubborn-ai/stubborn/blob/main/docs/MCP.md)

## Development

```bash
git clone https://github.com/stubborn-ai/stubborn-mcp.git
cd stubborn-mcp
pip install -e "../stubborn"
pip install -e ".[dev]"
pytest
```

## License

MIT — see [LICENSE](LICENSE).
