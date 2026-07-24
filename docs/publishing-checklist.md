# Public publishing checklist

Repository files are only half of a professional release. Before announcing:

- Set the description to “Agent-friendly CLI for safe DOCX inspection and
  transactional editing” and add topics: `docx`, `cli`, `ai-agents`,
  `agent-tools`, `agent-skill`, `python`, `automation`.
- Upload `assets/social-preview.png` as the GitHub social preview.
- Enable issues, private vulnerability reporting, secret scanning, push
  protection, Dependabot alerts, and automatic security updates.
- Keep the `main` ruleset requiring CI, CodeQL, dependency review, conversation
  resolution, linear history, and no force pushes or deletions. It asks for a
  pull request but zero approvals, because a sole maintainer cannot approve
  their own; repository admins may bypass it for release-blocking fixes.
- Confirm the release wheel contains the JSON schemas and that its GitHub
  attestations verify.
