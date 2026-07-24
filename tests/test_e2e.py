import json

from docx import Document
from typer.testing import CliRunner

from docx_tool.cli import app

runner = CliRunner()


def test_inspect_edit_verify_workflow(sample_docx, tmp_path):
    info = runner.invoke(app, ["info", str(sample_docx), "--json"])
    assert info.exit_code == 0

    located = runner.invoke(app, ["find", str(sample_docx), "TARGET", "--json"])
    assert located.exit_code == 0

    output = tmp_path / "finished.docx"
    edited = runner.invoke(
        app,
        ["batch", str(sample_docx), "-", "--output", str(output), "--json"],
        input=json.dumps(
            [
                {"type": "replace", "search": "TARGET", "value": "complete"},
                {"type": "table_cell", "table": 1, "row": 2, "column": 2, "value": "99"},
            ]
        ),
    )
    assert edited.exit_code == 0, edited.output

    verified = runner.invoke(
        app,
        ["read", str(output), "--paragraphs", "3", "--table", "1", "--cells", "2:2", "--json"],
    )
    assert verified.exit_code == 0
    data = json.loads(verified.output)
    assert data["paragraphs"][0]["text"] == "Replace complete in this paragraph."
    assert data["tables"][0]["rows"][0]["cells"][0]["text"] == "99"
    Document(output)
