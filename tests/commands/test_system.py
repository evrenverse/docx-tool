import json

from typer.testing import CliRunner

from docx_tool.cli import app
from docx_tool.commands import system

runner = CliRunner()


def test_capabilities_json():
    result = runner.invoke(app, ["capabilities", "--json"])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["tool"] == "docx-tool"
    assert payload["contract_version"] == "1"
    assert "batch" in payload["schemas"]


def test_doctor_json():
    result = runner.invoke(app, ["doctor", "--json"])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["tool"] == "docx-tool"
    assert payload["status"] in {"ok", "degraded"}
    assert any(check["name"] == "libreoffice" for check in payload["checks"])


def test_schema_and_version_json():
    schema_result = runner.invoke(app, ["schema", "batch"])
    assert schema_result.exit_code == 0, schema_result.output
    assert json.loads(schema_result.output)["title"] == "docx-tool batch input"

    version_result = runner.invoke(app, ["version", "--json"])
    assert version_result.exit_code == 0, version_result.output
    assert json.loads(version_result.output)["contract_version"] == "1"


def test_unknown_required_dependency_is_usage_error():
    result = runner.invoke(app, ["doctor", "--require", "ghost"])
    assert result.exit_code == 2
    assert "unknown optional dependency" in result.output


def test_human_readable_capabilities_version_and_doctor():
    capabilities_result = runner.invoke(app, ["capabilities"])
    assert capabilities_result.exit_code == 0
    assert "agent contract v1" in capabilities_result.output

    version_result = runner.invoke(app, ["version"])
    assert version_result.exit_code == 0
    assert version_result.output.startswith("docx-tool ")

    doctor_result = runner.invoke(app, ["doctor"])
    assert doctor_result.exit_code == 0
    assert "python: ok" in doctor_result.output


def test_schema_list_and_unknown_schema():
    list_result = runner.invoke(app, ["schema"])
    assert list_result.exit_code == 0
    assert json.loads(list_result.output)["schemas"] == [
        "batch",
        "capabilities",
        "doctor",
        "version",
    ]

    unknown_result = runner.invoke(app, ["schema", "ghost"])
    assert unknown_result.exit_code == 2
    assert "unknown schema" in unknown_result.output


def test_required_libreoffice_failure_is_machine_readable(monkeypatch):
    monkeypatch.setattr(system.shutil, "which", lambda _name: None)

    result = runner.invoke(
        app,
        ["doctor", "--json", "--require", "libreoffice"],
    )

    assert result.exit_code == 2
    assert json.loads(result.output)["status"] == "error"
