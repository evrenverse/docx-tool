import json

from typer.testing import CliRunner

from docx_tool.cli import app

runner = CliRunner()


def test_read_scoped_paragraphs(sample_docx):
    result = runner.invoke(
        app,
        ["read", str(sample_docx), "--paragraphs", "1,3", "--json"],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert [item["index"] for item in data["paragraphs"]] == [1, 3]
    assert data["paragraphs"][0]["text"] == "Quarterly Report"


def test_read_table_cells(sample_docx):
    result = runner.invoke(
        app,
        ["read", str(sample_docx), "--table", "1", "--cells", "1:1,2:2", "--json"],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    rows = data["tables"][0]["rows"]
    assert rows[0]["cells"] == [{"column": 1, "text": "Item"}]
    assert rows[1]["cells"] == [{"column": 2, "text": "10"}]


def test_read_cells_requires_table(sample_docx):
    result = runner.invoke(app, ["read", str(sample_docx), "--cells", "1:1"])
    assert result.exit_code == 2


def test_read_reports_revisions(tracked_docx):
    result = runner.invoke(app, ["read", str(tracked_docx), "--json"])
    assert result.exit_code == 0
    revisions = json.loads(result.output)["revisions"]
    assert {item["type"] for item in revisions} == {"insertion", "deletion"}
    assert {item["text"] for item in revisions} == {"added", "removed"}


def test_read_missing_paragraph(sample_docx):
    result = runner.invoke(
        app,
        ["read", str(sample_docx), "--paragraphs", "99", "--json"],
    )
    assert result.exit_code == 1
    assert json.loads(result.output)["missing"] == ["P99"]
