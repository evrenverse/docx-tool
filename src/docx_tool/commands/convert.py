"""Convert legacy .doc documents to .docx using an isolated LibreOffice profile."""

from pathlib import Path

import typer

from docx_tool.commands.common import libreoffice_convert, require_file


def convert(
    file: Path = typer.Argument(..., help="Path to a legacy .doc file."),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output DOCX path."),
) -> None:
    """Convert one legacy binary Word document to DOCX."""
    require_file(file, ".doc")
    output_path = output or file.with_suffix(".docx")
    if output_path.suffix.lower() != ".docx":
        typer.echo(f"Error: output must end in .docx: {output_path}", err=True)
        raise typer.Exit(code=1)
    libreoffice_convert(file, output_path, "docx")
    typer.echo(f"Converted: {file.name} -> {output_path}")
