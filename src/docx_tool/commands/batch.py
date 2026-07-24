"""Alias for the transactional write command."""

from pathlib import Path

import typer


def batch(
    file: Path = typer.Argument(..., help="Path to the DOCX file."),
    changes: str = typer.Argument(..., help="JSON file with operations, or '-' for stdin."),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output DOCX path."),
    output_json: bool = typer.Option(False, "--json", help="Output a structured result."),
) -> None:
    """Apply the write command's all-or-nothing JSON batch."""
    from docx_tool.commands.write import write

    write(file=file, changes=changes, output=output, output_json=output_json)
