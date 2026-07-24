"""Show concise DOCX structure."""

import json
from pathlib import Path

import typer

from docx_tool.commands.common import load_document
from docx_tool.commands.document import (
    comments_data,
    extract_checkboxes,
    extract_content_controls,
    extract_revisions,
)


def info(
    file: Path = typer.Argument(..., help="Path to the DOCX file."),
    output_json: bool = typer.Option(False, "--json", help="Output as JSON."),
) -> None:
    """Show document structure without dumping its content."""
    document = load_document(file)
    tables = [
        {
            "index": index,
            "rows": len(table.rows),
            "columns": len(table.columns),
        }
        for index, table in enumerate(document.tables, 1)
    ]
    images = sum(
        1 for relationship in document.part.rels.values() if "image" in relationship.reltype
    )
    checkboxes = extract_checkboxes(document)
    controls = extract_content_controls(document)
    comments = comments_data(document)
    revisions = extract_revisions(document)
    data = {
        "file": file.name,
        "paragraphs": len(document.paragraphs),
        "tables": tables,
        "images": images,
        "sections": len(document.sections),
        "checkboxes": checkboxes,
        "content_controls": controls,
        "comments": len(comments),
        "tracked_changes": len(revisions),
    }

    if output_json:
        typer.echo(json.dumps(data, indent=2, ensure_ascii=False))
        return

    typer.echo(
        f"File: {file.name} | Paragraphs: {data['paragraphs']} | "
        f"Tables: {len(tables)} | Images: {images} | "
        f"Comments: {len(comments)} | Tracked changes: {len(revisions)}"
    )
    for table in tables:
        typer.echo(f"  Table {table['index']}: {table['rows']} rows x {table['columns']} columns")
