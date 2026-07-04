"""Tests for MCP tool wiring (delegates to stubborn.api)."""

from __future__ import annotations

from pathlib import Path

import pytest
from stubborn.ingest.scip import load_scip_index
from stubborn.store.writer import (
    ContractEndpointRecord,
    ContractSchemaConstraintRecord,
    ContractSnapshot,
    IndexWriter,
)

from stubborn_mcp.server import get_context, list_contracts, list_symbols, metrics, workspace_info

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "minimal.json"
TARGET = "semanticdb maven com/example/OrderService#process()."
ENDPOINT = "openapi customers-service:v1 GET /owners/{ownerId}"
DEMO_JAVA = (
    Path(__file__).resolve().parents[2] / "stubborn" / "examples" / "demo-spring" / "src" / "main" / "java"
)


@pytest.fixture()
def indexed_db(tmp_path: Path) -> Path:
    db = tmp_path / "symbols.db"
    IndexWriter(db).write(load_scip_index(FIXTURE))
    return db


@pytest.fixture()
def contract_only_db(tmp_path: Path) -> Path:
    db = tmp_path / "contracts.db"
    IndexWriter(db).write_contract(
        ContractSnapshot(
            scip_source="contracts/openapi.json",
            language="openapi",
            endpoints=(
                ContractEndpointRecord(
                    stable_id=ENDPOINT,
                    protocol="http",
                    service="customers-service",
                    version="v1",
                    method_or_verb="GET",
                    address="/owners/{ownerId}",
                    display_name="getOwner",
                    schema_constraints=(
                        ContractSchemaConstraintRecord(
                            location="path",
                            field_path="ownerId",
                            type_name="integer",
                            required=True,
                        ),
                    ),
                ),
            ),
        ),
        workspace="petclinic",
        repo_key="customers-openapi",
    )
    return db


def test_mcp_get_context(indexed_db: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STUBBORN_DB", str(indexed_db))
    ctx = get_context(TARGET)
    assert ctx["text"]
    assert ctx["symbol_count"] >= 1
    assert "contract_endpoints" in ctx


def test_mcp_list_symbols(indexed_db: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STUBBORN_DB", str(indexed_db))
    listing = list_symbols(query="Order")
    assert listing["returned"] >= 1
    assert listing["symbols"]


def test_mcp_list_contracts_and_endpoint_context(
    contract_only_db: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("STUBBORN_DB", str(contract_only_db))

    workspace = workspace_info("petclinic")
    listing = list_contracts(workspace="petclinic")
    ctx = get_context(ENDPOINT, format="stubborn-dsl", workspace="petclinic")

    assert workspace["code_repo_count"] == 0
    assert workspace["contract_source_count"] == 1
    assert workspace["contract_endpoint_count"] == 1
    assert listing["returned"] == 1
    assert listing["contract_endpoints"][0]["stable_id"] == ENDPOINT
    assert ctx["symbol_count"] == 0
    assert ctx["contract_edges"] == []
    assert ctx["contract_endpoints"][0]["stable_id"] == ENDPOINT
    assert "schema path.ownerId integer required" in ctx["text"]


@pytest.mark.skipif(not DEMO_JAVA.is_dir(), reason="demo-spring sources not in workspace")
def test_mcp_metrics(indexed_db: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STUBBORN_DB", str(indexed_db))
    kpi = metrics(TARGET, str(DEMO_JAVA), include_stub_text=False)
    assert "stub_text" not in kpi
    assert kpi["token_savings_percent"] > 0
