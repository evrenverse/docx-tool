# docx-tool

[![CI](https://github.com/evrenverse/docx-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/evrenverse/docx-tool/actions/workflows/ci.yml)
[![CodeQL](https://github.com/evrenverse/docx-tool/actions/workflows/codeql.yml/badge.svg)](https://github.com/evrenverse/docx-tool/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/evrenverse/docx-tool/badge)](https://scorecard.dev/viewer/?uri=github.com/evrenverse/docx-tool)
[![PyPI](https://img.shields.io/pypi/v/docx-tool.svg)](https://pypi.org/project/docx-tool/)
[![Python](https://img.shields.io/pypi/pyversions/docx-tool.svg)](https://pypi.org/project/docx-tool/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An agent-friendly CLI for inspecting and editing `.docx` documents. It offers
bounded reads, structured JSON, one-based document addresses, validated
all-or-nothing edit batches, comments through `python-docx`, and crash-safe
atomic writes.

The repository is also a skills-only Codex plugin. Its portable Agent Skill is
under [`skills/docx-tool`](skills/docx-tool).

## Why agent-native

This is not a thin wrapper branded for AI. The executable exposes a versioned,
machine-readable contract; uses consistent one-based addresses; keeps reads
bounded; separates JSON stdout from diagnostics; limits document expansion and
batch input; publishes mutations atomically; and ships a synthetic
locate-edit-verify eval that drives the real CLI. An agent can discover
capabilities without opening a user document:

```bash
docx-tool capabilities --json
docx-tool doctor --json
docx-tool schema batch
docx-tool version --json
```

This is an independent implementation built on public `python-docx` and `lxml`
APIs. It does not vendor OOXML schemas, office macros, native shims, or code
from other document-skill repositories.

## Give this repository to an agent

Copy this prompt:

> Inspect https://github.com/evrenverse/docx-tool and follow `AGENTS.md`.
> Install `docx-tool`, verify it with `docx-tool --version`, install the bundled
> `docx-tool` skill for this project, then use the CLI instead of writing a
> one-off Word-processing script.

## Install

With [uv](https://docs.astral.sh/uv/):

```bash
uv tool install docx-tool
docx-tool --version
```

Directly from GitHub before the first PyPI release:

```bash
uv tool install git+https://github.com/evrenverse/docx-tool
```

From a clone:

```bash
uv sync --all-groups --locked
uv run docx-tool --version
uv run pytest
```

Python 3.12 or newer is required. Only `convert` and `export-pdf` require
LibreOffice (`soffice` or `libreoffice`) on `PATH`.

## Install the Agent Skill

For a project-local Agent Skills installation:

```bash
mkdir -p .agents/skills
cp -R skills/docx-tool .agents/skills/docx-tool
```

Codex can also load the repository as a skills-only plugin because
`.codex-plugin/plugin.json` is included. Claude Code users can copy the same
folder to `.claude/skills/docx-tool`.

## Quick start

```bash
# Inspect without dumping document content
docx-tool info report.docx --json

# Find and read bounded content
docx-tool find report.docx "Project owner" --json
docx-tool read report.docx --paragraphs 2,5 --json
docx-tool read report.docx --table 1 --cells 1:1,2:3 --json

# Apply a transactional batch and verify it
docx-tool write report.docx changes.json --output updated.docx --json
docx-tool read updated.docx --paragraphs 2 --table 1 --cells 2:3 --json

# Add a comment to an entire body paragraph
docx-tool comment updated.docx \
  --paragraph 2 \
  --text "Please verify this value." \
  --author "Reviewer"

# Accept supported tracked changes
docx-tool accept-changes reviewed.docx --output accepted.docx --json

# Optional LibreOffice conversions
docx-tool convert legacy.doc --output modern.docx
docx-tool export-pdf modern.docx --output modern.pdf
```

Commands:

| Command | Purpose |
| --- | --- |
| `info` | Summarize paragraphs, tables, images, fields, comments, and revisions |
| `find` | Locate body, table, field, and comment text |
| `read` | Read selected paragraphs, tables, cells, fields, comments, and revisions |
| `write` | Apply a validated JSON edit transaction |
| `batch` | Alias for `write` |
| `comment` | Comment an entire body paragraph |
| `accept-changes` | Accept supported OOXML revisions without macros |
| `convert` | Convert legacy `.doc` to `.docx` through LibreOffice |
| `export-pdf` | Export `.docx` to PDF through LibreOffice |
| `capabilities` | Print the versioned agent contract |
| `doctor` | Check runtime and optional dependencies |
| `schema` | List or print bundled JSON Schemas |
| `version` | Print tool and contract versions |

Run `docx-tool <command> --help` for complete syntax. Paragraph, table, row,
and column addresses are all one-based.

## Write operation schema

`write` accepts a JSON array. If any operation is invalid or cannot be applied,
the command exits nonzero and writes nothing.

```json
[
  {
    "type": "replace",
    "search": "Old text",
    "value": "New text"
  },
  {
    "type": "paragraph",
    "index": 2,
    "value": "Replacement paragraph"
  },
  {
    "type": "table_cell",
    "table": 1,
    "row": 2,
    "column": 3,
    "value": "42"
  },
  {
    "type": "checkbox",
    "id": "Approved",
    "checked": true
  },
  {
    "type": "content_control",
    "id": "ProjectName",
    "value": "Public Project"
  },
  {
    "type": "image",
    "search": "[[LOGO]]",
    "image": "logo.png",
    "width_inches": 2
  }
]
```

Replacement text inherits formatting from the first matched run. Replacements
cover ordinary body and table-cell runs, not headers, footers, hyperlinks, or
text inside tracked revisions.

## Tracked changes

`read --json` exposes insertion, deletion, and move summaries. The
`accept-changes` command supports text insertions/deletions, moves, formatting
changes, row deletion/insertion markers, and cell insertion/deletion markers.
It aborts transactionally when unsupported revision markup such as
`cellMerge` remains.

The CLI intentionally does not create tracked changes. Use Word or LibreOffice
when review-grade redlining semantics are required.

## Safe automation contract

- JSON goes to stdout; diagnostics go to stderr.
- All document addresses are one-based.
- Large unscoped reads require `--confirm-large`.
- Edit batches are all-or-nothing.
- Outputs are reopened for validation, synced, and atomically published.
- Digitally signed DOCX files are not rewritten.
- LibreOffice conversions use a private, throwaway user profile and no macros.
- The tool has no telemetry and performs no runtime network requests.

`python-docx` preserves many unknown package parts but cannot promise lossless
round-tripping of every Word extension. Keep an untouched copy and visually
review important output.

## Development

```bash
make install
make check
```

The quality gate includes formatting, linting, mypy, branch coverage, package
build, and the real CLI agent eval. CI additionally tests Python 3.12–3.14 on
Linux with and without LibreOffice, known vulnerabilities, CodeQL, and
dependency changes.

## Project documentation

- [Architecture](docs/architecture.md)
- [Agent contract](docs/agent-contract.md)
- [Threat model](docs/threat-model.md)
- [Compatibility](docs/compatibility.md)
- [Release process](docs/release-process.md)
- [Contributing](CONTRIBUTING.md), [security](SECURITY.md), and
  [support](SUPPORT.md)

## License

[MIT](LICENSE)
