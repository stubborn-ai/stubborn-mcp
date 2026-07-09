"""MCP package doctor checks (ADR-015)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import stubborn.api as stubborn_api
from stubborn.store.reader import resolve_db_path

from stubborn_mcp.__version__ import __version__
from stubborn_mcp.doctor.models import Check


def runtime_checks() -> list[Check]:
    checks: list[Check] = []
    major, minor = sys.version_info[:2]
    if (major, minor) < (3, 11):
        checks.append(
            Check(
                id="runtime.python",
                status="fail",
                message=f"Python {major}.{minor} is below the required 3.11+",
            )
        )
    else:
        checks.append(Check(id="runtime.python", status="pass", message=f"Python {major}.{minor}"))

    try:
        import stubborn_mcp  # noqa: F401
    except ImportError as exc:
        checks.append(
            Check(
                id="mcp.import",
                status="fail",
                message=f"stubborn-mcp not importable: {exc}",
                hint="pip install stubborn-mcp",
            )
        )
        return checks

    checks.append(Check(id="mcp.import", status="pass", message="stubborn-mcp importable"))
    checks.append(Check(id="mcp.version", status="info", message=f"stubborn-mcp {__version__}"))
    return checks


def database_checks(db_path: Path | None) -> list[Check]:
    checks: list[Check] = []
    env_db = os.environ.get("STUBBORN_DB")
    if env_db:
        checks.append(
            Check(
                id="mcp.stubborn_db",
                status="info",
                message=f"STUBBORN_DB={env_db}",
            )
        )
    else:
        checks.append(
            Check(
                id="mcp.stubborn_db",
                status="warn",
                message="STUBBORN_DB is not set",
                hint="export STUBBORN_DB=metadata/symbols.db (stubborn-mcp)",
            )
        )

    try:
        resolved = resolve_db_path(db_path)
    except ValueError as exc:
        checks.append(Check(id="mcp.db", status="fail", message=str(exc)))
        return checks

    if not resolved.is_file():
        checks.append(
            Check(
                id="mcp.db",
                status="fail",
                message=f"symbol graph not found: {resolved}",
                hint="Index first with stubborn index, then export STUBBORN_DB (stubborn-stub)",
            )
        )
        return checks

    checks.append(Check(id="mcp.db", status="pass", message=f"symbol graph: {resolved}"))
    try:
        info = stubborn_api.get_index_info(db_path=resolved)
    except Exception as exc:
        checks.append(Check(id="mcp.db_readable", status="fail", message=str(exc)))
        return checks

    checks.append(
        Check(
            id="mcp.db_readable",
            status="pass",
            message=(
                f"index_run {info['index_run_id']}: symbols={info['symbol_count']}, "
                f"kind={info.get('run_kind', 'code')}"
            ),
        )
    )

    workspace = info.get("workspace") or "default"
    try:
        summary = stubborn_api.get_workspace_info(db_path=resolved, workspace=workspace)
        checks.append(
            Check(
                id="mcp.workspace_info",
                status="pass",
                message=(
                    f"workspace_info({workspace!r}): repos={summary.get('repo_count', 0)}, "
                    f"symbols={summary.get('symbol_count', 0)}"
                ),
            )
        )
    except Exception as exc:
        checks.append(
            Check(
                id="mcp.workspace_info",
                status="warn",
                message=f"workspace_info smoke failed: {exc}",
            )
        )
    return checks


def cursor_config_checks(root: Path) -> list[Check]:
    config_path = root / ".cursor" / "mcp.json"
    if not config_path.is_file():
        return [
            Check(
                id="mcp.config",
                status="info",
                message="no .cursor/mcp.json in project root",
            )
        ]

    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [Check(id="mcp.config", status="fail", message=f"invalid mcp.json: {exc}")]

    servers = payload.get("mcpServers", {})
    if not isinstance(servers, dict):
        return [Check(id="mcp.config", status="fail", message="mcpServers must be an object")]

    stubborn_servers = [
        name
        for name, cfg in servers.items()
        if isinstance(cfg, dict) and "stubborn" in str(cfg.get("command", ""))
    ]
    if stubborn_servers:
        return [
            Check(
                id="mcp.config",
                status="pass",
                message=f".cursor/mcp.json references stubborn-mcp ({', '.join(stubborn_servers)})",
            )
        ]
    return [
        Check(
            id="mcp.config",
            status="warn",
            message=".cursor/mcp.json present but no stubborn-mcp server entry found",
            hint='Add "command": "stubborn-mcp" under mcpServers (stubborn-mcp)',
        )
    ]


def delegation_checks() -> list[Check]:
    return [
        Check(
            id="delegate.core",
            status="info",
            message="symbol graph ingest is diagnosed by stubborn-stub",
            hint="Run: stubborn doctor (stubborn-stub package)",
        )
    ]
