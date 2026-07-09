"""MCP server for Stubborn — agent integration over stdio."""

from stubborn_mcp.cli import main
from stubborn_mcp.server import mcp

__all__ = ["main", "mcp"]
