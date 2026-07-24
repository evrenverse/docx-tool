# Security policy

## Supported versions

Security fixes are provided for the latest released version.

## Report a vulnerability

Use GitHub's private vulnerability reporting for this repository. Do not open
a public issue containing exploit details or sensitive documents. Include the
affected version, impact, reproduction steps, and any suggested mitigation.

## Trust model

DOCX files are attacker-controlled ZIP/XML packages. Run untrusted documents
with the least filesystem access practical and keep locked dependencies
current. `accept-changes` rejects encrypted members, duplicate names,
oversized expanded packages, suspicious compression ratios, digitally signed
documents, external-entity resolution, and unsupported remaining revisions.

Other commands use `python-docx`, whose parser is part of the trusted computing
base. `convert` and `export-pdf` additionally trust the installed LibreOffice
binary; it runs with a private throwaway profile and no generated macros or
native preload shims.

Mutating commands validate first and atomically publish a reopened output.
They refuse digitally signed DOCX packages rather than silently invalidating
the signature. The CLI has no telemetry and performs no runtime network
requests.
