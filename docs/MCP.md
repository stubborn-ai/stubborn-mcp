# MCP server

`stubborn-mcp` **0.10.0b2** on [PyPI](https://pypi.org/project/stubborn-mcp/) exposes Stubborn code and contract graph tools over **stdio**. Implementation delegates to [`stubborn.api`](https://github.com/stubborn-ai/stubborn/blob/main/src/stubborn/api.py) from **`stubborn-stub`**.

## Install

```bash
pip install "stubborn-stub[scip]" stubborn-mcp
stubborn index --scip index.scip --out metadata/symbols.db
export STUBBORN_DB=metadata/symbols.db
stubborn-mcp
```

OpenAPI-only contract databases can use the core install:

```bash
pip install stubborn-stub stubborn-mcp
stubborn index-openapi \
  --openapi openapi.json \
  --service customers-service \
  --workspace petclinic \
  --out metadata/symbols.db
export STUBBORN_DB=metadata/symbols.db
stubborn-mcp
```

## Tools

| Tool | Purpose |
|------|---------|
| `workspace_info` | Inspect source-neutral workspace counts and latest runs |
| `get_context` | Prune code symbol or contract endpoint graph → LLM context (`format`, `prune_mode`, `member_signatures`, `javadoc`) |
| `list_symbols` | Browse/search code symbols (includes `documentation`) |
| `list_contracts` | Browse/search contract endpoints and schema constraints |
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
3. `workspace_info` with the workspace name if using a multi-source workspace
4. `list_symbols` with `query: "OrderService"` → pick a code `stable_id`
5. `get_context` with target before codegen
6. Optional: `metrics` with `sources: src/main/java`

## Contract-first workflow

1. `stubborn index-openapi --openapi openapi.json --service customers-service --workspace petclinic --out metadata/symbols.db`
2. Configure MCP with `STUBBORN_DB`
3. `workspace_info` with `workspace: "petclinic"` to confirm contract sources are visible
4. `list_contracts` with `workspace: "petclinic"` → pick an `openapi ...` stable ID
5. `get_context` with that endpoint target and `format: "stubborn-dsl"`

Contract endpoints with no code bindings still render endpoint/schema facts.
When bindings exist, `get_context` also returns structured `contract_edges` and
`contract_endpoints` fields.

Parameter tables and weave options: [stubborn STUBBORN-DSL-GUIDE](https://github.com/stubborn-ai/stubborn/blob/main/docs/STUBBORN-DSL-GUIDE.md).

## Related

- [stubborn-hub ECOSYSTEM](https://github.com/stubborn-ai/stubborn-hub/blob/main/docs/ECOSYSTEM.md)
- [stubborn ADR-006](https://github.com/stubborn-ai/stubborn/blob/main/docs/adr/ADR-006-mcp-first-agent-integration.md)
