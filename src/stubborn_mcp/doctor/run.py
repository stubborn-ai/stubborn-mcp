"""Run stubborn-mcp doctor."""

from __future__ import annotations

from pathlib import Path

from stubborn_mcp.__version__ import __version__
from stubborn_mcp.doctor.checks import (
    cursor_config_checks,
    database_checks,
    delegation_checks,
    runtime_checks,
)
from stubborn_mcp.doctor.models import DoctorReport


def run_doctor(
    project_root: Path,
    *,
    db_path: Path | None = None,
    fix_hint: bool = True,
) -> DoctorReport:
    root = project_root.resolve()
    report = DoctorReport(version=__version__, cwd=str(root))
    report.checks.extend(runtime_checks())
    report.checks.extend(cursor_config_checks(root))
    report.checks.extend(database_checks(db_path))
    if fix_hint:
        report.checks.extend(delegation_checks())
    return report
