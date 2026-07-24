"""Accept supported OOXML tracked changes without executing office macros."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import typer
from docx import Document
from lxml import etree

from docx_tool.commands.common import atomic_output, require_file

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
MAX_ENTRIES = 10_000
MAX_MEMBER_SIZE = 100 * 1024 * 1024
MAX_TOTAL_SIZE = 500 * 1024 * 1024
MAX_COMPRESSION_RATIO = 1_000

PROPERTY_CHANGES = {
    f"{W}rPrChange",
    f"{W}pPrChange",
    f"{W}tblPrChange",
    f"{W}tblGridChange",
    f"{W}trPrChange",
    f"{W}tcPrChange",
    f"{W}sectPrChange",
    f"{W}numberingChange",
}
RANGE_MARKERS = {
    f"{W}{name}"
    for name in (
        "moveFromRangeStart",
        "moveFromRangeEnd",
        "moveToRangeStart",
        "moveToRangeEnd",
        "customXmlInsRangeStart",
        "customXmlInsRangeEnd",
        "customXmlDelRangeStart",
        "customXmlDelRangeEnd",
        "customXmlMoveFromRangeStart",
        "customXmlMoveFromRangeEnd",
        "customXmlMoveToRangeStart",
        "customXmlMoveToRangeEnd",
    )
}
TRACKED_TAGS = (
    PROPERTY_CHANGES
    | RANGE_MARKERS
    | {
        f"{W}ins",
        f"{W}del",
        f"{W}moveFrom",
        f"{W}moveTo",
        f"{W}cellIns",
        f"{W}cellDel",
        f"{W}cellMerge",
    }
)


def _validate_archive(archive: zipfile.ZipFile) -> None:
    members = archive.infolist()
    if len(members) > MAX_ENTRIES:
        raise ValueError(f"DOCX contains too many ZIP entries ({len(members)})")
    total = 0
    names = {member.filename for member in members}
    if len(names) != len(members):
        raise ValueError("DOCX contains duplicate ZIP member names")
    if "[Content_Types].xml" not in names or "word/document.xml" not in names:
        raise ValueError("file is not a valid DOCX package")
    if any(name.lower().startswith("_xmlsignatures/") for name in names):
        raise ValueError("digitally signed DOCX files are not rewritten")
    for member in members:
        if member.flag_bits & 0x1:
            raise ValueError("encrypted ZIP members are not supported")
        if member.file_size > MAX_MEMBER_SIZE:
            raise ValueError(f"ZIP member is too large: {member.filename}")
        total += member.file_size
        if total > MAX_TOTAL_SIZE:
            raise ValueError("expanded DOCX package is too large")
        if (
            member.file_size > 1_000_000
            and member.compress_size > 0
            and member.file_size / member.compress_size > MAX_COMPRESSION_RATIO
        ):
            raise ValueError(f"suspicious ZIP compression ratio: {member.filename}")


def _remove(element) -> None:
    parent = element.getparent()
    if parent is not None:
        parent.remove(element)


def _unwrap(element) -> None:
    parent = element.getparent()
    if parent is None:
        return
    index = parent.index(element)
    children = list(element)
    for child in children:
        element.remove(child)
        parent.insert(index, child)
        index += 1
    tail = element.tail
    parent.remove(element)
    if tail:
        if index:
            previous = parent[index - 1]
            previous.tail = (previous.tail or "") + tail
        else:
            parent.text = (parent.text or "") + tail


def _nearest_ancestor(element, tag: str):
    current = element.getparent()
    while current is not None:
        if current.tag == tag:
            return current
        current = current.getparent()
    return None


def _accept_tree(root) -> int:
    count = 0

    # A deletion marker in row properties deletes the complete table row.
    for deletion in list(root.iter(f"{W}del")):
        if deletion.getparent() is not None and deletion.getparent().tag == f"{W}trPr":
            row = _nearest_ancestor(deletion, f"{W}tr")
            if row is not None:
                _remove(row)
                count += 1

    # A deleted table cell is removed; an inserted cell is kept and unmarked.
    for marker in list(root.iter(f"{W}cellDel")):
        cell = _nearest_ancestor(marker, f"{W}tc")
        if cell is not None:
            _remove(cell)
            count += 1
    for marker in list(root.iter(f"{W}cellIns")):
        _remove(marker)
        count += 1

    for deletion_tag in (f"{W}del", f"{W}moveFrom"):
        for element in list(root.iter(deletion_tag)):
            _remove(element)
            count += 1

    for insertion_tag in (f"{W}ins", f"{W}moveTo"):
        for element in list(root.iter(insertion_tag)):
            # Row insertion markers live inside properties and have no content.
            if element.getparent() is not None and element.getparent().tag == f"{W}trPr":
                _remove(element)
            else:
                _unwrap(element)
            count += 1

    for tag in PROPERTY_CHANGES | RANGE_MARKERS:
        for element in list(root.iter(tag)):
            _remove(element)
            count += 1

    unsupported = sorted(
        {etree.QName(element).localname for element in root.iter() if element.tag in TRACKED_TAGS}
    )
    if unsupported:
        raise ValueError("unsupported tracked-change markup remains: " + ", ".join(unsupported))
    return count


def _process_xml(data: bytes) -> tuple[bytes, int]:
    parser = etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        load_dtd=False,
        huge_tree=False,
        remove_blank_text=False,
    )
    root = etree.fromstring(data, parser=parser)
    count = _accept_tree(root)
    if count == 0:
        return data, 0
    return (
        etree.tostring(
            root,
            encoding="UTF-8",
            xml_declaration=True,
            standalone=None,
        ),
        count,
    )


def accept_changes(
    file: Path = typer.Argument(..., help="DOCX containing tracked changes."),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output DOCX path."),
    output_json: bool = typer.Option(False, "--json", help="Output a structured result."),
) -> None:
    """Accept text, move, formatting, row, and cell revisions transactionally."""
    require_file(file, ".docx")
    output_path = output or file
    accepted = 0
    try:
        with atomic_output(output_path) as temporary:
            with (
                zipfile.ZipFile(file, "r") as source,
                zipfile.ZipFile(temporary, "w") as destination,
            ):
                _validate_archive(source)
                destination.comment = source.comment
                for member in source.infolist():
                    data = source.read(member)
                    if member.filename.startswith("word/") and member.filename.endswith(".xml"):
                        data, count = _process_xml(data)
                        accepted += count
                    destination.writestr(member, data)
            Document(str(temporary))
    except typer.Exit:
        raise
    except Exception as exc:
        typer.echo(f"Error: cannot accept tracked changes: {exc}", err=True)
        raise typer.Exit(code=1)

    result_data = {"file": output_path.name, "accepted": accepted, "written": True}
    if output_json:
        typer.echo(json.dumps(result_data, indent=2))
    else:
        typer.echo(f"Accepted: {accepted} tracked changes in {output_path.name}")
