"""Add a simple comment through python-docx's public API."""

import json
from pathlib import Path

import typer

from docx_tool.commands.common import load_document, reject_digitally_signed, save_document


def comment(
    file: Path = typer.Argument(..., help="Path to the DOCX file."),
    paragraph: int = typer.Option(
        ...,
        "--paragraph",
        "-p",
        min=1,
        help="One-based body paragraph index to comment.",
    ),
    text: str = typer.Option(..., "--text", help="Comment text."),
    author: str = typer.Option(..., "--author", help="Comment author."),
    initials: str | None = typer.Option(None, "--initials", help="Optional author initials."),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output DOCX path."),
    output_json: bool = typer.Option(False, "--json", help="Output a structured result."),
) -> None:
    """Comment an entire body paragraph at run boundaries."""
    document = load_document(file)
    reject_digitally_signed(file)
    if paragraph > len(document.paragraphs):
        typer.echo(
            f"Error: paragraph {paragraph} out of range (1-{len(document.paragraphs)})",
            err=True,
        )
        raise typer.Exit(code=1)
    target = document.paragraphs[paragraph - 1]
    if not target.runs:
        typer.echo("Error: target paragraph has no runs to anchor a comment", err=True)
        raise typer.Exit(code=1)
    if "".join(run.text for run in target.runs) != target.text:
        typer.echo(
            "Error: paragraph contains text outside ordinary runs "
            "(for example a hyperlink) and cannot be commented safely",
            err=True,
        )
        raise typer.Exit(code=1)
    if not text:
        typer.echo("Error: comment text must not be empty", err=True)
        raise typer.Exit(code=1)
    if not author:
        typer.echo("Error: author must not be empty", err=True)
        raise typer.Exit(code=1)

    created = document.add_comment(
        runs=target.runs,
        text=text,
        author=author,
        initials=initials,
    )
    output_path = output or file
    save_document(document, output_path)
    data = {
        "file": output_path.name,
        "comment_id": created.comment_id,
        "paragraph": paragraph,
        "author": author,
    }
    if output_json:
        typer.echo(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        typer.echo(f"Commented: paragraph {paragraph} in {output_path.name}")
