import json

from docx import Document
from typer.testing import CliRunner

from docx_tool.cli import app

runner = CliRunner()


def test_add_comment(sample_docx, tmp_path):
    output = tmp_path / "commented.docx"
    result = runner.invoke(
        app,
        [
            "comment",
            str(sample_docx),
            "--paragraph",
            "2",
            "--text",
            "Please verify this owner.",
            "--author",
            "Reviewer",
            "--initials",
            "RV",
            "--output",
            str(output),
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.output)["paragraph"] == 2
    comments = list(Document(output).comments)
    assert len(comments) == 1
    assert comments[0].text == "Please verify this owner."
    assert comments[0].author == "Reviewer"


def test_comment_out_of_range(sample_docx):
    result = runner.invoke(
        app,
        [
            "comment",
            str(sample_docx),
            "--paragraph",
            "99",
            "--text",
            "No",
            "--author",
            "Reviewer",
        ],
    )
    assert result.exit_code == 1
