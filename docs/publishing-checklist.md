# Public publishing checklist

Repository files are only half of a professional release. Before announcing:

- Set the description to “Agent-friendly CLI for safe DOCX inspection and
  transactional editing” and add topics: `docx`, `cli`, `ai-agents`,
  `agent-tools`, `agent-skill`, `python`, `automation`.
- Upload `assets/social-preview.png` as the GitHub social preview.
- Enable issues, private vulnerability reporting, secret scanning, push
  protection, Dependabot alerts, and automatic security updates.
- Add a `main` ruleset requiring CI, CodeQL, dependency review, conversation
  resolution, linear history, and no force pushes or deletions.
- Require approval for changes matching `CODEOWNERS`. As the only
  maintainer you cannot approve your own pull requests, so either add
  yourself to the ruleset bypass list or push release-blocking fixes to
  `main` directly.
- Create the PyPI project/environment and configure Trusted Publishing before
  pushing `v0.1.0`.
- Confirm the published wheel contains the JSON schemas and the PyPI and GitHub
  attestations verify.
