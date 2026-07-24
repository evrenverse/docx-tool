# Threat model

## Assets

- DOCX confidentiality, integrity, signatures, and revision intent.
- Files available to the invoking user.
- Predictable agent output and host availability.

## Trust boundaries

DOCX input is an untrusted ZIP/XML package. `python-docx`, lxml, and Python's
ZIP/XML stack are parser trust boundaries. LibreOffice joins the trusted
computing base only for conversion and PDF export.

## Main threats and controls

| Threat | Control |
| --- | --- |
| ZIP bombs, duplicate members, hostile XML | Compressed/expanded-size, ratio, duplicate-name, and entity-resolution guards |
| Unsupported revision mutation | Guarded whitelist; abort while unsupported markup remains |
| Invalidating a document signature | Signed packages are detected and refused |
| Partial or corrupt output | Prevalidation, temporary output, reopen check, sync, atomic replace |
| Context flooding | Bounded paragraph/table/cell reads and explicit large-read confirmation |
| LibreOffice profile or macro side effects | Private temporary profile; no generated macros or native shims |
| Dependency compromise | Lockfile, Dependabot, dependency review, CodeQL, pip-audit, pinned Actions |
| Release substitution | SPDX SBOM, Sigstore/GitHub attestations |
| Accidental disclosure | No telemetry/runtime network; synthetic fixtures and issue policy |

## Out of scope

The CLI is not a malware sandbox, full Word rendering engine, review-grade
redlining author, or promise of lossless preservation for every proprietary
OOXML extension. Use an OS sandbox for hostile files and visually inspect
high-value output in a compatible office application.

Report vulnerabilities through [SECURITY.md](../SECURITY.md).
