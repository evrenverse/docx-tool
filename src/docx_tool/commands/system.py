"""Machine-readable capability discovery and runtime diagnostics."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
from importlib.resources import files

import typer

from docx_tool import __version__
from docx_tool.commands.common import MAX_BATCH_ITEMS, MAX_INPUT_BYTES, MAX_JSON_INPUT_BYTES

CONTRACT_VERSION = "1"
SCHEMA_NAMES = ("batch", "capabilities", "doctor", "version")


def _emit(payload: object) -> None:
    typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))


def _capability_payload() -> dict:
    return {
        "schema_version": CONTRACT_VERSION,
        "tool": "docx-tool",
        "tool_version": __version__,
        "contract_version": CONTRACT_VERSION,
        "addressing": "one-based paragraphs, tables, rows, and columns",
        "runtime_network_access": False,
        "atomic_writes": True,
        "structured_stdout": True,
        "diagnostics_stderr": True,
        "commands": [
            {"name": "info", "mutates": False, "json": True},
            {"name": "find", "mutates": False, "json": True},
            {"name": "read", "mutates": False, "json": True},
            {"name": "write", "mutates": True, "json": True},
            {"name": "batch", "mutates": True, "json": True},
            {"name": "comment", "mutates": True, "json": True},
            {"name": "accept-changes", "mutates": True, "json": True},
            {
                "name": "convert",
                "mutates": True,
                "json": False,
                "optional_dependency": "libreoffice",
            },
            {
                "name": "export-pdf",
                "mutates": True,
                "json": False,
                "optional_dependency": "libreoffice",
            },
            {"name": "capabilities", "mutates": False, "json": True},
            {"name": "doctor", "mutates": False, "json": True},
            {"name": "schema", "mutates": False, "json": True},
            {"name": "version", "mutates": False, "json": True},
        ],
        "optional_dependencies": ["libreoffice"],
        "schemas": list(SCHEMA_NAMES),
        "limits": {
            "input_docx_bytes": MAX_INPUT_BYTES,
            "json_input_bytes": MAX_JSON_INPUT_BYTES,
            "batch_items": MAX_BATCH_ITEMS,
            "expanded_docx_bytes": 500 * 1024 * 1024,
        },
    }


def capabilities(
    output_json: bool = typer.Option(False, "--json", help="Output the contract as JSON."),
) -> None:
    """Describe commands, conventions, dependencies, and bundled schemas."""
    payload = _capability_payload()
    if output_json:
        _emit(payload)
        return
    typer.echo(f"docx-tool {__version__} (agent contract v{CONTRACT_VERSION})")
    typer.echo("Addressing: one-based paragraphs, tables, rows, and columns")
    typer.echo("Writes: validated, reopened, and atomically published")
    typer.echo("Runtime network access: none")
    typer.echo("Optional dependency: LibreOffice (convert and export-pdf)")


def version(
    output_json: bool = typer.Option(False, "--json", help="Output version information as JSON."),
) -> None:
    """Show the tool and agent-contract versions."""
    if output_json:
        _emit(
            {
                "schema_version": CONTRACT_VERSION,
                "tool": "docx-tool",
                "version": __version__,
                "contract_version": CONTRACT_VERSION,
            }
        )
        return
    typer.echo(f"docx-tool {__version__}")


def _module_check(name: str, import_name: str) -> dict:
    available = importlib.util.find_spec(import_name) is not None
    return {
        "name": name,
        "required": True,
        "ok": available,
        "detail": "available" if available else "not importable",
    }


def doctor(
    output_json: bool = typer.Option(False, "--json", help="Output checks as JSON."),
    require: list[str] | None = typer.Option(
        None,
        "--require",
        help="Require an optional dependency. Repeatable: --require libreoffice.",
    ),
) -> None:
    """Check runtime requirements without opening a DOCX."""
    required = {item.strip().lower() for item in (require or [])}
    unknown = required - {"libreoffice"}
    if unknown:
        typer.echo(f"Error: unknown optional dependency: {sorted(unknown)[0]}", err=True)
        raise typer.Exit(code=2)

    checks = [
        {
            "name": "python",
            "required": True,
            "ok": sys.version_info >= (3, 12),
            "detail": sys.version.split()[0],
        },
        _module_check("python-docx", "docx"),
        _module_check("lxml", "lxml"),
    ]
    try:
        with tempfile.NamedTemporaryFile(prefix="docx-tool-doctor-"):
            pass
        temp_check = {
            "name": "temporary-directory",
            "required": True,
            "ok": True,
            "detail": "writable",
        }
    except OSError as exc:
        temp_check = {
            "name": "temporary-directory",
            "required": True,
            "ok": False,
            "detail": str(exc),
        }
    checks.append(temp_check)

    executable = shutil.which("soffice") or shutil.which("libreoffice")
    checks.append(
        {
            "name": "libreoffice",
            "required": "libreoffice" in required,
            "ok": executable is not None,
            "detail": executable or "not found; required only for conversion and PDF export",
        }
    )
    failed_required = any(check["required"] and not check["ok"] for check in checks)
    missing_optional = any(not check["required"] and not check["ok"] for check in checks)
    status = "error" if failed_required else "degraded" if missing_optional else "ok"
    payload = {
        "schema_version": CONTRACT_VERSION,
        "tool": "docx-tool",
        "tool_version": __version__,
        "status": status,
        "checks": checks,
    }
    if output_json:
        _emit(payload)
    else:
        for check in checks:
            state = "ok" if check["ok"] else "missing"
            typer.echo(f"{check['name']}: {state} ({check['detail']})")
    if failed_required:
        raise typer.Exit(code=2)


def schema(
    name: str | None = typer.Argument(None, help="Schema name to print."),
) -> None:
    """Print a bundled JSON Schema, or list available schema names."""
    if name is None:
        _emit({"schema_version": CONTRACT_VERSION, "schemas": list(SCHEMA_NAMES)})
        return
    normalized = name.lower()
    if normalized not in SCHEMA_NAMES:
        typer.echo(
            f"Error: unknown schema {name!r}; available: {', '.join(SCHEMA_NAMES)}",
            err=True,
        )
        raise typer.Exit(code=2)
    resource = files("docx_tool.schemas").joinpath(f"{normalized}.schema.json")
    typer.echo(resource.read_text(encoding="utf-8").rstrip())
