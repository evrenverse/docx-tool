import pytest
import typer

from docx_tool.commands import common


def test_require_file_enforces_input_limit(tmp_path, monkeypatch):
    path = tmp_path / "large.docx"
    path.write_bytes(b"too large")
    monkeypatch.setattr(common, "MAX_INPUT_BYTES", 4)

    with pytest.raises(typer.Exit) as excinfo:
        common.require_file(path, ".docx")

    assert excinfo.value.exit_code == 2


def test_json_size_limit(monkeypatch):
    monkeypatch.setattr(common, "MAX_JSON_INPUT_BYTES", 4)

    with pytest.raises(typer.Exit) as excinfo:
        common.ensure_json_size("12345")

    assert excinfo.value.exit_code == 2
