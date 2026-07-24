# Release process

Releases are automated from `vMAJOR.MINOR.PATCH` tags whose version must match
`docx_tool.__version__`.

1. Make `main` green. Promote the Unreleased changelog section to the new
   version with its release date, and point the `[Unreleased]` link at
   `compare/vPREVIOUS...HEAD` once a tag exists.
2. Run `make release-check`.
3. Configure the `pypi` GitHub environment and a PyPI Trusted Publisher for
   `evrenverse/docx-tool` and `.github/workflows/release.yml`.
4. Create and push the release tag.
5. The workflow rebuilds and checks the wheel and sdist, generates an SPDX
   SBOM, creates GitHub/Sigstore provenance and SBOM attestations, publishes to
   PyPI without a long-lived token, and creates the GitHub release.
6. Verify an artifact with
   `gh attestation verify <artifact> --repo evrenverse/docx-tool`.

Never reuse or move a published tag or PyPI version. Correct a failed public
release with a new patch version.
