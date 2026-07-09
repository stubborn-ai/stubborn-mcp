# stubborn-mcp

**MCP server for [Stubborn](https://github.com/stubborn-ai/stubborn)** — exposes source-neutral code and contract graph tools to Cursor and other MCP clients.

[![PyPI](https://img.shields.io/pypi/v/stubborn-mcp)](https://pypi.org/project/stubborn-mcp/)

Thin adapter over [`stubborn.api`](https://github.com/stubborn-ai/stubborn/blob/main/src/stubborn/api.py). All compile and contract graph logic lives in **[`stubborn-stub`](https://pypi.org/project/stubborn-stub/)**.

Part of the [stubborn-ai](https://github.com/stubborn-ai) program — see [stubborn-hub](https://github.com/stubborn-ai/stubborn-hub).

## Install

```bash
pip install stubborn-stub stubborn-mcp
```

For binary/NDJSON SCIP indexing, install Stubborn with its SCIP extra:

```bash
pip install "stubborn-stub[scip]" stubborn-mcp
stubborn index --scip index.scip --out metadata/symbols.db
export STUBBORN_DB=metadata/symbols.db
stubborn-mcp
```

Contract-only databases are also supported:

```bash
stubborn index-openapi \
  --openapi openapi.json \
  --service customers-service \
  --workspace petclinic \
  --out metadata/symbols.db
export STUBBORN_DB=metadata/symbols.db
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
| `workspace_info` | Inspect workspace source kinds: code repos, contract sources, symbols, endpoints |
| `get_context` | Prune + weave code or contract context (`java-stub` or `stubborn-dsl`) |
| `list_symbols` | Browse/search symbols by `stable_id` |
| `list_contracts` | Browse/search OpenAPI contract endpoint stable IDs and schema constraints |
| `metrics` | Compression KPI vs source tree |

Full parameter reference: [docs/MCP.md](docs/MCP.md)

## Setup diagnostics

Read-only MCP and DB checks ([ADR-015](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-015-federated-doctor-diagnostics.md)) — does not start the MCP server:

```bash
export STUBBORN_DB=metadata/symbols.db
stubborn-mcp doctor
stubborn-mcp doctor --json
```

Aggregate with sibling packages: [stubborn-hub DEMO-LAUNCHERS](https://github.com/stubborn-ai/stubborn-hub/blob/main/docs/DEMO-LAUNCHERS.md).

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
