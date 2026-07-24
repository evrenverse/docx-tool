# Contributing

Issues and focused pull requests are welcome.

## Development

1. Install Python 3.12 or newer and uv. `make check` also needs LibreOffice
   (`soffice` or `libreoffice` on `PATH`, package `libreoffice-writer`); the
   conversion tests skip without it and the coverage gate then fails.
2. Create a branch and add synthetic tests for behavior changes.
3. Run the same local gate used by CI:

   ```bash
   make install
   make check
   make build
   make audit
   ```

4. Update `README.md`, the bundled skill, and `CHANGELOG.md` for user-facing
   changes.

Preserve stable JSON fields, bounded output, one-based addresses,
all-or-nothing operations, and atomic writes. Do not vendor external schema
sets or copy code from source-available repositories. Fixtures must be
synthetic or redistributable and contain no personal, customer, or company
data.

## Pull requests

Keep changes focused and explain the user or agent workflow they improve. Add
tests for behavior, error paths, and limits. A contract change also needs
updated schemas and eval coverage. Prefer conventional commit subjects such as
`feat:`, `fix:`, `docs:`, `test:`, or `chore:`.

By participating, you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
