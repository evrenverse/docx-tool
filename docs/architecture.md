# Architecture

`docx-tool` is a local Python CLI with no server, telemetry, macros, native
shim, or runtime network dependency.

```text
agent or developer
        |
        v
Typer command layer  ------> JSON stdout / diagnostics stderr
        |
        v
validation + one-based bounded addressing
        |
        +--> python-docx for document operations
        +--> guarded lxml/ZIP path for tracked-change acceptance
        |
        v
same-directory temporary file -> reopen/check -> fsync -> atomic replace
```

`src/docx_tool/cli.py` registers commands. `commands/common.py` owns shared
package, signature, input-size, and atomic-publication guards. `document.py`
owns document-level helpers. Command modules keep public behavior local.
Bundled schemas live in `src/docx_tool/schemas`; `evals` drives the real CLI
through a synthetic locate-edit-verify workflow.

Only `convert` and `export-pdf` spawn a process. They invoke local LibreOffice
with a new throwaway profile and no generated macros.

## Design constraints

- One independent tool for DOCX workflows.
- Machine-readable capability discovery before document access.
- One-based addresses across paragraphs, tables, rows, and columns.
- Bounded inputs, transactional edits, and atomic publication.
- No organization-specific services, paths, vendored schema sets, or
  sibling-tool dependencies.
