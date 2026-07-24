"""Export DOCX documents to PDF using an isolated LibreOffice profile."""

from pathlib import Path

import typer

from docx_tool.commands.common import libreoffice_convert, require_file


def export_pdf(
    file: Path = typer.Argument(..., help="Path to the DOCX file."),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output PDF path."),
) -> None:
    """Export one DOCX document to PDF."""
    require_file(file, ".docx")
    output_path = output or file.with_suffix(".pdf")
    if output_path.suffix.lower() != ".pdf":
        typer.echo(f"Error: output must end in .pdf: {output_path}", err=True)
        raise typer.Exit(code=1)
    libreoffice_convert(file, output_path, "pdf")
    typer.echo(f"Exported: {file.name} -> {output_path}")
