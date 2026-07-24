# CLI reference

Use `docx-tool <command> --help` as the authoritative option reference. All
document addresses are one-based.

## Agent discovery

```bash
docx-tool capabilities --json
docx-tool doctor --json
docx-tool doctor --json --require libreoffice
docx-tool schema
docx-tool schema batch
docx-tool version --json
```

Use bundled schemas instead of inferring structured input. The contract reports
hard input limits and whether each command mutates files.

## Inspect

```bash
docx-tool info document.docx --json
docx-tool find document.docx "Project owner" --json
docx-tool read document.docx --paragraphs 2,5 --json
docx-tool read document.docx --table 1 --cells 1:1,2:3 --json
```

## Modify

```bash
docx-tool write document.docx changes.json --output result.docx --json
docx-tool comment result.docx --paragraph 2 --text "Verify this." --author Reviewer
docx-tool accept-changes reviewed.docx --output accepted.docx --json
```

`write` takes a JSON array with operation types `replace`, `paragraph`,
`table_cell`, `checkbox`, `content_control`, and `image`. Run
`docx-tool schema batch` for the schema. Any failure prevents all output.

## Convert

```bash
docx-tool convert legacy.doc --output modern.docx
docx-tool export-pdf modern.docx --output modern.pdf
```

These two commands require LibreOffice. Core inspection and editing do not.
