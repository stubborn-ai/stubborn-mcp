"""Tests for MCP tool wiring (delegates to stubborn.api)."""

from __future__ import annotations

from pathlib import Path

import pytest
from stubborn.ingest.scip import load_scip_index
from stubborn.store.writer import IndexWriter

from stubborn_mcp.server import get_context, list_symbols, metrics

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "minimal.json"
TARGET = "semanticdb maven com/example/OrderService#process()."
DEMO_JAVA = (
    Path(__file__).resolve().parents[2] / "stubborn" / "examples" / "demo-spring" / "src" / "main" / "java"
)


@pytest.fixture()
def indexed_db(tmp_path: Path) -> Path:
    db = tmp_path / "symbols.db"
    IndexWriter(db).write(load_scip_index(FIXTURE))
    return db


def test_mcp_get_context(indexed_db: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STUBBORN_DB", str(indexed_db))
    ctx = get_context(TARGET)
    assert ctx["text"]
    assert ctx["symbol_count"] >= 1


def test_mcp_list_symbols(indexed_db: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STUBBORN_DB", str(indexed_db))
    listing = list_symbols(query="Order")
    assert listing["returned"] >= 1
    assert listing["symbols"]


@pytest.mark.skipif(not DEMO_JAVA.is_dir(), reason="demo-spring sources not in workspace")
def test_mcp_metrics(indexed_db: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STUBBORN_DB", str(indexed_db))
    kpi = metrics(TARGET, str(DEMO_JAVA), include_stub_text=False)
    assert "stub_text" not in kpi
    assert kpi["token_savings_percent"] > 0
