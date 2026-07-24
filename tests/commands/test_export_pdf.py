import shutil

import pytest
from typer.testing import CliRunner

from docx_tool.cli import app

runner = CliRunner()


def test_export_delegates_to_isolated_converter(sample_docx, tmp_path, monkeypatch):
    output = tmp_path / "sample.pdf"
    called = {}

    def fake_convert(file, target, target_format):
        called.update(file=file, target=target, target_format=target_format)

    monkeypatch.setattr("docx_tool.commands.export_pdf.libreoffice_convert", fake_convert)
    result = runner.invoke(app, ["export-pdf", str(sample_docx), "--output", str(output)])
    assert result.exit_code == 0
    assert called == {"file": sample_docx, "target": output, "target_format": "pdf"}


def test_export_rejects_non_pdf_output(sample_docx, tmp_path):
    result = runner.invoke(
        app,
        ["export-pdf", str(sample_docx), "--output", str(tmp_path / "wrong.txt")],
    )
    assert result.exit_code == 1


def test_export_with_real_libreoffice_when_available(sample_docx, tmp_path):
    if shutil.which("soffice") is None and shutil.which("libreoffice") is None:
        pytest.skip("LibreOffice is not installed")
    output = tmp_path / "sample.pdf"
    result = runner.invoke(app, ["export-pdf", str(sample_docx), "--output", str(output)])
    assert result.exit_code == 0, result.output
    assert output.read_bytes().startswith(b"%PDF-")
