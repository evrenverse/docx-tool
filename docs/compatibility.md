# Compatibility

| Area | Supported |
| --- | --- |
| Python | 3.12, 3.13, 3.14 |
| Operating systems | Linux, macOS, Windows |
| Document format | `.docx` OOXML packages |
| Optional integration | LibreOffice for `convert` and `export-pdf` |
| Package installation | PyPI or a reviewed Git checkout through `uv tool` |

CI tests all supported Python minors and all three operating systems. The
primary Linux job installs LibreOffice and runs formatting, linting, mypy,
branch-coverage enforcement, the agent eval, package build, and metadata check.

All document addresses are one-based. Legacy `.doc` is input only through
LibreOffice conversion. Encrypted documents, creation of tracked changes,
comments on arbitrary run ranges, and perfect preservation of all proprietary
Word extensions are not promised.
