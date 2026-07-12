"""Tests for stubborn-mcp doctor."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from stubborn_mcp.cli import app
from stubborn_mcp.doctor.models import DOCTOR_REPORT_SCHEMA, PACKAGE_ID
from stubborn_mcp.doctor.run import run_doctor

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "minimal.json"


def test_mcp_doctor_warns_without_db(monkeypatch) -> None:
    monkeypatch.delenv("STUBBORN_DB", raising=False)
    report = run_doctor(Path.cwd(), fix_hint=False)
    assert report.exit_code() in (1, 2)
    assert any(check.id == "mcp.stubborn_db" for check in report.checks)


def test_mcp_doctor_with_db(tmp_path: Path, monkeypatch) -> None:
    from stubborn.ingest.scip import load_scip_index
    from stubborn.store.writer import IndexWriter

    db = tmp_path / "symbols.db"
    IndexWriter(db).write(load_scip_index(FIXTURE))
    monkeypatch.setenv("STUBBORN_DB", str(db))
    report = run_doctor(tmp_path, fix_hint=False)
    assert report.exit_code() == 0
    assert any(check.id == "mcp.db" and check.status == "pass" for check in report.checks)


def test_mcp_doctor_json_schema(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("STUBBORN_DB", raising=False)
    report = run_doctor(tmp_path, fix_hint=False)
    payload = report.to_dict()
    assert payload["schema"] == DOCTOR_REPORT_SCHEMA
    assert payload["package"] == PACKAGE_ID


def test_mcp_cli_doctor_json(tmp_path: Path, monkeypatch) -> None:
    from stubborn.ingest.scip import load_scip_index
    from stubborn.store.writer import IndexWriter

    db = tmp_path / "symbols.db"
    IndexWriter(db).write(load_scip_index(FIXTURE))
    monkeypatch.setenv("STUBBORN_DB", str(db))
    result = CliRunner().invoke(app, ["doctor", str(tmp_path), "--json", "--no-fix-hint"])
    assert result.exit_code == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["package"] == PACKAGE_ID


def test_mcp_cli_default_still_has_doctor_subcommand() -> None:
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "doctor" in result.stdout
