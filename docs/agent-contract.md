# Agent contract

Contract version `1` makes the CLI self-describing:

```bash
docx-tool capabilities --json
docx-tool doctor --json
docx-tool schema
docx-tool schema batch
docx-tool version --json
```

`capabilities` reports commands, mutation behavior, numbering, optional
dependencies, safety properties, bundled schemas, and hard limits. `doctor`
performs read-only runtime checks and can require LibreOffice with
`--require libreoffice`. `schema` prints JSON Schema locally.

## Stable conventions

- Contract and schema versions are independent from the package version.
- JSON is written to stdout; diagnostics and warnings go to stderr.
- Paragraphs, tables, rows, and columns are one-based.
- Success exits `0`. A no-match, invalid document operation, or rejected edit
  exits `1`; CLI usage, resource-policy, and failed explicitly required
  dependency checks exit `2`.
- A write batch is all-or-nothing. Agents should inspect, keep an original,
  mutate, and read every changed address back.
- Digitally signed packages are refused rather than silently invalidated.

Backward-incompatible changes require a new contract major version. Additive
JSON fields and schemas are allowed in version `1`.

Schemas ship inside the wheel under `docx_tool.schemas`. Portable agent
guidance is in `skills/docx-tool`.
