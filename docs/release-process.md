# Release process

Releases are automated from `vMAJOR.MINOR.PATCH` tags whose version must match
`docx_tool.__version__`.

1. Make `main` green. Promote the Unreleased changelog section to the new
   version with its release date, and point the `[Unreleased]` link at
   `compare/vPREVIOUS...HEAD` once a tag exists.
2. Run `make release-check`.
3. Create and push the release tag.
4. The workflow rebuilds the wheel and sdist, generates an SPDX SBOM, creates
   GitHub/Sigstore provenance and SBOM attestations, and attaches everything to
   the GitHub release.
5. Verify an artifact with
   `gh attestation verify <artifact> --repo evrenverse/docx-tool`.

Never reuse or move a published tag. Correct a failed public release with a
new patch version.
