from typer.testing import CliRunner

from docx_tool.cli import app

runner = CliRunner()


def test_convert_requires_doc_suffix(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("not a doc")
    result = runner.invoke(app, ["convert", str(source)])
    assert result.exit_code == 1
    assert "expected a .doc file" in result.output


def test_convert_delegates_to_isolated_converter(tmp_path, monkeypatch):
    source = tmp_path / "legacy.doc"
    source.write_bytes(b"legacy")
    output = tmp_path / "modern.docx"
    called = {}

    def fake_convert(file, target, target_format):
        called.update(file=file, target=target, target_format=target_format)

    monkeypatch.setattr("docx_tool.commands.convert.libreoffice_convert", fake_convert)
    result = runner.invoke(app, ["convert", str(source), "--output", str(output)])
    assert result.exit_code == 0
    assert called == {"file": source, "target": output, "target_format": "docx"}
