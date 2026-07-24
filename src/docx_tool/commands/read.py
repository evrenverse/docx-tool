"""Read body paragraphs, tables, controls, comments, and revisions."""

import json
from pathlib import Path
from typing import Any

import typer

from docx_tool.commands.common import load_document
from docx_tool.commands.document import (
    comments_data,
    extract_checkboxes,
    extract_content_controls,
    extract_revisions,
)

LARGE_READ_THRESHOLD = 500


def _parse_indices(specification: str, flag: str) -> list[int]:
    indices = []
    for item in specification.split(","):
        try:
            index = int(item.strip())
        except ValueError:
            typer.echo(f"Error: {flag} expects comma-separated integers", err=True)
            raise typer.Exit(code=2)
        if index < 1:
            typer.echo(f"Error: {flag} uses one-based positive indices", err=True)
            raise typer.Exit(code=2)
        indices.append(index)
    return indices


def _parse_cells(specification: str) -> list[tuple[int, int]]:
    result = []
    for item in specification.split(","):
        parts = item.strip().split(":")
        if len(parts) != 2:
            typer.echo("Error: --cells expects ROW:COL pairs such as 1:2,2:3", err=True)
            raise typer.Exit(code=2)
        try:
            row, column = (int(part) for part in parts)
        except ValueError:
            typer.echo("Error: --cells expects ROW:COL pairs such as 1:2,2:3", err=True)
            raise typer.Exit(code=2)
        if row < 1 or column < 1:
            typer.echo("Error: --cells uses one-based positive indices", err=True)
            raise typer.Exit(code=2)
        result.append((row, column))
    return result


def read(
    file: Path = typer.Argument(..., help="Path to the DOCX file."),
    paragraphs: str | None = typer.Option(
        None,
        "--paragraphs",
        help="Comma-separated one-based body paragraph indices.",
    ),
    table: int | None = typer.Option(
        None,
        "--table",
        "-t",
        help="Read only table N (one-based).",
    ),
    cells: str | None = typer.Option(
        None,
        "--cells",
        help="With --table, read ROW:COL pairs such as 1:2,2:3.",
    ),
    output_json: bool = typer.Option(False, "--json", help="Output as JSON."),
    confirm_large: bool = typer.Option(
        False,
        "--confirm-large",
        help="Allow an unscoped read of more than 500 paragraphs and cells.",
    ),
) -> None:
    """Read scoped DOCX content using one-based indices."""
    document = load_document(file)
    if cells is not None and table is None:
        typer.echo("Error: --cells requires --table", err=True)
        raise typer.Exit(code=2)

    paragraph_indices = (
        _parse_indices(paragraphs, "--paragraphs")
        if paragraphs is not None
        else list(range(1, len(document.paragraphs) + 1))
    )
    if table is not None and not 1 <= table <= len(document.tables):
        typer.echo(f"Error: table {table} out of range (1-{len(document.tables)})", err=True)
        raise typer.Exit(code=1)

    if table is not None:
        tables_to_read = [table]
    elif paragraphs is not None:
        tables_to_read = []
    else:
        tables_to_read = list(range(1, len(document.tables) + 1))
    size = len(document.paragraphs) + sum(
        len(document.tables[index - 1].rows) * len(document.tables[index - 1].columns)
        for index in tables_to_read
    )
    scoped = paragraphs is not None or table is not None or cells is not None
    if not scoped and size > LARGE_READ_THRESHOLD and not confirm_large:
        typer.echo(
            f"Error: unscoped read covers {size} elements; use --paragraphs, "
            "--table/--cells, or --confirm-large",
            err=True,
        )
        raise typer.Exit(code=2)

    missing = []
    paragraph_data: list[dict[str, Any]] = []
    for index in paragraph_indices:
        if 1 <= index <= len(document.paragraphs):
            paragraph = document.paragraphs[index - 1]
            paragraph_data.append(
                {
                    "index": index,
                    "text": paragraph.text,
                    "style": paragraph.style.name if paragraph.style else "",
                }
            )
        else:
            missing.append(f"P{index}")

    cell_filter = set(_parse_cells(cells)) if cells is not None else None
    table_data: list[dict[str, Any]] = []
    for table_index in tables_to_read:
        current = document.tables[table_index - 1]
        rows = []
        for row_index, row in enumerate(current.rows, 1):
            values = []
            for column_index, cell in enumerate(row.cells, 1):
                if cell_filter is None or (row_index, column_index) in cell_filter:
                    values.append({"column": column_index, "text": cell.text})
            if values:
                rows.append({"row": row_index, "cells": values})
        table_data.append({"index": table_index, "rows": rows})
    if cell_filter is not None:
        assert table is not None
        current = document.tables[table - 1]
        for row, column in sorted(cell_filter):
            if row > len(current.rows) or column > len(current.columns):
                missing.append(f"T{table}:R{row}:C{column}")

    data = {
        "paragraphs": paragraph_data,
        "tables": table_data,
        "checkboxes": extract_checkboxes(document),
        "content_controls": extract_content_controls(document),
        "comments": comments_data(document),
        "revisions": extract_revisions(document),
        "missing": missing,
    }
    if output_json:
        typer.echo(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        for paragraph in paragraph_data:
            typer.echo(f"P{paragraph['index']}: {paragraph['text']}")
        for table_entry in table_data:
            typer.echo(f"\nTable {table_entry['index']}:")
            for row in table_entry["rows"]:
                rendered_values = " | ".join(
                    f"C{cell['column']}={cell['text']}" for cell in row["cells"]
                )
                typer.echo(f"  R{row['row']}: {rendered_values}")
        for item in missing:
            typer.echo(f"{item}: (missing)")
    found_content = bool(paragraph_data) or any(entry["rows"] for entry in table_data)
    raise typer.Exit(code=0 if found_content else 1)
