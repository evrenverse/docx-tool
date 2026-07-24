# Agent setup

This repository is an independent public Python CLI. Do not install unrelated
document tools when the task only concerns DOCX files.

## Install for use

1. Inspect `README.md`, `SECURITY.md`, and `pyproject.toml`.
2. Install from the repository (this tool is not published to PyPI):

   ```bash
   uv tool install git+https://github.com/evrenverse/docx-tool
   docx-tool --version
   ```

3. To install a reviewed local checkout instead, run `uv tool install .`.
4. For development, run `uv sync --all-groups --locked` and `make check`.
5. Install the project skill only when requested:

   ```bash
   mkdir -p .agents/skills
   cp -R skills/docx-tool .agents/skills/docx-tool
   ```

6. Run `docx-tool capabilities --json` and `docx-tool doctor --json` before
   choosing a workflow. Use `docx-tool schema <name>` instead of guessing
   structured input.
7. Inspect first, make a backup, edit transactionally, and verify with a scoped
   read.

## Contributing

Keep stdout machine-readable, stderr diagnostic, addresses one-based, and
writes atomic and all-or-nothing. Do not add telemetry, office macros, native
runtime shims, vendored schemas, organization-specific workflows, or runtime
dependencies on sibling repositories.

Run `make check`, `make build`, and the dependency audit before submitting.
User-visible contract changes must update schemas, tests, the eval, README,
skill, and changelog together.
