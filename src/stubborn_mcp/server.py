"""stdio MCP server exposing Stubborn tools to agents."""

from __future__ import annotations

from typing import Any

import stubborn.api as stubborn_api
from mcp.server.fastmcp import FastMCP
from stubborn.weave.stubborn_dsl_llm import llm_guide_text

mcp = FastMCP(
    "stubborn",
    instructions=(
        "Deterministic code and contract context from Stubborn. "
        "Use workspace_info to inspect source kinds, list_symbols for code stable IDs, "
        "list_contracts for OpenAPI endpoint stable IDs, get_context for pruned context, "
        "and metrics for compression KPIs. "
        "Set STUBBORN_DB or pass db_path per call. "
        f"When format is stubborn-dsl: {llm_guide_text()}"
    ),
)


@mcp.tool()
def get_context(
    target: str,
    db_path: str | None = None,
    format: str = "java-stub",
    max_symbols: int = 200,
    call_depth: int = 2,
    max_tokens: int = 12_000,
    member_signatures: str = "target",
    javadoc: str | None = None,
    prune_mode: str = "smart",
    workspace: str | None = None,
    repo_key: str | None = None,
) -> dict[str, Any]:
    """Return pruned, privacy-safe context for a code symbol or contract endpoint stable_id.

    Use format=java-stub for Java/code targets and format=stubborn-dsl for contract endpoints
    or mixed code/contract context.

    member_signatures: off | target | neighbors | all — controls method lists on types.
    javadoc: off | summary | full — default summary (java-stub) or off (stubborn-dsl).
    prune_mode: smart (SCIP + signature heuristics) | strict (SCIP edges only) | fast (smaller neighborhood).
    """
    result = stubborn_api.get_context(
        target,
        db_path=db_path,
        format=format,
        max_symbols=max_symbols,
        call_depth=call_depth,
        max_tokens=max_tokens,
        member_signatures=member_signatures,
        javadoc=javadoc,
        prune_mode=prune_mode,
        workspace=workspace,
        repo_key=repo_key,
    )
    return {
        "target_stable_id": result.target_stable_id,
        "format": result.format,
        "text": result.text,
        "symbol_count": result.symbol_count,
        "estimated_tokens": result.estimated_tokens,
        "dropped_for_budget": result.dropped_for_budget,
        "contract_edges": getattr(result, "contract_edges", []),
        "contract_endpoints": getattr(result, "contract_endpoints", []),
        "contract_evidence_summary": getattr(result, "contract_evidence_summary", {}),
    }


@mcp.tool()
def workspace_info(
    workspace: str,
    db_path: str | None = None,
) -> dict[str, Any]:
    """Return source-neutral workspace summary: code repos, contract sources, symbols, endpoints."""
    return stubborn_api.get_workspace_info(db_path=db_path, workspace=workspace)


@mcp.tool()
def list_symbols(
    db_path: str | None = None,
    query: str | None = None,
    kind: str | None = None,
    limit: int = 50,
    workspace: str | None = None,
    repo_key: str | None = None,
) -> dict[str, Any]:
    """List code symbol stable IDs."""
    symbols = stubborn_api.list_index_symbols(
        db_path=db_path,
        query=query,
        kind=kind,
        limit=limit,
        workspace=workspace,
        repo_key=repo_key,
    )
    info = stubborn_api.get_index_info(db_path=db_path)
    return {
        "db_path": info["db_path"],
        "index_run_id": info["index_run_id"],
        "symbol_count": info["symbol_count"],
        "returned": len(symbols),
        "symbols": symbols,
    }


@mcp.tool()
def list_contracts(
    db_path: str | None = None,
    query: str | None = None,
    workspace: str | None = None,
    repo_key: str | None = None,
    index_run_id: int | None = None,
) -> dict[str, Any]:
    """List contract endpoint stable IDs and schema constraints."""
    endpoints = stubborn_api.list_contracts(
        db_path=db_path,
        query=query,
        index_run_id=index_run_id,
        workspace=workspace,
        repo_key=repo_key,
    )
    info = stubborn_api.get_index_info(db_path=db_path)
    return {
        "db_path": info["db_path"],
        "index_run_id": info["index_run_id"],
        "returned": len(endpoints),
        "contract_endpoints": endpoints,
    }


@mcp.tool()
def metrics(
    target: str,
    sources: str,
    db_path: str | None = None,
    max_symbols: int = 200,
    call_depth: int = 2,
    max_tokens: int = 12_000,
    member_signatures: str = "target",
    javadoc: str | None = None,
    prune_mode: str = "smart",
    include_stub_text: bool = False,
    workspace: str | None = None,
    repo_key: str | None = None,
) -> dict[str, Any]:
    """Compare pruned stub size against full Java sources (compression KPI)."""
    report = stubborn_api.get_metrics(
        target,
        sources,
        db_path=db_path,
        max_symbols=max_symbols,
        call_depth=call_depth,
        max_tokens=max_tokens,
        member_signatures=member_signatures,
        javadoc=javadoc,
        prune_mode=prune_mode,
        workspace=workspace,
        repo_key=repo_key,
    )
    if not include_stub_text:
        report = {k: v for k, v in report.items() if k != "stub_text"}
    return report


def main() -> None:
    """Run the MCP server over stdio (default transport)."""
    mcp.run()


if __name__ == "__main__":
    main()
