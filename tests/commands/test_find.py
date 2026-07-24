import json

from typer.testing import CliRunner

from docx_tool.cli import app

runner = CliRunner()


def test_find_paragraph(sample_docx):
    result = runner.invoke(app, ["find", str(sample_docx), "quarterly", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["matches"][0]["kind"] == "paragraph"
    assert data["matches"][0]["paragraph"] == 1


def test_find_table_cell(sample_docx):
    result = runner.invoke(app, ["find", str(sample_docx), "Alpha", "--json"])
    assert result.exit_code == 0
    match = json.loads(result.output)["matches"][0]
    assert (match["table"], match["row"], match["column"]) == (1, 2, 1)


def test_find_control_by_id(controls_docx):
    result = runner.invoke(app, ["find", str(controls_docx), "ProjectName", "--json"])
    assert result.exit_code == 0
    assert json.loads(result.output)["matches"][0]["kind"] == "content_control"


def test_find_no_match(sample_docx):
    result = runner.invoke(app, ["find", str(sample_docx), "not present", "--json"])
    assert result.exit_code == 1
    assert json.loads(result.output)["total"] == 0
