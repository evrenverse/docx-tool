"""Find text in the python-docx document model."""

import json
from pathlib import Path

import typer

from docx_tool.commands.common import load_document
from docx_tool.commands.document import (
    comments_data,
    extract_checkboxes,
    extract_content_controls,
    iter_table_cells,
)


def find(
    file: Path = typer.Argument(..., help="Path to the DOCX file."),
    text: str = typer.Argument(..., help="Text to locate."),
    exact: bool = typer.Option(False, "--exact", help="Use a case-sensitive full-value match."),
    max_results: int = typer.Option(50, "--max", min=1, help="Maximum matches to return."),
    output_json: bool = typer.Option(False, "--json", help="Output as JSON."),
) -> None:
    """Find text without dumping the document."""
    document = load_document(file)

    def matches(value: str) -> bool:
        return value == text if exact else text.casefold() in value.casefold()

    found = []
    for index, paragraph in enumerate(document.paragraphs, 1):
        if matches(paragraph.text):
            found.append({"kind": "paragraph", "paragraph": index, "text": paragraph.text})
    for table, row, column, cell in iter_table_cells(document):
        if matches(cell.text):
            found.append(
                {
                    "kind": "table_cell",
                    "table": table,
                    "row": row,
                    "column": column,
                    "text": cell.text,
                }
            )
    for kind, entries, value_key in (
        ("checkbox", extract_checkboxes(document), "text"),
        ("content_control", extract_content_controls(document), "value"),
        ("comment", comments_data(document), "text"),
    ):
        found.extend(
            {"kind": kind, **entry}
            for entry in entries
            if matches(str(entry.get("id", ""))) or matches(str(entry.get(value_key, "")))
        )

    total = len(found)
    shown = found[:max_results]
    if output_json:
        typer.echo(
            json.dumps(
                {"query": text, "matches": shown, "total": total, "truncated": total > len(shown)},
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        for match in shown:
            typer.echo(json.dumps(match, ensure_ascii=False))
        if total > len(shown):
            typer.echo(f"Showing {len(shown)} of {total} matches.")
        elif total == 0:
            typer.echo(f'No matches found for "{text}".')
    raise typer.Exit(code=0 if total else 1)
