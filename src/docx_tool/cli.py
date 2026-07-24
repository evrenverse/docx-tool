"""Agent-friendly DOCX command-line interface."""

import typer

app = typer.Typer(
    name="docx-tool",
    help="Inspect and edit DOCX documents from scripts and AI agents.",
    no_args_is_help=True,
)


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit."),
) -> None:
    if version:
        from docx_tool import __version__

        typer.echo(f"docx-tool {__version__}")
        raise typer.Exit()


from docx_tool.commands.accept_changes import accept_changes as accept_changes_cmd  # noqa: E402
from docx_tool.commands.batch import batch as batch_cmd  # noqa: E402
from docx_tool.commands.comment import comment as comment_cmd  # noqa: E402
from docx_tool.commands.convert import convert as convert_cmd  # noqa: E402
from docx_tool.commands.export_pdf import export_pdf as export_pdf_cmd  # noqa: E402
from docx_tool.commands.find import find as find_cmd  # noqa: E402
from docx_tool.commands.info import info as info_cmd  # noqa: E402
from docx_tool.commands.read import read as read_cmd  # noqa: E402
from docx_tool.commands.system import capabilities as capabilities_cmd  # noqa: E402
from docx_tool.commands.system import doctor as doctor_cmd  # noqa: E402
from docx_tool.commands.system import schema as schema_cmd  # noqa: E402
from docx_tool.commands.system import version as version_cmd  # noqa: E402
from docx_tool.commands.write import write as write_cmd  # noqa: E402

app.command(name="info", help="Show document structure and feature counts.")(info_cmd)
app.command(name="read", help="Read body paragraphs, tables, fields, and revisions.")(read_cmd)
app.command(name="find", help="Find text in body paragraphs, tables, fields, and comments.")(
    find_cmd
)
app.command(name="write", help="Apply a validated, all-or-nothing JSON edit batch.")(write_cmd)
app.command(name="batch", help="Alias for write.")(batch_cmd)
app.command(name="comment", help="Add a comment to a body paragraph.")(comment_cmd)
app.command(name="accept-changes", help="Accept supported tracked changes without LibreOffice.")(
    accept_changes_cmd
)
app.command(name="convert", help="Convert a legacy .doc file to .docx with LibreOffice.")(
    convert_cmd
)
app.command(name="export-pdf", help="Export a DOCX file to PDF with LibreOffice.")(export_pdf_cmd)
app.command(name="capabilities", help="Describe the stable automation contract.")(capabilities_cmd)
app.command(name="doctor", help="Check runtime requirements without opening a DOCX.")(doctor_cmd)
app.command(name="schema", help="Print a bundled JSON Schema.")(schema_cmd)
app.command(name="version", help="Show version and contract information.")(version_cmd)
