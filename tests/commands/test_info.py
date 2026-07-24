import json

from typer.testing import CliRunner

from docx_tool.cli import app

runner = CliRunner()


def test_info_json(sample_docx):
    result = runner.invoke(app, ["info", str(sample_docx), "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["paragraphs"] == 4
    assert data["tables"] == [{"index": 1, "rows": 2, "columns": 2}]
    assert data["comments"] == 0
    assert data["tracked_changes"] == 0


def test_info_controls(controls_docx):
    result = runner.invoke(app, ["info", str(controls_docx), "--json"])
    data = json.loads(result.output)
    assert data["checkboxes"][0]["id"] == "Approved"
    assert data["content_controls"][0]["id"] == "ProjectName"


def test_info_missing_file(tmp_path):
    result = runner.invoke(app, ["info", str(tmp_path / "missing.docx")])
    assert result.exit_code == 1
    assert "file not found" in result.output.lower()
