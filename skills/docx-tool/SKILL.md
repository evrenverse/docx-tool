---
name: docx-tool
description: Inspect, search, read, edit, comment, accept supported tracked changes in, convert, and export Microsoft Word DOCX documents with the docx-tool CLI. Use when an agent must work with DOCX paragraphs, tables, cells, content controls, checkboxes, comments, images, or revisions while keeping reads bounded, using one-based addresses, applying edits transactionally, and verifying the output.
---

# DOCX Tool

Use `docx-tool` instead of writing a one-off Word-processing script.

## Prepare

1. Run `command -v docx-tool`.
2. If missing and this repository is available, run `uv tool install .`.
   Otherwise run `uv tool install git+https://github.com/evrenverse/docx-tool`.
3. Run `docx-tool --version`.
4. Run `docx-tool capabilities --json` and `docx-tool doctor --json`.
5. Use `docx-tool schema <name>` when constructing structured input.
6. Work on a copy unless the user explicitly wants an in-place edit.

## Inspect before editing

1. Run `docx-tool info <file> --json`.
2. Use `find`, `read --paragraphs`, or `read --table --cells`.
3. Remember that all DOCX addresses are one-based.
4. Avoid an unscoped full read when bounded content is enough.

## Edit and verify

1. Prefer one `write` or `batch` operation for related edits.
2. Treat any failed operation as a failed transaction; the CLI writes nothing.
3. Read every changed paragraph or table cell back with `--json`.
4. Report the output path and any round-trip limitation.

Use `comment` only for an entire ordinary body paragraph. Inspect revisions
before `accept-changes`; that command aborts if unsupported change markup
remains. Do not use this CLI to rewrite a digitally signed DOCX.

Read [references/cli.md](references/cli.md) when exact syntax, operation
schemas, or LibreOffice requirements are needed.
