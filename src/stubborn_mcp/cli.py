"""CLI for stubborn-mcp: MCP server and doctor diagnostics."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from stubborn_mcp.doctor.report import format_json, format_text
from stubborn_mcp.doctor.run import run_doctor
from stubborn_mcp.server import mcp

app = typer.Typer(
    name="stubborn-mcp",
    help="MCP server and setup diagnostics for Stubborn.",
    no_args_is_help=False,
)


@app.callback(invoke_without_command=True)
def root(ctx: typer.Context) -> None:
    """Default: run MCP stdio server when no subcommand is given."""
    if ctx.invoked_subcommand is None:
        mcp.run()


@app.command("serve")
def serve_cmd() -> None:
    """Run the MCP server over stdio."""
    mcp.run()


@app.command("doctor")
def doctor_cmd(
    path: Path = typer.Argument(
        Path("."),
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        help="Project root to inspect",
    ),
    db: Optional[Path] = typer.Option(
        None,
        "--db",
        help="SQLite symbol graph (default: STUBBORN_DB)",
    ),
    json_output: bool = typer.Option(False, "--json", help="Emit Doctor Report v1 JSON"),
    fix_hint: bool = typer.Option(
        True,
        "--fix-hint/--no-fix-hint",
        help="Include copy-paste hints in human output",
    ),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Suppress output; exit code only"),
) -> None:
    """Diagnose MCP package readiness and STUBBORN_DB wiring (read-only)."""
    report = run_doctor(path, db_path=db, fix_hint=fix_hint)
    if not quiet:
        if json_output:
            typer.echo(format_json(report))
        else:
            typer.echo(format_text(report, fix_hint=fix_hint))
    raise typer.Exit(code=report.exit_code())


def main() -> None:
    app()


if __name__ == "__main__":
    main()
