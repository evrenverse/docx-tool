# Changelog

All notable changes are documented here. This project follows Semantic
Versioning and keeps an [Unreleased] section.

## [Unreleased]

- Provide an independent implementation on public `python-docx` and `lxml`
  APIs, without vendored schemas, macros, or native shims.
- Add bounded reads, transactional edit batches, atomic output, and signature
  protection.
- Add independently implemented, guarded tracked-change acceptance.
- Add an Agent Skill and Codex plugin manifest.
- Upgrade and audit all dependencies.
- Add a versioned, machine-readable Agent Contract with capabilities, doctor,
  version, and bundled JSON Schema commands.
- Add explicit document and JSON/batch limits, property tests, mypy, branch
  coverage enforcement, and a real CLI locate-edit-verify eval.
- Add CI, CodeQL, dependency review, OpenSSF Scorecard, SBOMs, and provenance
  attestations with commit-pinned GitHub Actions.
- Add architecture, threat-model, compatibility, release, support, governance,
  and public-publishing documentation.

[Unreleased]: https://github.com/evrenverse/docx-tool/commits/main
